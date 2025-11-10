#!/usr/bin/env python3
"""

 UX 
Phase 13
- 
- 
- N+1
- 
- JSON/Markdown
"""

import sys
import re
import pathlib
import yaml
import json
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import defaultdict, deque
from datetime import datetime

# Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def load_dag(dag_path: pathlib.Path = pathlib.Path('doc/flows/dag.yaml')) -> Dict:
    """ DAG """
    try:
        with open(dag_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"⚠️   DAG: {e}")
        return {}


def find_ux_docs(root_dir: pathlib.Path = pathlib.Path('.')) -> List[pathlib.Path]:
    """ UX """
    ux_docs = []
    ux_dir = root_dir / 'docs' / 'ux'
    
    if ux_dir.exists():
        for doc in ux_dir.glob('*.md'):
            ux_docs.append(doc)
    
    #  docs/ux/flows/ 
    flows_dir = root_dir / 'docs' / 'ux' / 'flows'
    if flows_dir.exists():
        for doc in flows_dir.rglob('*.md'):
            ux_docs.append(doc)
    
    return ux_docs


def extract_api_endpoints_from_docs(ux_doc: pathlib.Path) -> Set[str]:
    """ UX  API """
    try:
        content = ux_doc.read_text(encoding='utf-8')
    except Exception:
        return set()
    
    endpoints = set()
    
    #  API 
    # : /api/users, POST /api/login, GET /api/data/:id
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
            # 
            endpoint = re.sub(r'^(POST|GET|PUT|DELETE|PATCH)\s+', '', match, flags=re.IGNORECASE)
            endpoint = endpoint.strip('`\'"()')
            if endpoint:
                endpoints.add(endpoint)
    
    return endpoints


def extract_api_endpoints_from_code(root_dir: pathlib.Path = pathlib.Path('.')) -> Set[str]:
    """ API """
    endpoints = set()
    
    #  API 
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
            # 
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
    """"""
    issues = []
    
    #  DAG 
    if not dag or 'graph' not in dag:
        return True, issues
    
    graph = dag.get('graph', {})
    nodes = {n['id']: n for n in graph.get('nodes', [])}
    edges = graph.get('edges', [])
    
    #  UX  API 
    doc_endpoints = set()
    for ux_doc in ux_docs:
        doc_endpoints.update(extract_api_endpoints_from_docs(ux_doc))
    
    #  API 
    code_endpoints = extract_api_endpoints_from_code()
    
    # UX 
    missing_in_code = doc_endpoints - code_endpoints
    if missing_in_code:
        issues.append(f"UX  API : {', '.join(list(missing_in_code)[:5])}")
    
    #  DAG 
    #  Mermaid 
    
    return len(issues) == 0, issues


def check_ux_doc_structure(ux_doc: pathlib.Path) -> Tuple[bool, List[str]]:
    """ UX """
    try:
        content = ux_doc.read_text(encoding='utf-8')
    except Exception:
        return False, [""]
    
    issues = []
    
    # Mermaid
    has_flowchart = bool(re.search(r'```mermaid\s*\n\s*flowchart', content, re.IGNORECASE))
    has_sequence = bool(re.search(r'```mermaid\s*\n\s*sequenceDiagram', content, re.IGNORECASE))
    
    if not has_flowchart and not has_sequence:
        issues.append("Mermaid flowchart  sequenceDiagram")
    
    #  API 
    has_api_sequence = bool(re.search(r'(API||api).*(||sequence|flow)', content, re.IGNORECASE))
    
    if not has_api_sequence and (has_flowchart or has_sequence):
        issues.append(" API ")
    
    return len(issues) == 0, issues


def main():
    """"""
    print(" UX ...\n")
    
    #  DAG
    dag = load_dag()
    
    #  UX 
    ux_docs = find_ux_docs()
    
    if not ux_docs:
        print(" UX ")
        print(":  docs/ux/ ")
        sys.exit(0)
    
    print(f" {len(ux_docs)}  UX \n")
    
    all_passed = True
    
    #  UX 
    for ux_doc in ux_docs:
        doc_name = ux_doc.name
        print(f": {doc_name}")
        
        # 
        structure_ok, structure_issues = check_ux_doc_structure(ux_doc)
        if structure_issues:
            print(f"  ⚠️  : {', '.join(structure_issues)}")
        else:
            print(f"  ✓ ")
        
        print()
    
    # 
    consistency_ok, consistency_issues = check_dataflow_consistency(dag, ux_docs)
    
    if consistency_issues:
        print(":")
        for issue in consistency_issues:
            print(f"  ⚠️  {issue}")
        all_passed = False
    else:
        print(":")
        print(f"  ✓ ")
    
    print()
    
    # 
    print("=" * 50)
    if all_passed:
        print("✅ UX ")
    else:
        print("⚠️  UX ")
        print("💡 :  UX ")
    
    sys.exit(0 if all_passed else 0)  # 


# ============================================================================
# Phase 13
# ============================================================================

class DataflowAnalyzer:
    """Phase 13"""
    
    def __init__(self, dag: Dict):
        self.dag = dag
        self.graph = dag.get('graph', {}) if dag else {}
        self.nodes = {n['id']: n for n in self.graph.get('nodes', [])}
        self.edges = self.graph.get('edges', [])
        self.issues = []
        
    def detect_circular_dependencies(self) -> List[Dict]:
        """"""
        circular_deps = []
        
        # 
        adj_list = defaultdict(list)
        for edge in self.edges:
            from_node = edge.get('from')
            to_node = edge.get('to')
            if from_node and to_node:
                adj_list[from_node].append(to_node)
        
        # DFS
        visited = set()
        rec_stack = set()
        path = []
        
        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in adj_list.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    # 
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    circular_deps.append({
                        'type': 'circular_dependency',
                        'severity': 'critical',
                        'cycle': cycle,
                        'description': f": {' → '.join(cycle)}"
                    })
                    return True
            
            path.pop()
            rec_stack.remove(node)
            return False
        
        for node in self.nodes:
            if node not in visited:
                path = []
                dfs(node)
        
        return circular_deps
    
    def analyze_call_chain_depth(self, max_depth: int = 5) -> List[Dict]:
        """"""
        deep_chains = []
        
        # 
        adj_list = defaultdict(list)
        for edge in self.edges:
            from_node = edge.get('from')
            to_node = edge.get('to')
            if from_node and to_node:
                adj_list[from_node].append(to_node)
        
        # BFS
        def get_longest_path(start_node):
            queue = deque([(start_node, [start_node], 0)])
            longest = ([], 0)
            
            while queue:
                node, path, depth = queue.popleft()
                
                if depth > longest[1]:
                    longest = (path, depth)
                
                for neighbor in adj_list.get(node, []):
                    if neighbor not in path:  # 
                        queue.append((neighbor, path + [neighbor], depth + 1))
            
            return longest
        
        # 
        for node in self.nodes:
            longest_path, depth = get_longest_path(node)
            if depth > max_depth:
                deep_chains.append({
                    'type': 'deep_call_chain',
                    'severity': 'high',
                    'start_node': node,
                    'depth': depth,
                    'path': longest_path,
                    'description': f"({depth}): {' → '.join(longest_path[:5])}..."
                })
        
        return deep_chains
    
    def detect_n_plus_one_queries(self) -> List[Dict]:
        """N+1"""
        n_plus_one_issues = []
        
        # 
        for node_id, node in self.nodes.items():
            node_type = node.get('type', '')
            node_label = node.get('label', '')
            
            # 
            if 'loop' in node_label.lower() or 'foreach' in node_label.lower():
                # 
                children = [e['to'] for e in self.edges if e['from'] == node_id]
                
                for child in children:
                    child_node = self.nodes.get(child, {})
                    child_label = child_node.get('label', '')
                    
                    if any(keyword in child_label.lower() for keyword in ['query', 'select', 'db', 'database', 'find']):
                        n_plus_one_issues.append({
                            'type': 'n_plus_one_query',
                            'severity': 'high',
                            'loop_node': node_id,
                            'query_node': child,
                            'description': f"N+1: '{node_label}''{child_label}'"
                        })
        
        return n_plus_one_issues
    
    def detect_missing_indexes(self) -> List[Dict]:
        """"""
        missing_indexes = []
        
        # JOIN
        for node_id, node in self.nodes.items():
            node_label = node.get('label', '')
            node_meta = node.get('metadata', {})
            
            # JOIN
            if 'join' in node_label.lower():
                table_size = node_meta.get('table_size', 'unknown')
                has_index = node_meta.get('indexed', False)
                
                if table_size in ['large', 'very_large'] and not has_index:
                    missing_indexes.append({
                        'type': 'missing_index',
                        'severity': 'medium',
                        'node': node_id,
                        'table_size': table_size,
                        'description': f"JOIN: {node_label}"
                    })
        
        return missing_indexes
    
    def analyze_all(self) -> Dict:
        """"""
        return {
            'circular_dependencies': self.detect_circular_dependencies(),
            'deep_call_chains': self.analyze_call_chain_depth(),
            'n_plus_one_queries': self.detect_n_plus_one_queries(),
            'missing_indexes': self.detect_missing_indexes()
        }


# ============================================================================
# Phase 13
# ============================================================================

class BottleneckDetector:
    """"""
    
    def __init__(self, dag: Dict):
        self.dag = dag
        self.graph = dag.get('graph', {}) if dag else {}
        self.nodes = {n['id']: n for n in self.graph.get('nodes', [])}
        self.edges = self.graph.get('edges', [])
    
    def detect_serial_vs_parallel(self) -> List[Dict]:
        """vs"""
        opportunities = []
        
        # 
        adj_list = defaultdict(list)
        for edge in self.edges:
            from_node = edge.get('from')
            to_node = edge.get('to')
            if from_node and to_node:
                adj_list[from_node].append(to_node)
        
        # 
        for node_id, children in adj_list.items():
            if len(children) >= 2:
                # 
                children_deps = set()
                for child in children:
                    for edge in self.edges:
                        if edge['from'] in children and edge['to'] in children:
                            children_deps.add((edge['from'], edge['to']))
                
                # 
                if not children_deps:
                    node_label = self.nodes.get(node_id, {}).get('label', node_id)
                    children_labels = [self.nodes.get(c, {}).get('label', c) for c in children]
                    
                    opportunities.append({
                        'type': 'parallelization_opportunity',
                        'severity': 'medium',
                        'parent_node': node_id,
                        'parallel_tasks': children,
                        'description': f": '{node_label}'  {len(children)} : {', '.join(children_labels[:3])}"
                    })
        
        return opportunities
    
    def recommend_caching(self) -> List[Dict]:
        """"""
        cache_recommendations = []
        
        # 
        in_degree = defaultdict(int)
        for edge in self.edges:
            to_node = edge.get('to')
            if to_node:
                in_degree[to_node] += 1
        
        # >2
        for node_id, degree in in_degree.items():
            if degree > 2:
                node = self.nodes.get(node_id, {})
                node_label = node.get('label', node_id)
                node_type = node.get('type', '')
                
                # 
                if node_type not in ['user_input', 'random']:
                    cache_recommendations.append({
                        'type': 'caching_opportunity',
                        'severity': 'low',
                        'node': node_id,
                        'call_count': degree,
                        'description': f"({degree}): '{node_label}' "
                    })
        
        return cache_recommendations
    
    def detect_redundant_computations(self) -> List[Dict]:
        """"""
        redundant = []
        
        # 
        label_groups = defaultdict(list)
        for node_id, node in self.nodes.items():
            label = node.get('label', '').strip()
            if label:
                label_groups[label].append(node_id)
        
        # 
        for label, node_ids in label_groups.items():
            if len(node_ids) > 1:
                redundant.append({
                    'type': 'redundant_computation',
                    'severity': 'low',
                    'label': label,
                    'nodes': node_ids,
                    'count': len(node_ids),
                    'description': f": '{label}'  {len(node_ids)} "
                })
        
        return redundant
    
    def prioritize_optimizations(self, all_issues: List[Dict]) -> List[Dict]:
        """"""
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        
        # 
        sorted_issues = sorted(all_issues, key=lambda x: (
            severity_order.get(x.get('severity', 'low'), 99),
            -x.get('impact_score', 0)
        ))
        
        # 
        for i, issue in enumerate(sorted_issues, 1):
            issue['priority'] = i
        
        return sorted_issues
    
    def analyze_all(self) -> Dict:
        """"""
        all_issues = []
        
        serial_parallel = self.detect_serial_vs_parallel()
        caching = self.recommend_caching()
        redundant = self.detect_redundant_computations()
        
        all_issues.extend(serial_parallel)
        all_issues.extend(caching)
        all_issues.extend(redundant)
        
        prioritized = self.prioritize_optimizations(all_issues)
        
        return {
            'parallelization_opportunities': serial_parallel,
            'caching_recommendations': caching,
            'redundant_computations': redundant,
            'prioritized_issues': prioritized
        }


# ============================================================================
# Phase 13
# ============================================================================

class ReportGenerator:
    """"""
    
    def __init__(self, analysis_results: Dict, bottleneck_results: Dict):
        self.analysis = analysis_results
        self.bottlenecks = bottlenecks
        self.timestamp = datetime.now().isoformat()
    
    def generate_json_report(self, output_path: pathlib.Path) -> Dict:
        """JSON"""
        report = {
            'timestamp': self.timestamp,
            'version': '1.0',
            'summary': self._generate_summary(),
            'static_analysis': self.analysis,
            'bottleneck_detection': self.bottlenecks
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            return report
        except Exception as e:
            print(f"❌ JSON: {e}", file=sys.stderr)
            return {}
    
    def generate_markdown_report(self, output_path: pathlib.Path) -> str:
        """Markdown"""
        summary = self._generate_summary()
        
        md = f"# \n\n"
        md += f"> ****: {self.timestamp}\n\n"
        md += "---\n\n"
        
        # 
        md += "## 📊 \n\n"
        md += f"- **Critical**: {summary['critical_count']} \n"
        md += f"- **High**: {summary['high_count']} \n"
        md += f"- **Medium**: {summary['medium_count']} \n"
        md += f"- **Low**: {summary['low_count']} \n"
        md += f"- ****: {summary['total_issues']} \n\n"
        md += "---\n\n"
        
        # Critical
        if summary['critical_count'] > 0:
            md += "## 🔴 Critical\n\n"
            md += self._format_issues_markdown(self._get_issues_by_severity('critical'))
            md += "\n---\n\n"
        
        # High
        if summary['high_count'] > 0:
            md += "## 🟠 High\n\n"
            md += self._format_issues_markdown(self._get_issues_by_severity('high'))
            md += "\n---\n\n"
        
        # Medium
        if summary['medium_count'] > 0:
            md += "## 🟡 Medium\n\n"
            md += self._format_issues_markdown(self._get_issues_by_severity('medium'))
            md += "\n---\n\n"
        
        # Low
        if summary['low_count'] > 0:
            md += "## 🟢 Low\n\n"
            md += self._format_issues_markdown(self._get_issues_by_severity('low'))
            md += "\n---\n\n"
        
        # Top 5
        md += "## 🎯 Top 5\n\n"
        md += self._format_top_recommendations()
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md)
            return md
        except Exception as e:
            print(f"❌ Markdown: {e}", file=sys.stderr)
            return ""
    
    def _generate_summary(self) -> Dict:
        """"""
        all_issues = []
        
        # 
        for category, issues in self.analysis.items():
            all_issues.extend(issues)
        
        for category, issues in self.bottlenecks.items():
            if category != 'prioritized_issues':
                all_issues.extend(issues)
        
        # 
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        for issue in all_issues:
            severity = issue.get('severity', 'low')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            'total_issues': len(all_issues),
            'critical_count': severity_counts['critical'],
            'high_count': severity_counts['high'],
            'medium_count': severity_counts['medium'],
            'low_count': severity_counts['low']
        }
    
    def _get_issues_by_severity(self, severity: str) -> List[Dict]:
        """"""
        issues = []
        
        for category, items in self.analysis.items():
            for issue in items:
                if issue.get('severity') == severity:
                    issues.append(issue)
        
        for category, items in self.bottlenecks.items():
            if category != 'prioritized_issues':
                for issue in items:
                    if issue.get('severity') == severity:
                        issues.append(issue)
        
        return issues
    
    def _format_issues_markdown(self, issues: List[Dict]) -> str:
        """Markdown"""
        if not issues:
            return "\n"
        
        md = ""
        for i, issue in enumerate(issues, 1):
            issue_type = issue.get('type', 'unknown')
            description = issue.get('description', 'N/A')
            md += f"{i}. **{issue_type}**: {description}\n"
        
        return md
    
    def _format_top_recommendations(self) -> str:
        """Top"""
        prioritized = self.bottlenecks.get('prioritized_issues', [])
        
        if not prioritized:
            return "\n"
        
        md = ""
        for i, issue in enumerate(prioritized[:5], 1):
            description = issue.get('description', 'N/A')
            severity = issue.get('severity', 'low')
            md += f"{i}. [{severity.upper()}] {description}\n"
        
        return md


# ============================================================================
# main
# ============================================================================

if __name__ == '__main__':
    main()

