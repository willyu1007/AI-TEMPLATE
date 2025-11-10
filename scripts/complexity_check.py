#!/usr/bin/env python3
"""
代码复杂度检查脚本
使用简化的圈复杂度计算方法评估代码复杂度

Usage:
    python scripts/complexity_check.py [--json] [--module MODULE]
"""

import os
import sys
import json
import ast
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent


class ComplexityAnalyzer(ast.NodeVisitor):
    """AST访问器，计算函数的圈复杂度"""
    
    def __init__(self):
        self.complexity = 1  # 基础复杂度为1
    
    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_Assert(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        # and/or 操作符增加复杂度
        self.complexity += len(node.values) - 1
        self.generic_visit(node)
    
    def visit_Lambda(self, node):
        self.complexity += 1
        self.generic_visit(node)


class CodeComplexityChecker:
    """代码复杂度检查器"""
    
    def __init__(self):
        self.modules_path = REPO_ROOT / "modules"
        self.scripts_path = REPO_ROOT / "scripts"
        self.complexity_data = {}
        
        # 复杂度阈值
        self.thresholds = {
            "excellent": 10,
            "good": 15,
            "acceptable": 20,
            "warning": 30,
            "critical": 50
        }
    
    def calculate_function_complexity(self, func_node: ast.FunctionDef) -> int:
        """计算单个函数的圈复杂度"""
        analyzer = ComplexityAnalyzer()
        analyzer.visit(func_node)
        return analyzer.complexity
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """分析单个Python文件的复杂度"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            
            functions = []
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity = self.calculate_function_complexity(node)
                    functions.append({
                        "name": node.name,
                        "complexity": complexity,
                        "line": node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                    class_methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            complexity = self.calculate_function_complexity(item)
                            class_methods.append({
                                "name": item.name,
                                "complexity": complexity
                            })
                    
                    classes.append({
                        "name": node.name,
                        "methods": class_methods,
                        "line": node.lineno
                    })
            
            # 计算文件平均复杂度
            all_complexities = [f["complexity"] for f in functions]
            for cls in classes:
                all_complexities.extend([m["complexity"] for m in cls["methods"]])
            
            avg_complexity = sum(all_complexities) / len(all_complexities) if all_complexities else 0
            max_complexity = max(all_complexities) if all_complexities else 0
            
            return {
                "file": str(file_path.relative_to(REPO_ROOT)),
                "functions": functions,
                "classes": classes,
                "avg_complexity": round(avg_complexity, 1),
                "max_complexity": max_complexity,
                "line_count": len(content.splitlines())
            }
        
        except Exception as e:
            return {
                "file": str(file_path.relative_to(REPO_ROOT)),
                "error": str(e),
                "avg_complexity": 0,
                "max_complexity": 0
            }
    
    def analyze_module(self, module_name: Optional[str] = None) -> Dict[str, Any]:
        """分析模块或整个项目的复杂度"""
        files_to_analyze = []
        
        if module_name:
            # 分析特定模块
            module_path = self.modules_path / module_name
            if module_path.exists():
                files_to_analyze.extend(module_path.glob("**/*.py"))
        else:
            # 分析所有模块和脚本
            for module_dir in self.modules_path.glob("*"):
                if module_dir.is_dir():
                    files_to_analyze.extend(module_dir.glob("**/*.py"))
            files_to_analyze.extend(self.scripts_path.glob("*.py"))
        
        # 分析每个文件
        file_results = []
        for py_file in files_to_analyze:
            if "__pycache__" in str(py_file):
                continue
            result = self.analyze_file(py_file)
            file_results.append(result)
        
        # 计算总体统计
        all_avg = [f["avg_complexity"] for f in file_results if "error" not in f]
        all_max = [f["max_complexity"] for f in file_results if "error" not in f]
        
        overall_avg = sum(all_avg) / len(all_avg) if all_avg else 0
        overall_max = max(all_max) if all_max else 0
        
        # 找出高复杂度文件
        high_complexity_files = [
            f for f in file_results 
            if "error" not in f and f["avg_complexity"] > self.thresholds["acceptable"]
        ]
        
        # 找出高复杂度函数
        high_complexity_functions = []
        for file_result in file_results:
            if "error" in file_result:
                continue
            for func in file_result.get("functions", []):
                if func["complexity"] > self.thresholds["acceptable"]:
                    high_complexity_functions.append({
                        "file": file_result["file"],
                        "function": func["name"],
                        "complexity": func["complexity"],
                        "line": func["line"]
                    })
        
        return {
            "overall_avg_complexity": round(overall_avg, 1),
            "overall_max_complexity": overall_max,
            "file_count": len(file_results),
            "high_complexity_file_count": len(high_complexity_files),
            "high_complexity_function_count": len(high_complexity_functions),
            "high_complexity_files": high_complexity_files[:5],
            "high_complexity_functions": high_complexity_functions[:10],
            "status": self._get_status(overall_avg),
            "recommendations": self._get_recommendations(overall_avg, overall_max, high_complexity_functions)
        }
    
    def _get_status(self, avg_complexity: float) -> str:
        """根据平均复杂度返回状态"""
        if avg_complexity <= self.thresholds["excellent"]:
            return "⭐ Excellent"
        elif avg_complexity <= self.thresholds["good"]:
            return "✅ Good"
        elif avg_complexity <= self.thresholds["acceptable"]:
            return "⚠️ Acceptable"
        elif avg_complexity <= self.thresholds["warning"]:
            return "⚠️ Warning"
        else:
            return "❌ Critical"
    
    def _get_recommendations(self, avg: float, max_val: int, high_funcs: List[Dict]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        if avg > self.thresholds["good"]:
            recommendations.append(f"Average complexity is {avg:.1f}, consider refactoring to reduce to ≤15")
        
        if max_val > self.thresholds["warning"]:
            recommendations.append(f"Maximum complexity is {max_val}, split complex functions")
        
        if len(high_funcs) > 0:
            recommendations.append(f"Refactor {len(high_funcs)} high-complexity functions")
        
        if not recommendations:
            recommendations.append("Code complexity is well managed")
        
        return recommendations
    
    def print_report(self, report: Dict[str, Any]):
        """打印报告到控制台"""
        print("=" * 60)
        print("🔍 Code Complexity Report")
        print("=" * 60)
        print()
        
        print(f"Average Complexity: {report['overall_avg_complexity']} {report['status']}")
        print(f"Maximum Complexity: {report['overall_max_complexity']}")
        print(f"Files Analyzed: {report['file_count']}")
        print()
        
        if report['high_complexity_file_count'] > 0:
            print(f"High Complexity Files: {report['high_complexity_file_count']}")
            for file in report['high_complexity_files']:
                print(f"  - {file['file']}: avg={file['avg_complexity']}, max={file['max_complexity']}")
            print()
        
        if report['high_complexity_function_count'] > 0:
            print(f"High Complexity Functions: {report['high_complexity_function_count']}")
            for func in report['high_complexity_functions'][:5]:
                print(f"  - {func['file']}:{func['line']} {func['function']}() = {func['complexity']}")
            if report['high_complexity_function_count'] > 5:
                print(f"  ... and {report['high_complexity_function_count'] - 5} more")
            print()
        
        print("Recommendations:")
        for rec in report['recommendations']:
            print(f"  • {rec}")
        
        print()
        print("=" * 60)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Code Complexity Checker")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--module", type=str, help="Check specific module")
    args = parser.parse_args()
    
    checker = CodeComplexityChecker()
    report = checker.analyze_module(args.module)
    
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        checker.print_report(report)
    
    # 返回状态码
    if report['overall_avg_complexity'] > 30:
        return 1  # 失败
    return 0  # 成功


if __name__ == "__main__":
    sys.exit(main())
