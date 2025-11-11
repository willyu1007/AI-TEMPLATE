#!/usr/bin/env python3
"""

30

Usage:
    python scripts/doc_freshness_check.py [--json] [--days DAYS]
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent


class DocFreshnessChecker:
    """"""
    
    def __init__(self, stale_days: int = 30):
        """
        
        
        Args:
            stale_days: 30
        """
        self.repo_root = REPO_ROOT
        self.stale_days = stale_days
        self.stale_threshold = datetime.now() - timedelta(days=stale_days)
        
        # 
        self.critical_docs = [
            "README.md",
            "AGENTS.md",
            "doc/modules/MODULE_INIT_GUIDE.md",
            "doc/process/AI_CODING_GUIDE.md",
            "doc/policies/AI_INDEX.md",
            "QUICK_START.md",
            "TEMPLATE_USAGE.md"
        ]
    
    def get_file_last_modified(self, file_path: Path) -> datetime:
        """git log"""
        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%ai', '--', str(file_path)],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and result.stdout.strip():
                # git2025-11-09 14:30:00 +0800
                date_str = result.stdout.strip().split()[0]  # 
                return datetime.strptime(date_str, '%Y-%m-%d')
            else:
                # git log
                stat = file_path.stat()
                return datetime.fromtimestamp(stat.st_mtime)
        except Exception:
            # 
            try:
                stat = file_path.stat()
                return datetime.fromtimestamp(stat.st_mtime)
            except:
                return datetime.now()  # 
    
    def check_document(self, file_path: Path) -> Dict[str, Any]:
        """"""
        last_modified = self.get_file_last_modified(file_path)
        is_stale = last_modified < self.stale_threshold
        days_old = (datetime.now() - last_modified).days
        
        relative_path = file_path.relative_to(self.repo_root)
        is_critical = str(relative_path) in self.critical_docs
        
        return {
            'file': str(relative_path),
            'last_modified': last_modified.strftime('%Y-%m-%d'),
            'days_old': days_old,
            'is_stale': is_stale,
            'is_critical': is_critical
        }
    
    def scan_documents(self) -> Dict[str, Any]:
        """"""
        all_docs = []
        stale_docs = []
        critical_stale = []
        
        # markdown
        for md_file in self.repo_root.rglob("*.md"):
            # 
            if any(skip in str(md_file) for skip in [
                '.git', 'node_modules', '.venv', 'venv', '__pycache__',
                'build', 'dist', 'temp', 'archive'
            ]):
                continue
            
            doc_info = self.check_document(md_file)
            all_docs.append(doc_info)
            
            if doc_info['is_stale']:
                stale_docs.append(doc_info)
                if doc_info['is_critical']:
                    critical_stale.append(doc_info)
        
        # 
        stale_docs.sort(key=lambda x: x['days_old'], reverse=True)
        
        # 
        fresh_count = len(all_docs) - len(stale_docs)
        freshness_percentage = (fresh_count / len(all_docs) * 100) if all_docs else 100
        
        return {
            'total_docs': len(all_docs),
            'fresh_docs': fresh_count,
            'stale_docs': len(stale_docs),
            'critical_stale': len(critical_stale),
            'freshness_percentage': round(freshness_percentage, 1),
            'stale_threshold_days': self.stale_days,
            'stale_list': stale_docs[:20],  # 20
            'critical_stale_list': critical_stale,
            'oldest_docs': stale_docs[:10] if stale_docs else []
        }
    
    def generate_update_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """"""
        recommendations = []
        
        if results['critical_stale'] > 0:
            recommendations.append(f"URGENT: Update {results['critical_stale']} critical documents")
            for doc in results['critical_stale_list']:
                recommendations.append(f"  • {doc['file']} ({doc['days_old']} days old)")
        
        if results['stale_docs'] > 10:
            recommendations.append(f"Review and update {results['stale_docs']} stale documents")
        
        if results['oldest_docs']:
            oldest = results['oldest_docs'][0]
            recommendations.append(f"Oldest document: {oldest['file']} ({oldest['days_old']} days)")
        
        if results['freshness_percentage'] < 80:
            recommendations.append("Schedule regular documentation reviews (weekly/monthly)")
        
        if not recommendations:
            recommendations.append("Documentation freshness is good, keep it up!")
        
        return recommendations
    
    def print_report(self, results: Dict[str, Any]):
        """"""
        print("=" * 60)
        print("📅 Documentation Freshness Report")
        print("=" * 60)
        print()
        
        print(f"Threshold: {results['stale_threshold_days']} days")
        print(f"Total Documents: {results['total_docs']}")
        print(f"Fresh Documents: {results['fresh_docs']}")
        print(f"Stale Documents: {results['stale_docs']}")
        print(f"Freshness Rate: {results['freshness_percentage']}%")
        print()
        
        status = "✅" if results['freshness_percentage'] >= 90 else "⚠️" if results['freshness_percentage'] >= 80 else "❌"
        print(f"Status: {status}")
        
        if results['critical_stale'] > 0:
            print(f"\n⚠️ Critical Documents Need Update ({results['critical_stale']}):")
            for doc in results['critical_stale_list']:
                print(f"  • {doc['file']} - {doc['days_old']} days old")
        
        if results['oldest_docs']:
            print(f"\n📜 Oldest Documents:")
            for doc in results['oldest_docs'][:5]:
                print(f"  • {doc['file']} - {doc['days_old']} days old (last: {doc['last_modified']})")
        
        print("\nRecommendations:")
        for rec in self.generate_update_recommendations(results):
            print(f"  • {rec}")
        
        print()
        print("=" * 60)


def main():
    """"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Documentation Freshness Checker")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--days", type=int, default=30, 
                       help="Days threshold for stale documents (default: 30)")
    args = parser.parse_args()
    
    checker = DocFreshnessChecker(stale_days=args.days)
    results = checker.scan_documents()
    
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False, default=str))
    else:
        checker.print_report(results)
    
    # 
    if results['freshness_percentage'] < 70:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())