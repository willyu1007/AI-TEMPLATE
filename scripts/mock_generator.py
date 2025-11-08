#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock数据生成器 - Phase 8.5+实现

功能:
1. 从TEST_DATA.md读取Mock生成规则
2. 从表YAML读取字段定义和约束
3. 使用Faker生成符合规则的随机数据
4. 批量插入数据库
5. 注册到Mock生命周期管理

用法:
  python scripts/mock_generator.py --module <module_name> --table <table_name> --count <num>
  python scripts/mock_generator.py --module <module_name> --table <table_name> --count <num> --lifecycle <type>
  python scripts/mock_generator.py --module <module_name> --table <table_name> --count <num> --dry-run

示例:
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
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import uuid

# Faker库（可选依赖）
try:
    from faker import Faker
    HAS_FAKER = True
except ImportError:
    HAS_FAKER = False
    print("警告: 未安装Faker库。运行 'pip install faker' 来启用Mock数据生成。")

# 数据库连接（可选依赖）
try:
    import psycopg2
    from psycopg2 import sql
    from psycopg2.extras import execute_batch
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

# ANSI颜色
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'


def find_repo_root() -> Path:
    """查找仓库根目录"""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / 'agent.md').exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


def parse_yaml_frontmatter(content: str) -> Tuple[Optional[Dict], str]:
    """解析YAML Front Matter"""
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
    """读取模块的agent.md"""
    module_path = repo_root / 'modules' / module_name / 'agent.md'
    if not module_path.exists():
        module_path = repo_root / 'doc' / 'modules' / module_name / 'agent.md'
    
    if not module_path.exists():
        return None
    
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        yaml_data, _ = parse_yaml_frontmatter(content)
        return yaml_data
    except Exception as e:
        print(f"{RED}✗ 读取agent.md失败: {e}{RESET}")
        return None


def read_test_data_md(repo_root: Path, module_name: str) -> Optional[Dict]:
    """
    读取TEST_DATA.md，提取Mock规则
    
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
        
        # 查找Mock规则的YAML代码块
        mock_rules = {}
        in_yaml_block = False
        yaml_lines = []
        current_table = None
        
        for line in content.split('\n'):
            # 查找YAML代码块
            if line.strip().startswith('```yaml'):
                in_yaml_block = True
                yaml_lines = []
                continue
            elif line.strip() == '```' and in_yaml_block:
                in_yaml_block = False
                # 解析YAML
                try:
                    yaml_content = '\n'.join(yaml_lines)
                    rule_data = yaml.safe_load(yaml_content)
                    
                    # 检查是否是Mock规则（包含table和columns）
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
        print(f"{RED}✗ 读取TEST_DATA.md失败: {e}{RESET}")
        return None


def read_table_yaml(repo_root: Path, table_name: str) -> Optional[Dict]:
    """读取表结构YAML"""
    table_yaml_path = repo_root / 'db' / 'engines' / 'postgres' / 'schemas' / 'tables' / f'{table_name}.yaml'
    
    if not table_yaml_path.exists():
        return None
    
    try:
        with open(table_yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"{RED}✗ 读取表YAML失败: {e}{RESET}")
        return None


def generate_value(faker: Any, column_def: Dict, table_def: Optional[Dict] = None) -> Any:
    """
    根据列定义生成值
    
    Args:
        faker: Faker实例
        column_def: Mock规则中的列定义
        table_def: 表YAML中的列定义（用于约束检查）
    
    Returns:
        生成的值
    """
    col_type = column_def.get('type', 'string')
    generator = column_def.get('generator', None)
    
    # 特殊生成器
    if generator == 'uuid4':
        return str(uuid.uuid4())
    
    # Faker生成器
    if generator and generator.startswith('faker.'):
        faker_method = generator.replace('faker.', '')
        try:
            faker_func = getattr(faker, faker_method)
            params = column_def.get('params', {})
            
            # 特殊参数处理
            if faker_method == 'sentence':
                nb_words = column_def.get('nb_words', column_def.get('max_words', 10))
                return faker_func(nb_words=nb_words)
            elif faker_method == 'random_int':
                min_val = column_def.get('min', params.get('min', 0))
                max_val = column_def.get('max', params.get('max', 100))
                return faker_func(min=min_val, max=max_val)
            elif faker_method == 'date_time_between':
                start_date = column_def.get('start_date', params.get('start_date', '-30d'))
                end_date = column_def.get('end_date', params.get('end_date', 'now'))
                return faker_func(start_date=start_date, end_date=end_date)
            else:
                return faker_func(**params)
        except AttributeError:
            print(f"{YELLOW}⚠ Faker不支持方法: {faker_method}，使用默认值{RESET}")
    
    # Enum/Choice生成器
    if generator == 'choice' or col_type == 'enum':
        choices = column_def.get('choices', column_def.get('values', []))
        weights = column_def.get('weights', None)
        
        if choices:
            if weights:
                import random
                return random.choices(choices, weights=weights, k=1)[0]
            else:
                return faker.random_element(elements=choices)
    
    # 固定值
    if 'value' in column_def:
        return column_def['value']
    
    # 根据类型生成默认值
    if col_type == 'string' or col_type == 'text':
        max_length = column_def.get('max_length', 50)
        return faker.text(max_nb_chars=max_length)
    elif col_type == 'integer' or col_type == 'int':
        min_val = column_def.get('min', 0)
        max_val = column_def.get('max', 1000)
        return faker.random_int(min=min_val, max=max_val)
    elif col_type == 'float' or col_type == 'decimal':
        return round(faker.random.uniform(0, 1000), 2)
    elif col_type == 'boolean' or col_type == 'bool':
        return faker.boolean()
    elif col_type == 'uuid':
        return str(uuid.uuid4())
    elif col_type == 'datetime' or col_type == 'timestamp':
        return faker.date_time_between(start_date='-30d', end_date='now')
    elif col_type == 'date':
        return faker.date_between(start_date='-30d', end_date='today')
    elif col_type == 'json' or col_type == 'jsonb':
        return json.dumps({'key': faker.word(), 'value': faker.word()})
    else:
        return faker.word()


def generate_mock_data(
    faker: Any,
    mock_rule: Dict,
    table_yaml: Optional[Dict],
    count: int
) -> List[Dict]:
    """
    生成Mock数据
    
    Args:
        faker: Faker实例
        mock_rule: TEST_DATA.md中的Mock规则
        table_yaml: 表结构YAML
        count: 生成数量
    
    Returns:
        生成的数据列表
    """
    records = []
    columns = mock_rule.get('columns', {})
    
    # 获取表的列定义（用于类型检查）
    table_columns = {}
    if table_yaml and 'table' in table_yaml:
        table_columns = {
            col['name']: col 
            for col in table_yaml['table'].get('columns', [])
        }
    
    for i in range(count):
        record = {}
        for col_name, col_def in columns.items():
            # 跳过自动生成的列（如created_at如果有default）
            if col_name in table_columns:
                table_col = table_columns[col_name]
                if table_col.get('default') and col_name in ['created_at', 'updated_at', 'id']:
                    continue  # 跳过有默认值的列
            
            record[col_name] = generate_value(faker, col_def, table_columns.get(col_name))
        
        records.append(record)
    
    return records


def get_db_config(repo_root: Path, env: str = None) -> Optional[Dict]:
    """获取数据库配置（从fixture_loader.py复用）"""
    # 从环境变量获取
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
    
    # 从独立环境变量获取
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
    """连接数据库"""
    if not HAS_PSYCOPG2:
        print(f"{RED}✗ 未安装psycopg2库。运行 'pip install psycopg2-binary' 来启用数据库连接。{RESET}")
        return None
    
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        print(f"{RED}✗ 数据库连接失败: {e}{RESET}")
        return None


def insert_mock_data(
    conn,
    table_name: str,
    records: List[Dict],
    batch_size: int = 100
) -> int:
    """
    批量插入Mock数据
    
    Returns:
        成功插入的记录数
    """
    if not records:
        return 0
    
    # 获取列名
    columns = list(records[0].keys())
    
    # 构建INSERT语句
    insert_query = sql.SQL(
        "INSERT INTO {table} ({fields}) VALUES ({placeholders})"
    ).format(
        table=sql.Identifier(table_name),
        fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
        placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )
    
    try:
        with conn.cursor() as cur:
            # 准备数据
            data = [tuple(record[col] for col in columns) for record in records]
            
            # 批量插入
            execute_batch(cur, insert_query, data, page_size=batch_size)
            conn.commit()
            
            return len(records)
    except Exception as e:
        conn.rollback()
        print(f"{RED}✗ 插入数据失败: {e}{RESET}")
        return 0


def register_mock_lifecycle(
    conn,
    module_name: str,
    table_name: str,
    count: int,
    lifecycle_type: str = 'temporary'
) -> bool:
    """
    注册Mock生命周期记录
    
    Args:
        conn: 数据库连接
        module_name: 模块名称
        table_name: 表名
        count: 记录数
        lifecycle_type: 生命周期类型（ephemeral/temporary/persistent/fixture）
    
    Returns:
        是否成功
    """
    # 计算TTL
    ttl_map = {
        'ephemeral': timedelta(hours=1),
        'temporary': timedelta(days=7),
        'persistent': None,
        'fixture': None
    }
    
    ttl = ttl_map.get(lifecycle_type, timedelta(days=7))
    expires_at = datetime.now() + ttl if ttl else None
    
    # 确保_mock_lifecycle表存在
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
        print(f"{YELLOW}⚠ 注册Mock生命周期失败: {e}{RESET}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Mock数据生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/mock_generator.py --module example --table runs --count 1000
  python scripts/mock_generator.py --module example --table runs --count 100 --lifecycle ephemeral
  python scripts/mock_generator.py --module example --table runs --count 50 --dry-run
        """
    )
    
    parser.add_argument('--module', required=True, help='模块名称')
    parser.add_argument('--table', required=True, help='表名')
    parser.add_argument('--count', type=int, required=True, help='生成记录数')
    parser.add_argument('--lifecycle', 
                        choices=['ephemeral', 'temporary', 'persistent', 'fixture'],
                        default='temporary',
                        help='生命周期类型（默认: temporary，7天）')
    parser.add_argument('--dry-run', action='store_true', help='Dry-run模式（不实际插入）')
    parser.add_argument('--seed', type=int, help='随机种子（用于可重复生成）')
    
    args = parser.parse_args()
    
    # 检查依赖
    if not HAS_FAKER:
        print(f"{RED}✗ 缺少Faker库。请运行: pip install faker{RESET}")
        sys.exit(1)
    
    # 查找repo根目录
    repo_root = find_repo_root()
    print(f"{BLUE}📦 仓库根目录: {repo_root}{RESET}\n")
    
    # 初始化Faker
    faker = Faker('zh_CN')  # 支持中文
    if args.seed:
        Faker.seed(args.seed)
        print(f"{CYAN}🎲 使用随机种子: {args.seed}{RESET}")
    
    # 读取模块信息
    print(f"{CYAN}📖 读取模块信息: {args.module}{RESET}")
    agent_data = read_module_agent_md(repo_root, args.module)
    
    # 读取Mock规则
    print(f"{CYAN}📖 读取Mock规则: TEST_DATA.md{RESET}")
    mock_rules = read_test_data_md(repo_root, args.module)
    
    if not mock_rules or args.table not in mock_rules:
        print(f"{RED}✗ 未找到表 '{args.table}' 的Mock规则{RESET}")
        print(f"{YELLOW}💡 请在TEST_DATA.md中定义Mock规则{RESET}")
        sys.exit(1)
    
    mock_rule = mock_rules[args.table]
    print(f"{GREEN}✓ 找到Mock规则{RESET}")
    
    # 读取表结构
    print(f"{CYAN}📖 读取表结构: {args.table}.yaml{RESET}")
    table_yaml = read_table_yaml(repo_root, args.table)
    
    if table_yaml:
        print(f"{GREEN}✓ 找到表结构定义{RESET}")
    else:
        print(f"{YELLOW}⚠ 未找到表结构YAML，使用Mock规则定义{RESET}")
    
    # 生成Mock数据
    print(f"\n{CYAN}🎲 生成Mock数据...{RESET}")
    records = generate_mock_data(faker, mock_rule, table_yaml, args.count)
    print(f"{GREEN}✓ 生成 {len(records)} 条记录{RESET}")
    
    # 显示示例
    if records:
        print(f"\n{CYAN}📝 数据示例（前3条）:{RESET}")
        for i, record in enumerate(records[:3], 1):
            print(f"  {i}. {record}")
    
    # Dry-run模式
    if args.dry_run:
        print(f"\n{YELLOW}⚠ Dry-run模式，不实际插入数据{RESET}")
        print(f"{GREEN}✓ Mock数据生成成功！{RESET}")
        return
    
    # 获取数据库配置
    print(f"\n{CYAN}🔌 连接数据库...{RESET}")
    db_config = get_db_config(repo_root)
    
    if not db_config:
        print(f"{YELLOW}⚠ 未配置数据库连接{RESET}")
        print(f"{YELLOW}💡 设置环境变量: DATABASE_URL 或 DB_HOST, DB_NAME, DB_USER, DB_PASSWORD{RESET}")
        print(f"{GREEN}✓ Mock数据生成成功（dry-run）{RESET}")
        return
    
    if not HAS_PSYCOPG2:
        print(f"{YELLOW}⚠ 未安装psycopg2库{RESET}")
        print(f"{YELLOW}💡 运行: pip install psycopg2-binary{RESET}")
        print(f"{GREEN}✓ Mock数据生成成功（dry-run）{RESET}")
        return
    
    # 连接数据库
    conn = connect_to_db(db_config)
    if not conn:
        print(f"{YELLOW}⚠ 数据库连接失败，仅生成数据（dry-run）{RESET}")
        print(f"{GREEN}✓ Mock数据生成成功（dry-run）{RESET}")
        return
    
    print(f"{GREEN}✓ 数据库连接成功{RESET}")
    
    try:
        # 插入数据
        print(f"\n{CYAN}💾 插入Mock数据...{RESET}")
        inserted = insert_mock_data(conn, args.table, records)
        print(f"{GREEN}✓ 成功插入 {inserted} 条记录{RESET}")
        
        # 注册生命周期
        print(f"\n{CYAN}📝 注册Mock生命周期...{RESET}")
        registered = register_mock_lifecycle(
            conn, 
            args.module, 
            args.table, 
            inserted, 
            args.lifecycle
        )
        if registered:
            print(f"{GREEN}✓ 生命周期注册成功（类型: {args.lifecycle}）{RESET}")
            
            # 显示过期时间
            if args.lifecycle == 'ephemeral':
                print(f"  {CYAN}⏰ 将在1小时后过期{RESET}")
            elif args.lifecycle == 'temporary':
                print(f"  {CYAN}⏰ 将在7天后过期{RESET}")
            elif args.lifecycle == 'persistent':
                print(f"  {CYAN}♾️  持久保留（需手动清理）{RESET}")
        
        print(f"\n{GREEN}✅ Mock数据生成完成！{RESET}")
        
    finally:
        conn.close()


if __name__ == '__main__':
    main()

