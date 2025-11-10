#!/usr/bin/env python3
"""
 up/down 
"""
import sys
import pathlib
import re

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def find_migrations():
    """"""
    migrations_dir = pathlib.Path('migrations')
    
    if not migrations_dir.exists():
        print("⚠️  migrations/ ")
        return {}, {}
    
    up_files = {}
    down_files = {}
    
    #  up 
    for up_file in migrations_dir.glob('*_up.sql'):
        # 001_xxx_up.sql
        match = re.match(r'(\d+)_(.+)_up\.sql', up_file.name)
        if match:
            version = match.group(1)
            name = match.group(2)
            up_files[version] = (name, up_file)
    
    #  down 
    for down_file in migrations_dir.glob('*_down.sql'):
        match = re.match(r'(\d+)_(.+)_down\.sql', down_file.name)
        if match:
            version = match.group(1)
            name = match.group(2)
            down_files[version] = (name, down_file)
    
    return up_files, down_files

def check_paired_migrations(up_files, down_files):
    """"""
    all_versions = set(up_files.keys()) | set(down_files.keys())
    
    if not all_versions:
        print("⚠️  ")
        return True
    
    print(f"📊  {len(all_versions)} \n")
    
    errors = []
    
    for version in sorted(all_versions):
        up_info = up_files.get(version)
        down_info = down_files.get(version)
        
        if up_info and down_info:
            up_name, up_path = up_info
            down_name, down_path = down_info
            
            if up_name == down_name:
                print(f"✓ {version}_{up_name}: up/down ")
            else:
                error = f" {version}  up/down : {up_name} vs {down_name}"
                print(f"❌ {error}")
                errors.append(error)
        elif up_info:
            error = f" {version}  down : {up_info[1]}"
            print(f"❌ {error}")
            errors.append(error)
        else:
            error = f" {version}  up : {down_info[1]}"
            print(f"❌ {error}")
            errors.append(error)
    
    return len(errors) == 0, errors

def check_migration_syntax():
    """"""
    #  SQL 
    return True

def main():
    print("🔍 ...\n")
    
    up_files, down_files = find_migrations()
    is_paired, errors = check_paired_migrations(up_files, down_files)
    
    print("\n" + "="*50)
    
    if is_paired:
        print("✅ ")
        sys.exit(0)
    else:
        print("❌ ")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

if __name__ == '__main__':
    main()

