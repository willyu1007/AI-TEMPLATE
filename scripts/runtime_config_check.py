#!/usr/bin/env python3
"""

"""
import sys
import os
import yaml
import pathlib

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def load_yaml(path):
    """ YAML """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌  {path}: {e}")
        return None

def check_config_structure():
    """"""
    required_files = [
        'config/schema.yaml',
        'config/defaults.yaml'
    ]
    
    print(":")
    all_exists = True
    
    for file_path in required_files:
        if pathlib.Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ❌ : {file_path}")
            all_exists = False
    
    return all_exists

def check_defaults_against_schema():
    """ defaults.yaml  schema"""
    schema = load_yaml('config/schema.yaml')
    defaults = load_yaml('config/defaults.yaml')
    
    if not schema or not defaults:
        return False
    
    print("\n schema :")
    
    # schema  defaults 
    # 
    
    if 'app' in schema and 'app' not in defaults:
        print("  ❌ defaults.yaml  'app' ")
        return False
    
    print("  ✓ ")
    return True

def check_prod_secrets():
    """"""
    env = os.getenv('APP_ENV', 'dev')
    
    print(f"\n (APP_ENV={env}):")
    
    if env == 'prod':
        required_secrets = [
            'OPENAI_API_KEY',
            'DATABASE_URL',
            # 
        ]
        
        missing = []
        for key in required_secrets:
            if not os.getenv(key):
                missing.append(key)
        
        if missing:
            print(f"  ❌ : {', '.join(missing)}")
            return False
        
        print("  ✓ ")
    else:
        print(f"  ⚠️  ")
    
    return True

def check_config_types():
    """"""
    defaults = load_yaml('config/defaults.yaml')
    
    if not defaults:
        return False
    
    print("\n:")
    
    #  app.env 
    app_env = defaults.get('app', {}).get('env')
    valid_envs = ['dev', 'staging', 'prod']
    
    if app_env and app_env not in valid_envs:
        print(f"  ❌ app.env : {app_env} (: {valid_envs})")
        return False
    
    print("  ✓ ")
    return True

def main():
    print("🔍 ...\n")
    
    checks = [
        check_config_structure(),
        check_defaults_against_schema(),
        check_config_types(),
        check_prod_secrets()
    ]
    
    print("\n" + "="*50)
    
    if all(checks):
        print("✅ ")
        sys.exit(0)
    else:
        print("❌ ")
        sys.exit(1)

if __name__ == '__main__':
    main()

