#!/usr/bin/env python3
"""
契约兼容性检查：对比基线，检测破坏性变更
"""
import sys
import json
import pathlib
from typing import Dict, List, Tuple

def load_contract(path):
    """加载契约文件"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  无法加载契约 {path}: {e}")
        return None

def find_contract_files():
    """查找所有契约文件"""
    root = pathlib.Path('.')
    contracts = []
    
    # 在 tools/ 目录下查找
    for p in root.glob('tools/**/contract.json'):
        contracts.append(p)
    
    return contracts

def check_breaking_changes(baseline: Dict, current: Dict, path: str) -> Tuple[bool, List[str]]:
    """检查是否有破坏性变更"""
    errors = []
    
    # 检查类型变更
    baseline_type = baseline.get('type')
    current_type = current.get('type')
    if baseline_type and current_type and baseline_type != current_type:
        errors.append(f"类型变更: {baseline_type} -> {current_type}")
    
    # 检查必填字段
    baseline_required = set(baseline.get('required', []))
    current_required = set(current.get('required', []))
    
    # 新增必填字段是破坏性的
    new_required = current_required - baseline_required
    if new_required:
        errors.append(f"新增必填字段: {new_required}")
    
    # 检查字段删除
    baseline_props = set(baseline.get('properties', {}).keys())
    current_props = set(current.get('properties', {}).keys())
    
    deleted_fields = baseline_props - current_props
    if deleted_fields:
        errors.append(f"删除字段: {deleted_fields}")
    
    # 检查字段类型变更
    for field in baseline_props & current_props:
        baseline_field_type = baseline['properties'][field].get('type')
        current_field_type = current['properties'][field].get('type')
        
        if baseline_field_type and current_field_type and baseline_field_type != current_field_type:
            errors.append(f"字段 '{field}' 类型变更: {baseline_field_type} -> {current_field_type}")
    
    return len(errors) == 0, errors

def main():
    print("🔍 开始契约兼容性检查...\n")
    
    baseline_dir = pathlib.Path('.contracts_baseline')
    
    if not baseline_dir.exists():
        print("⚠️  基线目录不存在，创建中...")
        baseline_dir.mkdir(exist_ok=True)
        print("💡 提示：首次运行请执行 'make update_baselines' 创建基线")
        sys.exit(0)
    
    # 查找当前契约文件
    current_contracts = find_contract_files()
    
    if not current_contracts:
        print("⚠️  未找到契约文件")
        sys.exit(0)
    
    print(f"📄 找到 {len(current_contracts)} 个契约文件\n")
    
    all_passed = True
    
    for contract_path in current_contracts:
        relative_path = contract_path.relative_to('.')
        baseline_path = baseline_dir / relative_path
        
        print(f"检查: {relative_path}")
        
        # 加载当前契约
        current = load_contract(contract_path)
        if not current:
            continue
        
        # 检查基线是否存在
        if not baseline_path.exists():
            print(f"  ⚠️  基线不存在（新契约）")
            continue
        
        # 加载基线
        baseline = load_contract(baseline_path)
        if not baseline:
            continue
        
        # 检查兼容性
        is_compatible, errors = check_breaking_changes(baseline, current, str(relative_path))
        
        if is_compatible:
            print(f"  ✓ 兼容")
        else:
            print(f"  ❌ 发现破坏性变更:")
            for err in errors:
                print(f"    - {err}")
            all_passed = False
        
        print()
    
    # 总结
    print("="*50)
    if all_passed:
        print("✅ 契约兼容性检查通过")
        print("💡 若需更新基线: make update_baselines")
        sys.exit(0)
    else:
        print("❌ 契约存在破坏性变更")
        print("💡 请修复变更或创建新版本契约")
        sys.exit(1)

if __name__ == '__main__':
    main()

