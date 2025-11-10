#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
base_lint.py - Base Lint Framework for All Linters

提供统一的lint基础框架：
1. UTF-8处理
2. 输出格式化
3. 问题收集和报告
4. JSON/Markdown报告生成
5. 统一的退出码处理

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
    """问题严重级别"""
    ERROR = "error"      # 错误（必须修复）
    WARNING = "warning"  # 警告（建议修复）
    INFO = "info"       # 信息（可选优化）


@dataclass
class LintIssue:
    """Lint问题对象"""
    file: str                  # 文件路径
    line: Optional[int] = None  # 行号
    column: Optional[int] = None  # 列号
    severity: Severity = Severity.WARNING  # 严重级别
    message: str = ""           # 问题描述
    rule: Optional[str] = None  # 规则ID
    fix: Optional[str] = None   # 修复建议


class BaseLinter(ABC):
    """
    基础Linter类
    
    所有lint脚本应继承此类并实现check方法
    """
    
    def __init__(self, repo_root: Optional[Path] = None):
        """初始化Linter"""
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
        执行检查（子类必须实现）
        
        Returns:
            bool: True if no errors, False otherwise
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Linter名称（子类必须实现）"""
        pass
    
    def add_issue(self, issue: LintIssue):
        """添加问题"""
        self.issues.append(issue)
        # 更新统计
        if issue.severity == Severity.ERROR:
            self.stats['errors'] += 1
        elif issue.severity == Severity.WARNING:
            self.stats['warnings'] += 1
        else:
            self.stats['info'] += 1
    
    def print_header(self, title: Optional[str] = None):
        """打印标题"""
        title = title or f"{self.name} Lint"
        print("=" * 60)
        print(title)
        print("=" * 60)
    
    def print_separator(self):
        """打印分隔线"""
        print("-" * 60)
    
    def print_results(self):
        """打印检查结果"""
        if not self.issues:
            print(f"\n✅ {self.name}: 未发现问题")
            return
        
        # 按文件分组
        issues_by_file: Dict[str, List[LintIssue]] = {}
        for issue in self.issues:
            if issue.file not in issues_by_file:
                issues_by_file[issue.file] = []
            issues_by_file[issue.file].append(issue)
        
        # 打印问题
        for file_path, file_issues in issues_by_file.items():
            print(f"\n📄 {file_path}:")
            for issue in file_issues:
                # 构建位置信息
                location = ""
                if issue.line:
                    location = f"{issue.line}"
                    if issue.column:
                        location += f":{issue.column}"
                
                # 构建图标
                icon = "❌" if issue.severity == Severity.ERROR else "⚠️" if issue.severity == Severity.WARNING else "ℹ️"
                
                # 打印问题
                if location:
                    print(f"  {icon} [{location}] {issue.message}")
                else:
                    print(f"  {icon} {issue.message}")
                
                # 打印修复建议
                if issue.fix:
                    print(f"     💡 {issue.fix}")
    
    def print_summary(self):
        """打印汇总"""
        print("\n" + "=" * 60)
        print("📊 检查汇总")
        print("-" * 60)
        print(f"  文件数: {self.stats['files_checked']}")
        print(f"  错误数: {self.stats['errors']} ❌")
        print(f"  警告数: {self.stats['warnings']} ⚠️")
        print(f"  信息数: {self.stats['info']} ℹ️")
        
        # 计算退出码
        if self.stats['errors'] > 0:
            print(f"\n❌ {self.name}检查失败（发现{self.stats['errors']}个错误）")
        elif self.stats['warnings'] > 0:
            print(f"\n⚠️  {self.name}检查通过（有{self.stats['warnings']}个警告）")
        else:
            print(f"\n✅ {self.name}检查通过")
    
    def to_json(self) -> str:
        """导出为JSON格式"""
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
        """导出为Markdown格式"""
        lines = []
        lines.append(f"# {self.name} Report")
        lines.append(f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 汇总
        lines.append("## Summary\n")
        lines.append(f"- Files Checked: {self.stats['files_checked']}")
        lines.append(f"- Errors: {self.stats['errors']}")
        lines.append(f"- Warnings: {self.stats['warnings']}")
        lines.append(f"- Info: {self.stats['info']}\n")
        
        # 问题列表
        if self.issues:
            lines.append("## Issues\n")
            
            # 按严重级别分组
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
        运行Linter
        
        Args:
            json_output: 是否输出JSON格式
            markdown_output: 是否输出Markdown格式
            
        Returns:
            int: 退出码（0=成功，1=有错误，2=内部错误）
        """
        try:
            # 执行检查
            if not json_output and not markdown_output:
                self.print_header()
            
            success = self.check()
            
            # 输出结果
            if json_output:
                print(self.to_json())
            elif markdown_output:
                print(self.to_markdown())
            else:
                self.print_results()
                self.print_summary()
            
            # 返回退出码
            if not success or self.stats['errors'] > 0:
                return 1
            return 0
            
        except Exception as e:
            if not json_output:
                print(f"\n❌ {self.name}执行失败: {str(e)}", file=sys.stderr)
            return 2


class MultiLinter(BaseLinter):
    """
    组合多个Linter的元Linter
    
    可以组合多个linter一起执行
    """
    
    def __init__(self, linters: List[BaseLinter], name: str = "Multi"):
        """初始化组合Linter"""
        super().__init__()
        self.linters = linters
        self._name = name
    
    @property
    def name(self) -> str:
        """Linter名称"""
        return self._name
    
    def check(self) -> bool:
        """执行所有子Linter的检查"""
        all_success = True
        
        for linter in self.linters:
            print(f"\n▶ 执行 {linter.name}...")
            self.print_separator()
            
            # 执行子linter
            success = linter.check()
            if not success:
                all_success = False
            
            # 合并问题和统计
            self.issues.extend(linter.issues)
            self.stats['files_checked'] += linter.stats['files_checked']
            self.stats['errors'] += linter.stats['errors']
            self.stats['warnings'] += linter.stats['warnings']
            self.stats['info'] += linter.stats['info']
            
            # 打印子linter结果
            linter.print_results()
        
        return all_success


def run_linter(linter_class, args=None):
    """
    运行Linter的通用入口
    
    Args:
        linter_class: Linter类
        args: 命令行参数（可选）
    
    Returns:
        int: 退出码
    """
    import argparse
    
    # 如果没有提供参数，解析命令行
    if args is None:
        parser = argparse.ArgumentParser(
            description=f'{linter_class.__name__} - Lint检查工具'
        )
        parser.add_argument(
            '--json',
            action='store_true',
            help='输出JSON格式'
        )
        parser.add_argument(
            '--markdown',
            action='store_true', 
            help='输出Markdown格式'
        )
        args = parser.parse_args()
    
    # 创建并运行linter
    linter = linter_class()
    return linter.run(
        json_output=getattr(args, 'json', False),
        markdown_output=getattr(args, 'markdown', False)
    )


if __name__ == '__main__':
    # 示例：创建一个简单的测试Linter
    class TestLinter(BaseLinter):
        @property
        def name(self) -> str:
            return "Test"
        
        def check(self) -> bool:
            """执行测试检查"""
            self.stats['files_checked'] = 1
            
            # 添加一些测试问题
            self.add_issue(LintIssue(
                file="test.py",
                line=10,
                severity=Severity.ERROR,
                message="测试错误",
                fix="修复测试错误"
            ))
            
            self.add_issue(LintIssue(
                file="test.py",
                line=20,
                severity=Severity.WARNING,
                message="测试警告"
            ))
            
            return False
    
    # 运行测试
    sys.exit(run_linter(TestLinter))
