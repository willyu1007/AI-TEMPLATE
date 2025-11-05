#!/usr/bin/env python3
"""
应用层结构检查脚本
检查 app/ 和 apps/ 目录的职责边界和结构正确性
"""

import sys
import os
import pathlib
import re
from typing import List, Tuple

# Windows控制台编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def check_mutual_exclusivity() -> Tuple[bool, str]:
    """检查 app/ 和 apps/ 的互斥性"""
    app_exists = pathlib.Path('app').exists()
    apps_exists = pathlib.Path('apps').exists()
    
    if app_exists and apps_exists:
        return False, "app/ 和 apps/ 不能同时存在"
    
    return True, ""


def check_app_structure(app_dir: pathlib.Path) -> Tuple[bool, List[str]]:
    """检查应用层目录结构"""
    issues = []
    
    # 检查必要文件
    main_files = list(app_dir.glob('main.py')) + list(app_dir.glob('main.go')) + list(app_dir.glob('main.ts'))
    if not main_files:
        issues.append(f"缺少应用入口文件 (main.py/main.go/main.ts)")
    
    # 检查路由目录
    routes_dir = app_dir / 'routes'
    if not routes_dir.exists():
        issues.append(f"缺少 routes/ 目录")
    
    return len(issues) == 0, issues


def check_business_logic_in_app(app_dir: pathlib.Path) -> Tuple[bool, List[str]]:
    """检查应用层是否包含业务逻辑"""
    issues = []
    
    # 禁止的模式
    forbidden_patterns = [
        r'service\.py$',           # 服务层代码
        r'business_logic',         # 业务逻辑
        r'models/[^/]+\.py$',      # 数据模型（应在 modules/ 或 common/）
    ]
    
    # 检查文件
    for py_file in app_dir.rglob('*.py'):
        # 跳过 __init__.py 和 main.py
        if py_file.name in ['__init__.py', 'main.py']:
            continue
        
        file_content = ''
        try:
            file_content = py_file.read_text(encoding='utf-8')
        except Exception:
            continue
        
        # 检查是否包含业务逻辑关键词
        business_logic_keywords = [
            'def create_', 'def update_', 'def delete_',  # CRUD 操作
            'class Service', 'class Business',  # 业务类
            'from modules.*import.*service',  # 导入服务层
        ]
        
        for keyword in business_logic_keywords:
            if re.search(keyword, file_content, re.IGNORECASE):
                relative_path = py_file.relative_to(app_dir)
                issues.append(f"发现业务逻辑: {relative_path} (应移动到 modules/)")
                break
    
    return len(issues) == 0, issues


def check_routes_reference_modules(app_dir: pathlib.Path) -> Tuple[bool, List[str]]:
    """检查路由是否正确引用 modules"""
    issues = []
    routes_dir = app_dir / 'routes'
    
    if not routes_dir.exists():
        return True, issues
    
    # 检查路由文件
    for route_file in routes_dir.rglob('*.py'):
        try:
            content = route_file.read_text(encoding='utf-8')
        except Exception:
            continue
        
        # 检查是否导入 modules
        has_module_import = bool(re.search(r'from modules\.', content) or 
                                 re.search(r'import.*modules\.', content))
        
        # 检查是否直接实现业务逻辑
        has_business_logic = bool(re.search(r'def (create|update|delete|get)_', content, re.IGNORECASE))
        
        if has_business_logic and not has_module_import:
            relative_path = route_file.relative_to(app_dir)
            issues.append(f"路由文件包含业务逻辑: {relative_path} (应调用 modules/)")
    
    return len(issues) == 0, issues


def check_global_directories() -> Tuple[bool, List[str]]:
    """检查全局目录是否在正确位置"""
    issues = []
    
    # config/ 和 common/ 应该在根目录
    if pathlib.Path('app/config').exists():
        issues.append("config/ 不应在 app/ 目录下，应保持在根目录")
    
    if pathlib.Path('app/common').exists():
        issues.append("common/ 不应在 app/ 目录下，应保持在根目录")
    
    if pathlib.Path('apps/config').exists():
        issues.append("config/ 不应在 apps/ 目录下，应保持在根目录")
    
    if pathlib.Path('apps/common').exists():
        issues.append("common/ 不应在 apps/ 目录下，应保持在根目录")
    
    return len(issues) == 0, issues


def main():
    """主函数"""
    print("检查应用层结构...\n")
    
    all_passed = True
    app_exists = pathlib.Path('app').exists()
    apps_exists = pathlib.Path('apps').exists()
    
    # 1. 检查互斥性
    print("[1] 检查 app/ 和 apps/ 互斥性...")
    mutex_ok, mutex_msg = check_mutual_exclusivity()
    if not mutex_ok:
        print(f"  ❌ {mutex_msg}")
        all_passed = False
    else:
        print(f"  ✓ 互斥性检查通过")
    print()
    
    # 2. 检查目录结构
    if app_exists:
        print("[2] 检查 app/ 目录结构...")
        structure_ok, structure_issues = check_app_structure(pathlib.Path('app'))
        if structure_issues:
            for issue in structure_issues:
                print(f"  ⚠️  {issue}")
        else:
            print(f"  ✓ 目录结构完整")
        print()
        
        # 3. 检查业务逻辑
        print("[3] 检查 app/ 是否包含业务逻辑...")
        logic_ok, logic_issues = check_business_logic_in_app(pathlib.Path('app'))
        if logic_issues:
            for issue in logic_issues[:5]:  # 只显示前5个
                print(f"  ⚠️  {issue}")
            if len(logic_issues) > 5:
                print(f"  ... 还有 {len(logic_issues) - 5} 个问题")
            all_passed = False
        else:
            print(f"  ✓ 未发现业务逻辑")
        print()
        
        # 4. 检查路由引用
        print("[4] 检查 app/ 路由配置...")
        routes_ok, routes_issues = check_routes_reference_modules(pathlib.Path('app'))
        if routes_issues:
            for issue in routes_issues:
                print(f"  ⚠️  {issue}")
            all_passed = False
        else:
            print(f"  ✓ 路由配置正确")
        print()
    
    elif apps_exists:
        print("[2] 检查 apps/ 目录结构...")
        for app_subdir in pathlib.Path('apps').iterdir():
            if app_subdir.is_dir():
                app_name = app_subdir.name
                print(f"  检查应用: {app_name}")
                structure_ok, structure_issues = check_app_structure(app_subdir)
                if structure_issues:
                    for issue in structure_issues:
                        print(f"    ⚠️  {issue}")
                else:
                    print(f"    ✓ 目录结构完整")
                
                logic_ok, logic_issues = check_business_logic_in_app(app_subdir)
                if logic_issues:
                    for issue in logic_issues[:3]:
                        print(f"    ⚠️  {issue}")
                    all_passed = False
                
                routes_ok, routes_issues = check_routes_reference_modules(app_subdir)
                if routes_issues:
                    for issue in routes_issues:
                        print(f"    ⚠️  {issue}")
                    all_passed = False
        print()
    
    # 5. 检查全局目录
    print("[5] 检查全局目录位置...")
    global_ok, global_issues = check_global_directories()
    if global_issues:
        for issue in global_issues:
            print(f"  ❌ {issue}")
        all_passed = False
    else:
        print(f"  ✓ 全局目录位置正确")
    print()
    
    # 总结
    print("=" * 50)
    if all_passed:
        print("✅ 应用层结构检查通过")
        sys.exit(0)
    else:
        print("⚠️  应用层结构检查发现问题")
        print("💡 建议: 修复上述问题，确保应用层只负责路由和入口")
        sys.exit(1)


if __name__ == '__main__':
    main()

