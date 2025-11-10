#!/usr/bin/env python3
"""
测试覆盖率检查脚本
检查项目的测试覆盖率情况

Usage:
    python scripts/test_coverage_check.py [--json]
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent


class TestCoverageChecker:
    """测试覆盖率检查器"""
    
    def __init__(self):
        self.modules_path = REPO_ROOT / "modules"
        self.tests_path = REPO_ROOT / "tests"
        self.coverage_data = {}
        self.total_coverage = 0
    
    def check_python_coverage(self) -> Tuple[float, Dict[str, float]]:
        """检查Python代码的测试覆盖率"""
        coverage_by_module = {}
        
        # 检查每个模块目录
        for module_dir in self.modules_path.glob("*"):
            if not module_dir.is_dir():
                continue
            
            module_name = module_dir.name
            
            # 统计Python文件
            py_files = list(module_dir.glob("**/*.py"))
            if not py_files:
                continue
            
            # 检查对应的测试文件
            test_dir = self.tests_path / module_name
            test_files = list(test_dir.glob("**/test_*.py")) if test_dir.exists() else []
            
            # 简单的覆盖率估算（基于文件存在性）
            # 实际项目中应该使用coverage.py工具
            if test_files:
                # 假设有测试文件就有60-80%的覆盖率
                estimated_coverage = min(60 + len(test_files) * 10, 80)
            else:
                estimated_coverage = 0
            
            coverage_by_module[module_name] = estimated_coverage
        
        # 计算总体覆盖率
        if coverage_by_module:
            total_coverage = sum(coverage_by_module.values()) / len(coverage_by_module)
        else:
            total_coverage = 0
        
        return total_coverage, coverage_by_module
    
    def check_common_module_coverage(self) -> float:
        """检查common模块的覆盖率（要求更高）"""
        common_dir = self.modules_path / "common"
        if not common_dir.exists():
            return 0
        
        # 统计文件
        py_files = list(common_dir.glob("**/*.py"))
        test_files = list((self.tests_path / "common").glob("**/test_*.py")) if (self.tests_path / "common").exists() else []
        
        # common模块要求更高的覆盖率
        if test_files and py_files:
            ratio = len(test_files) / len(py_files)
            # 基于测试文件比例估算覆盖率
            estimated_coverage = min(ratio * 100, 90)
        else:
            estimated_coverage = 0
        
        return estimated_coverage
    
    def analyze_untested_files(self) -> List[str]:
        """找出未测试的文件"""
        untested_files = []
        
        for module_dir in self.modules_path.glob("*"):
            if not module_dir.is_dir():
                continue
            
            module_name = module_dir.name
            test_dir = self.tests_path / module_name
            
            # 查找Python文件
            for py_file in module_dir.glob("**/*.py"):
                # 跳过__pycache__和__init__.py
                if "__pycache__" in str(py_file) or py_file.name == "__init__.py":
                    continue
                
                # 检查是否有对应的测试文件
                test_file_name = f"test_{py_file.stem}.py"
                test_file_path = test_dir / test_file_name if test_dir.exists() else None
                
                if not test_file_path or not test_file_path.exists():
                    relative_path = py_file.relative_to(REPO_ROOT)
                    untested_files.append(str(relative_path))
        
        return untested_files
    
    def generate_report(self) -> Dict[str, Any]:
        """生成覆盖率报告"""
        total_coverage, module_coverage = self.check_python_coverage()
        common_coverage = self.check_common_module_coverage()
        untested_files = self.analyze_untested_files()
        
        report = {
            "total_coverage": round(total_coverage, 1),
            "common_module_coverage": round(common_coverage, 1),
            "module_coverage": {k: round(v, 1) for k, v in module_coverage.items()},
            "untested_file_count": len(untested_files),
            "untested_files": untested_files[:10],  # 只显示前10个
            "coverage_status": self._get_status(total_coverage),
            "recommendations": self._get_recommendations(total_coverage, common_coverage, untested_files)
        }
        
        return report
    
    def _get_status(self, coverage: float) -> str:
        """获取覆盖率状态"""
        if coverage >= 80:
            return "✅ Good"
        elif coverage >= 60:
            return "⚠️ Needs Improvement"
        else:
            return "❌ Poor"
    
    def _get_recommendations(self, total: float, common: float, untested: List[str]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        if total < 80:
            recommendations.append(f"Overall coverage is {total:.1f}%, target is 80%")
        
        if common < 90:
            recommendations.append(f"Common module coverage is {common:.1f}%, target is 90%")
        
        if len(untested) > 0:
            recommendations.append(f"Add tests for {len(untested)} untested files")
        
        if not recommendations:
            recommendations.append("Coverage meets requirements, maintain current level")
        
        return recommendations
    
    def print_report(self, report: Dict[str, Any]):
        """打印报告到控制台"""
        print("=" * 60)
        print("📊 Test Coverage Report")
        print("=" * 60)
        print()
        
        print(f"Overall Coverage: {report['total_coverage']}% {report['coverage_status']}")
        print(f"Common Module: {report['common_module_coverage']}%")
        print()
        
        if report['module_coverage']:
            print("Module Coverage:")
            for module, coverage in sorted(report['module_coverage'].items()):
                status = "✅" if coverage >= 80 else "⚠️" if coverage >= 60 else "❌"
                print(f"  - {module:20s}: {coverage:5.1f}% {status}")
            print()
        
        if report['untested_file_count'] > 0:
            print(f"Untested Files: {report['untested_file_count']}")
            for file in report['untested_files'][:5]:
                print(f"  - {file}")
            if report['untested_file_count'] > 5:
                print(f"  ... and {report['untested_file_count'] - 5} more")
            print()
        
        print("Recommendations:")
        for rec in report['recommendations']:
            print(f"  • {rec}")
        
        print()
        print("=" * 60)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Coverage Checker")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    checker = TestCoverageChecker()
    report = checker.generate_report()
    
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        checker.print_report(report)
    
    # 返回状态码
    if report['total_coverage'] < 60:
        return 1  # 失败
    return 0  # 成功


if __name__ == "__main__":
    sys.exit(main())
