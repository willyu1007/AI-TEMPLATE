#!/usr/bin/env python3
"""

 app/  apps/ 
"""

import sys
import os
import pathlib
import re
from typing import List, Tuple

# Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def check_mutual_exclusivity() -> Tuple[bool, str]:
    """ app/  apps/ """
    app_exists = pathlib.Path('app').exists()
    apps_exists = pathlib.Path('apps').exists()
    
    if app_exists and apps_exists:
        return False, "app/  apps/ "
    
    return True, ""


def check_app_structure(app_dir: pathlib.Path) -> Tuple[bool, List[str]]:
    """"""
    issues = []
    
    # 
    main_files = list(app_dir.glob('main.py')) + list(app_dir.glob('main.go')) + list(app_dir.glob('main.ts'))
    if not main_files:
        issues.append(f" (main.py/main.go/main.ts)")
    
    # 
    routes_dir = app_dir / 'routes'
    if not routes_dir.exists():
        issues.append(f" routes/ ")
    
    return len(issues) == 0, issues


def check_business_logic_in_app(app_dir: pathlib.Path) -> Tuple[bool, List[str]]:
    """"""
    issues = []
    
    # 
    forbidden_patterns = [
        r'service\.py$',           # 
        r'business_logic',         # 
        r'models/[^/]+\.py$',      #  modules/  common/
    ]
    
    # 
    for py_file in app_dir.rglob('*.py'):
        #  __init__.py  main.py
        if py_file.name in ['__init__.py', 'main.py']:
            continue
        
        file_content = ''
        try:
            file_content = py_file.read_text(encoding='utf-8')
        except Exception:
            continue
        
        # 
        business_logic_keywords = [
            'def create_', 'def update_', 'def delete_',  # CRUD 
            'class Service', 'class Business',  # 
            'from modules.*import.*service',  # 
        ]
        
        for keyword in business_logic_keywords:
            if re.search(keyword, file_content, re.IGNORECASE):
                relative_path = py_file.relative_to(app_dir)
                issues.append(f": {relative_path} ( modules/)")
                break
    
    return len(issues) == 0, issues


def check_routes_reference_modules(app_dir: pathlib.Path) -> Tuple[bool, List[str]]:
    """ modules"""
    issues = []
    routes_dir = app_dir / 'routes'
    
    if not routes_dir.exists():
        return True, issues
    
    # 
    for route_file in routes_dir.rglob('*.py'):
        try:
            content = route_file.read_text(encoding='utf-8')
        except Exception:
            continue
        
        #  modules
        has_module_import = bool(re.search(r'from modules\.', content) or 
                                 re.search(r'import.*modules\.', content))
        
        # 
        has_business_logic = bool(re.search(r'def (create|update|delete|get)_', content, re.IGNORECASE))
        
        if has_business_logic and not has_module_import:
            relative_path = route_file.relative_to(app_dir)
            issues.append(f": {relative_path} ( modules/)")
    
    return len(issues) == 0, issues


def check_global_directories() -> Tuple[bool, List[str]]:
    """"""
    issues = []
    
    # config/  common/ 
    if pathlib.Path('app/config').exists():
        issues.append("config/  app/ ")
    
    if pathlib.Path('app/common').exists():
        issues.append("common/  app/ ")
    
    if pathlib.Path('apps/config').exists():
        issues.append("config/  apps/ ")
    
    if pathlib.Path('apps/common').exists():
        issues.append("common/  apps/ ")
    
    return len(issues) == 0, issues


def _check_app_directory(app_path: pathlib.Path) -> Tuple[bool, List[str]]:
    """app"""
    all_issues = []
    
    # 
    print("[2]  app/ ...")
    structure_ok, structure_issues = check_app_structure(app_path)
    if structure_issues:
        for issue in structure_issues:
            print(f"  ⚠️  {issue}")
            all_issues.append(issue)
    else:
        print(f"  ✓ ")
    print()
    
    # 
    print("[3]  app/ ...")
    logic_ok, logic_issues = check_business_logic_in_app(app_path)
    if logic_issues:
        for issue in logic_issues[:5]:  # 5
            print(f"  ⚠️  {issue}")
        if len(logic_issues) > 5:
            print(f"  ...  {len(logic_issues) - 5} ")
        all_issues.extend(logic_issues)
    else:
        print(f"  ✓ ")
    print()
    
    # 
    print("[4]  app/ ...")
    routes_ok, routes_issues = check_routes_reference_modules(app_path)
    if routes_issues:
        for issue in routes_issues:
            print(f"  ⚠️  {issue}")
            all_issues.append(issue)
    else:
        print(f"  ✓ ")
    print()
    
    return len(all_issues) == 0, all_issues


def _check_apps_directory() -> Tuple[bool, List[str]]:
    """apps"""
    all_issues = []
    
    print("[2]  apps/ ...")
    for app_subdir in pathlib.Path('apps').iterdir():
        if app_subdir.is_dir():
            app_name = app_subdir.name
            print(f"  : {app_name}")
            structure_ok, structure_issues = check_app_structure(app_subdir)
            if structure_issues:
                for issue in structure_issues:
                    print(f"    ⚠️  {issue}")
                    all_issues.append(f"{app_name}: {issue}")
            else:
                print(f"    ✓ ")
            
            logic_ok, logic_issues = check_business_logic_in_app(app_subdir)
            if logic_issues:
                for issue in logic_issues[:3]:
                    print(f"    ⚠️  {issue}")
                all_issues.extend([f"{app_name}: {issue}" for issue in logic_issues])
            
            routes_ok, routes_issues = check_routes_reference_modules(app_subdir)
            if routes_issues:
                for issue in routes_issues:
                    print(f"    ⚠️  {issue}")
                    all_issues.append(f"{app_name}: {issue}")
    print()
    
    return len(all_issues) == 0, all_issues


def main():
    """"""
    print("...\n")
    
    all_passed = True
    app_exists = pathlib.Path('app').exists()
    apps_exists = pathlib.Path('apps').exists()
    
    # 1. 
    print("[1]  app/  apps/ ...")
    mutex_ok, mutex_msg = check_mutual_exclusivity()
    if not mutex_ok:
        print(f"  ❌ {mutex_msg}")
        all_passed = False
    else:
        print(f"  ✓ ")
    print()
    
    # 2-4. appapps
    if app_exists:
        app_ok, app_issues = _check_app_directory(pathlib.Path('app'))
        if not app_ok:
            all_passed = False
    elif apps_exists:
        apps_ok, apps_issues = _check_apps_directory()
        if not apps_ok:
            all_passed = False
    
    # 5. 
    print("[5] ...")
    global_ok, global_issues = check_global_directories()
    if global_issues:
        for issue in global_issues:
            print(f"  ❌ {issue}")
        all_passed = False
    else:
        print(f"  ✓ ")
    print()
    
    # 
    print("=" * 50)
    if all_passed:
        print("✅ ")
        sys.exit(0)
    else:
        print("⚠️  ")
        print("💡 : ")
        sys.exit(1)


if __name__ == '__main__':
    main()

