#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module_doc_gen.py - 模块实例文档生成工具

功能：
1. 读取doc/orchestration/registry.yaml
2. 生成doc/modules/MODULE_INSTANCES.md
3. 包含所有模块实例的索引和简介

用法：
    python scripts/module_doc_gen.py
    make module_doc_gen
"""

import os
import sys
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
REGISTRY_PATH = REPO_ROOT / "doc" / "orchestration" / "registry.yaml"
OUTPUT_PATH = REPO_ROOT / "doc" / "modules" / "MODULE_INSTANCES.md"

# 兼容Phase 3之前
ALT_REGISTRY_PATH = REPO_ROOT / "docs" / "orchestration" / "registry.yaml"
ALT_OUTPUT_PATH = REPO_ROOT / "docs" / "modules" / "MODULE_INSTANCES.md"


def load_registry():
    """加载registry.yaml"""
    # 尝试新路径
    if REGISTRY_PATH.exists():
        registry_path = REGISTRY_PATH
    elif ALT_REGISTRY_PATH.exists():
        registry_path = ALT_REGISTRY_PATH
    else:
        print(f"[error] registry.yaml未找到", file=sys.stderr)
        print(f"  期望位置: {REGISTRY_PATH.relative_to(REPO_ROOT)}", file=sys.stderr)
        return None
    
    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        print(f"✓ Registry已加载: {registry_path.relative_to(REPO_ROOT)}")
        return data
    except Exception as e:
        print(f"[error] 加载registry.yaml失败: {e}", file=sys.stderr)
        return None


def generate_type_section(module_types):
    """生成模块类型章节"""
    if not module_types:
        return "（暂无模块类型定义）\n"
    
    # 按level分组
    types_by_level = {}
    for t in module_types:
        level = t.get("level", 1)
        if level not in types_by_level:
            types_by_level[level] = []
        types_by_level[level].append(t)
    
    lines = []
    for level in sorted(types_by_level.keys()):
        lines.append(f"### {level}级模块类型\n")
        for t in types_by_level[level]:
            type_id = t.get("id", "unknown")
            name = t.get("name", "未命名")
            desc = t.get("description", "无描述")
            parent = t.get("parent", "")
            
            lines.append(f"#### {type_id} - {name}\n")
            lines.append(f"- **描述**: {desc}\n")
            if parent:
                lines.append(f"- **父类型**: {parent}\n")
            lines.append(f"- **I/O契约**: {t.get('io_contract', '未定义')}\n")
            lines.append("\n")
    
    return "".join(lines)


def generate_instance_section(module_instances):
    """生成模块实例章节"""
    if not module_instances:
        return "（暂无模块实例）\n"
    
    # 按level分组
    instances_by_level = {}
    for inst in module_instances:
        level = inst.get("level", 1)
        if level not in instances_by_level:
            instances_by_level[level] = []
        instances_by_level[level].append(inst)
    
    lines = []
    for level in sorted(instances_by_level.keys()):
        lines.append(f"### {level}级模块实例\n")
        for inst in instances_by_level[level]:
            inst_id = inst.get("id", "unknown")
            inst_type = inst.get("type", "unknown")
            path = inst.get("path", "")
            status = inst.get("status", "unknown")
            version = inst.get("version", "0.0.0")
            desc = inst.get("description", inst.get("role", "无描述"))
            
            # 状态emoji
            status_emoji = {
                "active": "🟢",
                "deprecated": "🔴",
                "wip": "🟡",
                "archived": "⚫"
            }.get(status, "❓")
            
            lines.append(f"#### {inst_id} {status_emoji}\n")
            lines.append(f"- **类型**: {inst_type}\n")
            lines.append(f"- **路径**: `{path}`\n")
            lines.append(f"- **状态**: {status}\n")
            lines.append(f"- **版本**: {version}\n")
            lines.append(f"- **描述**: {desc}\n")
            
            # 责任人
            owners = inst.get("owners", [])
            if owners:
                lines.append(f"- **责任人**: {', '.join(owners)}\n")
            
            # 依赖关系
            upstream = inst.get("upstream", [])
            downstream = inst.get("downstream", [])
            if upstream:
                lines.append(f"- **上游依赖**: {', '.join(upstream)}\n")
            if downstream:
                lines.append(f"- **下游输出**: {', '.join(downstream)}\n")
            
            # 文档链接
            agent_md = inst.get("agent_md")
            readme = inst.get("readme")
            if agent_md:
                lines.append(f"- **Agent文档**: [{agent_md}]({agent_md})\n")
            if readme:
                lines.append(f"- **README**: [{readme}]({readme})\n")
            
            # 测试数据信息（Phase 6新增）
            # 检查是否有test_data配置（通过检查文件是否存在）
            module_path = REPO_ROOT / path
            test_data_md = module_path / "doc" / "TEST_DATA.md"
            fixtures_dir = module_path / "fixtures"
            
            if test_data_md.exists() or fixtures_dir.exists():
                test_data_info = []
                if test_data_md.exists():
                    test_data_info.append(f"[规格文档]({path}/doc/TEST_DATA.md)")
                if fixtures_dir.exists():
                    # 统计fixtures文件
                    fixtures_files = list(fixtures_dir.glob("*.sql"))
                    if fixtures_files:
                        fixtures_names = [f.stem for f in fixtures_files]
                        test_data_info.append(f"Fixtures({len(fixtures_files)}个: {', '.join(fixtures_names)})")
                
                if test_data_info:
                    lines.append(f"- **测试数据**: {' | '.join(test_data_info)}\n")
            
            lines.append("\n")
    
    return "".join(lines)


def generate_dependency_graph(module_instances):
    """生成依赖关系图（Mermaid）"""
    if not module_instances:
        return ""
    
    lines = [
        "```mermaid\n",
        "graph LR\n"
    ]
    
    # 生成节点和边
    for inst in module_instances:
        inst_id = inst.get("id", "unknown")
        inst_id_safe = inst_id.replace(".", "_").replace("-", "_")
        
        upstream = inst.get("upstream", [])
        for up in upstream:
            up_safe = up.replace(".", "_").replace("-", "_")
            lines.append(f"  {up_safe}[{up}] --> {inst_id_safe}[{inst_id}]\n")
    
    lines.append("```\n")
    
    return "".join(lines)


def generate_markdown(registry):
    """生成Markdown文档"""
    module_types = registry.get("module_types", [])
    module_instances = registry.get("module_instances", [])
    
    lines = [
        "# 模块实例目录\n\n",
        f"> 自动生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"> 来源: doc/orchestration/registry.yaml\n",
        f"> 生成命令: `make module_doc_gen`\n\n",
        "---\n\n",
        "## 目标\n\n",
        "本文档提供所有模块实例的索引和简介，包括：\n",
        "- 模块类型定义\n",
        "- 模块实例列表（按层级分组）\n",
        "- 实例状态、版本、责任人\n",
        "- 依赖关系图\n\n",
        "---\n\n",
        "## 模块类型\n\n",
        generate_type_section(module_types),
        "---\n\n",
        "## 模块实例\n\n",
        generate_instance_section(module_instances),
        "---\n\n",
        "## 依赖关系图\n\n",
        generate_dependency_graph(module_instances),
        "---\n\n",
        "## 说明\n\n",
        "### 状态标记\n",
        "- 🟢 active: 活跃开发中\n",
        "- 🟡 wip: 工作进行中（未完成）\n",
        "- 🔴 deprecated: 已弃用\n",
        "- ⚫ archived: 已归档\n\n",
        "### 更新方式\n",
        "1. 修改`doc/orchestration/registry.yaml`\n",
        "2. 运行`make module_doc_gen`重新生成本文档\n\n",
        "### 相关文档\n",
        "- 模块类型详细说明: [MODULE_TYPES.md](MODULE_TYPES.md)\n",
        "- 模块初始化规范: [MODULE_INIT_GUIDE.md](MODULE_INIT_GUIDE.md)\n",
        "- 编排注册表: [../orchestration/registry.yaml](../orchestration/registry.yaml)\n"
    ]
    
    return "".join(lines)


def main():
    """主函数"""
    print("=" * 60)
    print("模块实例文档生成工具")
    print("=" * 60)
    
    # 加载registry
    print("\n加载registry.yaml...")
    registry = load_registry()
    if not registry:
        return 1
    
    module_types = registry.get("module_types", [])
    module_instances = registry.get("module_instances", [])
    print(f"✓ 模块类型: {len(module_types)}个")
    print(f"✓ 模块实例: {len(module_instances)}个")
    
    # 生成Markdown
    print("\n生成MODULE_INSTANCES.md...")
    markdown = generate_markdown(registry)
    
    # 确定输出路径
    if OUTPUT_PATH.parent.exists():
        output = OUTPUT_PATH
    elif ALT_OUTPUT_PATH.parent.exists():
        output = ALT_OUTPUT_PATH
    else:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        output = OUTPUT_PATH
    
    # 保存
    with open(output, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    rel_output = output.relative_to(REPO_ROOT)
    
    print()
    print("=" * 60)
    print(f"✅ 文档已生成: {rel_output}")
    print()
    print("内容包括:")
    print(f"  - {len(module_types)}个模块类型")
    print(f"  - {len(module_instances)}个模块实例")
    print(f"  - 依赖关系图")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

