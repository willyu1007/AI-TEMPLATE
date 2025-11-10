#!/usr/bin/env python3
"""

"""
import sys
import json
import pathlib
from typing import Dict, List, Tuple

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def load_contract(path):
    """"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️   {path}: {e}")
        return None

def find_contract_files():
    """"""
    root = pathlib.Path('.')
    contracts = []
    
    #  tools/ 
    for p in root.glob('tools/**/contract.json'):
        contracts.append(p)
    
    return contracts

def check_breaking_changes(baseline: Dict, current: Dict, path: str) -> Tuple[bool, List[str]]:
    """"""
    errors = []
    
    # 
    baseline_type = baseline.get('type')
    current_type = current.get('type')
    if baseline_type and current_type and baseline_type != current_type:
        errors.append(f": {baseline_type} -> {current_type}")
    
    # 
    baseline_required = set(baseline.get('required', []))
    current_required = set(current.get('required', []))
    
    # 
    new_required = current_required - baseline_required
    if new_required:
        errors.append(f": {new_required}")
    
    # 
    baseline_props = set(baseline.get('properties', {}).keys())
    current_props = set(current.get('properties', {}).keys())
    
    deleted_fields = baseline_props - current_props
    if deleted_fields:
        errors.append(f": {deleted_fields}")
    
    # 
    for field in baseline_props & current_props:
        baseline_field_type = baseline['properties'][field].get('type')
        current_field_type = current['properties'][field].get('type')
        
        if baseline_field_type and current_field_type and baseline_field_type != current_field_type:
            errors.append(f" '{field}' : {baseline_field_type} -> {current_field_type}")
    
    return len(errors) == 0, errors

def main():
    print("🔍 ...\n")
    
    baseline_dir = pathlib.Path('.contracts_baseline')
    
    if not baseline_dir.exists():
        print("⚠️  ...")
        baseline_dir.mkdir(exist_ok=True)
        print("💡  'make update_baselines' ")
        sys.exit(0)
    
    # 
    current_contracts = find_contract_files()
    
    if not current_contracts:
        print("⚠️  ")
        sys.exit(0)
    
    print(f"📄  {len(current_contracts)} \n")
    
    all_passed = True
    
    for contract_path in current_contracts:
        relative_path = contract_path.relative_to('.')
        baseline_path = baseline_dir / relative_path
        
        print(f": {relative_path}")
        
        # 
        current = load_contract(contract_path)
        if not current:
            continue
        
        # 
        if not baseline_path.exists():
            print(f"  ⚠️  ")
            continue
        
        # 
        baseline = load_contract(baseline_path)
        if not baseline:
            continue
        
        # 
        is_compatible, errors = check_breaking_changes(baseline, current, str(relative_path))
        
        if is_compatible:
            print(f"  ✓ ")
        else:
            print(f"  ❌ :")
            for err in errors:
                print(f"    - {err}")
            all_passed = False
        
        print()
    
    # 
    print("="*50)
    if all_passed:
        print("✅ ")
        print("💡 : make update_baselines")
        sys.exit(0)
    else:
        print("❌ ")
        print("💡 ")
        sys.exit(1)

if __name__ == '__main__':
    main()

