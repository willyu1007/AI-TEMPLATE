#!/usr/bin/env python3
"""
 (Agent Trigger Engine)

:
  - agent-triggers.yaml
  - 
  - prompt
  - 
  - dry-run

:
  python scripts/agent_trigger.py --file modules/user/models/user.py
  python scripts/agent_trigger.py --prompt ""
  python scripts/agent_trigger.py --file db/migrations/001_up.sql --dry-run

Created: 2025-11-08 (Phase 10.1)
"""

import os
import sys
import re
import yaml
import fnmatch
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple, Optional
from collections import defaultdict

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class AgentTrigger:
    """"""
    
    def __init__(self, config_path: str = "doc/orchestration/agent-triggers.yaml"):
        """
        
        
        Args:
            config_path: agent-triggers.yaml
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.repo_root = self._find_repo_root()
        
    def _load_config(self) -> Dict[str, Any]:
        """agent-triggers.yaml"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ : {self.config_path}", file=sys.stderr)
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ : {e}", file=sys.stderr)
            sys.exit(1)
    
    def _find_repo_root(self) -> Path:
        """"""
        current = Path.cwd()
        while current != current.parent:
            if (current / "agent.md").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def match_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        
        
        Args:
            file_path: 
        
        Returns:
            
        """
        # 
        file_path = self._normalize_path(file_path)
        
        # 
        file_content = self._read_file_safe(file_path)
        
        matched_triggers = []
        
        for trigger_id, trigger_config in self.config.get('triggers', {}).items():
            file_triggers = trigger_config.get('file_triggers', {})
            
            # 
            if self._match_path_patterns(file_path, file_triggers.get('path_patterns', [])):
                match_reason = f": {file_path}"
                matched_triggers.append(self._build_trigger_result(
                    trigger_id, trigger_config, match_reason
                ))
                continue
            
            # 
            if file_content and self._match_content_patterns(
                file_content, file_triggers.get('content_patterns', [])
            ):
                match_reason = f": {file_path}"
                matched_triggers.append(self._build_trigger_result(
                    trigger_id, trigger_config, match_reason
                ))
        
        return self._sort_by_priority(matched_triggers)
    
    def match_prompt(self, prompt: str) -> List[Dict[str, Any]]:
        """
        prompt
        
        Args:
            prompt: prompt
        
        Returns:
            
        """
        matched_triggers = []
        
        for trigger_id, trigger_config in self.config.get('triggers', {}).items():
            prompt_triggers = trigger_config.get('prompt_triggers', {})
            
            # 
            if self._match_keywords(prompt, prompt_triggers.get('keywords', [])):
                match_reason = f": {trigger_id}"
                matched_triggers.append(self._build_trigger_result(
                    trigger_id, trigger_config, match_reason
                ))
                continue
            
            # 
            if self._match_intent_patterns(prompt, prompt_triggers.get('intent_patterns', [])):
                match_reason = f": {trigger_id}"
                matched_triggers.append(self._build_trigger_result(
                    trigger_id, trigger_config, match_reason
                ))
        
        return self._sort_by_priority(matched_triggers)
    
    def _normalize_path(self, path: str) -> str:
        """"""
        path_obj = Path(path)
        if path_obj.is_absolute():
            try:
                return str(path_obj.relative_to(self.repo_root))
            except ValueError:
                return str(path_obj)
        return path
    
    def _read_file_safe(self, file_path: str) -> str:
        """"""
        try:
            full_path = self.repo_root / file_path
            if full_path.exists() and full_path.is_file():
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read(10000)  # 10KB
        except Exception:
            pass
        return ""
    
    def _match_path_patterns(self, file_path: str, patterns: List[str]) -> bool:
        """"""
        for pattern in patterns:
            # glob
            if fnmatch.fnmatch(file_path, pattern):
                return True
            # **
            pattern_re = pattern.replace('**', '.*').replace('*', '[^/]*')
            if re.search(pattern_re, file_path):
                return True
        return False
    
    def _match_content_patterns(self, content: str, patterns: List[str]) -> bool:
        """"""
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _match_keywords(self, prompt: str, keywords: List[str]) -> bool:
        """"""
        prompt_lower = prompt.lower()
        for keyword in keywords:
            if keyword.lower() in prompt_lower:
                return True
        return False
    
    def _match_intent_patterns(self, prompt: str, patterns: List[str]) -> bool:
        """"""
        for pattern in patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return True
        return False
    
    def _build_trigger_result(self, trigger_id: str, trigger_config: Dict, reason: str) -> Dict:
        """"""
        return {
            'id': trigger_id,
            'description': trigger_config.get('description', ''),
            'priority': trigger_config.get('priority', 'medium'),
            'enforcement': trigger_config.get('enforcement', 'suggest'),
            'match_reason': reason,
            'load_documents': trigger_config.get('load_documents', []),
            'guardrail': trigger_config.get('guardrail', [])
        }
    
    def _sort_by_priority(self, triggers: List[Dict]) -> List[Dict]:
        """"""
        priority_order = self.config.get('config', {}).get('priority_order', 
                                                            ['critical', 'high', 'medium', 'low'])
        priority_map = {p: i for i, p in enumerate(priority_order)}
        return sorted(triggers, key=lambda t: priority_map.get(t['priority'], 99))
    
    def format_output(self, triggers: List[Dict], verbose: bool = False) -> str:
        """"""
        if not triggers:
            return "ℹ️  \n"
        
        lines = []
        lines.append(f"\n🎯  {len(triggers)} :\n")
        
        for i, trigger in enumerate(triggers, 1):
            lines.append(f"\n{'='*60}")
            lines.append(f" {i}: {trigger['id']}")
            lines.append(f"{'='*60}")
            lines.append(f": {trigger['description']}")
            lines.append(f": {trigger['priority']}")
            lines.append(f": {trigger['enforcement']}")
            lines.append(f": {trigger['match_reason']}")
            
            # 
            if trigger['load_documents']:
                lines.append(f"\n📚  ({len(trigger['load_documents'])}):")
                for doc in trigger['load_documents']:
                    priority = doc.get('priority', 'medium')
                    path = doc['path']
                    note = doc.get('note', '')
                    priority_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}
                    icon = priority_icon.get(priority, '⚪')
                    lines.append(f"  {icon} [{priority:8s}] {path}")
                    if note and verbose:
                        lines.append(f"           : {note}")
            
            # Guardrail
            if trigger['guardrail']:
                lines.append(f"\n🛡️   ({len(trigger['guardrail'])}):")
                for check in trigger['guardrail']:
                    enforcement = check.get('enforcement', 'suggest')
                    message = check.get('message', '')
                    check_cmd = check.get('check', '')
                    lines.append(f"  [{enforcement:7s}] {check_cmd}")
                    lines.append(f"           {message}")
        
        lines.append(f"\n{'='*60}\n")
        return '\n'.join(lines)
    
    def check_make_command(self, command: str, timeout: int = 30) -> bool:
        """
        make
        
        Args:
            command: make "make db_lint"
            timeout: 
        
        Returns:
            True ifFalse if
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                timeout=timeout,
                cwd=self.repo_root
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"⏱️  : {command}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"❌ : {command} - {e}", file=sys.stderr)
            return False
    
    def check_skip_conditions(self, skip_conditions: Dict[str, Any]) -> Tuple[bool, str]:
        """
        
        
        Args:
            skip_conditions: 
        
        Returns:
            (, )
        """
        reasons = []
        
        # make
        make_commands = skip_conditions.get('make_commands_passed', [])
        if make_commands:
            all_passed = True
            for cmd in make_commands:
                if not self.check_make_command(cmd):
                    all_passed = False
                    reasons.append(f"✗ : {cmd}")
                else:
                    reasons.append(f"✓ : {cmd}")
            
            if all_passed:
                return True, '\n'.join(reasons)
        
        # 
        env_var = skip_conditions.get('env_var')
        if env_var and os.environ.get(env_var):
            reasons.append(f"✓ : {env_var}")
            return True, '\n'.join(reasons)
        
        or_env_var = skip_conditions.get('or_env_var')
        if or_env_var and os.environ.get(or_env_var):
            reasons.append(f"✓ : {or_env_var}")
            return True, '\n'.join(reasons)
        
        # and_confirmation
        and_confirmation = skip_conditions.get('and_confirmation', False)
        if and_confirmation:
            reasons.append("")
        
        return False, '\n'.join(reasons) if reasons else ""
    
    def check_enforcement(self, matched_triggers: List[Dict[str, Any]], 
                         file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        enforcementGuardrail
        
        Args:
            matched_triggers: 
            file_path: 
        
        Returns:
            {
                "action": "allow" | "block" | "warn" | "suggest",
                "message": "",
                "rule_id": "ID",
                "details": ""
            }
        """
        # enforcement
        sorted_triggers = self._sort_by_priority(matched_triggers)
        
        for trigger in sorted_triggers:
            enforcement = trigger.get('enforcement', 'suggest')
            rule_id = trigger['id']
            trigger_config = self.config['triggers'][rule_id]
            
            # Block
            if enforcement == 'block':
                block_config = trigger_config.get('block_config', {})
                skip_conditions = block_config.get('skip_conditions', {})
                
                # 
                if skip_conditions:
                    can_skip, reason = self.check_skip_conditions(skip_conditions)
                    if can_skip:
                        return {
                            "action": "allow",
                            "message": f"✅ Block - \n\n{reason}",
                            "rule_id": rule_id,
                            "details": reason
                        }
                    else:
                        return {
                            "action": "block",
                            "message": block_config.get('message', ''),
                            "rule_id": rule_id,
                            "details": f"Block:\n{reason}",
                            "require_confirmation": block_config.get('require_confirmation', False),
                            "confirmation_prompt": block_config.get('confirmation_prompt', '')
                        }
                else:
                    # Block
                    return {
                        "action": "block",
                        "message": block_config.get('message', ''),
                        "rule_id": rule_id,
                        "require_confirmation": block_config.get('require_confirmation', False),
                        "confirmation_prompt": block_config.get('confirmation_prompt', '')
                    }
            
            # Warn
            elif enforcement == 'warn':
                warn_config = trigger_config.get('warn_config', {})
                return {
                    "action": "warn",
                    "message": warn_config.get('message', ''),
                    "rule_id": rule_id,
                    "require_confirmation": warn_config.get('require_confirmation', True),
                    "confirmation_prompt": warn_config.get('confirmation_prompt', '? (yes/no)')
                }
        
        # suggest
        return {
            "action": "suggest",
            "message": "✅ ",
            "rule_id": None
        }


def main():
    """"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description=' - ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
:
  # 
  python scripts/agent_trigger.py --file modules/user/models/user.py
  
  # prompt
  python scripts/agent_trigger.py --prompt ""
  
  # Dry-run
  python scripts/agent_trigger.py --file db/migrations/001_up.sql --dry-run
  
  # 
  python scripts/agent_trigger.py --prompt "" --verbose
        """
    )
    
    parser.add_argument('--file', '-f', type=str, help='')
    parser.add_argument('--prompt', '-p', type=str, help='prompt')
    parser.add_argument('--config', '-c', type=str, 
                       default='doc/orchestration/agent-triggers.yaml',
                       help=' (: doc/orchestration/agent-triggers.yaml)')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Dry-run')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='')
    
    args = parser.parse_args()
    
    # 
    if not args.file and not args.prompt:
        parser.print_help()
        sys.exit(1)
    
    # 
    try:
        trigger = AgentTrigger(args.config)
    except Exception as e:
        print(f"❌ : {e}", file=sys.stderr)
        sys.exit(1)
    
    # 
    matched_triggers = []
    if args.file:
        print(f"🔍 : {args.file}")
        matched_triggers = trigger.match_file(args.file)
    elif args.prompt:
        print(f"🔍 prompt: {args.prompt}")
        matched_triggers = trigger.match_prompt(args.prompt)
    
    # 
    if not matched_triggers:
        print("ℹ️  \n")
        sys.exit(0)
    
    output = trigger.format_output(matched_triggers, verbose=args.verbose)
    print(output)
    
    # Dry-run
    if args.dry_run:
        print("🔍 Dry-runGuardrail\n")
        sys.exit(0)
    
    # Guardrail enforcement
    enforcement_result = trigger.check_enforcement(matched_triggers, args.file)
    action = enforcement_result["action"]
    message = enforcement_result["message"]
    rule_id = enforcement_result.get("rule_id")
    
    # Block
    if action == "block":
        print("\n" + "="*60)
        print("🛑 BLOCKED")
        print("="*60)
        print(message)
        
        # 
        require_confirmation = enforcement_result.get("require_confirmation", False)
        if require_confirmation:
            confirmation_prompt = enforcement_result.get("confirmation_prompt", "? (yes/no)")
            print(f"\n{confirmation_prompt}: ", end='')
            user_input = input().strip().lower()
            if user_input == 'yes':
                print("✅ ")
                sys.exit(0)
            else:
                print("❌ ")
                sys.exit(1)
        else:
            # 
            if "details" in enforcement_result:
                print(f"\n:\n{enforcement_result['details']}")
            sys.exit(1)
    
    # Warn
    elif action == "warn":
        print("\n" + "="*60)
        print("⚠️  WARNING")
        print("="*60)
        print(message)
        
        # 
        require_confirmation = enforcement_result.get("require_confirmation", True)
        if require_confirmation:
            confirmation_prompt = enforcement_result.get("confirmation_prompt", "? (yes/no)")
            print(f"\n{confirmation_prompt}: ", end='')
            user_input = input().strip().lower()
            if user_input == 'yes':
                print("✅ ")
                sys.exit(0)
            else:
                print("❌ ")
                sys.exit(1)
        else:
            sys.exit(0)
    
    # AllowSuggest
    else:
        if "details" in enforcement_result and enforcement_result["details"]:
            print(f"\n{enforcement_result['details']}\n")
        print(message)
        sys.exit(0)


if __name__ == "__main__":
    main()

