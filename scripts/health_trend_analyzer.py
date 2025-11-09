#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
health_trend_analyzer.py - 健康度趋势分析工具

功能：
1. 读取历史健康度数据
2. 计算趋势（改善/退化）
3. 显示关键指标变化
4. 预测何时达到目标分数
5. 检测回归并告警

历史数据存储：ai/maintenance_reports/health-history.json

用法：
    python scripts/health_trend_analyzer.py
    python scripts/health_trend_analyzer.py --days 30
    python scripts/health_trend_analyzer.py --json
    make health_trend

Created: 2025-11-09 (Phase 14.2)
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
HISTORY_FILE = REPO_ROOT / "ai" / "maintenance_reports" / "health-history.json"


class HealthTrendAnalyzer:
    """健康度趋势分析器"""
    
    def __init__(self, days: int = 30):
        """初始化分析器"""
        self.days = days
        self.history = []
        self.results = {
            "analysis_date": datetime.now().isoformat(),
            "days_analyzed": days,
            "data_points": 0,
            "current_score": 0,
            "trend": "unknown",
            "velocity": 0,  # 每周变化的点数
            "regression_detected": False,
            "metrics": {},
            "projection": {}
        }
    
    def load_history(self) -> bool:
        """加载历史数据"""
        if not HISTORY_FILE.exists():
            print(f"⚠️ 历史数据文件不存在: {HISTORY_FILE.relative_to(REPO_ROOT)}")
            print("  提示: 运行多次 make health_check 后会自动生成历史数据")
            return False
        
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 过滤指定天数内的数据
            cutoff_date = datetime.now() - timedelta(days=self.days)
            
            if isinstance(data, list):
                self.history = [
                    entry for entry in data
                    if datetime.fromisoformat(entry["timestamp"]) >= cutoff_date
                ]
            elif isinstance(data, dict) and "history" in data:
                self.history = [
                    entry for entry in data["history"]
                    if datetime.fromisoformat(entry["timestamp"]) >= cutoff_date
                ]
            
            self.results["data_points"] = len(self.history)
            
            print(f"✓ 加载了 {len(self.history)} 条历史记录")
            return len(self.history) > 0
        
        except Exception as e:
            print(f"❌ 加载历史数据失败: {e}", file=sys.stderr)
            return False
    
    def analyze_overall_trend(self):
        """分析整体趋势"""
        if len(self.history) < 2:
            self.results["trend"] = "insufficient_data"
            return
        
        # 获取最早和最新的分数
        scores = [entry.get("total_score", 0) for entry in self.history]
        
        first_score = scores[0]
        last_score = scores[-1]
        
        self.results["current_score"] = last_score
        self.results["score_change"] = last_score - first_score
        
        # 计算趋势
        if last_score > first_score + 2:
            self.results["trend"] = "improving"
            self.results["trend_label"] = "📈 改善"
        elif last_score < first_score - 2:
            self.results["trend"] = "declining"
            self.results["trend_label"] = "📉 退化"
        else:
            self.results["trend"] = "stable"
            self.results["trend_label"] = "➡️ 稳定"
        
        # 计算速度（每周变化）
        days_span = (datetime.fromisoformat(self.history[-1]["timestamp"]) - 
                    datetime.fromisoformat(self.history[0]["timestamp"])).days
        
        if days_span > 0:
            weeks = days_span / 7
            self.results["velocity"] = (last_score - first_score) / weeks
        else:
            self.results["velocity"] = 0
    
    def analyze_metric_trends(self):
        """分析各指标的趋势"""
        if len(self.history) < 2:
            return
        
        # 追踪的关键指标
        tracked_metrics = [
            ("dimensions.code_quality.actual_score", "Code Quality"),
            ("dimensions.documentation.actual_score", "Documentation"),
            ("dimensions.architecture.actual_score", "Architecture"),
            ("dimensions.ai_friendliness.actual_score", "AI Friendliness"),
            ("dimensions.operations.actual_score", "Operations"),
        ]
        
        for metric_path, metric_name in tracked_metrics:
            values = []
            
            for entry in self.history:
                value = self._get_nested_value(entry, metric_path)
                if value is not None:
                    values.append(value)
            
            if len(values) >= 2:
                change = values[-1] - values[0]
                trend = "up" if change > 0.5 else ("down" if change < -0.5 else "stable")
                
                self.results["metrics"][metric_name] = {
                    "first": values[0],
                    "last": values[-1],
                    "change": change,
                    "trend": trend
                }
    
    def _get_nested_value(self, data: Dict, path: str) -> Optional[float]:
        """获取嵌套字典的值"""
        keys = path.split('.')
        value = data
        
        try:
            for key in keys:
                value = value[key]
            return float(value) if value is not None else None
        except (KeyError, TypeError, ValueError):
            return None
    
    def detect_regression(self):
        """检测回归"""
        if len(self.history) < 2:
            return
        
        # 检查最近一次是否有显著下降
        if len(self.history) >= 2:
            recent_score = self.history[-1].get("total_score", 0)
            previous_score = self.history[-2].get("total_score", 0)
            
            if recent_score < previous_score - 5:  # 下降超过5分
                self.results["regression_detected"] = True
                self.results["regression_amount"] = previous_score - recent_score
    
    def project_target_achievement(self):
        """预测何时达到目标分数"""
        target_score = 100
        current_score = self.results.get("current_score", 0)
        velocity = self.results.get("velocity", 0)
        
        if velocity <= 0:
            self.results["projection"] = {
                "target": target_score,
                "achievable": False,
                "reason": "当前速度为0或负值"
            }
            return
        
        points_needed = target_score - current_score
        weeks_needed = points_needed / velocity
        
        projected_date = datetime.now() + timedelta(weeks=weeks_needed)
        
        self.results["projection"] = {
            "target": target_score,
            "current": current_score,
            "points_needed": points_needed,
            "weeks_needed": round(weeks_needed, 1),
            "projected_date": projected_date.strftime("%Y-%m-%d"),
            "achievable": True
        }
    
    def analyze(self):
        """执行完整分析"""
        print("=" * 70)
        print("📊 Health Trend Analyzer - 开始分析...")
        print("=" * 70)
        
        # 加载历史数据
        if not self.load_history():
            print("\n❌ 无法加载历史数据，分析终止")
            return False
        
        # 分析趋势
        print("\n分析整体趋势...")
        self.analyze_overall_trend()
        
        print("分析各维度指标...")
        self.analyze_metric_trends()
        
        print("检测回归...")
        self.detect_regression()
        
        print("预测目标达成...")
        self.project_target_achievement()
        
        print("\n" + "=" * 70)
        print("✅ 趋势分析完成！")
        print("=" * 70)
        
        return True
    
    def print_console_report(self):
        """打印控制台报告"""
        print("\n" + "=" * 70)
        print("📈 HEALTH TREND ANALYSIS REPORT")
        print("=" * 70)
        
        print(f"\n📊 Overall Trend:")
        print(f"  分析天数: {self.results['days_analyzed']}天")
        print(f"  数据点数: {self.results['data_points']}")
        print(f"  当前分数: {self.results.get('current_score', 0):.1f}/100")
        
        if self.results.get("score_change") is not None:
            change = self.results["score_change"]
            print(f"  分数变化: {change:+.1f}")
        
        print(f"  趋势: {self.results.get('trend_label', '未知')}")
        print(f"  速度: {self.results.get('velocity', 0):+.2f} 点/周")
        
        # 回归警告
        if self.results.get("regression_detected", False):
            print(f"\n⚠️ 检测到回归！")
            print(f"  下降: {self.results.get('regression_amount', 0):.1f} 点")
        
        # 维度趋势
        if self.results.get("metrics"):
            print(f"\n📋 维度趋势:")
            for metric_name, metric_data in self.results["metrics"].items():
                trend_icon = "📈" if metric_data["trend"] == "up" else ("📉" if metric_data["trend"] == "down" else "➡️")
                print(f"  {trend_icon} {metric_name}: {metric_data['first']:.1f} → {metric_data['last']:.1f} ({metric_data['change']:+.1f})")
        
        # 预测
        if self.results.get("projection"):
            proj = self.results["projection"]
            print(f"\n🎯 目标预测（100分）:")
            
            if proj.get("achievable", False):
                print(f"  需要: {proj['points_needed']:.1f} 点")
                print(f"  预计: {proj['weeks_needed']} 周")
                print(f"  日期: {proj['projected_date']}")
            else:
                print(f"  状态: 不可预测")
                print(f"  原因: {proj.get('reason', '未知')}")
        
        # 建议
        print(f"\n💡 建议:")
        if self.results.get("trend") == "improving":
            print("  ✅ 保持当前改进速度")
            print("  📈 继续关注待改进项")
        elif self.results.get("trend") == "declining":
            print("  ⚠️ 分数下降，需要关注")
            print("  🔍 审查最近的变更")
            print("  📝 执行健康度检查找出问题")
        else:
            print("  ➡️ 分数稳定，考虑主动改进")
        
        print("\n" + "=" * 70)
    
    def print_json_report(self):
        """打印JSON报告"""
        print(json.dumps(self.results, indent=2, ensure_ascii=False))


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Health Trend Analyzer")
    parser.add_argument("--days", type=int, default=30, help="分析天数（默认30天）")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    
    args = parser.parse_args()
    
    analyzer = HealthTrendAnalyzer(days=args.days)
    
    if not analyzer.analyze():
        sys.exit(1)
    
    if args.json:
        analyzer.print_json_report()
    else:
        analyzer.print_console_report()
    
    # 如果检测到回归，退出码为1
    if analyzer.results.get("regression_detected", False):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

