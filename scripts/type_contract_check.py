#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
type_contract_check.py - 模块类型契约校验工具

功能：
1. 读取MODULE_TYPE_CONTRACTS.yaml中的类型定义
2. 扫描modules/目录下的所有模块
3. 检查每个模块的IO是否符合其声明的类型契约
4. 验证输入/输出字段是否匹配

用法：
    python scripts/type_contract_check.py
    make type_contract_check
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 设置Windows控制台UTF-8输出
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
MODULES_DIR = REPO_ROOT / "modules"
CONTRACTS_FILE = REPO_ROOT / "doc" / "modules" / "MODULE_TYPE_CONTRACTS.yaml"
REGISTRY_FILE = REPO_ROOT / "doc" / "orchestration" / "registry.yaml"

# YAML Front Matter正则
YAML_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL | re.MULTILINE)


def print_header(title):
    """打印标题"""
    print("=" * 60)
    print(title)
    print("=" * 60)


def extract_yaml_front_matter(md_text):
    """提取YAML Front Matter"""
    match = YAML_FRONT_MATTER_RE.match(md_text)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return None


def load_type_contracts():
    """加载类型契约定义"""
    if not CONTRACTS_FILE.exists():
        print(f"❌ 错误: 类型契约文件不存在: {CONTRACTS_FILE}")
        return None
    
    try:
        with open(CONTRACTS_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ 错误: 无法读取类型契约文件: {e}")
        return None


def load_registry():
    """加载模块注册表"""
    if not REGISTRY_FILE.exists():
        return None
    
    try:
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        return None


def find_all_agent_md():
    """查找所有modules/下的agent.md文件"""
    agent_files = []
    
    if not MODULES_DIR.exists():
        return agent_files
    
    for module_dir in MODULES_DIR.iterdir():
        if not module_dir.is_dir():
            continue
        
        agent_file = module_dir / "agent.md"
        if agent_file.exists():
            agent_files.append(agent_file)
    
    return agent_files


def get_module_type_from_registry(module_path: str, registry: dict) -> Optional[str]:
    """从registry.yaml获取模块的类型"""
    if not registry or 'module_instances' not in registry:
        return None
    
    for instance in registry.get('module_instances', []):
        if instance.get('path') == module_path:
            return instance.get('type')
    
    return None


def get_type_contract(type_id: str, contracts: dict) -> Optional[dict]:
    """获取指定类型的契约定义"""
    for contract in contracts.get('type_contracts', []):
        if contract.get('id') == type_id:
            return contract
    return None


def validate_io_fields(module_io: dict, contract_io: dict, io_type: str) -> Tuple[bool, List[str]]:
    """
    验证模块的IO字段是否符合契约
    
    Args:
        module_io: 模块定义的IO（从agent.md）
        contract_io: 契约定义的IO（从CONTRACTS.yaml）
        io_type: 'inputs' 或 'outputs'
    
    Returns:
        (是否通过, 错误消息列表)
    """
    errors = []
    
    if not module_io or io_type not in module_io:
        errors.append(f"  ❌ 模块缺少{io_type}定义")
        return False, errors
    
    module_fields = module_io.get(io_type, [])
    contract_fields = contract_io.get(io_type, [])
    
    # 创建字段名映射
    module_field_names = {f.get('name') for f in module_fields if isinstance(f, dict)}
    contract_required_fields = {
        f.get('name') for f in contract_fields 
        if isinstance(f, dict) and f.get('required', False)
    }
    
    # 检查必需字段
    missing_fields = contract_required_fields - module_field_names
    if missing_fields:
        errors.append(f"  ❌ {io_type}缺少必需字段: {', '.join(missing_fields)}")
        return False, errors
    
    return True, []


def check_module_contract(agent_file: Path, contracts: dict, registry: dict) -> Tuple[bool, List[str]]:
    """
    检查单个模块是否符合类型契约
    
    Returns:
        (是否通过, 错误/警告消息列表)
    """
    messages = []
    
    # 读取agent.md
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, [f"❌ 无法读取文件: {e}"]
    
    # 提取YAML
    yaml_data = extract_yaml_front_matter(content)
    if not yaml_data:
        return False, ["❌ 无法提取YAML Front Matter"]
    
    # 获取模块类型
    module_type = yaml_data.get('module_type')
    if not module_type:
        return False, ["❌ agent.md中缺少module_type字段"]
    
    # 获取类型契约
    type_contract = get_type_contract(module_type, contracts)
    if not type_contract:
        return False, [f"❌ 未找到类型'{module_type}'的契约定义"]
    
    # 验证IO契约
    all_pass = True
    
    # 获取模块的io定义
    module_io = yaml_data.get('io', {})
    
    # 验证inputs
    pass_inputs, input_errors = validate_io_fields(
        module_io, 
        type_contract.get('io_contract', {}), 
        'inputs'
    )
    if not pass_inputs:
        all_pass = False
        messages.extend(input_errors)
    
    # 验证outputs
    pass_outputs, output_errors = validate_io_fields(
        module_io, 
        type_contract.get('io_contract', {}), 
        'outputs'
    )
    if not pass_outputs:
        all_pass = False
        messages.extend(output_errors)
    
    # 验证level范围
    module_level = yaml_data.get('level')
    level_range = type_contract.get('level_range', [])
    if module_level and level_range:
        if module_level < level_range[0] or module_level > level_range[1]:
            all_pass = False
            messages.append(
                f"  ❌ Level {module_level} 超出类型允许范围 {level_range}"
            )
    
    if all_pass:
        messages.append("  ✓ IO契约符合类型定义")
    
    return all_pass, messages


def main():
    """主函数"""
    print_header("模块类型契约校验")
    
    # 1. 加载类型契约
    contracts = load_type_contracts()
    if not contracts:
        sys.exit(1)
    
    print(f"✓ 类型契约已加载: {CONTRACTS_FILE.relative_to(REPO_ROOT)}")
    type_count = len(contracts.get('type_contracts', []))
    print(f"✓ 已定义类型: {type_count}个")
    
    # 2. 加载注册表
    registry = load_registry()
    if registry:
        print(f"✓ 模块注册表已加载")
    
    # 3. 查找所有模块
    agent_files = find_all_agent_md()
    
    if not agent_files:
        print("\n⚠️  警告: modules/目录下未找到任何模块")
        print("提示: 当创建业务模块后，此工具将校验其IO契约")
        print()
        print("=" * 60)
        print("✅ 校验完成（无模块需要检查）")
        print("=" * 60)
        return
    
    print(f"✓ 找到{len(agent_files)}个模块")
    print()
    
    # 4. 检查每个模块
    print("检查模块契约...")
    print()
    
    results = []
    for agent_file in agent_files:
        module_name = agent_file.parent.name
        print(f"[检查] {module_name}")
        
        passed, messages = check_module_contract(agent_file, contracts, registry)
        results.append((module_name, passed))
        
        for msg in messages:
            print(msg)
        print()
    
    # 5. 汇总结果
    print()
    print_header("检查完成")
    
    passed_count = sum(1 for _, p in results if p)
    failed_count = len(results) - passed_count
    
    print(f"总计: {len(results)}个模块")
    print(f"通过: {passed_count}个")
    print(f"失败: {failed_count}个")
    print()
    
    if failed_count > 0:
        print("❌ 部分模块的IO契约不符合类型定义")
        print()
        print("建议:")
        print("1. 查看MODULE_TYPE_CONTRACTS.yaml中的类型定义")
        print("2. 更新模块agent.md中的io字段")
        print("3. 确保必需字段都已定义")
        print("4. 运行 make agent_lint 验证YAML格式")
        sys.exit(1)
    else:
        print("=" * 60)
        print("✅ 所有模块的IO契约都符合类型定义")
        print("=" * 60)


if __name__ == "__main__":
    main()

