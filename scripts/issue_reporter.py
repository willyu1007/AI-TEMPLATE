#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
issue_reporter.py - Issue Reporter for Health Check Reports

Generates structured, human-readable health check reports with:
- Executive summary
- Categorized issue lists
- Improvement roadmap with priorities
- Multiple output formats (Markdown, JSON, CSV)

Created: 2025-11-09 (Phase 14.2+)
"""

import sys
import json
import csv
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Import Issue model
from issue_model import Issue, IssueLevel, IssueCategory


class IssueReporter:
    """
    Issue Reporter for generating structured health check reports
    
    Features:
    - Categorize issues by level and category
    - Generate executive summary
    - Create prioritized improvement roadmap
    - Export to multiple formats (Markdown, JSON, CSV)
    """
    
    def __init__(self, issues: List[Issue], overall_score: float = 0, duration: float = 0):
        """
        Initialize issue reporter
        
        Args:
            issues: List of Issue objects
            overall_score: Overall health score (0-100)
            duration: Check duration in seconds
        """
        self.issues = issues
        self.overall_score = overall_score
        self.duration = duration
        self.categorized = self._categorize_issues()
        self.by_category = self._group_by_category()
    
    def _categorize_issues(self) -> Dict[str, List[Issue]]:
        """Categorize issues by severity level"""
        categorized = {
            'blocker': [],
            'error': [],
            'warning': [],
            'info': [],
            'suggestion': []
        }
        
        for issue in self.issues:
            if issue.is_blocker():
                categorized['blocker'].append(issue)
            elif issue.level == IssueLevel.ERROR:
                categorized['error'].append(issue)
            elif issue.level == IssueLevel.WARNING:
                categorized['warning'].append(issue)
            elif issue.level == IssueLevel.INFO:
                categorized['info'].append(issue)
            elif issue.level == IssueLevel.SUGGESTION:
                categorized['suggestion'].append(issue)
        
        return categorized
    
    def _group_by_category(self) -> Dict[str, List[Issue]]:
        """Group issues by category (dimension)"""
        by_category = defaultdict(list)
        for issue in self.issues:
            by_category[issue.category.value].append(issue)
        return dict(by_category)
    
    def generate_summary(self) -> str:
        """
        Generate executive summary
        
        Returns:
            Markdown formatted executive summary
        """
        blocker_count = len(self.categorized['blocker'])
        error_count = len(self.categorized['error'])
        warning_count = len(self.categorized['warning'])
        info_count = len(self.categorized['info']) + len(self.categorized['suggestion'])
        
        summary = """## 📋 

### 
"""
        
        # Status indicators
        if blocker_count > 0:
            summary += f"- 🔴 ****: {blocker_count} - ****\n"
        if error_count > 0:
            summary += f"- 🟠 ****: {error_count} - \n"
        if warning_count > 0:
            summary += f"- 🟡 ****: {warning_count} - \n"
        if info_count > 0:
            summary += f"- 🔵 **/**: {info_count} - \n"
        
        if not self.issues:
            summary += "- ✅ **** - \n"
        
        summary += "\n### \n"
        
        if blocker_count > 0:
            summary += f"- 🔴 ****: {blocker_count}\n"
        
        high_priority_count = blocker_count + error_count
        if high_priority_count > 0:
            summary += f"- 🔴 ****: {high_priority_count}\n"
        
        if warning_count > 0:
            summary += f"- 🟡 ****: {warning_count}\n"
        
        # Category breakdown
        summary += "\n### \n"
        for cat_name, cat_issues in sorted(self.by_category.items(), key=lambda x: len(x[1]), reverse=True):
            if cat_issues:
                summary += f"- **{cat_name}**: {len(cat_issues)}\n"
        
        return summary + "\n"
    
    def generate_issue_list(self, level: str, max_issues: int = None) -> str:
        """
        Generate categorized issue list
        
        Args:
            level: Issue level ("blocker", "error", "warning", "info", "suggestion")
            max_issues: Maximum issues to display (None = all)
            
        Returns:
            Markdown formatted issue list
        """
        issues = self.categorized.get(level, [])
        if not issues:
            return ""
        
        # Title mapping
        title_map = {
            'blocker': "🔥 ",
            'error': "🚨 ",
            'warning': "⚠️  ",
            'info': "ℹ️  ",
            'suggestion': "💡 "
        }
        
        md = f"## {title_map.get(level, level.upper())}\n\n"
        
        # Sort by priority (descending)
        sorted_issues = sorted(issues, key=lambda x: x.priority, reverse=True)
        
        if max_issues:
            sorted_issues = sorted_issues[:max_issues]
        
        for i, issue in enumerate(sorted_issues, 1):
            md += f"### {i}. [{issue.rule}] {issue.message}\n\n"
            
            # Location
            if issue.file:
                md += f"- ****: `{issue.file}`"
                if issue.line:
                    md += f":{issue.line}"
                    if issue.column:
                        md += f":{issue.column}"
                md += "\n"
            
            # Code context
            if issue.context_before or issue.context_after:
                md += "- ****:\n\n```python\n"
                if issue.context_before:
                    for line in issue.context_before:
                        md += f"{line}\n"
                md += ">>> ISSUE LINE <<<\n"
                if issue.context_after:
                    for line in issue.context_after:
                        md += f"{line}\n"
                md += "```\n\n"
            
            # Fix information
            if issue.suggestion:
                md += f"- ****: {issue.suggestion}\n"
            if issue.fix_command:
                md += f"- ****: `{issue.fix_command}`\n"
            if issue.estimated_time:
                md += f"- ****: {issue.estimated_time}\n"
            if issue.reference:
                md += f"- ****: {issue.reference}\n"
            if issue.impact:
                md += f"- ****: {issue.impact}\n"
            
            md += "\n---\n\n"
        
        if max_issues and len(issues) > max_issues:
            md += f"* {len(issues) - max_issues} {level}JSON*\n\n"
        
        return md
    
    def generate_improvement_path(self) -> str:
        """
        Generate prioritized improvement roadmap
        
        Returns:
            Markdown formatted improvement roadmap
        """
        # Sort all issues by priority
        sorted_issues = sorted(self.issues, key=lambda x: x.priority, reverse=True)
        
        # Categorize by urgency
        immediate = [i for i in sorted_issues if i.is_high_priority()]
        short_term = [i for i in sorted_issues if i.level == IssueLevel.WARNING]
        long_term = [i for i in sorted_issues if i.level in [IssueLevel.INFO, IssueLevel.SUGGESTION]]
        
        md = "## 📈 \n\n"
        
        if immediate:
            md += "### \n\n"
            for i, issue in enumerate(immediate[:5], 1):
                time_est = issue.estimated_time or ""
                md += f"{i}. [{issue.rule}] {issue.message} ({time_est})\n"
                if issue.fix_command:
                    md += f"   ```bash\n   {issue.fix_command}\n   ```\n"
            if len(immediate) > 5:
                md += f"\n* {len(immediate) - 5} ...*\n"
            md += "\n"
        
        if short_term:
            md += "### \n\n"
            for i, issue in enumerate(short_term[:10], 1):
                time_est = issue.estimated_time or ""
                md += f"{i}. [{issue.rule}] {issue.message} ({time_est})\n"
            if len(short_term) > 10:
                md += f"\n* {len(short_term) - 10} ...*\n"
            md += "\n"
        
        if long_term:
            md += "### 2\n\n"
            for i, issue in enumerate(long_term[:10], 1):
                time_est = issue.estimated_time or ""
                md += f"{i}. [{issue.rule}] {issue.message} ({time_est})\n"
            if len(long_term) > 10:
                md += f"\n* {len(long_term) - 10} ...*\n"
            md += "\n"
        
        # Expected improvement calculation
        immediate_score = sum(issue.priority for issue in immediate) / 10
        short_score = sum(issue.priority for issue in short_term) / 10
        mid_score = sum(issue.priority for issue in long_term) / 10
        
        md += "### \n\n"
        if immediate:
            md += f"- ****:  +{immediate_score:.0f}\n"
        if short_term:
            md += f"- ****:  +{short_score:.0f}\n"
        if long_term:
            md += f"- ****:  +{mid_score:.0f}\n"
        md += f"- ****:  +{immediate_score + short_score + mid_score:.0f}\n"
        
        return md + "\n"
    
    def save_report(self, output_path: str):
        """
        Save complete Markdown report
        
        Args:
            output_path: Output file path (should end with .md)
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Calculate grade
        if self.overall_score >= 90:
            grade = "⭐⭐⭐⭐⭐ Excellent"
        elif self.overall_score >= 80:
            grade = "⭐⭐⭐⭐ Good"
        elif self.overall_score >= 70:
            grade = "⭐⭐⭐ Fair"
        else:
            grade = "⚠️ Needs Improvement"
        
        report = f"""# 

> ****: {timestamp}  
> ****: {self.overall_score:.1f}/100  
> ****: {grade}  
> ****: {self.duration:.2f}  
> ****: {len(self.issues)}

---

{self.generate_summary()}

---

{self.generate_issue_list('blocker')}

{self.generate_issue_list('error')}

{self.generate_issue_list('warning')}

{self.generate_issue_list('suggestion', max_issues=10)}

---

{self.generate_improvement_path()}

---

## 📁 

- JSON: `{Path(output_path).stem}.json`
- CSV: `{Path(output_path).stem}.csv`

---

****: 24  
****: `make health_check`  
****: `make health_check_strict`

---

*: {timestamp}*
"""
        
        # Save Markdown report
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Markdown report saved: {output_path}")
    
    def save_json(self, output_path: str):
        """
        Save JSON format report
        
        Args:
            output_path: Output file path (should end with .json)
        """
        data = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': self.overall_score,
            'duration': self.duration,
            'total_issues': len(self.issues),
            'issues_by_level': {
                level: len(issues) for level, issues in self.categorized.items()
            },
            'issues_by_category': {
                cat: len(issues) for cat, issues in self.by_category.items()
            },
            'issues': [issue.to_dict() for issue in self.issues]
        }
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON report saved: {output_path}")
    
    def save_csv(self, output_path: str):
        """
        Save CSV format issue list
        
        Args:
            output_path: Output file path (should end with .csv)
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Rule', 'Level', 'Category', 'Message', 'File', 'Line',
                'Suggestion', 'Fix Command', 'Estimated Time', 'Priority'
            ])
            
            for issue in sorted(self.issues, key=lambda x: x.priority, reverse=True):
                writer.writerow([
                    issue.rule,
                    issue.level.value,
                    issue.category.value,
                    issue.message,
                    issue.file or '',
                    issue.line or '',
                    issue.suggestion or '',
                    issue.fix_command or '',
                    issue.estimated_time or '',
                    issue.priority
                ])
        
        print(f"✅ CSV report saved: {output_path}")


# Example usage and testing
if __name__ == '__main__':
    from issue_model import create_issue
    
    # Create sample issues
    test_issues = [
        create_issue(
            level="error",
            category="code_quality",
            rule="CQ-001",
            message="Test coverage too low: 45% (target: ≥90%)",
            file="modules/common/utils.py",
            line=1,
            suggestion="Add unit tests to increase coverage",
            fix_command="make test_coverage",
            estimated_time="2 hours",
            priority=85
        ),
        create_issue(
            level="warning",
            category="documentation",
            rule="DOC-001",
            message="Module missing RUNBOOK.md",
            file="modules/common/",
            suggestion="Create RUNBOOK.md using template",
            fix_command="make module_doc_gen MODULE=common",
            estimated_time="30 minutes",
            priority=60
        ),
        create_issue(
            level="blocker",
            category="security",
            rule="BLOCKER-001",
            message="Potential secret key detected in config",
            file="config/prod.yaml",
            line=45,
            suggestion="Move to environment variable",
            fix_command="Use SECRET_KEY env var",
            estimated_time="15 minutes",
            priority=100,
            impact="Security risk - must fix immediately"
        )
    ]
    
    print("=== Issue Reporter Test ===\n")
    
    # Create reporter
    reporter = IssueReporter(test_issues, overall_score=65.5, duration=12.3)
    
    # Test Markdown generation
    print("Generating Markdown report...")
    reporter.save_report('temp/test-health-report.md')
    
    # Test JSON generation
    print("Generating JSON report...")
    reporter.save_json('temp/test-health-report.json')
    
    # Test CSV generation
    print("Generating CSV report...")
    reporter.save_csv('temp/test-health-report.csv')
    
    print("\n✅ Issue reporter test completed successfully!")

