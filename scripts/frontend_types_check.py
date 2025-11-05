#!/usr/bin/env python3
"""
检查前端类型与 OpenAPI 契约的一致性

检查项目：
1. OpenAPI 文件是否存在且有效
2. 前端类型文件是否存在
3. 前端类型是否与 OpenAPI 同步（通过文件修改时间）
"""
import json
import pathlib
import sys
from typing import List, Tuple


def check_openapi_exists(openapi_file: pathlib.Path) -> Tuple[bool, str]:
    """检查 OpenAPI 文件是否存在且有效"""
    if not openapi_file.exists():
        return False, f"OpenAPI 文件不存在: {openapi_file}"
    
    try:
        with open(openapi_file, "r", encoding="utf-8") as f:
            json.load(f)
        return True, "OpenAPI 文件有效"
    except Exception as e:
        return False, f"OpenAPI 文件无效: {e}"


def find_frontend_dirs(workspace_root: pathlib.Path) -> List[pathlib.Path]:
    """查找前端目录"""
    frontend_dirs = []
    
    # 检查 frontend/
    frontend_dir = workspace_root / "frontend"
    if frontend_dir.exists() and frontend_dir.is_dir():
        frontend_dirs.append(frontend_dir)
    
    # 检查 frontends/
    frontends_dir = workspace_root / "frontends"
    if frontends_dir.exists() and frontends_dir.is_dir():
        for app_dir in frontends_dir.iterdir():
            if app_dir.is_dir():
                frontend_dirs.append(app_dir)
    
    return frontend_dirs


def find_types_file(frontend_dir: pathlib.Path) -> pathlib.Path:
    """查找类型文件"""
    # 优先使用 src/types/api.d.ts，否则使用 types/api.d.ts
    candidates = [
        frontend_dir / "src" / "types" / "api.d.ts",
        frontend_dir / "types" / "api.d.ts"
    ]
    
    for candidate in candidates:
        if candidate.exists():
            return candidate
    
    return None


def check_types_sync(openapi_file: pathlib.Path, types_file: pathlib.Path) -> Tuple[bool, str]:
    """检查类型文件是否与 OpenAPI 同步"""
    if not types_file.exists():
        return False, f"类型文件不存在: {types_file}"
    
    # 比较修改时间
    openapi_mtime = openapi_file.stat().st_mtime
    types_mtime = types_file.stat().st_mtime
    
    if openapi_mtime > types_mtime:
        return False, f"类型文件已过期（OpenAPI 更新于 {openapi_mtime}，类型文件更新于 {types_mtime}）"
    
    return True, "类型文件已同步"


def main():
    """主函数"""
    workspace_root = pathlib.Path(__file__).parent.parent
    openapi_file = workspace_root / "tools" / "openapi.json"
    
    print("[INFO] 检查前端类型一致性...")
    
    # 检查 OpenAPI 文件
    openapi_ok, openapi_msg = check_openapi_exists(openapi_file)
    if not openapi_ok:
        print(f"[WARN] {openapi_msg}")
        print("[INFO] 请先运行: make generate_openapi")
        # OpenAPI 不存在时，如果有前端目录，应该生成类型
        # 但这里我们只做检查，不生成
        sys.exit(0)
    
    print(f"[OK] {openapi_msg}")
    
    # 查找前端目录
    frontend_dirs = find_frontend_dirs(workspace_root)
    
    if not frontend_dirs:
        print("[INFO] 未找到前端目录，跳过检查")
        return
    
    print(f"[INFO] 找到 {len(frontend_dirs)} 个前端目录")
    
    # 检查每个前端目录
    all_ok = True
    for frontend_dir in frontend_dirs:
        print(f"[INFO] 检查: {frontend_dir.name}")
        
        types_file = find_types_file(frontend_dir)
        if not types_file:
            print(f"[WARN] 类型文件不存在: {frontend_dir.name}")
            print(f"[INFO] 请运行: make generate_frontend_types")
            all_ok = False
            continue
        
        sync_ok, sync_msg = check_types_sync(openapi_file, types_file)
        if not sync_ok:
            print(f"[ERROR] {sync_msg}")
            print(f"[INFO] 请运行: make generate_frontend_types")
            all_ok = False
        else:
            print(f"[OK] {sync_msg}")
    
    if not all_ok:
        print("\n[ERROR] 前端类型检查失败")
        sys.exit(1)
    
    print("\n[OK] 前端类型检查通过")


if __name__ == "__main__":
    main()

