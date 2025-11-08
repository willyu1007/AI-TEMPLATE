#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock生命周期管理工具 - Phase 8.5+实现

功能:
1. 查看活跃的Mock数据
2. 清理过期的Mock数据
3. 查看Mock统计信息
4. 手动清理指定Mock数据

用法:
  python scripts/mock_lifecycle.py --list
  python scripts/mock_lifecycle.py --cleanup
  python scripts/mock_lifecycle.py --stats
  python scripts/mock_lifecycle.py --delete <id>

示例:
  python scripts/mock_lifecycle.py --list
  python scripts/mock_lifecycle.py --cleanup --dry-run
  python scripts/mock_lifecycle.py --stats --module example
"""

import os
import sys
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# 数据库连接（可选依赖）
try:
    import psycopg2
    from psycopg2 import sql
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

# ANSI颜色
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RESET = '\033[0m'
BOLD = '\033[1m'


def find_repo_root() -> Path:
    """查找仓库根目录"""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / 'agent.md').exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


def get_db_config(repo_root: Path, env: str = None) -> Optional[Dict]:
    """获取数据库配置"""
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


def list_mock_records(conn, module_filter: Optional[str] = None) -> List[Dict]:
    """
    列出活跃的Mock记录
    
    Args:
        conn: 数据库连接
        module_filter: 模块名称过滤（可选）
    
    Returns:
        Mock记录列表
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
        print(f"{RED}✗ 查询失败: {e}{RESET}")
        return []


def cleanup_expired_mocks(conn, dry_run: bool = False) -> int:
    """
    清理过期的Mock数据
    
    Args:
        conn: 数据库连接
        dry_run: 是否仅模拟运行
    
    Returns:
        清理的记录数
    """
    # 查找过期记录
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
            
            print(f"\n{CYAN}发现 {len(expired_records)} 个过期Mock记录:{RESET}")
            for i, (rec_id, module, table, count, expires) in enumerate(expired_records, 1):
                print(f"  {i}. {module}.{table} - {count}条记录（过期于: {expires}）")
            
            if dry_run:
                print(f"\n{YELLOW}⚠ Dry-run模式，不实际清理{RESET}")
                return len(expired_records)
            
            # 标记为已清理
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
        print(f"{RED}✗ 清理失败: {e}{RESET}")
        return 0


def get_mock_stats(conn, module_filter: Optional[str] = None) -> Dict:
    """
    获取Mock统计信息
    
    Returns:
        统计信息字典
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
        print(f"{RED}✗ 统计失败: {e}{RESET}")
        return {}


def delete_mock_record(conn, record_id: str, dry_run: bool = False) -> bool:
    """
    手动删除Mock记录
    
    Args:
        conn: 数据库连接
        record_id: 记录ID
        dry_run: 是否仅模拟运行
    
    Returns:
        是否成功
    """
    # 查询记录信息
    query = "SELECT module_name, table_name, record_count FROM _mock_lifecycle WHERE id = %s AND status = 'active'"
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, (record_id,))
            record = cur.fetchone()
            
            if not record:
                print(f"{RED}✗ 未找到ID为 {record_id} 的活跃Mock记录{RESET}")
                return False
            
            module, table, count = record
            print(f"\n{CYAN}准备删除Mock记录:{RESET}")
            print(f"  模块: {module}")
            print(f"  表: {table}")
            print(f"  记录数: {count}")
            
            if dry_run:
                print(f"\n{YELLOW}⚠ Dry-run模式，不实际删除{RESET}")
                return True
            
            # 标记为已删除
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
        print(f"{RED}✗ 删除失败: {e}{RESET}")
        return False


def print_table_header():
    """打印表格头部"""
    print(f"\n{BOLD}{'ID':<8} {'模块':<15} {'表':<15} {'记录数':<8} {'类型':<12} {'创建时间':<20} {'过期时间':<20}{RESET}")
    print("-" * 108)


def print_record_row(record: Dict):
    """打印记录行"""
    rec_id = str(record['id'])[:8]
    module = record['module_name'][:14]
    table = record['table_name'][:14]
    count = str(record['record_count'])
    lifecycle = record['lifecycle_type']
    created = record['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    expires = record['expires_at'].strftime('%Y-%m-%d %H:%M:%S') if record['expires_at'] else '永久'
    
    # 根据过期状态着色
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
        description='Mock生命周期管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/mock_lifecycle.py --list
  python scripts/mock_lifecycle.py --list --module example
  python scripts/mock_lifecycle.py --cleanup
  python scripts/mock_lifecycle.py --cleanup --dry-run
  python scripts/mock_lifecycle.py --stats
  python scripts/mock_lifecycle.py --delete <id>
        """
    )
    
    parser.add_argument('--list', action='store_true', help='列出活跃的Mock记录')
    parser.add_argument('--cleanup', action='store_true', help='清理过期的Mock记录')
    parser.add_argument('--stats', action='store_true', help='显示Mock统计信息')
    parser.add_argument('--delete', metavar='ID', help='删除指定ID的Mock记录')
    parser.add_argument('--module', help='按模块过滤')
    parser.add_argument('--dry-run', action='store_true', help='Dry-run模式（不实际执行）')
    
    args = parser.parse_args()
    
    # 至少需要一个操作
    if not any([args.list, args.cleanup, args.stats, args.delete]):
        parser.print_help()
        sys.exit(1)
    
    # 检查依赖
    if not HAS_PSYCOPG2:
        print(f"{RED}✗ 缺少psycopg2库。请运行: pip install psycopg2-binary{RESET}")
        sys.exit(1)
    
    # 查找repo根目录
    repo_root = find_repo_root()
    print(f"{BLUE}📦 仓库根目录: {repo_root}{RESET}")
    
    # 获取数据库配置
    print(f"{CYAN}🔌 连接数据库...{RESET}")
    db_config = get_db_config(repo_root)
    
    if not db_config:
        print(f"{RED}✗ 未配置数据库连接{RESET}")
        print(f"{YELLOW}💡 设置环境变量: DATABASE_URL 或 DB_HOST, DB_NAME, DB_USER, DB_PASSWORD{RESET}")
        sys.exit(1)
    
    # 连接数据库
    conn = connect_to_db(db_config)
    if not conn:
        sys.exit(1)
    
    print(f"{GREEN}✓ 数据库连接成功{RESET}")
    
    try:
        # 执行操作
        if args.list:
            print(f"\n{CYAN}📋 活跃的Mock记录:{RESET}")
            records = list_mock_records(conn, args.module)
            
            if not records:
                print(f"{YELLOW}  （无记录）{RESET}")
            else:
                print_table_header()
                for record in records:
                    print_record_row(record)
                print(f"\n{GREEN}总计: {len(records)} 条记录{RESET}")
        
        if args.cleanup:
            print(f"\n{CYAN}🧹 清理过期Mock记录...{RESET}")
            cleaned = cleanup_expired_mocks(conn, args.dry_run)
            
            if cleaned > 0:
                print(f"\n{GREEN}✓ 清理了 {cleaned} 条过期记录{RESET}")
            else:
                print(f"\n{GREEN}✓ 没有过期记录需要清理{RESET}")
        
        if args.stats:
            print(f"\n{CYAN}📊 Mock统计信息:{RESET}")
            stats = get_mock_stats(conn, args.module)
            
            if stats:
                print(f"\n{BOLD}总体统计:{RESET}")
                print(f"  总记录数: {stats['total_records']}")
                print(f"  总数据行数: {stats['total_rows']:,}")
                print(f"  活跃记录: {GREEN}{stats['active_records']}{RESET}")
                print(f"  已清理记录: {YELLOW}{stats['cleaned_records']}{RESET}")
                
                print(f"\n{BOLD}按生命周期类型:{RESET}")
                print(f"  Ephemeral (1小时): {stats['ephemeral_count']}")
                print(f"  Temporary (7天): {stats['temporary_count']}")
                print(f"  Persistent (永久): {stats['persistent_count']}")
        
        if args.delete:
            print(f"\n{CYAN}🗑️  删除Mock记录...{RESET}")
            success = delete_mock_record(conn, args.delete, args.dry_run)
            
            if success:
                print(f"\n{GREEN}✓ Mock记录已删除{RESET}")
            else:
                sys.exit(1)
    
    finally:
        conn.close()


if __name__ == '__main__':
    main()

