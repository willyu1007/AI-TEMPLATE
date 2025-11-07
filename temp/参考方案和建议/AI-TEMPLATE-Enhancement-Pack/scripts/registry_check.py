#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
registry_check.py
- 校验 doc/orchestration/registry.yaml
  1) 实例命名唯一
  2) DAG 无环
  3) upstream/downstream 引用的实例存在
"""
import os, sys, yaml, collections

HERE = os.path.abspath(os.path.dirname(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
REG_FP = os.path.join(REPO, "doc", "orchestration", "registry.yaml")

def load_registry():
    if not os.path.exists(REG_FP):
        print(f"[warn] registry not found: {REG_FP}")
        return {"modules": []}
    with open(REG_FP, "r", encoding="utf-8") as f:
        return yaml.safe_load(f.read())

def ensure_unique_instances(items):
    seen = set()
    for it in items:
        name = it.get("instance")
        if name in seen:
            raise AssertionError(f"duplicate instance: {name}")
        seen.add(name)

def ensure_refs_exist(items):
    instances = {it.get("instance") for it in items}
    for it in items:
        for dep in it.get("upstream", []) + it.get("downstream", []):
            if dep not in instances:
                raise AssertionError(f"{it.get('instance')}: reference not found -> {dep}")

def build_graph(items):
    graph = collections.defaultdict(list)
    for it in items:
        u = it.get("instance")
        for v in it.get("downstream", []):
            graph[u].append(v)
    return graph

def has_cycle(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {u: WHITE for u in graph}
    def dfs(u):
        color[u] = GRAY
        for v in graph.get(u, []):
            c = color.get(v, WHITE)
            if c == GRAY:
                return True
            if c == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False
    for u in list(graph.keys()):
        if color[u] == WHITE:
            if dfs(u):
                return True
    return False

def main():
    reg = load_registry()
    items = reg.get("modules", [])
    try:
        ensure_unique_instances(items)
        ensure_refs_exist(items)
        g = build_graph(items)
        if has_cycle(g):
            raise AssertionError("registry has cycle(s)")
        print("[ok] registry check passed")
        sys.exit(0)
    except AssertionError as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
