#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
health_trend_analyzer.py - 


1. 
2. /
3. 
4. 
5. 

ai/maintenance_reports/health-history.json


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

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
HISTORY_FILE = REPO_ROOT / "ai" / "maintenance_reports" / "health-history.json"


class HealthTrendAnalyzer:
    """"""
    
    def __init__(self, days: int = 30):
        """"""
        self.days = days
        self.history = []
        self.results = {
            "analysis_date": datetime.now().isoformat(),
            "days_analyzed": days,
            "data_points": 0,
            "current_score": 0,
            "trend": "unknown",
            "velocity": 0,  # 
            "regression_detected": False,
            "metrics": {},
            "projection": {}
        }
    
    def load_history(self) -> bool:
        """"""
        if not HISTORY_FILE.exists():
            print(f"⚠️ : {HISTORY_FILE.relative_to(REPO_ROOT)}")
            print("  :  make health_check ")
            return False
        
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 
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
            
            print(f"✓  {len(self.history)} ")
            return len(self.history) > 0
        
        except Exception as e:
            print(f"❌ : {e}", file=sys.stderr)
            return False
    
    def analyze_overall_trend(self):
        """"""
        if len(self.history) < 2:
            self.results["trend"] = "insufficient_data"
            return
        
        # 
        scores = [entry.get("total_score", 0) for entry in self.history]
        
        first_score = scores[0]
        last_score = scores[-1]
        
        self.results["current_score"] = last_score
        self.results["score_change"] = last_score - first_score
        
        # 
        if last_score > first_score + 2:
            self.results["trend"] = "improving"
            self.results["trend_label"] = "📈 "
        elif last_score < first_score - 2:
            self.results["trend"] = "declining"
            self.results["trend_label"] = "📉 "
        else:
            self.results["trend"] = "stable"
            self.results["trend_label"] = "➡️ "
        
        # 
        days_span = (datetime.fromisoformat(self.history[-1]["timestamp"]) - 
                    datetime.fromisoformat(self.history[0]["timestamp"])).days
        
        if days_span > 0:
            weeks = days_span / 7
            self.results["velocity"] = (last_score - first_score) / weeks
        else:
            self.results["velocity"] = 0
    
    def analyze_metric_trends(self):
        """"""
        if len(self.history) < 2:
            return
        
        # 
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
        """"""
        keys = path.split('.')
        value = data
        
        try:
            for key in keys:
                value = value[key]
            return float(value) if value is not None else None
        except (KeyError, TypeError, ValueError):
            return None
    
    def detect_regression(self):
        """"""
        if len(self.history) < 2:
            return
        
        # 
        if len(self.history) >= 2:
            recent_score = self.history[-1].get("total_score", 0)
            previous_score = self.history[-2].get("total_score", 0)
            
            if recent_score < previous_score - 5:  # 5
                self.results["regression_detected"] = True
                self.results["regression_amount"] = previous_score - recent_score
    
    def project_target_achievement(self):
        """"""
        target_score = 100
        current_score = self.results.get("current_score", 0)
        velocity = self.results.get("velocity", 0)
        
        if velocity <= 0:
            self.results["projection"] = {
                "target": target_score,
                "achievable": False,
                "reason": "0"
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
        """"""
        print("=" * 70)
        print("📊 Health Trend Analyzer - ...")
        print("=" * 70)
        
        # 
        if not self.load_history():
            print("\n❌ ")
            return False
        
        # 
        print("\n...")
        self.analyze_overall_trend()
        
        print("...")
        self.analyze_metric_trends()
        
        print("...")
        self.detect_regression()
        
        print("...")
        self.project_target_achievement()
        
        print("\n" + "=" * 70)
        print("✅ ")
        print("=" * 70)
        
        return True
    
    def print_console_report(self):
        """"""
        print("\n" + "=" * 70)
        print("📈 HEALTH TREND ANALYSIS REPORT")
        print("=" * 70)
        
        print(f"\n📊 Overall Trend:")
        print(f"  : {self.results['days_analyzed']}")
        print(f"  : {self.results['data_points']}")
        print(f"  : {self.results.get('current_score', 0):.1f}/100")
        
        if self.results.get("score_change") is not None:
            change = self.results["score_change"]
            print(f"  : {change:+.1f}")
        
        print(f"  : {self.results.get('trend_label', '')}")
        print(f"  : {self.results.get('velocity', 0):+.2f} /")
        
        # 
        if self.results.get("regression_detected", False):
            print(f"\n⚠️ ")
            print(f"  : {self.results.get('regression_amount', 0):.1f} ")
        
        # 
        if self.results.get("metrics"):
            print(f"\n📋 :")
            for metric_name, metric_data in self.results["metrics"].items():
                trend_icon = "📈" if metric_data["trend"] == "up" else ("📉" if metric_data["trend"] == "down" else "➡️")
                print(f"  {trend_icon} {metric_name}: {metric_data['first']:.1f} → {metric_data['last']:.1f} ({metric_data['change']:+.1f})")
        
        # 
        if self.results.get("projection"):
            proj = self.results["projection"]
            print(f"\n🎯 100:")
            
            if proj.get("achievable", False):
                print(f"  : {proj['points_needed']:.1f} ")
                print(f"  : {proj['weeks_needed']} ")
                print(f"  : {proj['projected_date']}")
            else:
                print(f"  : ")
                print(f"  : {proj.get('reason', '')}")
        
        # 
        print(f"\n💡 :")
        if self.results.get("trend") == "improving":
            print("  ✅ ")
            print("  📈 ")
        elif self.results.get("trend") == "declining":
            print("  ⚠️ ")
            print("  🔍 ")
            print("  📝 ")
        else:
            print("  ➡️ ")
        
        print("\n" + "=" * 70)
    
    def print_json_report(self):
        """JSON"""
        print(json.dumps(self.results, indent=2, ensure_ascii=False))


def main():
    """"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Health Trend Analyzer")
    parser.add_argument("--days", type=int, default=30, help="30")
    parser.add_argument("--json", action="store_true", help="JSON")
    
    args = parser.parse_args()
    
    analyzer = HealthTrendAnalyzer(days=args.days)
    
    if not analyzer.analyze():
        sys.exit(1)
    
    if args.json:
        analyzer.print_json_report()
    else:
        analyzer.print_console_report()
    
    # 1
    if analyzer.results.get("regression_detected", False):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

