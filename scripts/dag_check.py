#!/usr/bin/env python3
"""
DAG 校验：检查无环、去重、引用存在、契约文件存在
"""
import sys
import yaml
import pathlib
from collections import defaultdict, deque

def load_dag(dag_path='flows/dag.yaml'):
    """加载 DAG 配置"""
    try:
        with open(dag_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ 无法加载 DAG 文件: {e}")
        sys.exit(1)

def check_duplicate_nodes(nodes):
    """检查重复节点"""
    node_ids = [n['id'] for n in nodes]
    duplicates = [nid for nid in node_ids if node_ids.count(nid) > 1]
    if duplicates:
        print(f"❌ 发现重复节点: {set(duplicates)}")
        return False
    print("✓ 无重复节点")
    return True

def check_cycle(nodes, edges):
    """检查是否有环（拓扑排序）"""
    # 构建邻接表和入度表
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    node_ids = {n['id'] for n in nodes}
    
    for n in nodes:
        in_degree[n['id']] = 0
    
    for edge in edges:
        from_node = edge.get('from')
        to_node = edge.get('to')
        if from_node and to_node:
            graph[from_node].append(to_node)
            in_degree[to_node] += 1
    
    # 拓扑排序（Kahn算法）
    queue = deque([nid for nid in node_ids if in_degree[nid] == 0])
    sorted_nodes = []
    
    while queue:
        node = queue.popleft()
        sorted_nodes.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(sorted_nodes) != len(node_ids):
        print(f"❌ DAG 存在环！已排序 {len(sorted_nodes)}/{len(node_ids)} 个节点")
        return False
    
    print("✓ DAG 无环")
    return True

def check_edge_references(nodes, edges):
    """检查边引用的节点是否存在"""
    node_ids = {n['id'] for n in nodes}
    errors = []
    
    for edge in edges:
        from_node = edge.get('from')
        to_node = edge.get('to')
        
        if from_node and from_node not in node_ids:
            errors.append(f"边引用的源节点不存在: {from_node}")
        if to_node and to_node not in node_ids:
            errors.append(f"边引用的目标节点不存在: {to_node}")
    
    if errors:
        print(f"❌ 边引用错误:")
        for err in errors:
            print(f"  - {err}")
        return False
    
    print("✓ 所有边引用有效")
    return True

def check_contract_files(nodes):
    """检查契约文件是否存在"""
    errors = []
    
    for node in nodes:
        contracts = node.get('contracts', {})
        contract_file = contracts.get('file')
        
        if contract_file:
            path = pathlib.Path(contract_file)
            if not path.exists():
                errors.append(f"节点 {node['id']} 的契约文件不存在: {contract_file}")
    
    if errors:
        print(f"❌ 契约文件缺失:")
        for err in errors:
            print(f"  - {err}")
        return False
    
    print("✓ 所有契约文件存在")
    return True

def main():
    print("🔍 开始 DAG 校验...\n")
    
    # 加载 DAG
    dag = load_dag()
    
    if not dag or 'graph' not in dag:
        print("❌ DAG 格式错误：缺少 'graph' 字段")
        sys.exit(1)
    
    graph = dag['graph']
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])
    
    if not nodes:
        print("⚠️  DAG 中没有节点")
        sys.exit(0)
    
    print(f"📊 节点数: {len(nodes)}, 边数: {len(edges)}\n")
    
    # 执行检查
    checks = [
        check_duplicate_nodes(nodes),
        check_cycle(nodes, edges),
        check_edge_references(nodes, edges),
        check_contract_files(nodes)
    ]
    
    # 总结
    print("\n" + "="*50)
    if all(checks):
        print("✅ DAG 校验通过")
        sys.exit(0)
    else:
        print("❌ DAG 校验失败")
        sys.exit(1)

if __name__ == '__main__':
    main()

