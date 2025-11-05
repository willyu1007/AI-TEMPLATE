#!/usr/bin/env python3
"""
全库编码检查和修复脚本
检查所有文本文件是否为 UTF-8 编码，并提供修复选项
"""

import sys
from pathlib import Path
from typing import List, Tuple

# 要检查的文件扩展名
TEXT_EXTENSIONS = {
    '.md', '.py', '.js', '.ts', '.tsx', '.vue', '.go', '.java',
    '.yaml', '.yml', '.json', '.txt', '.sh', '.sql', '.toml',
    '.html', '.css', '.scss', '.xml', '.rst', '.cfg', '.ini'
}

# 排除的目录
EXCLUDE_DIRS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    'dist', 'build', '.aicontext', '.contracts_baseline',
    'htmlcov', '.pytest_cache', '.mypy_cache'
}


def is_text_file(file_path: Path) -> bool:
    """判断是否为文本文件"""
    return file_path.suffix.lower() in TEXT_EXTENSIONS


def check_file_encoding(file_path: Path) -> Tuple[bool, str]:
    """
    检查文件编码
    返回: (是否UTF-8, 错误信息)
    """
    try:
        # 尝试以 UTF-8 读取
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return (True, '')
    except UnicodeDecodeError as e:
        # UTF-8 读取失败
        return (False, str(e))
    except Exception as e:
        return (False, f'读取错误: {str(e)}')


def try_fix_encoding(file_path: Path) -> bool:
    """
    尝试修复文件编码
    返回: 是否成功
    """
    # 尝试常见编码
    encodings = ['gbk', 'gb2312', 'gb18030', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for enc in encodings:
        try:
            # 尝试读取
            with open(file_path, 'r', encoding=enc) as f:
                content = f.read()
            
            # 写入 UTF-8
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 验证转换
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read()
            
            print(f"  [OK] 成功（从 {enc} 转换）")
            return True
        except:
            continue
    
    print(f"  [ERROR] 转换失败：无法识别原始编码")
    return False


def scan_repository(base_path: Path = Path('.')) -> List[Tuple[Path, str]]:
    """
    扫描仓库中的所有文本文件
    返回: [(文件路径, 错误信息)]
    """
    non_utf8_files = []
    
    for file_path in base_path.rglob('*'):
        # 跳过目录
        if file_path.is_dir():
            continue
        
        # 跳过排除的目录
        if any(excluded in file_path.parts for excluded in EXCLUDE_DIRS):
            continue
        
        # 只检查文本文件
        if not is_text_file(file_path):
            continue
        
        # 检查编码
        is_utf8, error_msg = check_file_encoding(file_path)
        
        if not is_utf8:
            non_utf8_files.append((file_path, error_msg))
    
    return non_utf8_files


def main():
    """主函数"""
    import sys
    import io
    
    # Windows控制台编码修复
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 70)
    print("全库编码检查（UTF-8 Encoding Check）")
    print("=" * 70)
    print()
    
    # 扫描文件
    print("正在扫描文件...")
    non_utf8_files = scan_repository()
    
    if not non_utf8_files:
        print("[OK] 所有文本文件都是 UTF-8 编码！")
        return 0
    
    # 显示问题文件
    print(f"\n[WARNING] 发现 {len(non_utf8_files)} 个非 UTF-8 编码的文件：\n")
    
    for file_path, error_msg in non_utf8_files:
        print(f"文件: {file_path}")
        print(f"  错误: {error_msg[:100]}")  # 限制错误信息长度
        print()
    
    # 询问是否自动修复
    print("=" * 70)
    response = input("是否尝试自动转换为 UTF-8？(y/N): ").strip().lower()
    
    if response == 'y':
        print("\n开始转换...")
        success_count = 0
        fail_count = 0
        
        for file_path, _ in non_utf8_files:
            print(f"转换: {file_path}")
            if try_fix_encoding(file_path):
                success_count += 1
            else:
                fail_count += 1
        
        print()
        print("=" * 70)
        print(f"转换完成: {success_count} 成功, {fail_count} 失败")
        print("=" * 70)
        
        # 重新检查
        print("\n重新检查...")
        remaining = scan_repository()
        if not remaining:
            print("[OK] 所有文件现在都是 UTF-8 编码！")
            return 0
        else:
            print(f"[WARNING] 仍有 {len(remaining)} 个文件转换失败")
            return 1
    else:
        print("\n取消转换。")
        print("建议：手动检查这些文件并转换为 UTF-8 编码。")
        return 1


if __name__ == '__main__':
    sys.exit(main())

