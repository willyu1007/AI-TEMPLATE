#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock - Phase 8.5+

:
1. TEST_DATA.mdMock
2. YAML
3. Faker
4. 
5. Mock

:
  python scripts/mock_generator.py --module <module_name> --table <table_name> --count <num>
  python scripts/mock_generator.py --module <module_name> --table <table_name> --count <num> --lifecycle <type>
  python scripts/mock_generator.py --module <module_name> --table <table_name> --count <num> --dry-run

:
  python scripts/mock_generator.py --module example --table runs --count 1000
  python scripts/mock_generator.py --module example --table runs --count 100 --lifecycle ephemeral
  python scripts/mock_generator.py --module example --table runs --count 50 --dry-run
"""

import os
import sys
import argparse
import yaml
import re
import json
from pathlib import Path

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import uuid

# Faker
try:
    from faker import Faker
    HAS_FAKER = True
except ImportError:
    HAS_FAKER = False
    print(": Faker 'pip install faker' Mock")

# 
try:
    import psycopg2
    from psycopg2 import sql
    from psycopg2.extras import execute_batch
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

# ANSI
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'


def find_repo_root() -> Path:
    """"""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / 'AGENTS.md').exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


def parse_yaml_frontmatter(content: str) -> Tuple[Optional[Dict], str]:
    """YAML Front Matter"""
    lines = content.split('\n')
    if not lines or not lines[0].strip().startswith('---'):
        return None, content
    
    yaml_lines = []
    body_start = 0
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            body_start = i + 1
            break
        yaml_lines.append(line)
    
    if body_start > 0:
        try:
            yaml_data = yaml.safe_load('\n'.join(yaml_lines))
            body = '\n'.join(lines[body_start:])
            return yaml_data, body
        except yaml.YAMLError:
            return None, content
    
    return None, content


def read_module_agent_md(repo_root: Path, module_name: str) -> Optional[Dict]:
    """AGENTS.md"""
    module_path = repo_root / 'modules' / module_name / 'AGENTS.md'
    if not module_path.exists():
        module_path = repo_root / 'doc' / 'modules' / module_name / 'AGENTS.md'
    
    if not module_path.exists():
        return None
    
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        yaml_data, _ = parse_yaml_frontmatter(content)
        return yaml_data
    except Exception as e:
        print(f"{RED}✗ AGENTS.md: {e}{RESET}")
        return None


def read_test_data_md(repo_root: Path, module_name: str) -> Optional[Dict]:
    """
    TEST_DATA.mdMock
    
    Returns:
        Dict: {
            'table_name': {
                'count': 1000,
                'columns': {
                    'column_name': {
                        'type': 'string',
                        'generator': 'faker.sentence',
                        'params': {...}
                    }
                }
            }
        }
    """
    test_data_paths = [
        repo_root / 'modules' / module_name / 'doc' / 'TEST_DATA.md',
        repo_root / 'doc' / 'modules' / module_name / 'doc' / 'TEST_DATA.md'
    ]
    
    test_data_path = None
    for path in test_data_paths:
        if path.exists():
            test_data_path = path
            break
    
    if not test_data_path:
        return None
    
    try:
        with open(test_data_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # MockYAML
        mock_rules = {}
        in_yaml_block = False
        yaml_lines = []
        current_table = None
        
        for line in content.split('\n'):
            # YAML
            if line.strip().startswith('```yaml'):
                in_yaml_block = True
                yaml_lines = []
                continue
            elif line.strip() == '```' and in_yaml_block:
                in_yaml_block = False
                # YAML
                try:
                    yaml_content = '\n'.join(yaml_lines)
                    rule_data = yaml.safe_load(yaml_content)
                    
                    # Mocktablecolumns
                    if isinstance(rule_data, dict) and 'table' in rule_data and 'columns' in rule_data:
                        table_name = rule_data['table']
                        mock_rules[table_name] = rule_data
                except yaml.YAMLError:
                    pass
                continue
            
            if in_yaml_block:
                yaml_lines.append(line)
        
        return mock_rules if mock_rules else None
    
    except Exception as e:
        print(f"{RED}✗ TEST_DATA.md: {e}{RESET}")
        return None


def read_table_yaml(repo_root: Path, table_name: str) -> Optional[Dict]:
    """YAML"""
    table_yaml_path = repo_root / 'db' / 'engines' / 'postgres' / 'schemas' / 'tables' / f'{table_name}.yaml'
    
    if not table_yaml_path.exists():
        return None
    
    try:
        with open(table_yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"{RED}✗ YAML: {e}{RESET}")
        return None


def _generate_uuid() -> str:
    """UUID"""
    return str(uuid.uuid4())


def _generate_faker_value(faker: Any, column_def: Dict, generator: str) -> Any:
    """Faker"""
    faker_method = generator.replace('faker.', '')
    try:
        faker_func = getattr(faker, faker_method)
        params = column_def.get('params', {})
        
        # 
        special_handlers = {
            'sentence': lambda: faker_func(nb_words=column_def.get('nb_words', column_def.get('max_words', 10))),
            'random_int': lambda: faker_func(
                min=column_def.get('min', params.get('min', 0)),
                max=column_def.get('max', params.get('max', 100))
            ),
            'date_time_between': lambda: faker_func(
                start_date=column_def.get('start_date', params.get('start_date', '-30d')),
                end_date=column_def.get('end_date', params.get('end_date', 'now'))
            )
        }
        
        if faker_method in special_handlers:
            return special_handlers[faker_method]()
        else:
            return faker_func(**params)
    except AttributeError:
        print(f"{YELLOW}⚠ Faker: {faker_method}{RESET}")
        return None


def _generate_choice_value(faker: Any, column_def: Dict) -> Any:
    """/"""
    choices = column_def.get('choices', column_def.get('values', []))
    weights = column_def.get('weights', None)
    
    if choices:
        if weights:
            import random
            return random.choices(choices, weights=weights, k=1)[0]
        else:
            return faker.random_element(elements=choices)
    return None


def _generate_default_value_by_type(faker: Any, col_type: str, column_def: Dict) -> Any:
    """"""
    type_generators = {
        'string': lambda: faker.text(max_nb_chars=column_def.get('max_length', 50)),
        'text': lambda: faker.text(max_nb_chars=column_def.get('max_length', 50)),
        'integer': lambda: faker.random_int(
            min=column_def.get('min', 0),
            max=column_def.get('max', 1000)
        ),
        'int': lambda: faker.random_int(
            min=column_def.get('min', 0),
            max=column_def.get('max', 1000)
        ),
        'float': lambda: round(faker.random.uniform(0, 1000), 2),
        'decimal': lambda: round(faker.random.uniform(0, 1000), 2),
        'boolean': lambda: faker.boolean(),
        'bool': lambda: faker.boolean(),
        'uuid': lambda: _generate_uuid(),
        'datetime': lambda: faker.date_time_between(start_date='-30d', end_date='now'),
        'timestamp': lambda: faker.date_time_between(start_date='-30d', end_date='now'),
        'date': lambda: faker.date_between(start_date='-30d', end_date='today'),
        'json': lambda: json.dumps({'key': faker.word(), 'value': faker.word()}),
        'jsonb': lambda: json.dumps({'key': faker.word(), 'value': faker.word()}),
    }
    
    generator = type_generators.get(col_type, lambda: faker.word())
    return generator()


def generate_value(faker: Any, column_def: Dict, table_def: Optional[Dict] = None) -> Any:
    """
    
    
    Args:
        faker: Faker
        column_def: Mock
        table_def: YAML
    
    Returns:
        
    """
    col_type = column_def.get('type', 'string')
    generator = column_def.get('generator', None)
    
    # 
    if 'value' in column_def:
        return column_def['value']
    
    # 
    if generator == 'uuid4':
        return _generate_uuid()
    
    # Faker
    if generator and generator.startswith('faker.'):
        result = _generate_faker_value(faker, column_def, generator)
        if result is not None:
            return result
    
    # Enum/Choice
    if generator == 'choice' or col_type == 'enum':
        result = _generate_choice_value(faker, column_def)
        if result is not None:
            return result
    
    # 
    return _generate_default_value_by_type(faker, col_type, column_def)


def generate_mock_data(
    faker: Any,
    mock_rule: Dict,
    table_yaml: Optional[Dict],
    count: int
) -> List[Dict]:
    """
    Mock
    
    Args:
        faker: Faker
        mock_rule: TEST_DATA.mdMock
        table_yaml: YAML
        count: 
    
    Returns:
        
    """
    records = []
    columns = mock_rule.get('columns', {})
    
    # 
    table_columns = {}
    if table_yaml and 'table' in table_yaml:
        table_columns = {
            col['name']: col 
            for col in table_yaml['table'].get('columns', [])
        }
    
    for i in range(count):
        record = {}
        for col_name, col_def in columns.items():
            # created_atdefault
            if col_name in table_columns:
                table_col = table_columns[col_name]
                if table_col.get('default') and col_name in ['created_at', 'updated_at', 'id']:
                    continue  # 
            
            record[col_name] = generate_value(faker, col_def, table_columns.get(col_name))
        
        records.append(record)
    
    return records


def get_db_config(repo_root: Path, env: str = None) -> Optional[Dict]:
    """fixture_loader.py"""
    # 
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        try:
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
    
    return None


def connect_to_db(db_config: Dict):
    """"""
    if not HAS_PSYCOPG2:
        print(f"{RED}✗ psycopg2 'pip install psycopg2-binary' {RESET}")
        return None
    
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        print(f"{RED}✗ : {e}{RESET}")
        return None


def insert_mock_data(
    conn,
    table_name: str,
    records: List[Dict],
    batch_size: int = 100
) -> int:
    """
    Mock
    
    Returns:
        
    """
    if not records:
        return 0
    
    # 
    columns = list(records[0].keys())
    
    # INSERT
    insert_query = sql.SQL(
        "INSERT INTO {table} ({fields}) VALUES ({placeholders})"
    ).format(
        table=sql.Identifier(table_name),
        fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
        placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )
    
    try:
        with conn.cursor() as cur:
            # 
            data = [tuple(record[col] for col in columns) for record in records]
            
            # 
            execute_batch(cur, insert_query, data, page_size=batch_size)
            conn.commit()
            
            return len(records)
    except Exception as e:
        conn.rollback()
        print(f"{RED}✗ : {e}{RESET}")
        return 0


def register_mock_lifecycle(
    conn,
    module_name: str,
    table_name: str,
    count: int,
    lifecycle_type: str = 'temporary'
) -> bool:
    """
    Mock
    
    Args:
        conn: 
        module_name: 
        table_name: 
        count: 
        lifecycle_type: ephemeral/temporary/persistent/fixture
    
    Returns:
        
    """
    # TTL
    ttl_map = {
        'ephemeral': timedelta(hours=1),
        'temporary': timedelta(days=7),
        'persistent': None,
        'fixture': None
    }
    
    ttl = ttl_map.get(lifecycle_type, timedelta(days=7))
    expires_at = datetime.now() + ttl if ttl else None
    
    # _mock_lifecycle
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS _mock_lifecycle (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        module_name TEXT NOT NULL,
        table_name TEXT NOT NULL,
        record_count INTEGER NOT NULL,
        lifecycle_type TEXT NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        expires_at TIMESTAMPTZ,
        status TEXT NOT NULL DEFAULT 'active'
    );
    """
    
    insert_sql = """
    INSERT INTO _mock_lifecycle (module_name, table_name, record_count, lifecycle_type, expires_at)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(create_table_sql)
            cur.execute(insert_sql, (module_name, table_name, count, lifecycle_type, expires_at))
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        print(f"{YELLOW}⚠ Mock: {e}{RESET}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Mock',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
:
  python scripts/mock_generator.py --module example --table runs --count 1000
  python scripts/mock_generator.py --module example --table runs --count 100 --lifecycle ephemeral
  python scripts/mock_generator.py --module example --table runs --count 50 --dry-run
        """
    )
    
    parser.add_argument('--module', required=True, help='')
    parser.add_argument('--table', required=True, help='')
    parser.add_argument('--count', type=int, required=True, help='')
    parser.add_argument('--lifecycle', 
                        choices=['ephemeral', 'temporary', 'persistent', 'fixture'],
                        default='temporary',
                        help=': temporary7')
    parser.add_argument('--dry-run', action='store_true', help='Dry-run')
    parser.add_argument('--seed', type=int, help='')
    
    args = parser.parse_args()
    
    # 
    if not HAS_FAKER:
        print(f"{RED}✗ Faker: pip install faker{RESET}")
        sys.exit(1)
    
    # repo
    repo_root = find_repo_root()
    print(f"{BLUE}📦 : {repo_root}{RESET}\n")
    
    # Faker
    faker = Faker('zh_CN')  # 
    if args.seed:
        Faker.seed(args.seed)
        print(f"{CYAN}🎲 : {args.seed}{RESET}")
    
    # 
    print(f"{CYAN}📖 : {args.module}{RESET}")
    agent_data = read_module_agent_md(repo_root, args.module)
    
    # Mock
    print(f"{CYAN}📖 Mock: TEST_DATA.md{RESET}")
    mock_rules = read_test_data_md(repo_root, args.module)
    
    if not mock_rules or args.table not in mock_rules:
        print(f"{RED}✗  '{args.table}' Mock{RESET}")
        print(f"{YELLOW}💡 TEST_DATA.mdMock{RESET}")
        sys.exit(1)
    
    mock_rule = mock_rules[args.table]
    print(f"{GREEN}✓ Mock{RESET}")
    
    # 
    print(f"{CYAN}📖 : {args.table}.yaml{RESET}")
    table_yaml = read_table_yaml(repo_root, args.table)
    
    if table_yaml:
        print(f"{GREEN}✓ {RESET}")
    else:
        print(f"{YELLOW}⚠ YAMLMock{RESET}")
    
    # Mock
    print(f"\n{CYAN}🎲 Mock...{RESET}")
    records = generate_mock_data(faker, mock_rule, table_yaml, args.count)
    print(f"{GREEN}✓  {len(records)} {RESET}")
    
    # 
    if records:
        print(f"\n{CYAN}📝 3:{RESET}")
        for i, record in enumerate(records[:3], 1):
            print(f"  {i}. {record}")
    
    # Dry-run
    if args.dry_run:
        print(f"\n{YELLOW}⚠ Dry-run{RESET}")
        print(f"{GREEN}✓ Mock{RESET}")
        return
    
    # 
    print(f"\n{CYAN}🔌 ...{RESET}")
    db_config = get_db_config(repo_root)
    
    if not db_config:
        print(f"{YELLOW}⚠ {RESET}")
        print(f"{YELLOW}💡 : DATABASE_URL  DB_HOST, DB_NAME, DB_USER, DB_PASSWORD{RESET}")
        print(f"{GREEN}✓ Mockdry-run{RESET}")
        return
    
    if not HAS_PSYCOPG2:
        print(f"{YELLOW}⚠ psycopg2{RESET}")
        print(f"{YELLOW}💡 : pip install psycopg2-binary{RESET}")
        print(f"{GREEN}✓ Mockdry-run{RESET}")
        return
    
    # 
    conn = connect_to_db(db_config)
    if not conn:
        print(f"{YELLOW}⚠ dry-run{RESET}")
        print(f"{GREEN}✓ Mockdry-run{RESET}")
        return
    
    print(f"{GREEN}✓ {RESET}")
    
    try:
        # 
        print(f"\n{CYAN}💾 Mock...{RESET}")
        inserted = insert_mock_data(conn, args.table, records)
        print(f"{GREEN}✓  {inserted} {RESET}")
        
        # 
        print(f"\n{CYAN}📝 Mock...{RESET}")
        registered = register_mock_lifecycle(
            conn, 
            args.module, 
            args.table, 
            inserted, 
            args.lifecycle
        )
        if registered:
            print(f"{GREEN}✓ : {args.lifecycle}{RESET}")
            
            # 
            if args.lifecycle == 'ephemeral':
                print(f"  {CYAN}⏰ 1{RESET}")
            elif args.lifecycle == 'temporary':
                print(f"  {CYAN}⏰ 7{RESET}")
            elif args.lifecycle == 'persistent':
                print(f"  {CYAN}♾️  {RESET}")
        
        print(f"\n{GREEN}✅ Mock{RESET}")
        
    finally:
        conn.close()


if __name__ == '__main__':
    main()

