#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agent_lint.py
- 遍历仓库内所有 agent.md
- 提取 YAML Front Matter
- 进行最小必要校验 + （如存在）按 schemas/agent.schema.yaml 做 jsonschema 校验
"""
import os, sys, re, yaml, json

HERE = os.path.abspath(os.path.dirname(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
SCHEMA_FP = os.path.join(REPO, "schemas", "agent.schema.yaml")

YAML_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.S)

def load_schema():
    if not os.path.exists(SCHEMA_FP):
        return None
    with open(SCHEMA_FP, "r", encoding="utf-8") as f:
        return yaml.safe_load(f.read())

def extract_yaml_front_matter(md_text):
    m = YAML_RE.match(md_text)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except Exception as e:
        raise RuntimeError(f"YAML front matter parse error: {e}")

def iter_agent_files():
    for root, _, files in os.walk(REPO):
        for fn in files:
            if fn.lower() == "agent.md":
                yield os.path.join(root, fn)

def basic_check(meta, fp):
    required = ["spec_version", "agent_id", "role"]
    missing = [k for k in required if k not in meta]
    if missing:
        raise AssertionError(f"{fp}: missing required fields: {missing}")

def schema_check(meta, schema, fp):
    try:
        import jsonschema
    except Exception:
        print("[warn] jsonschema not installed; skip schema validation", file=sys.stderr)
        return
    try:
        jsonschema.validate(meta, schema)
    except Exception as e:
        raise AssertionError(f"{fp}: schema validation failed: {e}")

def main():
    schema = load_schema()
    failed = False
    for fp in iter_agent_files():
        with open(fp, "r", encoding="utf-8") as f:
            text = f.read()
        meta = extract_yaml_front_matter(text)
        if meta is None:
            print(f"[error] {fp}: missing YAML front matter", file=sys.stderr)
            failed = True
            continue
        try:
            basic_check(meta, fp)
            if schema:
                schema_check(meta, schema, fp)
            print(f"[ok] {fp}")
        except AssertionError as e:
            print(f"[error] {e}", file=sys.stderr)
            failed = True
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
