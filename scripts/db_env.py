#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库环境管理工具 - Phase 8.5实现

功能:
1. 识别当前数据库环境
2. 显示环境信息和连接参数
3. 验证数据库连接
4. 支持多环境（dev/test/prod）

用法:
  python scripts/db_env.py                    # 显示当前环境
  python scripts/db_env.py --env dev          # 显示指定环境
  python scripts/db_env.py --test-connection  # 测试连接
  python scripts/db_env.py --show-all         # 显示所有环境配置

示例:
  python scripts/db_env.py
  python scripts/db_env.py --env test --test-connection
"""

import os
import sys
import argparse
import yaml
from pathlib import Path
from typing import Dict, Optional

# 可选的数据库连接库
try:
    import psycopg2
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


def get_db_config_from_env(env_name: str = None) -> Optional[Dict]:
    """
    从环境变量获取数据库配置
    
    优先级:
    1. DATABASE_URL
    2. DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
    
    Args:
        env_name: 环境名称（可选）
    
    Returns:
        数据库配置字典或None
    """
    # 从DATABASE_URL获取
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        import re
        match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', db_url)
        if match:
            return {
                'host': match.group(3),
                'port': int(match.group(4)),
                'database': match.group(5),
                'user': match.group(1),
                'password': match.group(2),
                'source': 'DATABASE_URL'
            }
    
    # 从独立环境变量获取
    if all(os.getenv(key) for key in ['DB_HOST', 'DB_NAME', 'DB_USER']):
        return {
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD', ''),
            'source': '环境变量'
        }
    
    return None


def get_db_config_from_file(repo_root: Path, env_name: str) -> Optional[Dict]:
    """
    从配置文件获取数据库配置
    
    Args:
        repo_root: 仓库根目录
        env_name: 环境名称（dev/test/prod等）
    
    Returns:
        数据库配置字典或None
    """
    config_file = repo_root / 'config' / f'{env_name}.yaml'
    
    if not config_file.exists():
        return None
    
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
                    'password': db_config.get('password', ''),
                    'source': f'config/{env_name}.yaml'
                }
    except Exception as e:
        print(f"{RED}✗{RESET} 读取配置文件失败: {e}")
    
    return None


def test_db_connection(db_config: Dict) -> bool:
    """
    测试数据库连接
    
    Args:
        db_config: 数据库配置
    
    Returns:
        连接是否成功
    """
    if not HAS_PSYCOPG2:
        print(f"{YELLOW}⚠{RESET}  未安装 psycopg2，无法测试连接")
        print(f"{BLUE}ℹ{RESET}  运行: pip install psycopg2-binary")
        return False
    
    try:
        print(f"{BLUE}ℹ{RESET}  测试连接中...")
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            connect_timeout=5
        )
        
        # 执行简单查询
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"{GREEN}✓{RESET} 连接成功！")
        print(f"{CYAN}数据库版本:{RESET} {version[:80]}...")
        return True
        
    except Exception as e:
        print(f"{RED}✗{RESET} 连接失败: {e}")
        return False


def display_config(env_name: str, db_config: Dict, hide_password: bool = True):
    """
    显示数据库配置信息
    
    Args:
        env_name: 环境名称
        db_config: 数据库配置
        hide_password: 是否隐藏密码
    """
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{CYAN}数据库环境信息 - {env_name.upper()}{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")
    
    print(f"  {BLUE}配置来源:{RESET} {db_config.get('source', '未知')}")
    print(f"  {BLUE}主机:{RESET}     {db_config['host']}")
    print(f"  {BLUE}端口:{RESET}     {db_config['port']}")
    print(f"  {BLUE}数据库:{RESET}   {db_config['database']}")
    print(f"  {BLUE}用户:{RESET}     {db_config['user']}")
    
    if hide_password:
        print(f"  {BLUE}密码:{RESET}     {'*' * 8} (已隐藏)")
    else:
        print(f"  {BLUE}密码:{RESET}     {db_config['password']}")
    
    print(f"\n{CYAN}连接字符串:{RESET}")
    masked_password = '***' if hide_password else db_config['password']
    print(f"  postgresql://{db_config['user']}:{masked_password}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='数据库环境管理工具 - 查看和测试数据库连接',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 显示当前环境
  python scripts/db_env.py
  
  # 显示指定环境
  python scripts/db_env.py --env test
  
  # 测试数据库连接
  python scripts/db_env.py --test-connection
  
  # 显示所有环境配置
  python scripts/db_env.py --show-all
  
  # 显示密码（不推荐）
  python scripts/db_env.py --show-password
        """
    )
    
    parser.add_argument('--env', type=str, help='环境名称（dev/test/prod等）')
    parser.add_argument('--test-connection', '-t', action='store_true', help='测试数据库连接')
    parser.add_argument('--show-all', action='store_true', help='显示所有环境配置')
    parser.add_argument('--show-password', action='store_true', help='显示密码（默认隐藏）')
    
    args = parser.parse_args()
    
    # 查找仓库根目录
    repo_root = find_repo_root()
    
    # 确定环境名称
    env_name = args.env or os.getenv('APP_ENV', 'dev')
    
    # 显示所有环境
    if args.show_all:
        print(f"\n{CYAN}所有环境配置:{RESET}\n")
        
        for env in ['dev', 'test', 'staging', 'prod']:
            db_config = get_db_config_from_file(repo_root, env)
            if db_config:
                print(f"  {GREEN}✓{RESET} {env.upper()}: {db_config['host']}:{db_config['port']}/{db_config['database']}")
            else:
                print(f"  {YELLOW}⚠{RESET} {env.upper()}: 未配置")
        
        print()
        return 0
    
    # 获取数据库配置
    print(f"{BLUE}ℹ{RESET}  当前环境: {CYAN}{env_name.upper()}{RESET}\n")
    
    # 优先从环境变量获取
    db_config = get_db_config_from_env()
    
    # 从配置文件获取
    if not db_config:
        db_config = get_db_config_from_file(repo_root, env_name)
    
    if not db_config:
        print(f"{RED}✗{RESET} 错误：未找到数据库配置")
        print(f"\n{BLUE}ℹ{RESET}  配置数据库连接的方式：")
        print(f"  1. 环境变量 DATABASE_URL")
        print(f"  2. 环境变量 DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
        print(f"  3. config/{env_name}.yaml 中的 database.postgres 配置")
        print()
        return 1
    
    # 显示配置
    display_config(env_name, db_config, hide_password=not args.show_password)
    
    # 测试连接
    if args.test_connection:
        success = test_db_connection(db_config)
        return 0 if success else 1
    
    print(f"{BLUE}ℹ{RESET}  提示: 使用 --test-connection 测试连接\n")
    return 0


if __name__ == '__main__':
    sys.exit(main())

