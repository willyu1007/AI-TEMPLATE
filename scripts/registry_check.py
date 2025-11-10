#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
registry_check.py - 


1. doc/orchestration/registry.yaml
2. ID
3. agent_md
4. DAG
5. module_type


    python scripts/registry_check.py
    make registry_check
"""

import os
import sys
import yaml
from pathlib import Path
from collections import defaultdict

# WindowsUTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
REGISTRY_PATH = REPO_ROOT / "doc" / "orchestration" / "registry.yaml"


def load_registry():
    """registry.yaml"""
    if not REGISTRY_PATH.exists():
        # docs/Phase 3
        alt_path = REPO_ROOT / "docs" / "orchestration" / "registry.yaml"
        if alt_path.exists():
            registry_path = alt_path
        else:
            print(f"[error] registry.yaml", file=sys.stderr)
            print(f"  : {REGISTRY_PATH.relative_to(REPO_ROOT)}", file=sys.stderr)
            return None
    else:
        registry_path = REGISTRY_PATH
    
    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        print(f"✓ Registry: {registry_path.relative_to(REPO_ROOT)}")
        return data
    except Exception as e:
        print(f"[error] registry.yaml: {e}", file=sys.stderr)
        return None


def check_module_types(registry):
    """"""
    if "module_types" not in registry:
        print("[warn] registry.yamlmodule_types", file=sys.stderr)
        return {}, []
    
    types = registry["module_types"]
    type_map = {}
    issues = []
    
    for t in types:
        if "id" not in t:
            issues.append("id")
            continue
        
        type_id = t["id"]
        
        # 
        if type_id in type_map:
            issues.append(f"ID: {type_id}")
        
        type_map[type_id] = t
        
        # 
        required = ["name", "level"]
        missing = [f for f in required if f not in t]
        if missing:
            issues.append(f"'{type_id}': {', '.join(missing)}")
        
        # level
        if "level" in t:
            level = t["level"]
            if not isinstance(level, int) or level < 1 or level > 4:
                issues.append(f"'{type_id}'level1-4: {level}")
    
    return type_map, issues


def check_module_instances(registry, type_map):
    """"""
    if "module_instances" not in registry:
        print("[warn] registry.yamlmodule_instances", file=sys.stderr)
        return {}, []
    
    instances = registry["module_instances"]
    instance_map = {}
    issues = []
    
    for inst in instances:
        if "id" not in inst:
            issues.append("id")
            continue
        
        inst_id = inst["id"]
        
        # 
        if inst_id in instance_map:
            issues.append(f"ID: {inst_id}")
        
        instance_map[inst_id] = inst
        
        # 
        required = ["type", "path", "level", "status"]
        missing = [f for f in required if f not in inst]
        if missing:
            issues.append(f"'{inst_id}': {', '.join(missing)}")
        
        # type
        if "type" in inst:
            inst_type = inst["type"]
            if type_map and inst_type not in type_map:
                issues.append(f"'{inst_id}''{inst_type}'")
        
        # agent_md
        if "agent_md" in inst and inst["agent_md"] is not None:
            agent_md_path = REPO_ROOT / inst["agent_md"]
            if not agent_md_path.exists():
                issues.append(f"'{inst_id}'agent_md: {inst['agent_md']}")
        
        # path
        if "path" in inst:
            path = REPO_ROOT / inst["path"]
            if not path.exists():
                issues.append(f"'{inst_id}'path: {inst['path']}")
        
        # status
        if "status" in inst:
            status = inst["status"]
            valid_status = ["active", "deprecated", "wip", "archived"]
            if status not in valid_status:
                issues.append(f"'{inst_id}'status: {status}: {', '.join(valid_status)}")
    
    return instance_map, issues


def check_dependencies_dag(instance_map):
    """DAG"""
    if not instance_map:
        return []
    
    issues = []
    
    # 
    graph = defaultdict(list)
    for inst_id, inst in instance_map.items():
        if "upstream" in inst and inst["upstream"]:
            for upstream_id in inst["upstream"]:
                # upstream_idinst_id inst_id -> upstream_id
                #  upstream_id -> inst_id
                # upstream
                if upstream_id not in instance_map:
                    issues.append(f"'{inst_id}'upstream'{upstream_id}'")
                else:
                    graph[upstream_id].append(inst_id)
    
    # DFS
    def has_cycle():
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {inst_id: WHITE for inst_id in instance_map}
        
        def dfs(node, path):
            if color[node] == GRAY:
                # 
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                return cycle
            if color[node] == BLACK:
                return None
            
            color[node] = GRAY
            path.append(node)
            
            for neighbor in graph.get(node, []):
                result = dfs(neighbor, path[:])
                if result:
                    return result
            
            color[node] = BLACK
            return None
        
        for node in instance_map:
            if color[node] == WHITE:
                result = dfs(node, [])
                if result:
                    return result
        return None
    
    cycle = has_cycle()
    if cycle:
        cycle_str = " → ".join(cycle)
        issues.append(f": {cycle_str}")
    
    return issues


def main():
    """"""
    print("=" * 60)
    print("")
    print("=" * 60)
    
    # registry
    registry = load_registry()
    if not registry:
        print("[error] registry.yaml", file=sys.stderr)
        return 1
    
    all_issues = []
    
    # 
    print("\n...")
    type_map, type_issues = check_module_types(registry)
    if type_issues:
        all_issues.extend(type_issues)
        for issue in type_issues:
            print(f"  [error] {issue}", file=sys.stderr)
    else:
        print(f"  ✓ {len(type_map)}")
    
    # 
    print("\n...")
    instance_map, inst_issues = check_module_instances(registry, type_map)
    if inst_issues:
        all_issues.extend(inst_issues)
        for issue in inst_issues:
            print(f"  [error] {issue}", file=sys.stderr)
    else:
        print(f"  ✓ {len(instance_map)}")
    
    # DAG
    print("\n...")
    dag_issues = check_dependencies_dag(instance_map)
    if dag_issues:
        all_issues.extend(dag_issues)
        for issue in dag_issues:
            print(f"  [error] {issue}", file=sys.stderr)
    else:
        print(f"  ✓ ")
    
    # 
    print()
    print("=" * 60)
    if all_issues:
        print(f": {len(all_issues)}")
        print("\n:")
        for i, issue in enumerate(all_issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("✅ ")
    print("=" * 60)
    
    return 1 if all_issues else 0


if __name__ == "__main__":
    sys.exit(main())

