#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_doc_headers.py - 批量添加文档audience头部

为所有缺少头部声明的文档添加 YAML front matter。

Usage:
    python scripts/add_doc_headers.py --dry-run
    python scripts/add_doc_headers.py --apply
    
Created: 2025-11-09 (Phase 14.3 optimization)
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent

# 文档分类规则
DOC_HEADERS = {
    # AI documents (English)
    'ai': {
        'audience': 'ai',
        'language': 'en',
        'version': 'summary',
        'files': [
            'config/AI_GUIDE.md',
            'doc/process/workdocs-quickstart.md',
            'doc/process/guardrail-quickstart.md',
            'doc/process/dataflow-quickstart.md',
            'doc/process/MOCK_RULES.md',
            'doc/policies/security.md',
            'doc/policies/quality.md',
            'modules/common/USAGE.md',
            'ai/workflow-patterns/README.md',
            'ai/maintenance_reports/health-summary.md',
        ]
    },
    
    # Human documents (Chinese)
    'human': {
        'audience': 'human',
        'language': 'zh',
        'version': 'complete',
        'files': [
            'doc/process/CONVENTIONS.md',
            'doc/process/GUARDRAIL_GUIDE.md',
            'doc/process/WORKDOCS_GUIDE.md',
            'doc/process/DATAFLOW_ANALYSIS_GUIDE.md',
            'doc/process/MOCK_RULES_GUIDE.md',
            'doc/process/HEALTH_MONITORING_GUIDE.md',
            'doc/policies/security_details.md',
            'doc/policies/quality_standards.md',
        ]
    },
    
    # Both audiences
    'both': {
        'audience': 'both',
        'language': 'zh',
        'version': 'summary',
        'files': [
            'README.md',
        ]
    },
    
    # Chinese AI documents (need translation)
    'ai_chinese': {
        'audience': 'ai',
        'language': 'zh',
        'version': 'summary',
        'purpose': '⚠️ To be translated to English',
        'files': [
            'doc/policies/goals.md',
            'doc/policies/safety.md',
            'doc/policies/DOC_ROLES.md',
            'doc/modules/MODULE_TYPES.md',
            'doc/process/DB_CHANGE_GUIDE.md',
            'doc/process/testing.md',
            'doc/process/pr_workflow.md',
            'doc/process/CONFIG_GUIDE.md',
        ]
    },
    
    # Config/reference files
    'config': {
        'audience': 'ai',
        'language': 'en',
        'version': 'config',
        'files': [
            'doc/orchestration/agent-triggers.yaml',
            'ai/workflow-patterns/catalog.yaml',
            'doc/orchestration/registry.yaml',
            'doc/process/HEALTH_CHECK_MODEL.yaml',
        ]
    }
}


def has_yaml_header(file_path: Path) -> bool:
    """检查文件是否已有YAML头部"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            return first_line == '---'
    except:
        return False


def add_header(file_path: Path, audience: str, language: str, version: str, purpose: str = None, full_version: str = None, ai_version: str = None) -> bool:
    """添加YAML头部到文档"""
    try:
        # 读取原内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 构建头部
        header_lines = ['---']
        header_lines.append(f'audience: {audience}')
        header_lines.append(f'language: {language}')
        header_lines.append(f'version: {version}')
        
        if purpose:
            header_lines.append(f'purpose: {purpose}')
        
        if full_version:
            header_lines.append(f'full_version: {full_version}')
        
        if ai_version:
            header_lines.append(f'ai_version: {ai_version}')
        
        header_lines.append('---')
        header_lines.append('')
        
        # 组合新内容
        new_content = '\n'.join(header_lines) + content
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='批量添加文档audience头部')
    parser.add_argument('--dry-run', action='store_true', help='仅显示将要修改的文件，不实际修改')
    parser.add_argument('--apply', action='store_true', help='实际应用修改')
    
    args = parser.parse_args()
    
    if not args.dry_run and not args.apply:
        print("请指定 --dry-run 或 --apply")
        print("用法: python scripts/add_doc_headers.py --dry-run")
        sys.exit(1)
    
    # 统计
    total_files = 0
    skipped_files = 0
    updated_files = 0
    
    print("=" * 70)
    print("📝 Document Header Batch Update")
    print("=" * 70)
    print()
    
    # 处理每个类别
    for category, config in DOC_HEADERS.items():
        print(f"\n📂 Category: {category}")
        print(f"   Audience: {config['audience']}, Language: {config['language']}, Version: {config['version']}")
        print()
        
        for rel_path in config['files']:
            total_files += 1
            file_path = REPO_ROOT / rel_path
            
            if not file_path.exists():
                print(f"  ⚠️  File not found: {rel_path}")
                skipped_files += 1
                continue
            
            if has_yaml_header(file_path):
                print(f"  ⏭️  Already has header: {rel_path}")
                skipped_files += 1
                continue
            
            if args.dry_run:
                print(f"  🔜 Would add header: {rel_path}")
            else:
                # 获取purpose
                purpose = config.get('purpose', f"Documentation for {file_path.stem}")
                
                # 确定full_version或ai_version
                full_version = None
                ai_version = None
                
                if config['audience'] == 'ai' and 'quickstart' in str(file_path):
                    # quickstart -> GUIDE
                    guide_name = str(file_path).replace('quickstart', 'GUIDE').replace('-', '_').upper()
                    if Path(guide_name).exists():
                        full_version = '/' + guide_name
                
                if config['audience'] == 'human' and 'GUIDE' in str(file_path):
                    # GUIDE -> quickstart
                    quickstart_name = str(file_path).replace('GUIDE', 'quickstart').lower()
                    if Path(quickstart_name).exists():
                        ai_version = '/' + quickstart_name
                
                success = add_header(file_path, config['audience'], config['language'], config['version'], purpose, full_version, ai_version)
                
                if success:
                    print(f"  ✅ Added header: {rel_path}")
                    updated_files += 1
                else:
                    print(f"  ❌ Failed: {rel_path}")
                    skipped_files += 1
    
    # 总结
    print()
    print("=" * 70)
    print("📊 Summary")
    print("=" * 70)
    print(f"Total files: {total_files}")
    print(f"Updated: {updated_files}")
    print(f"Skipped: {skipped_files}")
    
    if args.dry_run:
        print()
        print("ℹ️  This was a dry-run. Use --apply to actually modify files.")
    else:
        print()
        print("✅ Headers added successfully!")


if __name__ == "__main__":
    main()

