#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_route_check.py - 


1. agent.md
2. context_routes
3. 
4. 


    python scripts/doc_route_check.py
    make doc_route_check
"""

import os
import sys
import re
import yaml
from pathlib import Path

# WindowsUTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent

# YAML Front Matter
YAML_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL | re.MULTILINE)


def extract_yaml_front_matter(md_text):
    """MarkdownYAML Front Matter"""
    match = YAML_FRONT_MATTER_RE.match(md_text)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def find_agent_md_files():
    """agent.md"""
    agent_files = []
    
    # agent.md
    root_agent = REPO_ROOT / "agent.md"
    if root_agent.exists():
        agent_files.append(root_agent)
    
    # modules/agent.md
    modules_dir = REPO_ROOT / "modules"
    if modules_dir.exists():
        for agent_path in modules_dir.rglob("agent.md"):
            agent_files.append(agent_path)
    
    # temp
    agent_files = [f for f in agent_files if "temp" not in str(f)]
    
    return agent_files


def extract_routes_from_context_routes(context_routes, agent_file_path):
    """context_routes"""
    routes = []
    
    if not context_routes:
        return routes
    
    # always_read
    if "always_read" in context_routes:
        for path in context_routes["always_read"]:
            routes.append(("always_read", path, agent_file_path))
    
    # on_demand
    if "on_demand" in context_routes:
        for item in context_routes["on_demand"]:
            topic = item.get("topic", "unknown")
            if "paths" in item:
                for path in item["paths"]:
                    routes.append(("on_demand", path, agent_file_path, topic))
    
    # by_scope
    if "by_scope" in context_routes:
        for item in context_routes["by_scope"]:
            scope = item.get("scope", "unknown")
            if "read" in item:
                for path in item["read"]:
                    routes.append(("by_scope", path, agent_file_path, scope))
    
    return routes


def resolve_path(path, agent_file_path):
    """"""
    # ./
    if path.startswith("./"):
        base_dir = agent_file_path.parent
        resolved = (base_dir / path).resolve()
        return resolved
    
    # /
    return REPO_ROOT / path.lstrip("/")


def check_path_exists(route_info):
    """"""
    route_type = route_info[0]
    path = route_info[1]
    agent_file = route_info[2]
    
    # 
    full_path = resolve_path(path, agent_file)
    
    # 
    if full_path.exists():
        return True, None
    
    # 
    rel_agent = agent_file.relative_to(REPO_ROOT)
    
    if route_type == "always_read":
        error = f"always_read: {path}"
    elif route_type == "on_demand":
        topic = route_info[3] if len(route_info) > 3 else "unknown"
        error = f"on_demand: {path} (topic: {topic})"
    elif route_type == "by_scope":
        scope = route_info[3] if len(route_info) > 3 else "unknown"
        error = f"by_scope: {path} (scope: {scope})"
    else:
        error = f": {path}"
    
    return False, {"agent": str(rel_agent), "error": error, "path": path}


def check_wildcard_paths(routes):
    """modules/*/agent.md"""
    issues = []
    
    for route_info in routes:
        path = route_info[1]
        
        # 
        if "*" in path:
            agent_file = route_info[2]
            rel_agent = agent_file.relative_to(REPO_ROOT)
            
            # 
            pattern = path.lstrip("/")
            matches = list(REPO_ROOT.glob(pattern))
            
            if not matches:
                issues.append({
                    "agent": str(rel_agent),
                    "error": f": {path}",
                    "path": path
                })
    
    return issues


def main():
    """"""
    print("=" * 60)
    print("")
    print("=" * 60)
    
    # agent.md
    agent_files = find_agent_md_files()
    print(f"✓ {len(agent_files)}agent.md")
    
    if not agent_files:
        print("[warn] agent.md", file=sys.stderr)
        return 0
    
    # routes
    all_routes = []
    files_with_routes = 0
    files_without_meta = 0
    
    for agent_file in agent_files:
        rel_path = agent_file.relative_to(REPO_ROOT)
        
        try:
            with open(agent_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            meta = extract_yaml_front_matter(content)
            if not meta:
                files_without_meta += 1
                continue
            
            if "context_routes" not in meta:
                continue
            
            routes = extract_routes_from_context_routes(meta["context_routes"], agent_file)
            if routes:
                all_routes.extend(routes)
                files_with_routes += 1
        
        except Exception as e:
            print(f"[warn] {rel_path}: {e}", file=sys.stderr)
    
    print(f"✓ {files_with_routes}context_routes")
    if files_without_meta > 0:
        print(f"  [info] {files_without_meta}YAML Front MatterPhase")
    
    print(f"✓ {len(all_routes)}")
    print()
    
    if not all_routes:
        print("[info] ")
        return 0
    
    # 
    print("...")
    missing_paths = []
    checked = 0
    
    for route_info in all_routes:
        exists, error_info = check_path_exists(route_info)
        checked += 1
        if not exists and error_info:
            missing_paths.append(error_info)
    
    # 
    wildcard_issues = check_wildcard_paths(all_routes)
    
    # 
    print()
    print("=" * 60)
    
    total_issues = len(missing_paths) + len(wildcard_issues)
    
    if total_issues == 0:
        print(f"✅ : {checked}")
    else:
        print(f": {checked - total_issues}, {total_issues}")
        print()
        
        if missing_paths:
            print(":")
            for item in missing_paths:
                print(f"  : {item['agent']}")
                print(f"  : {item['error']}")
                print()
        
        if wildcard_issues:
            print(":")
            for item in wildcard_issues:
                print(f"  : {item['agent']}")
                print(f"  : {item['error']}")
                print()
    
    print("=" * 60)
    
    # 
    return 1 if total_issues > 0 else 0


if __name__ == "__main__":
    sys.exit(main())

