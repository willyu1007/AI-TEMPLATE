#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""



:
    python scripts/workflow_suggest.py --context ""
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

# UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class WorkflowSuggester:
    """"""
    
    def __init__(self, repo_root: Optional[str] = None):
        """"""
        self.repo_root = Path(repo_root) if repo_root else Path.cwd()
        self.patterns_dir = self.repo_root / "ai" / "workflow-patterns" / "patterns"
        self.patterns = self._load_patterns()
    
    def _load_patterns(self) -> Dict[str, Dict]:
        """"""
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
                print(f":  {pattern_file}: {e}", file=sys.stderr)
        
        return patterns
    
    def analyze_context(self) -> Dict[str, any]:
        """"""
        context = {
            'current_directory': os.getcwd(),
            'git_status': self._get_git_status(),
            'recent_files': self._get_recent_files(),
            'staged_files': self._get_staged_files(),
        }
        return context
    
    def _get_git_status(self) -> List[str]:
        """Git"""
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
        """"""
        try:
            result = subprocess.run(
                ['git', 'log', '--name-only', '--pretty=format:', '-n', str(limit)],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                files = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
                return list(dict.fromkeys(files))[:limit]  # 
            return []
        except:
            return []
    
    def _get_staged_files(self) -> List[str]:
        """"""
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
        """"""
        matches = []
        
        for pattern_id, pattern in self.patterns.items():
            score = 0.0
            
            # 
            # 
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
        
        # 
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    
    def match_prompt(self, prompt: str) -> List[Tuple[str, float]]:
        """prompt"""
        matches = []
        prompt_lower = prompt.lower()
        
        # 
        keyword_rules = {
            'module-creation': [
                (r'(||).{0,5}', 0.9),
                (r'(create|new|add).{0,10}module', 0.9),
                (r'.*', 0.8),
            ],
            'database-migration': [
                (r'(||).{0,5}(||)', 0.9),
                (r'(create|alter|drop).{0,10}table', 0.9),
                (r'.{0,5}(|)', 0.85),
                (r'database.{0,10}(change|migration)', 0.85),
            ],
            'api-development': [
                (r'(||).{0,5}(api|)', 0.9),
                (r'(create|develop|implement).{0,10}api', 0.9),
                (r'restful|graphql', 0.8),
            ],
            'bug-fix': [
                (r'(|).{0,5}(bug||)', 0.9),
                (r'(fix|solve|resolve).{0,10}(bug|issue|error)', 0.9),
                (r'||', 0.8),
            ],
            'refactoring': [
                (r'(|).{0,5}', 0.9),
                (r'refactor|restructure', 0.9),
                (r'.{0,5}(|)', 0.7),
            ],
            'feature-development': [
                (r'(||).{0,5}(|)', 0.9),
                (r'(develop|implement|add).{0,10}feature', 0.9),
                (r'|', 0.8),
            ],
            'performance-optimization': [
                (r'(|).{0,5}', 0.9),
                (r'performance.{0,10}optimi[zs]ation', 0.9),
                (r'(||)', 0.7),
                (r'(slow|lag|latency)', 0.7),
            ],
            'security-audit': [
                (r'(|).{0,5}(|)', 0.9),
                (r'security.{0,10}(audit|check)', 0.9),
                (r'|', 0.8),
            ],
        }
        
        for pattern_id, rules in keyword_rules.items():
            max_score = 0.0
            for pattern, score in rules:
                if re.search(pattern, prompt_lower):
                    max_score = max(max_score, score)
            
            if max_score > 0:
                matches.append((pattern_id, max_score))
        
        # 
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    
    def get_top_suggestions(
        self, 
        context_matches: List[Tuple[str, float]], 
        prompt_matches: List[Tuple[str, float]], 
        top_n: int = 3
    ) -> List[Tuple[str, float, Dict]]:
        """promptTop N"""
        # 
        combined_scores = {}
        
        for pattern_id, score in context_matches:
            combined_scores[pattern_id] = combined_scores.get(pattern_id, 0.0) + score * 0.4
        
        for pattern_id, score in prompt_matches:
            combined_scores[pattern_id] = combined_scores.get(pattern_id, 0.0) + score * 0.6
        
        # Top N
        sorted_patterns = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        
        suggestions = []
        for pattern_id, score in sorted_patterns[:top_n]:
            pattern = self.patterns.get(pattern_id, {})
            suggestions.append((pattern_id, score, pattern))
        
        return suggestions
    
    def show_quick_start(self, pattern_id: str):
        """"""
        pattern = self.patterns.get(pattern_id)
        if not pattern:
            print(f":  {pattern_id} ")
            return
        
        print(f"\n{'='*60}")
        print(f": {pattern.get('name', pattern_id)}")
        print(f": {pattern.get('description', 'N/A')}")
        print(f": {pattern.get('complexity', 'N/A')}")
        print(f": {pattern.get('estimated_time', 'N/A')}")
        print(f"{'='*60}\n")
        
        print("📖 :")
        print(f"  make workflow_show PATTERN={pattern_id}")
        print(f"  make workflow_apply PATTERN={pattern_id}")
        
        print("\n📚 :")
        workflow = pattern.get('workflow', [])
        if workflow and len(workflow) > 0:
            first_step = workflow[0]
            docs = first_step.get('documents_to_load', [])
            for doc in docs[:3]:  # 3
                path = doc.get('path', '')
                priority = doc.get('priority', '')
                print(f"  [{priority:8s}] {path}")
        
        print("\n✅ :")
        checklist = pattern.get('quality_checklist', [])
        for item in checklist[:5]:  # 5
            print(f"  {item}")
        
        print(f"\n💡 : {pattern.get('references', {}).get('detailed_guide', 'N/A')}")
        print()
    
    def generate_checklist(self, pattern_id: str) -> str:
        """Markdown"""
        pattern = self.patterns.get(pattern_id)
        if not pattern:
            return f":  {pattern_id} "
        
        checklist_md = f"# {pattern.get('name', pattern_id)} - \n\n"
        checklist_md += f"> ****: {pattern.get('estimated_time', 'N/A')}\n"
        checklist_md += f"> ****: {pattern.get('complexity', 'N/A')}\n\n"
        
        checklist_md += "## \n\n"
        workflow = pattern.get('workflow', [])
        for step in workflow:
            step_num = step.get('step', '')
            step_name = step.get('name', '')
            estimated_time = step.get('estimated_time', '')
            checklist_md += f"### Step {step_num}: {step_name}\n"
            checklist_md += f"⏱️ {estimated_time}\n\n"
            
            # 
            expected = step.get('expected_output', [])
            if expected:
                checklist_md += "****:\n"
                for item in expected:
                    checklist_md += f"- [ ] {item}\n"
                checklist_md += "\n"
        
        checklist_md += "## \n\n"
        quality_checklist = pattern.get('quality_checklist', [])
        for item in quality_checklist:
            checklist_md += f"{item}\n"
        
        return checklist_md


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--context', '-c', type=str, help='prompt/')
    parser.add_argument('--file', '-f', type=str, help='')
    parser.add_argument('--analyze-context', '-a', action='store_true', help='')
    parser.add_argument('--show', '-s', type=str, help='')
    parser.add_argument('--generate-checklist', '-g', type=str, help='')
    parser.add_argument('--top-n', '-n', type=int, default=3, help='Top N3')
    
    args = parser.parse_args()
    
    # 
    suggester = WorkflowSuggester()
    
    if not suggester.patterns:
        print(": ", file=sys.stderr)
        print(" ai/workflow-patterns/patterns/ ", file=sys.stderr)
        sys.exit(1)
    
    # 
    if args.show:
        suggester.show_quick_start(args.show)
        sys.exit(0)
    
    # 
    if args.generate_checklist:
        checklist = suggester.generate_checklist(args.generate_checklist)
        print(checklist)
        sys.exit(0)
    
    # 
    if args.analyze_context:
        context = suggester.analyze_context()
        print(":")
        print(f"  : {context['current_directory']}")
        print(f"  Git: {len(context['git_status'])} ")
        print(f"  : {len(context['recent_files'])} ")
        if context['recent_files']:
            print("  :")
            for f in context['recent_files'][:5]:
                print(f"    - {f}")
        sys.exit(0)
    
    # 
    context_matches = []
    prompt_matches = []
    
    if args.file:
        context_matches = suggester.match_file_patterns(args.file)
    
    if args.context:
        prompt_matches = suggester.match_prompt(args.context)
    
    if not context_matches and not prompt_matches:
        print(" --context  --file ", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    
    # Top N
    suggestions = suggester.get_top_suggestions(context_matches, prompt_matches, args.top_n)
    
    if not suggestions:
        print("")
        sys.exit(0)
    
    print(f"\n🎯  (Top {args.top_n}):\n")
    
    for i, (pattern_id, score, pattern) in enumerate(suggestions, 1):
        print(f"{i}. {pattern.get('name', pattern_id)}")
        print(f"   : {score:.2f}")
        print(f"   : {pattern.get('description', 'N/A')}")
        print(f"   : {pattern.get('complexity', 'N/A')}")
        print(f"   : {pattern.get('estimated_time', 'N/A')}")
        print(f"   : make workflow_show PATTERN={pattern_id}")
        print(f"   : make workflow_apply PATTERN={pattern_id}")
        print()


if __name__ == '__main__':
    main()

