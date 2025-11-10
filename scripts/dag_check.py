#!/usr/bin/env python3
"""
DAG 
"""
import sys
import yaml
import pathlib
from collections import defaultdict, deque

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def load_dag(dag_path='doc/flows/dag.yaml'):
    """ DAG """
    try:
        with open(dag_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌  DAG : {e}")
        sys.exit(1)

def check_duplicate_nodes(nodes):
    """"""
    node_ids = [n['id'] for n in nodes]
    duplicates = [nid for nid in node_ids if node_ids.count(nid) > 1]
    if duplicates:
        print(f"❌ : {set(duplicates)}")
        return False
    print("✓ ")
    return True

def check_cycle(nodes, edges):
    """"""
    # 
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
    
    # Kahn
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
        print(f"❌ DAG  {len(sorted_nodes)}/{len(node_ids)} ")
        return False
    
    print("✓ DAG ")
    return True

def check_edge_references(nodes, edges):
    """"""
    node_ids = {n['id'] for n in nodes}
    errors = []
    
    for edge in edges:
        from_node = edge.get('from')
        to_node = edge.get('to')
        
        if from_node and from_node not in node_ids:
            errors.append(f": {from_node}")
        if to_node and to_node not in node_ids:
            errors.append(f": {to_node}")
    
    if errors:
        print(f"❌ :")
        for err in errors:
            print(f"  - {err}")
        return False
    
    print("✓ ")
    return True

def check_contract_files(nodes):
    """"""
    errors = []
    
    for node in nodes:
        contracts = node.get('contracts', {})
        contract_file = contracts.get('file')
        
        if contract_file:
            path = pathlib.Path(contract_file)
            if not path.exists():
                errors.append(f" {node['id']} : {contract_file}")
    
    if errors:
        print(f"❌ :")
        for err in errors:
            print(f"  - {err}")
        return False
    
    print("✓ ")
    return True

def main():
    print("🔍  DAG ...\n")
    
    #  DAG
    dag = load_dag()
    
    if not dag or 'graph' not in dag:
        print("❌ DAG  'graph' ")
        sys.exit(1)
    
    graph = dag['graph']
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])
    
    if not nodes:
        print("⚠️  DAG ")
        sys.exit(0)
    
    print(f"📊 : {len(nodes)}, : {len(edges)}\n")
    
    # 
    checks = [
        check_duplicate_nodes(nodes),
        check_cycle(nodes, edges),
        check_edge_references(nodes, edges),
        check_contract_files(nodes)
    ]
    
    # 
    print("\n" + "="*50)
    if all(checks):
        print("✅ DAG ")
        sys.exit(0)
    else:
        print("❌ DAG ")
        sys.exit(1)

if __name__ == '__main__':
    main()

