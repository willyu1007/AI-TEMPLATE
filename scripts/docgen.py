#!/usr/bin/env python3
"""
 docgen index.json  module_index.json
summary/keywords/deps/version/snapshot_hash
"""
import json
import pathlib
import re
import hashlib
import sys
from datetime import datetime
from collections import Counter

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def sha256_file(path):
    """ SHA256 """
    try:
        content = path.read_bytes()
        return hashlib.sha256(content).hexdigest()[:16]  # 16
    except:
        return "error"

def extract_summary(path, max_len=240):
    """ max_len """
    try:
        content = path.read_text(encoding='utf-8')
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]
        summary = ' '.join(lines)[:max_len]
        return summary if summary else "(empty)"
    except:
        return "(error)"

def extract_keywords(path, top_n=5):
    """ TF """
    try:
        content = path.read_text(encoding='utf-8').lower()
        # 
        words = re.findall(r'\b[a-z]{3,}\b', content)
        # 
        stopwords = {'the', 'and', 'for', 'this', 'that', 'with', 'from', 'are', 'was', 'not'}
        words = [w for w in words if w not in stopwords]
        counter = Counter(words)
        return [w for w, _ in counter.most_common(top_n)]
    except:
        return []

def extract_deps(path):
    """"""
    deps = []
    try:
        content = path.read_text(encoding='utf-8')
        # `/path/to/file`  "path/to/file"
        file_refs = re.findall(r'[`"]([a-zA-Z0-9_/.]+\.(md|yaml|json|py|sh))[`"]', content)
        deps.extend([ref[0] for ref in file_refs])
        
        # 
        contract_refs = re.findall(r'(tools/[a-zA-Z0-9_/]+/contract\.json)', content)
        deps.extend(contract_refs)
    except:
        pass
    return list(set(deps))  # 

def scan_docs():
    """"""
    root = pathlib.Path('.')
    index = {"docs": [], "generated_at": datetime.now().isoformat()}
    
    # 
    target_dirs = ['docs', 'modules', 'flows', 'tools', '.aicontext']
    
    for p in root.rglob('*'):
        if p.is_file() and p.suffix in {'.md', '.yaml', '.json'}:
            # 
            if any(str(p).startswith(s) for s in target_dirs):
                doc_info = {
                    "path": str(p).replace('\\', '/'),
                    "hash": sha256_file(p),
                    "summary": extract_summary(p) if p.suffix == '.md' else None,
                    "keywords": extract_keywords(p) if p.suffix == '.md' else None,
                    "deps": extract_deps(p) if p.suffix == '.md' else None
                }
                index["docs"].append(doc_info)
    
    return index

def build_module_index():
    """"""
    root = pathlib.Path('.')
    mod = {}
    
    modules_dir = root / 'modules'
    if modules_dir.exists():
        for m in modules_dir.glob('*'):
            if m.is_dir():
                mod[m.name] = {
                    "readme": str(m/'README.md').replace('\\', '/'),
                    "plan": str(m/'plan.md').replace('\\', '/'),
                    "contract": str(m/'CONTRACT.md').replace('\\', '/'),
                    "test_plan": str(m/'TEST_PLAN.md').replace('\\', '/'),
                    "tests": f"tests/{m.name}/"
                }
    
    return {"modules": mod, "generated_at": datetime.now().isoformat()}

def compute_snapshot_hash(index_data):
    """"""
    # 
    sorted_json = json.dumps(index_data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(sorted_json.encode()).hexdigest()[:16]

def main():
    # 
    pathlib.Path('.aicontext').mkdir(exist_ok=True)
    
    # 
    print("📚 ...")
    index = scan_docs()
    
    # 
    print("📦 ...")
    module_index = build_module_index()
    
    # 
    snapshot_hash = compute_snapshot_hash({"index": index, "modules": module_index})
    
    #  snapshot.json
    snapshot = {
        "snapshot_hash": snapshot_hash,
        "generated_at": datetime.now().isoformat(),
        "version": "1.0"
    }
    
    # 
    index_path = pathlib.Path('.aicontext/index.json')
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✓  {index_path}")
    
    module_path = pathlib.Path('.aicontext/module_index.json')
    module_path.write_text(json.dumps(module_index, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✓  {module_path}")
    
    snapshot_path = pathlib.Path('.aicontext/snapshot.json')
    snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✓  {snapshot_path} (hash: {snapshot_hash})")
    
    print("\n✅ docgen ")

if __name__ == '__main__':
    main()
