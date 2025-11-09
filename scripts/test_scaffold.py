#!/usr/bin/env python3
"""
测试脚手架生成：为模块生成基础测试文件
"""
import sys
import pathlib
import argparse

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def create_test_structure(module_name):
    """创建测试目录结构"""
    test_dir = pathlib.Path(f'tests/{module_name}')
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建 __init__.py
    init_file = test_dir / '__init__.py'
    if not init_file.exists():
        init_file.write_text('"""Tests for {} module"""\n'.format(module_name), encoding='utf-8')
        print(f"✓ 创建 {init_file}")
    
    # 创建 test_smoke.py
    smoke_test = test_dir / 'test_smoke.py'
    if not smoke_test.exists():
        content = f'''"""
Smoke tests for {module_name} module
"""
import pytest


def test_module_imports():
    """测试：模块可以被导入"""
    # TODO: 根据实际模块路径调整
    # import {module_name}
    assert True


def test_basic_functionality():
    """测试：基本功能正常"""
    # TODO: 实现基础功能测试
    assert True


@pytest.mark.skip(reason="待实现")
def test_edge_cases():
    """测试：边界情况"""
    pass
'''
        smoke_test.write_text(content, encoding='utf-8')
        print(f"✓ 创建 {smoke_test}")
    
    # 创建 conftest.py（可选）
    conftest = test_dir / 'conftest.py'
    if not conftest.exists():
        content = f'''"""
Pytest configuration for {module_name} tests
"""
import pytest


@pytest.fixture
def sample_data():
    """示例测试数据"""
    return {{"key": "value"}}
'''
        conftest.write_text(content, encoding='utf-8')
        print(f"✓ 创建 {conftest}")
    
    return test_dir

def main():
    parser = argparse.ArgumentParser(description='为模块生成测试脚手架')
    parser.add_argument('module', help='模块名称')
    args = parser.parse_args()
    
    module_name = args.module
    
    print(f"🧪 为模块 '{module_name}' 生成测试脚手架...\n")
    
    test_dir = create_test_structure(module_name)
    
    print(f"\n✅ 测试脚手架生成完成: {test_dir}")
    print("\n💡 下一步:")
    print(f"   1. 根据 modules/{module_name}/CONTRACT.md 编写契约测试")
    print(f"   2. 根据 modules/{module_name}/TEST_PLAN.md 补充用例")
    print(f"   3. 运行测试: pytest tests/{module_name}/")

if __name__ == '__main__':
    main()

