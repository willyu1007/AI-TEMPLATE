#!/usr/bin/env python3
"""
轻量 docgen：汇总关键文档路径为 index.json 与 module_index.json
新增：summary/keywords/deps/version/snapshot_hash
"""
import json
import pathlib
import re
import hashlib
from datetime import datetime
from collections import Counter

def sha256_file(path):
    """计算文件的 SHA256 哈希"""
    try:
        content = path.read_bytes()
        return hashlib.sha256(content).hexdigest()[:16]  # 取前16字符
    except:
        return "error"

def extract_summary(path, max_len=240):
    """提取文档摘要（首 max_len 字符，跳过空行和标题）"""
    try:
        content = path.read_text(encoding='utf-8')
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]
        summary = ' '.join(lines)[:max_len]
        return summary if summary else "(empty)"
    except:
        return "(error)"

def extract_keywords(path, top_n=5):
    """提取关键词（简易 TF 统计）"""
    try:
        content = path.read_text(encoding='utf-8').lower()
        # 简单分词（移除标点）
        words = re.findall(r'\b[a-z]{3,}\b', content)
        # 停用词
        stopwords = {'the', 'and', 'for', 'this', 'that', 'with', 'from', 'are', 'was', 'not'}
        words = [w for w in words if w not in stopwords]
        counter = Counter(words)
        return [w for w, _ in counter.most_common(top_n)]
    except:
        return []

def extract_deps(path):
    """提取文档依赖（文件引用和契约引用）"""
    deps = []
    try:
        content = path.read_text(encoding='utf-8')
        # 查找文件引用模式：`/path/to/file` 或 "path/to/file"
        file_refs = re.findall(r'[`"]([a-zA-Z0-9_/.]+\.(md|yaml|json|py|sh))[`"]', content)
        deps.extend([ref[0] for ref in file_refs])
        
        # 查找契约引用
        contract_refs = re.findall(r'(tools/[a-zA-Z0-9_/]+/contract\.json)', content)
        deps.extend(contract_refs)
    except:
        pass
    return list(set(deps))  # 去重

def scan_docs():
    """扫描文档并生成索引"""
    root = pathlib.Path('.')
    index = {"docs": [], "generated_at": datetime.now().isoformat()}
    
    # 扫描关键目录
    target_dirs = ['docs', 'modules', 'flows', 'tools', '.aicontext']
    
    for p in root.rglob('*'):
        if p.is_file() and p.suffix in {'.md', '.yaml', '.json'}:
            # 检查是否在目标目录中
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
    """构建模块索引"""
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
    """计算整个索引的快照哈希"""
    # 排序后序列化，确保稳定性
    sorted_json = json.dumps(index_data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(sorted_json.encode()).hexdigest()[:16]

def main():
    # 确保目录存在
    pathlib.Path('.aicontext').mkdir(exist_ok=True)
    
    # 生成文档索引
    print("📚 扫描文档...")
    index = scan_docs()
    
    # 生成模块索引
    print("📦 构建模块索引...")
    module_index = build_module_index()
    
    # 计算快照哈希
    snapshot_hash = compute_snapshot_hash({"index": index, "modules": module_index})
    
    # 生成 snapshot.json
    snapshot = {
        "snapshot_hash": snapshot_hash,
        "generated_at": datetime.now().isoformat(),
        "version": "1.0"
    }
    
    # 写入文件
    index_path = pathlib.Path('.aicontext/index.json')
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✓ 生成 {index_path}")
    
    module_path = pathlib.Path('.aicontext/module_index.json')
    module_path.write_text(json.dumps(module_index, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✓ 生成 {module_path}")
    
    snapshot_path = pathlib.Path('.aicontext/snapshot.json')
    snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✓ 生成 {snapshot_path} (hash: {snapshot_hash})")
    
    print("\n✅ docgen 完成")

if __name__ == '__main__':
    main()
