#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
secret_scan.py - 密钥泄露扫描工具

功能：
1. 扫描代码中的密钥、密码、API key等敏感信息
2. 扫描配置文件中的密钥
3. 扫描文档中的密钥
4. 检查.env文件是否被.gitignore

扫描模式（根据HEALTH_CHECK_MODEL.yaml）：
- 代码中无密钥
- 配置中无密钥
- 文档中无密钥
- .env文件已被gitignore

用法：
    python scripts/secret_scan.py
    python scripts/secret_scan.py --json
    python scripts/secret_scan.py --path modules/
    make secret_scan

Created: 2025-11-09 (Phase 14.2)
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent

# 密钥检测模式
SECRET_PATTERNS = [
    # API Keys
    (r'api[_-]?key\s*[=:]\s*[\'"]([a-zA-Z0-9_\-]{20,})[\'"]', 'API Key'),
    (r'apikey\s*[=:]\s*[\'"]([a-zA-Z0-9_\-]{20,})[\'"]', 'API Key'),
    
    # Passwords
    (r'password\s*[=:]\s*[\'"]([^\'"]{8,})[\'"]', 'Password'),
    (r'passwd\s*[=:]\s*[\'"]([^\'"]{8,})[\'"]', 'Password'),
    (r'pwd\s*[=:]\s*[\'"]([^\'"]{8,})[\'"]', 'Password'),
    
    # Tokens
    (r'token\s*[=:]\s*[\'"]([a-zA-Z0-9_\-\.]{20,})[\'"]', 'Token'),
    (r'access[_-]?token\s*[=:]\s*[\'"]([a-zA-Z0-9_\-\.]{20,})[\'"]', 'Access Token'),
    (r'auth[_-]?token\s*[=:]\s*[\'"]([a-zA-Z0-9_\-\.]{20,})[\'"]', 'Auth Token'),
    
    # Secrets
    (r'secret[_-]?key\s*[=:]\s*[\'"]([a-zA-Z0-9_\-]{20,})[\'"]', 'Secret Key'),
    (r'client[_-]?secret\s*[=:]\s*[\'"]([a-zA-Z0-9_\-]{20,})[\'"]', 'Client Secret'),
    
    # Database connection strings
    (r'mongodb(\+srv)?://[^:]+:([^@]+)@', 'MongoDB Password'),
    (r'postgres://[^:]+:([^@]+)@', 'PostgreSQL Password'),
    (r'mysql://[^:]+:([^@]+)@', 'MySQL Password'),
    
    # AWS
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
    (r'aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*[\'"]([^\'"]{40})[\'"]', 'AWS Secret Key'),
    
    # Private keys
    (r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', 'Private Key'),
    
    # Generic secrets (但排除占位符)
    (r'(?<!example_|test_|demo_|placeholder_|your_)(?:secret|password|token|key)\s*[=:]\s*[\'"](?!xxx|placeholder|your_|test|demo|example)([a-zA-Z0-9_\-\.]{16,})[\'"]', 'Generic Secret'),
]

# 排除的模式（占位符、示例等）
EXCLUDE_PATTERNS = [
    r'xxx+',  # xxx, xxxx, xxxxx等
    r'placeholder',
    r'your_\w+',
    r'<\w+>',  # <your_key>, <token>等
    r'\{\{\s*\w+\s*\}\}',  # {{ key }}等模板变量
    r'\$\{\w+\}',  # ${KEY}等环境变量
    r'example',
    r'test_\w+',
    r'demo_\w+',
    r'changeme',
    r'TODO',
    r'sample',  # sample_key
    r'dummy',  # dummy_token
    r'fake',  # fake_secret
    r'mock',  # mock_password
    r'default',  # default_key
    r'null',  # null值
    r'none',  # none值
    r'undefined',  # undefined
    r'(your|my|the)[-_]?\w+',  # your-key, my-token等
    r'\.\.\.+',  # ... 省略号
    r'[*]{3,}',  # *** 星号占位符
    r'^-+$',  # --- 横线占位符
    r'0{8,}',  # 全0占位符
    r'1{8,}',  # 全1占位符
    r'[a-z]+_secret_key',  # 带后缀的明显占位符
    r'secret_key_\d+',  # secret_key_123等
]

# 排除的文件路径模式（这些位置的密钥通常是示例）
EXCLUDE_FILE_PATTERNS = [
    r'doc/',  # 文档目录
    r'docs/',  # 文档目录
    r'example/',  # 示例目录
    r'examples/',  # 示例目录
    r'test/',  # 测试目录
    r'tests/',  # 测试目录
    r'temp/',  # 临时目录
    r'README\.md$',  # README文件
    r'\.template$',  # 模板文件
    r'RUNBOOK\.md$',  # 运维手册（包含示例命令）
    r'TEST_PLAN\.md$',  # 测试计划（包含测试数据）
]


class SecretScanner:
    """密钥扫描器"""
    
    def __init__(self, scan_path: Path = REPO_ROOT):
        """初始化扫描器"""
        self.scan_path = scan_path
        self.results = {
            "security_checks_passed": 0,
            "total_checks": 4,
            "secrets_found": 0,
            "issues": [],
            "checks": {}
        }
    
    def is_excluded_value(self, value: str) -> bool:
        """检查是否为排除的占位符值"""
        for pattern in EXCLUDE_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        return False
    
    def is_excluded_file(self, file_path: Path) -> bool:
        """检查是否为排除的文件路径"""
        file_str = str(file_path)
        for pattern in EXCLUDE_FILE_PATTERNS:
            if re.search(pattern, file_str):
                return True
        return False
    
    def scan_file_for_secrets(self, file_path: Path) -> List[Dict[str, Any]]:
        """扫描单个文件中的密钥"""
        secrets = []
        
        # 检查是否为排除的文件
        if self.is_excluded_file(file_path):
            return secrets
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            for pattern, secret_type in SECRET_PATTERNS:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                
                for match in matches:
                    # 获取匹配的值
                    if match.groups():
                        secret_value = match.group(1) if len(match.groups()) >= 1 else match.group(0)
                    else:
                        secret_value = match.group(0)
                    
                    # 排除占位符
                    if self.is_excluded_value(secret_value):
                        continue
                    
                    # 获取行号
                    line_num = content[:match.start()].count('\n') + 1
                    
                    secrets.append({
                        "file": str(file_path.relative_to(REPO_ROOT)),
                        "line": line_num,
                        "type": secret_type,
                        "pattern": pattern[:50],  # 截断模式
                        "snippet": match.group(0)[:80]  # 截断snippet
                    })
        
        except Exception as e:
            # 忽略读取错误（二进制文件等）
            pass
        
        return secrets
    
    def scan_code_files(self) -> Dict[str, Any]:
        """扫描代码文件中的密钥"""
        print("🔍 扫描代码文件...")
        
        result = {
            "check_name": "No Secrets in Code",
            "passed": True,
            "secrets_found": 0,
            "files_scanned": 0
        }
        
        # 扫描Python, Go, TypeScript文件
        patterns = ["**/*.py", "**/*.go", "**/*.ts", "**/*.js"]
        
        for pattern in patterns:
            for file_path in self.scan_path.glob(pattern):
                # 排除特定目录
                if any(part in file_path.parts for part in ['.git', 'node_modules', '__pycache__', 'venv', '.venv', 'temp']):
                    continue
                
                result["files_scanned"] += 1
                secrets = self.scan_file_for_secrets(file_path)
                
                if secrets:
                    result["secrets_found"] += len(secrets)
                    result["passed"] = False
                    self.results["issues"].extend(secrets)
        
        return result
    
    def scan_config_files(self) -> Dict[str, Any]:
        """扫描配置文件中的密钥"""
        print("🔍 扫描配置文件...")
        
        result = {
            "check_name": "No Secrets in Configs",
            "passed": True,
            "secrets_found": 0,
            "files_scanned": 0
        }
        
        # 扫描YAML, JSON, ENV文件
        patterns = ["**/*.yaml", "**/*.yml", "**/*.json", "**/*.env*"]
        
        for pattern in patterns:
            for file_path in self.scan_path.glob(pattern):
                # 排除特定目录和文件
                if any(part in file_path.parts for part in ['.git', 'node_modules', 'temp']):
                    continue
                if file_path.name == '.gitignore':
                    continue
                
                result["files_scanned"] += 1
                secrets = self.scan_file_for_secrets(file_path)
                
                if secrets:
                    result["secrets_found"] += len(secrets)
                    result["passed"] = False
                    self.results["issues"].extend(secrets)
        
        return result
    
    def scan_docs(self) -> Dict[str, Any]:
        """扫描文档中的密钥"""
        print("🔍 扫描文档...")
        
        result = {
            "check_name": "No Secrets in Docs",
            "passed": True,
            "secrets_found": 0,
            "files_scanned": 0
        }
        
        # 扫描Markdown文件
        patterns = ["**/*.md", "**/*.MD"]
        
        for pattern in patterns:
            for file_path in self.scan_path.glob(pattern):
                # 排除特定目录
                if any(part in file_path.parts for part in ['.git', 'node_modules', 'temp']):
                    continue
                
                result["files_scanned"] += 1
                secrets = self.scan_file_for_secrets(file_path)
                
                if secrets:
                    result["secrets_found"] += len(secrets)
                    result["passed"] = False
                    self.results["issues"].extend(secrets)
        
        return result
    
    def check_gitignore(self) -> Dict[str, Any]:
        """检查.env文件是否被.gitignore"""
        print("🔍 检查.gitignore配置...")
        
        result = {
            "check_name": ".env Files Gitignored",
            "passed": False,
            "details": {}
        }
        
        gitignore_path = REPO_ROOT / ".gitignore"
        
        if not gitignore_path.exists():
            result["details"]["error"] = ".gitignore文件不存在"
            return result
        
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含.env相关规则
            env_patterns = ['.env', '*.env', '.env.*']
            found_patterns = []
            
            for pattern in env_patterns:
                if pattern in content:
                    found_patterns.append(pattern)
            
            if found_patterns:
                result["passed"] = True
                result["details"]["patterns"] = found_patterns
                result["details"]["status"] = "✅"
            else:
                result["details"]["error"] = ".gitignore中未找到.env相关规则"
                result["details"]["status"] = "❌"
        
        except Exception as e:
            result["details"]["error"] = f"读取.gitignore失败: {e}"
        
        return result
    
    def run_all_scans(self):
        """运行所有扫描"""
        print("=" * 70)
        print("🔒 Secret Scan - 开始扫描...")
        print("=" * 70)
        
        # 运行4项检查
        self.results["checks"]["code"] = self.scan_code_files()
        self.results["checks"]["configs"] = self.scan_config_files()
        self.results["checks"]["docs"] = self.scan_docs()
        self.results["checks"]["gitignore"] = self.check_gitignore()
        
        # 统计
        self.results["secrets_found"] = len(self.results["issues"])
        self.results["security_checks_passed"] = sum(
            1 for check in self.results["checks"].values()
            if check.get("passed", False)
        )
        
        print("\n" + "=" * 70)
        print("✅ 密钥扫描完成！")
        print("=" * 70)
    
    def print_console_report(self):
        """打印控制台报告"""
        print("\n" + "=" * 70)
        print("📊 SECRET SCAN REPORT")
        print("=" * 70)
        
        print(f"\n🔐 Security Status:")
        print(f"  通过检查: {self.results['security_checks_passed']}/{self.results['total_checks']}")
        print(f"  发现密钥: {self.results['secrets_found']}")
        
        # 检查详情
        print(f"\n📋 Check Results:")
        for check_key, check_result in self.results["checks"].items():
            check_name = check_result["check_name"]
            passed = "✅" if check_result.get("passed", False) else "❌"
            
            print(f"  {passed} {check_name}")
            
            if "files_scanned" in check_result:
                print(f"     扫描文件: {check_result['files_scanned']}")
                if check_result.get("secrets_found", 0) > 0:
                    print(f"     发现密钥: {check_result['secrets_found']}")
            
            if "details" in check_result:
                if "patterns" in check_result["details"]:
                    print(f"     忽略模式: {', '.join(check_result['details']['patterns'])}")
                if "error" in check_result["details"]:
                    print(f"     错误: {check_result['details']['error']}")
        
        # 显示发现的密钥
        if self.results["issues"]:
            print(f"\n🚨 发现的密钥 ({len(self.results['issues'])}):")
            for issue in self.results["issues"][:10]:  # 只显示前10个
                print(f"  ❌ {issue['file']}:{issue['line']}")
                print(f"     类型: {issue['type']}")
                print(f"     片段: {issue['snippet']}")
        
        # 建议
        print(f"\n💡 建议:")
        if self.results["secrets_found"] > 0:
            print("  🚨 立即删除所有泄露的密钥！")
            print("  🔑 轮换所有泄露的凭据")
            print("  📝 更新.gitignore以防止未来泄露")
            print("  🔍 审查历史提交，确保密钥未提交到仓库")
        else:
            print("  ✅ 未发现密钥泄露，很好！")
            print("  📝 定期运行密钥扫描")
        
        print("\n" + "=" * 70)
    
    def print_json_report(self):
        """打印JSON报告"""
        print(json.dumps(self.results, indent=2, ensure_ascii=False))


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Secret Scan")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    parser.add_argument("--path", type=str, help="扫描路径（默认仓库根目录）")
    
    args = parser.parse_args()
    
    scan_path = Path(args.path) if args.path else REPO_ROOT
    
    scanner = SecretScanner(scan_path=scan_path)
    scanner.run_all_scans()
    
    if args.json:
        scanner.print_json_report()
    else:
        scanner.print_console_report()
    
    # 如果发现密钥，退出码为1
    if scanner.results["secrets_found"] > 0:
        sys.exit(1)
    elif scanner.results["security_checks_passed"] < 3:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

