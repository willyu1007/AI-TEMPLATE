#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
coupling_check.py - 


1. 
2. /
3. 
4. 

HEALTH_CHECK_MODEL.yaml
- Low (0-3 dependencies): 
- Medium (4-6 dependencies): 
- High (7-10 dependencies): 
- Very High (>10 dependencies): 


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

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
MODULES_DIR = REPO_ROOT / "modules"
REGISTRY_PATH = REPO_ROOT / "doc" / "orchestration" / "registry.yaml"


class CouplingChecker:
    """"""
    
    def __init__(self):
        """"""
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
        """"""
        if not REGISTRY_PATH.exists():
            print(f"⚠️ : {REGISTRY_PATH.relative_to(REPO_ROOT)}", file=sys.stderr)
            return None
        
        try:
            with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            return data
        except Exception as e:
            print(f"❌ : {e}", file=sys.stderr)
            return None
    
    def analyze_module_dependencies_from_registry(self, registry: Dict):
        """"""
        modules = registry.get("module_instances", [])
        
        for module in modules:
            module_id = module.get("id", "unknown")
            dependencies = module.get("dependencies", [])
            
            # 
            for dep in dependencies:
                self.module_dependencies[module_id].add(dep)
                self.module_dependents[dep].add(module_id)
    
    def analyze_module_dependencies_from_code(self):
        """import"""
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
        """import"""
        dependencies = set()
        
        # Python
        py_files = list(module_dir.glob("**/*.py"))
        
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                #  from modules.xxx import
                pattern1 = r'from modules\.(\w+)'
                matches1 = re.findall(pattern1, content)
                dependencies.update(matches1)
                
                #  import modules.xxx
                pattern2 = r'import modules\.(\w+)'
                matches2 = re.findall(pattern2, content)
                dependencies.update(matches2)
                
            except Exception:
                continue
        
        # 
        dependencies.discard(module_dir.name)
        
        return dependencies
    
    def calculate_coupling_metrics(self):
        """"""
        print("🔍 ...")
        
        # 
        all_modules = set(self.module_dependencies.keys()) | set(self.module_dependents.keys())
        self.results["total_modules"] = len(all_modules)
        
        if len(all_modules) == 0:
            print("  ⚠️ ")
            return
        
        print(f"   {len(all_modules)} \n")
        
        total_dependencies = 0
        
        for module in all_modules:
            dependencies = self.module_dependencies.get(module, set())
            dependents = self.module_dependents.get(module, set())
            
            dep_count = len(dependencies)
            dependent_count = len(dependents)
            total_coupling = dep_count + dependent_count
            
            total_dependencies += dep_count
            
            # 
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
            
            # 
            if coupling_level in ["high", "very_high"]:
                self.results["high_coupling_modules"].append(module)
            elif coupling_level == "low":
                self.results["low_coupling_modules"].append(module)
        
        # 
        if len(all_modules) > 0:
            self.results["average_dependencies"] = total_dependencies / len(all_modules)
        
        # 
        if self.results["average_dependencies"] <= 3:
            self.results["coupling_level"] = "low"
        elif self.results["average_dependencies"] <= 6:
            self.results["coupling_level"] = "medium"
        elif self.results["average_dependencies"] <= 10:
            self.results["coupling_level"] = "high"
        else:
            self.results["coupling_level"] = "very_high"
    
    def _get_coupling_status(self, coupling_level: str) -> str:
        """"""
        if coupling_level == "low":
            return "✅ "
        elif coupling_level == "medium":
            return "⚠️ "
        elif coupling_level == "high":
            return "❌ "
        else:
            return "🚨 "
    
    def run_analysis(self):
        """"""
        # 
        registry = self.load_registry()
        if registry:
            self.analyze_module_dependencies_from_registry(registry)
        
        # 
        self.analyze_module_dependencies_from_code()
        
        # 
        self.calculate_coupling_metrics()
    
    def print_console_report(self):
        """"""
        print("\n" + "=" * 70)
        print("📊 MODULE COUPLING ANALYSIS REPORT")
        print("=" * 70)
        
        print(f"\n📈 Overall Metrics:")
        print(f"  : {self.results['total_modules']}")
        print(f"  : {self.results['average_dependencies']:.1f}")
        print(f"  : {self.results['coupling_level']}")
        print(f"  : {len(self.results['high_coupling_modules'])}")
        print(f"  : {len(self.results['low_coupling_modules'])}")
        
        # 
        if self.results["high_coupling_modules"]:
            print(f"\n⚠️  ({len(self.results['high_coupling_modules'])}):")
            for module_name in self.results["high_coupling_modules"]:
                module = self.results["modules"][module_name]
                print(f"  - {module_name}: {module['total_coupling']}  "
                      f"({module['dependency_count']} + {module['dependent_count']})")
        
        # 
        if self.results["low_coupling_modules"]:
            low_count = len(self.results["low_coupling_modules"])
            show_count = min(5, low_count)
            print(f"\n✅  ({show_count}/{low_count}):")
            for module_name in self.results["low_coupling_modules"][:show_count]:
                module = self.results["modules"][module_name]
                print(f"  - {module_name}: {module['total_coupling']} ")
        
        # 
        print(f"\n💡 :")
        if self.results["coupling_level"] in ["high", "very_high"]:
            print("  - ")
            print("  - common")
            print("  - ")
        elif self.results["coupling_level"] == "medium":
            print("  - ")
            print("  - ")
        else:
            print("  - ")
        
        print("\n" + "=" * 70)
    
    def print_module_detail(self, module_name: str):
        """"""
        if module_name not in self.results["modules"]:
            print(f"❌  '{module_name}' ", file=sys.stderr)
            return
        
        m = self.results["modules"][module_name]
        
        print(f"\n📦 : {m['name']}")
        print(f": {m['coupling_level']}")
        print(f": {m['total_coupling']}")
        print(f": {m['status']}")
        
        if m["dependencies"]:
            print(f"\n➡️  ({m['dependency_count']}):")
            for dep in m["dependencies"]:
                print(f"  - {dep}")
        else:
            print(f"\n➡️ ")
        
        if m["dependents"]:
            print(f"\n⬅️  ({m['dependent_count']}):")
            for dep in m["dependents"]:
                print(f"  - {dep}")
        else:
            print(f"\n⬅️ ")
    
    def print_json_report(self):
        """JSON"""
        print(json.dumps(self.results, indent=2, ensure_ascii=False))


def main():
    """"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Module Coupling Check")
    parser.add_argument("--json", action="store_true", help="JSON")
    parser.add_argument("--module", type=str, help="")
    
    args = parser.parse_args()
    
    checker = CouplingChecker()
    checker.run_analysis()
    
    if args.json:
        checker.print_json_report()
    elif args.module:
        checker.print_module_detail(args.module)
    else:
        checker.print_console_report()
    
    # 
    if checker.results["coupling_level"] in ["high", "very_high"]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

