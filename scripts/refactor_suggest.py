#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refactor_suggest.py - 


1. 
2. 
3. 
4. 


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

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent


@dataclass
class RefactorSuggestion:
    """"""
    pattern: str            # 
    description: str        # 
    priority: str          #  (high/medium/low)
    example: Optional[str] = None  # 


@dataclass
class FunctionAnalysis:
    """"""
    file_path: str          # 
    function_name: str      # 
    line_number: int        # 
    complexity: int         # 
    lines_of_code: int      # 
    parameters: int         # 
    nested_depth: int       # 
    issues: List[str] = field(default_factory=list)  # 
    suggestions: List[RefactorSuggestion] = field(default_factory=list)  # 


class RefactorAnalyzer(ast.NodeVisitor):
    """"""
    
    def __init__(self, threshold: int = 15):
        """"""
        self.threshold = threshold
        self.current_file = ""
        self.analyses: List[FunctionAnalysis] = []
        self.current_depth = 0
        self.max_depth = 0
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """"""
        # 
        complexity = self._calculate_complexity(node)
        
        if complexity >= self.threshold:
            # 
            analysis = self._analyze_function(node, complexity)
            
            # 
            self._generate_suggestions(analysis)
            
            self.analyses.append(analysis)
        
        self.generic_visit(node)
    
    visit_AsyncFunctionDef = visit_FunctionDef
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """"""
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
        """"""
        # 
        lines_of_code = node.end_lineno - node.lineno + 1 if node.end_lineno else 0
        
        # 
        parameters = len(node.args.args) + len(node.args.kwonlyargs)
        if node.args.vararg:
            parameters += 1
        if node.args.kwarg:
            parameters += 1
        
        # 
        nested_depth = self._calculate_nested_depth(node)
        
        # 
        analysis = FunctionAnalysis(
            file_path=self.current_file,
            function_name=node.name,
            line_number=node.lineno,
            complexity=complexity,
            lines_of_code=lines_of_code,
            parameters=parameters,
            nested_depth=nested_depth
        )
        
        # 
        self._detect_issues(node, analysis)
        
        return analysis
    
    def _calculate_nested_depth(self, node: ast.FunctionDef) -> int:
        """"""
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
        """"""
        # 
        if analysis.complexity > 20:
            analysis.issues.append(f": {analysis.complexity}")
        elif analysis.complexity > 15:
            analysis.issues.append(f": {analysis.complexity}")
        
        # 
        if analysis.lines_of_code > 100:
            analysis.issues.append(f": {analysis.lines_of_code}")
        elif analysis.lines_of_code > 50:
            analysis.issues.append(f": {analysis.lines_of_code}")
        
        # 
        if analysis.parameters > 7:
            analysis.issues.append(f": {analysis.parameters}")
        elif analysis.parameters > 5:
            analysis.issues.append(f": {analysis.parameters}")
        
        # 
        if analysis.nested_depth > 4:
            analysis.issues.append(f": {analysis.nested_depth}")
        elif analysis.nested_depth > 3:
            analysis.issues.append(f": {analysis.nested_depth}")
    
    def _generate_suggestions(self, analysis: FunctionAnalysis):
        """"""
        # 
        if analysis.complexity > 20:
            analysis.suggestions.append(RefactorSuggestion(
                pattern="Extract Method",
                description="",
                priority="high",
                example=textwrap.dedent("""
                    # Before:
                    def process_data(data):
                        # A (10)
                        # B (15)
                        # C (20)
                    
                    # After:
                    def process_data(data):
                        data = _preprocess(data)
                        data = _transform(data)
                        return _postprocess(data)
                """)
            ))
        
        # 
        if analysis.lines_of_code > 50:
            analysis.suggestions.append(RefactorSuggestion(
                pattern="Split Responsibilities",
                description="",
                priority="high" if analysis.lines_of_code > 100 else "medium"
            ))
        
        # 
        if analysis.parameters > 5:
            analysis.suggestions.append(RefactorSuggestion(
                pattern="Parameter Object",
                description="",
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
        
        # 
        if analysis.nested_depth > 3:
            analysis.suggestions.append(RefactorSuggestion(
                pattern="Guard Clause",
                description="",
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
        
        # 
        if analysis.complexity > 10:
            analysis.suggestions.append(RefactorSuggestion(
                pattern="Strategy Pattern",
                description="",
                priority="low"
            ))


def analyze_file(file_path: Path, threshold: int = 15) -> List[FunctionAnalysis]:
    """Python"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=str(file_path))
        analyzer = RefactorAnalyzer(threshold)
        analyzer.current_file = str(file_path.relative_to(REPO_ROOT))
        analyzer.visit(tree)
        
        return analyzer.analyses
    
    except Exception as e:
        print(f"❌  {file_path}: {e}", file=sys.stderr)
        return []


def analyze_directory(directory: Path, threshold: int = 15) -> List[FunctionAnalysis]:
    """Python"""
    all_analyses = []
    
    for py_file in directory.rglob("*.py"):
        # 
        if any(part in py_file.parts for part in [
            "__pycache__", "venv", "node_modules", ".git", "build", "dist"
        ]):
            continue
        
        analyses = analyze_file(py_file, threshold)
        all_analyses.extend(analyses)
    
    return all_analyses


def print_analysis_report(analyses: List[FunctionAnalysis]):
    """"""
    if not analyses:
        print("✅ ")
        return
    
    print("=" * 80)
    print("🔧 ")
    print("=" * 80)
    print(f"\n {len(analyses)} \n")
    
    # 
    analyses.sort(key=lambda x: (-x.complexity, -x.lines_of_code))
    
    for i, analysis in enumerate(analyses, 1):
        print(f"{i}. {analysis.file_path}:{analysis.line_number}")
        print(f"   : {analysis.function_name}()")
        print(f"   : {analysis.complexity} | : {analysis.lines_of_code} | "
              f": {analysis.parameters} | : {analysis.nested_depth}")
        
        if analysis.issues:
            print("   :")
            for issue in analysis.issues:
                print(f"     - {issue}")
        
        if analysis.suggestions:
            print("   :")
            for suggestion in analysis.suggestions:
                print(f"     ⭐ [{suggestion.priority.upper()}] {suggestion.pattern}")
                print(f"        {suggestion.description}")
                if suggestion.example:
                    print("        :")
                    for line in suggestion.example.strip().split('\n'):
                        print(f"          {line}")
        
        print()
    
    # 
    print("-" * 80)
    print("📊 ")
    print(f"   : {len(analyses)}")
    print(f"   : {sum(a.complexity for a in analyses) / len(analyses):.1f}")
    print(f"   : {max(a.complexity for a in analyses)}")
    print(f"   : {sum(1 for a in analyses if a.complexity > 20)}")
    print("=" * 80)


def generate_refactor_plan(analyses: List[FunctionAnalysis]) -> str:
    """"""
    plan = []
    plan.append("# \n")
    plan.append(f": {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    plan.append(f": {len(analyses)}\n")
    
    # P0 - 
    p0 = [a for a in analyses if a.complexity > 25 or a.lines_of_code > 100]
    if p0:
        plan.append("\n## P0 - \n")
        for a in p0:
            plan.append(f"- [ ] {a.file_path}:{a.function_name} (:{a.complexity})")
    
    # P1 - 
    p1 = [a for a in analyses if 20 <= a.complexity <= 25 or 70 <= a.lines_of_code <= 100]
    if p1:
        plan.append("\n## P1 - \n")
        for a in p1:
            plan.append(f"- [ ] {a.file_path}:{a.function_name} (:{a.complexity})")
    
    # P2 - 
    p2 = [a for a in analyses if a.complexity < 20 and a.lines_of_code < 70]
    if p2:
        plan.append("\n## P2 - \n")
        for a in p2[:10]:  # 10
            plan.append(f"- [ ] {a.file_path}:{a.function_name} (:{a.complexity})")
        if len(p2) > 10:
            plan.append(f"... {len(p2)-10}")
    
    return "\n".join(plan)


def main():
    """"""
    import argparse
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--file', '-f',
        type=str,
        help=''
    )
    parser.add_argument(
        '--directory', '-d',
        type=str,
        default=str(REPO_ROOT / "scripts"),
        help=': scripts/'
    )
    parser.add_argument(
        '--complexity', '-c',
        type=int,
        default=15,
        help=': 15'
    )
    parser.add_argument(
        '--output-plan',
        action='store_true',
        help=''
    )
    
    args = parser.parse_args()
    
    # 
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ : {file_path}", file=sys.stderr)
            return 1
        analyses = analyze_file(file_path, args.complexity)
    else:
        directory = Path(args.directory)
        if not directory.exists():
            print(f"❌ : {directory}", file=sys.stderr)
            return 1
        analyses = analyze_directory(directory, args.complexity)
    
    # 
    print_analysis_report(analyses)
    
    # 
    if args.output_plan and analyses:
        plan = generate_refactor_plan(analyses)
        plan_file = REPO_ROOT / "REFACTOR_PLAN.md"
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(plan)
        print(f"\n✅ : {plan_file}")
    
    return 0 if not analyses else 1


if __name__ == '__main__':
    sys.exit(main())
