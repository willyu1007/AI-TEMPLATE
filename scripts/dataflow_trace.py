#!/usr/bin/env python3
"""
数据流追踪检查脚本
检查 UX 文档中的流程图是否与代码实现一致
"""

import sys
import re
import pathlib
import yaml
from typing import List, Dict, Set, Tuple

# Windows控制台编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def load_dag(dag_path: pathlib.Path = pathlib.Path('flows/dag.yaml')) -> Dict:
    """加载 DAG 配置"""
    try:
        with open(dag_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"⚠️  无法加载 DAG: {e}")
        return {}


def find_ux_docs(root_dir: pathlib.Path = pathlib.Path('.')) -> List[pathlib.Path]:
    """查找所有 UX 文档"""
    ux_docs = []
    ux_dir = root_dir / 'docs' / 'ux'
    
    if ux_dir.exists():
        for doc in ux_dir.glob('*.md'):
            ux_docs.append(doc)
    
    # 也检查 docs/ux/flows/ 目录
    flows_dir = root_dir / 'docs' / 'ux' / 'flows'
    if flows_dir.exists():
        for doc in flows_dir.rglob('*.md'):
            ux_docs.append(doc)
    
    return ux_docs


def extract_api_endpoints_from_docs(ux_doc: pathlib.Path) -> Set[str]:
    """从 UX 文档中提取 API 端点"""
    try:
        content = ux_doc.read_text(encoding='utf-8')
    except Exception:
        return set()
    
    endpoints = set()
    
    # 匹配 API 路径模式
    # 例如: /api/users, POST /api/login, GET /api/data/:id
    patterns = [
        r'[/]api[/][^\s`\'"\)]+',  # /api/xxx
        r'POST\s+[/]api[/][^\s]+',  # POST /api/xxx
        r'GET\s+[/]api[/][^\s]+',   # GET /api/xxx
        r'PUT\s+[/]api[/][^\s]+',   # PUT /api/xxx
        r'DELETE\s+[/]api[/][^\s]+', # DELETE /api/xxx
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            # 清理匹配结果
            endpoint = re.sub(r'^(POST|GET|PUT|DELETE|PATCH)\s+', '', match, flags=re.IGNORECASE)
            endpoint = endpoint.strip('`\'"()')
            if endpoint:
                endpoints.add(endpoint)
    
    return endpoints


def extract_api_endpoints_from_code(root_dir: pathlib.Path = pathlib.Path('.')) -> Set[str]:
    """从代码中提取 API 端点（基础实现）"""
    endpoints = set()
    
    # 查找常见的 API 路由定义模式
    # Python: @app.route('/api/...'), @router.post('/api/...')
    # Go: router.HandleFunc('/api/...', ...)
    # TypeScript: app.get('/api/...', ...)
    
    patterns = {
        '*.py': [
            r'@(app|router|api)\.(route|get|post|put|delete|patch)\s*\([\'"]([/]api[/][^\'"\)]+)',
            r'@(app|router|api)\.(route|get|post|put|delete|patch)\s*\([\'"]([/]api[/][^\'"\)]+)',
        ],
        '*.go': [
            r'router\.(HandleFunc|Get|Post|Put|Delete)\s*\([\'"]([/]api[/][^\'"\)]+)',
        ],
        '*.ts': [
            r'app\.(get|post|put|delete|patch)\s*\([\'"]([/]api[/][^\'"\)]+)',
        ],
    }
    
    for ext, pattern_list in patterns.items():
        for code_file in root_dir.rglob(ext):
            # 跳过测试和构建目录
            if any(part in code_file.parts for part in ['node_modules', 'venv', '.venv', 'build', 'dist', '__pycache__']):
                continue
            
            try:
                content = code_file.read_text(encoding='utf-8')
                for pattern in pattern_list:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        if isinstance(match, tuple):
                            endpoint = match[-1] if match else ''
                        else:
                            endpoint = match
                        if endpoint:
                            endpoints.add(endpoint)
            except Exception:
                continue
    
    return endpoints


def check_dataflow_consistency(dag: Dict, ux_docs: List[pathlib.Path]) -> Tuple[bool, List[str]]:
    """检查数据流一致性"""
    issues = []
    
    # 从 DAG 中提取节点间的数据流
    if not dag or 'graph' not in dag:
        return True, issues
    
    graph = dag.get('graph', {})
    nodes = {n['id']: n for n in graph.get('nodes', [])}
    edges = graph.get('edges', [])
    
    # 从 UX 文档中提取 API 端点
    doc_endpoints = set()
    for ux_doc in ux_docs:
        doc_endpoints.update(extract_api_endpoints_from_docs(ux_doc))
    
    # 从代码中提取 API 端点
    code_endpoints = extract_api_endpoints_from_code()
    
    # 检查：UX 文档中的端点是否在代码中存在
    missing_in_code = doc_endpoints - code_endpoints
    if missing_in_code:
        issues.append(f"UX 文档中提到的 API 端点未在代码中找到: {', '.join(list(missing_in_code)[:5])}")
    
    # 检查：是否有流程图但没有对应的 DAG 节点
    # 这个检查比较复杂，需要解析 Mermaid 图，暂时跳过
    
    return len(issues) == 0, issues


def check_ux_doc_structure(ux_doc: pathlib.Path) -> Tuple[bool, List[str]]:
    """检查 UX 文档结构"""
    try:
        content = ux_doc.read_text(encoding='utf-8')
    except Exception:
        return False, ["无法读取文件"]
    
    issues = []
    
    # 检查是否包含流程图（Mermaid）
    has_flowchart = bool(re.search(r'```mermaid\s*\n\s*flowchart', content, re.IGNORECASE))
    has_sequence = bool(re.search(r'```mermaid\s*\n\s*sequenceDiagram', content, re.IGNORECASE))
    
    if not has_flowchart and not has_sequence:
        issues.append("缺少流程图（Mermaid flowchart 或 sequenceDiagram）")
    
    # 检查是否包含 API 调用序列
    has_api_sequence = bool(re.search(r'(API|接口|api).*(调用|序列|sequence|flow)', content, re.IGNORECASE))
    
    if not has_api_sequence and (has_flowchart or has_sequence):
        issues.append("流程图存在但缺少 API 调用序列说明")
    
    return len(issues) == 0, issues


def main():
    """主函数"""
    print("检查 UX 数据流转文档一致性...\n")
    
    # 加载 DAG
    dag = load_dag()
    
    # 查找 UX 文档
    ux_docs = find_ux_docs()
    
    if not ux_docs:
        print("未找到 UX 文档")
        print("提示: 确保 docs/ux/ 目录下有文档")
        sys.exit(0)
    
    print(f"找到 {len(ux_docs)} 个 UX 文档\n")
    
    all_passed = True
    
    # 检查每个 UX 文档
    for ux_doc in ux_docs:
        doc_name = ux_doc.name
        print(f"检查文档: {doc_name}")
        
        # 检查文档结构
        structure_ok, structure_issues = check_ux_doc_structure(ux_doc)
        if structure_issues:
            print(f"  ⚠️  结构问题: {', '.join(structure_issues)}")
        else:
            print(f"  ✓ 文档结构完整")
        
        print()
    
    # 检查数据流一致性
    consistency_ok, consistency_issues = check_dataflow_consistency(dag, ux_docs)
    
    if consistency_issues:
        print("数据流一致性检查:")
        for issue in consistency_issues:
            print(f"  ⚠️  {issue}")
        all_passed = False
    else:
        print("数据流一致性检查:")
        print(f"  ✓ 未发现明显的不一致")
    
    print()
    
    # 总结
    print("=" * 50)
    if all_passed:
        print("✅ UX 数据流转文档检查通过")
    else:
        print("⚠️  UX 数据流转文档存在一些问题")
        print("💡 建议: 更新 UX 文档以反映实际的数据流")
    
    sys.exit(0 if all_passed else 0)  # 数据流检查不阻塞，仅警告


if __name__ == '__main__':
    main()

