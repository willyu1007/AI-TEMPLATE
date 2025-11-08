#!/usr/bin/env python3
"""
resources_check.py - Resources文件完整性检查

检查渐进式披露文档的resources结构：
  - 主文件Resources索引表完整性
  - Resource文件实际存在
  - Resource文件大小控制（建议≤250行）
  - 主文件与resources引用关系正确

用法:
    python scripts/resources_check.py
    make resources_check

Created: 2025-11-08 (Phase 10.5)
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple

# ANSI颜色
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


class ResourcesChecker:
    """Resources文件检查器"""
    
    def __init__(self, repo_root: str = "."):
        """初始化"""
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
        检查主文件及其resources
        
        Args:
            main_file_path: 主文件路径
            resources_dir: resources目录路径
        
        Returns:
            True if检查通过
        """
        if not main_file_path.exists():
            self.issues.append(f"主文件不存在: {main_file_path}")
            return False
        
        self.stats["main_files_checked"] += 1
        
        print(f"\n{'='*60}")
        print(f"检查主文件: {main_file_path.relative_to(self.repo_root)}")
        print(f"{'='*60}")
        
        # 读取主文件
        try:
            with open(main_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.issues.append(f"读取主文件失败: {main_file_path} - {e}")
            return False
        
        # 检查主文件大小
        line_count = len(content.split('\n'))
        if line_count > 350:
            self.warnings.append(f"主文件较大: {main_file_path} ({line_count}行，建议≤300行)")
            print(f"{YELLOW}⚠️{NC}  主文件: {line_count}行（建议≤300行）")
        else:
            print(f"{GREEN}✓{NC} 主文件: {line_count}行")
        
        # 查找resources引用
        resource_pattern = r'\[([^\]]+)\]\(resources/([^)]+\.md)\)'
        matches = re.findall(resource_pattern, content)
        
        if not matches:
            print(f"{YELLOW}ℹ️{NC}  未找到resources引用（可能不需要）")
            return True
        
        print(f"\n找到 {len(matches)} 个resource引用:")
        
        # 检查每个resource
        all_exist = True
        for title, resource_file in matches:
            resource_path = resources_dir / resource_file
            
            if not resource_path.exists():
                self.issues.append(f"Resource文件不存在: {resource_path}")
                print(f"{RED}✗{NC} {resource_file} - 文件不存在")
                self.stats["resources_missing"] += 1
                all_exist = False
            else:
                # 检查文件大小
                try:
                    with open(resource_path, 'r', encoding='utf-8') as f:
                        resource_content = f.read()
                    resource_lines = len(resource_content.split('\n'))
                    
                    if resource_lines > 250:
                        self.warnings.append(
                            f"Resource文件较大: {resource_path} ({resource_lines}行，建议≤250行)"
                        )
                        print(f"{YELLOW}⚠️{NC}  {resource_file} - {resource_lines}行（建议≤250行）")
                        self.stats["resources_oversized"] += 1
                    else:
                        print(f"{GREEN}✓{NC} {resource_file} - {resource_lines}行")
                    
                    self.stats["resources_found"] += 1
                except Exception as e:
                    self.warnings.append(f"读取resource失败: {resource_path} - {e}")
        
        # 检查resources目录中是否有未引用的文件
        if resources_dir.exists():
            resource_files_in_dir = set(f.name for f in resources_dir.glob('*.md'))
            referenced_files = set(resource_file for _, resource_file in matches)
            
            unreferenced = resource_files_in_dir - referenced_files
            if unreferenced:
                print(f"\n{YELLOW}⚠️{NC}  未引用的resource文件:")
                for f in unreferenced:
                    print(f"  - {f}")
                    self.warnings.append(f"未引用的resource: {resources_dir / f}")
        
        return all_exist
    
    def check_resources_index_table(self, main_file_path: Path) -> bool:
        """检查主文件是否有Resources索引表"""
        try:
            with open(main_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return False
        
        # 查找表格
        table_patterns = [
            r'\| Resource \| 内容 \| 何时阅读 \|',
            r'## Resources索引',
            r'### Resources索引'
        ]
        
        has_index = any(re.search(pattern, content) for pattern in table_patterns)
        
        if has_index:
            print(f"{GREEN}✓{NC} 包含Resources索引表")
        else:
            self.warnings.append(f"建议添加Resources索引表: {main_file_path}")
            print(f"{YELLOW}⚠️{NC}  未找到Resources索引表（建议添加）")
        
        return has_index
    
    def run(self) -> bool:
        """运行完整检查"""
        print(f"\n{BLUE}{'='*60}{NC}")
        print(f"{BLUE}Resources文件完整性检查{NC}")
        print(f"{BLUE}{'='*60}{NC}")
        
        # 检查MODULE_INIT_GUIDE.md
        module_init_guide = self.repo_root / "doc/modules/MODULE_INIT_GUIDE.md"
        module_resources = self.repo_root / "doc/modules/resources"
        
        if module_init_guide.exists():
            self.check_main_file(module_init_guide, module_resources)
            self.check_resources_index_table(module_init_guide)
        
        # 检查DB_CHANGE_GUIDE.md
        db_change_guide = self.repo_root / "doc/process/DB_CHANGE_GUIDE.md"
        process_resources = self.repo_root / "doc/process/resources"
        
        if db_change_guide.exists():
            self.check_main_file(db_change_guide, process_resources)
            self.check_resources_index_table(db_change_guide)
        
        # 汇总报告
        print(f"\n{BLUE}{'='*60}{NC}")
        print(f"{BLUE}检查汇总{NC}")
        print(f"{BLUE}{'='*60}{NC}")
        
        print(f"\n📊 统计:")
        print(f"  主文件检查: {self.stats['main_files_checked']}")
        print(f"  Resources找到: {self.stats['resources_found']}")
        print(f"  Resources缺失: {self.stats['resources_missing']}")
        print(f"  Resources超大: {self.stats['resources_oversized']}")
        
        # 问题汇总
        if self.issues:
            print(f"\n{RED}❌ 发现 {len(self.issues)} 个问题:{NC}")
            for issue in self.issues:
                print(f"  - {issue}")
        
        if self.warnings:
            print(f"\n{YELLOW}⚠️  发现 {len(self.warnings)} 个警告:{NC}")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        # 结论
        print(f"\n{BLUE}{'='*60}{NC}")
        if not self.issues:
            print(f"{GREEN}✅ Resources检查通过{NC}")
            print(f"{BLUE}{'='*60}{NC}\n")
            return True
        else:
            print(f"{RED}❌ Resources检查失败{NC}")
            print(f"{BLUE}{'='*60}{NC}\n")
            return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Resources文件完整性检查',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--repo-root', type=str, default='.',
                       help='仓库根目录路径')
    
    args = parser.parse_args()
    
    # 运行检查
    checker = ResourcesChecker(args.repo_root)
    success = checker.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

