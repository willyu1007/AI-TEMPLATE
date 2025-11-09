#!/usr/bin/env python3
"""
Trigger Visualizer - Generate visual representations of triggers

Purpose:
- Generate trigger matrix (Markdown table)
- Create trigger flow diagram (Mermaid)
- Export coverage report

Usage:
    python scripts/trigger_visualizer.py matrix
    python scripts/trigger_visualizer.py flow
    make trigger_matrix
"""

import sys
import yaml
from pathlib import Path

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def load_config(config_path: Path):
    """Load trigger configuration"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def generate_matrix(config: dict) -> str:
    """Generate trigger matrix as Markdown table"""
    triggers = config.get('triggers', [])
    
    md = "# Script Trigger Matrix\n\n"
    md += "| Script | Category | CI | Git Hook | Manual | Est. Time |\n"
    md += "|--------|----------|----|-----------|---------|-----------|\n"
    
    for trigger in triggers:
        name = trigger['name']
        category = trigger.get('category', '')
        
        # Check trigger types
        trigger_types = trigger.get('triggers', [])
        has_ci = any(t.get('type') in ['push', 'pr'] for t in trigger_types)
        has_git_hook = any(t.get('type') == 'git_hook' for t in trigger_types)
        has_manual = any(t.get('type') == 'manual' for t in trigger_types)
        
        ci_mark = '✓' if has_ci else ''
        git_mark = '✓' if has_git_hook else ''
        manual_mark = '✓' if has_manual else ''
        
        est_time = trigger.get('estimated_time', '')
        
        md += f"| `{name}` | {category} | {ci_mark} | {git_mark} | {manual_mark} | {est_time} |\n"
        
    return md


def main():
    """Main entry point"""
    repo_root = Path(__file__).parent.parent
    config_path = repo_root / 'scripts' / 'trigger-config.yaml'
    
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return 1
        
    config = load_config(config_path)
    
    # Determine command
    command = sys.argv[1] if len(sys.argv) > 1 else 'matrix'
    
    if command == 'matrix':
        matrix_md = generate_matrix(config)
        
        # Save to file
        output_path = repo_root / 'temp' / 'TRIGGER_MATRIX.md'
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(matrix_md)
            
        print(f"✅ Trigger matrix generated: {output_path}")
        print("\nPreview:")
        print(matrix_md)
        
    else:
        print(f"Unknown command: {command}")
        print("Usage: trigger_visualizer.py [matrix]")
        return 1
        
    return 0


if __name__ == '__main__':
    sys.exit(main())

