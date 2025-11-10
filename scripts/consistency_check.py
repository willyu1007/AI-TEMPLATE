#!/usr/bin/env python3
"""

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
    """ JSON """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌  {path}: {e}")
        return None

def check_snapshot_consistency():
    """"""
    snapshot = load_json('.aicontext/snapshot.json')
    
    if not snapshot:
        print("❌ snapshot.json ")
        return False
    
    snapshot_hash = snapshot.get('snapshot_hash')
    if not snapshot_hash:
        print("❌ snapshot.json  snapshot_hash")
        return False
    
    print(f"✓ snapshot_hash: {snapshot_hash}")
    return True

def check_module_docs():
    """"""
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
        print("⚠️  modules/ ")
        return True
    
    all_passed = True
    
    for module_dir in modules_dir.iterdir():
        if not module_dir.is_dir():
            continue
        
        print(f"\n: {module_dir.name}")
        missing = []
        
        for doc in required_docs:
            doc_path = module_dir / doc
            if not doc_path.exists():
                missing.append(doc)
        
        if missing:
            print(f"  ❌ : {', '.join(missing)}")
            all_passed = False
        else:
            print(f"  ✓ ")
    
    return all_passed

def check_key_references():
    """"""
    checks = [
        ('doc/flows/dag.yaml', 'DAG '),
        ('db/engines/postgres/docs/DB_SPEC.yaml', ''),
        ('doc/process/ENV_SPEC.yaml', ''),
        ('.aicontext/index.json', ''),
        ('.aicontext/module_index.json', ''),
    ]
    
    print("\n:")
    all_passed = True
    
    for path, desc in checks:
        if pathlib.Path(path).exists():
            print(f"  ✓ {desc}: {path}")
        else:
            print(f"  ❌ {desc} : {path}")
            all_passed = False
    
    return all_passed

def main():
    print("🔍 ...\n")
    
    checks = [
        ("", check_snapshot_consistency()),
        ("", check_module_docs()),
        ("", check_key_references())
    ]
    
    print("\n" + "="*50)
    
    failed_checks = [name for name, passed in checks if not passed]
    
    if not failed_checks:
        print("✅ ")
        sys.exit(0)
    else:
        print(f"❌ : {', '.join(failed_checks)}")
        print("💡  'make docgen' ")
        sys.exit(1)

if __name__ == '__main__':
    main()

