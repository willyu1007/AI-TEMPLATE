#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
base_lint.py - Base Lint Framework for All Linters

lint
1. UTF-8
2. 
3. 
4. JSON/Markdown
5. 

Created: 2025-11-09
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class Severity(Enum):
    """"""
    ERROR = "error"      # 
    WARNING = "warning"  # 
    INFO = "info"       # 


@dataclass
class LintIssue:
    """Lint"""
    file: str                  # 
    line: Optional[int] = None  # 
    column: Optional[int] = None  # 
    severity: Severity = Severity.WARNING  # 
    message: str = ""           # 
    rule: Optional[str] = None  # ID
    fix: Optional[str] = None   # 


class BaseLinter(ABC):
    """
    Linter
    
    lintcheck
    """
    
    def __init__(self, repo_root: Optional[Path] = None):
        """Linter"""
        self.repo_root = repo_root or Path(__file__).parent.parent
        self.issues: List[LintIssue] = []
        self.stats = {
            'files_checked': 0,
            'errors': 0,
            'warnings': 0,
            'info': 0
        }
    
    @abstractmethod
    def check(self) -> bool:
        """
        
        
        Returns:
            bool: True if no errors, False otherwise
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Linter"""
        pass
    
    def add_issue(self, issue: LintIssue):
        """"""
        self.issues.append(issue)
        # 
        if issue.severity == Severity.ERROR:
            self.stats['errors'] += 1
        elif issue.severity == Severity.WARNING:
            self.stats['warnings'] += 1
        else:
            self.stats['info'] += 1
    
    def print_header(self, title: Optional[str] = None):
        """"""
        title = title or f"{self.name} Lint"
        print("=" * 60)
        print(title)
        print("=" * 60)
    
    def print_separator(self):
        """"""
        print("-" * 60)
    
    def print_results(self):
        """"""
        if not self.issues:
            print(f"\n✅ {self.name}: ")
            return
        
        # 
        issues_by_file: Dict[str, List[LintIssue]] = {}
        for issue in self.issues:
            if issue.file not in issues_by_file:
                issues_by_file[issue.file] = []
            issues_by_file[issue.file].append(issue)
        
        # 
        for file_path, file_issues in issues_by_file.items():
            print(f"\n📄 {file_path}:")
            for issue in file_issues:
                # 
                location = ""
                if issue.line:
                    location = f"{issue.line}"
                    if issue.column:
                        location += f":{issue.column}"
                
                # 
                icon = "❌" if issue.severity == Severity.ERROR else "⚠️" if issue.severity == Severity.WARNING else "ℹ️"
                
                # 
                if location:
                    print(f"  {icon} [{location}] {issue.message}")
                else:
                    print(f"  {icon} {issue.message}")
                
                # 
                if issue.fix:
                    print(f"     💡 {issue.fix}")
    
    def print_summary(self):
        """"""
        print("\n" + "=" * 60)
        print("📊 ")
        print("-" * 60)
        print(f"  : {self.stats['files_checked']}")
        print(f"  : {self.stats['errors']} ❌")
        print(f"  : {self.stats['warnings']} ⚠️")
        print(f"  : {self.stats['info']} ℹ️")
        
        # 
        if self.stats['errors'] > 0:
            print(f"\n❌ {self.name}{self.stats['errors']}")
        elif self.stats['warnings'] > 0:
            print(f"\n⚠️  {self.name}{self.stats['warnings']}")
        else:
            print(f"\n✅ {self.name}")
    
    def to_json(self) -> str:
        """JSON"""
        data = {
            'linter': self.name,
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats,
            'issues': [
                {
                    'file': issue.file,
                    'line': issue.line,
                    'column': issue.column,
                    'severity': issue.severity.value,
                    'message': issue.message,
                    'rule': issue.rule,
                    'fix': issue.fix
                }
                for issue in self.issues
            ]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def to_markdown(self) -> str:
        """Markdown"""
        lines = []
        lines.append(f"# {self.name} Report")
        lines.append(f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 
        lines.append("## Summary\n")
        lines.append(f"- Files Checked: {self.stats['files_checked']}")
        lines.append(f"- Errors: {self.stats['errors']}")
        lines.append(f"- Warnings: {self.stats['warnings']}")
        lines.append(f"- Info: {self.stats['info']}\n")
        
        # 
        if self.issues:
            lines.append("## Issues\n")
            
            # 
            for severity in [Severity.ERROR, Severity.WARNING, Severity.INFO]:
                severity_issues = [i for i in self.issues if i.severity == severity]
                if severity_issues:
                    lines.append(f"### {severity.value.title()}s\n")
                    for issue in severity_issues:
                        location = f"L{issue.line}" if issue.line else ""
                        if issue.column:
                            location += f":C{issue.column}"
                        
                        lines.append(f"- **{issue.file}** {location}")
                        lines.append(f"  - {issue.message}")
                        if issue.fix:
                            lines.append(f"  - 💡 {issue.fix}")
                    lines.append("")
        
        return "\n".join(lines)
    
    def run(self, json_output: bool = False, markdown_output: bool = False) -> int:
        """
        Linter
        
        Args:
            json_output: JSON
            markdown_output: Markdown
            
        Returns:
            int: 0=1=2=
        """
        try:
            # 
            if not json_output and not markdown_output:
                self.print_header()
            
            success = self.check()
            
            # 
            if json_output:
                print(self.to_json())
            elif markdown_output:
                print(self.to_markdown())
            else:
                self.print_results()
                self.print_summary()
            
            # 
            if not success or self.stats['errors'] > 0:
                return 1
            return 0
            
        except Exception as e:
            if not json_output:
                print(f"\n❌ {self.name}: {str(e)}", file=sys.stderr)
            return 2


class MultiLinter(BaseLinter):
    """
    LinterLinter
    
    linter
    """
    
    def __init__(self, linters: List[BaseLinter], name: str = "Multi"):
        """Linter"""
        super().__init__()
        self.linters = linters
        self._name = name
    
    @property
    def name(self) -> str:
        """Linter"""
        return self._name
    
    def check(self) -> bool:
        """Linter"""
        all_success = True
        
        for linter in self.linters:
            print(f"\n▶  {linter.name}...")
            self.print_separator()
            
            # linter
            success = linter.check()
            if not success:
                all_success = False
            
            # 
            self.issues.extend(linter.issues)
            self.stats['files_checked'] += linter.stats['files_checked']
            self.stats['errors'] += linter.stats['errors']
            self.stats['warnings'] += linter.stats['warnings']
            self.stats['info'] += linter.stats['info']
            
            # linter
            linter.print_results()
        
        return all_success


def run_linter(linter_class, args=None):
    """
    Linter
    
    Args:
        linter_class: Linter
        args: 
    
    Returns:
        int: 
    """
    import argparse
    
    # 
    if args is None:
        parser = argparse.ArgumentParser(
            description=f'{linter_class.__name__} - Lint'
        )
        parser.add_argument(
            '--json',
            action='store_true',
            help='JSON'
        )
        parser.add_argument(
            '--markdown',
            action='store_true', 
            help='Markdown'
        )
        args = parser.parse_args()
    
    # linter
    linter = linter_class()
    return linter.run(
        json_output=getattr(args, 'json', False),
        markdown_output=getattr(args, 'markdown', False)
    )


if __name__ == '__main__':
    # Linter
    class TestLinter(BaseLinter):
        @property
        def name(self) -> str:
            return "Test"
        
        def check(self) -> bool:
            """"""
            self.stats['files_checked'] = 1
            
            # 
            self.add_issue(LintIssue(
                file="test.py",
                line=10,
                severity=Severity.ERROR,
                message="",
                fix=""
            ))
            
            self.add_issue(LintIssue(
                file="test.py",
                line=20,
                severity=Severity.WARNING,
                message=""
            ))
            
            return False
    
    # 
    sys.exit(run_linter(TestLinter))
