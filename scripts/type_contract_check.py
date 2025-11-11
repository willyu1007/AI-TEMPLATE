#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
type_contract_check.py - 


1. MODULE_TYPE_CONTRACTS.yaml
2. modules/
3. IO
4. /


    python scripts/type_contract_check.py
    make type_contract_check
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# WindowsUTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
MODULES_DIR = REPO_ROOT / "modules"
CONTRACTS_FILE = REPO_ROOT / "doc" / "modules" / "MODULE_TYPE_CONTRACTS.yaml"
REGISTRY_FILE = REPO_ROOT / "doc" / "orchestration" / "registry.yaml"

# YAML Front Matter
YAML_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL | re.MULTILINE)


def print_header(title):
    """"""
    print("=" * 60)
    print(title)
    print("=" * 60)


def extract_yaml_front_matter(md_text):
    """YAML Front Matter"""
    match = YAML_FRONT_MATTER_RE.match(md_text)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return None


def load_type_contracts():
    """"""
    if not CONTRACTS_FILE.exists():
        print(f"❌ : : {CONTRACTS_FILE}")
        return None
    
    try:
        with open(CONTRACTS_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ : : {e}")
        return None


def load_registry():
    """"""
    if not REGISTRY_FILE.exists():
        return None
    
    try:
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        return None


def find_all_agent_md():
    """modules/AGENTS.md"""
    agent_files = []
    
    if not MODULES_DIR.exists():
        return agent_files
    
    for module_dir in MODULES_DIR.iterdir():
        if not module_dir.is_dir():
            continue
        
        agent_file = module_dir / "AGENTS.md"
        if agent_file.exists():
            agent_files.append(agent_file)
    
    return agent_files


def get_module_type_from_registry(module_path: str, registry: dict) -> Optional[str]:
    """registry.yaml"""
    if not registry or 'module_instances' not in registry:
        return None
    
    for instance in registry.get('module_instances', []):
        if instance.get('path') == module_path:
            return instance.get('type')
    
    return None


def get_type_contract(type_id: str, contracts: dict) -> Optional[dict]:
    """"""
    for contract in contracts.get('type_contracts', []):
        if contract.get('id') == type_id:
            return contract
    return None


def validate_io_fields(module_io: dict, contract_io: dict, io_type: str) -> Tuple[bool, List[str]]:
    """
    IO
    
    Args:
        module_io: IOAGENTS.md
        contract_io: IOCONTRACTS.yaml
        io_type: 'inputs'  'outputs'
    
    Returns:
        (, )
    """
    errors = []
    
    if not module_io or io_type not in module_io:
        errors.append(f"  ❌ {io_type}")
        return False, errors
    
    module_fields = module_io.get(io_type, [])
    contract_fields = contract_io.get(io_type, [])
    
    # 
    module_field_names = {f.get('name') for f in module_fields if isinstance(f, dict)}
    contract_required_fields = {
        f.get('name') for f in contract_fields 
        if isinstance(f, dict) and f.get('required', False)
    }
    
    # 
    missing_fields = contract_required_fields - module_field_names
    if missing_fields:
        errors.append(f"  ❌ {io_type}: {', '.join(missing_fields)}")
        return False, errors
    
    return True, []


def check_module_contract(agent_file: Path, contracts: dict, registry: dict) -> Tuple[bool, List[str]]:
    """
    
    
    Returns:
        (, /)
    """
    messages = []
    
    # AGENTS.md
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, [f"❌ : {e}"]
    
    # YAML
    yaml_data = extract_yaml_front_matter(content)
    if not yaml_data:
        return False, ["❌ YAML Front Matter"]
    
    # 
    module_type = yaml_data.get('module_type')
    if not module_type:
        return False, ["❌ AGENTS.mdmodule_type"]
    
    # 
    type_contract = get_type_contract(module_type, contracts)
    if not type_contract:
        return False, [f"❌ '{module_type}'"]
    
    # IO
    all_pass = True
    
    # io
    module_io = yaml_data.get('io', {})
    
    # inputs
    pass_inputs, input_errors = validate_io_fields(
        module_io, 
        type_contract.get('io_contract', {}), 
        'inputs'
    )
    if not pass_inputs:
        all_pass = False
        messages.extend(input_errors)
    
    # outputs
    pass_outputs, output_errors = validate_io_fields(
        module_io, 
        type_contract.get('io_contract', {}), 
        'outputs'
    )
    if not pass_outputs:
        all_pass = False
        messages.extend(output_errors)
    
    # level
    module_level = yaml_data.get('level')
    level_range = type_contract.get('level_range', [])
    if module_level and level_range:
        if module_level < level_range[0] or module_level > level_range[1]:
            all_pass = False
            messages.append(
                f"  ❌ Level {module_level}  {level_range}"
            )
    
    if all_pass:
        messages.append("  ✓ IO")
    
    return all_pass, messages


def main():
    """"""
    print_header("")
    
    # 1. 
    contracts = load_type_contracts()
    if not contracts:
        sys.exit(1)
    
    print(f"✓ : {CONTRACTS_FILE.relative_to(REPO_ROOT)}")
    type_count = len(contracts.get('type_contracts', []))
    print(f"✓ : {type_count}")
    
    # 2. 
    registry = load_registry()
    if registry:
        print(f"✓ ")
    
    # 3. 
    agent_files = find_all_agent_md()
    
    if not agent_files:
        print("\n⚠️  : modules/")
        print(": IO")
        print()
        print("=" * 60)
        print("✅ ")
        print("=" * 60)
        return
    
    print(f"✓ {len(agent_files)}")
    print()
    
    # 4. 
    print("...")
    print()
    
    results = []
    for agent_file in agent_files:
        module_name = agent_file.parent.name
        print(f"[] {module_name}")
        
        passed, messages = check_module_contract(agent_file, contracts, registry)
        results.append((module_name, passed))
        
        for msg in messages:
            print(msg)
        print()
    
    # 5. 
    print()
    print_header("")
    
    passed_count = sum(1 for _, p in results if p)
    failed_count = len(results) - passed_count
    
    print(f": {len(results)}")
    print(f": {passed_count}")
    print(f": {failed_count}")
    print()
    
    if failed_count > 0:
        print("❌ IO")
        print()
        print(":")
        print("1. MODULE_TYPE_CONTRACTS.yaml")
        print("2. AGENTS.mdio")
        print("3. ")
        print("4.  make agent_lint YAML")
        sys.exit(1)
    else:
        print("=" * 60)
        print("✅ IO")
        print("=" * 60)


if __name__ == "__main__":
    main()

