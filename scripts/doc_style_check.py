#!/usr/bin/env python3
"""

 agent.md §13 
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
VAGUE_PATTERNS = [
    (r'', '"..."'),
    (r'', ''),
    (r'', '"..."'),
    (r'|(?![\d])', ''),
    (r'(?![\n])', '""'),
    (r'', ''),
    (r'[\u4e00-\u9fa5]{1,3}', ''),
    (r'', ''),
    (r'', '"""..."'),
    (r'', '"""..."'),
]

# 
UNTAGGED_CODE_BLOCK = r'```\s*\n[^`]'

#  emoji 
EMOJI_IN_HEADING = r'^#{1,6}\s+[🎯📚🔧📝🧩⚡📁🛠️🎓⚠️🚀🤝📄🔗💡🎉🐛📦⚙️🏗️📋📞📜🏆]\s+'

# 
LANGUAGE_MIX_PATTERN = r'[\u4e00-\u9fa5]{10,}.*?[A-Z][a-z]{5,}.*?[A-Z][a-z]{5,}'


def check_file(file_path: Path) -> List[Tuple[int, str, str]]:
    """ [(, , )]"""
    issues = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # 
        for line_num, line in enumerate(lines, 1):
            for pattern, suggestion in VAGUE_PATTERNS:
                if re.search(pattern, line):
                    issues.append((line_num, f' "{pattern}"', suggestion))
        
        # 
        if re.search(UNTAGGED_CODE_BLOCK, content):
            issues.append((0, '', ' ```python'))
        
        #  emoji
        for line_num, line in enumerate(lines, 1):
            if re.match(EMOJI_IN_HEADING, line):
                issues.append((line_num, 'emoji', 'emoji'))
        
        # /
        if file_path.name in ['README.md', 'RUNBOOK.md', 'plan.md', 'CONTRACT.md']:
            # 100"""##"
            first_100_lines = '\n'.join(lines[:100])
            if not re.search(r'##\s+(||Purpose|Objective)', first_100_lines, re.IGNORECASE):
                issues.append((0, '', ''))
        
    except UnicodeDecodeError:
        issues.append((0, '', ' UTF-8 '))
    except Exception as e:
        issues.append((0, '', str(e)))
    
    return issues


def scan_docs(base_path: Path = Path('.')) -> Dict[str, List[Tuple[int, str, str]]]:
    """ markdown """
    results = {}
    
    # 
    scan_dirs = ['docs', 'modules', '.']
    
    for dir_path in scan_dirs:
        full_path = base_path / dir_path
        if not full_path.exists():
            continue
        
        # 
        if dir_path == '.':
            md_files = [f for f in full_path.glob('*.md')]
        else:
            md_files = full_path.rglob('*.md')
        
        for md_file in md_files:
            issues = check_file(md_file)
            if issues:
                relative_path = md_file.relative_to(base_path)
                results[str(relative_path)] = issues
    
    return results


def main():
    """"""
    import sys
    import io
    
    # Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 70)
    print("Documentation Style Check")
    print("=" * 70)
    print()
    
    results = scan_docs()
    
    if not results:
        print("[OK] ")
        return 0
    
    total_issues = sum(len(issues) for issues in results.values())
    print(f"[WARNING]  {total_issues}  {len(results)} \n")
    
    for file_path, issues in sorted(results.items()):
        print(f": {file_path}")
        for line_num, issue_type, detail in issues:
            if line_num > 0:
                print(f"   {line_num} : [{issue_type}] {detail}")
            else:
                print(f"  [{issue_type}] {detail}")
        print()
    
    print("=" * 70)
    print("")
    print("1.  agent.md §13 ")
    print("2. ")
    print("3.  emoji")
    print("4. /")
    print("=" * 70)
    
    #  CI
    return 1


if __name__ == '__main__':
    sys.exit(main())

