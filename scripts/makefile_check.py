#!/usr/bin/env python3
"""
Makefile Checker - Validates Makefile targets and dependencies

Purpose:
- Verify all targets have valid commands
- Check for undefined variables
- Detect circular dependencies
- Validate script references exist

Usage:
    python scripts/makefile_check.py
    make makefile_check
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class MakefileChecker:
    def __init__(self, makefile_path: Path):
        self.makefile_path = makefile_path
        self.targets: Dict[str, List[str]] = {}  # target -> dependencies
        self.commands: Dict[str, List[str]] = {}  # target -> commands
        self.variables: Dict[str, str] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def parse(self) -> bool:
        """Parse Makefile"""
        try:
            with open(self.makefile_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            self.errors.append(f"Failed to read Makefile: {e}")
            return False
            
        current_target = None
        
        for line_num, line in enumerate(lines, 1):
            # Skip comments and empty lines
            if line.strip().startswith('#') or not line.strip():
                continue
                
            # Variable definition
            if '=' in line and not line.startswith('\t'):
                var_match = re.match(r'^([A-Z_][A-Z0-9_]*)\s*[:?]?=\s*(.*)$', line.strip())
                if var_match:
                    var_name, var_value = var_match.groups()
                    self.variables[var_name] = var_value.strip()
                    
            # Target definition
            elif ':' in line and not line.startswith('\t'):
                target_match = re.match(r'^([a-z_][a-z0-9_]*)\s*:\s*(.*)$', line.strip())
                if target_match:
                    target_name, deps = target_match.groups()
                    current_target = target_name
                    self.targets[target_name] = deps.split() if deps else []
                    self.commands[target_name] = []
                    
            # Command
            elif line.startswith('\t') and current_target:
                cmd = line.strip()
                if cmd:  # Skip empty tab lines
                    self.commands[current_target].append(cmd)
                    
        return True
        
    def check_undefined_variables(self):
        """Check for undefined variables in commands"""
        var_pattern = re.compile(r'\$\(([A-Z_][A-Z0-9_]*)\)')
        
        for target, cmds in self.commands.items():
            for cmd in cmds:
                for var_match in var_pattern.finditer(cmd):
                    var_name = var_match.group(1)
                    # Skip built-in make variables
                    if var_name not in self.variables and var_name not in ['MAKE', 'MAKEFILE_LIST']:
                        self.warnings.append(
                            f"Target '{target}': Variable $({var_name}) may be undefined"
                        )
                        
    def check_script_references(self):
        """Check if referenced scripts exist"""
        script_dir = self.makefile_path.parent / 'scripts'
        
        for target, cmds in self.commands.items():
            for cmd in cmds:
                # Check Python scripts
                if 'python' in cmd.lower():
                    script_match = re.search(r'scripts/([a-z_]+\.py)', cmd)
                    if script_match:
                        script_file = script_dir / script_match.group(1)
                        if not script_file.exists():
                            self.errors.append(
                                f"Target '{target}': Script '{script_match.group(1)}' not found"
                            )
                            
                # Check shell scripts
                if 'bash' in cmd.lower() or '.sh' in cmd:
                    script_match = re.search(r'scripts/([a-z_]+\.sh)', cmd)
                    if script_match:
                        script_file = script_dir / script_match.group(1)
                        if not script_file.exists():
                            self.errors.append(
                                f"Target '{target}': Script '{script_match.group(1)}' not found"
                            )
                            
    def check_circular_dependencies(self):
        """Detect circular dependencies using DFS"""
        def has_cycle(target: str, visited: Set[str], rec_stack: Set[str]) -> bool:
            visited.add(target)
            rec_stack.add(target)
            
            for dep in self.targets.get(target, []):
                if dep not in visited:
                    if has_cycle(dep, visited, rec_stack):
                        return True
                elif dep in rec_stack:
                    self.errors.append(
                        f"Circular dependency detected: {target} -> {dep}"
                    )
                    return True
                    
            rec_stack.remove(target)
            return False
            
        visited = set()
        for target in self.targets:
            if target not in visited:
                has_cycle(target, visited, set())
                
    def check_missing_commands(self):
        """Check targets without commands (except .PHONY)"""
        for target, cmds in self.commands.items():
            if not cmds and target not in ['.PHONY', 'help', 'all']:
                # Check if it has dependencies (aggregator target)
                if not self.targets.get(target):
                    self.warnings.append(
                        f"Target '{target}' has no commands and no dependencies"
                    )
                    
    def check_phony_declaration(self):
        """Check if targets are declared in .PHONY"""
        # Common phony targets that should be declared
        phony_candidates = {t for t in self.targets if not t.startswith('.')}
        
        # Find .PHONY declaration
        phony_targets = set()
        if '.PHONY' in self.targets:
            phony_targets = set(self.targets['.PHONY'])
            
        # Warn about missing .PHONY declarations
        missing_phony = phony_candidates - phony_targets
        if missing_phony and len(missing_phony) < 10:  # Don't spam for large Makefiles
            for target in sorted(missing_phony):
                if target not in ['all', 'default']:
                    self.warnings.append(
                        f"Target '{target}' should be declared in .PHONY"
                    )
                    
    def run_checks(self) -> bool:
        """Run all checks"""
        if not self.parse():
            return False
            
        self.check_undefined_variables()
        self.check_script_references()
        self.check_circular_dependencies()
        self.check_missing_commands()
        # Skip phony check as it generates too many warnings
        # self.check_phony_declaration()
        
        return len(self.errors) == 0
        
    def report(self):
        """Print check results"""
        if self.errors:
            print("\n❌ Makefile Check Failed\n")
            print("Errors:")
            for error in self.errors:
                print(f"  - {error}")
                
        if self.warnings:
            print("\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  - {warning}")
                
        if not self.errors and not self.warnings:
            print("✅ Makefile check passed")
            print(f"   Targets: {len(self.targets)}")
            print(f"   Variables: {len(self.variables)}")
            

def main():
    """Main entry point"""
    repo_root = Path(__file__).parent.parent
    makefile_path = repo_root / 'Makefile'
    
    if not makefile_path.exists():
        print(f"❌ Makefile not found: {makefile_path}")
        return 1
        
    checker = MakefileChecker(makefile_path)
    success = checker.run_checks()
    checker.report()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())

