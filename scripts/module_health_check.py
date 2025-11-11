#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module_health_check.py - 


1. AGENTS.md
2. CONTRACT.md, CHANGELOG.md, RUNBOOK.md
3. AGENTS.mdYAML front matter
4. AGENTS.mdcontext_routes
5. 

HEALTH_CHECK_MODEL.yaml
- AGENTS.md
- doc/CONTRACT.md
- doc/CHANGELOG.md
- doc/RUNBOOK.md
- doc/BUGS.md
- doc/PROGRESS.md
- doc/TEST_PLAN.md


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

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
MODULES_DIR = REPO_ROOT / "modules"

# 
REQUIRED_DOCS = [
    "AGENTS.md",
    "doc/CONTRACT.md",
    "doc/CHANGELOG.md",
    "doc/RUNBOOK.md",
    "doc/BUGS.md",
    "doc/PROGRESS.md",
    "doc/TEST_PLAN.md"
]


class ModuleHealthChecker:
    """"""
    
    def __init__(self):
        """"""
        self.results = {
            "total_modules": 0,
            "complete_modules": 0,
            "incomplete_modules": 0,
            "coverage_percentage": 0,
            "completeness_percentage": 0,
            "modules": {}
        }
    
    def find_all_modules(self) -> List[Path]:
        """"""
        if not MODULES_DIR.exists():
            return []
        
        modules = []
        for item in MODULES_DIR.iterdir():
            if item.is_dir() and not item.name.startswith('.') and not item.name.startswith('_'):
                # AGENTS.mddoc
                if (item / "AGENTS.md").exists() or (item / "doc").exists():
                    modules.append(item)
        
        return modules
    
    def check_module(self, module_path: Path) -> Dict[str, Any]:
        """"""
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
        
        # AGENTS.md
        agent_md_path = module_path / "AGENTS.md"
        if agent_md_path.exists():
            result["has_agent_md"] = True
            result["existing_docs"].append("AGENTS.md")
            
            # YAML front matter
            try:
                with open(agent_md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # YAML front matter
                match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
                if match:
                    yaml_content = yaml.safe_load(match.group(1))
                    result["agent_md_valid"] = True
                    
                    # context_routes
                    if "context_routing" in yaml_content or "context_routes" in yaml_content:
                        result["has_context_routes"] = True
            except Exception as e:
                result["agent_md_error"] = str(e)
        else:
            result["missing_docs"].append("AGENTS.md")
        
        # 
        for doc in REQUIRED_DOCS[1:]:  # AGENTS.md
            doc_path = module_path / doc
            if doc_path.exists():
                result["existing_docs"].append(doc)
            else:
                result["missing_docs"].append(doc)
        
        # 
        result["completeness"] = (len(result["existing_docs"]) / len(REQUIRED_DOCS)) * 100
        
        # 
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
        """"""
        print("🔍 ...")
        
        modules = self.find_all_modules()
        self.results["total_modules"] = len(modules)
        
        if len(modules) == 0:
            print("  ⚠️ ")
            return
        
        print(f"   {len(modules)} \n")
        
        for module_path in modules:
            result = self.check_module(module_path)
            self.results["modules"][result["name"]] = result
            
            # 
            if result["status"] == "complete":
                self.results["complete_modules"] += 1
            else:
                self.results["incomplete_modules"] += 1
        
        # AGENTS.md
        modules_with_agent_md = sum(1 for m in self.results["modules"].values() if m["has_agent_md"])
        self.results["coverage_percentage"] = (modules_with_agent_md / len(modules) * 100) if len(modules) > 0 else 0
        
        # 
        self.results["completeness_percentage"] = (self.results["complete_modules"] / len(modules) * 100) if len(modules) > 0 else 0
    
    def print_console_report(self):
        """"""
        print("\n" + "=" * 70)
        print("📊 MODULE HEALTH CHECK REPORT")
        print("=" * 70)
        
        print(f"\n📈 Overall Statistics:")
        print(f"  : {self.results['total_modules']}")
        print(f"  : {self.results['complete_modules']}")
        print(f"  : {self.results['incomplete_modules']}")
        print(f"  AGENTS.md: {self.results['coverage_percentage']:.1f}%")
        print(f"  : {self.results['completeness_percentage']:.1f}%")
        
        # 
        complete = [m for m in self.results["modules"].values() if m["status"] == "complete"]
        good = [m for m in self.results["modules"].values() if m["status"] == "good"]
        fair = [m for m in self.results["modules"].values() if m["status"] == "fair"]
        incomplete = [m for m in self.results["modules"].values() if m["status"] == "incomplete"]
        
        if complete:
            print(f"\n✅  ({len(complete)}):")
            for m in complete:
                print(f"  - {m['name']} ({m['completeness']:.0f}%)")
        
        if good:
            print(f"\n⚠️  ({len(good)}):")
            for m in good:
                print(f"  - {m['name']} ({m['completeness']:.0f}%)")
                if m["missing_docs"]:
                    print(f"    : {', '.join(m['missing_docs'][:3])}")
        
        if fair:
            print(f"\n⚠️  ({len(fair)}):")
            for m in fair:
                print(f"  - {m['name']} ({m['completeness']:.0f}%)")
                if m["missing_docs"]:
                    print(f"    : {', '.join(m['missing_docs'][:3])}")
        
        if incomplete:
            print(f"\n❌  ({len(incomplete)}):")
            for m in incomplete:
                print(f"  - {m['name']} ({m['completeness']:.0f}%)")
                if m["missing_docs"]:
                    print(f"    : {', '.join(m['missing_docs'][:5])}")
        
        print("\n" + "=" * 70)
    
    def print_module_detail(self, module_name: str):
        """"""
        if module_name not in self.results["modules"]:
            print(f"❌  '{module_name}' ", file=sys.stderr)
            return
        
        m = self.results["modules"][module_name]
        
        print(f"\n📦 : {m['name']}")
        print(f": {m['path']}")
        print(f": {m['status']}")
        print(f": {m['completeness']:.0f}%")
        
        print(f"\n✅  ({len(m['existing_docs'])}):")
        for doc in m["existing_docs"]:
            print(f"  - {doc}")
        
        if m["missing_docs"]:
            print(f"\n❌  ({len(m['missing_docs'])}):")
            for doc in m["missing_docs"]:
                print(f"  - {doc}")
        
        print(f"\nAGENTS.md:")
        print(f"  AGENTS.md: {'✅' if m['has_agent_md'] else '❌'}")
        print(f"  YAML: {'✅' if m['agent_md_valid'] else '❌'}")
        print(f"  context_routes: {'✅' if m['has_context_routes'] else '❌'}")
    
    def print_json_report(self):
        """JSON"""
        print(json.dumps(self.results, indent=2, ensure_ascii=False))


def main():
    """"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Module Health Check")
    parser.add_argument("--json", action="store_true", help="JSON")
    parser.add_argument("--module", type=str, help="")
    
    args = parser.parse_args()
    
    checker = ModuleHealthChecker()
    checker.check_all_modules()
    
    if args.json:
        checker.print_json_report()
    elif args.module:
        checker.print_module_detail(args.module)
    else:
        checker.print_console_report()
    
    # 
    if checker.results["completeness_percentage"] < 70:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

