#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
coupling_check.py - 模块耦合度分析工具

功能：
1. 分析模块间的依赖关系
2. 计算每个模块的依赖数量（扇入/扇出）
3. 识别高耦合模块
4. 评估整体耦合度水平

耦合度级别（根据HEALTH_CHECK_MODEL.yaml）：
- Low (0-3 dependencies): 低耦合，优秀
- Medium (4-6 dependencies): 中等耦合，可接受
- High (7-10 dependencies): 高耦合，需要重构
- Very High (>10 dependencies): 极高耦合，关键问题

用法：
    python scripts/coupling_check.py
    python scripts/coupling_check.py --json
    python scripts/coupling_check.py --module common
    make coupling_check

Created: 2025-11-09 (Phase 14.2)
"""

import os
import sys
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from collections import defaultdict

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
MODULES_DIR = REPO_ROOT / "modules"
REGISTRY_PATH = REPO_ROOT / "doc" / "orchestration" / "registry.yaml"


class CouplingChecker:
    """耦合度检查器"""
    
    def __init__(self):
        """初始化检查器"""
        self.results = {
            "total_modules": 0,
            "coupling_level": "unknown",
            "average_dependencies": 0,
            "modules": {},
            "high_coupling_modules": [],
            "low_coupling_modules": []
        }
        self.module_dependencies = defaultdict(set)
        self.module_dependents = defaultdict(set)
    
    def load_registry(self) -> Optional[Dict]:
        """加载模块注册表"""
        if not REGISTRY_PATH.exists():
            print(f"⚠️ 注册表不存在: {REGISTRY_PATH.relative_to(REPO_ROOT)}", file=sys.stderr)
            return None
        
        try:
            with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            return data
        except Exception as e:
            print(f"❌ 加载注册表失败: {e}", file=sys.stderr)
            return None
    
    def analyze_module_dependencies_from_registry(self, registry: Dict):
        """从注册表分析模块依赖"""
        modules = registry.get("module_instances", [])
        
        for module in modules:
            module_id = module.get("id", "unknown")
            dependencies = module.get("dependencies", [])
            
            # 记录依赖关系
            for dep in dependencies:
                self.module_dependencies[module_id].add(dep)
                self.module_dependents[dep].add(module_id)
    
    def analyze_module_dependencies_from_code(self):
        """从代码分析模块依赖（通过import语句）"""
        if not MODULES_DIR.exists():
            return
        
        for module_dir in MODULES_DIR.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith('.'):
                continue
            
            module_name = module_dir.name
            dependencies = self._find_imports_in_module(module_dir)
            
            for dep in dependencies:
                self.module_dependencies[module_name].add(dep)
                self.module_dependents[dep].add(module_name)
    
    def _find_imports_in_module(self, module_dir: Path) -> Set[str]:
        """在模块目录中查找import语句"""
        dependencies = set()
        
        # 查找所有Python文件
        py_files = list(module_dir.glob("**/*.py"))
        
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 查找 from modules.xxx import
                pattern1 = r'from modules\.(\w+)'
                matches1 = re.findall(pattern1, content)
                dependencies.update(matches1)
                
                # 查找 import modules.xxx
                pattern2 = r'import modules\.(\w+)'
                matches2 = re.findall(pattern2, content)
                dependencies.update(matches2)
                
            except Exception:
                continue
        
        # 移除自己
        dependencies.discard(module_dir.name)
        
        return dependencies
    
    def calculate_coupling_metrics(self):
        """计算耦合度指标"""
        print("🔍 分析模块耦合度...")
        
        # 合并所有模块
        all_modules = set(self.module_dependencies.keys()) | set(self.module_dependents.keys())
        self.results["total_modules"] = len(all_modules)
        
        if len(all_modules) == 0:
            print("  ⚠️ 未找到任何模块")
            return
        
        print(f"  找到 {len(all_modules)} 个模块\n")
        
        total_dependencies = 0
        
        for module in all_modules:
            dependencies = self.module_dependencies.get(module, set())
            dependents = self.module_dependents.get(module, set())
            
            dep_count = len(dependencies)
            dependent_count = len(dependents)
            total_coupling = dep_count + dependent_count
            
            total_dependencies += dep_count
            
            # 确定耦合级别
            if total_coupling <= 3:
                coupling_level = "low"
            elif total_coupling <= 6:
                coupling_level = "medium"
            elif total_coupling <= 10:
                coupling_level = "high"
            else:
                coupling_level = "very_high"
            
            module_result = {
                "name": module,
                "dependencies": list(dependencies),
                "dependents": list(dependents),
                "dependency_count": dep_count,
                "dependent_count": dependent_count,
                "total_coupling": total_coupling,
                "coupling_level": coupling_level,
                "status": self._get_coupling_status(coupling_level)
            }
            
            self.results["modules"][module] = module_result
            
            # 分类
            if coupling_level in ["high", "very_high"]:
                self.results["high_coupling_modules"].append(module)
            elif coupling_level == "low":
                self.results["low_coupling_modules"].append(module)
        
        # 计算平均依赖数
        if len(all_modules) > 0:
            self.results["average_dependencies"] = total_dependencies / len(all_modules)
        
        # 确定整体耦合级别
        if self.results["average_dependencies"] <= 3:
            self.results["coupling_level"] = "low"
        elif self.results["average_dependencies"] <= 6:
            self.results["coupling_level"] = "medium"
        elif self.results["average_dependencies"] <= 10:
            self.results["coupling_level"] = "high"
        else:
            self.results["coupling_level"] = "very_high"
    
    def _get_coupling_status(self, coupling_level: str) -> str:
        """获取耦合状态标记"""
        if coupling_level == "low":
            return "✅ 低耦合"
        elif coupling_level == "medium":
            return "⚠️ 中等耦合"
        elif coupling_level == "high":
            return "❌ 高耦合"
        else:
            return "🚨 极高耦合"
    
    def run_analysis(self):
        """运行耦合度分析"""
        # 尝试从注册表加载
        registry = self.load_registry()
        if registry:
            self.analyze_module_dependencies_from_registry(registry)
        
        # 从代码分析
        self.analyze_module_dependencies_from_code()
        
        # 计算指标
        self.calculate_coupling_metrics()
    
    def print_console_report(self):
        """打印控制台报告"""
        print("\n" + "=" * 70)
        print("📊 MODULE COUPLING ANALYSIS REPORT")
        print("=" * 70)
        
        print(f"\n📈 Overall Metrics:")
        print(f"  总模块数: {self.results['total_modules']}")
        print(f"  平均依赖数: {self.results['average_dependencies']:.1f}")
        print(f"  整体耦合度: {self.results['coupling_level']}")
        print(f"  高耦合模块: {len(self.results['high_coupling_modules'])}")
        print(f"  低耦合模块: {len(self.results['low_coupling_modules'])}")
        
        # 高耦合模块警告
        if self.results["high_coupling_modules"]:
            print(f"\n⚠️ 高耦合模块 ({len(self.results['high_coupling_modules'])}):")
            for module_name in self.results["high_coupling_modules"]:
                module = self.results["modules"][module_name]
                print(f"  - {module_name}: {module['total_coupling']} 耦合 "
                      f"({module['dependency_count']}出 + {module['dependent_count']}入)")
        
        # 低耦合模块（表扬）
        if self.results["low_coupling_modules"]:
            low_count = len(self.results["low_coupling_modules"])
            show_count = min(5, low_count)
            print(f"\n✅ 低耦合模块 (显示{show_count}/{low_count}):")
            for module_name in self.results["low_coupling_modules"][:show_count]:
                module = self.results["modules"][module_name]
                print(f"  - {module_name}: {module['total_coupling']} 耦合")
        
        # 建议
        print(f"\n💡 建议:")
        if self.results["coupling_level"] in ["high", "very_high"]:
            print("  - 识别并重构高耦合模块")
            print("  - 提取共享逻辑到common模块")
            print("  - 审查并简化模块间依赖关系")
        elif self.results["coupling_level"] == "medium":
            print("  - 当前耦合度可接受")
            print("  - 关注高耦合模块，避免继续增加依赖")
        else:
            print("  - 耦合度控制良好，继续保持！")
        
        print("\n" + "=" * 70)
    
    def print_module_detail(self, module_name: str):
        """打印单个模块的耦合详情"""
        if module_name not in self.results["modules"]:
            print(f"❌ 模块 '{module_name}' 不存在", file=sys.stderr)
            return
        
        m = self.results["modules"][module_name]
        
        print(f"\n📦 模块: {m['name']}")
        print(f"耦合级别: {m['coupling_level']}")
        print(f"总耦合度: {m['total_coupling']}")
        print(f"状态: {m['status']}")
        
        if m["dependencies"]:
            print(f"\n➡️ 依赖 ({m['dependency_count']}):")
            for dep in m["dependencies"]:
                print(f"  - {dep}")
        else:
            print(f"\n➡️ 无依赖")
        
        if m["dependents"]:
            print(f"\n⬅️ 被依赖 ({m['dependent_count']}):")
            for dep in m["dependents"]:
                print(f"  - {dep}")
        else:
            print(f"\n⬅️ 未被依赖")
    
    def print_json_report(self):
        """打印JSON报告"""
        print(json.dumps(self.results, indent=2, ensure_ascii=False))


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Module Coupling Check")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    parser.add_argument("--module", type=str, help="查看指定模块详情")
    
    args = parser.parse_args()
    
    checker = CouplingChecker()
    checker.run_analysis()
    
    if args.json:
        checker.print_json_report()
    elif args.module:
        checker.print_module_detail(args.module)
    else:
        checker.print_console_report()
    
    # 根据耦合度决定退出码
    if checker.results["coupling_level"] in ["high", "very_high"]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

