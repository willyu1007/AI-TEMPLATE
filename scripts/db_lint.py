#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
db_lint.py - 


1. up/down
2.  tables/*.yaml 
3.  YAML 
4. 


    python scripts/db_lint.py
    make db_lint
    

    CI- 0
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import List, Tuple, Dict, Set

# WindowsUTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
DB_ROOT = REPO_ROOT / "db" / "engines" / "postgres"
MIGRATIONS_DIR = DB_ROOT / "migrations"
TABLES_DIR = DB_ROOT / "schemas" / "tables"

# 
REQUIRED_META_FIELDS = ["table_name", "description", "migration_version"]
REQUIRED_TABLE_FIELDS = ["name", "columns"]
REQUIRED_COLUMN_FIELDS = ["name", "type", "nullable", "description"]


def print_header(title):
    """"""
    print("=" * 60)
    print(title)
    print("=" * 60)


def check_migrations_pairing() -> Tuple[List[str], List[str]]:
    """
    
    
    Returns:
        (downup, updown)
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
    
    # 
    missing_down = sorted([f"{name}_up.sql" for name in ups - downs])
    missing_up = sorted([f"{name}_down.sql" for name in downs - ups])
    
    return missing_down, missing_up


def check_table_yaml_format(yaml_file: Path) -> List[str]:
    """
     table YAML 
    
    Returns:
        
    """
    issues = []
    
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        issues.append(f"YAML : {e}")
        return issues
    except Exception as e:
        issues.append(f": {e}")
        return issues
    
    if not isinstance(data, dict):
        issues.append("YAML ")
        return issues
    
    #  meta 
    if "meta" not in data:
        issues.append(" 'meta' ")
    else:
        meta = data["meta"]
        for field in REQUIRED_META_FIELDS:
            if field not in meta:
                issues.append(f"meta.{field} ")
        
        #  table_name 
        expected_name = yaml_file.stem
        if "table_name" in meta and meta["table_name"] != expected_name:
            issues.append(
                f"({expected_name}) meta.table_name({meta['table_name']})"
            )
    
    #  table 
    if "table" not in data:
        issues.append(" 'table' ")
    else:
        table = data["table"]
        for field in REQUIRED_TABLE_FIELDS:
            if field not in table:
                issues.append(f"table.{field} ")
        
        #  columns
        if "columns" in table:
            if not isinstance(table["columns"], list):
                issues.append("table.columns ")
            else:
                for idx, col in enumerate(table["columns"]):
                    for field in REQUIRED_COLUMN_FIELDS:
                        if field not in col:
                            issues.append(
                                f"table.columns[{idx}]  '{field}' "
                            )
    
    #  migrations 
    if "migrations" not in data:
        issues.append(" 'migrations' ")
    else:
        migrations = data["migrations"]
        if "up" not in migrations:
            issues.append("migrations.up ")
        if "down" not in migrations:
            issues.append("migrations.down ")
        
        # 
        for key in ["up", "down"]:
            if key in migrations:
                migration_path = migrations[key]
                #  YAML 
                full_path = (yaml_file.parent / migration_path).resolve()
                if not full_path.exists():
                    issues.append(
                        f"migrations.{key} : {migration_path}"
                    )
    
    return issues


def check_all_table_yamls() -> Dict[str, List[str]]:
    """
     table YAML 
    
    Returns:
        {: }
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
    
    
    Returns:
        [(, )]
    """
    issues = []
    
    # 
    if MIGRATIONS_DIR.exists():
        for file in MIGRATIONS_DIR.glob("*.sql"):
            filename = file.name
            # <version>_<description>_up/down.sql
            if not re.match(r'^\d+_[a-z0-9_]+_(up|down)\.sql$', filename):
                issues.append((
                    filename,
                    " <version>_<description>_up/down.sql"
                ))
    
    #  table YAML 
    if TABLES_DIR.exists():
        for file in TABLES_DIR.glob("*.yaml"):
            filename = file.name
            if filename == "README.md":
                continue
            # 
            if not re.match(r'^[a-z0-9_]+\.yaml$', filename):
                issues.append((
                    filename,
                    " my_table.yaml"
                ))
    
    return issues


def main():
    """"""
    print_header("DB Lint")
    
    has_issues = False
    
    # 1. 
    print("\n1. ")
    print("-" * 60)
    
    if not MIGRATIONS_DIR.exists():
        print(f"⚠️  : {MIGRATIONS_DIR}")
        print("   ")
    else:
        missing_down, missing_up = check_migrations_pairing()
        
        if missing_down:
            has_issues = True
            print(f"\n❌  up  down :")
            for script in missing_down:
                print(f"   - {script}")
        
        if missing_up:
            has_issues = True
            print(f"\n❌  down  up :")
            for script in missing_up:
                print(f"   - {script}")
        
        if not missing_down and not missing_up:
            print("✅ ")
    
    # 2.  table YAML 
    print("\n\n2. Table YAML ")
    print("-" * 60)
    
    if not TABLES_DIR.exists():
        print(f"⚠️  : {TABLES_DIR}")
        print("   YAML")
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
                print(f"✅  {yaml_count}  table YAML ")
            else:
                print("⚠️   table YAML ")
    
    # 3. 
    print("\n\n3. ")
    print("-" * 60)
    
    naming_issues = check_naming_conventions()
    
    if naming_issues:
        has_issues = True
        for filename, issue in naming_issues:
            print(f"❌ {filename}")
            print(f"   {issue}")
    else:
        print("✅ ")
    
    # 
    print("\n")
    print_header("")
    
    if has_issues:
        print()
        print("⚠️  CI")
        print()
        print(":")
        print("1. ")
        print("2.  YAML ")
        print("3. ")
        print("4.  'make db_lint' ")
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

