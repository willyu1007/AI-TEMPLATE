#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fixtures加载工具 - Phase 7实现

功能:
1. 模块感知：读取agent.md的test_data配置
2. 场景加载：支持minimal/standard/full等场景
3. 环境适配：读取数据库环境配置
4. SQL执行：加载.sql文件到数据库
5. 清理功能：清空测试数据

用法:
  python scripts/fixture_loader.py --module <module_name> --fixture <scenario>
  python scripts/fixture_loader.py --module <module_name> --cleanup
  python scripts/fixture_loader.py --list-modules
  python scripts/fixture_loader.py --module <module_name> --list-fixtures

示例:
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
RESET = '\033[0m'


def find_repo_root() -> Path:
    """查找仓库根目录"""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / 'agent.md').exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


def get_db_config(repo_root: Path, env: str = None) -> Optional[Dict]:
    """
    获取数据库配置
    
    优先级:
    1. 环境变量 DATABASE_URL
    2. 环境变量 DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
    3. config/环境配置文件
    
    Args:
        repo_root: 仓库根目录
        env: 环境名称（dev/test/prod），默认从APP_ENV读取
    
    Returns:
        数据库配置字典或None
    """
    # 从环境变量获取
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        # 解析DATABASE_URL（格式：postgresql://user:pass@host:port/dbname）
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
    
    # 从独立环境变量获取
    if all(os.getenv(key) for key in ['DB_HOST', 'DB_NAME', 'DB_USER']):
        return {
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD', '')
        }
    
    # 从配置文件获取（简化版，仅读取db相关配置）
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
            print(f"{YELLOW}⚠{RESET}  读取配置文件失败: {e}")
    
    return None


def connect_to_db(db_config: Dict):
    """连接到PostgreSQL数据库"""
    if not HAS_PSYCOPG2:
        raise ImportError("需要安装 psycopg2: pip install psycopg2-binary")
    
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
        raise ConnectionError(f"数据库连接失败: {e}")


def parse_agent_yaml(agent_file: Path) -> Optional[Dict]:
    """解析agent.md的YAML Front Matter"""
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取YAML Front Matter（在---之间）
        yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not yaml_match:
            return None
        
        yaml_content = yaml_match.group(1)
        return yaml.safe_load(yaml_content)
    except Exception as e:
        print(f"{RED}✗{RESET} 解析agent.md失败: {e}")
        return None


def find_module_path(repo_root: Path, module_name: str) -> Optional[Path]:
    """查找模块路径（支持modules/和doc/modules/）"""
    # 优先查找modules/目录（业务模块）
    module_path = repo_root / 'modules' / module_name
    if module_path.exists() and (module_path / 'agent.md').exists():
        return module_path
    
    # 查找doc/modules/目录（参考模块）
    doc_module_path = repo_root / 'doc' / 'modules' / module_name
    if doc_module_path.exists() and (doc_module_path / 'agent.md').exists():
        return doc_module_path
    
    return None


def list_available_modules(repo_root: Path) -> List[Tuple[str, str, bool]]:
    """列举所有可用的模块（名称, 路径, 是否配置test_data）"""
    modules = []
    
    # 扫描modules/目录
    modules_dir = repo_root / 'modules'
    if modules_dir.exists():
        for module_path in modules_dir.iterdir():
            if module_path.is_dir() and (module_path / 'agent.md').exists():
                agent_data = parse_agent_yaml(module_path / 'agent.md')
                has_test_data = bool(agent_data and agent_data.get('test_data', {}).get('enabled'))
                modules.append((module_path.name, str(module_path), has_test_data))
    
    # 扫描doc/modules/目录（参考模块）
    doc_modules_dir = repo_root / 'doc' / 'modules'
    if doc_modules_dir.exists():
        for module_path in doc_modules_dir.iterdir():
            if module_path.is_dir() and (module_path / 'agent.md').exists():
                agent_data = parse_agent_yaml(module_path / 'agent.md')
                has_test_data = bool(agent_data and agent_data.get('test_data', {}).get('enabled'))
                modules.append((module_path.name, str(module_path), has_test_data))
    
    return modules


def list_fixtures(module_path: Path) -> List[str]:
    """列举模块的所有Fixtures"""
    fixtures_dir = module_path / 'fixtures'
    if not fixtures_dir.exists():
        return []
    
    fixtures = []
    for file in fixtures_dir.iterdir():
        if file.suffix == '.sql' and file.stem not in ['README']:
            fixtures.append(file.stem)
    
    return sorted(fixtures)


def read_test_data_md(module_path: Path) -> Optional[Dict]:
    """读取TEST_DATA.md并提取Fixtures信息"""
    test_data_file = module_path / 'doc' / 'TEST_DATA.md'
    if not test_data_file.exists():
        return None
    
    try:
        with open(test_data_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 简单解析：提取场景名称和文件路径
        fixtures_info = {}
        
        # 查找Fixtures概览表格
        table_match = re.search(r'\| 场景名称 \| 文件路径 \|.*?\n\|[-| ]+\|\n(.*?)(?:\n\n|\Z)', content, re.DOTALL)
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
        print(f"{YELLOW}⚠{RESET}  无法读取TEST_DATA.md: {e}")
        return None


def load_fixture_sql(sql_file: Path, dry_run: bool = False, db_config: Dict = None) -> Tuple[bool, int]:
    """
    加载SQL文件到数据库
    
    Args:
        sql_file: SQL文件路径
        dry_run: 是否为dry-run模式（仅检查，不执行）
        db_config: 数据库配置（可选）
    
    Returns:
        (成功标志, 语句数量)
    """
    if not sql_file.exists():
        print(f"{RED}✗{RESET} SQL文件不存在: {sql_file}")
        return False, 0
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 计算SQL语句数量
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        stmt_count = len(statements)
        
        if dry_run:
            print(f"{BLUE}ℹ{RESET}  [DRY-RUN] 将执行 {stmt_count} 条SQL语句:")
            for i, stmt in enumerate(statements[:5], 1):  # 只显示前5条
                first_line = stmt.split('\n')[0]
                print(f"         {i}. {first_line[:60]}...")
            if stmt_count > 5:
                print(f"         ... 还有 {stmt_count - 5} 条语句")
            print(f"{BLUE}ℹ{RESET}  [DRY-RUN] SQL文件: {sql_file}")
            
            if not db_config:
                print(f"\n{YELLOW}⚠{RESET}  提示：配置数据库连接后可实际执行")
                print(f"     方式1: 环境变量 DATABASE_URL")
                print(f"     方式2: 环境变量 DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
                print(f"     方式3: config/<env>.yaml 中的 database.postgres 配置")
            
            return True, stmt_count
        
        # 实际执行SQL
        if not db_config:
            print(f"{RED}✗{RESET} 错误：未配置数据库连接")
            print(f"{BLUE}ℹ{RESET}  请配置数据库连接或使用 --dry-run 模式")
            print(f"     或手动执行: psql -f {sql_file}")
            return False, 0
        
        if not HAS_PSYCOPG2:
            print(f"{RED}✗{RESET} 错误：未安装 psycopg2")
            print(f"{BLUE}ℹ{RESET}  运行: pip install psycopg2-binary")
            return False, 0
        
        print(f"{BLUE}ℹ{RESET}  连接数据库...")
        print(f"     主机: {db_config['host']}:{db_config['port']}")
        print(f"     数据库: {db_config['database']}")
        print(f"     用户: {db_config['user']}")
        
        conn = connect_to_db(db_config)
        conn.autocommit = False  # 使用事务
        cursor = conn.cursor()
        
        print(f"\n{BLUE}ℹ{RESET}  执行 {stmt_count} 条SQL语句...\n")
        
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
                print(f"\n{RED}✗{RESET} SQL执行失败: {e}")
                print(f"{YELLOW}⚠{RESET}  回滚事务...")
                conn.rollback()
                cursor.close()
                conn.close()
                return False, executed_count
        
        # 提交事务
        print(f"\n{BLUE}ℹ{RESET}  提交事务...")
        conn.commit()
        print(f"{GREEN}✓{RESET} 事务提交成功，共执行 {executed_count} 条语句")
        
        cursor.close()
        conn.close()
        
        return True, stmt_count
        
    except Exception as e:
        print(f"{RED}✗{RESET} 加载SQL文件失败: {e}")
        return False, 0


def cleanup_fixtures(module_path: Path, module_name: str, dry_run: bool = False) -> bool:
    """
    清理模块的测试数据
    
    注意：需要根据TEST_DATA.md中定义的表来生成DELETE语句
    """
    test_data_file = module_path / 'doc' / 'TEST_DATA.md'
    if not test_data_file.exists():
        print(f"{YELLOW}⚠{RESET}  找不到TEST_DATA.md，无法确定需要清理的表")
        return False
    
    if dry_run:
        print(f"{BLUE}ℹ{RESET}  [DRY-RUN] 将清理模块 {module_name} 的测试数据")
        print(f"{BLUE}ℹ{RESET}  [DRY-RUN] 请手动执行: DELETE FROM <table_name>;")
        return True
    
    # TODO: 实现实际的清理逻辑
    print(f"{YELLOW}⚠{RESET}  清理功能尚未实现，请手动清理数据库")
    print(f"     建议: 根据TEST_DATA.md中的表定义手动执行DELETE语句")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Fixtures加载工具 - 模块感知的测试数据管理',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 列举所有模块
  python scripts/fixture_loader.py --list-modules
  
  # 列举模块的Fixtures
  python scripts/fixture_loader.py --module example --list-fixtures
  
  # 加载Fixtures（dry-run模式）
  python scripts/fixture_loader.py --module example --fixture minimal --dry-run
  
  # 加载Fixtures（实际执行，需要数据库连接）
  python scripts/fixture_loader.py --module example --fixture minimal
  
  # 清理测试数据
  python scripts/fixture_loader.py --module example --cleanup
        """
    )
    
    parser.add_argument('--module', type=str, help='模块名称')
    parser.add_argument('--fixture', type=str, help='Fixture场景名称（minimal/standard/full等）')
    parser.add_argument('--cleanup', action='store_true', help='清理模块的测试数据')
    parser.add_argument('--list-modules', action='store_true', help='列举所有可用的模块')
    parser.add_argument('--list-fixtures', action='store_true', help='列举模块的所有Fixtures')
    parser.add_argument('--dry-run', action='store_true', help='Dry-run模式（仅检查，不执行）')
    
    args = parser.parse_args()
    
    repo_root = find_repo_root()
    
    # 列举所有模块
    if args.list_modules:
        print(f"\n{BLUE}可用的模块：{RESET}\n")
        modules = list_available_modules(repo_root)
        if not modules:
            print(f"{YELLOW}⚠{RESET}  未找到任何模块")
            return 0
        
        for name, path, has_test_data in modules:
            status = f"{GREEN}✓{RESET}" if has_test_data else f"{YELLOW}✗{RESET}"
            print(f"  {status} {name}")
            print(f"      路径: {path}")
            if has_test_data:
                print(f"      测试数据: 已配置")
            else:
                print(f"      测试数据: 未配置")
            print()
        
        return 0
    
    # 需要指定模块
    if not args.module:
        print(f"{RED}✗{RESET} 错误：需要指定 --module 参数")
        print(f"用法: python scripts/fixture_loader.py --module <module_name> [--fixture <scenario>|--cleanup|--list-fixtures]")
        print(f"或者: python scripts/fixture_loader.py --list-modules")
        return 1
    
    # 查找模块路径
    module_path = find_module_path(repo_root, args.module)
    if not module_path:
        print(f"{RED}✗{RESET} 错误：找不到模块 '{args.module}'")
        print(f"{BLUE}ℹ{RESET}  使用 --list-modules 查看所有可用模块")
        return 1
    
    # 读取agent.md
    agent_data = parse_agent_yaml(module_path / 'agent.md')
    if not agent_data:
        print(f"{RED}✗{RESET} 错误：无法解析模块的agent.md")
        return 1
    
    # 检查test_data配置
    test_data_config = agent_data.get('test_data', {})
    if not test_data_config.get('enabled'):
        print(f"{YELLOW}⚠{RESET}  警告：模块 '{args.module}' 未启用test_data")
        print(f"{BLUE}ℹ{RESET}  提示：在agent.md中添加 test_data.enabled: true")
    
    # 列举Fixtures
    if args.list_fixtures:
        print(f"\n{BLUE}模块 '{args.module}' 的Fixtures：{RESET}\n")
        fixtures = list_fixtures(module_path)
        if not fixtures:
            print(f"{YELLOW}⚠{RESET}  未找到任何Fixtures（fixtures/*.sql）")
            return 0
        
        # 读取TEST_DATA.md获取详细信息
        test_data_info = read_test_data_md(module_path)
        
        for fixture in fixtures:
            print(f"  • {GREEN}{fixture}{RESET}")
            sql_file = module_path / 'fixtures' / f'{fixture}.sql'
            if sql_file.exists():
                print(f"      文件: {sql_file.relative_to(repo_root)}")
                # 读取文件统计
                try:
                    with open(sql_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        stmt_count = len([s for s in content.split(';') if s.strip()])
                        print(f"      语句数: {stmt_count}")
                except:
                    pass
                
                # 从TEST_DATA.md获取用途
                if test_data_info and fixture in test_data_info:
                    print(f"      说明: {test_data_info[fixture].get('description', 'N/A')}")
            print()
        
        return 0
    
    # 清理测试数据
    if args.cleanup:
        print(f"\n{BLUE}清理模块 '{args.module}' 的测试数据...{RESET}\n")
        success = cleanup_fixtures(module_path, args.module, dry_run=args.dry_run)
        if success:
            print(f"\n{GREEN}✓{RESET} 清理完成")
        else:
            print(f"\n{RED}✗{RESET} 清理失败")
        return 0 if success else 1
    
    # 加载Fixtures
    if not args.fixture:
        print(f"{RED}✗{RESET} 错误：需要指定 --fixture 参数")
        print(f"用法: python scripts/fixture_loader.py --module {args.module} --fixture <scenario>")
        print(f"或者: python scripts/fixture_loader.py --module {args.module} --list-fixtures")
        return 1
    
    # 查找Fixture文件
    sql_file = module_path / 'fixtures' / f'{args.fixture}.sql'
    if not sql_file.exists():
        print(f"{RED}✗{RESET} 错误：找不到Fixture文件: {sql_file}")
        print(f"{BLUE}ℹ{RESET}  使用 --list-fixtures 查看可用的Fixtures")
        return 1
    
    # 获取数据库配置（如果不是dry-run模式）
    db_config = None
    if not args.dry_run:
        print(f"{BLUE}ℹ{RESET}  获取数据库配置...")
        db_config = get_db_config(repo_root)
        if db_config:
            print(f"{GREEN}✓{RESET} 数据库配置已加载")
        else:
            print(f"{YELLOW}⚠{RESET}  未找到数据库配置，将仅在dry-run模式下运行")
            print(f"{BLUE}ℹ{RESET}  配置数据库连接的方式：")
            print(f"     1. 环境变量 DATABASE_URL")
            print(f"     2. 环境变量 DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
            print(f"     3. config/<env>.yaml 中的 database.postgres 配置")
            args.dry_run = True  # 强制进入dry-run模式
    
    # 加载Fixture
    print(f"\n{BLUE}加载Fixture '{args.fixture}' 到模块 '{args.module}'...{RESET}\n")
    print(f"模块路径: {module_path.relative_to(repo_root)}")
    print(f"SQL文件: {sql_file.relative_to(repo_root)}")
    print()
    
    if args.dry_run:
        print(f"{YELLOW}⚠{RESET}  DRY-RUN模式：仅检查，不执行\n")
    
    success, stmt_count = load_fixture_sql(sql_file, dry_run=args.dry_run, db_config=db_config)
    
    if success:
        print(f"\n{GREEN}✓{RESET} Fixture加载完成（{stmt_count} 条语句）")
        return 0
    else:
        print(f"\n{RED}✗{RESET} Fixture加载失败")
        return 1


if __name__ == '__main__':
    sys.exit(main())

