#!/usr/bin/env python3
"""
AI
AI Agent

Usage:
    python scripts/ai_friendliness_check.py [--check CHECK_TYPE] [--json]
    
CHECK_TYPE:
    - lightweight: agent.md
    - clarity: 
    - automation: 
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent


class AIFriendlinessChecker:
    """AI"""
    
    def __init__(self):
        self.repo_root = REPO_ROOT
        self.agent_md_path = self.repo_root / "agent.md"
        self.doc_path = self.repo_root / "doc"
        self.makefile_path = self.repo_root / "Makefile"
        self.trigger_path = self.repo_root / "doc" / "orchestration" / "agent-triggers.yaml"
        
    def check_lightweight(self) -> Dict[str, Any]:
        """agent.md"""
        thresholds_met = 0
        results = {}
        
        # 1agent.md
        if self.agent_md_path.exists():
            with open(self.agent_md_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                line_count = len(lines)
                results['root_agent_md_lines'] = line_count
                
                if line_count <= 400:
                    thresholds_met += 1
                    results['root_agent_md_status'] = '✅'
                else:
                    results['root_agent_md_status'] = '❌'
        
        # 2always_read
        always_read_lines = 0
        always_read_files = 0
        
        # agent.mdYAML front matteralways_read
        if self.agent_md_path.exists():
            with open(self.agent_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '---' in content:
                    yaml_content = content.split('---')[1]
                    try:
                        agent_config = yaml.safe_load(yaml_content)
                        if 'context_routes' in agent_config:
                            always_read = agent_config['context_routes'].get('always_read', [])
                            always_read_files = len(always_read)
                            
                            for doc_path in always_read:
                                full_path = self.repo_root / doc_path.lstrip('/')
                                if full_path.exists():
                                    with open(full_path, 'r', encoding='utf-8') as doc_f:
                                        always_read_lines += len(doc_f.readlines())
                    except:
                        pass
        
        results['always_read_total_lines'] = always_read_lines
        results['always_read_file_count'] = always_read_files
        
        # always_read
        if always_read_lines <= 150:
            thresholds_met += 1
            results['always_read_lines_status'] = '✅'
        else:
            results['always_read_lines_status'] = '❌'
        
        if always_read_files <= 1:
            thresholds_met += 1
            results['always_read_count_status'] = '✅'
        else:
            results['always_read_count_status'] = '❌'
        
        results['thresholds_met'] = thresholds_met
        results['max_thresholds'] = 3
        
        return results
    
    def check_clarity(self) -> Dict[str, Any]:
        """"""
        total_docs = 0
        clear_docs = 0
        unclear_docs = []
        
        # markdown
        for md_file in self.doc_path.rglob("*.md"):
            total_docs += 1
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                first_lines = '\n'.join(content.split('\n')[:20])  # 20
                
                # 
                is_ai_doc = False
                is_human_doc = False
                
                # AI
                if any(marker in first_lines.lower() for marker in [
                    'for ai agents', 'ai-optimized', 'audience: ai',
                    'ai quickstart', 'ai reference'
                ]):
                    is_ai_doc = True
                
                # 
                if '_guide.md' in str(md_file).lower():
                    is_human_doc = True
                elif any(marker in first_lines.lower() for marker in [
                    'audience: human', 'complete guide',
                    'detailed documentation', 'comprehensive'
                ]):
                    is_human_doc = True
                
                # YAML front matter
                if '---' in content:
                    try:
                        yaml_content = content.split('---')[1]
                        doc_meta = yaml.safe_load(yaml_content)
                        if isinstance(doc_meta, dict):
                            audience = doc_meta.get('audience', '')
                            if audience == 'ai':
                                is_ai_doc = True
                            elif audience == 'human':
                                is_human_doc = True
                            elif audience == 'both':
                                is_ai_doc = True
                                is_human_doc = True
                    except:
                        pass
                
                # 
                if is_ai_doc or is_human_doc:
                    clear_docs += 1
                else:
                    unclear_docs.append(str(md_file.relative_to(self.repo_root)))
        
        clarity_percentage = (clear_docs / total_docs * 100) if total_docs > 0 else 0
        
        return {
            'total_docs': total_docs,
            'clear_docs': clear_docs,
            'unclear_docs_count': len(unclear_docs),
            'clarity_percentage': round(clarity_percentage, 1),
            'unclear_docs_sample': unclear_docs[:5]
        }
    
    def check_automation(self) -> Dict[str, Any]:
        """"""
        targets_met = 0
        results = {}
        
        # 1dev_check
        dev_check_count = 0
        if self.makefile_path.exists():
            with open(self.makefile_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # dev_check
                if 'dev_check:' in content:
                    # dev_check
                    dev_check_section = content.split('dev_check:')[1].split('\n\n')[0]
                    # make
                    dev_check_count = dev_check_section.count('$(MAKE)') + dev_check_section.count('make ')
        
        results['dev_check_count'] = dev_check_count
        if dev_check_count >= 21:
            targets_met += 1
            results['dev_check_status'] = '✅'
        else:
            results['dev_check_status'] = '❌'
        
        # 2Makefile
        makefile_commands = 0
        if self.makefile_path.exists():
            with open(self.makefile_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # make target
                    line = line.strip()
                    if line and not line.startswith('#') and ':' in line:
                        if line[0].isalpha() or line[0] == '.':
                            makefile_commands += 1
        
        results['makefile_commands'] = makefile_commands
        if makefile_commands >= 95:
            targets_met += 1
            results['makefile_status'] = '✅'
        else:
            results['makefile_status'] = '❌'
        
        # 3
        trigger_count = 0
        if self.trigger_path.exists():
            try:
                with open(self.trigger_path, 'r', encoding='utf-8') as f:
                    trigger_data = yaml.safe_load(f)
                    if 'triggers' in trigger_data:
                        trigger_count = len(trigger_data['triggers'])
            except:
                pass
        
        results['trigger_count'] = trigger_count
        if trigger_count >= 16:
            targets_met += 1
            results['trigger_status'] = '✅'
        else:
            results['trigger_status'] = '❌'
        
        results['automation_targets_met'] = targets_met
        results['max_targets'] = 3
        
        return results
    
    def run_all_checks(self) -> Dict[str, Any]:
        """"""
        return {
            'lightweight': self.check_lightweight(),
            'clarity': self.check_clarity(),
            'automation': self.check_automation()
        }
    
    def print_report(self, results: Dict[str, Any], check_type: str = None):
        """"""
        print("=" * 60)
        print("🤖 AI Friendliness Check Report")
        print("=" * 60)
        print()
        
        if check_type == 'lightweight' or check_type is None:
            if 'lightweight' in results:
                lw = results['lightweight']
                print("📏 Agent.md Lightweight Check:")
                print(f"  - Root agent.md: {lw['root_agent_md_lines']} lines {lw['root_agent_md_status']}")
                print(f"  - Always_read total: {lw['always_read_total_lines']} lines {lw['always_read_lines_status']}")
                print(f"  - Always_read files: {lw['always_read_file_count']} {lw['always_read_count_status']}")
                print(f"  - Thresholds met: {lw['thresholds_met']}/{lw['max_thresholds']}")
                print()
        
        if check_type == 'clarity' or check_type is None:
            if 'clarity' in results:
                cl = results['clarity']
                print("📖 Document Role Clarity:")
                print(f"  - Total docs: {cl['total_docs']}")
                print(f"  - Clear role docs: {cl['clear_docs']}")
                print(f"  - Clarity: {cl['clarity_percentage']}%")
                if cl['unclear_docs_count'] > 0:
                    print(f"  - Unclear docs: {cl['unclear_docs_count']}")
                    for doc in cl['unclear_docs_sample']:
                        print(f"    • {doc}")
                print()
        
        if check_type == 'automation' or check_type is None:
            if 'automation' in results:
                auto = results['automation']
                print("🔧 Automation Coverage:")
                print(f"  - Dev_check commands: {auto['dev_check_count']} {auto['dev_check_status']}")
                print(f"  - Makefile targets: {auto['makefile_commands']} {auto['makefile_status']}")
                print(f"  - Trigger rules: {auto['trigger_count']} {auto['trigger_status']}")
                print(f"  - Targets met: {auto['automation_targets_met']}/{auto['max_targets']}")
                print()
        
        print("=" * 60)


def main():
    """"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Friendliness Checker")
    parser.add_argument("--check", choices=['lightweight', 'clarity', 'automation'],
                       help="Specific check to run")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    checker = AIFriendlinessChecker()
    
    if args.check:
        # 
        if args.check == 'lightweight':
            results = {'lightweight': checker.check_lightweight()}
        elif args.check == 'clarity':
            results = {'clarity': checker.check_clarity()}
        elif args.check == 'automation':
            results = {'automation': checker.check_automation()}
    else:
        # 
        results = checker.run_all_checks()
    
    if args.json:
        # 
        if args.check and args.check in results:
            print(json.dumps(results[args.check], indent=2, ensure_ascii=False))
        else:
            print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        checker.print_report(results, args.check)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())