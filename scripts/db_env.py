#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 - Phase 8.5

:
1. 
2. 
3. 
4. dev/test/prod

:
  python scripts/db_env.py                    # 
  python scripts/db_env.py --env dev          # 
  python scripts/db_env.py --test-connection  # 
  python scripts/db_env.py --show-all         # 

:
  python scripts/db_env.py
  python scripts/db_env.py --env test --test-connection
"""

import os
import sys
import argparse
import yaml
from pathlib import Path
from typing import Dict, Optional

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
try:
    import psycopg2
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
        if (current / 'agent.md').exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


def get_db_config_from_env(env_name: str = None) -> Optional[Dict]:
    """
    
    
    :
    1. DATABASE_URL
    2. DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
    
    Args:
        env_name: 
    
    Returns:
        None
    """
    # DATABASE_URL
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
    
    # 
    if all(os.getenv(key) for key in ['DB_HOST', 'DB_NAME', 'DB_USER']):
        return {
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD', ''),
            'source': ''
        }
    
    return None


def get_db_config_from_file(repo_root: Path, env_name: str) -> Optional[Dict]:
    """
    
    
    Args:
        repo_root: 
        env_name: dev/test/prod
    
    Returns:
        None
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
        print(f"{RED}✗{RESET} : {e}")
    
    return None


def test_db_connection(db_config: Dict) -> bool:
    """
    
    
    Args:
        db_config: 
    
    Returns:
        
    """
    if not HAS_PSYCOPG2:
        print(f"{YELLOW}⚠{RESET}   psycopg2")
        print(f"{BLUE}ℹ{RESET}  : pip install psycopg2-binary")
        return False
    
    try:
        print(f"{BLUE}ℹ{RESET}  ...")
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            connect_timeout=5
        )
        
        # 
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"{GREEN}✓{RESET} ")
        print(f"{CYAN}:{RESET} {version[:80]}...")
        return True
        
    except Exception as e:
        print(f"{RED}✗{RESET} : {e}")
        return False


def display_config(env_name: str, db_config: Dict, hide_password: bool = True):
    """
    
    
    Args:
        env_name: 
        db_config: 
        hide_password: 
    """
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{CYAN} - {env_name.upper()}{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")
    
    print(f"  {BLUE}:{RESET} {db_config.get('source', '')}")
    print(f"  {BLUE}:{RESET}     {db_config['host']}")
    print(f"  {BLUE}:{RESET}     {db_config['port']}")
    print(f"  {BLUE}:{RESET}   {db_config['database']}")
    print(f"  {BLUE}:{RESET}     {db_config['user']}")
    
    if hide_password:
        print(f"  {BLUE}:{RESET}     {'*' * 8} ()")
    else:
        print(f"  {BLUE}:{RESET}     {db_config['password']}")
    
    print(f"\n{CYAN}:{RESET}")
    masked_password = '***' if hide_password else db_config['password']
    print(f"  postgresql://{db_config['user']}:{masked_password}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description=' - ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
:
  # 
  python scripts/db_env.py
  
  # 
  python scripts/db_env.py --env test
  
  # 
  python scripts/db_env.py --test-connection
  
  # 
  python scripts/db_env.py --show-all
  
  # 
  python scripts/db_env.py --show-password
        """
    )
    
    parser.add_argument('--env', type=str, help='dev/test/prod')
    parser.add_argument('--test-connection', '-t', action='store_true', help='')
    parser.add_argument('--show-all', action='store_true', help='')
    parser.add_argument('--show-password', action='store_true', help='')
    
    args = parser.parse_args()
    
    # 
    repo_root = find_repo_root()
    
    # 
    env_name = args.env or os.getenv('APP_ENV', 'dev')
    
    # 
    if args.show_all:
        print(f"\n{CYAN}:{RESET}\n")
        
        for env in ['dev', 'test', 'staging', 'prod']:
            db_config = get_db_config_from_file(repo_root, env)
            if db_config:
                print(f"  {GREEN}✓{RESET} {env.upper()}: {db_config['host']}:{db_config['port']}/{db_config['database']}")
            else:
                print(f"  {YELLOW}⚠{RESET} {env.upper()}: ")
        
        print()
        return 0
    
    # 
    print(f"{BLUE}ℹ{RESET}  : {CYAN}{env_name.upper()}{RESET}\n")
    
    # 
    db_config = get_db_config_from_env()
    
    # 
    if not db_config:
        db_config = get_db_config_from_file(repo_root, env_name)
    
    if not db_config:
        print(f"{RED}✗{RESET} ")
        print(f"\n{BLUE}ℹ{RESET}  ")
        print(f"  1.  DATABASE_URL")
        print(f"  2.  DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
        print(f"  3. config/{env_name}.yaml  database.postgres ")
        print()
        return 1
    
    # 
    display_config(env_name, db_config, hide_password=not args.show_password)
    
    # 
    if args.test_connection:
        success = test_db_connection(db_config)
        return 0 if success else 1
    
    print(f"{BLUE}ℹ{RESET}  :  --test-connection \n")
    return 0


if __name__ == '__main__':
    sys.exit(main())

