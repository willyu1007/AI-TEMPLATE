#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_script_sync_check.py - 文档与脚本同步检查工具

功能：
1. 扫描文档中提及的所有脚本和make命令
2. 扫描scripts/目录下的所有实际脚本
3. 双向对比，发现：
   - 文档提及但脚本不存在（缺失实现）
   - 脚本存在但文档未提及（孤儿脚本）
4. 生成同步报告

用法：
    python scripts/doc_script_sync_check.py
    make doc_script_sync_check
    
建议：
    在Phase 9（文档审查与清理）中运行此检查
"""

import os
import sys
import re
from pathlib import Path
from typing import Set, Dict, List, Tuple

# 设置Windows控制台UTF-8输出
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
DOC_DIR = REPO_ROOT / "doc"
TEMP_DIR = REPO_ROOT / "temp"

# 需要扫描的文档
DOC_FILES = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "QUICK_START.md",
    REPO_ROOT / "TEMPLATE_USAGE.md",
    REPO_ROOT / "agent.md",
    REPO_ROOT / "Makefile",
    SCRIPTS_DIR / "README.md",
]

# 添加doc/下的主要文档
for subdir in ["modules", "process", "reference", "init"]:
    doc_subdir = DOC_DIR / subdir
    if doc_subdir.exists():
        for md_file in doc_subdir.rglob("*.md"):
            DOC_FILES.append(md_file)

# 脚本名称模式
SCRIPT_PATTERN = re.compile(r'(?:scripts/|make\s+)([a-z_][a-z0-9_]*(?:\.py|\.sh)?)', re.IGNORECASE)
MAKE_PATTERN = re.compile(r'make\s+([a-z_][a-z0-9_]*)', re.IGNORECASE)


def print_header(title):
    """打印标题"""
    print("=" * 60)
    print(title)
    print("=" * 60)


def get_actual_scripts() -> Dict[str, str]:
    """
    获取scripts/目录下的所有实际脚本
    
    Returns:
        {脚本名: 脚本路径}
    """
    scripts = {}
    
    if not SCRIPTS_DIR.exists():
        return scripts
    
    for script_file in SCRIPTS_DIR.iterdir():
        if script_file.is_file() and script_file.suffix in ['.py', '.sh']:
            # 脚本名（不含扩展名）
            name = script_file.stem
            scripts[name] = str(script_file.relative_to(REPO_ROOT))
    
    return scripts


def extract_scripts_from_makefile() -> Dict[str, Set[str]]:
    """
    从Makefile提取make命令和其使用的脚本
    
    Returns:
        {make命令: {使用的脚本集合}}
    """
    makefile = REPO_ROOT / "Makefile"
    if not makefile.exists():
        return {}
    
    make_targets = {}
    current_target = None
    
    try:
        with open(makefile, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip()
                
                # 检测make目标（不以tab开头的行，以:结尾）
                if line and not line.startswith('\t') and ':' in line and not line.startswith('#'):
                    target = line.split(':')[0].strip()
                    # 过滤掉变量定义和特殊目标
                    if target and not target.startswith('.') and '=' not in target:
                        current_target = target
                        make_targets[current_target] = set()
                
                # 检测脚本调用（以tab开头）
                elif line.startswith('\t') and current_target:
                    # 查找python/bash调用
                    if 'python' in line or 'bash' in line or './' in line:
                        # 提取脚本名
                        matches = re.findall(r'scripts/([a-z_][a-z0-9_]*\.(?:py|sh))', line)
                        for match in matches:
                            script_name = match.replace('.py', '').replace('.sh', '')
                            make_targets[current_target].add(script_name)
    
    except Exception as e:
        print(f"⚠️  警告: 无法读取Makefile: {e}")
    
    return make_targets


def extract_mentioned_scripts(doc_file: Path) -> Set[str]:
    """
    从文档中提取提及的脚本和make命令
    
    Returns:
        提及的脚本名集合（不含扩展名）
    """
    mentioned = set()
    
    if not doc_file.exists():
        return mentioned
    
    try:
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return mentioned
    
    # 提取scripts/xxx.py或scripts/xxx.sh
    script_matches = re.findall(r'scripts/([a-z_][a-z0-9_]*?)\.(?:py|sh)', content, re.IGNORECASE)
    for match in script_matches:
        mentioned.add(match)
    
    # 提取make xxx命令
    make_matches = re.findall(r'make\s+([a-z_][a-z0-9_]*)', content, re.IGNORECASE)
    for match in make_matches:
        mentioned.add(match)
    
    return mentioned


def get_all_mentioned_scripts() -> Dict[str, List[str]]:
    """
    扫描所有文档，获取提及的脚本
    
    Returns:
        {脚本名: [提及它的文档列表]}
    """
    all_mentioned = {}
    
    for doc_file in DOC_FILES:
        if not doc_file.exists():
            continue
        
        mentioned = extract_mentioned_scripts(doc_file)
        for script in mentioned:
            if script not in all_mentioned:
                all_mentioned[script] = []
            all_mentioned[script].append(str(doc_file.relative_to(REPO_ROOT)))
    
    return all_mentioned


def check_sync() -> Tuple[Dict, Dict, Dict]:
    """
    执行双向检查
    
    Returns:
        (文档提及的脚本, 实际存在的脚本, make命令映射)
    """
    # 1. 获取实际脚本
    actual_scripts = get_actual_scripts()
    
    # 2. 获取文档提及的脚本
    mentioned_scripts = get_all_mentioned_scripts()
    
    # 3. 获取Makefile的make命令
    make_targets = extract_scripts_from_makefile()
    
    return mentioned_scripts, actual_scripts, make_targets


def main():
    """主函数"""
    print_header("文档与脚本同步检查")
    
    # 1. 扫描
    print("扫描文档...")
    mentioned_scripts, actual_scripts, make_targets = check_sync()
    
    print(f"✓ 扫描完成")
    print(f"  - 文档提及的脚本/命令: {len(mentioned_scripts)}个")
    print(f"  - scripts/目录下的脚本: {len(actual_scripts)}个")
    print(f"  - Makefile中的make命令: {len(make_targets)}个")
    print()
    
    # 2. 双向检查
    print_header("双向一致性检查")
    print()
    
    # 检查1: 文档提及但脚本不存在（缺失实现）
    missing_scripts = []
    for mentioned in mentioned_scripts:
        # 检查是否是实际脚本
        if mentioned in actual_scripts:
            continue
        
        # 检查是否是make命令
        if mentioned in make_targets:
            # 检查make命令是否调用了实际存在的脚本
            scripts_used = make_targets[mentioned]
            if scripts_used and all(s in actual_scripts for s in scripts_used):
                continue  # make命令有效
            elif not scripts_used:
                continue  # make命令不调用脚本（如只是输出）
        
        missing_scripts.append((mentioned, mentioned_scripts[mentioned]))
    
    # 检查2: 脚本存在但文档未提及（孤儿脚本）
    orphan_scripts = []
    for script_name, script_path in actual_scripts.items():
        # 检查是否在文档中提及
        if script_name not in mentioned_scripts:
            # 检查是否被make命令使用
            used_by_make = [
                target for target, scripts in make_targets.items()
                if script_name in scripts
            ]
            if not used_by_make:
                orphan_scripts.append((script_name, script_path))
    
    # 3. 报告结果
    has_issues = False
    
    if missing_scripts:
        has_issues = True
        print("❌ 缺失实现（文档提及但脚本/命令不存在）:")
        print()
        for script, docs in missing_scripts:
            print(f"  [{script}]")
            print(f"    提及文档:")
            for doc in docs[:3]:  # 最多显示3个
                print(f"      - {doc}")
            if len(docs) > 3:
                print(f"      - ... 及其他{len(docs)-3}个文档")
            print()
    else:
        print("✅ 无缺失实现")
        print()
    
    if orphan_scripts:
        has_issues = True
        print("⚠️  孤儿脚本（脚本存在但文档未提及）:")
        print()
        for script, path in orphan_scripts:
            print(f"  [{script}]")
            print(f"    路径: {path}")
            print(f"    建议: 检查是否仍需要，如不需要可删除")
            print()
    else:
        print("✅ 无孤儿脚本")
        print()
    
    # 4. 额外信息：make命令映射
    if make_targets:
        print()
        print("📋 Make命令映射（供参考）:")
        print()
        for target, scripts in sorted(make_targets.items()):
            if scripts:
                print(f"  make {target}")
                for script in sorted(scripts):
                    status = "✓" if script in actual_scripts else "✗"
                    print(f"    {status} scripts/{script}")
        print()
    
    # 5. 汇总
    print()
    print_header("检查完成")
    
    if has_issues:
        print()
        print("发现问题:")
        if missing_scripts:
            print(f"  - 缺失实现: {len(missing_scripts)}个")
        if orphan_scripts:
            print(f"  - 孤儿脚本: {len(orphan_scripts)}个")
        print()
        print("建议:")
        print("1. 对于缺失实现：实现对应的脚本或更新文档")
        print("2. 对于孤儿脚本：在文档中补充说明或删除脚本")
        print("3. 更新scripts/README.md确保所有脚本都有说明")
        print()
        print("=" * 60)
        print("⚠️  发现不一致（允许，建议修复）")
        print("=" * 60)
        sys.exit(0)  # 警告模式，不退出
    else:
        print()
        print("=" * 60)
        print("✅ 文档与脚本完全同步")
        print("=" * 60)


if __name__ == "__main__":
    main()

