#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 13
DAGMermaidGraphviz DOTD3.js HTML
"""

import sys
import pathlib
import yaml
import json
from typing import Dict, List, Optional
from datetime import datetime

# Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class DataflowVisualizer:
    """"""
    
    def __init__(self, dag_path: str = 'doc/flows/dag.yaml'):
        """"""
        self.dag_path = pathlib.Path(dag_path)
        self.dag = self._load_dag()
        self.graph = self.dag.get('graph', {}) if self.dag else {}
        self.nodes = {n['id']: n for n in self.graph.get('nodes', [])}
        self.edges = self.graph.get('edges', [])
    
    def _load_dag(self) -> Dict:
        """DAG"""
        try:
            with open(self.dag_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"❌ DAG: {e}", file=sys.stderr)
            return {}
    
    def generate_mermaid(self) -> str:
        """Mermaid"""
        if not self.nodes:
            return "graph TD\n  Start[]\n"
        
        mermaid = "graph TD\n"
        
        # 
        for node_id, node in self.nodes.items():
            label = node.get('label', node_id)
            node_type = node.get('type', 'default')
            
            # 
            if node_type == 'start':
                shape = f"({label})"
            elif node_type == 'end':
                shape = f"([{label}])"
            elif node_type == 'decision':
                shape = f"{{{label}}}"
            elif node_type == 'database':
                shape = f"[({{label}})]"
            else:
                shape = f"[{label}]"
            
            mermaid += f"  {node_id}{shape}\n"
        
        # 
        for edge in self.edges:
            from_node = edge.get('from')
            to_node = edge.get('to')
            label = edge.get('label', '')
            
            if from_node and to_node:
                if label:
                    mermaid += f"  {from_node} -->|{label}| {to_node}\n"
                else:
                    mermaid += f"  {from_node} --> {to_node}\n"
        
        return mermaid
    
    def generate_graphviz_dot(self) -> str:
        """Graphviz DOT"""
        if not self.nodes:
            return 'digraph G {\n  Start [label=""];\n}\n'
        
        dot = 'digraph DataFlow {\n'
        dot += '  // \n'
        dot += '  rankdir=TB;\n'
        dot += '  node [fontname="SimHei", fontsize=12];\n'
        dot += '  edge [fontname="SimHei", fontsize=10];\n\n'
        
        # 
        dot += '  // \n'
        for node_id, node in self.nodes.items():
            label = node.get('label', node_id)
            node_type = node.get('type', 'default')
            
            # 
            if node_type == 'start':
                attrs = 'shape=circle, style=filled, fillcolor=lightgreen'
            elif node_type == 'end':
                attrs = 'shape=doublecircle, style=filled, fillcolor=lightcoral'
            elif node_type == 'decision':
                attrs = 'shape=diamond, style=filled, fillcolor=lightyellow'
            elif node_type == 'database':
                attrs = 'shape=cylinder, style=filled, fillcolor=lightblue'
            elif node_type == 'process':
                attrs = 'shape=box, style="rounded,filled", fillcolor=lightgray'
            else:
                attrs = 'shape=box'
            
            dot += f'  {node_id} [label="{label}", {attrs}];\n'
        
        # 
        dot += '\n  // \n'
        for edge in self.edges:
            from_node = edge.get('from')
            to_node = edge.get('to')
            label = edge.get('label', '')
            edge_type = edge.get('type', 'normal')
            
            if from_node and to_node:
                # 
                if edge_type == 'critical':
                    style = 'color=red, penwidth=2'
                elif edge_type == 'async':
                    style = 'style=dashed'
                else:
                    style = ''
                
                if label:
                    dot += f'  {from_node} -> {to_node} [label="{label}", {style}];\n'
                else:
                    dot += f'  {from_node} -> {to_node} [{style}];\n'
        
        dot += '}\n'
        return dot
    
    def generate_d3_html(self, title: str = "", 
                        include_analysis: Optional[Dict] = None) -> str:
        """D3.jsHTML"""
        
        # 
        nodes_data = []
        for node_id, node in self.nodes.items():
            nodes_data.append({
                'id': node_id,
                'label': node.get('label', node_id),
                'type': node.get('type', 'default'),
                'group': node.get('group', 1)
            })
        
        edges_data = []
        for edge in self.edges:
            edges_data.append({
                'source': edge.get('from'),
                'target': edge.get('to'),
                'label': edge.get('label', ''),
                'type': edge.get('type', 'normal')
            })
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{
            font-family: "Microsoft YaHei", "SimHei", sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 20px;
        }}
        h1 {{
            margin: 0 0 20px 0;
            color: #333;
        }}
        .metadata {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }}
        #graph {{
            width: 100%;
            height: 600px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: #fff;
        }}
        .controls {{
            margin-top: 20px;
            display: flex;
            gap: 10px;
        }}
        button {{
            padding: 8px 16px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 4px;
            cursor: pointer;
        }}
        button:hover {{
            background: #f0f0f0;
        }}
        .node {{
            cursor: pointer;
        }}
        .node circle {{
            stroke: #fff;
            stroke-width: 2px;
        }}
        .node text {{
            font-size: 12px;
            pointer-events: none;
        }}
        .link {{
            stroke: #999;
            stroke-opacity: 0.6;
        }}
        .link-label {{
            font-size: 10px;
            fill: #666;
        }}
        .tooltip {{
            position: absolute;
            padding: 8px 12px;
            background: rgba(0,0,0,0.8);
            color: white;
            border-radius: 4px;
            font-size: 12px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
        }}
        .analysis-panel {{
            margin-top: 20px;
            padding: 15px;
            background: #fff3cd;
            border-radius: 4px;
        }}
        .issue-critical {{ color: #d32f2f; }}
        .issue-high {{ color: #f57c00; }}
        .issue-medium {{ color: #fbc02d; }}
        .issue-low {{ color: #388e3c; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        
        <div class="metadata">
            <strong>:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            <strong>:</strong> {len(self.nodes)}  | 
            <strong>:</strong> {len(self.edges)} 
        </div>
        
        <div id="graph"></div>
        
        <div class="controls">
            <button onclick="resetZoom()"></button>
            <button onclick="exportSVG()">SVG</button>
            <button onclick="exportPNG()">PNG</button>
        </div>
        
        {'<div class="analysis-panel"><h3>⚠️ </h3>' + self._render_analysis_html(include_analysis) + '</div>' if include_analysis else ''}
    </div>
    
    <div class="tooltip" id="tooltip"></div>
    
    <script>
        // 
        const nodesData = {json.dumps(nodes_data, ensure_ascii=False)};
        const linksData = {json.dumps(edges_data, ensure_ascii=False)};
        
        // SVG
        const width = document.getElementById('graph').clientWidth;
        const height = 600;
        
        const svg = d3.select("#graph")
            .append("svg")
            .attr("width", width)
            .attr("height", height);
        
        const g = svg.append("g");
        
        // 
        const zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on("zoom", (event) => g.attr("transform", event.transform));
        
        svg.call(zoom);
        
        // 
        const simulation = d3.forceSimulation(nodesData)
            .force("link", d3.forceLink(linksData).id(d => d.id).distance(150))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2));
        
        // 
        const link = g.append("g")
            .selectAll("line")
            .data(linksData)
            .enter().append("line")
            .attr("class", "link")
            .attr("stroke-width", d => d.type === 'critical' ? 3 : 1);
        
        // 
        const linkLabel = g.append("g")
            .selectAll("text")
            .data(linksData)
            .enter().append("text")
            .attr("class", "link-label")
            .text(d => d.label);
        
        // 
        const node = g.append("g")
            .selectAll("g")
            .data(nodesData)
            .enter().append("g")
            .attr("class", "node")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
        
        // 
        node.append("circle")
            .attr("r", 20)
            .attr("fill", d => getNodeColor(d.type));
        
        // 
        node.append("text")
            .attr("dy", -25)
            .attr("text-anchor", "middle")
            .text(d => d.label);
        
        // 
        node.on("mouseover", showTooltip)
            .on("mouseout", hideTooltip);
        
        // 
        simulation.on("tick", () => {{
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            
            linkLabel
                .attr("x", d => (d.source.x + d.target.x) / 2)
                .attr("y", d => (d.source.y + d.target.y) / 2);
            
            node.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
        }});
        
        // 
        function getNodeColor(type) {{
            const colors = {{
                'start': '#4caf50',
                'end': '#f44336',
                'decision': '#ffeb3b',
                'database': '#2196f3',
                'process': '#9e9e9e',
                'default': '#bdbdbd'
            }};
            return colors[type] || colors['default'];
        }}
        
        function showTooltip(event, d) {{
            const tooltip = d3.select("#tooltip");
            tooltip.style("opacity", 1)
                .html(`<strong>${{d.label}}</strong><br>: ${{d.type}}`)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 28) + "px");
        }}
        
        function hideTooltip() {{
            d3.select("#tooltip").style("opacity", 0);
        }}
        
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}
        
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
        
        function resetZoom() {{
            svg.transition().duration(750).call(zoom.transform, d3.zoomIdentity);
        }}
        
        function exportSVG() {{
            const svgData = svg.node().outerHTML;
            const blob = new Blob([svgData], {{type: 'image/svg+xml'}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'dataflow.svg';
            a.click();
        }}
        
        function exportPNG() {{
            alert('PNG');
        }}
    </script>
</body>
</html>'''
        
        return html
    
    def _render_analysis_html(self, analysis: Optional[Dict]) -> str:
        """HTML"""
        if not analysis:
            return "<p></p>"
        
        html = ""
        
        # Critical
        critical = analysis.get('critical_issues', [])
        if critical:
            html += "<h4 class='issue-critical'>🔴 Critical</h4><ul>"
            for issue in critical[:5]:
                html += f"<li>{issue.get('description', 'N/A')}</li>"
            html += "</ul>"
        
        # High
        high = analysis.get('high_issues', [])
        if high:
            html += "<h4 class='issue-high'>🟠 High</h4><ul>"
            for issue in high[:5]:
                html += f"<li>{issue.get('description', 'N/A')}</li>"
            html += "</ul>"
        
        return html if html else "<p>✅ </p>"
    
    def save_visualization(self, format_type: str, output_path: str, 
                          include_analysis: Optional[Dict] = None) -> bool:
        """"""
        try:
            output_file = pathlib.Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            if format_type == 'mermaid':
                content = self.generate_mermaid()
            elif format_type == 'dot':
                content = self.generate_graphviz_dot()
            elif format_type == 'html':
                content = self.generate_d3_html(include_analysis=include_analysis)
            else:
                print(f"❌ : {format_type}", file=sys.stderr)
                return False
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ : {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ : {e}", file=sys.stderr)
            return False


def main():
    """"""
    import argparse
    
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--dag', type=str, default='doc/flows/dag.yaml', help='DAG')
    parser.add_argument('--format', type=str, choices=['mermaid', 'dot', 'html'], 
                       default='mermaid', help='')
    parser.add_argument('--output', '-o', type=str, help='')
    parser.add_argument('--analysis', type=str, help='JSON')
    
    args = parser.parse_args()
    
    # 
    visualizer = DataflowVisualizer(args.dag)
    
    if not visualizer.nodes:
        print("❌ DAGDAG", file=sys.stderr)
        sys.exit(1)
    
    # 
    analysis_data = None
    if args.analysis:
        try:
            with open(args.analysis, 'r', encoding='utf-8') as f:
                analysis_data = json.load(f)
        except Exception as e:
            print(f"⚠️ : {e}", file=sys.stderr)
    
    # 
    if args.output:
        visualizer.save_visualization(args.format, args.output, analysis_data)
    else:
        # 
        if args.format == 'mermaid':
            print(visualizer.generate_mermaid())
        elif args.format == 'dot':
            print(visualizer.generate_graphviz_dot())
        elif args.format == 'html':
            print(visualizer.generate_d3_html(include_analysis=analysis_data))


if __name__ == '__main__':
    main()

