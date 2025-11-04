#!/usr/bin/env python3
"""
运行时配置校验：检查配置结构、必填字段、生产环境密钥
"""
import sys
import os
import yaml
import pathlib

def load_yaml(path):
    """加载 YAML 文件"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ 无法加载 {path}: {e}")
        return None

def check_config_structure():
    """检查配置文件结构"""
    required_files = [
        'config/schema.yaml',
        'config/defaults.yaml'
    ]
    
    print("检查配置文件结构:")
    all_exists = True
    
    for file_path in required_files:
        if pathlib.Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ❌ 缺失: {file_path}")
            all_exists = False
    
    return all_exists

def check_defaults_against_schema():
    """检查 defaults.yaml 是否符合 schema"""
    schema = load_yaml('config/schema.yaml')
    defaults = load_yaml('config/defaults.yaml')
    
    if not schema or not defaults:
        return False
    
    print("\n检查配置与 schema 一致性:")
    
    # 简单检查：schema 中定义的键在 defaults 中是否存在
    # 这里做简化版本的验证
    
    if 'app' in schema and 'app' not in defaults:
        print("  ❌ defaults.yaml 缺少 'app' 配置")
        return False
    
    print("  ✓ 基本结构一致")
    return True

def check_prod_secrets():
    """检查生产环境必需密钥"""
    env = os.getenv('APP_ENV', 'dev')
    
    print(f"\n检查环境配置 (APP_ENV={env}):")
    
    if env == 'prod':
        required_secrets = [
            'OPENAI_API_KEY',
            'DATABASE_URL',
            # 可添加更多必需的环境变量
        ]
        
        missing = []
        for key in required_secrets:
            if not os.getenv(key):
                missing.append(key)
        
        if missing:
            print(f"  ❌ 生产环境缺少必需密钥: {', '.join(missing)}")
            return False
        
        print("  ✓ 生产环境密钥完整")
    else:
        print(f"  ⚠️  非生产环境，跳过密钥检查")
    
    return True

def check_config_types():
    """检查配置值的基本类型"""
    defaults = load_yaml('config/defaults.yaml')
    
    if not defaults:
        return False
    
    print("\n检查配置类型:")
    
    # 检查 app.env 是否是合法值
    app_env = defaults.get('app', {}).get('env')
    valid_envs = ['dev', 'staging', 'prod']
    
    if app_env and app_env not in valid_envs:
        print(f"  ❌ app.env 值非法: {app_env} (应为: {valid_envs})")
        return False
    
    print("  ✓ 配置类型检查通过")
    return True

def main():
    print("🔍 开始运行时配置校验...\n")
    
    checks = [
        check_config_structure(),
        check_defaults_against_schema(),
        check_config_types(),
        check_prod_secrets()
    ]
    
    print("\n" + "="*50)
    
    if all(checks):
        print("✅ 运行时配置校验通过")
        sys.exit(0)
    else:
        print("❌ 运行时配置校验失败")
        sys.exit(1)

if __name__ == '__main__':
    main()

