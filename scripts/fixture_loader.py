#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fixtures - Phase 7

:
1. agent.mdtest_data
2. minimal/standard/full
3. 
4. SQL.sql
5. 

:
  python scripts/fixture_loader.py --module <module_name> --fixture <scenario>
  python scripts/fixture_loader.py --module <module_name> --cleanup
  python scripts/fixture_loader.py --list-modules
  python scripts/fixture_loader.py --module <module_name> --list-fixtures

:
  python scripts/fixture_loader.py --module example --fixture minimal
  python scripts/fixture_loader.py --module example --cleanup
"""

import os
import sys
import argparse
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
try:
    import psycopg2
    from psycopg2 import sql
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

# ANSI
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'


def find_repo_root() -> Path:
    """"""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / 'agent.md').exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


def get_db_config(repo_root: Path, env: str = None) -> Optional[Dict]:
    """
    
    
    :
    1.  DATABASE_URL
    2.  DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
    3. config/
    
    Args:
        repo_root: 
        env: dev/test/prodAPP_ENV
    
    Returns:
        None
    """
    # 
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        # DATABASE_URLpostgresql://user:pass@host:port/dbname
        try:
            import re
            match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', db_url)
            if match:
                return {
                    'host': match.group(3),
                    'port': int(match.group(4)),
                    'database': match.group(5),
                    'user': match.group(1),
                    'password': match.group(2)
                }
        except:
            pass
    
    # 
    if all(os.getenv(key) for key in ['DB_HOST', 'DB_NAME', 'DB_USER']):
        return {
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD', '')
        }
    
    # db
    env = env or os.getenv('APP_ENV', 'dev')
    config_file = repo_root / 'config' / f'{env}.yaml'
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                db_config = config.get('database', {}).get('postgres', {})
                if db_config.get('host'):
                    return {
                        'host': db_config.get('host'),
                        'port': db_config.get('port', 5432),
                        'database': db_config.get('database'),
                        'user': db_config.get('user'),
                        'password': db_config.get('password', '')
                    }
        except Exception as e:
            print(f"{YELLOW}⚠{RESET}  : {e}")
    
    return None


def connect_to_db(db_config: Dict):
    """PostgreSQL"""
    if not HAS_PSYCOPG2:
        raise ImportError(" psycopg2: pip install psycopg2-binary")
    
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        return conn
    except Exception as e:
        raise ConnectionError(f": {e}")


def parse_agent_yaml(agent_file: Path) -> Optional[Dict]:
    """agent.mdYAML Front Matter"""
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # YAML Front Matter---
        yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not yaml_match:
            return None
        
        yaml_content = yaml_match.group(1)
        return yaml.safe_load(yaml_content)
    except Exception as e:
        print(f"{RED}✗{RESET} agent.md: {e}")
        return None


def find_module_path(repo_root: Path, module_name: str) -> Optional[Path]:
    """modules/doc/modules/"""
    # modules/
    module_path = repo_root / 'modules' / module_name
    if module_path.exists() and (module_path / 'agent.md').exists():
        return module_path
    
    # doc/modules/
    doc_module_path = repo_root / 'doc' / 'modules' / module_name
    if doc_module_path.exists() and (doc_module_path / 'agent.md').exists():
        return doc_module_path
    
    return None


def list_available_modules(repo_root: Path) -> List[Tuple[str, str, bool]]:
    """, , test_data"""
    modules = []
    
    # modules/
    modules_dir = repo_root / 'modules'
    if modules_dir.exists():
        for module_path in modules_dir.iterdir():
            if module_path.is_dir() and (module_path / 'agent.md').exists():
                agent_data = parse_agent_yaml(module_path / 'agent.md')
                has_test_data = bool(agent_data and agent_data.get('test_data', {}).get('enabled'))
                modules.append((module_path.name, str(module_path), has_test_data))
    
    # doc/modules/
    doc_modules_dir = repo_root / 'doc' / 'modules'
    if doc_modules_dir.exists():
        for module_path in doc_modules_dir.iterdir():
            if module_path.is_dir() and (module_path / 'agent.md').exists():
                agent_data = parse_agent_yaml(module_path / 'agent.md')
                has_test_data = bool(agent_data and agent_data.get('test_data', {}).get('enabled'))
                modules.append((module_path.name, str(module_path), has_test_data))
    
    return modules


def list_fixtures(module_path: Path) -> List[str]:
    """Fixtures"""
    fixtures_dir = module_path / 'fixtures'
    if not fixtures_dir.exists():
        return []
    
    fixtures = []
    for file in fixtures_dir.iterdir():
        if file.suffix == '.sql' and file.stem not in ['README']:
            fixtures.append(file.stem)
    
    return sorted(fixtures)


def read_test_data_md(module_path: Path) -> Optional[Dict]:
    """TEST_DATA.mdFixtures"""
    test_data_file = module_path / 'doc' / 'TEST_DATA.md'
    if not test_data_file.exists():
        return None
    
    try:
        with open(test_data_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 
        fixtures_info = {}
        
        # Fixtures
        table_match = re.search(r'\|  \|  \|.*?\n\|[-| ]+\|\n(.*?)(?:\n\n|\Z)', content, re.DOTALL)
        if table_match:
            table_rows = table_match.group(1).strip().split('\n')
            for row in table_rows:
                parts = [p.strip() for p in row.split('|') if p.strip()]
                if len(parts) >= 2:
                    scenario = parts[0]
                    file_path = parts[1]
                    fixtures_info[scenario] = {'file': file_path}
        
        return fixtures_info
    except Exception as e:
        print(f"{YELLOW}⚠{RESET}  TEST_DATA.md: {e}")
        return None


def load_fixture_sql(sql_file: Path, dry_run: bool = False, db_config: Dict = None) -> Tuple[bool, int]:
    """
    SQL
    
    Args:
        sql_file: SQL
        dry_run: dry-run
        db_config: 
    
    Returns:
        (, )
    """
    if not sql_file.exists():
        print(f"{RED}✗{RESET} SQL: {sql_file}")
        return False, 0
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # SQL
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        stmt_count = len(statements)
        
        if dry_run:
            print(f"{BLUE}ℹ{RESET}  [DRY-RUN]  {stmt_count} SQL:")
            for i, stmt in enumerate(statements[:5], 1):  # 5
                first_line = stmt.split('\n')[0]
                print(f"         {i}. {first_line[:60]}...")
            if stmt_count > 5:
                print(f"         ...  {stmt_count - 5} ")
            print(f"{BLUE}ℹ{RESET}  [DRY-RUN] SQL: {sql_file}")
            
            if not db_config:
                print(f"\n{YELLOW}⚠{RESET}  ")
                print(f"     1:  DATABASE_URL")
                print(f"     2:  DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
                print(f"     3: config/<env>.yaml  database.postgres ")
            
            return True, stmt_count
        
        # SQL
        if not db_config:
            print(f"{RED}✗{RESET} ")
            print(f"{BLUE}ℹ{RESET}   --dry-run ")
            print(f"     : psql -f {sql_file}")
            return False, 0
        
        if not HAS_PSYCOPG2:
            print(f"{RED}✗{RESET}  psycopg2")
            print(f"{BLUE}ℹ{RESET}  : pip install psycopg2-binary")
            return False, 0
        
        print(f"{BLUE}ℹ{RESET}  ...")
        print(f"     : {db_config['host']}:{db_config['port']}")
        print(f"     : {db_config['database']}")
        print(f"     : {db_config['user']}")
        
        conn = connect_to_db(db_config)
        conn.autocommit = False  # 
        cursor = conn.cursor()
        
        print(f"\n{BLUE}ℹ{RESET}   {stmt_count} SQL...\n")
        
        executed_count = 0
        for i, stmt in enumerate(statements, 1):
            try:
                first_line = stmt.split('\n')[0]
                print(f"     [{i}/{stmt_count}] {first_line[:50]}...", end=' ')
                
                cursor.execute(stmt)
                executed_count += 1
                
                print(f"{GREEN}✓{RESET}")
                
            except Exception as e:
                print(f"{RED}✗{RESET}")
                print(f"\n{RED}✗{RESET} SQL: {e}")
                print(f"{YELLOW}⚠{RESET}  ...")
                conn.rollback()
                cursor.close()
                conn.close()
                return False, executed_count
        
        # 
        print(f"\n{BLUE}ℹ{RESET}  ...")
        conn.commit()
        print(f"{GREEN}✓{RESET}  {executed_count} ")
        
        cursor.close()
        conn.close()
        
        return True, stmt_count
        
    except Exception as e:
        print(f"{RED}✗{RESET} SQL: {e}")
        return False, 0


def cleanup_fixtures(module_path: Path, module_name: str, dry_run: bool = False) -> bool:
    """
    
    
    TEST_DATA.mdDELETE
    """
    test_data_file = module_path / 'doc' / 'TEST_DATA.md'
    if not test_data_file.exists():
        print(f"{YELLOW}⚠{RESET}  TEST_DATA.md")
        return False
    
    if dry_run:
        print(f"{BLUE}ℹ{RESET}  [DRY-RUN]  {module_name} ")
        print(f"{BLUE}ℹ{RESET}  [DRY-RUN] : DELETE FROM <table_name>;")
        return True
    
    # TODO: 
    print(f"{YELLOW}⚠{RESET}  ")
    print(f"     : TEST_DATA.mdDELETE")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Fixtures - ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
:
  # 
  python scripts/fixture_loader.py --list-modules
  
  # Fixtures
  python scripts/fixture_loader.py --module example --list-fixtures
  
  # Fixturesdry-run
  python scripts/fixture_loader.py --module example --fixture minimal --dry-run
  
  # Fixtures
  python scripts/fixture_loader.py --module example --fixture minimal
  
  # 
  python scripts/fixture_loader.py --module example --cleanup
        """
    )
    
    parser.add_argument('--module', type=str, help='')
    parser.add_argument('--fixture', type=str, help='Fixtureminimal/standard/full')
    parser.add_argument('--cleanup', action='store_true', help='')
    parser.add_argument('--list-modules', action='store_true', help='')
    parser.add_argument('--list-fixtures', action='store_true', help='Fixtures')
    parser.add_argument('--dry-run', action='store_true', help='Dry-run')
    
    args = parser.parse_args()
    
    repo_root = find_repo_root()
    
    # 
    if args.list_modules:
        print(f"\n{BLUE}{RESET}\n")
        modules = list_available_modules(repo_root)
        if not modules:
            print(f"{YELLOW}⚠{RESET}  ")
            return 0
        
        for name, path, has_test_data in modules:
            status = f"{GREEN}✓{RESET}" if has_test_data else f"{YELLOW}✗{RESET}"
            print(f"  {status} {name}")
            print(f"      : {path}")
            if has_test_data:
                print(f"      : ")
            else:
                print(f"      : ")
            print()
        
        return 0
    
    # 
    if not args.module:
        print(f"{RED}✗{RESET}  --module ")
        print(f": python scripts/fixture_loader.py --module <module_name> [--fixture <scenario>|--cleanup|--list-fixtures]")
        print(f": python scripts/fixture_loader.py --list-modules")
        return 1
    
    # 
    module_path = find_module_path(repo_root, args.module)
    if not module_path:
        print(f"{RED}✗{RESET}  '{args.module}'")
        print(f"{BLUE}ℹ{RESET}   --list-modules ")
        return 1
    
    # agent.md
    agent_data = parse_agent_yaml(module_path / 'agent.md')
    if not agent_data:
        print(f"{RED}✗{RESET} agent.md")
        return 1
    
    # test_data
    test_data_config = agent_data.get('test_data', {})
    if not test_data_config.get('enabled'):
        print(f"{YELLOW}⚠{RESET}   '{args.module}' test_data")
        print(f"{BLUE}ℹ{RESET}  agent.md test_data.enabled: true")
    
    # Fixtures
    if args.list_fixtures:
        print(f"\n{BLUE} '{args.module}' Fixtures{RESET}\n")
        fixtures = list_fixtures(module_path)
        if not fixtures:
            print(f"{YELLOW}⚠{RESET}  Fixturesfixtures/*.sql")
            return 0
        
        # TEST_DATA.md
        test_data_info = read_test_data_md(module_path)
        
        for fixture in fixtures:
            print(f"  • {GREEN}{fixture}{RESET}")
            sql_file = module_path / 'fixtures' / f'{fixture}.sql'
            if sql_file.exists():
                print(f"      : {sql_file.relative_to(repo_root)}")
                # 
                try:
                    with open(sql_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        stmt_count = len([s for s in content.split(';') if s.strip()])
                        print(f"      : {stmt_count}")
                except:
                    pass
                
                # TEST_DATA.md
                if test_data_info and fixture in test_data_info:
                    print(f"      : {test_data_info[fixture].get('description', 'N/A')}")
            print()
        
        return 0
    
    # 
    if args.cleanup:
        print(f"\n{BLUE} '{args.module}' ...{RESET}\n")
        success = cleanup_fixtures(module_path, args.module, dry_run=args.dry_run)
        if success:
            print(f"\n{GREEN}✓{RESET} ")
        else:
            print(f"\n{RED}✗{RESET} ")
        return 0 if success else 1
    
    # Fixtures
    if not args.fixture:
        print(f"{RED}✗{RESET}  --fixture ")
        print(f": python scripts/fixture_loader.py --module {args.module} --fixture <scenario>")
        print(f": python scripts/fixture_loader.py --module {args.module} --list-fixtures")
        return 1
    
    # Fixture
    sql_file = module_path / 'fixtures' / f'{args.fixture}.sql'
    if not sql_file.exists():
        print(f"{RED}✗{RESET} Fixture: {sql_file}")
        print(f"{BLUE}ℹ{RESET}   --list-fixtures Fixtures")
        return 1
    
    # dry-run
    db_config = None
    if not args.dry_run:
        print(f"{BLUE}ℹ{RESET}  ...")
        db_config = get_db_config(repo_root)
        if db_config:
            print(f"{GREEN}✓{RESET} ")
        else:
            print(f"{YELLOW}⚠{RESET}  dry-run")
            print(f"{BLUE}ℹ{RESET}  ")
            print(f"     1.  DATABASE_URL")
            print(f"     2.  DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
            print(f"     3. config/<env>.yaml  database.postgres ")
            args.dry_run = True  # dry-run
    
    # Fixture
    print(f"\n{BLUE}Fixture '{args.fixture}'  '{args.module}'...{RESET}\n")
    print(f": {module_path.relative_to(repo_root)}")
    print(f"SQL: {sql_file.relative_to(repo_root)}")
    print()
    
    if args.dry_run:
        print(f"{YELLOW}⚠{RESET}  DRY-RUN\n")
    
    success, stmt_count = load_fixture_sql(sql_file, dry_run=args.dry_run, db_config=db_config)
    
    if success:
        print(f"\n{GREEN}✓{RESET} Fixture{stmt_count} ")
        return 0
    else:
        print(f"\n{RED}✗{RESET} Fixture")
        return 1


if __name__ == '__main__':
    sys.exit(main())

