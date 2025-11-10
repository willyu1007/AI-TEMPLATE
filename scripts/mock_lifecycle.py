#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock - Phase 8.5+

:
1. Mock
2. Mock
3. Mock
4. Mock

:
  python scripts/mock_lifecycle.py --list
  python scripts/mock_lifecycle.py --cleanup
  python scripts/mock_lifecycle.py --stats
  python scripts/mock_lifecycle.py --delete <id>

:
  python scripts/mock_lifecycle.py --list
  python scripts/mock_lifecycle.py --cleanup --dry-run
  python scripts/mock_lifecycle.py --stats --module example
"""

import os
import sys
import argparse
import re
from pathlib import Path

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from typing import Dict, List, Optional
from datetime import datetime

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
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RESET = '\033[0m'
BOLD = '\033[1m'


def find_repo_root() -> Path:
    """"""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / 'agent.md').exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


def get_db_config(repo_root: Path, env: str = None) -> Optional[Dict]:
    """"""
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


def list_mock_records(conn, module_filter: Optional[str] = None) -> List[Dict]:
    """
    Mock
    
    Args:
        conn: 
        module_filter: 
    
    Returns:
        Mock
    """
    query = """
    SELECT 
        id,
        module_name,
        table_name,
        record_count,
        lifecycle_type,
        created_at,
        expires_at,
        status
    FROM _mock_lifecycle
    WHERE status = 'active'
    """
    
    params = []
    if module_filter:
        query += " AND module_name = %s"
        params.append(module_filter)
    
    query += " ORDER BY created_at DESC"
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            columns = [desc[0] for desc in cur.description]
            records = []
            for row in cur.fetchall():
                records.append(dict(zip(columns, row)))
            return records
    except Exception as e:
        print(f"{RED}✗ : {e}{RESET}")
        return []


def cleanup_expired_mocks(conn, dry_run: bool = False) -> int:
    """
    Mock
    
    Args:
        conn: 
        dry_run: 
    
    Returns:
        
    """
    # 
    query = """
    SELECT id, module_name, table_name, record_count, expires_at
    FROM _mock_lifecycle
    WHERE status = 'active'
      AND expires_at IS NOT NULL
      AND expires_at < NOW()
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            expired_records = cur.fetchall()
            
            if not expired_records:
                return 0
            
            print(f"\n{CYAN} {len(expired_records)} Mock:{RESET}")
            for i, (rec_id, module, table, count, expires) in enumerate(expired_records, 1):
                print(f"  {i}. {module}.{table} - {count}: {expires}")
            
            if dry_run:
                print(f"\n{YELLOW}⚠ Dry-run{RESET}")
                return len(expired_records)
            
            # 
            update_query = """
            UPDATE _mock_lifecycle
            SET status = 'cleaned', updated_at = NOW()
            WHERE id = ANY(%s)
            """
            
            ids = [rec[0] for rec in expired_records]
            cur.execute(update_query, (ids,))
            conn.commit()
            
            return len(expired_records)
    
    except Exception as e:
        conn.rollback()
        print(f"{RED}✗ : {e}{RESET}")
        return 0


def get_mock_stats(conn, module_filter: Optional[str] = None) -> Dict:
    """
    Mock
    
    Returns:
        
    """
    base_query = """
    SELECT 
        COUNT(*) as total_records,
        SUM(record_count) as total_rows,
        COUNT(CASE WHEN status = 'active' THEN 1 END) as active_records,
        COUNT(CASE WHEN status = 'cleaned' THEN 1 END) as cleaned_records,
        COUNT(CASE WHEN lifecycle_type = 'ephemeral' THEN 1 END) as ephemeral_count,
        COUNT(CASE WHEN lifecycle_type = 'temporary' THEN 1 END) as temporary_count,
        COUNT(CASE WHEN lifecycle_type = 'persistent' THEN 1 END) as persistent_count
    FROM _mock_lifecycle
    """
    
    params = []
    if module_filter:
        base_query += " WHERE module_name = %s"
        params.append(module_filter)
    
    try:
        with conn.cursor() as cur:
            cur.execute(base_query, params)
            row = cur.fetchone()
            
            return {
                'total_records': row[0] or 0,
                'total_rows': row[1] or 0,
                'active_records': row[2] or 0,
                'cleaned_records': row[3] or 0,
                'ephemeral_count': row[4] or 0,
                'temporary_count': row[5] or 0,
                'persistent_count': row[6] or 0
            }
    except Exception as e:
        print(f"{RED}✗ : {e}{RESET}")
        return {}


def delete_mock_record(conn, record_id: str, dry_run: bool = False) -> bool:
    """
    Mock
    
    Args:
        conn: 
        record_id: ID
        dry_run: 
    
    Returns:
        
    """
    # 
    query = "SELECT module_name, table_name, record_count FROM _mock_lifecycle WHERE id = %s AND status = 'active'"
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, (record_id,))
            record = cur.fetchone()
            
            if not record:
                print(f"{RED}✗ ID {record_id} Mock{RESET}")
                return False
            
            module, table, count = record
            print(f"\n{CYAN}Mock:{RESET}")
            print(f"  : {module}")
            print(f"  : {table}")
            print(f"  : {count}")
            
            if dry_run:
                print(f"\n{YELLOW}⚠ Dry-run{RESET}")
                return True
            
            # 
            update_query = """
            UPDATE _mock_lifecycle
            SET status = 'deleted', updated_at = NOW()
            WHERE id = %s
            """
            
            cur.execute(update_query, (record_id,))
            conn.commit()
            
            return True
    
    except Exception as e:
        conn.rollback()
        print(f"{RED}✗ : {e}{RESET}")
        return False


def print_table_header():
    """"""
    print(f"\n{BOLD}{'ID':<8} {'':<15} {'':<15} {'':<8} {'':<12} {'':<20} {'':<20}{RESET}")
    print("-" * 108)


def print_record_row(record: Dict):
    """"""
    rec_id = str(record['id'])[:8]
    module = record['module_name'][:14]
    table = record['table_name'][:14]
    count = str(record['record_count'])
    lifecycle = record['lifecycle_type']
    created = record['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    expires = record['expires_at'].strftime('%Y-%m-%d %H:%M:%S') if record['expires_at'] else ''
    
    # 
    if record['expires_at'] and record['expires_at'] < datetime.now():
        color = RED
    elif record['lifecycle_type'] == 'ephemeral':
        color = YELLOW
    elif record['lifecycle_type'] == 'persistent':
        color = GREEN
    else:
        color = RESET
    
    print(f"{color}{rec_id:<8} {module:<15} {table:<15} {count:<8} {lifecycle:<12} {created:<20} {expires:<20}{RESET}")


def main():
    parser = argparse.ArgumentParser(
        description='Mock',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
:
  python scripts/mock_lifecycle.py --list
  python scripts/mock_lifecycle.py --list --module example
  python scripts/mock_lifecycle.py --cleanup
  python scripts/mock_lifecycle.py --cleanup --dry-run
  python scripts/mock_lifecycle.py --stats
  python scripts/mock_lifecycle.py --delete <id>
        """
    )
    
    parser.add_argument('--list', action='store_true', help='Mock')
    parser.add_argument('--cleanup', action='store_true', help='Mock')
    parser.add_argument('--stats', action='store_true', help='Mock')
    parser.add_argument('--delete', metavar='ID', help='IDMock')
    parser.add_argument('--module', help='')
    parser.add_argument('--dry-run', action='store_true', help='Dry-run')
    
    args = parser.parse_args()
    
    # 
    if not any([args.list, args.cleanup, args.stats, args.delete]):
        parser.print_help()
        sys.exit(1)
    
    # 
    if not HAS_PSYCOPG2:
        print(f"{RED}✗ psycopg2: pip install psycopg2-binary{RESET}")
        sys.exit(1)
    
    # repo
    repo_root = find_repo_root()
    print(f"{BLUE}📦 : {repo_root}{RESET}")
    
    # 
    print(f"{CYAN}🔌 ...{RESET}")
    db_config = get_db_config(repo_root)
    
    if not db_config:
        print(f"{RED}✗ {RESET}")
        print(f"{YELLOW}💡 : DATABASE_URL  DB_HOST, DB_NAME, DB_USER, DB_PASSWORD{RESET}")
        sys.exit(1)
    
    # 
    conn = connect_to_db(db_config)
    if not conn:
        sys.exit(1)
    
    print(f"{GREEN}✓ {RESET}")
    
    try:
        # 
        if args.list:
            print(f"\n{CYAN}📋 Mock:{RESET}")
            records = list_mock_records(conn, args.module)
            
            if not records:
                print(f"{YELLOW}  {RESET}")
            else:
                print_table_header()
                for record in records:
                    print_record_row(record)
                print(f"\n{GREEN}: {len(records)} {RESET}")
        
        if args.cleanup:
            print(f"\n{CYAN}🧹 Mock...{RESET}")
            cleaned = cleanup_expired_mocks(conn, args.dry_run)
            
            if cleaned > 0:
                print(f"\n{GREEN}✓  {cleaned} {RESET}")
            else:
                print(f"\n{GREEN}✓ {RESET}")
        
        if args.stats:
            print(f"\n{CYAN}📊 Mock:{RESET}")
            stats = get_mock_stats(conn, args.module)
            
            if stats:
                print(f"\n{BOLD}:{RESET}")
                print(f"  : {stats['total_records']}")
                print(f"  : {stats['total_rows']:,}")
                print(f"  : {GREEN}{stats['active_records']}{RESET}")
                print(f"  : {YELLOW}{stats['cleaned_records']}{RESET}")
                
                print(f"\n{BOLD}:{RESET}")
                print(f"  Ephemeral (1): {stats['ephemeral_count']}")
                print(f"  Temporary (7): {stats['temporary_count']}")
                print(f"  Persistent (): {stats['persistent_count']}")
        
        if args.delete:
            print(f"\n{CYAN}🗑️  Mock...{RESET}")
            success = delete_mock_record(conn, args.delete, args.dry_run)
            
            if success:
                print(f"\n{GREEN}✓ Mock{RESET}")
            else:
                sys.exit(1)
    
    finally:
        conn.close()


if __name__ == '__main__':
    main()

