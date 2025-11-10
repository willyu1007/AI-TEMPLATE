#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report_location_check.py - 验证报告文件位置是否正确

功能：
1. 扫描根目录的报告文件
2. 检查报告是否在正确位置
3. 提供移动建议

用法：
    python scripts/report_location_check.py
    python scripts/report_location_check.py --fix
    make check_report_locations

Created: 2025-11-10
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent

# 报告文件模式
REPORT_PATTERNS = [
    r'.*report.*\.md$',
    r'.*report.*\.json$',
    r'.*report.*\.html$',
    r'.*summary.*\.md$',
    r'.*optimization.*\.md$',
    r'.*refactor.*\.md$',
    r'.*maintenance.*\.md$',
    r'.*health.*\.md$',
    r'.*health.*\.json$',
    r'.*PLAN.*\.md$'
]

# 正确的报告位置
CORRECT_LOCATIONS = {
    'health': 'ai/maintenance_reports/',
    'optimization': 'ai/maintenance_reports/',
    'refactor': 'ai/maintenance_reports/',
    'maintenance': 'ai/maintenance_reports/',
    'session': 'ai/sessions/',
    'dataflow': 'ai/maintenance_reports/',
    'report': 'ai/maintenance_reports/',
    'summary': 'ai/maintenance_reports/',
    'PLAN': 'ai/maintenance_reports/'
}

# 允许在根目录的文件
ALLOWED_ROOT_FILES = [
    'README.md',
    'CONTRIBUTING.md',
    'QUICK_START.md',
    'TEMPLATE_USAGE.md',
    'LICENSE',
    'agent.md'
]


def is_report_file(file_path: Path) -> bool:
    """判断是否是报告文件"""
    name = file_path.name.lower()
    
    # 检查是否匹配报告模式
    for pattern in REPORT_PATTERNS:
        if re.match(pattern, name, re.IGNORECASE):
            # 排除允许的文件
            if file_path.name in ALLOWED_ROOT_FILES:
                return False
            return True
    
    return False


def get_correct_location(file_path: Path) -> str:
    """获取文件的正确位置"""
    name = file_path.name.lower()
    
    # 根据关键字判断
    for keyword, location in CORRECT_LOCATIONS.items():
        if keyword.lower() in name:
            return location
    
    # 默认位置
    return 'ai/maintenance_reports/'


def scan_misplaced_reports() -> List[Tuple[Path, str]]:
    """扫描错误位置的报告"""
    misplaced = []
    
    # 检查根目录
    for file in REPO_ROOT.glob('*.md'):
        if is_report_file(file):
            correct_loc = get_correct_location(file)
            misplaced.append((file, correct_loc))
    
    for file in REPO_ROOT.glob('*.json'):
        if is_report_file(file):
            correct_loc = get_correct_location(file)
            misplaced.append((file, correct_loc))
    
    for file in REPO_ROOT.glob('*.html'):
        if is_report_file(file):
            correct_loc = get_correct_location(file)
            misplaced.append((file, correct_loc))
    
    # 检查tmp目录的报告
    tmp_dir = REPO_ROOT / 'tmp'
    if tmp_dir.exists():
        for file in tmp_dir.rglob('*'):
            if file.is_file() and is_report_file(file):
                correct_loc = get_correct_location(file)
                misplaced.append((file, correct_loc))
    
    return misplaced


def fix_misplaced_reports(misplaced: List[Tuple[Path, str]], dry_run: bool = True):
    """修复错误位置的报告"""
    for file_path, correct_location in misplaced:
        target_dir = REPO_ROOT / correct_location
        
        # 确保目标目录存在
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成新文件名（如果需要添加日期）
        new_name = file_path.name
        if not re.search(r'\d{8}', new_name):
            # 如果文件名中没有日期，添加日期
            stem = file_path.stem
            suffix = file_path.suffix
            date_str = datetime.now().strftime('%Y%m%d')
            new_name = f"{stem}-{date_str}{suffix}"
        
        target_path = target_dir / new_name
        
        if dry_run:
            print(f"  📋 将移动: {file_path.relative_to(REPO_ROOT)}")
            print(f"     → {target_path.relative_to(REPO_ROOT)}")
        else:
            try:
                file_path.rename(target_path)
                print(f"  ✅ 已移动: {file_path.relative_to(REPO_ROOT)}")
                print(f"     → {target_path.relative_to(REPO_ROOT)}")
            except Exception as e:
                print(f"  ❌ 移动失败: {file_path.relative_to(REPO_ROOT)}")
                print(f"     错误: {e}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='检查报告文件位置')
    parser.add_argument(
        '--fix',
        action='store_true',
        help='自动修复错误位置的报告'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔍 报告位置检查")
    print("=" * 60)
    
    # 扫描错误位置的报告
    misplaced = scan_misplaced_reports()
    
    if not misplaced:
        print("\n✅ 所有报告都在正确的位置")
        return 0
    
    print(f"\n⚠️  发现 {len(misplaced)} 个报告在错误的位置：\n")
    
    for file_path, correct_location in misplaced:
        print(f"  ❌ {file_path.relative_to(REPO_ROOT)}")
        print(f"     应该在: {correct_location}")
    
    if args.fix:
        print("\n" + "-" * 60)
        print("🔧 开始修复...")
        print("-" * 60 + "\n")
        fix_misplaced_reports(misplaced, dry_run=False)
        print("\n✅ 修复完成")
    else:
        print("\n" + "-" * 60)
        print("💡 建议操作:")
        print("-" * 60 + "\n")
        fix_misplaced_reports(misplaced, dry_run=True)
        print("\n提示: 使用 --fix 参数自动修复")
    
    print("=" * 60)
    
    return 0 if not misplaced or args.fix else 1


if __name__ == '__main__':
    sys.exit(main())
