#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report_location_check.py - 


1. 
2. 
3. 


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

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent

# 
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

# 
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

# 
ALLOWED_ROOT_FILES = [
    'README.md',
    'CONTRIBUTING.md',
    'QUICK_START.md',
    'TEMPLATE_USAGE.md',
    'LICENSE',
    'agent.md'
]


def is_report_file(file_path: Path) -> bool:
    """"""
    name = file_path.name.lower()
    
    # 
    for pattern in REPORT_PATTERNS:
        if re.match(pattern, name, re.IGNORECASE):
            # 
            if file_path.name in ALLOWED_ROOT_FILES:
                return False
            return True
    
    return False


def get_correct_location(file_path: Path) -> str:
    """"""
    name = file_path.name.lower()
    
    # 
    for keyword, location in CORRECT_LOCATIONS.items():
        if keyword.lower() in name:
            return location
    
    # 
    return 'ai/maintenance_reports/'


def scan_misplaced_reports() -> List[Tuple[Path, str]]:
    """"""
    misplaced = []
    
    # 
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
    
    # tmp
    tmp_dir = REPO_ROOT / 'tmp'
    if tmp_dir.exists():
        for file in tmp_dir.rglob('*'):
            if file.is_file() and is_report_file(file):
                correct_loc = get_correct_location(file)
                misplaced.append((file, correct_loc))
    
    return misplaced


def fix_misplaced_reports(misplaced: List[Tuple[Path, str]], dry_run: bool = True):
    """"""
    for file_path, correct_location in misplaced:
        target_dir = REPO_ROOT / correct_location
        
        # 
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 
        new_name = file_path.name
        if not re.search(r'\d{8}', new_name):
            # 
            stem = file_path.stem
            suffix = file_path.suffix
            date_str = datetime.now().strftime('%Y%m%d')
            new_name = f"{stem}-{date_str}{suffix}"
        
        target_path = target_dir / new_name
        
        if dry_run:
            print(f"  📋 : {file_path.relative_to(REPO_ROOT)}")
            print(f"     → {target_path.relative_to(REPO_ROOT)}")
        else:
            try:
                file_path.rename(target_path)
                print(f"  ✅ : {file_path.relative_to(REPO_ROOT)}")
                print(f"     → {target_path.relative_to(REPO_ROOT)}")
            except Exception as e:
                print(f"  ❌ : {file_path.relative_to(REPO_ROOT)}")
                print(f"     : {e}")


def main():
    """"""
    import argparse
    
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--fix',
        action='store_true',
        help=''
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔍 ")
    print("=" * 60)
    
    # 
    misplaced = scan_misplaced_reports()
    
    if not misplaced:
        print("\n✅ ")
        return 0
    
    print(f"\n⚠️   {len(misplaced)} \n")
    
    for file_path, correct_location in misplaced:
        print(f"  ❌ {file_path.relative_to(REPO_ROOT)}")
        print(f"     : {correct_location}")
    
    if args.fix:
        print("\n" + "-" * 60)
        print("🔧 ...")
        print("-" * 60 + "\n")
        fix_misplaced_reports(misplaced, dry_run=False)
        print("\n✅ ")
    else:
        print("\n" + "-" * 60)
        print("💡 :")
        print("-" * 60 + "\n")
        fix_misplaced_reports(misplaced, dry_run=True)
        print("\n:  --fix ")
    
    print("=" * 60)
    
    return 0 if not misplaced or args.fix else 1


if __name__ == '__main__':
    sys.exit(main())
