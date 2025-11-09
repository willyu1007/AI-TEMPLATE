#!/usr/bin/env python3
"""
智能触发器引擎 (Agent Trigger Engine)

功能:
  - 读取agent-triggers.yaml配置
  - 基于文件路径自动匹配触发规则
  - 基于prompt关键词自动匹配触发规则
  - 输出建议加载的文档列表
  - 支持dry-run模式

使用:
  python scripts/agent_trigger.py --file modules/user/models/user.py
  python scripts/agent_trigger.py --prompt "创建一个新的用户模块"
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
    """智能触发器引擎"""
    
    def __init__(self, config_path: str = "doc/orchestration/agent-triggers.yaml"):
        """
        初始化触发器引擎
        
        Args:
            config_path: agent-triggers.yaml配置文件路径
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.repo_root = self._find_repo_root()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载agent-triggers.yaml配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ 配置文件不存在: {self.config_path}", file=sys.stderr)
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ 配置文件格式错误: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _find_repo_root(self) -> Path:
        """查找仓库根目录"""
        current = Path.cwd()
        while current != current.parent:
            if (current / "agent.md").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def match_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        匹配文件路径触发规则
        
        Args:
            file_path: 文件路径（相对或绝对）
        
        Returns:
            匹配的触发规则列表
        """
        # 转换为相对路径
        file_path = self._normalize_path(file_path)
        
        # 读取文件内容（如果存在）
        file_content = self._read_file_safe(file_path)
        
        matched_triggers = []
        
        for trigger_id, trigger_config in self.config.get('triggers', {}).items():
            file_triggers = trigger_config.get('file_triggers', {})
            
            # 检查路径匹配
            if self._match_path_patterns(file_path, file_triggers.get('path_patterns', [])):
                match_reason = f"路径匹配: {file_path}"
                matched_triggers.append(self._build_trigger_result(
                    trigger_id, trigger_config, match_reason
                ))
                continue
            
            # 检查内容匹配
            if file_content and self._match_content_patterns(
                file_content, file_triggers.get('content_patterns', [])
            ):
                match_reason = f"内容匹配: {file_path}"
                matched_triggers.append(self._build_trigger_result(
                    trigger_id, trigger_config, match_reason
                ))
        
        return self._sort_by_priority(matched_triggers)
    
    def match_prompt(self, prompt: str) -> List[Dict[str, Any]]:
        """
        匹配prompt触发规则
        
        Args:
            prompt: 用户输入的prompt
        
        Returns:
            匹配的触发规则列表
        """
        matched_triggers = []
        
        for trigger_id, trigger_config in self.config.get('triggers', {}).items():
            prompt_triggers = trigger_config.get('prompt_triggers', {})
            
            # 检查关键词匹配
            if self._match_keywords(prompt, prompt_triggers.get('keywords', [])):
                match_reason = f"关键词匹配: {trigger_id}"
                matched_triggers.append(self._build_trigger_result(
                    trigger_id, trigger_config, match_reason
                ))
                continue
            
            # 检查意图模式匹配
            if self._match_intent_patterns(prompt, prompt_triggers.get('intent_patterns', [])):
                match_reason = f"意图模式匹配: {trigger_id}"
                matched_triggers.append(self._build_trigger_result(
                    trigger_id, trigger_config, match_reason
                ))
        
        return self._sort_by_priority(matched_triggers)
    
    def _normalize_path(self, path: str) -> str:
        """标准化路径为相对路径"""
        path_obj = Path(path)
        if path_obj.is_absolute():
            try:
                return str(path_obj.relative_to(self.repo_root))
            except ValueError:
                return str(path_obj)
        return path
    
    def _read_file_safe(self, file_path: str) -> str:
        """安全读取文件内容"""
        try:
            full_path = self.repo_root / file_path
            if full_path.exists() and full_path.is_file():
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read(10000)  # 只读取前10KB
        except Exception:
            pass
        return ""
    
    def _match_path_patterns(self, file_path: str, patterns: List[str]) -> bool:
        """匹配路径模式"""
        for pattern in patterns:
            # 支持glob模式
            if fnmatch.fnmatch(file_path, pattern):
                return True
            # 支持简单的**通配符
            pattern_re = pattern.replace('**', '.*').replace('*', '[^/]*')
            if re.search(pattern_re, file_path):
                return True
        return False
    
    def _match_content_patterns(self, content: str, patterns: List[str]) -> bool:
        """匹配内容模式（正则表达式）"""
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _match_keywords(self, prompt: str, keywords: List[str]) -> bool:
        """匹配关键词"""
        prompt_lower = prompt.lower()
        for keyword in keywords:
            if keyword.lower() in prompt_lower:
                return True
        return False
    
    def _match_intent_patterns(self, prompt: str, patterns: List[str]) -> bool:
        """匹配意图模式（正则表达式）"""
        for pattern in patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return True
        return False
    
    def _build_trigger_result(self, trigger_id: str, trigger_config: Dict, reason: str) -> Dict:
        """构建触发结果"""
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
        """按优先级排序"""
        priority_order = self.config.get('config', {}).get('priority_order', 
                                                            ['critical', 'high', 'medium', 'low'])
        priority_map = {p: i for i, p in enumerate(priority_order)}
        return sorted(triggers, key=lambda t: priority_map.get(t['priority'], 99))
    
    def format_output(self, triggers: List[Dict], verbose: bool = False) -> str:
        """格式化输出结果"""
        if not triggers:
            return "ℹ️  未匹配到任何触发规则\n"
        
        lines = []
        lines.append(f"\n🎯 匹配到 {len(triggers)} 个触发规则:\n")
        
        for i, trigger in enumerate(triggers, 1):
            lines.append(f"\n{'='*60}")
            lines.append(f"规则 {i}: {trigger['id']}")
            lines.append(f"{'='*60}")
            lines.append(f"描述: {trigger['description']}")
            lines.append(f"优先级: {trigger['priority']}")
            lines.append(f"强制级别: {trigger['enforcement']}")
            lines.append(f"匹配原因: {trigger['match_reason']}")
            
            # 文档列表
            if trigger['load_documents']:
                lines.append(f"\n📚 建议加载的文档 ({len(trigger['load_documents'])}个):")
                for doc in trigger['load_documents']:
                    priority = doc.get('priority', 'medium')
                    path = doc['path']
                    note = doc.get('note', '')
                    priority_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}
                    icon = priority_icon.get(priority, '⚪')
                    lines.append(f"  {icon} [{priority:8s}] {path}")
                    if note and verbose:
                        lines.append(f"           说明: {note}")
            
            # Guardrail检查
            if trigger['guardrail']:
                lines.append(f"\n🛡️  质量门槛 ({len(trigger['guardrail'])}项):")
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
        检查make命令是否通过
        
        Args:
            command: make命令，如 "make db_lint"
            timeout: 超时时间（秒）
        
        Returns:
            True if命令成功，False if失败
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
            print(f"⏱️  命令超时: {command}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"❌ 命令执行失败: {command} - {e}", file=sys.stderr)
            return False
    
    def check_skip_conditions(self, skip_conditions: Dict[str, Any]) -> Tuple[bool, str]:
        """
        检查跳过条件
        
        Args:
            skip_conditions: 跳过条件配置
        
        Returns:
            (是否可以跳过, 原因说明)
        """
        reasons = []
        
        # 检查make命令
        make_commands = skip_conditions.get('make_commands_passed', [])
        if make_commands:
            all_passed = True
            for cmd in make_commands:
                if not self.check_make_command(cmd):
                    all_passed = False
                    reasons.append(f"✗ 命令未通过: {cmd}")
                else:
                    reasons.append(f"✓ 命令通过: {cmd}")
            
            if all_passed:
                return True, '\n'.join(reasons)
        
        # 检查环境变量
        env_var = skip_conditions.get('env_var')
        if env_var and os.environ.get(env_var):
            reasons.append(f"✓ 环境变量已设置: {env_var}")
            return True, '\n'.join(reasons)
        
        or_env_var = skip_conditions.get('or_env_var')
        if or_env_var and os.environ.get(or_env_var):
            reasons.append(f"✓ 环境变量已设置: {or_env_var}")
            return True, '\n'.join(reasons)
        
        # 检查and_confirmation
        and_confirmation = skip_conditions.get('and_confirmation', False)
        if and_confirmation:
            reasons.append("需要用户确认")
        
        return False, '\n'.join(reasons) if reasons else "未满足跳过条件"
    
    def check_enforcement(self, matched_triggers: List[Dict[str, Any]], 
                         file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        检查enforcement模式并处理Guardrail
        
        Args:
            matched_triggers: 匹配的触发规则列表
            file_path: 文件路径（用于显示）
        
        Returns:
            {
                "action": "allow" | "block" | "warn" | "suggest",
                "message": "提示信息",
                "rule_id": "规则ID",
                "details": "详细信息"
            }
        """
        # 按优先级排序，最高优先级的enforcement生效
        sorted_triggers = self._sort_by_priority(matched_triggers)
        
        for trigger in sorted_triggers:
            enforcement = trigger.get('enforcement', 'suggest')
            rule_id = trigger['id']
            trigger_config = self.config['triggers'][rule_id]
            
            # Block模式
            if enforcement == 'block':
                block_config = trigger_config.get('block_config', {})
                skip_conditions = block_config.get('skip_conditions', {})
                
                # 检查跳过条件
                if skip_conditions:
                    can_skip, reason = self.check_skip_conditions(skip_conditions)
                    if can_skip:
                        return {
                            "action": "allow",
                            "message": f"✅ 跳过Block - 满足跳过条件\n\n{reason}",
                            "rule_id": rule_id,
                            "details": reason
                        }
                    else:
                        return {
                            "action": "block",
                            "message": block_config.get('message', ''),
                            "rule_id": rule_id,
                            "details": f"Block原因:\n{reason}",
                            "require_confirmation": block_config.get('require_confirmation', False),
                            "confirmation_prompt": block_config.get('confirmation_prompt', '')
                        }
                else:
                    # 无跳过条件，直接Block
                    return {
                        "action": "block",
                        "message": block_config.get('message', ''),
                        "rule_id": rule_id,
                        "require_confirmation": block_config.get('require_confirmation', False),
                        "confirmation_prompt": block_config.get('confirmation_prompt', '')
                    }
            
            # Warn模式
            elif enforcement == 'warn':
                warn_config = trigger_config.get('warn_config', {})
                return {
                    "action": "warn",
                    "message": warn_config.get('message', ''),
                    "rule_id": rule_id,
                    "require_confirmation": warn_config.get('require_confirmation', True),
                    "confirmation_prompt": warn_config.get('confirmation_prompt', '继续? (yes/no)')
                }
        
        # 默认：suggest模式
        return {
            "action": "suggest",
            "message": "✅ 无强制限制，建议查看推荐文档",
            "rule_id": None
        }


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='智能触发器引擎 - 自动匹配相关文档',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 匹配文件路径
  python scripts/agent_trigger.py --file modules/user/models/user.py
  
  # 匹配prompt
  python scripts/agent_trigger.py --prompt "创建一个新的用户模块"
  
  # Dry-run模式
  python scripts/agent_trigger.py --file db/migrations/001_up.sql --dry-run
  
  # 详细模式
  python scripts/agent_trigger.py --prompt "修改数据库表结构" --verbose
        """
    )
    
    parser.add_argument('--file', '-f', type=str, help='要检查的文件路径')
    parser.add_argument('--prompt', '-p', type=str, help='要检查的prompt')
    parser.add_argument('--config', '-c', type=str, 
                       default='doc/orchestration/agent-triggers.yaml',
                       help='配置文件路径 (默认: doc/orchestration/agent-triggers.yaml)')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Dry-run模式，仅显示匹配结果')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='详细模式，显示更多信息')
    
    args = parser.parse_args()
    
    # 检查参数
    if not args.file and not args.prompt:
        parser.print_help()
        sys.exit(1)
    
    # 初始化触发器引擎
    try:
        trigger = AgentTrigger(args.config)
    except Exception as e:
        print(f"❌ 初始化失败: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 匹配规则
    matched_triggers = []
    if args.file:
        print(f"🔍 检查文件: {args.file}")
        matched_triggers = trigger.match_file(args.file)
    elif args.prompt:
        print(f"🔍 检查prompt: {args.prompt}")
        matched_triggers = trigger.match_prompt(args.prompt)
    
    # 输出匹配结果
    if not matched_triggers:
        print("ℹ️  未匹配到任何触发规则\n")
        sys.exit(0)
    
    output = trigger.format_output(matched_triggers, verbose=args.verbose)
    print(output)
    
    # Dry-run模式：仅显示匹配结果
    if args.dry_run:
        print("🔍 Dry-run模式：不执行Guardrail检查\n")
        sys.exit(0)
    
    # 检查Guardrail enforcement
    enforcement_result = trigger.check_enforcement(matched_triggers, args.file)
    action = enforcement_result["action"]
    message = enforcement_result["message"]
    rule_id = enforcement_result.get("rule_id")
    
    # Block模式
    if action == "block":
        print("\n" + "="*60)
        print("🛑 BLOCKED")
        print("="*60)
        print(message)
        
        # 检查是否需要确认
        require_confirmation = enforcement_result.get("require_confirmation", False)
        if require_confirmation:
            confirmation_prompt = enforcement_result.get("confirmation_prompt", "继续? (yes/no)")
            print(f"\n{confirmation_prompt}: ", end='')
            user_input = input().strip().lower()
            if user_input == 'yes':
                print("✅ 用户确认继续")
                sys.exit(0)
            else:
                print("❌ 用户拒绝，操作终止")
                sys.exit(1)
        else:
            # 显示详细信息
            if "details" in enforcement_result:
                print(f"\n详细信息:\n{enforcement_result['details']}")
            sys.exit(1)
    
    # Warn模式
    elif action == "warn":
        print("\n" + "="*60)
        print("⚠️  WARNING")
        print("="*60)
        print(message)
        
        # 需要用户确认
        require_confirmation = enforcement_result.get("require_confirmation", True)
        if require_confirmation:
            confirmation_prompt = enforcement_result.get("confirmation_prompt", "继续? (yes/no)")
            print(f"\n{confirmation_prompt}: ", end='')
            user_input = input().strip().lower()
            if user_input == 'yes':
                print("✅ 用户确认继续")
                sys.exit(0)
            else:
                print("❌ 用户拒绝，操作终止")
                sys.exit(1)
        else:
            sys.exit(0)
    
    # Allow或Suggest模式
    else:
        if "details" in enforcement_result and enforcement_result["details"]:
            print(f"\n{enforcement_result['details']}\n")
        print(message)
        sys.exit(0)


if __name__ == "__main__":
    main()

