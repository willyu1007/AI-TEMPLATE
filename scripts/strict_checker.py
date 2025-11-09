#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
strict_checker.py - Strict Mode Checker for Health Checks

Implements strict/blocker-level checks for production readiness:
- Blocker checks (zero tolerance)
- Strict thresholds (higher standards)
- Additional code quality checks

Created: 2025-11-09 (Phase 14.2+)
"""

import sys
import re
import yaml
from pathlib import Path
from typing import List, Dict, Any, Tuple
import subprocess

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Import Issue model
from issue_model import Issue, create_issue


class StrictChecker:
    """
    Strict Mode Checker for production readiness verification
    
    Features:
    - Blocker checks (BLOCKER-001 to BLOCKER-004)
    - Strict thresholds application
    - Additional code quality checks
    """
    
    def __init__(self, config_path: str = 'scripts/strict_thresholds.yaml', repo_root: Path = None):
        """
        Initialize strict checker
        
        Args:
            config_path: Path to strict thresholds config
            repo_root: Repository root directory
        """
        self.config_path = Path(config_path)
        self.repo_root = repo_root or Path(__file__).parent.parent
        self.config = self._load_config()
        self.blocker_issues: List[Issue] = []
    
    def _load_config(self) -> Dict[str, Any]:
        """Load strict thresholds configuration"""
        if not self.config_path.exists():
            print(f"⚠️ Strict config not found: {self.config_path}, using defaults")
            return {}
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def run_blocker_checks(self) -> List[Issue]:
        """
        Run all blocker-level checks
        
        Returns:
            List of blocker issues (empty if all pass)
        """
        if not self.config.get('blocker_checks'):
            return []
        
        print("🔥 Running BLOCKER checks (zero tolerance)...")
        
        for check_config in self.config['blocker_checks']:
            rule_id = check_config['rule']
            
            if rule_id == 'BLOCKER-001':
                issues = self._check_secrets(check_config)
            elif rule_id == 'BLOCKER-002':
                issues = self._check_circular_deps(check_config)
            elif rule_id == 'BLOCKER-003':
                issues = self._check_critical_docs(check_config)
            elif rule_id == 'BLOCKER-004':
                issues = self._check_license(check_config)
            else:
                issues = []
            
            self.blocker_issues.extend(issues)
            
            if issues:
                print(f"  🔴 {rule_id}: {check_config['name']} - {len(issues)} violation(s)")
            else:
                print(f"  ✅ {rule_id}: {check_config['name']} - PASS")
        
        return self.blocker_issues
    
    def _check_secrets(self, config: Dict) -> List[Issue]:
        """
        Check for secret leakage (BLOCKER-001)
        
        Scans code files for hardcoded secrets/passwords/keys
        """
        issues = []
        patterns = config.get('patterns', [])
        excludes = config.get('excludes', [])
        
        # File patterns to scan
        extensions = ['*.py', '*.yaml', '*.yml', '*.json', '*.env', '*.conf', '*.cfg']
        exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}
        
        for ext in extensions:
            for file_path in self.repo_root.rglob(ext):
                # Skip excluded directories
                if any(excluded in file_path.parts for excluded in exclude_dirs):
                    continue
                
                # Skip test files with example passwords
                if 'test' in file_path.name.lower() or 'example' in file_path.name.lower():
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    
                    for line_num, line in enumerate(lines, 1):
                        # Check each pattern
                        for pattern in patterns:
                            if re.search(pattern, line, re.IGNORECASE):
                                # Check excludes
                                is_excluded = any(re.search(exc, line, re.IGNORECASE) for exc in excludes)
                                if is_excluded:
                                    continue
                                
                                # Found a potential secret
                                relative_path = file_path.relative_to(self.repo_root)
                                context_before = lines[max(0, line_num-4):line_num-1]
                                context_after = lines[line_num:min(len(lines), line_num+3)]
                                
                                issues.append(create_issue(
                                    level="blocker",
                                    category="security",
                                    rule="BLOCKER-001",
                                    message=f"Potential secret detected: {pattern[:30]}...",
                                    file=str(relative_path),
                                    line=line_num,
                                    context_before=[l.rstrip() for l in context_before],
                                    context_after=[l.rstrip() for l in context_after],
                                    suggestion="Move sensitive data to environment variables or secrets management",
                                    fix_command="Use SECRET_KEY or AWS_SECRET_KEY env vars",
                                    reference="/doc/policies/security_details.md",
                                    estimated_time="15 minutes",
                                    priority=100,
                                    impact="Critical security risk - secrets exposed in code"
                                ))
                                break  # One issue per line
                
                except Exception as e:
                    print(f"  ⚠️ Error scanning {file_path}: {e}")
        
        return issues
    
    def _check_circular_deps(self, config: Dict) -> List[Issue]:
        """
        Check for circular dependencies (BLOCKER-002)
        
        Uses dag_check.py to detect circular dependencies
        """
        issues = []
        check_command = config.get('check_command', 'make dag_check')
        
        try:
            result = subprocess.run(
                check_command.split(),
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # If dag_check fails (exit code != 0), likely has circular deps
            if result.returncode != 0:
                # Parse output for details
                output = result.stdout + result.stderr
                
                issues.append(create_issue(
                    level="blocker",
                    category="architecture",
                    rule="BLOCKER-002",
                    message="Circular dependencies detected in module graph",
                    suggestion="Refactor modules to remove circular dependencies",
                    fix_command="Review doc/flows/dag.yaml and refactor module relationships",
                    reference="/doc/architecture/directory.md",
                    estimated_time="2 hours",
                    priority=100,
                    impact="Circular dependencies can cause import errors and tight coupling"
                ))
        
        except subprocess.TimeoutExpired:
            issues.append(create_issue(
                level="error",
                category="architecture",
                rule="BLOCKER-002",
                message="DAG check timed out (possibly complex circular dependency)",
                priority=90
            ))
        except Exception as e:
            print(f"  ⚠️ Error running dag_check: {e}")
        
        return issues
    
    def _check_critical_docs(self, config: Dict) -> List[Issue]:
        """
        Check for missing critical documentation (BLOCKER-003)
        
        Verifies presence of required documentation files
        """
        issues = []
        required = config.get('required_docs', {})
        
        # Check repo-level docs
        for doc_file in required.get('repo_level', []):
            doc_path = self.repo_root / doc_file
            if not doc_path.exists():
                issues.append(create_issue(
                    level="blocker",
                    category="documentation",
                    rule="BLOCKER-003",
                    message=f"Missing critical document: {doc_file}",
                    file=doc_file,
                    suggestion=f"Create {doc_file} using appropriate template",
                    reference="/doc/init/PROJECT_INIT_GUIDE.md",
                    estimated_time="1 hour",
                    priority=95,
                    impact="Critical documentation missing - affects project understanding"
                ))
        
        # Check module-level docs
        modules_dir = self.repo_root / "modules"
        if modules_dir.exists():
            for module_dir in modules_dir.iterdir():
                if not module_dir.is_dir() or module_dir.name.startswith('.'):
                    continue
                
                for doc_file in required.get('module_level', []):
                    doc_path = module_dir / doc_file
                    if not doc_path.exists():
                        rel_path = doc_path.relative_to(self.repo_root)
                        issues.append(create_issue(
                            level="error",  # Module docs are errors, not blockers
                            category="documentation",
                            rule="DOC-001",
                            message=f"Module {module_dir.name} missing: {doc_file}",
                            file=str(rel_path),
                            suggestion=f"Create {doc_file} for module {module_dir.name}",
                            fix_command=f"make module_doc_gen MODULE={module_dir.name}",
                            reference="/doc/modules/MODULE_INIT_GUIDE.md",
                            estimated_time="30 minutes",
                            priority=70
                        ))
        
        return issues
    
    def _check_license(self, config: Dict) -> List[Issue]:
        """
        Check for license compliance (BLOCKER-004)
        
        Verifies LICENSE file exists and is compatible
        """
        issues = []
        license_file = self.repo_root / "LICENSE"
        
        if not license_file.exists():
            issues.append(create_issue(
                level="blocker",
                category="operations",
                rule="BLOCKER-004",
                message="LICENSE file missing",
                file="LICENSE",
                suggestion="Add LICENSE file with approved license (MIT, Apache-2.0, BSD-3-Clause)",
                reference="/doc/policies/safety.md",
                estimated_time="5 minutes",
                priority=100,
                impact="Missing license affects legal compliance and usage rights"
            ))
        else:
            # Check if license is compatible
            allowed_licenses = config.get('allowed_licenses', [])
            if allowed_licenses:
                try:
                    content = license_file.read_text()
                    # Simple check - look for license keywords
                    found_license = None
                    for lic in allowed_licenses:
                        if lic.upper() in content.upper():
                            found_license = lic
                            break
                    
                    if not found_license:
                        issues.append(create_issue(
                            level="warning",
                            category="operations",
                            rule="OPS-001",
                            message=f"License may not be compatible (allowed: {', '.join(allowed_licenses)})",
                            file="LICENSE",
                            suggestion="Verify license compatibility",
                            priority=60
                        ))
                except Exception as e:
                    print(f"  ⚠️ Error reading LICENSE: {e}")
        
        return issues
    
    def apply_strict_thresholds(self, metric_name: str, current_value: float) -> Tuple[float, bool, int]:
        """
        Apply strict thresholds to a metric
        
        Args:
            metric_name: Name of metric (e.g., "test_coverage")
            current_value: Current metric value
            
        Returns:
            Tuple of (strict_threshold, passed, penalty_points)
        """
        thresholds = self.config.get('strict_thresholds', {}).get(metric_name)
        
        if not thresholds:
            # No strict threshold defined, use current
            return current_value, True, 0
        
        strict_value = thresholds.get('strict')
        priority = thresholds.get('priority', 'medium')
        
        # Check if passed strict threshold
        passed = current_value >= strict_value
        
        # Calculate penalty (if not passed)
        penalty = 0
        if not passed:
            enforcement = self.config.get('enforcement', {}).get('strict', {})
            penalty = enforcement.get('penalty_per_violation', 5)
            
            # Adjust penalty by priority
            priority_multipliers = {
                'critical': 2.0,
                'high': 1.5,
                'medium': 1.0,
                'low': 0.5
            }
            penalty = int(penalty * priority_multipliers.get(priority, 1.0))
        
        return strict_value, passed, penalty
    
    def has_blockers(self) -> bool:
        """Check if there are any blocker issues"""
        return len(self.blocker_issues) > 0
    
    def get_blocker_summary(self) -> str:
        """Get summary of blocker issues"""
        if not self.blocker_issues:
            return "✅ No blocker issues found"
        
        summary = f"🔥 {len(self.blocker_issues)} BLOCKER ISSUE(S) FOUND:\n"
        for issue in self.blocker_issues:
            summary += f"  - [{issue.rule}] {issue.message}\n"
            if issue.file:
                summary += f"    File: {issue.file}\n"
        
        return summary


# Example usage and testing
if __name__ == '__main__':
    import os
    
    print("=== Strict Checker Test ===\n")
    
    # Create checker
    checker = StrictChecker()
    
    # Run blocker checks
    print("Running blocker checks...\n")
    blocker_issues = checker.run_blocker_checks()
    
    print(f"\n{checker.get_blocker_summary()}")
    
    # Test strict thresholds
    print("\n=== Testing Strict Thresholds ===\n")
    
    test_metrics = [
        ("test_coverage", 85.0),
        ("linter_pass_rate", 98.0),
        ("agent_md_lines", 380),
    ]
    
    for metric_name, current_value in test_metrics:
        strict_val, passed, penalty = checker.apply_strict_thresholds(metric_name, current_value)
        status = "✅ PASS" if passed else f"❌ FAIL (penalty: -{penalty}pts)"
        print(f"{metric_name}: {current_value} (strict: ≥{strict_val}) - {status}")
    
    print("\n✅ Strict checker test completed!")

