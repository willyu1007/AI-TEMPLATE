#!/usr/bin/env python3
"""
文档风格预检脚本
检查项目文档是否符合 agent.md §13 文档编写规范
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

# 模糊表达模式
VAGUE_PATTERNS = [
    (r'有点像', '使用精确描述，如"实现了...模式"'),
    (r'差不多', '使用具体数值或明确描述'),
    (r'类似于', '使用"与...相同"或具体说明差异'),
    (r'大概|大约(?![\d])', '使用精确数值'),
    (r'等等(?![。\n])', '列出完整列表或使用"包括"'),
    (r'之类的', '明确列举或使用具体分类'),
    (r'比较[\u4e00-\u9fa5]{1,3}', '使用具体度量标准'),
    (r'基本上', '使用明确的条件或百分比'),
    (r'一般来说', '使用"通常"或"在...情况下"'),
    (r'可能会', '使用"会"或"在...条件下会"'),
]

# 未标记语言的代码块模式
UNTAGGED_CODE_BLOCK = r'```\s*\n[^`]'

# 标题中的 emoji 模式（不包括状态标记）
EMOJI_IN_HEADING = r'^#{1,6}\s+[🎯📚🔧📝🧩⚡📁🛠️🎓⚠️🚀🤝📄🔗💡🎉🐛📦⚙️🏗️📋📞📜🏆]\s+'

# 语言混用检测（简单版本：一行中既有大量中文又有大量英文句子）
LANGUAGE_MIX_PATTERN = r'[\u4e00-\u9fa5]{10,}.*?[A-Z][a-z]{5,}.*?[A-Z][a-z]{5,}'


def check_file(file_path: Path) -> List[Tuple[int, str, str]]:
    """检查单个文件，返回问题列表 [(行号, 问题类型, 具体内容)]"""
    issues = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # 检查模糊表达
        for line_num, line in enumerate(lines, 1):
            for pattern, suggestion in VAGUE_PATTERNS:
                if re.search(pattern, line):
                    issues.append((line_num, f'模糊表达 "{pattern}"', suggestion))
        
        # 检查未标记语言的代码块（多行检查）
        if re.search(UNTAGGED_CODE_BLOCK, content):
            issues.append((0, '未标记语言的代码块', '所有代码块必须标记语言，如 ```python'))
        
        # 检查标题中的 emoji
        for line_num, line in enumerate(lines, 1):
            if re.match(EMOJI_IN_HEADING, line):
                issues.append((line_num, 'emoji标题前缀', '标题不应使用emoji前缀'))
        
        # 检查文档是否以目标/上下文开头（针对主要文档）
        if file_path.name in ['README.md', 'RUNBOOK.md', 'plan.md', 'CONTRACT.md']:
            # 检查前100行是否包含"目标"或"##"标题
            first_100_lines = '\n'.join(lines[:100])
            if not re.search(r'##\s+(目标|目的|Purpose|Objective)', first_100_lines, re.IGNORECASE):
                issues.append((0, '缺少目标说明', '文档应以明确的目标说明开头'))
        
    except UnicodeDecodeError:
        issues.append((0, '编码错误', '文件不是 UTF-8 编码'))
    except Exception as e:
        issues.append((0, '读取错误', str(e)))
    
    return issues


def scan_docs(base_path: Path = Path('.')) -> Dict[str, List[Tuple[int, str, str]]]:
    """扫描所有 markdown 文档"""
    results = {}
    
    # 要扫描的目录
    scan_dirs = ['docs', 'modules', '.']
    
    for dir_path in scan_dirs:
        full_path = base_path / dir_path
        if not full_path.exists():
            continue
        
        # 根目录只扫描直接子文件
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
    """主函数"""
    import sys
    import io
    
    # Windows控制台编码修复
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 70)
    print("文档风格预检（Documentation Style Check）")
    print("=" * 70)
    print()
    
    results = scan_docs()
    
    if not results:
        print("[OK] 所有文档符合规范！")
        return 0
    
    total_issues = sum(len(issues) for issues in results.values())
    print(f"[WARNING] 发现 {total_issues} 个问题，涉及 {len(results)} 个文件\n")
    
    for file_path, issues in sorted(results.items()):
        print(f"文件: {file_path}")
        for line_num, issue_type, detail in issues:
            if line_num > 0:
                print(f"  第 {line_num} 行: [{issue_type}] {detail}")
            else:
                print(f"  [{issue_type}] {detail}")
        print()
    
    print("=" * 70)
    print("建议：")
    print("1. 参考 agent.md §13 文档编写规范")
    print("2. 使用明确的数值和逻辑连接词")
    print("3. 移除所有装饰性 emoji")
    print("4. 确保文档以目标/上下文开头")
    print("=" * 70)
    
    # 返回非零退出码以阻断 CI
    return 1


if __name__ == '__main__':
    sys.exit(main())

