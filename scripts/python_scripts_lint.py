#!/usr/bin/env python3
"""
Python Scripts Linter - Validates Python scripts quality

Purpose:
- Check for proper shebang
- Verify UTF-8 encoding support (Windows compatibility)
- Check for docstrings
- Detect common anti-patterns
- Validate imports

Usage:
    python scripts/python_scripts_lint.py
    make python_scripts_lint
"""

import ast
import re
import sys
from pathlib import Path
from typing import List, Dict

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class PythonScriptLinter:
    def __init__(self, scripts_dir: Path):
        self.scripts_dir = scripts_dir
        self.errors: Dict[str, List[str]] = {}
        self.warnings: Dict[str, List[str]] = {}
        self.checked_count = 0
        
    def check_file(self, script_path: Path):
        """Check a single Python file"""
        self.checked_count += 1
        file_errors = []
        file_warnings = []
        
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
        except Exception as e:
            file_errors.append(f"Failed to read file: {e}")
            self.errors[script_path.name] = file_errors
            return
            
        # Check shebang
        if lines and not lines[0].startswith('#!'):
            file_warnings.append("Missing shebang (#!/usr/bin/env python3)")
            
        # Check for Windows UTF-8 support
        has_utf8_support = False
        for line in lines[:50]:  # Check first 50 lines
            if 'sys.platform' in line and 'win32' in line:
                has_utf8_support = True
                break
        if not has_utf8_support:
            file_warnings.append(
                "Missing Windows UTF-8 support (sys.stdout = io.TextIOWrapper...)"
            )
            
        # Check for module docstring
        try:
            tree = ast.parse(content)
            has_docstring = ast.get_docstring(tree) is not None
            if not has_docstring:
                file_warnings.append("Missing module docstring")
        except SyntaxError as e:
            file_errors.append(f"Syntax error: {e}")
            
        # Check for main guard
        has_main_guard = 'if __name__' in content
        if not has_main_guard and 'def main' in content:
            file_warnings.append("Has main() but missing if __name__ == '__main__' guard")
            
        # Check for pathlib usage (recommended over os.path)
        if 'import os' in content and 'os.path' in content:
            if 'from pathlib import Path' not in content:
                file_warnings.append("Consider using pathlib.Path instead of os.path")
                
        # Check for print statements in non-main code
        # (Should use logging for library code)
        if 'print(' in content and script_path.stem not in ['__init__', 'setup']:
            # This is expected for scripts, so just info
            pass
            
        # Store results
        if file_errors:
            self.errors[script_path.name] = file_errors
        if file_warnings:
            self.warnings[script_path.name] = file_warnings
            
    def run_checks(self) -> bool:
        """Check all Python scripts"""
        if not self.scripts_dir.exists():
            print(f"❌ Scripts directory not found: {self.scripts_dir}")
            return False
            
        # Find all Python files
        python_files = list(self.scripts_dir.glob('*.py'))
        
        if not python_files:
            print(f"⚠️  No Python scripts found in {self.scripts_dir}")
            return True
            
        for script_path in sorted(python_files):
            # Skip __pycache__ and test files
            if '__pycache__' in str(script_path) or script_path.stem.startswith('test_'):
                continue
            self.check_file(script_path)
            
        return len(self.errors) == 0
        
    def report(self):
        """Print check results"""
        if self.errors:
            print("\n❌ Python Scripts Lint Failed\n")
            print("Errors:")
            for filename, errors in sorted(self.errors.items()):
                print(f"\n  {filename}:")
                for error in errors:
                    print(f"    - {error}")
                    
        if self.warnings:
            print("\n⚠️  Warnings:")
            for filename, warnings in sorted(self.warnings.items()):
                print(f"\n  {filename}:")
                for warning in warnings:
                    print(f"    - {warning}")
                    
        if not self.errors and not self.warnings:
            print(f"✅ Python scripts lint passed ({self.checked_count} files checked)")
            

def main():
    """Main entry point"""
    repo_root = Path(__file__).parent.parent
    scripts_dir = repo_root / 'scripts'
    
    linter = PythonScriptLinter(scripts_dir)
    success = linter.run_checks()
    linter.report()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())

