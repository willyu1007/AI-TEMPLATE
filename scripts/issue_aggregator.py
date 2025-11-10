#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
issue_aggregator.py - Issue Aggregation and Root Cause Analysis

Provides intelligent issue clustering and root cause analysis:
- Cluster similar issues by pattern
- Identify root causes affecting multiple issues
- Generate batch fix proposals
- Calculate improvement potential

Created: 2025-11-09 (Phase 14.2+)
"""

import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Import Issue model
from issue_model import Issue, IssueLevel, IssueCategory


@dataclass
class IssueCluster:
    """Cluster of similar issues"""
    name: str                    # Cluster name
    root_cause: str             # Root cause description
    affected_issues: List[Issue] = field(default_factory=list)
    impact_score: int = 0       # Total impact score
    fix_strategy: str = ""      # Proposed fix strategy


@dataclass
class RootCause:
    """Root cause analysis result"""
    id: str                     # Root cause ID (e.g., "RC-001")
    name: str                   # Short name
    description: str            # Detailed description
    affected_dimensions: List[str] = field(default_factory=list)
    affected_count: int = 0     # Number of affected issues
    fix_proposal: str = ""      # Fix proposal with commands
    expected_improvement: str = ""  # Expected score improvement
    estimated_time: str = ""    # Estimated fix time


class IssueAggregator:
    """
    Issue Aggregator for clustering and root cause analysis
    
    Features:
    - Cluster similar issues by pattern
    - Identify root causes
    - Generate batch fix proposals
    - Prioritize improvements
    """
    
    def __init__(self, issues: List[Issue]):
        """
        Initialize aggregator
        
        Args:
            issues: List of Issue objects
        """
        self.issues = issues
        self.clusters: List[IssueCluster] = []
        self.root_causes: List[RootCause] = []
    
    def cluster_similar_issues(self) -> List[IssueCluster]:
        """
        Cluster similar issues together
        
        Returns:
            List of IssueCluster objects
        """
        clusters = []
        
        # Cluster 1: Testing infrastructure issues
        test_issues = [
            i for i in self.issues 
            if any(keyword in i.message.lower() for keyword in ['test', 'coverage', 'pytest'])
        ]
        if test_issues:
            clusters.append(IssueCluster(
                name="",
                root_cause="Testing infrastructure not configured or insufficient",
                affected_issues=test_issues,
                impact_score=sum(i.priority for i in test_issues),
                fix_strategy="Setup pytest infrastructure with coverage tools"
            ))
        
        # Cluster 2: Documentation issues
        doc_issues = [
            i for i in self.issues
            if i.category == IssueCategory.DOCUMENTATION or 
            any(keyword in i.message.lower() for keyword in ['document', 'doc', 'readme', 'missing'])
        ]
        if doc_issues:
            clusters.append(IssueCluster(
                name="",
                root_cause="Module documentation templates missing or incomplete",
                affected_issues=doc_issues,
                impact_score=sum(i.priority for i in doc_issues),
                fix_strategy="Generate missing documentation using templates"
            ))
        
        # Cluster 3: Code quality issues
        quality_issues = [
            i for i in self.issues
            if i.category == IssueCategory.CODE_QUALITY and
            any(keyword in i.message.lower() for keyword in ['linter', 'complexity', 'type'])
        ]
        if quality_issues:
            clusters.append(IssueCluster(
                name="",
                root_cause="Code quality tools not configured or standards not met",
                affected_issues=quality_issues,
                impact_score=sum(i.priority for i in quality_issues),
                fix_strategy="Configure linters and refactor complex code"
            ))
        
        # Cluster 4: Security issues
        security_issues = [
            i for i in self.issues
            if i.category == IssueCategory.SECURITY or 'secret' in i.message.lower()
        ]
        if security_issues:
            clusters.append(IssueCluster(
                name="",
                root_cause="Secrets or credentials hardcoded in code",
                affected_issues=security_issues,
                impact_score=sum(i.priority for i in security_issues),
                fix_strategy="Move all secrets to environment variables"
            ))
        
        # Cluster 5: Architecture issues
        arch_issues = [
            i for i in self.issues
            if i.category == IssueCategory.ARCHITECTURE
        ]
        if arch_issues:
            clusters.append(IssueCluster(
                name="",
                root_cause="Module dependencies or architecture not optimal",
                affected_issues=arch_issues,
                impact_score=sum(i.priority for i in arch_issues),
                fix_strategy="Refactor module relationships"
            ))
        
        self.clusters = sorted(clusters, key=lambda x: x.impact_score, reverse=True)
        return self.clusters
    
    def analyze_root_causes(self) -> List[RootCause]:
        """
        Analyze root causes of issues
        
        Returns:
            List of RootCause objects
        """
        root_causes = []
        
        # Root Cause 1: Testing infrastructure missing
        test_related = [
            i for i in self.issues
            if any(kw in i.message.lower() for kw in ['test', 'coverage', 'pytest'])
        ]
        if len(test_related) >= 3:  # Significant impact
            root_causes.append(RootCause(
                id="RC-001",
                name="",
                description="No pytest or coverage tools configured, leading to zero test coverage",
                affected_dimensions=['code_quality', 'operations'],
                affected_count=len(test_related),
                fix_proposal="""
****:
```bash
# 1. 
pip install pytest pytest-cov pytest-mock

# 2. 
cat > pytest.ini << EOF
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --cov=modules --cov=scripts --cov-report=term-missing
EOF

# 3. 
make test_coverage
```

 {count} :
- {files}
                """.format(
                    count=len(test_related),
                    files="\n- ".join(set(i.file for i in test_related if i.file))[:500]
                ),
                expected_improvement="+15-20",
                estimated_time="1-2"
            ))
        
        # Root Cause 2: Module documentation incomplete
        doc_issues = [
            i for i in self.issues
            if i.category == IssueCategory.DOCUMENTATION and 'missing' in i.message.lower()
        ]
        if len(doc_issues) >= 2:
            affected_modules = set()
            for issue in doc_issues:
                if issue.file and 'modules/' in issue.file:
                    module = issue.file.split('modules/')[1].split('/')[0]
                    affected_modules.add(module)
            
            root_causes.append(RootCause(
                id="RC-002",
                name="",
                description=f"Modules missing standard documentation (affects {len(affected_modules)} module(s))",
                affected_dimensions=['documentation', 'ai_friendliness'],
                affected_count=len(doc_issues),
                fix_proposal=f"""
****:
```bash
# 
{chr(10).join([f"make module_doc_gen MODULE={m}" for m in sorted(affected_modules)])}
```

:
- RUNBOOK.md ()
- BUGS.md ()
- PROGRESS.md ()
- TEST_PLAN.md ()
                """,
                expected_improvement="+5-8",
                estimated_time="30-1"
            ))
        
        # Root Cause 3: Linter/code quality tools not configured
        linter_issues = [
            i for i in self.issues
            if 'linter' in i.message.lower() or 'complexity' in i.message.lower()
        ]
        if len(linter_issues) >= 2:
            root_causes.append(RootCause(
                id="RC-003",
                name="",
                description="Linters and complexity tools not properly configured",
                affected_dimensions=['code_quality'],
                affected_count=len(linter_issues),
                fix_proposal="""
****:
```bash
# 1. 
pip install pylint flake8 radon mypy

# 2. 
cat > .pylintrc << EOF
[MASTER]
max-line-length=120
EOF

# 3. 
make python_scripts_lint
make complexity_check
```
                """,
                expected_improvement="+8-10",
                estimated_time="1-1.5"
            ))
        
        # Root Cause 4: Secrets not externalized
        secret_issues = [
            i for i in self.issues
            if 'secret' in i.message.lower() or 'password' in i.message.lower()
        ]
        if len(secret_issues) >= 1:
            root_causes.append(RootCause(
                id="RC-004",
                name="",
                description="Secrets, passwords, or tokens hardcoded in configuration",
                affected_dimensions=['security', 'operations'],
                affected_count=len(secret_issues),
                fix_proposal="""
****:
```bash
# 1. .env.example
cat > .env.example << EOF
DB_PASSWORD=your_password_here
AWS_SECRET_KEY=your_key_here
API_TOKEN=your_token_here
EOF

# 2. 
# config/prod.yaml:
# password: ${DB_PASSWORD}

# 3. .env.gitignore
echo ".env" >> .gitignore
```
                """,
                expected_improvement="+5-10",
                estimated_time="15-30"
            ))
        
        self.root_causes = sorted(root_causes, key=lambda x: x.affected_count, reverse=True)
        return self.root_causes
    
    def generate_aggregated_report(self) -> str:
        """
        Generate aggregated analysis report
        
        Returns:
            Markdown formatted aggregation report
        """
        clusters = self.cluster_similar_issues()
        root_causes = self.analyze_root_causes()
        
        md = "## 🎯 \n\n"
        
        if not root_causes:
            md += "✅ \n\n"
            return md
        
        md += f" **{len(root_causes)}** **{sum(rc.affected_count for rc in root_causes)}**\n\n"
        md += "---\n\n"
        
        for i, rc in enumerate(root_causes, 1):
            md += f"### {i}: {rc.name}\n\n"
            md += f"**ID**: {rc.id}  \n"
            md += f"****: {rc.affected_count} {', '.join(rc.affected_dimensions)}   \n"
            md += f"****: {rc.description}  \n\n"
            
            md += rc.fix_proposal
            md += "\n\n"
            
            md += f"****: {rc.expected_improvement}  \n"
            md += f"****: {rc.estimated_time}  \n\n"
            md += "---\n\n"
        
        # Add cluster summary
        if clusters:
            md += "### \n\n"
            md += "|  |  |  |  |\n"
            md += "|----------|--------|----------|----------|\n"
            for cluster in clusters:
                md += f"| {cluster.name} | {len(cluster.affected_issues)} | {cluster.impact_score} | {cluster.fix_strategy} |\n"
            md += "\n"
        
        return md
    
    def get_quick_wins(self, max_count: int = 5) -> List[Issue]:
        """
        Get quick win issues (high impact, low effort)
        
        Args:
            max_count: Maximum number of quick wins to return
            
        Returns:
            List of quick win issues
        """
        # Filter issues with high priority and short estimated time
        quick_wins = []
        
        time_keywords = ['minute', 'min', '15', '30']
        for issue in self.issues:
            if issue.priority >= 60 and issue.estimated_time:
                if any(kw in issue.estimated_time.lower() for kw in time_keywords):
                    quick_wins.append(issue)
        
        return sorted(quick_wins, key=lambda x: x.priority, reverse=True)[:max_count]
    
    def calculate_improvement_potential(self) -> Dict[str, float]:
        """
        Calculate potential score improvement by fixing issues
        
        Returns:
            Dict mapping urgency level to potential improvement
        """
        improvement = {
            'immediate': 0.0,
            'short_term': 0.0,
            'long_term': 0.0
        }
        
        for issue in self.issues:
            # Estimate score impact based on priority
            impact = issue.priority / 10
            
            if issue.is_high_priority():
                improvement['immediate'] += impact
            elif issue.level == IssueLevel.WARNING:
                improvement['short_term'] += impact
            else:
                improvement['long_term'] += impact
        
        return improvement
    
    def save_aggregated_report(self, output_path: str):
        """
        Save aggregated analysis report
        
        Args:
            output_path: Output file path
        """
        report = self.generate_aggregated_report()
        
        # Add quick wins section
        quick_wins = self.get_quick_wins()
        if quick_wins:
            report += "## 🚀 Quick Wins\n\n"
            report += "\n\n"
            for i, issue in enumerate(quick_wins, 1):
                report += f"{i}. **[{issue.rule}]** {issue.message}\n"
                if issue.fix_command:
                    report += f"   - : `{issue.fix_command}`\n"
                report += f"   - : {issue.estimated_time}\n"
                report += f"   - : +{issue.priority/10:.0f}\n\n"
        
        # Add improvement potential
        potential = self.calculate_improvement_potential()
        report += "## 📈 \n\n"
        report += f"- **** ({len([i for i in self.issues if i.is_high_priority()])}):  +{potential['immediate']:.0f}\n"
        report += f"- **** ({len([i for i in self.issues if i.level == IssueLevel.WARNING])}):  +{potential['short_term']:.0f}\n"
        report += f"- **** ({len([i for i in self.issues if not i.is_high_priority() and i.level != IssueLevel.WARNING])}):  +{potential['long_term']:.0f}\n"
        report += f"- ****:  +{sum(potential.values()):.0f}\n\n"
        
        # Save report
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Aggregated report saved: {output_path}")


# Example usage and testing
if __name__ == '__main__':
    from issue_model import create_issue
    
    print("=== Issue Aggregator Test ===\n")
    
    # Create sample issues
    test_issues = [
        create_issue(
            level="error",
            category="code_quality",
            rule="CQ-001",
            message="Test coverage too low: 45% (target: ≥90%)",
            file="modules/common/utils.py",
            suggestion="Add unit tests",
            fix_command="pytest tests/",
            estimated_time="2 hours",
            priority=85
        ),
        create_issue(
            level="error",
            category="code_quality",
            rule="CQ-002",
            message="Test coverage missing for module",
            file="modules/user/service.py",
            suggestion="Create test file",
            estimated_time="1 hour",
            priority=80
        ),
        create_issue(
            level="warning",
            category="documentation",
            rule="DOC-001",
            message="Module common missing RUNBOOK.md",
            file="modules/common/doc/",
            suggestion="Create RUNBOOK.md",
            fix_command="make module_doc_gen MODULE=common",
            estimated_time="30 minutes",
            priority=60
        ),
        create_issue(
            level="warning",
            category="documentation",
            rule="DOC-002",
            message="Module user missing TEST_PLAN.md",
            file="modules/user/doc/",
            suggestion="Create TEST_PLAN.md",
            estimated_time="20 minutes",
            priority=55
        ),
        create_issue(
            level="blocker",
            category="security",
            rule="BLOCKER-001",
            message="Potential secret detected in config",
            file="config/prod.yaml",
            line=45,
            suggestion="Move to environment variable",
            fix_command="export DB_PASSWORD=xxx",
            estimated_time="15 minutes",
            priority=100
        )
    ]
    
    # Create aggregator
    aggregator = IssueAggregator(test_issues)
    
    # Test clustering
    print("Clustering similar issues...")
    clusters = aggregator.cluster_similar_issues()
    print(f"Found {len(clusters)} clusters\n")
    
    for cluster in clusters:
        print(f"  - {cluster.name}: {len(cluster.affected_issues)} issues (impact: {cluster.impact_score})")
    
    # Test root cause analysis
    print("\nAnalyzing root causes...")
    root_causes = aggregator.analyze_root_causes()
    print(f"Found {len(root_causes)} root causes\n")
    
    for rc in root_causes:
        print(f"  - [{rc.id}] {rc.name}: {rc.affected_count} issues")
    
    # Test quick wins
    print("\nIdentifying quick wins...")
    quick_wins = aggregator.get_quick_wins()
    print(f"Found {len(quick_wins)} quick wins\n")
    
    # Calculate improvement potential
    print("Calculating improvement potential...")
    potential = aggregator.calculate_improvement_potential()
    print(f"  - Immediate: +{potential['immediate']:.0f} points")
    print(f"  - Short-term: +{potential['short_term']:.0f} points")
    print(f"  - Long-term: +{potential['long_term']:.0f} points")
    print(f"  - Total: +{sum(potential.values()):.0f} points")
    
    # Save report
    print("\nGenerating aggregated report...")
    aggregator.save_aggregated_report('temp/test-aggregated-report.md')
    
    print("\n✅ Issue aggregator test completed successfully!")

