#!/usr/bin/env python3
"""

 UTF-8 
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
TEXT_EXTENSIONS = {
    '.md', '.py', '.js', '.ts', '.tsx', '.vue', '.go', '.java',
    '.yaml', '.yml', '.json', '.txt', '.sh', '.sql', '.toml',
    '.html', '.css', '.scss', '.xml', '.rst', '.cfg', '.ini'
}

# 
EXCLUDE_DIRS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    'dist', 'build', '.aicontext', '.contracts_baseline',
    'htmlcov', '.pytest_cache', '.mypy_cache'
}


def is_text_file(file_path: Path) -> bool:
    """"""
    return file_path.suffix.lower() in TEXT_EXTENSIONS


def check_file_encoding(file_path: Path) -> Tuple[bool, str]:
    """
    
    : (UTF-8, )
    """
    try:
        #  UTF-8 
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return (True, '')
    except UnicodeDecodeError as e:
        # UTF-8 
        return (False, str(e))
    except Exception as e:
        return (False, f': {str(e)}')


def try_fix_encoding(file_path: Path) -> bool:
    """
    
    : 
    """
    # 
    encodings = ['gbk', 'gb2312', 'gb18030', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for enc in encodings:
        try:
            # 
            with open(file_path, 'r', encoding=enc) as f:
                content = f.read()
            
            #  UTF-8
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read()
            
            print(f"  [OK]  {enc} ")
            return True
        except:
            continue
    
    print(f"  [ERROR] ")
    return False


def scan_repository(base_path: Path = Path('.')) -> List[Tuple[Path, str]]:
    """
    
    : [(, )]
    """
    non_utf8_files = []
    
    for file_path in base_path.rglob('*'):
        # 
        if file_path.is_dir():
            continue
        
        # 
        if any(excluded in file_path.parts for excluded in EXCLUDE_DIRS):
            continue
        
        # 
        if not is_text_file(file_path):
            continue
        
        # 
        is_utf8, error_msg = check_file_encoding(file_path)
        
        if not is_utf8:
            non_utf8_files.append((file_path, error_msg))
    
    return non_utf8_files


def main():
    """"""
    import sys
    import io
    
    # Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 70)
    print("UTF-8 Encoding Check")
    print("=" * 70)
    print()
    
    # 
    print("...")
    non_utf8_files = scan_repository()
    
    if not non_utf8_files:
        print("[OK]  UTF-8 ")
        return 0
    
    # 
    print(f"\n[WARNING]  {len(non_utf8_files)}  UTF-8 \n")
    
    for file_path, error_msg in non_utf8_files:
        print(f": {file_path}")
        print(f"  : {error_msg[:100]}")  # 
        print()
    
    # 
    print("=" * 70)
    response = input(" UTF-8(y/N): ").strip().lower()
    
    if response == 'y':
        print("\n...")
        success_count = 0
        fail_count = 0
        
        for file_path, _ in non_utf8_files:
            print(f": {file_path}")
            if try_fix_encoding(file_path):
                success_count += 1
            else:
                fail_count += 1
        
        print()
        print("=" * 70)
        print(f": {success_count} , {fail_count} ")
        print("=" * 70)
        
        # 
        print("\n...")
        remaining = scan_repository()
        if not remaining:
            print("[OK]  UTF-8 ")
            return 0
        else:
            print(f"[WARNING]  {len(remaining)} ")
            return 1
    else:
        print("\n")
        print(" UTF-8 ")
        return 1


if __name__ == '__main__':
    sys.exit(main())

