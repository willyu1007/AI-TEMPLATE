#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
db_lint.py - 数据库文件校验工具

功能：
1. 校验迁移脚本成对性（up/down）
2. 校验 tables/*.yaml 格式和必需字段
3. 校验 YAML 与迁移脚本的引用关系
4. 校验文件命名规范

用法：
    python scripts/db_lint.py
    make db_lint
    
模式：
    警告模式（不影响CI）- 发现问题输出警告但退出码为0
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import List, Tuple, Dict, Set

# 设置Windows控制台UTF-8输出
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
DB_ROOT = REPO_ROOT / "db" / "engines" / "postgres"
MIGRATIONS_DIR = DB_ROOT / "migrations"
TABLES_DIR = DB_ROOT / "schemas" / "tables"

# 必需字段定义
REQUIRED_META_FIELDS = ["table_name", "description", "migration_version"]
REQUIRED_TABLE_FIELDS = ["name", "columns"]
REQUIRED_COLUMN_FIELDS = ["name", "type", "nullable", "description"]


def print_header(title):
    """打印标题"""
    print("=" * 60)
    print(title)
    print("=" * 60)


def check_migrations_pairing() -> Tuple[List[str], List[str]]:
    """
    检查迁移脚本的成对性
    
    Returns:
        (缺少down的up脚本列表, 缺少up的down脚本列表)
    """
    if not MIGRATIONS_DIR.exists():
        return [], []
    
    ups = set()
    downs = set()
    
    for file in MIGRATIONS_DIR.glob("*.sql"):
        filename = file.name
        if filename.endswith("_up.sql"):
            base_name = filename.replace("_up.sql", "")
            ups.add(base_name)
        elif filename.endswith("_down.sql"):
            base_name = filename.replace("_down.sql", "")
            downs.add(base_name)
    
    # 找出缺少配对的
    missing_down = sorted([f"{name}_up.sql" for name in ups - downs])
    missing_up = sorted([f"{name}_down.sql" for name in downs - ups])
    
    return missing_down, missing_up


def check_table_yaml_format(yaml_file: Path) -> List[str]:
    """
    检查单个 table YAML 文件的格式
    
    Returns:
        问题列表
    """
    issues = []
    
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        issues.append(f"YAML 格式错误: {e}")
        return issues
    except Exception as e:
        issues.append(f"无法读取文件: {e}")
        return issues
    
    if not isinstance(data, dict):
        issues.append("YAML 根节点必须是字典")
        return issues
    
    # 检查 meta 字段
    if "meta" not in data:
        issues.append("缺少 'meta' 字段")
    else:
        meta = data["meta"]
        for field in REQUIRED_META_FIELDS:
            if field not in meta:
                issues.append(f"meta.{field} 缺失")
        
        # 文件名与 table_name 一致性
        expected_name = yaml_file.stem
        if "table_name" in meta and meta["table_name"] != expected_name:
            issues.append(
                f"文件名({expected_name})与 meta.table_name({meta['table_name']})不一致"
            )
    
    # 检查 table 字段
    if "table" not in data:
        issues.append("缺少 'table' 字段")
    else:
        table = data["table"]
        for field in REQUIRED_TABLE_FIELDS:
            if field not in table:
                issues.append(f"table.{field} 缺失")
        
        # 检查 columns
        if "columns" in table:
            if not isinstance(table["columns"], list):
                issues.append("table.columns 必须是列表")
            else:
                for idx, col in enumerate(table["columns"]):
                    for field in REQUIRED_COLUMN_FIELDS:
                        if field not in col:
                            issues.append(
                                f"table.columns[{idx}] 缺少 '{field}' 字段"
                            )
    
    # 检查 migrations 字段
    if "migrations" not in data:
        issues.append("缺少 'migrations' 字段")
    else:
        migrations = data["migrations"]
        if "up" not in migrations:
            issues.append("migrations.up 缺失")
        if "down" not in migrations:
            issues.append("migrations.down 缺失")
        
        # 检查迁移脚本路径是否存在
        for key in ["up", "down"]:
            if key in migrations:
                migration_path = migrations[key]
                # 相对于 YAML 文件的路径
                full_path = (yaml_file.parent / migration_path).resolve()
                if not full_path.exists():
                    issues.append(
                        f"migrations.{key} 引用的文件不存在: {migration_path}"
                    )
    
    return issues


def check_all_table_yamls() -> Dict[str, List[str]]:
    """
    检查所有 table YAML 文件
    
    Returns:
        {文件名: 问题列表}
    """
    if not TABLES_DIR.exists():
        return {}
    
    results = {}
    
    for yaml_file in TABLES_DIR.glob("*.yaml"):
        if yaml_file.name == "README.md":
            continue
        issues = check_table_yaml_format(yaml_file)
        if issues:
            results[yaml_file.name] = issues
    
    return results


def check_naming_conventions() -> List[Tuple[str, str]]:
    """
    检查文件命名规范
    
    Returns:
        [(文件名, 问题描述)]
    """
    issues = []
    
    # 检查迁移脚本命名
    if MIGRATIONS_DIR.exists():
        for file in MIGRATIONS_DIR.glob("*.sql"):
            filename = file.name
            # 检查格式：<version>_<description>_up/down.sql
            if not re.match(r'^\d+_[a-z0-9_]+_(up|down)\.sql$', filename):
                issues.append((
                    filename,
                    "命名不符合规范：应为 <version>_<description>_up/down.sql"
                ))
    
    # 检查 table YAML 命名
    if TABLES_DIR.exists():
        for file in TABLES_DIR.glob("*.yaml"):
            filename = file.name
            if filename == "README.md":
                continue
            # 应为小写字母和下划线
            if not re.match(r'^[a-z0-9_]+\.yaml$', filename):
                issues.append((
                    filename,
                    "命名不符合规范：应为小写字母和下划线，如 my_table.yaml"
                ))
    
    return issues


def main():
    """主函数"""
    print_header("数据库文件校验（DB Lint）")
    
    has_issues = False
    
    # 1. 检查迁移脚本成对性
    print("\n1. 迁移脚本成对性检查")
    print("-" * 60)
    
    if not MIGRATIONS_DIR.exists():
        print(f"⚠️  迁移目录不存在: {MIGRATIONS_DIR}")
        print("   （如果项目不使用数据库，可以忽略）")
    else:
        missing_down, missing_up = check_migrations_pairing()
        
        if missing_down:
            has_issues = True
            print(f"\n❌ 以下 up 脚本缺少对应的 down 脚本:")
            for script in missing_down:
                print(f"   - {script}")
        
        if missing_up:
            has_issues = True
            print(f"\n❌ 以下 down 脚本缺少对应的 up 脚本:")
            for script in missing_up:
                print(f"   - {script}")
        
        if not missing_down and not missing_up:
            print("✅ 所有迁移脚本都有对应的配对")
    
    # 2. 检查 table YAML 格式
    print("\n\n2. Table YAML 格式检查")
    print("-" * 60)
    
    if not TABLES_DIR.exists():
        print(f"⚠️  表定义目录不存在: {TABLES_DIR}")
        print("   （如果项目不使用表YAML，可以忽略）")
    else:
        yaml_issues = check_all_table_yamls()
        
        if yaml_issues:
            has_issues = True
            for filename, issues in yaml_issues.items():
                print(f"\n❌ {filename}:")
                for issue in issues:
                    print(f"   - {issue}")
        else:
            yaml_count = len(list(TABLES_DIR.glob("*.yaml")))
            if yaml_count > 0:
                print(f"✅ 所有 {yaml_count} 个 table YAML 文件格式正确")
            else:
                print("⚠️  未找到 table YAML 文件")
    
    # 3. 检查命名规范
    print("\n\n3. 文件命名规范检查")
    print("-" * 60)
    
    naming_issues = check_naming_conventions()
    
    if naming_issues:
        has_issues = True
        for filename, issue in naming_issues:
            print(f"❌ {filename}")
            print(f"   {issue}")
    else:
        print("✅ 所有文件命名符合规范")
    
    # 汇总
    print("\n")
    print_header("检查完成")
    
    if has_issues:
        print()
        print("⚠️  发现问题（警告模式，不影响CI）")
        print()
        print("建议:")
        print("1. 补齐缺少配对的迁移脚本")
        print("2. 修复 YAML 格式问题")
        print("3. 检查文件命名规范")
        print("4. 运行 'make db_lint' 再次检查")
        print()
        print("=" * 60)
        print("⚠️  警告模式：允许存在问题")
        print("=" * 60)
        sys.exit(0)  # 警告模式，不退出失败
    else:
        print()
        print("=" * 60)
        print("✅ 所有数据库文件校验通过")
        print("=" * 60)


if __name__ == "__main__":
    main()

