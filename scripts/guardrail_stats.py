#!/usr/bin/env python3
"""
guardrail_stats.py - Guardrail

agent-triggers.yamlGuardrail

:
    python scripts/guardrail_stats.py
    python scripts/guardrail_stats.py --detailed
    make guardrail_stats

Created: 2025-11-08 (Phase 10.4)
"""

import os
import sys
import yaml
from typing import Dict, List, Any
from collections import defaultdict

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class GuardrailStats:
    """Guardrail"""
    
    def __init__(self, config_path: str = "doc/orchestration/agent-triggers.yaml"):
        """"""
        self.config_path = config_path
        self.config = self._load_config()
        self.triggers = self.config.get('triggers', {})
    
    def _load_config(self) -> Dict[str, Any]:
        """"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"❌ : {e}", file=sys.stderr)
            sys.exit(1)
    
    def analyze(self) -> Dict[str, Any]:
        """"""
        stats = {
            "total_rules": len(self.triggers),
            "by_enforcement": defaultdict(int),
            "by_priority": defaultdict(int),
            "block_rules": [],
            "warn_rules": [],
            "suggest_rules": [],
            "with_guardrail": 0,
            "with_skip_conditions": 0,
            "file_patterns_count": 0,
            "prompt_keywords_count": 0
        }
        
        for rule_id, rule in self.triggers.items():
            # enforcement
            enforcement = rule.get('enforcement', 'suggest')
            stats["by_enforcement"][enforcement] += 1
            
            # priority
            priority = rule.get('priority', 'medium')
            stats["by_priority"][priority] += 1
            
            # 
            rule_info = {
                "id": rule_id,
                "description": rule.get('description', ''),
                "priority": priority
            }
            
            if enforcement == 'block':
                stats["block_rules"].append(rule_info)
                # block_config
                if 'block_config' in rule:
                    block_config = rule['block_config']
                    rule_info['has_skip_conditions'] = 'skip_conditions' in block_config
                    rule_info['require_confirmation'] = block_config.get('require_confirmation', False)
                    if 'skip_conditions' in block_config:
                        stats["with_skip_conditions"] += 1
            
            elif enforcement == 'warn':
                stats["warn_rules"].append(rule_info)
                # warn_config
                if 'warn_config' in rule:
                    warn_config = rule['warn_config']
                    rule_info['require_confirmation'] = warn_config.get('require_confirmation', True)
            
            else:
                stats["suggest_rules"].append(rule_info)
            
            # Guardrail
            if 'guardrail' in rule and rule['guardrail']:
                stats["with_guardrail"] += 1
            
            # 
            if 'file_triggers' in rule:
                file_triggers = rule['file_triggers']
                if 'path_patterns' in file_triggers:
                    stats["file_patterns_count"] += len(file_triggers['path_patterns'])
            
            if 'prompt_triggers' in rule:
                prompt_triggers = rule['prompt_triggers']
                if 'keywords' in prompt_triggers:
                    stats["prompt_keywords_count"] += len(prompt_triggers['keywords'])
        
        return stats
    
    def print_summary(self, stats: Dict[str, Any]):
        """"""
        print("\n" + "="*60)
        print("🛡️  Guardrail")
        print("="*60)
        print()
        
        # 
        print(f"📊 :")
        print(f"  : {stats['total_rules']}")
        print(f"  : {stats['file_patterns_count']}")
        print(f"  Prompt: {stats['prompt_keywords_count']}")
        print()
        
        # Enforcement
        print(f"🔐 Enforcement:")
        for enforcement, count in sorted(stats['by_enforcement'].items()):
            icon = {"block": "🛑", "warn": "⚠️", "suggest": "💡"}.get(enforcement, "⚪")
            percentage = (count / stats['total_rules'] * 100) if stats['total_rules'] > 0 else 0
            print(f"  {icon} {enforcement:8s}: {count:2d} ({percentage:5.1f}%)")
        print()
        
        # Priority
        print(f"⭐ Priority:")
        priority_order = ['critical', 'high', 'medium', 'low']
        for priority in priority_order:
            count = stats['by_priority'].get(priority, 0)
            if count > 0:
                icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                percentage = (count / stats['total_rules'] * 100) if stats['total_rules'] > 0 else 0
                print(f"  {icon} {priority:8s}: {count:2d} ({percentage:5.1f}%)")
        print()
        
        # Guardrail
        print(f"🛡️  Guardrail:")
        print(f"  skip_conditions: {stats['with_skip_conditions']}")
        print(f"  guardrail: {stats['with_guardrail']}")
        print()
    
    def print_detailed(self, stats: Dict[str, Any]):
        """"""
        self.print_summary(stats)
        
        # Block
        if stats['block_rules']:
            print("="*60)
            print(f"🛑 Block ({len(stats['block_rules'])})")
            print("="*60)
            for rule in stats['block_rules']:
                print(f"\n  • {rule['id']}")
                print(f"    : {rule['description']}")
                print(f"    : {rule['priority']}")
                if rule.get('has_skip_conditions'):
                    print(f"    : ✅ ")
                if rule.get('require_confirmation'):
                    print(f"    : ✅ ")
        
        # Warn
        if stats['warn_rules']:
            print("\n" + "="*60)
            print(f"⚠️  Warn ({len(stats['warn_rules'])})")
            print("="*60)
            for rule in stats['warn_rules']:
                print(f"\n  • {rule['id']}")
                print(f"    : {rule['description']}")
                print(f"    : {rule['priority']}")
                if rule.get('require_confirmation'):
                    print(f"    : ✅ ")
        
        # Suggest
        if stats['suggest_rules']:
            print("\n" + "="*60)
            print(f"💡 Suggest ({len(stats['suggest_rules'])})")
            print("="*60)
            for rule in stats['suggest_rules']:
                print(f"\n  • {rule['id']}")
                print(f"    : {rule['description']}")
                print(f"    : {rule['priority']}")
        
        print("\n" + "="*60 + "\n")
    
    def check_coverage(self):
        """"""
        print("\n" + "="*60)
        print("📈 Guardrail")
        print("="*60)
        print()
        
        critical_areas = {
            "": False,
            "": False,
            "": False,
            "": False,
            "": False
        }
        
        for rule_id, rule in self.triggers.items():
            description = rule.get('description', '')
            
            if '' in description or 'security' in rule_id:
                critical_areas[""] = True
            if '' in description or 'contract' in rule_id:
                critical_areas[""] = True
            if '' in description or 'prod' in rule_id:
                critical_areas[""] = True
            if '' in description or 'migration' in rule_id:
                critical_areas[""] = True
            if 'agent' in rule_id or '' in description:
                critical_areas[""] = True
        
        print(":")
        for area, covered in critical_areas.items():
            icon = "✅" if covered else "❌"
            print(f"  {icon} {area}")
        
        coverage_rate = sum(critical_areas.values()) / len(critical_areas) * 100
        print(f"\n: {coverage_rate:.0f}%")
        
        if coverage_rate == 100:
            print("✅ Guardrail\n")
        else:
            print("⚠️  Guardrail\n")


def main():
    """"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Guardrail',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--config', '-c', type=str,
                       default='doc/orchestration/agent-triggers.yaml',
                       help='')
    parser.add_argument('--detailed', '-d', action='store_true',
                       help='')
    parser.add_argument('--check-coverage', action='store_true',
                       help='')
    
    args = parser.parse_args()
    
    # 
    stats_tool = GuardrailStats(args.config)
    
    # 
    stats = stats_tool.analyze()
    
    # 
    if args.detailed:
        stats_tool.print_detailed(stats)
    else:
        stats_tool.print_summary(stats)
    
    # 
    if args.check_coverage:
        stats_tool.check_coverage()


if __name__ == "__main__":
    main()

