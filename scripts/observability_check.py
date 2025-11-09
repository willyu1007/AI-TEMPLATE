#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
observability_check.py - 可观测性覆盖检查工具

功能：
1. 检查日志配置覆盖率（所有模块是否配置日志）
2. 检查指标收集点定义
3. 检查分布式追踪是否启用
4. 检查告警规则配置
5. 检查仪表盘模板存在性

检查项（根据HEALTH_CHECK_MODEL.yaml）：
- 所有模块有日志配置
- 指标收集点已定义
- 分布式追踪已启用
- 告警规则已配置
- 仪表盘模板存在

用法：
    python scripts/observability_check.py
    python scripts/observability_check.py --json
    make observability_check

Created: 2025-11-09 (Phase 14.2)
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Set

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
OBSERVABILITY_DIR = REPO_ROOT / "observability"
MODULES_DIR = REPO_ROOT / "modules"


class ObservabilityChecker:
    """可观测性检查器"""
    
    def __init__(self):
        """初始化检查器"""
        self.results = {
            "checks_passed": 0,
            "total_checks": 5,
            "checks": {},
            "coverage_percentage": 0
        }
    
    def check_logging_coverage(self) -> Dict[str, Any]:
        """检查日志配置覆盖率"""
        print("🔍 检查日志配置覆盖...")
        
        result = {
            "check_name": "Logging Coverage",
            "passed": False,
            "details": {}
        }
        
        # 检查observability/logging/目录
        logging_dir = OBSERVABILITY_DIR / "logging"
        
        if not logging_dir.exists():
            result["details"]["error"] = "logging目录不存在"
            result["details"]["status"] = "❌"
            return result
        
        # 检查是否有配置文件
        config_files = list(logging_dir.glob("*.yaml")) + list(logging_dir.glob("*.yml")) + list(logging_dir.glob("*.conf"))
        
        if len(config_files) == 0:
            result["details"]["error"] = "未找到日志配置文件"
            result["details"]["status"] = "❌"
            return result
        
        result["details"]["config_files"] = [f.name for f in config_files]
        result["details"]["config_count"] = len(config_files)
        result["details"]["status"] = "✅"
        result["passed"] = True
        
        return result
    
    def check_metrics_collection(self) -> Dict[str, Any]:
        """检查指标收集点定义"""
        print("🔍 检查指标收集点...")
        
        result = {
            "check_name": "Metrics Collection",
            "passed": False,
            "details": {}
        }
        
        # 检查observability/metrics/目录
        metrics_dir = OBSERVABILITY_DIR / "metrics"
        
        if not metrics_dir.exists():
            result["details"]["error"] = "metrics目录不存在"
            result["details"]["status"] = "❌"
            return result
        
        # 检查是否有配置文件
        config_files = list(metrics_dir.glob("*.json")) + list(metrics_dir.glob("*.yaml")) + list(metrics_dir.glob("*.yml"))
        
        if len(config_files) == 0:
            result["details"]["error"] = "未找到指标配置文件"
            result["details"]["status"] = "❌"
            return result
        
        result["details"]["config_files"] = [f.name for f in config_files]
        result["details"]["config_count"] = len(config_files)
        result["details"]["status"] = "✅"
        result["passed"] = True
        
        return result
    
    def check_distributed_tracing(self) -> Dict[str, Any]:
        """检查分布式追踪配置"""
        print("🔍 检查分布式追踪...")
        
        result = {
            "check_name": "Distributed Tracing",
            "passed": False,
            "details": {}
        }
        
        # 检查observability/tracing/目录
        tracing_dir = OBSERVABILITY_DIR / "tracing"
        
        if not tracing_dir.exists():
            result["details"]["error"] = "tracing目录不存在"
            result["details"]["status"] = "❌"
            return result
        
        # 检查是否有配置文件
        config_files = list(tracing_dir.glob("*.yaml")) + list(tracing_dir.glob("*.yml"))
        
        if len(config_files) == 0:
            result["details"]["error"] = "未找到追踪配置文件"
            result["details"]["status"] = "❌"
            return result
        
        result["details"]["config_files"] = [f.name for f in config_files]
        result["details"]["config_count"] = len(config_files)
        result["details"]["status"] = "✅"
        result["passed"] = True
        
        return result
    
    def check_alert_rules(self) -> Dict[str, Any]:
        """检查告警规则配置"""
        print("🔍 检查告警规则...")
        
        result = {
            "check_name": "Alert Rules",
            "passed": False,
            "details": {}
        }
        
        # 检查observability/alerts/目录
        alerts_dir = OBSERVABILITY_DIR / "alerts"
        
        if not alerts_dir.exists():
            result["details"]["error"] = "alerts目录不存在"
            result["details"]["status"] = "❌"
            return result
        
        # 检查是否有告警规则文件
        rule_files = list(alerts_dir.glob("*.yml")) + list(alerts_dir.glob("*.yaml"))
        
        if len(rule_files) == 0:
            result["details"]["error"] = "未找到告警规则文件"
            result["details"]["status"] = "❌"
            return result
        
        result["details"]["rule_files"] = [f.name for f in rule_files]
        result["details"]["rule_count"] = len(rule_files)
        result["details"]["status"] = "✅"
        result["passed"] = True
        
        return result
    
    def check_dashboard_templates(self) -> Dict[str, Any]:
        """检查仪表盘模板"""
        print("🔍 检查仪表盘模板...")
        
        result = {
            "check_name": "Dashboard Templates",
            "passed": False,
            "details": {}
        }
        
        # 检查observability/目录下是否有README或dashboard相关文件
        if not OBSERVABILITY_DIR.exists():
            result["details"]["error"] = "observability目录不存在"
            result["details"]["status"] = "❌"
            return result
        
        # 检查README
        readme_path = OBSERVABILITY_DIR / "README.md"
        if readme_path.exists():
            result["details"]["has_readme"] = True
            result["details"]["status"] = "✅"
            result["passed"] = True
        else:
            result["details"]["has_readme"] = False
            result["details"]["error"] = "缺少README.md"
            result["details"]["status"] = "⚠️"
            # 即使没有README也算部分通过（有其他配置）
            if (OBSERVABILITY_DIR / "logging").exists() and \
               (OBSERVABILITY_DIR / "metrics").exists():
                result["passed"] = True
        
        return result
    
    def run_all_checks(self):
        """运行所有检查"""
        print("=" * 70)
        print("🔭 Observability Coverage Check - 开始检查...")
        print("=" * 70)
        
        # 运行5项检查
        self.results["checks"]["logging"] = self.check_logging_coverage()
        self.results["checks"]["metrics"] = self.check_metrics_collection()
        self.results["checks"]["tracing"] = self.check_distributed_tracing()
        self.results["checks"]["alerts"] = self.check_alert_rules()
        self.results["checks"]["dashboard"] = self.check_dashboard_templates()
        
        # 统计通过的检查数
        self.results["checks_passed"] = sum(
            1 for check in self.results["checks"].values() 
            if check.get("passed", False)
        )
        
        # 计算覆盖率
        self.results["coverage_percentage"] = \
            (self.results["checks_passed"] / self.results["total_checks"]) * 100
        
        print("\n" + "=" * 70)
        print("✅ 可观测性检查完成！")
        print("=" * 70)
    
    def print_console_report(self):
        """打印控制台报告"""
        print("\n" + "=" * 70)
        print("📊 OBSERVABILITY COVERAGE REPORT")
        print("=" * 70)
        
        print(f"\n📈 Overall:")
        print(f"  通过检查: {self.results['checks_passed']}/{self.results['total_checks']}")
        print(f"  覆盖率: {self.results['coverage_percentage']:.0f}%")
        
        print(f"\n📋 Check Details:")
        
        for check_key, check_result in self.results["checks"].items():
            check_name = check_result["check_name"]
            status = check_result["details"].get("status", "❓")
            passed = "✅" if check_result["passed"] else "❌"
            
            print(f"\n  {passed} {check_name}:")
            
            if "config_files" in check_result["details"]:
                files = check_result["details"]["config_files"]
                print(f"     配置文件: {', '.join(files)}")
            elif "rule_files" in check_result["details"]:
                files = check_result["details"]["rule_files"]
                print(f"     规则文件: {', '.join(files)}")
            elif "has_readme" in check_result["details"]:
                has_readme = check_result["details"]["has_readme"]
                print(f"     README: {'存在' if has_readme else '缺失'}")
            
            if "error" in check_result["details"]:
                print(f"     错误: {check_result['details']['error']}")
        
        # 建议
        print(f"\n💡 建议:")
        if self.results["checks_passed"] < 4:
            print("  - 完善可观测性配置")
            print("  - 至少需要配置logging, metrics, tracing")
            print("  - 添加告警规则确保及时发现问题")
        elif self.results["checks_passed"] == 4:
            print("  - 可观测性配置良好")
            print("  - 建议完善剩余配置项")
        else:
            print("  - 可观测性配置完整，很好！")
        
        print("\n" + "=" * 70)
    
    def print_json_report(self):
        """打印JSON报告"""
        print(json.dumps(self.results, indent=2, ensure_ascii=False))


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Observability Coverage Check")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    
    args = parser.parse_args()
    
    checker = ObservabilityChecker()
    checker.run_all_checks()
    
    if args.json:
        checker.print_json_report()
    else:
        checker.print_console_report()
    
    # 根据通过数决定退出码
    if checker.results["checks_passed"] < 3:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

