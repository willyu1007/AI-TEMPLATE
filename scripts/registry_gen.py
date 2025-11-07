#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
registry_gen.py - 模块注册表生成工具

功能：
1. 扫描modules/目录下所有模块
2. 提取模块信息（从README.md和agent.md）
3. 生成registry.yaml草案
4. 输出到doc/orchestration/registry.yaml.draft

用法：
    python scripts/registry_gen.py
    make registry_gen
"""

import os
import sys
import re
import yaml
from pathlib import Path
from datetime import datetime

# 设置Windows控制台UTF-8输出
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
MODULES_DIR = REPO_ROOT / "modules"
OUTPUT_PATH = REPO_ROOT / "doc" / "orchestration" / "registry.yaml.draft"

# 兼容Phase 3之前
ALT_OUTPUT_PATH = REPO_ROOT / "docs" / "orchestration" / "registry.yaml.draft"

# YAML Front Matter正则
YAML_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL | re.MULTILINE)


def extract_yaml_front_matter(md_text):
    """提取YAML Front Matter"""
    match = YAML_FRONT_MATTER_RE.match(md_text)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def scan_modules():
    """扫描modules/目录"""
    if not MODULES_DIR.exists():
        print(f"[error] modules/目录不存在", file=sys.stderr)
        return []
    
    modules = []
    for module_dir in MODULES_DIR.iterdir():
        if not module_dir.is_dir():
            continue
        if module_dir.name.startswith(".") or module_dir.name == "__pycache__":
            continue
        
        module_info = extract_module_info(module_dir)
        if module_info:
            modules.append(module_info)
    
    return modules


def extract_module_info(module_dir):
    """提取单个模块的信息"""
    module_name = module_dir.name
    rel_path = module_dir.relative_to(REPO_ROOT)
    
    info = {
        "name": module_name,
        "path": str(rel_path),
        "agent_md": None,
        "readme": None,
        "meta": None
    }
    
    # 检查agent.md
    agent_md = module_dir / "agent.md"
    if agent_md.exists():
        info["agent_md"] = str(agent_md.relative_to(REPO_ROOT))
        # 尝试提取YAML Front Matter
        try:
            with open(agent_md, "r", encoding="utf-8") as f:
                content = f.read()
            meta = extract_yaml_front_matter(content)
            if meta:
                info["meta"] = meta
        except Exception as e:
            print(f"  [warn] 读取{agent_md.relative_to(REPO_ROOT)}失败: {e}", file=sys.stderr)
    
    # 检查README.md
    readme = module_dir / "README.md"
    if readme.exists():
        info["readme"] = str(readme.relative_to(REPO_ROOT))
    
    return info


def generate_registry_draft(modules):
    """生成registry.yaml草案"""
    registry = {
        "version": "1.0",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": "模块类型、实例、依赖关系注册表（草案，需人工审核）",
        "module_types": [],
        "module_instances": []
    }
    
    # 生成module_types（需人工补充）
    seen_types = set()
    for module in modules:
        meta = module.get("meta")
        if meta and "module_type" in meta:
            module_type = meta["module_type"]
            if module_type not in seen_types:
                seen_types.add(module_type)
                
                level = meta.get("level", 1)
                
                type_entry = {
                    "id": module_type,
                    "name": f"TODO: 填写{module_type}的名称",
                    "level": level,
                    "description": f"TODO: 填写{module_type}的描述",
                    "io_contract": "TODO: 填写I/O契约说明"
                }
                
                registry["module_types"].append(type_entry)
    
    # 如果没有找到任何类型，添加示例
    if not registry["module_types"]:
        registry["module_types"].append({
            "id": "1_example",
            "name": "示例模块类型",
            "level": 1,
            "description": "一级模块示例类型",
            "io_contract": "标准HTTP请求/响应"
        })
    
    # 生成module_instances
    for module in modules:
        name = module["name"]
        path = module["path"]
        meta = module.get("meta")
        
        # 从meta中提取信息
        if meta:
            instance_id = meta.get("agent_id", f"{name}.v1")
            if instance_id.startswith("modules."):
                # 去掉modules.前缀
                instance_id = instance_id.replace("modules.", "", 1)
            
            module_type = meta.get("module_type", "1_example")
            level = meta.get("level", 1)
            role = meta.get("role", "TODO: 填写角色描述")
            
            upstream = []
            downstream = []
            if "dependencies" in meta:
                upstream = meta["dependencies"].get("upstream", [])
                downstream = meta["dependencies"].get("downstream", [])
            
        else:
            # 没有agent.md，使用默认值
            instance_id = f"{name}.v1"
            module_type = "1_example"
            level = 1
            role = "TODO: 填写角色描述"
            upstream = []
            downstream = []
        
        instance_entry = {
            "id": instance_id,
            "type": module_type,
            "path": path,
            "level": level,
            "status": "active",
            "version": "1.0.0",
            "owners": ["TODO: 填写责任人"],
            "agent_md": module["agent_md"] if module["agent_md"] else f"{path}/agent.md (待创建)",
            "readme": module["readme"] if module["readme"] else f"{path}/README.md",
            "contracts": [f"{path}/doc/CONTRACT.md"] if Path(REPO_ROOT / path / "doc" / "CONTRACT.md").exists() else [f"{path}/CONTRACT.md"],
            "upstream": upstream,
            "downstream": downstream,
            "tags": [name, f"level:{level}"],
            "description": role
        }
        
        registry["module_instances"].append(instance_entry)
    
    return registry


def save_draft(registry):
    """保存草案"""
    # 确定输出路径
    if OUTPUT_PATH.parent.exists():
        output = OUTPUT_PATH
    elif ALT_OUTPUT_PATH.parent.exists():
        output = ALT_OUTPUT_PATH
    else:
        # 创建doc/orchestration/目录
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        output = OUTPUT_PATH
    
    # 保存
    with open(output, "w", encoding="utf-8") as f:
        f.write("# 模块注册表（草案）\n")
        f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# ⚠️ 此文件为草案，请人工审核并补充TODO标记的内容\n")
        f.write("# 审核完成后，删除.draft后缀，重命名为registry.yaml\n\n")
        yaml.dump(registry, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    return output


def main():
    """主函数"""
    print("=" * 60)
    print("模块注册表生成工具")
    print("=" * 60)
    
    # 扫描modules/
    print(f"\n扫描modules/目录...")
    modules = scan_modules()
    print(f"✓ 找到{len(modules)}个模块")
    
    if not modules:
        print("[error] 未找到任何模块", file=sys.stderr)
        return 1
    
    # 显示找到的模块
    print("\n找到的模块:")
    for module in modules:
        has_agent = "✓" if module["agent_md"] else "✗"
        print(f"  {has_agent} {module['name']} ({module['path']})")
    
    # 生成草案
    print("\n生成registry.yaml草案...")
    registry = generate_registry_draft(modules)
    
    # 保存
    output_file = save_draft(registry)
    rel_output = output_file.relative_to(REPO_ROOT)
    
    print()
    print("=" * 60)
    print(f"✅ 草案已生成: {rel_output}")
    print()
    print("下一步:")
    print(f"  1. 审核文件: {rel_output}")
    print(f"  2. 补充TODO标记的内容（类型描述、责任人等）")
    print(f"  3. 删除.draft后缀，重命名为registry.yaml")
    print(f"  4. 运行: make registry_check")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

