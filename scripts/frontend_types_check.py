#!/usr/bin/env python3
"""
 OpenAPI 


1. OpenAPI 
2. 
3.  OpenAPI 
"""
import json
import pathlib
import sys
from typing import List, Tuple

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def check_openapi_exists(openapi_file: pathlib.Path) -> Tuple[bool, str]:
    """ OpenAPI """
    if not openapi_file.exists():
        return False, f"OpenAPI : {openapi_file}"
    
    try:
        with open(openapi_file, "r", encoding="utf-8") as f:
            json.load(f)
        return True, "OpenAPI "
    except Exception as e:
        return False, f"OpenAPI : {e}"


def find_frontend_dirs(workspace_root: pathlib.Path) -> List[pathlib.Path]:
    """"""
    frontend_dirs = []
    
    #  frontend/
    frontend_dir = workspace_root / "frontend"
    if frontend_dir.exists() and frontend_dir.is_dir():
        frontend_dirs.append(frontend_dir)
    
    #  frontends/
    frontends_dir = workspace_root / "frontends"
    if frontends_dir.exists() and frontends_dir.is_dir():
        for app_dir in frontends_dir.iterdir():
            if app_dir.is_dir():
                frontend_dirs.append(app_dir)
    
    return frontend_dirs


def find_types_file(frontend_dir: pathlib.Path) -> pathlib.Path:
    """"""
    #  src/types/api.d.ts types/api.d.ts
    candidates = [
        frontend_dir / "src" / "types" / "api.d.ts",
        frontend_dir / "types" / "api.d.ts"
    ]
    
    for candidate in candidates:
        if candidate.exists():
            return candidate
    
    return None


def check_types_sync(openapi_file: pathlib.Path, types_file: pathlib.Path) -> Tuple[bool, str]:
    """ OpenAPI """
    if not types_file.exists():
        return False, f": {types_file}"
    
    # 
    openapi_mtime = openapi_file.stat().st_mtime
    types_mtime = types_file.stat().st_mtime
    
    if openapi_mtime > types_mtime:
        return False, f"OpenAPI  {openapi_mtime} {types_mtime}"
    
    return True, ""


def main():
    """"""
    workspace_root = pathlib.Path(__file__).parent.parent
    openapi_file = workspace_root / "tools" / "openapi.json"
    
    print("[INFO] ...")
    
    #  OpenAPI 
    openapi_ok, openapi_msg = check_openapi_exists(openapi_file)
    if not openapi_ok:
        print(f"[WARN] {openapi_msg}")
        print("[INFO] : make generate_openapi")
        # OpenAPI 
        # 
        sys.exit(0)
    
    print(f"[OK] {openapi_msg}")
    
    # 
    frontend_dirs = find_frontend_dirs(workspace_root)
    
    if not frontend_dirs:
        print("[INFO] ")
        return
    
    print(f"[INFO]  {len(frontend_dirs)} ")
    
    # 
    all_ok = True
    for frontend_dir in frontend_dirs:
        print(f"[INFO] : {frontend_dir.name}")
        
        types_file = find_types_file(frontend_dir)
        if not types_file:
            print(f"[WARN] : {frontend_dir.name}")
            print(f"[INFO] : make generate_frontend_types")
            all_ok = False
            continue
        
        sync_ok, sync_msg = check_types_sync(openapi_file, types_file)
        if not sync_ok:
            print(f"[ERROR] {sync_msg}")
            print(f"[INFO] : make generate_frontend_types")
            all_ok = False
        else:
            print(f"[OK] {sync_msg}")
    
    if not all_ok:
        print("\n[ERROR] ")
        sys.exit(1)
    
    print("\n[OK] ")


if __name__ == "__main__":
    main()

