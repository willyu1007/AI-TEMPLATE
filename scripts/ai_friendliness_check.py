#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_friendliness_check.py - AI友好度检查工具

功能：
1. 检查agent.md轻量化（≤400行，always_read≤150行，≤1文件）
2. 检查文档职责清晰度（AI/Human文档分离）
3. 检查脚本自动化覆盖率（dev_check数量、Makefile命令数）

这是Phase 14新增的行业首创维度，用于评估仓库对AI Agent的友好程度。

用法：
    python scripts/ai_friendliness_check.py
    python scripts/ai_friendliness_check.py --check lightweight --json
    python scripts/ai_friendliness_check.py --check clarity
    python scripts/ai_friendliness_check.py --check automation
    make ai_friendliness_check

Created: 2025-11-09 (Phase 14.2)
"""

import os
import sys
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
AGENT_MD_PATH = REPO_ROOT / "agent.md"
DOC_DIR = REPO_ROOT / "doc"
AI_DIR = REPO_ROOT / "ai"
MAKEFILE_PATH = REPO_ROOT / "Makefile"


class AIFriendlinessChecker:
    """AI友好度检查器"""
    
    def __init__(self):
        """初始化检查器"""
        self.results = {
            "lightweight": {},
            "clarity": {},
            "automation": {},
            "overall_score": 0
        }
    
    def check_lightweight(self) -> Dict[str, Any]:
        """检查agent.md轻量化"""
        print("🔍 检查 agent.md 轻量化...")
        
        result = {
            "root_agent_md_lines": 0,
            "always_read_total_lines": 0,
            "always_read_file_count": 0,
            "thresholds_met": 0,
            "checks": {}
        }
        
        # 检查1: Root agent.md行数
        if AGENT_MD_PATH.exists():
            with open(AGENT_MD_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                result["root_agent_md_lines"] = len(lines)
            
            check1_pass = result["root_agent_md_lines"] <= 400
            result["checks"]["root_agent_md"] = {
                "threshold": 400,
                "actual": result["root_agent_md_lines"],
                "pass": check1_pass,
                "status": "✅" if check1_pass else "❌"
            }
            if check1_pass:
                result["thresholds_met"] += 1
        else:
            result["checks"]["root_agent_md"] = {
                "threshold": 400,
                "actual": 0,
                "pass": False,
                "status": "❌",
                "error": "agent.md不存在"
            }
        
        # 检查2: always_read总行数和文件数
        always_read_files = self._get_always_read_files()
        result["always_read_file_count"] = len(always_read_files)
        
        total_lines = 0
        for file_path in always_read_files:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    total_lines += len(f.readlines())
        
        result["always_read_total_lines"] = total_lines
        
        check2_pass = total_lines <= 150
        result["checks"]["always_read_lines"] = {
            "threshold": 150,
            "actual": total_lines,
            "pass": check2_pass,
            "status": "✅" if check2_pass else "❌"
        }
        if check2_pass:
            result["thresholds_met"] += 1
        
        check3_pass = len(always_read_files) <= 1
        result["checks"]["always_read_files"] = {
            "threshold": 1,
            "actual": len(always_read_files),
            "pass": check3_pass,
            "status": "✅" if check3_pass else "❌"
        }
        if check3_pass:
            result["thresholds_met"] += 1
        
        return result
    
    def _get_always_read_files(self) -> List[Path]:
        """从agent.md中提取always_read的文件列表"""
        if not AGENT_MD_PATH.exists():
            return []
        
        with open(AGENT_MD_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取YAML front matter
        match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
        if not match:
            return []
        
        try:
            yaml_content = yaml.safe_load(match.group(1))
            always_read = yaml_content.get("context_routing", {}).get("always_read", [])
            
            files = []
            for item in always_read:
                if isinstance(item, str):
                    files.append(REPO_ROOT / item)
                elif isinstance(item, dict) and "path" in item:
                    files.append(REPO_ROOT / item["path"])
            
            return files
        except Exception as e:
            print(f"  ⚠️ 解析agent.md YAML失败: {e}", file=sys.stderr)
            return []
    
    def check_doc_role_clarity(self) -> Dict[str, Any]:
        """检查文档职责清晰度（AI/Human文档分离）"""
        print("🔍 检查文档职责清晰度...")
        
        result = {
            "total_docs": 0,
            "ai_docs": 0,
            "human_docs": 0,
            "unclear_docs": 0,
            "clarity_percentage": 0,
            "doc_details": []
        }
        
        # 扫描doc/和ai/目录下的所有Markdown文档
        doc_files = []
        for pattern in ["**/*.md", "**/*.MD"]:
            doc_files.extend(DOC_DIR.glob(pattern))
            if AI_DIR.exists():
                doc_files.extend(AI_DIR.glob(pattern))
        
        # 排除temp目录
        doc_files = [f for f in doc_files if "temp" not in f.parts]
        
        result["total_docs"] = len(doc_files)
        
        for doc_file in doc_files:
            role = self._classify_doc_role(doc_file)
            
            if role == "ai":
                result["ai_docs"] += 1
            elif role == "human":
                result["human_docs"] += 1
            else:
                result["unclear_docs"] += 1
                result["doc_details"].append({
                    "file": str(doc_file.relative_to(REPO_ROOT)),
                    "role": "unclear",
                    "reason": "无法确定文档角色"
                })
        
        # 计算清晰度百分比
        clear_docs = result["ai_docs"] + result["human_docs"]
        result["clarity_percentage"] = (clear_docs / result["total_docs"] * 100) if result["total_docs"] > 0 else 0
        
        return result
    
    def _classify_doc_role(self, doc_file: Path) -> str:
        """分类文档角色（AI文档 vs 人类文档）"""
        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # AI文档标记
            ai_markers = [
                "For AI Agents",
                "AI Document",
                "quickstart",
                "AI-friendly"
            ]
            
            # 人类文档标记
            human_markers = [
                "_GUIDE.md",
                "GUIDE.md",
                "详细指南",
                "完整文档"
            ]
            
            # 检查文件名
            filename = doc_file.name
            if any(marker in filename for marker in ["quickstart", "AI_INDEX"]):
                return "ai"
            if filename.endswith("_GUIDE.md") or filename == "GUIDE.md":
                return "human"
            
            # 检查内容前200行
            lines = content.split('\n')[:200]
            content_sample = '\n'.join(lines)
            
            # 检查标记
            ai_score = sum(1 for marker in ai_markers if marker in content_sample)
            human_score = sum(1 for marker in human_markers if marker in content_sample)
            
            if ai_score > human_score:
                return "ai"
            elif human_score > ai_score:
                return "human"
            else:
                # 根据行数判断（AI文档通常<300行，人类文档>300行）
                if len(lines) <= 300:
                    return "ai"
                else:
                    return "human"
        except Exception as e:
            return "unclear"
    
    def check_script_automation(self) -> Dict[str, Any]:
        """检查脚本自动化覆盖率"""
        print("🔍 检查脚本自动化覆盖率...")
        
        result = {
            "dev_check_count": 0,
            "makefile_commands": 0,
            "trigger_rules": 0,
            "automation_targets_met": 0,
            "targets": {}
        }
        
        # 检查dev_check命令数量
        dev_check_count = self._count_dev_check_commands()
        result["dev_check_count"] = dev_check_count
        result["targets"]["dev_check"] = {
            "target": 21,
            "actual": dev_check_count,
            "met": dev_check_count >= 21
        }
        if dev_check_count >= 21:
            result["automation_targets_met"] += 1
        
        # 检查Makefile命令数量
        makefile_commands = self._count_makefile_commands()
        result["makefile_commands"] = makefile_commands
        result["targets"]["makefile_commands"] = {
            "target": 95,
            "actual": makefile_commands,
            "met": makefile_commands >= 95
        }
        if makefile_commands >= 95:
            result["automation_targets_met"] += 1
        
        # 检查触发规则数量
        trigger_rules = self._count_trigger_rules()
        result["trigger_rules"] = trigger_rules
        result["targets"]["trigger_rules"] = {
            "target": 16,
            "actual": trigger_rules,
            "met": trigger_rules >= 16
        }
        if trigger_rules >= 16:
            result["automation_targets_met"] += 1
        
        return result
    
    def _count_dev_check_commands(self) -> int:
        """统计dev_check中的检查命令数量"""
        if not MAKEFILE_PATH.exists():
            return 0
        
        try:
            with open(MAKEFILE_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找dev_check目标
            match = re.search(r'^dev_check:(.*)$', content, re.MULTILINE)
            if not match:
                return 0
            
            dev_check_line = match.group(1).strip()
            # 统计依赖的命令数量（空格分隔）
            commands = [cmd.strip() for cmd in dev_check_line.split() if cmd.strip()]
            return len(commands)
        except Exception as e:
            print(f"  ⚠️ 统计dev_check命令失败: {e}", file=sys.stderr)
            return 0
    
    def _count_makefile_commands(self) -> int:
        """统计Makefile中的命令数量"""
        if not MAKEFILE_PATH.exists():
            return 0
        
        try:
            with open(MAKEFILE_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 统计以目标定义开头的行（不包含.PHONY）
            pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*:'
            matches = re.findall(pattern, content, re.MULTILINE)
            return len(matches)
        except Exception as e:
            print(f"  ⚠️ 统计Makefile命令失败: {e}", file=sys.stderr)
            return 0
    
    def _count_trigger_rules(self) -> int:
        """统计触发规则数量"""
        trigger_file = REPO_ROOT / "doc" / "orchestration" / "agent-triggers.yaml"
        if not trigger_file.exists():
            return 0
        
        try:
            with open(trigger_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            triggers = data.get("triggers", [])
            return len(triggers)
        except Exception as e:
            print(f"  ⚠️ 统计触发规则失败: {e}", file=sys.stderr)
            return 0
    
    def run_all_checks(self):
        """运行所有检查"""
        print("=" * 70)
        print("🤖 AI Friendliness Check - 开始检查...")
        print("=" * 70)
        
        self.results["lightweight"] = self.check_lightweight()
        self.results["clarity"] = self.check_doc_role_clarity()
        self.results["automation"] = self.check_script_automation()
        
        # 计算总分（简化版）
        lightweight_score = self.results["lightweight"]["thresholds_met"] / 3 * 100
        clarity_score = self.results["clarity"]["clarity_percentage"]
        automation_score = self.results["automation"]["automation_targets_met"] / 3 * 100
        
        self.results["overall_score"] = (lightweight_score + clarity_score + automation_score) / 3
        
        print("\n" + "=" * 70)
        print("✅ AI友好度检查完成！")
        print("=" * 70)
    
    def print_console_report(self):
        """打印控制台报告"""
        print("\n" + "=" * 70)
        print("📊 AI FRIENDLINESS REPORT")
        print("=" * 70)
        
        # 1. Lightweight
        print("\n📏 1. agent.md Lightweight")
        lw = self.results["lightweight"]
        print(f"  Root agent.md行数: {lw['root_agent_md_lines']} "
              f"(阈值: ≤400) {lw['checks']['root_agent_md']['status']}")
        print(f"  always_read总行数: {lw['always_read_total_lines']} "
              f"(阈值: ≤150) {lw['checks']['always_read_lines']['status']}")
        print(f"  always_read文件数: {lw['always_read_file_count']} "
              f"(阈值: ≤1) {lw['checks']['always_read_files']['status']}")
        print(f"  达标数: {lw['thresholds_met']}/3")
        
        # 2. Clarity
        print("\n📚 2. Doc Role Clarity")
        clarity = self.results["clarity"]
        print(f"  总文档数: {clarity['total_docs']}")
        print(f"  AI文档: {clarity['ai_docs']}")
        print(f"  人类文档: {clarity['human_docs']}")
        print(f"  角色不明: {clarity['unclear_docs']}")
        print(f"  清晰度: {clarity['clarity_percentage']:.1f}%")
        
        # 3. Automation
        print("\n⚙️ 3. Script Automation Coverage")
        auto = self.results["automation"]
        print(f"  dev_check检查数: {auto['dev_check_count']} "
              f"(目标: ≥21) {'✅' if auto['dev_check_count'] >= 21 else '❌'}")
        print(f"  Makefile命令数: {auto['makefile_commands']} "
              f"(目标: ≥95) {'✅' if auto['makefile_commands'] >= 95 else '❌'}")
        print(f"  触发规则数: {auto['trigger_rules']} "
              f"(目标: ≥16) {'✅' if auto['trigger_rules'] >= 16 else '❌'}")
        print(f"  达标数: {auto['automation_targets_met']}/3")
        
        # Overall
        print(f"\n🎯 Overall AI Friendliness: {self.results['overall_score']:.1f}/100")
        print("=" * 70)
    
    def print_json_report(self):
        """打印JSON报告"""
        print(json.dumps(self.results, indent=2, ensure_ascii=False))


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Friendliness Check")
    parser.add_argument("--check", choices=["lightweight", "clarity", "automation", "all"],
                       default="all", help="检查类型")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    
    args = parser.parse_args()
    
    checker = AIFriendlinessChecker()
    
    if args.check == "lightweight":
        result = checker.check_lightweight()
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            checker.results["lightweight"] = result
            print(f"\n达标数: {result['thresholds_met']}/3")
    
    elif args.check == "clarity":
        result = checker.check_doc_role_clarity()
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            checker.results["clarity"] = result
            print(f"\n清晰度: {result['clarity_percentage']:.1f}%")
    
    elif args.check == "automation":
        result = checker.check_script_automation()
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            checker.results["automation"] = result
            print(f"\n达标数: {result['automation_targets_met']}/3")
    
    else:  # all
        checker.run_all_checks()
        if args.json:
            checker.print_json_report()
        else:
            checker.print_console_report()
    
    # 根据结果决定退出码
    if args.check == "all":
        if checker.results["overall_score"] < 70:
            sys.exit(1)
        else:
            sys.exit(0)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

