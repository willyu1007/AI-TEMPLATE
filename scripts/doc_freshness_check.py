#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_freshness_check.py - 文档时效性检查工具

功能：
1. 检查文档的最后修改时间
2. 标记超过90天未更新的文档为"过时"
3. 计算文档新鲜度百分比
4. 重点关注关键文档（README.md, agent.md等）

过时阈值：90天（根据HEALTH_CHECK_MODEL.yaml）

用法：
    python scripts/doc_freshness_check.py
    python scripts/doc_freshness_check.py --json
    python scripts/doc_freshness_check.py --threshold 60
    make doc_freshness_check

Created: 2025-11-09 (Phase 14.2)
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
DOC_DIR = REPO_ROOT / "doc"
AI_DIR = REPO_ROOT / "ai"

# 关键文档列表
CRITICAL_DOCS = [
    "README.md",
    "agent.md",
    "doc/modules/MODULE_INIT_GUIDE.md",
    "doc/process/AI_CODING_GUIDE.md",
    "doc/policies/AI_INDEX.md"
]

# 默认过时阈值（天）
DEFAULT_STALE_THRESHOLD_DAYS = 90


class DocFreshnessChecker:
    """文档时效性检查器"""
    
    def __init__(self, stale_threshold_days: int = DEFAULT_STALE_THRESHOLD_DAYS):
        """初始化检查器"""
        self.stale_threshold_days = stale_threshold_days
        self.stale_threshold = datetime.now() - timedelta(days=stale_threshold_days)
        
        self.results = {
            "check_time": datetime.now().isoformat(),
            "stale_threshold_days": stale_threshold_days,
            "total_docs": 0,
            "fresh_docs": 0,
            "stale_docs": 0,
            "freshness_percentage": 0,
            "critical_docs_stale": [],
            "stale_doc_list": [],
            "fresh_doc_list": []
        }
    
    def find_all_docs(self) -> List[Path]:
        """查找所有文档"""
        doc_files = []
        
        # 搜索doc/目录
        if DOC_DIR.exists():
            for pattern in ["**/*.md", "**/*.MD"]:
                doc_files.extend(DOC_DIR.glob(pattern))
        
        # 搜索ai/目录
        if AI_DIR.exists():
            for pattern in ["**/*.md", "**/*.MD"]:
                doc_files.extend(AI_DIR.glob(pattern))
        
        # 搜索根目录的README和agent.md
        doc_files.append(REPO_ROOT / "README.md")
        doc_files.append(REPO_ROOT / "agent.md")
        
        # 排除temp目录和隐藏目录
        doc_files = [f for f in doc_files if f.exists() and "temp" not in f.parts and not any(part.startswith('.') for part in f.parts)]
        
        return list(set(doc_files))  # 去重
    
    def check_doc_freshness(self, doc_path: Path) -> Dict[str, Any]:
        """检查单个文档的时效性"""
        try:
            # 获取文件最后修改时间
            mtime = os.path.getmtime(doc_path)
            last_modified = datetime.fromtimestamp(mtime)
            
            # 计算天数差
            days_since_update = (datetime.now() - last_modified).days
            
            # 判断是否过时
            is_stale = last_modified < self.stale_threshold
            
            # 判断是否为关键文档
            rel_path = str(doc_path.relative_to(REPO_ROOT))
            is_critical = rel_path in CRITICAL_DOCS
            
            return {
                "path": rel_path,
                "last_modified": last_modified.isoformat(),
                "days_since_update": days_since_update,
                "is_stale": is_stale,
                "is_critical": is_critical,
                "status": "❌ 过时" if is_stale else "✅ 新鲜"
            }
        except Exception as e:
            return {
                "path": str(doc_path.relative_to(REPO_ROOT)),
                "error": str(e),
                "is_stale": True,
                "is_critical": False,
                "status": "❌ 错误"
            }
    
    def check_all_docs(self):
        """检查所有文档的时效性"""
        print(f"🔍 检查文档时效性（过时阈值: {self.stale_threshold_days}天）...")
        
        doc_files = self.find_all_docs()
        self.results["total_docs"] = len(doc_files)
        
        if len(doc_files) == 0:
            print("  ⚠️ 未找到任何文档")
            return
        
        print(f"  找到 {len(doc_files)} 个文档\n")
        
        for doc_path in doc_files:
            result = self.check_doc_freshness(doc_path)
            
            if result.get("is_stale", False):
                self.results["stale_docs"] += 1
                self.results["stale_doc_list"].append(result)
                
                # 检查是否为关键文档
                if result.get("is_critical", False):
                    self.results["critical_docs_stale"].append(result)
            else:
                self.results["fresh_docs"] += 1
                self.results["fresh_doc_list"].append(result)
        
        # 计算新鲜度百分比
        if self.results["total_docs"] > 0:
            self.results["freshness_percentage"] = (self.results["fresh_docs"] / self.results["total_docs"]) * 100
        else:
            self.results["freshness_percentage"] = 0
    
    def print_console_report(self):
        """打印控制台报告"""
        print("\n" + "=" * 70)
        print("📊 DOCUMENTATION FRESHNESS REPORT")
        print("=" * 70)
        
        print(f"\n📈 Overall Statistics:")
        print(f"  总文档数: {self.results['total_docs']}")
        print(f"  新鲜文档: {self.results['fresh_docs']}")
        print(f"  过时文档: {self.results['stale_docs']}")
        print(f"  新鲜度: {self.results['freshness_percentage']:.1f}%")
        print(f"  阈值: {self.stale_threshold_days}天")
        
        # 关键文档过时警告
        if self.results["critical_docs_stale"]:
            print(f"\n⚠️ 关键文档过时 ({len(self.results['critical_docs_stale'])}):")
            for doc in self.results["critical_docs_stale"]:
                print(f"  - {doc['path']} (已{doc['days_since_update']}天未更新)")
        
        # 显示部分过时文档
        if self.results["stale_doc_list"]:
            stale_count = len(self.results["stale_doc_list"])
            show_count = min(10, stale_count)
            
            print(f"\n❌ 过时文档 (显示前{show_count}/{stale_count}):")
            # 按天数排序，最久的在前
            sorted_stale = sorted(self.results["stale_doc_list"], 
                                 key=lambda x: x.get("days_since_update", 0), 
                                 reverse=True)
            
            for doc in sorted_stale[:show_count]:
                days = doc.get("days_since_update", 0)
                print(f"  - {doc['path']} ({days}天)")
        
        # 建议
        print(f"\n💡 建议:")
        if self.results["freshness_percentage"] < 90:
            print("  - 定期审查和更新文档")
            print("  - 优先更新关键文档")
            print("  - 在CHANGELOG.md中记录重大变更")
        else:
            print("  - 文档时效性良好，继续保持！")
        
        print("\n" + "=" * 70)
    
    def print_json_report(self):
        """打印JSON报告"""
        print(json.dumps(self.results, indent=2, ensure_ascii=False))


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Documentation Freshness Check")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    parser.add_argument("--threshold", type=int, default=DEFAULT_STALE_THRESHOLD_DAYS,
                       help=f"过时阈值（天，默认{DEFAULT_STALE_THRESHOLD_DAYS}）")
    
    args = parser.parse_args()
    
    checker = DocFreshnessChecker(stale_threshold_days=args.threshold)
    checker.check_all_docs()
    
    if args.json:
        checker.print_json_report()
    else:
        checker.print_console_report()
    
    # 根据新鲜度决定退出码
    if checker.results["freshness_percentage"] < 85:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

