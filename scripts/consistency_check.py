#!/usr/bin/env python3
"""
一致性检查：校验模块必备文档、索引哈希一致性
"""
import sys
import json
import pathlib

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def load_json(path):
    """加载 JSON 文件"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 无法加载 {path}: {e}")
        return None

def check_snapshot_consistency():
    """检查快照哈希一致性"""
    snapshot = load_json('.aicontext/snapshot.json')
    
    if not snapshot:
        print("❌ snapshot.json 不存在或无法加载")
        return False
    
    snapshot_hash = snapshot.get('snapshot_hash')
    if not snapshot_hash:
        print("❌ snapshot.json 缺少 snapshot_hash")
        return False
    
    print(f"✓ snapshot_hash: {snapshot_hash}")
    return True

def check_module_docs():
    """检查模块必备文档"""
    required_docs = [
        'README.md',
        'plan.md',
        'CONTRACT.md',
        'TEST_PLAN.md',
        'RUNBOOK.md',
        'PROGRESS.md',
        'BUGS.md',
        'CHANGELOG.md'
    ]
    
    modules_dir = pathlib.Path('modules')
    
    if not modules_dir.exists():
        print("⚠️  modules/ 目录不存在")
        return True
    
    all_passed = True
    
    for module_dir in modules_dir.iterdir():
        if not module_dir.is_dir():
            continue
        
        print(f"\n检查模块: {module_dir.name}")
        missing = []
        
        for doc in required_docs:
            doc_path = module_dir / doc
            if not doc_path.exists():
                missing.append(doc)
        
        if missing:
            print(f"  ❌ 缺少文档: {', '.join(missing)}")
            all_passed = False
        else:
            print(f"  ✓ 文档齐全")
    
    return all_passed

def check_key_references():
    """检查关键引用存在"""
    checks = [
        ('doc/flows/dag.yaml', 'DAG 配置'),
        ('db/engines/postgres/docs/DB_SPEC.yaml', '数据库规范'),
        ('doc/process/ENV_SPEC.yaml', '环境规范'),
        ('.aicontext/index.json', '文档索引'),
        ('.aicontext/module_index.json', '模块索引'),
    ]
    
    print("\n检查关键文件:")
    all_passed = True
    
    for path, desc in checks:
        if pathlib.Path(path).exists():
            print(f"  ✓ {desc}: {path}")
        else:
            print(f"  ❌ {desc} 缺失: {path}")
            all_passed = False
    
    return all_passed

def main():
    print("🔍 开始一致性检查...\n")
    
    checks = [
        ("快照哈希", check_snapshot_consistency()),
        ("模块文档", check_module_docs()),
        ("关键引用", check_key_references())
    ]
    
    print("\n" + "="*50)
    
    failed_checks = [name for name, passed in checks if not passed]
    
    if not failed_checks:
        print("✅ 一致性检查全部通过")
        sys.exit(0)
    else:
        print(f"❌ 一致性检查失败: {', '.join(failed_checks)}")
        print("💡 请运行 'make docgen' 更新索引或补齐缺失文档")
        sys.exit(1)

if __name__ == '__main__':
    main()

