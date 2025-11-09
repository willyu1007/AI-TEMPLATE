#!/usr/bin/env python3
"""
迁移脚本检查：验证 up/down 成对存在
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
    """查找所有迁移脚本"""
    migrations_dir = pathlib.Path('migrations')
    
    if not migrations_dir.exists():
        print("⚠️  migrations/ 目录不存在")
        return {}, {}
    
    up_files = {}
    down_files = {}
    
    # 查找 up 脚本
    for up_file in migrations_dir.glob('*_up.sql'):
        # 提取版本号（假设格式：001_xxx_up.sql）
        match = re.match(r'(\d+)_(.+)_up\.sql', up_file.name)
        if match:
            version = match.group(1)
            name = match.group(2)
            up_files[version] = (name, up_file)
    
    # 查找 down 脚本
    for down_file in migrations_dir.glob('*_down.sql'):
        match = re.match(r'(\d+)_(.+)_down\.sql', down_file.name)
        if match:
            version = match.group(1)
            name = match.group(2)
            down_files[version] = (name, down_file)
    
    return up_files, down_files

def check_paired_migrations(up_files, down_files):
    """检查迁移脚本是否成对"""
    all_versions = set(up_files.keys()) | set(down_files.keys())
    
    if not all_versions:
        print("⚠️  未找到迁移脚本")
        return True
    
    print(f"📊 找到 {len(all_versions)} 个迁移版本\n")
    
    errors = []
    
    for version in sorted(all_versions):
        up_info = up_files.get(version)
        down_info = down_files.get(version)
        
        if up_info and down_info:
            up_name, up_path = up_info
            down_name, down_path = down_info
            
            if up_name == down_name:
                print(f"✓ {version}_{up_name}: up/down 成对")
            else:
                error = f"版本 {version} 的 up/down 名称不匹配: {up_name} vs {down_name}"
                print(f"❌ {error}")
                errors.append(error)
        elif up_info:
            error = f"版本 {version} 缺少 down 脚本: {up_info[1]}"
            print(f"❌ {error}")
            errors.append(error)
        else:
            error = f"版本 {version} 缺少 up 脚本: {down_info[1]}"
            print(f"❌ {error}")
            errors.append(error)
    
    return len(errors) == 0, errors

def check_migration_syntax():
    """基础语法检查（可选）"""
    # 可以添加 SQL 语法检查，这里暂时跳过
    return True

def main():
    print("🔍 开始迁移脚本检查...\n")
    
    up_files, down_files = find_migrations()
    is_paired, errors = check_paired_migrations(up_files, down_files)
    
    print("\n" + "="*50)
    
    if is_paired:
        print("✅ 迁移脚本检查通过")
        sys.exit(0)
    else:
        print("❌ 迁移脚本检查失败")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

if __name__ == '__main__':
    main()

