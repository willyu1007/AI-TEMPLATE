#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agent_lint.py - agent.md YAML前言校验工具

功能：
1. 遍历仓库内所有agent.md文件
2. 提取YAML Front Matter
3. 进行基础必填字段校验
4. 使用schemas/agent.schema.yaml进行Schema校验（如jsonschema已安装）

用法：
    python scripts/agent_lint.py
    make agent_lint
"""

import os
import sys
import re
import yaml
from pathlib import Path

# 设置Windows控制台UTF-8输出
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "agent.schema.yaml"

# YAML Front Matter正则
YAML_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL | re.MULTILINE)


def load_schema():
    """加载agent.schema.yaml"""
    if not SCHEMA_PATH.exists():
        return None
    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[warn] 无法加载Schema: {e}", file=sys.stderr)
        return None


def extract_yaml_front_matter(md_text):
    """从Markdown文件中提取YAML Front Matter"""
    match = YAML_FRONT_MATTER_RE.match(md_text)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        raise ValueError(f"YAML解析错误: {e}")


def find_agent_md_files():
    """查找所有agent.md文件"""
    agent_files = []
    
    # 查找根目录agent.md
    root_agent = REPO_ROOT / "agent.md"
    if root_agent.exists():
        agent_files.append(root_agent)
    
    # 查找modules/下的agent.md
    modules_dir = REPO_ROOT / "modules"
    if modules_dir.exists():
        for agent_path in modules_dir.rglob("agent.md"):
            agent_files.append(agent_path)
    
    # 排除temp目录
    agent_files = [f for f in agent_files if "temp" not in str(f)]
    
    return agent_files


def basic_validation(meta, file_path):
    """基础必填字段校验"""
    required_fields = ["spec_version", "agent_id", "role"]
    missing = [field for field in required_fields if field not in meta]
    
    if missing:
        raise AssertionError(f"缺少必填字段: {', '.join(missing)}")
    
    # spec_version格式检查
    if not re.match(r"^\d+\.\d+$", meta["spec_version"]):
        raise AssertionError(f"spec_version格式错误，应为'X.Y'格式: {meta['spec_version']}")
    
    # agent_id格式检查
    agent_id = meta["agent_id"]
    if agent_id != "repo" and not agent_id.startswith("modules."):
        print(f"  [warn] agent_id建议格式: 'repo'或'modules.<entity>.<instance>'", file=sys.stderr)


def schema_validation(meta, schema, file_path):
    """使用jsonschema进行Schema校验"""
    try:
        import jsonschema
    except ImportError:
        print("  [info] jsonschema未安装，跳过Schema校验（可选）", file=sys.stderr)
        print("        安装方法: pip install jsonschema", file=sys.stderr)
        return
    
    try:
        jsonschema.validate(meta, schema)
    except jsonschema.ValidationError as e:
        raise AssertionError(f"Schema校验失败: {e.message}\n  路径: {'.'.join(str(p) for p in e.path)}")


def validate_context_routes(meta, file_path):
    """校验context_routes中引用的路径"""
    if "context_routes" not in meta:
        return
    
    routes = meta["context_routes"]
    issues = []
    
    # 检查always_read
    if "always_read" in routes:
        for path in routes["always_read"]:
            full_path = REPO_ROOT / path.lstrip("/")
            if not full_path.exists():
                issues.append(f"always_read路径不存在: {path}")
    
    # 检查on_demand
    if "on_demand" in routes:
        for item in routes["on_demand"]:
            if "paths" in item:
                for path in item["paths"]:
                    # 相对路径（./开头）需要基于agent.md所在目录
                    if path.startswith("./"):
                        base_dir = file_path.parent
                        full_path = (base_dir / path).resolve()
                    else:
                        full_path = REPO_ROOT / path.lstrip("/")
                    
                    if not full_path.exists():
                        issues.append(f"on_demand路径不存在: {path} (topic: {item.get('topic', 'unknown')})")
    
    # 检查by_scope
    if "by_scope" in routes:
        for item in routes["by_scope"]:
            if "read" in item:
                for path in item["read"]:
                    full_path = REPO_ROOT / path.lstrip("/")
                    if not full_path.exists():
                        issues.append(f"by_scope路径不存在: {path} (scope: {item.get('scope', 'unknown')})")
    
    if issues:
        print(f"  [warn] context_routes路径检查:", file=sys.stderr)
        for issue in issues:
            print(f"    - {issue}", file=sys.stderr)


def check_agent_file(file_path, schema):
    """检查单个agent.md文件"""
    rel_path = file_path.relative_to(REPO_ROOT)
    
    try:
        # 读取文件
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取YAML Front Matter
        meta = extract_yaml_front_matter(content)
        if meta is None:
            print(f"[error] {rel_path}: 缺少YAML Front Matter", file=sys.stderr)
            print(f"        agent.md文件应以 --- 开头并包含YAML前言", file=sys.stderr)
            return False
        
        # 基础校验
        basic_validation(meta, file_path)
        
        # Schema校验
        if schema:
            schema_validation(meta, schema, file_path)
        
        # context_routes路径校验
        validate_context_routes(meta, file_path)
        
        print(f"[ok] {rel_path}")
        return True
        
    except AssertionError as e:
        print(f"[error] {rel_path}: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[error] {rel_path}: 未预期的错误: {e}", file=sys.stderr)
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("Agent.md YAML前言校验")
    print("=" * 60)
    
    # 加载Schema
    schema = load_schema()
    if schema:
        print(f"✓ Schema已加载: {SCHEMA_PATH.relative_to(REPO_ROOT)}")
    else:
        print(f"⚠ Schema未找到，将仅进行基础校验", file=sys.stderr)
    
    # 查找所有agent.md
    agent_files = find_agent_md_files()
    print(f"✓ 找到{len(agent_files)}个agent.md文件")
    print()
    
    if not agent_files:
        print("[warn] 未找到任何agent.md文件", file=sys.stderr)
        return 0
    
    # 逐个检查
    results = []
    for file_path in agent_files:
        success = check_agent_file(file_path, schema)
        results.append((file_path, success))
    
    # 汇总结果
    print()
    print("=" * 60)
    passed = sum(1 for _, success in results if success)
    failed = len(results) - passed
    
    print(f"检查完成: {passed}个通过, {failed}个失败")
    
    if failed > 0:
        print()
        print("失败的文件:")
        for file_path, success in results:
            if not success:
                print(f"  - {file_path.relative_to(REPO_ROOT)}")
    
    print("=" * 60)
    
    # 返回状态码
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())

