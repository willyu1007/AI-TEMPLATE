#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module_doc_gen.py - 


1. doc/orchestration/registry.yaml
2. doc/modules/MODULE_INSTANCES.md
3. 


    python scripts/module_doc_gen.py
    make module_doc_gen
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime

# WindowsUTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
REGISTRY_PATH = REPO_ROOT / "doc" / "orchestration" / "registry.yaml"
OUTPUT_PATH = REPO_ROOT / "doc" / "modules" / "MODULE_INSTANCES.md"

# Phase 3
ALT_REGISTRY_PATH = REPO_ROOT / "docs" / "orchestration" / "registry.yaml"
ALT_OUTPUT_PATH = REPO_ROOT / "docs" / "modules" / "MODULE_INSTANCES.md"


def load_registry():
    """registry.yaml"""
    # 
    if REGISTRY_PATH.exists():
        registry_path = REGISTRY_PATH
    elif ALT_REGISTRY_PATH.exists():
        registry_path = ALT_REGISTRY_PATH
    else:
        print(f"[error] registry.yaml", file=sys.stderr)
        print(f"  : {REGISTRY_PATH.relative_to(REPO_ROOT)}", file=sys.stderr)
        return None
    
    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        print(f"✓ Registry: {registry_path.relative_to(REPO_ROOT)}")
        return data
    except Exception as e:
        print(f"[error] registry.yaml: {e}", file=sys.stderr)
        return None


def generate_type_section(module_types):
    """"""
    if not module_types:
        return "\n"
    
    # level
    types_by_level = {}
    for t in module_types:
        level = t.get("level", 1)
        if level not in types_by_level:
            types_by_level[level] = []
        types_by_level[level].append(t)
    
    lines = []
    for level in sorted(types_by_level.keys()):
        lines.append(f"### {level}\n")
        for t in types_by_level[level]:
            type_id = t.get("id", "unknown")
            name = t.get("name", "")
            desc = t.get("description", "")
            parent = t.get("parent", "")
            
            lines.append(f"#### {type_id} - {name}\n")
            lines.append(f"- ****: {desc}\n")
            if parent:
                lines.append(f"- ****: {parent}\n")
            lines.append(f"- **I/O**: {t.get('io_contract', '')}\n")
            lines.append("\n")
    
    return "".join(lines)


def generate_instance_section(module_instances):
    """"""
    if not module_instances:
        return "\n"
    
    # level
    instances_by_level = {}
    for inst in module_instances:
        level = inst.get("level", 1)
        if level not in instances_by_level:
            instances_by_level[level] = []
        instances_by_level[level].append(inst)
    
    lines = []
    for level in sorted(instances_by_level.keys()):
        lines.append(f"### {level}\n")
        for inst in instances_by_level[level]:
            inst_id = inst.get("id", "unknown")
            inst_type = inst.get("type", "unknown")
            path = inst.get("path", "")
            status = inst.get("status", "unknown")
            version = inst.get("version", "0.0.0")
            desc = inst.get("description", inst.get("role", ""))
            
            # emoji
            status_emoji = {
                "active": "🟢",
                "deprecated": "🔴",
                "wip": "🟡",
                "archived": "⚫"
            }.get(status, "❓")
            
            lines.append(f"#### {inst_id} {status_emoji}\n")
            lines.append(f"- ****: {inst_type}\n")
            lines.append(f"- ****: `{path}`\n")
            lines.append(f"- ****: {status}\n")
            lines.append(f"- ****: {version}\n")
            lines.append(f"- ****: {desc}\n")
            
            # 
            owners = inst.get("owners", [])
            if owners:
                lines.append(f"- ****: {', '.join(owners)}\n")
            
            # 
            upstream = inst.get("upstream", [])
            downstream = inst.get("downstream", [])
            if upstream:
                lines.append(f"- ****: {', '.join(upstream)}\n")
            if downstream:
                lines.append(f"- ****: {', '.join(downstream)}\n")
            
            # 
            agent_md = inst.get("agent_md")
            readme = inst.get("readme")
            if agent_md:
                lines.append(f"- **Agent**: [{agent_md}]({agent_md})\n")
            if readme:
                lines.append(f"- **README**: [{readme}]({readme})\n")
            
            # Phase 6
            # test_data
            module_path = REPO_ROOT / path
            test_data_md = module_path / "doc" / "TEST_DATA.md"
            fixtures_dir = module_path / "fixtures"
            
            if test_data_md.exists() or fixtures_dir.exists():
                test_data_info = []
                if test_data_md.exists():
                    test_data_info.append(f"[]({path}/doc/TEST_DATA.md)")
                if fixtures_dir.exists():
                    # fixtures
                    fixtures_files = list(fixtures_dir.glob("*.sql"))
                    if fixtures_files:
                        fixtures_names = [f.stem for f in fixtures_files]
                        test_data_info.append(f"Fixtures({len(fixtures_files)}: {', '.join(fixtures_names)})")
                
                if test_data_info:
                    lines.append(f"- ****: {' | '.join(test_data_info)}\n")
            
            lines.append("\n")
    
    return "".join(lines)


def generate_dependency_graph(module_instances):
    """Mermaid"""
    if not module_instances:
        return ""
    
    lines = [
        "```mermaid\n",
        "graph LR\n"
    ]
    
    # 
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
    """Markdown"""
    module_types = registry.get("module_types", [])
    module_instances = registry.get("module_instances", [])
    
    lines = [
        "# \n\n",
        f"> : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"> : doc/orchestration/registry.yaml\n",
        f"> : `make module_doc_gen`\n\n",
        "---\n\n",
        "## \n\n",
        "\n",
        "- \n",
        "- \n",
        "- \n",
        "- \n\n",
        "---\n\n",
        "## \n\n",
        generate_type_section(module_types),
        "---\n\n",
        "## \n\n",
        generate_instance_section(module_instances),
        "---\n\n",
        "## \n\n",
        generate_dependency_graph(module_instances),
        "---\n\n",
        "## \n\n",
        "### \n",
        "- 🟢 active: \n",
        "- 🟡 wip: \n",
        "- 🔴 deprecated: \n",
        "- ⚫ archived: \n\n",
        "### \n",
        "1. `doc/orchestration/registry.yaml`\n",
        "2. `make module_doc_gen`\n\n",
        "### \n",
        "- : [MODULE_TYPES.md](MODULE_TYPES.md)\n",
        "- : [MODULE_INIT_GUIDE.md](MODULE_INIT_GUIDE.md)\n",
        "- : [../orchestration/registry.yaml](../orchestration/registry.yaml)\n"
    ]
    
    return "".join(lines)


def main():
    """"""
    print("=" * 60)
    print("")
    print("=" * 60)
    
    # registry
    print("\nregistry.yaml...")
    registry = load_registry()
    if not registry:
        return 1
    
    module_types = registry.get("module_types", [])
    module_instances = registry.get("module_instances", [])
    print(f"✓ : {len(module_types)}")
    print(f"✓ : {len(module_instances)}")
    
    # Markdown
    print("\nMODULE_INSTANCES.md...")
    markdown = generate_markdown(registry)
    
    # 
    if OUTPUT_PATH.parent.exists():
        output = OUTPUT_PATH
    elif ALT_OUTPUT_PATH.parent.exists():
        output = ALT_OUTPUT_PATH
    else:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        output = OUTPUT_PATH
    
    # 
    with open(output, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    rel_output = output.relative_to(REPO_ROOT)
    
    print()
    print("=" * 60)
    print(f"✅ : {rel_output}")
    print()
    print(":")
    print(f"  - {len(module_types)}")
    print(f"  - {len(module_instances)}")
    print(f"  - ")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

