#!/usr/bin/env python3
"""
依赖管理器：根据项目技术栈自动补全 requirements.txt
支持：Python, Node.js/Vue, Go, C/C++, C#
"""
import sys
import pathlib
import re
from collections import defaultdict

# Python 依赖检测规则
PYTHON_DEPS = {
    # 核心框架
    'fastapi': {'import': ['fastapi'], 'version': '>=0.100.0', 'desc': 'FastAPI web框架'},
    'flask': {'import': ['flask'], 'version': '>=2.0.0', 'desc': 'Flask web框架'},
    'django': {'import': ['django'], 'version': '>=4.0', 'desc': 'Django web框架'},
    
    # 数据库
    'sqlalchemy': {'import': ['sqlalchemy'], 'version': '>=2.0', 'desc': 'SQL ORM'},
    'psycopg2-binary': {'import': ['psycopg2'], 'version': '>=2.9', 'desc': 'PostgreSQL适配器'},
    'pymongo': {'import': ['pymongo'], 'version': '>=4.0', 'desc': 'MongoDB驱动'},
    'redis': {'import': ['redis'], 'version': '>=4.0', 'desc': 'Redis客户端'},
    
    # 数据处理
    'pandas': {'import': ['pandas'], 'version': '>=2.0', 'desc': '数据分析'},
    'numpy': {'import': ['numpy'], 'version': '>=1.24', 'desc': '数值计算'},
    
    # 测试
    'pytest': {'import': ['pytest'], 'version': '>=7.0', 'desc': '测试框架'},
    'pytest-cov': {'import': ['pytest_cov'], 'version': '>=4.0', 'desc': '测试覆盖率'},
    'pytest-asyncio': {'import': ['pytest_asyncio'], 'version': '>=0.21', 'desc': '异步测试'},
    
    # 工具
    'pyyaml': {'import': ['yaml'], 'version': '>=6.0', 'desc': 'YAML解析'},
    'python-dotenv': {'import': ['dotenv'], 'version': '>=1.0', 'desc': '环境变量管理'},
    'requests': {'import': ['requests'], 'version': '>=2.28', 'desc': 'HTTP客户端'},
    'httpx': {'import': ['httpx'], 'version': '>=0.24', 'desc': '异步HTTP客户端'},
    
    # 任务队列
    'celery': {'import': ['celery'], 'version': '>=5.3', 'desc': '分布式任务队列'},
    
    # AI/ML (可选)
    'openai': {'import': ['openai'], 'version': '>=1.0', 'desc': 'OpenAI API客户端'},
    'anthropic': {'import': ['anthropic'], 'version': '>=0.5', 'desc': 'Anthropic API客户端'},
}

def scan_python_imports(root_dir='.'):
    """扫描Python文件中的import语句"""
    imports = set()
    
    for py_file in pathlib.Path(root_dir).rglob('*.py'):
        # 跳过虚拟环境和构建目录
        if any(part in py_file.parts for part in ['venv', 'env', '.venv', 'node_modules', 'build', 'dist']):
            continue
        
        try:
            content = py_file.read_text(encoding='utf-8')
            # 匹配 import xxx 和 from xxx import yyy
            for match in re.finditer(r'^\s*(?:from|import)\s+([a-zA-Z_][a-zA-Z0-9_]*)', content, re.MULTILINE):
                imports.add(match.group(1))
        except:
            continue
    
    return imports

def detect_framework():
    """检测项目使用的技术栈"""
    frameworks = []
    
    # 检测 Python
    if list(pathlib.Path('.').rglob('*.py')):
        frameworks.append('python')
    
    # 检测 Node.js/Vue
    if pathlib.Path('package.json').exists():
        frameworks.append('nodejs')
        try:
            import json
            pkg = json.loads(pathlib.Path('package.json').read_text())
            if 'vue' in pkg.get('dependencies', {}) or 'vue' in pkg.get('devDependencies', {}):
                frameworks.append('vue')
        except:
            pass
    
    # 检测 Go
    if pathlib.Path('go.mod').exists() or list(pathlib.Path('.').rglob('*.go')):
        frameworks.append('go')
    
    # 检测 C/C++
    if list(pathlib.Path('.').rglob('*.cpp')) or list(pathlib.Path('.').rglob('*.c')) or list(pathlib.Path('.').rglob('*.h')):
        frameworks.append('c/c++')
    
    # 检测 C#
    if list(pathlib.Path('.').rglob('*.csproj')) or list(pathlib.Path('.').rglob('*.cs')):
        frameworks.append('csharp')
    
    return frameworks

def generate_requirements(imports, existing_requirements=None):
    """根据检测到的imports生成requirements.txt"""
    detected = []
    
    for pkg, info in PYTHON_DEPS.items():
        # 检查是否使用了该包
        if any(imp in imports for imp in info['import']):
            detected.append((pkg, info['version'], info['desc']))
    
    # 读取现有requirements
    existing = set()
    if existing_requirements and pathlib.Path(existing_requirements).exists():
        content = pathlib.Path(existing_requirements).read_text()
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # 提取包名（去除版本）
                pkg_name = re.split(r'[><=!]', line)[0].strip()
                existing.add(pkg_name)
    
    return detected, existing

def main():
    print("🔍 检测项目技术栈...\n")
    
    frameworks = detect_framework()
    print(f"检测到的技术栈: {', '.join(frameworks)}\n")
    
    if 'python' not in frameworks:
        print("⚠️  未检测到 Python 项目")
        print("💡 如果这是一个 Python 项目，请确保有 .py 文件")
        return
    
    print("🔍 扫描 Python imports...\n")
    imports = scan_python_imports()
    print(f"发现 {len(imports)} 个独特的 import\n")
    
    print("📦 分析依赖需求...\n")
    detected, existing = generate_requirements(imports, 'requirements.txt')
    
    if not detected:
        print("✅ 未检测到需要添加的依赖")
        return
    
    # 分类：新增和已存在
    new_deps = [(pkg, ver, desc) for pkg, ver, desc in detected if pkg not in existing]
    existing_deps = [(pkg, ver, desc) for pkg, ver, desc in detected if pkg in existing]
    
    if existing_deps:
        print("✓ 已存在的依赖:")
        for pkg, ver, desc in existing_deps:
            print(f"  - {pkg}{ver} # {desc}")
        print()
    
    if new_deps:
        print("➕ 建议添加的依赖:")
        for pkg, ver, desc in new_deps:
            print(f"  - {pkg}{ver} # {desc}")
        print()
        
        # 询问是否添加
        response = input("是否自动添加到 requirements.txt? (y/N): ").strip().lower()
        
        if response == 'y':
            with open('requirements.txt', 'a', encoding='utf-8') as f:
                f.write('\n# 自动检测的依赖\n')
                for pkg, ver, desc in new_deps:
                    f.write(f'{pkg}{ver}  # {desc}\n')
            print("\n✅ 已更新 requirements.txt")
        else:
            print("\n💡 手动添加命令:")
            print("echo '# 自动检测的依赖' >> requirements.txt")
            for pkg, ver, desc in new_deps:
                print(f"echo '{pkg}{ver}  # {desc}' >> requirements.txt")
    else:
        print("✅ requirements.txt 已包含所有检测到的依赖")
    
    # 其他技术栈提示
    if 'vue' in frameworks or 'nodejs' in frameworks:
        print("\n💡 检测到 Node.js/Vue 项目")
        print("   依赖管理: package.json")
        print("   安装命令: npm install / yarn install / pnpm install")
    
    if 'go' in frameworks:
        print("\n💡 检测到 Go 项目")
        print("   依赖管理: go.mod")
        print("   更新命令: go mod tidy")
    
    if 'c/c++' in frameworks:
        print("\n💡 检测到 C/C++ 项目")
        print("   依赖管理: CMakeLists.txt / Makefile / vcpkg / conan")
    
    if 'csharp' in frameworks:
        print("\n💡 检测到 C# 项目")
        print("   依赖管理: *.csproj / packages.config")
        print("   更新命令: dotnet restore")

if __name__ == '__main__':
    main()

