#!/usr/bin/env python3
"""
 requirements.txt
Python, Node.js/Vue, Go, C/C++, C#
"""
import sys
import pathlib
import re
from collections import defaultdict

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Python 
PYTHON_DEPS = {
    # 
    'fastapi': {'import': ['fastapi'], 'version': '>=0.100.0', 'desc': 'FastAPI web'},
    'flask': {'import': ['flask'], 'version': '>=2.0.0', 'desc': 'Flask web'},
    'django': {'import': ['django'], 'version': '>=4.0', 'desc': 'Django web'},
    
    # 
    'sqlalchemy': {'import': ['sqlalchemy'], 'version': '>=2.0', 'desc': 'SQL ORM'},
    'psycopg2-binary': {'import': ['psycopg2'], 'version': '>=2.9', 'desc': 'PostgreSQL'},
    'pymongo': {'import': ['pymongo'], 'version': '>=4.0', 'desc': 'MongoDB'},
    'redis': {'import': ['redis'], 'version': '>=4.0', 'desc': 'Redis'},
    
    # 
    'pandas': {'import': ['pandas'], 'version': '>=2.0', 'desc': ''},
    'numpy': {'import': ['numpy'], 'version': '>=1.24', 'desc': ''},
    
    # 
    'pytest': {'import': ['pytest'], 'version': '>=7.0', 'desc': ''},
    'pytest-cov': {'import': ['pytest_cov'], 'version': '>=4.0', 'desc': ''},
    'pytest-asyncio': {'import': ['pytest_asyncio'], 'version': '>=0.21', 'desc': ''},
    
    # 
    'pyyaml': {'import': ['yaml'], 'version': '>=6.0', 'desc': 'YAML'},
    'python-dotenv': {'import': ['dotenv'], 'version': '>=1.0', 'desc': ''},
    'requests': {'import': ['requests'], 'version': '>=2.28', 'desc': 'HTTP'},
    'httpx': {'import': ['httpx'], 'version': '>=0.24', 'desc': 'HTTP'},
    
    # 
    'celery': {'import': ['celery'], 'version': '>=5.3', 'desc': ''},
    
    # AI/ML ()
    'openai': {'import': ['openai'], 'version': '>=1.0', 'desc': 'OpenAI API'},
    'anthropic': {'import': ['anthropic'], 'version': '>=0.5', 'desc': 'Anthropic API'},
}

def scan_python_imports(root_dir='.'):
    """Pythonimport"""
    imports = set()
    
    for py_file in pathlib.Path(root_dir).rglob('*.py'):
        # 
        if any(part in py_file.parts for part in ['venv', 'env', '.venv', 'node_modules', 'build', 'dist']):
            continue
        
        try:
            content = py_file.read_text(encoding='utf-8')
            #  import xxx  from xxx import yyy
            for match in re.finditer(r'^\s*(?:from|import)\s+([a-zA-Z_][a-zA-Z0-9_]*)', content, re.MULTILINE):
                imports.add(match.group(1))
        except:
            continue
    
    return imports

def detect_framework():
    """"""
    frameworks = []
    
    #  Python
    if list(pathlib.Path('.').rglob('*.py')):
        frameworks.append('python')
    
    #  Node.js/Vue
    if pathlib.Path('package.json').exists():
        frameworks.append('nodejs')
        try:
            import json
            pkg = json.loads(pathlib.Path('package.json').read_text())
            if 'vue' in pkg.get('dependencies', {}) or 'vue' in pkg.get('devDependencies', {}):
                frameworks.append('vue')
        except:
            pass
    
    #  Go
    if pathlib.Path('go.mod').exists() or list(pathlib.Path('.').rglob('*.go')):
        frameworks.append('go')
    
    #  C/C++
    if list(pathlib.Path('.').rglob('*.cpp')) or list(pathlib.Path('.').rglob('*.c')) or list(pathlib.Path('.').rglob('*.h')):
        frameworks.append('c/c++')
    
    #  C#
    if list(pathlib.Path('.').rglob('*.csproj')) or list(pathlib.Path('.').rglob('*.cs')):
        frameworks.append('csharp')
    
    return frameworks

def generate_requirements(imports, existing_requirements=None):
    """importsrequirements.txt"""
    detected = []
    
    for pkg, info in PYTHON_DEPS.items():
        # 
        if any(imp in imports for imp in info['import']):
            detected.append((pkg, info['version'], info['desc']))
    
    # requirements
    existing = set()
    if existing_requirements and pathlib.Path(existing_requirements).exists():
        content = pathlib.Path(existing_requirements).read_text()
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # 
                pkg_name = re.split(r'[><=!]', line)[0].strip()
                existing.add(pkg_name)
    
    return detected, existing

def main():
    print("🔍 ...\n")
    
    frameworks = detect_framework()
    print(f": {', '.join(frameworks)}\n")
    
    if 'python' not in frameworks:
        print("⚠️   Python ")
        print("💡  Python  .py ")
        return
    
    print("🔍  Python imports...\n")
    imports = scan_python_imports()
    print(f" {len(imports)}  import\n")
    
    print("📦 ...\n")
    detected, existing = generate_requirements(imports, 'requirements.txt')
    
    if not detected:
        print("✅ ")
        return
    
    # 
    new_deps = [(pkg, ver, desc) for pkg, ver, desc in detected if pkg not in existing]
    existing_deps = [(pkg, ver, desc) for pkg, ver, desc in detected if pkg in existing]
    
    if existing_deps:
        print("✓ :")
        for pkg, ver, desc in existing_deps:
            print(f"  - {pkg}{ver} # {desc}")
        print()
    
    if new_deps:
        print("➕ :")
        for pkg, ver, desc in new_deps:
            print(f"  - {pkg}{ver} # {desc}")
        print()
        
        # 
        response = input(" requirements.txt? (y/N): ").strip().lower()
        
        if response == 'y':
            with open('requirements.txt', 'a', encoding='utf-8') as f:
                f.write('\n# \n')
                for pkg, ver, desc in new_deps:
                    f.write(f'{pkg}{ver}  # {desc}\n')
            print("\n✅  requirements.txt")
        else:
            print("\n💡 :")
            print("echo '# ' >> requirements.txt")
            for pkg, ver, desc in new_deps:
                print(f"echo '{pkg}{ver}  # {desc}' >> requirements.txt")
    else:
        print("✅ requirements.txt ")
    
    # 
    if 'vue' in frameworks or 'nodejs' in frameworks:
        print("\n💡  Node.js/Vue ")
        print("   : package.json")
        print("   : npm install / yarn install / pnpm install")
    
    if 'go' in frameworks:
        print("\n💡  Go ")
        print("   : go.mod")
        print("   : go mod tidy")
    
    if 'c/c++' in frameworks:
        print("\n💡  C/C++ ")
        print("   : CMakeLists.txt / Makefile / vcpkg / conan")
    
    if 'csharp' in frameworks:
        print("\n💡  C# ")
        print("   : *.csproj / packages.config")
        print("   : dotnet restore")

if __name__ == '__main__':
    main()

