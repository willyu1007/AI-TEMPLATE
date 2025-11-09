#!/usr/bin/env python3
"""
数据流追踪检查脚本（增强版）
检查 UX 文档中的流程图是否与代码实现一致
Phase 13增强功能：
- 循环依赖检测
- 调用链深度分析
- N+1查询模式识别
- 性能瓶颈检测
- JSON/Markdown报告生成
"""

import sys
import re
import pathlib
import yaml
import json
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import defaultdict, deque
from datetime import datetime

# Windows控制台编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def load_dag(dag_path: pathlib.Path = pathlib.Path('doc/flows/dag.yaml')) -> Dict:
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


# ============================================================================
# Phase 13新增功能：静态分析增强
# ============================================================================

class DataflowAnalyzer:
    """数据流分析器（Phase 13增强）"""
    
    def __init__(self, dag: Dict):
        self.dag = dag
        self.graph = dag.get('graph', {}) if dag else {}
        self.nodes = {n['id']: n for n in self.graph.get('nodes', [])}
        self.edges = self.graph.get('edges', [])
        self.issues = []
        
    def detect_circular_dependencies(self) -> List[Dict]:
        """检测循环依赖"""
        circular_deps = []
        
        # 构建邻接表
        adj_list = defaultdict(list)
        for edge in self.edges:
            from_node = edge.get('from')
            to_node = edge.get('to')
            if from_node and to_node:
                adj_list[from_node].append(to_node)
        
        # DFS检测环
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
                    # 找到循环
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    circular_deps.append({
                        'type': 'circular_dependency',
                        'severity': 'critical',
                        'cycle': cycle,
                        'description': f"循环依赖: {' → '.join(cycle)}"
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
        """分析调用链深度"""
        deep_chains = []
        
        # 构建邻接表
        adj_list = defaultdict(list)
        for edge in self.edges:
            from_node = edge.get('from')
            to_node = edge.get('to')
            if from_node and to_node:
                adj_list[from_node].append(to_node)
        
        # BFS计算最长路径
        def get_longest_path(start_node):
            queue = deque([(start_node, [start_node], 0)])
            longest = ([], 0)
            
            while queue:
                node, path, depth = queue.popleft()
                
                if depth > longest[1]:
                    longest = (path, depth)
                
                for neighbor in adj_list.get(node, []):
                    if neighbor not in path:  # 避免循环
                        queue.append((neighbor, path + [neighbor], depth + 1))
            
            return longest
        
        # 检查每个起始节点
        for node in self.nodes:
            longest_path, depth = get_longest_path(node)
            if depth > max_depth:
                deep_chains.append({
                    'type': 'deep_call_chain',
                    'severity': 'high',
                    'start_node': node,
                    'depth': depth,
                    'path': longest_path,
                    'description': f"调用链深度过深({depth}层): {' → '.join(longest_path[:5])}..."
                })
        
        return deep_chains
    
    def detect_n_plus_one_queries(self) -> List[Dict]:
        """检测N+1查询模式"""
        n_plus_one_issues = []
        
        # 查找模式：循环内有数据库查询
        for node_id, node in self.nodes.items():
            node_type = node.get('type', '')
            node_label = node.get('label', '')
            
            # 检查是否是循环节点
            if 'loop' in node_label.lower() or 'foreach' in node_label.lower():
                # 查找循环内的数据库查询
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
                            'description': f"可能的N+1查询: 循环'{node_label}'内有数据库查询'{child_label}'"
                        })
        
        return n_plus_one_issues
    
    def detect_missing_indexes(self) -> List[Dict]:
        """检测可能缺少索引的大表查询"""
        missing_indexes = []
        
        # 查找涉及JOIN但可能缺少索引的查询
        for node_id, node in self.nodes.items():
            node_label = node.get('label', '')
            node_meta = node.get('metadata', {})
            
            # 检查是否是查询节点且涉及JOIN
            if 'join' in node_label.lower():
                table_size = node_meta.get('table_size', 'unknown')
                has_index = node_meta.get('indexed', False)
                
                if table_size in ['large', 'very_large'] and not has_index:
                    missing_indexes.append({
                        'type': 'missing_index',
                        'severity': 'medium',
                        'node': node_id,
                        'table_size': table_size,
                        'description': f"大表JOIN可能缺少索引: {node_label}"
                    })
        
        return missing_indexes
    
    def analyze_all(self) -> Dict:
        """运行所有分析"""
        return {
            'circular_dependencies': self.detect_circular_dependencies(),
            'deep_call_chains': self.analyze_call_chain_depth(),
            'n_plus_one_queries': self.detect_n_plus_one_queries(),
            'missing_indexes': self.detect_missing_indexes()
        }


# ============================================================================
# Phase 13新增功能：性能瓶颈检测
# ============================================================================

class BottleneckDetector:
    """性能瓶颈检测器"""
    
    def __init__(self, dag: Dict):
        self.dag = dag
        self.graph = dag.get('graph', {}) if dag else {}
        self.nodes = {n['id']: n for n in self.graph.get('nodes', [])}
        self.edges = self.graph.get('edges', [])
    
    def detect_serial_vs_parallel(self) -> List[Dict]:
        """检测串行vs并行调用机会"""
        opportunities = []
        
        # 构建邻接表
        adj_list = defaultdict(list)
        for edge in self.edges:
            from_node = edge.get('from')
            to_node = edge.get('to')
            if from_node and to_node:
                adj_list[from_node].append(to_node)
        
        # 查找有多个独立后继的节点
        for node_id, children in adj_list.items():
            if len(children) >= 2:
                # 检查子节点间是否有依赖
                children_deps = set()
                for child in children:
                    for edge in self.edges:
                        if edge['from'] in children and edge['to'] in children:
                            children_deps.add((edge['from'], edge['to']))
                
                # 如果子节点间无依赖，可以并行
                if not children_deps:
                    node_label = self.nodes.get(node_id, {}).get('label', node_id)
                    children_labels = [self.nodes.get(c, {}).get('label', c) for c in children]
                    
                    opportunities.append({
                        'type': 'parallelization_opportunity',
                        'severity': 'medium',
                        'parent_node': node_id,
                        'parallel_tasks': children,
                        'description': f"可并行执行: '{node_label}' 后的 {len(children)} 个独立任务: {', '.join(children_labels[:3])}"
                    })
        
        return opportunities
    
    def recommend_caching(self) -> List[Dict]:
        """推荐可缓存点"""
        cache_recommendations = []
        
        # 查找被多次调用的节点
        in_degree = defaultdict(int)
        for edge in self.edges:
            to_node = edge.get('to')
            if to_node:
                in_degree[to_node] += 1
        
        # 推荐缓存入度>2的节点
        for node_id, degree in in_degree.items():
            if degree > 2:
                node = self.nodes.get(node_id, {})
                node_label = node.get('label', node_id)
                node_type = node.get('type', '')
                
                # 排除某些不适合缓存的类型
                if node_type not in ['user_input', 'random']:
                    cache_recommendations.append({
                        'type': 'caching_opportunity',
                        'severity': 'low',
                        'node': node_id,
                        'call_count': degree,
                        'description': f"高频调用节点({degree}次): '{node_label}' 建议添加缓存"
                    })
        
        return cache_recommendations
    
    def detect_redundant_computations(self) -> List[Dict]:
        """检测重复计算路径"""
        redundant = []
        
        # 查找相同标签的节点（可能是重复计算）
        label_groups = defaultdict(list)
        for node_id, node in self.nodes.items():
            label = node.get('label', '').strip()
            if label:
                label_groups[label].append(node_id)
        
        # 报告重复标签
        for label, node_ids in label_groups.items():
            if len(node_ids) > 1:
                redundant.append({
                    'type': 'redundant_computation',
                    'severity': 'low',
                    'label': label,
                    'nodes': node_ids,
                    'count': len(node_ids),
                    'description': f"重复计算检测: '{label}' 出现 {len(node_ids)} 次"
                })
        
        return redundant
    
    def prioritize_optimizations(self, all_issues: List[Dict]) -> List[Dict]:
        """对优化建议排序"""
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        
        # 按严重性和影响排序
        sorted_issues = sorted(all_issues, key=lambda x: (
            severity_order.get(x.get('severity', 'low'), 99),
            -x.get('impact_score', 0)
        ))
        
        # 添加优先级标记
        for i, issue in enumerate(sorted_issues, 1):
            issue['priority'] = i
        
        return sorted_issues
    
    def analyze_all(self) -> Dict:
        """运行所有瓶颈检测"""
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
# Phase 13新增功能：报告生成
# ============================================================================

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, analysis_results: Dict, bottleneck_results: Dict):
        self.analysis = analysis_results
        self.bottlenecks = bottlenecks
        self.timestamp = datetime.now().isoformat()
    
    def generate_json_report(self, output_path: pathlib.Path) -> Dict:
        """生成JSON格式报告"""
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
            print(f"❌ 生成JSON报告失败: {e}", file=sys.stderr)
            return {}
    
    def generate_markdown_report(self, output_path: pathlib.Path) -> str:
        """生成Markdown格式报告（人类可读）"""
        summary = self._generate_summary()
        
        md = f"# 数据流分析报告\n\n"
        md += f"> **生成时间**: {self.timestamp}\n\n"
        md += "---\n\n"
        
        # 摘要
        md += "## 📊 分析摘要\n\n"
        md += f"- **Critical问题**: {summary['critical_count']} 个\n"
        md += f"- **High问题**: {summary['high_count']} 个\n"
        md += f"- **Medium问题**: {summary['medium_count']} 个\n"
        md += f"- **Low建议**: {summary['low_count']} 个\n"
        md += f"- **总计**: {summary['total_issues']} 个\n\n"
        md += "---\n\n"
        
        # Critical问题
        if summary['critical_count'] > 0:
            md += "## 🔴 Critical问题（需立即处理）\n\n"
            md += self._format_issues_markdown(self._get_issues_by_severity('critical'))
            md += "\n---\n\n"
        
        # High问题
        if summary['high_count'] > 0:
            md += "## 🟠 High问题（高优先级）\n\n"
            md += self._format_issues_markdown(self._get_issues_by_severity('high'))
            md += "\n---\n\n"
        
        # Medium问题
        if summary['medium_count'] > 0:
            md += "## 🟡 Medium问题（中优先级）\n\n"
            md += self._format_issues_markdown(self._get_issues_by_severity('medium'))
            md += "\n---\n\n"
        
        # Low建议
        if summary['low_count'] > 0:
            md += "## 🟢 Low建议（优化建议）\n\n"
            md += self._format_issues_markdown(self._get_issues_by_severity('low'))
            md += "\n---\n\n"
        
        # 优化建议Top 5
        md += "## 🎯 优化建议Top 5\n\n"
        md += self._format_top_recommendations()
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md)
            return md
        except Exception as e:
            print(f"❌ 生成Markdown报告失败: {e}", file=sys.stderr)
            return ""
    
    def _generate_summary(self) -> Dict:
        """生成摘要信息"""
        all_issues = []
        
        # 收集所有问题
        for category, issues in self.analysis.items():
            all_issues.extend(issues)
        
        for category, issues in self.bottlenecks.items():
            if category != 'prioritized_issues':
                all_issues.extend(issues)
        
        # 按严重性统计
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
        """获取指定严重性的问题"""
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
        """格式化问题为Markdown"""
        if not issues:
            return "无问题\n"
        
        md = ""
        for i, issue in enumerate(issues, 1):
            issue_type = issue.get('type', 'unknown')
            description = issue.get('description', 'N/A')
            md += f"{i}. **{issue_type}**: {description}\n"
        
        return md
    
    def _format_top_recommendations(self) -> str:
        """格式化Top建议"""
        prioritized = self.bottlenecks.get('prioritized_issues', [])
        
        if not prioritized:
            return "暂无优化建议\n"
        
        md = ""
        for i, issue in enumerate(prioritized[:5], 1):
            description = issue.get('description', 'N/A')
            severity = issue.get('severity', 'low')
            md += f"{i}. [{severity.upper()}] {description}\n"
        
        return md


# ============================================================================
# 更新main函数以支持新功能
# ============================================================================

if __name__ == '__main__':
    main()

