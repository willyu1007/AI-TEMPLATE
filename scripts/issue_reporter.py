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
        
        summary = """## 📋 执行摘要

### 关键指标
"""
        
        # Status indicators
        if blocker_count > 0:
            summary += f"- 🔴 **阻断性问题**: {blocker_count}个 - **必须立即修复**\n"
        if error_count > 0:
            summary += f"- 🟠 **错误**: {error_count}个 - 高优先级修复\n"
        if warning_count > 0:
            summary += f"- 🟡 **警告**: {warning_count}个 - 建议修复\n"
        if info_count > 0:
            summary += f"- 🔵 **信息/建议**: {info_count}个 - 可选优化\n"
        
        if not self.issues:
            summary += "- ✅ **没有检测到问题** - 状态良好！\n"
        
        summary += "\n### 影响评估\n"
        
        if blocker_count > 0:
            summary += f"- 🔴 **阻断发布**: {blocker_count}个阻断性问题必须解决\n"
        
        high_priority_count = blocker_count + error_count
        if high_priority_count > 0:
            summary += f"- 🔴 **必须修复**: {high_priority_count}个高优先级问题\n"
        
        if warning_count > 0:
            summary += f"- 🟡 **建议修复**: {warning_count}个警告\n"
        
        # Category breakdown
        summary += "\n### 问题分布（按维度）\n"
        for cat_name, cat_issues in sorted(self.by_category.items(), key=lambda x: len(x[1]), reverse=True):
            if cat_issues:
                summary += f"- **{cat_name}**: {len(cat_issues)}个问题\n"
        
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
            'blocker': "🔥 阻断性问题（必须立即修复）",
            'error': "🚨 严重问题（优先修复）",
            'warning': "⚠️  一般问题（建议修复）",
            'info': "ℹ️  信息提示",
            'suggestion': "💡 优化建议（可选）"
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
                md += f"- **文件**: `{issue.file}`"
                if issue.line:
                    md += f":{issue.line}"
                    if issue.column:
                        md += f":{issue.column}"
                md += "\n"
            
            # Code context
            if issue.context_before or issue.context_after:
                md += "- **代码上下文**:\n\n```python\n"
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
                md += f"- **修复建议**: {issue.suggestion}\n"
            if issue.fix_command:
                md += f"- **修复命令**: `{issue.fix_command}`\n"
            if issue.estimated_time:
                md += f"- **预估时间**: {issue.estimated_time}\n"
            if issue.reference:
                md += f"- **参考文档**: {issue.reference}\n"
            if issue.impact:
                md += f"- **影响**: {issue.impact}\n"
            
            md += "\n---\n\n"
        
        if max_issues and len(issues) > max_issues:
            md += f"*还有 {len(issues) - max_issues} 个{level}问题，请查看完整JSON报告*\n\n"
        
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
        
        md = "## 📈 改进路径（优先级排序）\n\n"
        
        if immediate:
            md += "### 立即执行（今日内）\n\n"
            for i, issue in enumerate(immediate[:5], 1):
                time_est = issue.estimated_time or "未知"
                md += f"{i}. [{issue.rule}] {issue.message} ({time_est})\n"
                if issue.fix_command:
                    md += f"   ```bash\n   {issue.fix_command}\n   ```\n"
            if len(immediate) > 5:
                md += f"\n*还有 {len(immediate) - 5} 个高优先级问题...*\n"
            md += "\n"
        
        if short_term:
            md += "### 短期改进（本周内）\n\n"
            for i, issue in enumerate(short_term[:10], 1):
                time_est = issue.estimated_time or "未知"
                md += f"{i}. [{issue.rule}] {issue.message} ({time_est})\n"
            if len(short_term) > 10:
                md += f"\n*还有 {len(short_term) - 10} 个警告...*\n"
            md += "\n"
        
        if long_term:
            md += "### 中长期改进（2周内）\n\n"
            for i, issue in enumerate(long_term[:10], 1):
                time_est = issue.estimated_time or "未知"
                md += f"{i}. [{issue.rule}] {issue.message} ({time_est})\n"
            if len(long_term) > 10:
                md += f"\n*还有 {len(long_term) - 10} 个优化建议...*\n"
            md += "\n"
        
        # Expected improvement calculation
        immediate_score = sum(issue.priority for issue in immediate) / 10
        short_score = sum(issue.priority for issue in short_term) / 10
        mid_score = sum(issue.priority for issue in long_term) / 10
        
        md += "### 预期效果\n\n"
        if immediate:
            md += f"- **立即执行**: 约 +{immediate_score:.0f}分\n"
        if short_term:
            md += f"- **短期改进**: 约 +{short_score:.0f}分\n"
        if long_term:
            md += f"- **中期改进**: 约 +{mid_score:.0f}分\n"
        md += f"- **总潜在提升**: 约 +{immediate_score + short_score + mid_score:.0f}分\n"
        
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
        
        report = f"""# 仓库健康度检查报告

> **检查时间**: {timestamp}  
> **总体评分**: {self.overall_score:.1f}/100  
> **评级**: {grade}  
> **检查时长**: {self.duration:.2f}秒  
> **检测问题**: {len(self.issues)}个

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

## 📁 附件

- 完整JSON报告: `{Path(output_path).stem}.json`
- 问题清单CSV: `{Path(output_path).stem}.csv`

---

**下次检查**: 建议24小时后重新检查  
**命令**: `make health_check`  
**严格模式**: `make health_check_strict`

---

*报告生成时间: {timestamp}*
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

