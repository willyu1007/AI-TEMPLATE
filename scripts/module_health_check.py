#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module_health_check.py - 模块文档完整性检查工具

功能：
1. 检查每个模块是否有agent.md
2. 检查每个模块的必需文档（CONTRACT.md, CHANGELOG.md, RUNBOOK.md等）
3. 检查agent.md是否有有效的YAML front matter
4. 检查agent.md是否定义了context_routes
5. 计算模块文档覆盖率

必需文档列表（根据HEALTH_CHECK_MODEL.yaml）：
- agent.md
- doc/CONTRACT.md
- doc/CHANGELOG.md
- doc/RUNBOOK.md
- doc/BUGS.md
- doc/PROGRESS.md
- doc/TEST_PLAN.md

用法：
    python scripts/module_health_check.py
    python scripts/module_health_check.py --json
    python scripts/module_health_check.py --module common
    make module_health_check

Created: 2025-11-09 (Phase 14.2)
"""

import os
import sys
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
MODULES_DIR = REPO_ROOT / "modules"

# 必需文档列表
REQUIRED_DOCS = [
    "agent.md",
    "doc/CONTRACT.md",
    "doc/CHANGELOG.md",
    "doc/RUNBOOK.md",
    "doc/BUGS.md",
    "doc/PROGRESS.md",
    "doc/TEST_PLAN.md"
]


class ModuleHealthChecker:
    """模块健康度检查器"""
    
    def __init__(self):
        """初始化检查器"""
        self.results = {
            "total_modules": 0,
            "complete_modules": 0,
            "incomplete_modules": 0,
            "coverage_percentage": 0,
            "completeness_percentage": 0,
            "modules": {}
        }
    
    def find_all_modules(self) -> List[Path]:
        """查找所有模块目录"""
        if not MODULES_DIR.exists():
            return []
        
        modules = []
        for item in MODULES_DIR.iterdir():
            if item.is_dir() and not item.name.startswith('.') and not item.name.startswith('_'):
                # 检查是否有agent.md或doc目录
                if (item / "agent.md").exists() or (item / "doc").exists():
                    modules.append(item)
        
        return modules
    
    def check_module(self, module_path: Path) -> Dict[str, Any]:
        """检查单个模块的文档完整性"""
        module_name = module_path.name
        
        result = {
            "name": module_name,
            "path": str(module_path.relative_to(REPO_ROOT)),
            "has_agent_md": False,
            "agent_md_valid": False,
            "has_context_routes": False,
            "missing_docs": [],
            "existing_docs": [],
            "completeness": 0,
            "status": "incomplete"
        }
        
        # 检查agent.md
        agent_md_path = module_path / "agent.md"
        if agent_md_path.exists():
            result["has_agent_md"] = True
            result["existing_docs"].append("agent.md")
            
            # 检查YAML front matter
            try:
                with open(agent_md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取YAML front matter
                match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
                if match:
                    yaml_content = yaml.safe_load(match.group(1))
                    result["agent_md_valid"] = True
                    
                    # 检查是否有context_routes
                    if "context_routing" in yaml_content or "context_routes" in yaml_content:
                        result["has_context_routes"] = True
            except Exception as e:
                result["agent_md_error"] = str(e)
        else:
            result["missing_docs"].append("agent.md")
        
        # 检查其他必需文档
        for doc in REQUIRED_DOCS[1:]:  # 跳过agent.md
            doc_path = module_path / doc
            if doc_path.exists():
                result["existing_docs"].append(doc)
            else:
                result["missing_docs"].append(doc)
        
        # 计算完整度
        result["completeness"] = (len(result["existing_docs"]) / len(REQUIRED_DOCS)) * 100
        
        # 判断状态
        if result["completeness"] == 100:
            result["status"] = "complete"
        elif result["completeness"] >= 70:
            result["status"] = "good"
        elif result["completeness"] >= 50:
            result["status"] = "fair"
        else:
            result["status"] = "incomplete"
        
        return result
    
    def check_all_modules(self):
        """检查所有模块"""
        print("🔍 检查所有模块的文档完整性...")
        
        modules = self.find_all_modules()
        self.results["total_modules"] = len(modules)
        
        if len(modules) == 0:
            print("  ⚠️ 未找到任何模块")
            return
        
        print(f"  找到 {len(modules)} 个模块\n")
        
        for module_path in modules:
            result = self.check_module(module_path)
            self.results["modules"][result["name"]] = result
            
            # 统计完整模块
            if result["status"] == "complete":
                self.results["complete_modules"] += 1
            else:
                self.results["incomplete_modules"] += 1
        
        # 计算覆盖率（有agent.md的模块比例）
        modules_with_agent_md = sum(1 for m in self.results["modules"].values() if m["has_agent_md"])
        self.results["coverage_percentage"] = (modules_with_agent_md / len(modules) * 100) if len(modules) > 0 else 0
        
        # 计算完整性（所有必需文档都存在的模块比例）
        self.results["completeness_percentage"] = (self.results["complete_modules"] / len(modules) * 100) if len(modules) > 0 else 0
    
    def print_console_report(self):
        """打印控制台报告"""
        print("\n" + "=" * 70)
        print("📊 MODULE HEALTH CHECK REPORT")
        print("=" * 70)
        
        print(f"\n📈 Overall Statistics:")
        print(f"  总模块数: {self.results['total_modules']}")
        print(f"  完整模块: {self.results['complete_modules']}")
        print(f"  不完整模块: {self.results['incomplete_modules']}")
        print(f"  agent.md覆盖率: {self.results['coverage_percentage']:.1f}%")
        print(f"  文档完整性: {self.results['completeness_percentage']:.1f}%")
        
        # 按状态分组显示模块
        complete = [m for m in self.results["modules"].values() if m["status"] == "complete"]
        good = [m for m in self.results["modules"].values() if m["status"] == "good"]
        fair = [m for m in self.results["modules"].values() if m["status"] == "fair"]
        incomplete = [m for m in self.results["modules"].values() if m["status"] == "incomplete"]
        
        if complete:
            print(f"\n✅ 完整模块 ({len(complete)}):")
            for m in complete:
                print(f"  - {m['name']} ({m['completeness']:.0f}%)")
        
        if good:
            print(f"\n⚠️ 良好模块 ({len(good)}):")
            for m in good:
                print(f"  - {m['name']} ({m['completeness']:.0f}%)")
                if m["missing_docs"]:
                    print(f"    缺失: {', '.join(m['missing_docs'][:3])}")
        
        if fair:
            print(f"\n⚠️ 一般模块 ({len(fair)}):")
            for m in fair:
                print(f"  - {m['name']} ({m['completeness']:.0f}%)")
                if m["missing_docs"]:
                    print(f"    缺失: {', '.join(m['missing_docs'][:3])}")
        
        if incomplete:
            print(f"\n❌ 不完整模块 ({len(incomplete)}):")
            for m in incomplete:
                print(f"  - {m['name']} ({m['completeness']:.0f}%)")
                if m["missing_docs"]:
                    print(f"    缺失: {', '.join(m['missing_docs'][:5])}")
        
        print("\n" + "=" * 70)
    
    def print_module_detail(self, module_name: str):
        """打印单个模块的详细信息"""
        if module_name not in self.results["modules"]:
            print(f"❌ 模块 '{module_name}' 不存在", file=sys.stderr)
            return
        
        m = self.results["modules"][module_name]
        
        print(f"\n📦 模块: {m['name']}")
        print(f"路径: {m['path']}")
        print(f"状态: {m['status']}")
        print(f"完整度: {m['completeness']:.0f}%")
        
        print(f"\n✅ 存在的文档 ({len(m['existing_docs'])}):")
        for doc in m["existing_docs"]:
            print(f"  - {doc}")
        
        if m["missing_docs"]:
            print(f"\n❌ 缺失的文档 ({len(m['missing_docs'])}):")
            for doc in m["missing_docs"]:
                print(f"  - {doc}")
        
        print(f"\nagent.md检查:")
        print(f"  有agent.md: {'✅' if m['has_agent_md'] else '❌'}")
        print(f"  YAML有效: {'✅' if m['agent_md_valid'] else '❌'}")
        print(f"  有context_routes: {'✅' if m['has_context_routes'] else '❌'}")
    
    def print_json_report(self):
        """打印JSON报告"""
        print(json.dumps(self.results, indent=2, ensure_ascii=False))


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Module Health Check")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    parser.add_argument("--module", type=str, help="检查指定模块")
    
    args = parser.parse_args()
    
    checker = ModuleHealthChecker()
    checker.check_all_modules()
    
    if args.json:
        checker.print_json_report()
    elif args.module:
        checker.print_module_detail(args.module)
    else:
        checker.print_console_report()
    
    # 根据完整性决定退出码
    if checker.results["completeness_percentage"] < 70:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

