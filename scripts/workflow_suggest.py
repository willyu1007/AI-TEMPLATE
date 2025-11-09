#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作流模式推荐引擎
根据当前操作上下文推荐合适的工作流模式

使用方法:
    python scripts/workflow_suggest.py --context "创建用户模块"
    python scripts/workflow_suggest.py --file "modules/users/core/service.py"
    python scripts/workflow_suggest.py --analyze-context
"""

import os
import sys
import argparse
import yaml
import re
import subprocess
from typing import List, Dict, Tuple, Optional
from pathlib import Path

# 添加UTF-8编码声明
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class WorkflowSuggester:
    """工作流模式推荐引擎"""
    
    def __init__(self, repo_root: Optional[str] = None):
        """初始化推荐引擎"""
        self.repo_root = Path(repo_root) if repo_root else Path.cwd()
        self.patterns_dir = self.repo_root / "ai" / "workflow-patterns" / "patterns"
        self.patterns = self._load_patterns()
    
    def _load_patterns(self) -> Dict[str, Dict]:
        """加载所有模式文件"""
        patterns = {}
        if not self.patterns_dir.exists():
            return patterns
        
        for pattern_file in self.patterns_dir.glob("*.yaml"):
            try:
                with open(pattern_file, 'r', encoding='utf-8') as f:
                    pattern = yaml.safe_load(f)
                    pattern_id = pattern.get('pattern_id')
                    if pattern_id:
                        patterns[pattern_id] = pattern
            except Exception as e:
                print(f"警告: 加载模式文件失败 {pattern_file}: {e}", file=sys.stderr)
        
        return patterns
    
    def analyze_context(self) -> Dict[str, any]:
        """分析当前操作上下文"""
        context = {
            'current_directory': os.getcwd(),
            'git_status': self._get_git_status(),
            'recent_files': self._get_recent_files(),
            'staged_files': self._get_staged_files(),
        }
        return context
    
    def _get_git_status(self) -> List[str]:
        """获取Git状态"""
        try:
            result = subprocess.run(
                ['git', 'status', '--short'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
            return []
        except:
            return []
    
    def _get_recent_files(self, limit: int = 10) -> List[str]:
        """获取最近修改的文件"""
        try:
            result = subprocess.run(
                ['git', 'log', '--name-only', '--pretty=format:', '-n', str(limit)],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                files = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
                return list(dict.fromkeys(files))[:limit]  # 去重并限制数量
            return []
        except:
            return []
    
    def _get_staged_files(self) -> List[str]:
        """获取暂存区文件"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
            return []
        except:
            return []
    
    def match_file_patterns(self, file_path: str) -> List[Tuple[str, float]]:
        """基于文件路径匹配模式"""
        matches = []
        
        for pattern_id, pattern in self.patterns.items():
            score = 0.0
            
            # 检查文件路径模式（如果模式中有定义）
            # 简化版实现：基于路径关键词
            if 'modules/' in file_path and '/core/' in file_path:
                if pattern_id == 'module-creation':
                    score += 0.7
                elif pattern_id == 'api-development' and '/api/' in file_path:
                    score += 0.8
            
            if 'db/engines/' in file_path or 'migrations/' in file_path:
                if pattern_id == 'database-migration':
                    score += 0.9
            
            if '/test' in file_path or 'test_' in file_path:
                if pattern_id in ['bug-fix', 'refactoring']:
                    score += 0.5
            
            if score > 0:
                matches.append((pattern_id, score))
        
        # 按分数排序
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    
    def match_prompt(self, prompt: str) -> List[Tuple[str, float]]:
        """基于prompt匹配模式"""
        matches = []
        prompt_lower = prompt.lower()
        
        # 定义关键词匹配规则
        keyword_rules = {
            'module-creation': [
                (r'(创建|新建|添加).{0,5}模块', 0.9),
                (r'(create|new|add).{0,10}module', 0.9),
                (r'初始化.*模块', 0.8),
            ],
            'database-migration': [
                (r'(创建|修改|删除).{0,5}(表|字段|索引)', 0.9),
                (r'(create|alter|drop).{0,10}table', 0.9),
                (r'数据库.{0,5}(变更|迁移)', 0.85),
                (r'database.{0,10}(change|migration)', 0.85),
            ],
            'api-development': [
                (r'(创建|开发|实现).{0,5}(api|接口)', 0.9),
                (r'(create|develop|implement).{0,10}api', 0.9),
                (r'restful|graphql', 0.8),
            ],
            'bug-fix': [
                (r'(修复|解决).{0,5}(bug|问题|错误)', 0.9),
                (r'(fix|solve|resolve).{0,10}(bug|issue|error)', 0.9),
                (r'报错|异常|崩溃', 0.8),
            ],
            'refactoring': [
                (r'(重构|优化).{0,5}代码', 0.9),
                (r'refactor|restructure', 0.9),
                (r'代码.{0,5}(整理|清理)', 0.7),
            ],
            'feature-development': [
                (r'(开发|实现|添加).{0,5}(功能|特性)', 0.9),
                (r'(develop|implement|add).{0,10}feature', 0.9),
                (r'新功能|新特性', 0.8),
            ],
            'performance-optimization': [
                (r'(性能|速度).{0,5}优化', 0.9),
                (r'performance.{0,10}optimi[zs]ation', 0.9),
                (r'(慢|卡|延迟)', 0.7),
                (r'(slow|lag|latency)', 0.7),
            ],
            'security-audit': [
                (r'(安全|漏洞).{0,5}(审计|检查)', 0.9),
                (r'security.{0,10}(audit|check)', 0.9),
                (r'安全扫描|漏洞修复', 0.8),
            ],
        }
        
        for pattern_id, rules in keyword_rules.items():
            max_score = 0.0
            for pattern, score in rules:
                if re.search(pattern, prompt_lower):
                    max_score = max(max_score, score)
            
            if max_score > 0:
                matches.append((pattern_id, max_score))
        
        # 按分数排序
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    
    def get_top_suggestions(
        self, 
        context_matches: List[Tuple[str, float]], 
        prompt_matches: List[Tuple[str, float]], 
        top_n: int = 3
    ) -> List[Tuple[str, float, Dict]]:
        """合并上下文和prompt匹配，返回Top N推荐"""
        # 合并分数
        combined_scores = {}
        
        for pattern_id, score in context_matches:
            combined_scores[pattern_id] = combined_scores.get(pattern_id, 0.0) + score * 0.4
        
        for pattern_id, score in prompt_matches:
            combined_scores[pattern_id] = combined_scores.get(pattern_id, 0.0) + score * 0.6
        
        # 排序并返回Top N
        sorted_patterns = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        
        suggestions = []
        for pattern_id, score in sorted_patterns[:top_n]:
            pattern = self.patterns.get(pattern_id, {})
            suggestions.append((pattern_id, score, pattern))
        
        return suggestions
    
    def show_quick_start(self, pattern_id: str):
        """显示模式的快速启动命令"""
        pattern = self.patterns.get(pattern_id)
        if not pattern:
            print(f"错误: 模式 {pattern_id} 不存在")
            return
        
        print(f"\n{'='*60}")
        print(f"模式: {pattern.get('name', pattern_id)}")
        print(f"描述: {pattern.get('description', 'N/A')}")
        print(f"复杂度: {pattern.get('complexity', 'N/A')}")
        print(f"预估时间: {pattern.get('estimated_time', 'N/A')}")
        print(f"{'='*60}\n")
        
        print("📖 快速开始命令:")
        print(f"  make workflow_show PATTERN={pattern_id}")
        print(f"  make workflow_apply PATTERN={pattern_id}")
        
        print("\n📚 需要加载的文档:")
        workflow = pattern.get('workflow', [])
        if workflow and len(workflow) > 0:
            first_step = workflow[0]
            docs = first_step.get('documents_to_load', [])
            for doc in docs[:3]:  # 只显示前3个
                path = doc.get('path', '')
                priority = doc.get('priority', '')
                print(f"  [{priority:8s}] {path}")
        
        print("\n✅ 质量检查清单:")
        checklist = pattern.get('quality_checklist', [])
        for item in checklist[:5]:  # 只显示前5个
            print(f"  {item}")
        
        print(f"\n💡 详细参考: {pattern.get('references', {}).get('detailed_guide', 'N/A')}")
        print()
    
    def generate_checklist(self, pattern_id: str) -> str:
        """生成任务清单（Markdown格式）"""
        pattern = self.patterns.get(pattern_id)
        if not pattern:
            return f"错误: 模式 {pattern_id} 不存在"
        
        checklist_md = f"# {pattern.get('name', pattern_id)} - 任务清单\n\n"
        checklist_md += f"> **预估时间**: {pattern.get('estimated_time', 'N/A')}\n"
        checklist_md += f"> **复杂度**: {pattern.get('complexity', 'N/A')}\n\n"
        
        checklist_md += "## 工作流步骤\n\n"
        workflow = pattern.get('workflow', [])
        for step in workflow:
            step_num = step.get('step', '')
            step_name = step.get('name', '')
            estimated_time = step.get('estimated_time', '')
            checklist_md += f"### Step {step_num}: {step_name}\n"
            checklist_md += f"⏱️ {estimated_time}\n\n"
            
            # 添加预期输出
            expected = step.get('expected_output', [])
            if expected:
                checklist_md += "**预期输出**:\n"
                for item in expected:
                    checklist_md += f"- [ ] {item}\n"
                checklist_md += "\n"
        
        checklist_md += "## 质量检查清单\n\n"
        quality_checklist = pattern.get('quality_checklist', [])
        for item in quality_checklist:
            checklist_md += f"{item}\n"
        
        return checklist_md


def main():
    parser = argparse.ArgumentParser(description='工作流模式推荐引擎')
    parser.add_argument('--context', '-c', type=str, help='用户prompt/意图描述')
    parser.add_argument('--file', '-f', type=str, help='正在编辑的文件路径')
    parser.add_argument('--analyze-context', '-a', action='store_true', help='分析当前上下文')
    parser.add_argument('--show', '-s', type=str, help='显示指定模式的快速启动信息')
    parser.add_argument('--generate-checklist', '-g', type=str, help='生成指定模式的任务清单')
    parser.add_argument('--top-n', '-n', type=int, default=3, help='显示Top N推荐（默认3）')
    
    args = parser.parse_args()
    
    # 初始化推荐引擎
    suggester = WorkflowSuggester()
    
    if not suggester.patterns:
        print("错误: 未找到工作流模式文件", file=sys.stderr)
        print("请确保 ai/workflow-patterns/patterns/ 目录存在且包含模式文件", file=sys.stderr)
        sys.exit(1)
    
    # 显示指定模式
    if args.show:
        suggester.show_quick_start(args.show)
        sys.exit(0)
    
    # 生成任务清单
    if args.generate_checklist:
        checklist = suggester.generate_checklist(args.generate_checklist)
        print(checklist)
        sys.exit(0)
    
    # 分析上下文
    if args.analyze_context:
        context = suggester.analyze_context()
        print("当前上下文分析:")
        print(f"  当前目录: {context['current_directory']}")
        print(f"  Git状态: {len(context['git_status'])} 个文件变更")
        print(f"  最近文件: {len(context['recent_files'])} 个")
        if context['recent_files']:
            print("  最近修改的文件:")
            for f in context['recent_files'][:5]:
                print(f"    - {f}")
        sys.exit(0)
    
    # 模式推荐
    context_matches = []
    prompt_matches = []
    
    if args.file:
        context_matches = suggester.match_file_patterns(args.file)
    
    if args.context:
        prompt_matches = suggester.match_prompt(args.context)
    
    if not context_matches and not prompt_matches:
        print("请提供 --context 或 --file 参数", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    
    # 获取Top N推荐
    suggestions = suggester.get_top_suggestions(context_matches, prompt_matches, args.top_n)
    
    if not suggestions:
        print("未找到匹配的工作流模式")
        sys.exit(0)
    
    print(f"\n🎯 推荐的工作流模式 (Top {args.top_n}):\n")
    
    for i, (pattern_id, score, pattern) in enumerate(suggestions, 1):
        print(f"{i}. {pattern.get('name', pattern_id)}")
        print(f"   匹配度: {score:.2f}")
        print(f"   描述: {pattern.get('description', 'N/A')}")
        print(f"   复杂度: {pattern.get('complexity', 'N/A')}")
        print(f"   预估时间: {pattern.get('estimated_time', 'N/A')}")
        print(f"   查看详情: make workflow_show PATTERN={pattern_id}")
        print(f"   应用模式: make workflow_apply PATTERN={pattern_id}")
        print()


if __name__ == '__main__':
    main()

