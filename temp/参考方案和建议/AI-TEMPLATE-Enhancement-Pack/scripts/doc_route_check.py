#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_route_check.py
- 校验每个 agent.md YAML 中 context_routes 所指路径是否存在
"""
import os, sys, re, yaml, glob

HERE = os.path.abspath(os.path.dirname(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
YAML_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.S)

def extract_yaml(fp):
    with open(fp, "r", encoding="utf-8") as f:
        text = f.read()
    m = YAML_RE.match(text)
    if not m:
        return None
    return yaml.safe_load(m.group(1))

def iter_agent_files():
    for root, _, files in os.walk(REPO):
        for fn in files:
            if fn.lower() == "agent.md":
                yield os.path.join(root, fn)

def paths_from_routes(routes):
    results = []
    if not routes:
        return results
    for p in routes.get("always_read", []):
        results.append(p)
    for item in routes.get("on_demand", []):
        for p in item.get("paths", []):
            results.append(p)
    for item in routes.get("by_scope", []):
        for p in item.get("read", []):
            results.append(p)
    return results

def check_paths(paths, base_dir):
    ok = True
    for p in paths:
        expanded = glob.glob(os.path.join(base_dir, p.lstrip("/")))
        if not expanded:
            print(f"[error] missing path: {p}", file=sys.stderr)
            ok = False
    return ok

def main():
    ok_all = True
    for fp in iter_agent_files():
        meta = extract_yaml(fp)
        if not meta:
            print(f"[warn] {fp}: no YAML front matter; skip")
            continue
        routes = meta.get("context_routes")
        if not routes:
            print(f"[warn] {fp}: no context_routes")
            continue
        ok = check_paths(paths_from_routes(routes), os.path.dirname(REPO))
        if ok:
            print(f"[ok] {fp}: routes valid")
        else:
            ok_all = False
    sys.exit(0 if ok_all else 1)

if __name__ == "__main__":
    main()
