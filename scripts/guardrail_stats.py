#!/usr/bin/env python3
"""
guardrail_stats.py - Guardrail统计工具

分析agent-triggers.yaml，统计Guardrail规则的配置和覆盖情况。

用法:
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
    """Guardrail统计分析"""
    
    def __init__(self, config_path: str = "doc/orchestration/agent-triggers.yaml"):
        """初始化"""
        self.config_path = config_path
        self.config = self._load_config()
        self.triggers = self.config.get('triggers', {})
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"❌ 加载配置失败: {e}", file=sys.stderr)
            sys.exit(1)
    
    def analyze(self) -> Dict[str, Any]:
        """分析统计"""
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
            # 统计enforcement
            enforcement = rule.get('enforcement', 'suggest')
            stats["by_enforcement"][enforcement] += 1
            
            # 统计priority
            priority = rule.get('priority', 'medium')
            stats["by_priority"][priority] += 1
            
            # 分类规则
            rule_info = {
                "id": rule_id,
                "description": rule.get('description', ''),
                "priority": priority
            }
            
            if enforcement == 'block':
                stats["block_rules"].append(rule_info)
                # 检查是否有block_config
                if 'block_config' in rule:
                    block_config = rule['block_config']
                    rule_info['has_skip_conditions'] = 'skip_conditions' in block_config
                    rule_info['require_confirmation'] = block_config.get('require_confirmation', False)
                    if 'skip_conditions' in block_config:
                        stats["with_skip_conditions"] += 1
            
            elif enforcement == 'warn':
                stats["warn_rules"].append(rule_info)
                # 检查是否有warn_config
                if 'warn_config' in rule:
                    warn_config = rule['warn_config']
                    rule_info['require_confirmation'] = warn_config.get('require_confirmation', True)
            
            else:
                stats["suggest_rules"].append(rule_info)
            
            # 统计Guardrail
            if 'guardrail' in rule and rule['guardrail']:
                stats["with_guardrail"] += 1
            
            # 统计触发模式
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
        """打印摘要"""
        print("\n" + "="*60)
        print("🛡️  Guardrail统计摘要")
        print("="*60)
        print()
        
        # 总体统计
        print(f"📊 总体统计:")
        print(f"  总规则数: {stats['total_rules']}")
        print(f"  文件模式数: {stats['file_patterns_count']}")
        print(f"  Prompt关键词数: {stats['prompt_keywords_count']}")
        print()
        
        # Enforcement分布
        print(f"🔐 Enforcement分布:")
        for enforcement, count in sorted(stats['by_enforcement'].items()):
            icon = {"block": "🛑", "warn": "⚠️", "suggest": "💡"}.get(enforcement, "⚪")
            percentage = (count / stats['total_rules'] * 100) if stats['total_rules'] > 0 else 0
            print(f"  {icon} {enforcement:8s}: {count:2d} ({percentage:5.1f}%)")
        print()
        
        # Priority分布
        print(f"⭐ Priority分布:")
        priority_order = ['critical', 'high', 'medium', 'low']
        for priority in priority_order:
            count = stats['by_priority'].get(priority, 0)
            if count > 0:
                icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                percentage = (count / stats['total_rules'] * 100) if stats['total_rules'] > 0 else 0
                print(f"  {icon} {priority:8s}: {count:2d} ({percentage:5.1f}%)")
        print()
        
        # Guardrail特性
        print(f"🛡️  Guardrail特性:")
        print(f"  带skip_conditions: {stats['with_skip_conditions']}")
        print(f"  带guardrail检查: {stats['with_guardrail']}")
        print()
    
    def print_detailed(self, stats: Dict[str, Any]):
        """打印详细信息"""
        self.print_summary(stats)
        
        # Block规则详情
        if stats['block_rules']:
            print("="*60)
            print(f"🛑 Block规则 ({len(stats['block_rules'])}个)")
            print("="*60)
            for rule in stats['block_rules']:
                print(f"\n  • {rule['id']}")
                print(f"    描述: {rule['description']}")
                print(f"    优先级: {rule['priority']}")
                if rule.get('has_skip_conditions'):
                    print(f"    跳过条件: ✅ 有")
                if rule.get('require_confirmation'):
                    print(f"    需要确认: ✅ 是")
        
        # Warn规则详情
        if stats['warn_rules']:
            print("\n" + "="*60)
            print(f"⚠️  Warn规则 ({len(stats['warn_rules'])}个)")
            print("="*60)
            for rule in stats['warn_rules']:
                print(f"\n  • {rule['id']}")
                print(f"    描述: {rule['description']}")
                print(f"    优先级: {rule['priority']}")
                if rule.get('require_confirmation'):
                    print(f"    需要确认: ✅ 是")
        
        # Suggest规则
        if stats['suggest_rules']:
            print("\n" + "="*60)
            print(f"💡 Suggest规则 ({len(stats['suggest_rules'])}个)")
            print("="*60)
            for rule in stats['suggest_rules']:
                print(f"\n  • {rule['id']}")
                print(f"    描述: {rule['description']}")
                print(f"    优先级: {rule['priority']}")
        
        print("\n" + "="*60 + "\n")
    
    def check_coverage(self):
        """检查覆盖情况"""
        print("\n" + "="*60)
        print("📈 Guardrail覆盖检查")
        print("="*60)
        print()
        
        critical_areas = {
            "安全相关": False,
            "契约变更": False,
            "生产配置": False,
            "数据库迁移": False,
            "根配置变更": False
        }
        
        for rule_id, rule in self.triggers.items():
            description = rule.get('description', '')
            
            if '安全' in description or 'security' in rule_id:
                critical_areas["安全相关"] = True
            if '契约' in description or 'contract' in rule_id:
                critical_areas["契约变更"] = True
            if '生产' in description or 'prod' in rule_id:
                critical_areas["生产配置"] = True
            if '迁移' in description or 'migration' in rule_id:
                critical_areas["数据库迁移"] = True
            if 'agent' in rule_id or '根' in description:
                critical_areas["根配置变更"] = True
        
        print("关键领域覆盖:")
        for area, covered in critical_areas.items():
            icon = "✅" if covered else "❌"
            print(f"  {icon} {area}")
        
        coverage_rate = sum(critical_areas.values()) / len(critical_areas) * 100
        print(f"\n总体覆盖率: {coverage_rate:.0f}%")
        
        if coverage_rate == 100:
            print("✅ 所有关键领域都有Guardrail保护\n")
        else:
            print("⚠️  部分关键领域缺少Guardrail保护\n")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Guardrail统计工具',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--config', '-c', type=str,
                       default='doc/orchestration/agent-triggers.yaml',
                       help='配置文件路径')
    parser.add_argument('--detailed', '-d', action='store_true',
                       help='显示详细信息')
    parser.add_argument('--check-coverage', action='store_true',
                       help='检查覆盖情况')
    
    args = parser.parse_args()
    
    # 初始化
    stats_tool = GuardrailStats(args.config)
    
    # 分析
    stats = stats_tool.analyze()
    
    # 输出
    if args.detailed:
        stats_tool.print_detailed(stats)
    else:
        stats_tool.print_summary(stats)
    
    # 覆盖检查
    if args.check_coverage:
        stats_tool.check_coverage()


if __name__ == "__main__":
    main()

