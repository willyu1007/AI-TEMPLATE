#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
registry_gen.py - 


1. modules/
2. README.mdAGENTS.md
3. registry.yaml
4. doc/orchestration/registry.yaml.draft


    python scripts/registry_gen.py
    make registry_gen
"""

import os
import sys
import re
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
MODULES_DIR = REPO_ROOT / "modules"
OUTPUT_PATH = REPO_ROOT / "doc" / "orchestration" / "registry.yaml.draft"

# Phase 3
ALT_OUTPUT_PATH = REPO_ROOT / "docs" / "orchestration" / "registry.yaml.draft"

# YAML Front Matter
YAML_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL | re.MULTILINE)


def extract_yaml_front_matter(md_text):
    """YAML Front Matter"""
    match = YAML_FRONT_MATTER_RE.match(md_text)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def scan_modules():
    """modules/"""
    if not MODULES_DIR.exists():
        print(f"[error] modules/", file=sys.stderr)
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
    """"""
    module_name = module_dir.name
    rel_path = module_dir.relative_to(REPO_ROOT)
    
    info = {
        "name": module_name,
        "path": str(rel_path),
        "agent_md": None,
        "readme": None,
        "meta": None
    }
    
    # AGENTS.md
    agent_md = module_dir / "AGENTS.md"
    if agent_md.exists():
        info["agent_md"] = str(agent_md.relative_to(REPO_ROOT))
        # YAML Front Matter
        try:
            with open(agent_md, "r", encoding="utf-8") as f:
                content = f.read()
            meta = extract_yaml_front_matter(content)
            if meta:
                info["meta"] = meta
        except Exception as e:
            print(f"  [warn] {agent_md.relative_to(REPO_ROOT)}: {e}", file=sys.stderr)
    
    # README.md
    readme = module_dir / "README.md"
    if readme.exists():
        info["readme"] = str(readme.relative_to(REPO_ROOT))
    
    return info


def generate_registry_draft(modules):
    """registry.yaml"""
    registry = {
        "version": "1.0",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": "",
        "module_types": [],
        "module_instances": []
    }
    
    # module_types
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
                    "name": f"TODO: {module_type}",
                    "level": level,
                    "description": f"TODO: {module_type}",
                    "io_contract": "TODO: I/O"
                }
                
                registry["module_types"].append(type_entry)
    
    # 
    if not registry["module_types"]:
        registry["module_types"].append({
            "id": "1_example",
            "name": "",
            "level": 1,
            "description": "",
            "io_contract": "HTTP/"
        })
    
    # module_instances
    for module in modules:
        name = module["name"]
        path = module["path"]
        meta = module.get("meta")
        
        # meta
        if meta:
            instance_id = meta.get("agent_id", f"{name}.v1")
            if instance_id.startswith("modules."):
                # modules.
                instance_id = instance_id.replace("modules.", "", 1)
            
            module_type = meta.get("module_type", "1_example")
            level = meta.get("level", 1)
            role = meta.get("role", "TODO: ")
            
            upstream = []
            downstream = []
            if "dependencies" in meta:
                upstream = meta["dependencies"].get("upstream", [])
                downstream = meta["dependencies"].get("downstream", [])
            
        else:
            # AGENTS.md
            instance_id = f"{name}.v1"
            module_type = "1_example"
            level = 1
            role = "TODO: "
            upstream = []
            downstream = []
        
        instance_entry = {
            "id": instance_id,
            "type": module_type,
            "path": path,
            "level": level,
            "status": "active",
            "version": "1.0.0",
            "owners": ["TODO: "],
            "agent_md": module["agent_md"] if module["agent_md"] else f"{path}/AGENTS.md ()",
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
    """"""
    # 
    if OUTPUT_PATH.parent.exists():
        output = OUTPUT_PATH
    elif ALT_OUTPUT_PATH.parent.exists():
        output = ALT_OUTPUT_PATH
    else:
        # doc/orchestration/
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        output = OUTPUT_PATH
    
    # 
    with open(output, "w", encoding="utf-8") as f:
        f.write("# \n")
        f.write(f"# : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# ⚠️ TODO\n")
        f.write("# .draftregistry.yaml\n\n")
        yaml.dump(registry, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    return output


def main():
    """"""
    print("=" * 60)
    print("")
    print("=" * 60)
    
    # modules/
    print(f"\nmodules/...")
    modules = scan_modules()
    print(f"✓ {len(modules)}")
    
    if not modules:
        print("[error] ", file=sys.stderr)
        return 1
    
    # 
    print("\n:")
    for module in modules:
        has_agent = "✓" if module["agent_md"] else "✗"
        print(f"  {has_agent} {module['name']} ({module['path']})")
    
    # 
    print("\nregistry.yaml...")
    registry = generate_registry_draft(modules)
    
    # 
    output_file = save_draft(registry)
    rel_output = output_file.relative_to(REPO_ROOT)
    
    print()
    print("=" * 60)
    print(f"✅ : {rel_output}")
    print()
    print(":")
    print(f"  1. : {rel_output}")
    print(f"  2. TODO")
    print(f"  3. .draftregistry.yaml")
    print(f"  4. : make registry_check")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

