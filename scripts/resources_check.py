#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
resources_check.py - Resources

resources
  - Resources
  - Resource
  - Resource≤250
  - resources

:
    python scripts/resources_check.py
    make resources_check

Created: 2025-11-08 (Phase 10.5)
Updated: 2025-11-09 (Phase 11 - Windows)
"""

import os
import sys
import io
import re
from pathlib import Path
from typing import List, Dict, Tuple

# WindowsUTF-8
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except AttributeError:
        pass  # TextIOWrapper

# ANSI
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


class ResourcesChecker:
    """Resources"""
    
    def __init__(self, repo_root: str = "."):
        """"""
        self.repo_root = Path(repo_root)
        self.issues = []
        self.warnings = []
        self.stats = {
            "main_files_checked": 0,
            "resources_found": 0,
            "resources_missing": 0,
            "resources_oversized": 0
        }
    
    def check_main_file(self, main_file_path: Path, resources_dir: Path) -> bool:
        """
        resources
        
        Args:
            main_file_path: 
            resources_dir: resources
        
        Returns:
            True if
        """
        if not main_file_path.exists():
            self.issues.append(f": {main_file_path}")
            return False
        
        self.stats["main_files_checked"] += 1
        
        print(f"\n{'='*60}")
        print(f": {main_file_path.relative_to(self.repo_root)}")
        print(f"{'='*60}")
        
        # 
        try:
            with open(main_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.issues.append(f": {main_file_path} - {e}")
            return False
        
        # 
        line_count = len(content.split('\n'))
        if line_count > 350:
            self.warnings.append(f": {main_file_path} ({line_count}≤300)")
            print(f"{YELLOW}⚠️{NC}  : {line_count}≤300")
        else:
            print(f"{GREEN}✓{NC} : {line_count}")
        
        # resources
        resource_pattern = r'\[([^\]]+)\]\(resources/([^)]+\.md)\)'
        matches = re.findall(resource_pattern, content)
        
        if not matches:
            print(f"{YELLOW}ℹ️{NC}  resources")
            return True
        
        print(f"\n {len(matches)} resource:")
        
        # resource
        all_exist = True
        for title, resource_file in matches:
            resource_path = resources_dir / resource_file
            
            if not resource_path.exists():
                self.issues.append(f"Resource: {resource_path}")
                print(f"{RED}✗{NC} {resource_file} - ")
                self.stats["resources_missing"] += 1
                all_exist = False
            else:
                # 
                try:
                    with open(resource_path, 'r', encoding='utf-8') as f:
                        resource_content = f.read()
                    resource_lines = len(resource_content.split('\n'))
                    
                    if resource_lines > 250:
                        self.warnings.append(
                            f"Resource: {resource_path} ({resource_lines}≤250)"
                        )
                        print(f"{YELLOW}⚠️{NC}  {resource_file} - {resource_lines}≤250")
                        self.stats["resources_oversized"] += 1
                    else:
                        print(f"{GREEN}✓{NC} {resource_file} - {resource_lines}")
                    
                    self.stats["resources_found"] += 1
                except Exception as e:
                    self.warnings.append(f"resource: {resource_path} - {e}")
        
        # resources
        if resources_dir.exists():
            resource_files_in_dir = set(f.name for f in resources_dir.glob('*.md'))
            referenced_files = set(resource_file for _, resource_file in matches)
            
            unreferenced = resource_files_in_dir - referenced_files
            if unreferenced:
                print(f"\n{YELLOW}⚠️{NC}  resource:")
                for f in unreferenced:
                    print(f"  - {f}")
                    self.warnings.append(f"resource: {resources_dir / f}")
        
        return all_exist
    
    def check_resources_index_table(self, main_file_path: Path) -> bool:
        """Resources"""
        try:
            with open(main_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return False
        
        # 
        table_patterns = [
            r'\| Resource \|  \|  \|',
            r'## Resources',
            r'### Resources'
        ]
        
        has_index = any(re.search(pattern, content) for pattern in table_patterns)
        
        if has_index:
            print(f"{GREEN}✓{NC} Resources")
        else:
            self.warnings.append(f"Resources: {main_file_path}")
            print(f"{YELLOW}⚠️{NC}  Resources")
        
        return has_index
    
    def run(self) -> bool:
        """"""
        print(f"\n{BLUE}{'='*60}{NC}")
        print(f"{BLUE}Resources{NC}")
        print(f"{BLUE}{'='*60}{NC}")
        
        # MODULE_INIT_GUIDE.md
        module_init_guide = self.repo_root / "doc/modules/MODULE_INIT_GUIDE.md"
        module_resources = self.repo_root / "doc/modules/resources"
        
        if module_init_guide.exists():
            self.check_main_file(module_init_guide, module_resources)
            self.check_resources_index_table(module_init_guide)
        
        # DB_CHANGE_GUIDE.md
        db_change_guide = self.repo_root / "doc/process/DB_CHANGE_GUIDE.md"
        process_resources = self.repo_root / "doc/process/resources"
        
        if db_change_guide.exists():
            self.check_main_file(db_change_guide, process_resources)
            self.check_resources_index_table(db_change_guide)
        
        # 
        print(f"\n{BLUE}{'='*60}{NC}")
        print(f"{BLUE}{NC}")
        print(f"{BLUE}{'='*60}{NC}")
        
        print(f"\n📊 :")
        print(f"  : {self.stats['main_files_checked']}")
        print(f"  Resources: {self.stats['resources_found']}")
        print(f"  Resources: {self.stats['resources_missing']}")
        print(f"  Resources: {self.stats['resources_oversized']}")
        
        # 
        if self.issues:
            print(f"\n{RED}❌  {len(self.issues)} :{NC}")
            for issue in self.issues:
                print(f"  - {issue}")
        
        if self.warnings:
            print(f"\n{YELLOW}⚠️   {len(self.warnings)} :{NC}")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        # 
        print(f"\n{BLUE}{'='*60}{NC}")
        if not self.issues:
            print(f"{GREEN}✅ Resources{NC}")
            print(f"{BLUE}{'='*60}{NC}\n")
            return True
        else:
            print(f"{RED}❌ Resources{NC}")
            print(f"{BLUE}{'='*60}{NC}\n")
            return False


def main():
    """"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Resources',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--repo-root', type=str, default='.',
                       help='')
    
    args = parser.parse_args()
    
    # 
    checker = ResourcesChecker(args.repo_root)
    success = checker.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

