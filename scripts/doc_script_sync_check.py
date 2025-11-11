#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_script_sync_check.py - 


1. make
2. scripts/
3. 
   - 
   - 
4. 


    python scripts/doc_script_sync_check.py
    make doc_script_sync_check
    

    Phase 9
"""

import os
import sys
import re
from pathlib import Path
from typing import Set, Dict, List, Tuple

# WindowsUTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
DOC_DIR = REPO_ROOT / "doc"
TEMP_DIR = REPO_ROOT / "temp"

# 
DOC_FILES = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "QUICK_START.md",
    REPO_ROOT / "TEMPLATE_USAGE.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "Makefile",
    SCRIPTS_DIR / "README.md",
]

# doc/
for subdir in ["modules", "process", "reference", "init"]:
    doc_subdir = DOC_DIR / subdir
    if doc_subdir.exists():
        for md_file in doc_subdir.rglob("*.md"):
            DOC_FILES.append(md_file)

# 
SCRIPT_PATTERN = re.compile(r'(?:scripts/|make\s+)([a-z_][a-z0-9_]*(?:\.py|\.sh)?)', re.IGNORECASE)
MAKE_PATTERN = re.compile(r'make\s+([a-z_][a-z0-9_]*)', re.IGNORECASE)


def print_header(title):
    """"""
    print("=" * 60)
    print(title)
    print("=" * 60)


def get_actual_scripts() -> Dict[str, str]:
    """
    scripts/
    
    Returns:
        {: }
    """
    scripts = {}
    
    if not SCRIPTS_DIR.exists():
        return scripts
    
    for script_file in SCRIPTS_DIR.iterdir():
        if script_file.is_file() and script_file.suffix in ['.py', '.sh']:
            # 
            name = script_file.stem
            scripts[name] = str(script_file.relative_to(REPO_ROOT))
    
    return scripts


def extract_scripts_from_makefile() -> Dict[str, Set[str]]:
    """
    Makefilemake
    
    Returns:
        {make: {}}
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
                
                # maketab:
                if line and not line.startswith('\t') and ':' in line and not line.startswith('#'):
                    target = line.split(':')[0].strip()
                    # 
                    if target and not target.startswith('.') and '=' not in target:
                        current_target = target
                        make_targets[current_target] = set()
                
                # tab
                elif line.startswith('\t') and current_target:
                    # python/bash
                    if 'python' in line or 'bash' in line or './' in line:
                        # 
                        matches = re.findall(r'scripts/([a-z_][a-z0-9_]*\.(?:py|sh))', line)
                        for match in matches:
                            script_name = match.replace('.py', '').replace('.sh', '')
                            make_targets[current_target].add(script_name)
    
    except Exception as e:
        print(f"⚠️  : Makefile: {e}")
    
    return make_targets


def extract_mentioned_scripts(doc_file: Path) -> Set[str]:
    """
    make
    
    Returns:
        
    """
    mentioned = set()
    
    if not doc_file.exists():
        return mentioned
    
    try:
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return mentioned
    
    # scripts/xxx.pyscripts/xxx.sh
    script_matches = re.findall(r'scripts/([a-z_][a-z0-9_]*?)\.(?:py|sh)', content, re.IGNORECASE)
    for match in script_matches:
        mentioned.add(match)
    
    # make xxx
    make_matches = re.findall(r'make\s+([a-z_][a-z0-9_]*)', content, re.IGNORECASE)
    for match in make_matches:
        mentioned.add(match)
    
    return mentioned


def get_all_mentioned_scripts() -> Dict[str, List[str]]:
    """
    
    
    Returns:
        {: []}
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
    
    
    Returns:
        (, , make)
    """
    # 1. 
    actual_scripts = get_actual_scripts()
    
    # 2. 
    mentioned_scripts = get_all_mentioned_scripts()
    
    # 3. Makefilemake
    make_targets = extract_scripts_from_makefile()
    
    return mentioned_scripts, actual_scripts, make_targets


def main():
    """"""
    print_header("")
    
    # 1. 
    print("...")
    mentioned_scripts, actual_scripts, make_targets = check_sync()
    
    print(f"✓ ")
    print(f"  - /: {len(mentioned_scripts)}")
    print(f"  - scripts/: {len(actual_scripts)}")
    print(f"  - Makefilemake: {len(make_targets)}")
    print()
    
    # 2. 
    print_header("")
    print()
    
    # 1: 
    missing_scripts = []
    for mentioned in mentioned_scripts:
        # 
        if mentioned in actual_scripts:
            continue
        
        # make
        if mentioned in make_targets:
            # make
            scripts_used = make_targets[mentioned]
            if scripts_used and all(s in actual_scripts for s in scripts_used):
                continue  # make
            elif not scripts_used:
                continue  # make
        
        missing_scripts.append((mentioned, mentioned_scripts[mentioned]))
    
    # 2: 
    orphan_scripts = []
    for script_name, script_path in actual_scripts.items():
        # 
        if script_name not in mentioned_scripts:
            # make
            used_by_make = [
                target for target, scripts in make_targets.items()
                if script_name in scripts
            ]
            if not used_by_make:
                orphan_scripts.append((script_name, script_path))
    
    # 3. 
    has_issues = False
    
    if missing_scripts:
        has_issues = True
        print("❌ /:")
        print()
        for script, docs in missing_scripts:
            print(f"  [{script}]")
            print(f"    :")
            for doc in docs[:3]:  # 3
                print(f"      - {doc}")
            if len(docs) > 3:
                print(f"      - ... {len(docs)-3}")
            print()
    else:
        print("✅ ")
        print()
    
    if orphan_scripts:
        has_issues = True
        print("⚠️  :")
        print()
        for script, path in orphan_scripts:
            print(f"  [{script}]")
            print(f"    : {path}")
            print(f"    : ")
            print()
    else:
        print("✅ ")
        print()
    
    # 4. make
    if make_targets:
        print()
        print("📋 Make:")
        print()
        for target, scripts in sorted(make_targets.items()):
            if scripts:
                print(f"  make {target}")
                for script in sorted(scripts):
                    status = "✓" if script in actual_scripts else "✗"
                    print(f"    {status} scripts/{script}")
        print()
    
    # 5. 
    print()
    print_header("")
    
    if has_issues:
        print()
        print(":")
        if missing_scripts:
            print(f"  - : {len(missing_scripts)}")
        if orphan_scripts:
            print(f"  - : {len(orphan_scripts)}")
        print()
        print(":")
        print("1. ")
        print("2. ")
        print("3. scripts/README.md")
        print()
        print("=" * 60)
        print("⚠️  ")
        print("=" * 60)
        sys.exit(0)  # 
    else:
        print()
        print("=" * 60)
        print("✅ ")
        print("=" * 60)


if __name__ == "__main__":
    main()

