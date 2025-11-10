#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refactor_suggest.py - 代码重构建议工具

功能：
1. 分析高复杂度函数
2. 提供重构建议和模式
3. 生成重构计划
4. 支持自动化简单重构

用法：
    python scripts/refactor_suggest.py
    python scripts/refactor_suggest.py --file <path>
    python scripts/refactor_suggest.py --complexity 15
    make refactor_suggest

Created: 2025-11-09
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
import textwrap

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent


@dataclass
class RefactorSuggestion:
    """重构建议"""
    pattern: str            # 重构模式名称
    description: str        # 建议描述
    priority: str          # 优先级 (high/medium/low)
    example: Optional[str] = None  # 示例代码


@dataclass
class FunctionAnalysis:
    """函数分析结果"""
    file_path: str          # 文件路径
    function_name: str      # 函数名
    line_number: int        # 行号
    complexity: int         # 复杂度
    lines_of_code: int      # 代码行数
    parameters: int         # 参数数量
    nested_depth: int       # 最大嵌套深度
    issues: List[str] = field(default_factory=list)  # 发现的问题
    suggestions: List[RefactorSuggestion] = field(default_factory=list)  # 重构建议


class RefactorAnalyzer(ast.NodeVisitor):
    """代码重构分析器"""
    
    def __init__(self, threshold: int = 15):
        """初始化分析器"""
        self.threshold = threshold
        self.current_file = ""
        self.analyses: List[FunctionAnalysis] = []
        self.current_depth = 0
        self.max_depth = 0
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """访问函数定义"""
        # 计算复杂度
        complexity = self._calculate_complexity(node)
        
        if complexity >= self.threshold:
            # 分析函数
            analysis = self._analyze_function(node, complexity)
            
            # 生成建议
            self._generate_suggestions(analysis)
            
            self.analyses.append(analysis)
        
        self.generic_visit(node)
    
    visit_AsyncFunctionDef = visit_FunctionDef
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """计算圈复杂度"""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor,
                                ast.ExceptHandler, ast.With, ast.AsyncWith,
                                ast.Assert, ast.comprehension)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _analyze_function(self, node: ast.FunctionDef, complexity: int) -> FunctionAnalysis:
        """分析函数详情"""
        # 计算代码行数
        lines_of_code = node.end_lineno - node.lineno + 1 if node.end_lineno else 0
        
        # 计算参数数量
        parameters = len(node.args.args) + len(node.args.kwonlyargs)
        if node.args.vararg:
            parameters += 1
        if node.args.kwarg:
            parameters += 1
        
        # 计算嵌套深度
        nested_depth = self._calculate_nested_depth(node)
        
        # 创建分析结果
        analysis = FunctionAnalysis(
            file_path=self.current_file,
            function_name=node.name,
            line_number=node.lineno,
            complexity=complexity,
            lines_of_code=lines_of_code,
            parameters=parameters,
            nested_depth=nested_depth
        )
        
        # 检测问题
        self._detect_issues(node, analysis)
        
        return analysis
    
    def _calculate_nested_depth(self, node: ast.FunctionDef) -> int:
        """计算最大嵌套深度"""
        max_depth = 0
        
        def calculate_depth(node, depth=0):
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                    calculate_depth(child, depth + 1)
                else:
                    calculate_depth(child, depth)
        
        calculate_depth(node)
        return max_depth
    
    def _detect_issues(self, node: ast.FunctionDef, analysis: FunctionAnalysis):
        """检测代码问题"""
        # 复杂度过高
        if analysis.complexity > 20:
            analysis.issues.append(f"极高复杂度: {analysis.complexity}")
        elif analysis.complexity > 15:
            analysis.issues.append(f"高复杂度: {analysis.complexity}")
        
        # 函数过长
        if analysis.lines_of_code > 100:
            analysis.issues.append(f"函数过长: {analysis.lines_of_code}行")
        elif analysis.lines_of_code > 50:
            analysis.issues.append(f"函数较长: {analysis.lines_of_code}行")
        
        # 参数过多
        if analysis.parameters > 7:
            analysis.issues.append(f"参数过多: {analysis.parameters}个")
        elif analysis.parameters > 5:
            analysis.issues.append(f"参数较多: {analysis.parameters}个")
        
        # 嵌套过深
        if analysis.nested_depth > 4:
            analysis.issues.append(f"嵌套过深: {analysis.nested_depth}层")
        elif analysis.nested_depth > 3:
            analysis.issues.append(f"嵌套较深: {analysis.nested_depth}层")
    
    def _generate_suggestions(self, analysis: FunctionAnalysis):
        """生成重构建议"""
        # 基于复杂度的建议
        if analysis.complexity > 20:
            analysis.suggestions.append(RefactorSuggestion(
                pattern="Extract Method",
                description="将复杂逻辑拆分为多个小函数",
                priority="high",
                example=textwrap.dedent("""
                    # Before:
                    def process_data(data):
                        # 复杂逻辑A (10行)
                        # 复杂逻辑B (15行)
                        # 复杂逻辑C (20行)
                    
                    # After:
                    def process_data(data):
                        data = _preprocess(data)
                        data = _transform(data)
                        return _postprocess(data)
                """)
            ))
        
        # 基于代码行数的建议
        if analysis.lines_of_code > 50:
            analysis.suggestions.append(RefactorSuggestion(
                pattern="Split Responsibilities",
                description="根据单一职责原则拆分函数",
                priority="high" if analysis.lines_of_code > 100 else "medium"
            ))
        
        # 基于参数数量的建议
        if analysis.parameters > 5:
            analysis.suggestions.append(RefactorSuggestion(
                pattern="Parameter Object",
                description="使用参数对象或配置类封装参数",
                priority="medium",
                example=textwrap.dedent("""
                    # Before:
                    def create_user(name, email, age, address, phone, role):
                        pass
                    
                    # After:
                    @dataclass
                    class UserInfo:
                        name: str
                        email: str
                        age: int
                        address: str
                        phone: str
                        role: str
                    
                    def create_user(user_info: UserInfo):
                        pass
                """)
            ))
        
        # 基于嵌套深度的建议
        if analysis.nested_depth > 3:
            analysis.suggestions.append(RefactorSuggestion(
                pattern="Guard Clause",
                description="使用卫语句减少嵌套",
                priority="medium",
                example=textwrap.dedent("""
                    # Before:
                    def process(data):
                        if data:
                            if validate(data):
                                if check(data):
                                    return transform(data)
                    
                    # After:
                    def process(data):
                        if not data:
                            return None
                        if not validate(data):
                            return None
                        if not check(data):
                            return None
                        return transform(data)
                """)
            ))
        
        # 通用建议
        if analysis.complexity > 10:
            analysis.suggestions.append(RefactorSuggestion(
                pattern="Strategy Pattern",
                description="考虑使用策略模式处理复杂条件分支",
                priority="low"
            ))


def analyze_file(file_path: Path, threshold: int = 15) -> List[FunctionAnalysis]:
    """分析单个Python文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=str(file_path))
        analyzer = RefactorAnalyzer(threshold)
        analyzer.current_file = str(file_path.relative_to(REPO_ROOT))
        analyzer.visit(tree)
        
        return analyzer.analyses
    
    except Exception as e:
        print(f"❌ 分析文件失败 {file_path}: {e}", file=sys.stderr)
        return []


def analyze_directory(directory: Path, threshold: int = 15) -> List[FunctionAnalysis]:
    """分析目录中的所有Python文件"""
    all_analyses = []
    
    for py_file in directory.rglob("*.py"):
        # 跳过测试文件和特定目录
        if any(part in py_file.parts for part in [
            "__pycache__", "venv", "node_modules", ".git", "build", "dist"
        ]):
            continue
        
        analyses = analyze_file(py_file, threshold)
        all_analyses.extend(analyses)
    
    return all_analyses


def print_analysis_report(analyses: List[FunctionAnalysis]):
    """打印分析报告"""
    if not analyses:
        print("✅ 未发现需要重构的函数")
        return
    
    print("=" * 80)
    print("🔧 代码重构建议报告")
    print("=" * 80)
    print(f"\n发现 {len(analyses)} 个需要重构的函数\n")
    
    # 按优先级排序
    analyses.sort(key=lambda x: (-x.complexity, -x.lines_of_code))
    
    for i, analysis in enumerate(analyses, 1):
        print(f"{i}. {analysis.file_path}:{analysis.line_number}")
        print(f"   函数: {analysis.function_name}()")
        print(f"   复杂度: {analysis.complexity} | 代码行: {analysis.lines_of_code} | "
              f"参数: {analysis.parameters} | 嵌套: {analysis.nested_depth}")
        
        if analysis.issues:
            print("   问题:")
            for issue in analysis.issues:
                print(f"     - {issue}")
        
        if analysis.suggestions:
            print("   建议:")
            for suggestion in analysis.suggestions:
                print(f"     ⭐ [{suggestion.priority.upper()}] {suggestion.pattern}")
                print(f"        {suggestion.description}")
                if suggestion.example:
                    print("        示例:")
                    for line in suggestion.example.strip().split('\n'):
                        print(f"          {line}")
        
        print()
    
    # 汇总统计
    print("-" * 80)
    print("📊 汇总统计")
    print(f"   总函数数: {len(analyses)}")
    print(f"   平均复杂度: {sum(a.complexity for a in analyses) / len(analyses):.1f}")
    print(f"   最高复杂度: {max(a.complexity for a in analyses)}")
    print(f"   需要优先重构: {sum(1 for a in analyses if a.complexity > 20)}个")
    print("=" * 80)


def generate_refactor_plan(analyses: List[FunctionAnalysis]) -> str:
    """生成重构计划"""
    plan = []
    plan.append("# 代码重构计划\n")
    plan.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    plan.append(f"需重构函数: {len(analyses)}个\n")
    
    # P0 - 紧急
    p0 = [a for a in analyses if a.complexity > 25 or a.lines_of_code > 100]
    if p0:
        plan.append("\n## P0 - 紧急重构\n")
        for a in p0:
            plan.append(f"- [ ] {a.file_path}:{a.function_name} (复杂度:{a.complexity})")
    
    # P1 - 重要
    p1 = [a for a in analyses if 20 <= a.complexity <= 25 or 70 <= a.lines_of_code <= 100]
    if p1:
        plan.append("\n## P1 - 重要重构\n")
        for a in p1:
            plan.append(f"- [ ] {a.file_path}:{a.function_name} (复杂度:{a.complexity})")
    
    # P2 - 一般
    p2 = [a for a in analyses if a.complexity < 20 and a.lines_of_code < 70]
    if p2:
        plan.append("\n## P2 - 一般优化\n")
        for a in p2[:10]:  # 只显示前10个
            plan.append(f"- [ ] {a.file_path}:{a.function_name} (复杂度:{a.complexity})")
        if len(p2) > 10:
            plan.append(f"... 还有{len(p2)-10}个函数")
    
    return "\n".join(plan)


def main():
    """主函数"""
    import argparse
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description='代码重构建议工具')
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='分析指定文件'
    )
    parser.add_argument(
        '--directory', '-d',
        type=str,
        default=str(REPO_ROOT / "scripts"),
        help='分析指定目录（默认: scripts/）'
    )
    parser.add_argument(
        '--complexity', '-c',
        type=int,
        default=15,
        help='复杂度阈值（默认: 15）'
    )
    parser.add_argument(
        '--output-plan',
        action='store_true',
        help='生成重构计划文件'
    )
    
    args = parser.parse_args()
    
    # 执行分析
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ 文件不存在: {file_path}", file=sys.stderr)
            return 1
        analyses = analyze_file(file_path, args.complexity)
    else:
        directory = Path(args.directory)
        if not directory.exists():
            print(f"❌ 目录不存在: {directory}", file=sys.stderr)
            return 1
        analyses = analyze_directory(directory, args.complexity)
    
    # 打印报告
    print_analysis_report(analyses)
    
    # 生成重构计划
    if args.output_plan and analyses:
        plan = generate_refactor_plan(analyses)
        plan_file = REPO_ROOT / "REFACTOR_PLAN.md"
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(plan)
        print(f"\n✅ 重构计划已生成: {plan_file}")
    
    return 0 if not analyses else 1


if __name__ == '__main__':
    sys.exit(main())
