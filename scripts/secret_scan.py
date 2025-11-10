#!/usr/bin/env python3
"""



Usage:
    python scripts/secret_scan.py [--json]
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent


class SecretScanner:
    """"""
    
    def __init__(self):
        self.repo_root = REPO_ROOT
        self.issues = []
        
        # 
        self.patterns = {
            'api_key': [
                r'api[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',
                r'apikey\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',
                r'API_KEY\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',
            ],
            'aws_key': [
                r'aws_access_key_id\s*[=:]\s*["\']?[A-Z0-9]{20}',
                r'aws_secret_access_key\s*[=:]\s*["\']?[a-zA-Z0-9/+=]{40}',
                r'AKIA[0-9A-Z]{16}',
            ],
            'private_key': [
                r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY',
                r'private[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9+/]{40,}',
            ],
            'password': [
                r'password\s*[=:]\s*["\'][^"\']{8,}["\']',
                r'passwd\s*[=:]\s*["\'][^"\']{8,}["\']',
                r'pwd\s*[=:]\s*["\'][^"\']{8,}["\']',
            ],
            'token': [
                r'token\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',
                r'auth[_-]?token\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',
                r'access[_-]?token\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}',
            ],
            'database_url': [
                r'(postgres|postgresql|mysql|mongodb|redis)://[^:]+:[^@]+@[^/\s]+',
                r'DATABASE_URL\s*[=:]\s*["\'][^"\']+["\']',
            ],
            'jwt_secret': [
                r'jwt[_-]?secret\s*[=:]\s*["\'][^"\']{10,}["\']',
                r'JWT_SECRET\s*[=:]\s*["\'][^"\']{10,}["\']',
            ]
        }
        
        # 
        self.ignore_patterns = [
            '.git',
            'node_modules',
            '.venv',
            'venv',
            '__pycache__',
            '.pytest_cache',
            'htmlcov',
            'coverage',
            '.idea',
            '.vscode',
            '*.pyc',
            '*.pyo',
            '*.egg-info',
            'dist',
            'build',
        ]
        
        # 
        self.allowed_patterns = [
            r'example',
            r'sample',
            r'test',
            r'demo',
            r'placeholder',
            r'your[_-]?',
            r'<[^>]+>',
            r'xxx+',
            r'change[_-]?me',
            r'todo',
            r'fixme',
            r'replace',
            r'\$\{[^}]+\}',  # 
            r'Bearer\s+(valid_token|invalid_token|expired_token|refreshed_)',  # token
        ]
    
    def should_ignore(self, file_path: Path) -> bool:
        """"""
        path_str = str(file_path)
        
        for pattern in self.ignore_patterns:
            if pattern in path_str:
                return True
        
        # 
        if file_path.suffix in ['.jpg', '.png', '.gif', '.pdf', '.zip', '.tar', '.gz']:
            return True
        
        return False
    
    def is_allowed(self, matched_text: str) -> bool:
        """"""
        matched_lower = matched_text.lower()
        
        for pattern in self.allowed_patterns:
            if re.search(pattern, matched_lower, re.IGNORECASE):
                return True
        
        #  "xxxxxxxx"
        if len(set(re.sub(r'[^a-zA-Z0-9]', '', matched_text))) <= 2:
            return True
        
        return False
    
    def scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """"""
        file_issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            for secret_type, patterns in self.patterns.items():
                for pattern in patterns:
                    for match in re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE):
                        matched_text = match.group(0)
                        
                        # 
                        if self.is_allowed(matched_text):
                            continue
                        
                        # 
                        line_start = content[:match.start()].count('\n') + 1
                        
                        # 
                        if len(matched_text) > 20:
                            sanitized = matched_text[:10] + '...[REDACTED]'
                        else:
                            sanitized = matched_text[:5] + '...[REDACTED]'
                        
                        file_issues.append({
                            'file': str(file_path.relative_to(self.repo_root)),
                            'line': line_start,
                            'type': secret_type,
                            'match': sanitized,
                            'severity': self.get_severity(secret_type)
                        })
        
        except Exception as e:
            # 
            pass
        
        return file_issues
    
    def get_severity(self, secret_type: str) -> str:
        """"""
        high_severity = ['private_key', 'aws_key', 'database_url']
        medium_severity = ['api_key', 'token', 'jwt_secret']
        
        if secret_type in high_severity:
            return 'HIGH'
        elif secret_type in medium_severity:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def scan_repository(self) -> Dict[str, Any]:
        """"""
        self.issues = []
        files_scanned = 0
        
        # 
        for root, dirs, files in os.walk(self.repo_root):
            root_path = Path(root)
            
            # 
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.ignore_patterns)]
            
            for file in files:
                file_path = root_path / file
                
                if self.should_ignore(file_path):
                    continue
                
                files_scanned += 1
                file_issues = self.scan_file(file_path)
                self.issues.extend(file_issues)
        
        # .env.gitignore
        env_in_gitignore = self.check_env_gitignore()
        
        # 
        security_checks_passed = self.calculate_security_score()
        
        return {
            'files_scanned': files_scanned,
            'issues_found': len(self.issues),
            'issues': self.issues[:10],  # 10
            'high_severity_count': len([i for i in self.issues if i['severity'] == 'HIGH']),
            'medium_severity_count': len([i for i in self.issues if i['severity'] == 'MEDIUM']),
            'low_severity_count': len([i for i in self.issues if i['severity'] == 'LOW']),
            'env_in_gitignore': env_in_gitignore,
            'security_checks_passed': security_checks_passed,
            'status': self.get_status()
        }
    
    def check_env_gitignore(self) -> bool:
        """.env.gitignore"""
        gitignore_path = self.repo_root / '.gitignore'
        if gitignore_path.exists():
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return '.env' in content or '*.env' in content
        return False
    
    def calculate_security_score(self) -> int:
        """4"""
        score = 0
        
        # 1
        if not any(i['severity'] == 'HIGH' for i in self.issues):
            score += 1
        
        # 2
        if not any(i['severity'] == 'MEDIUM' for i in self.issues):
            score += 1
        
        # 35
        if len(self.issues) < 5:
            score += 1
        
        # 4.env.gitignore
        if self.check_env_gitignore():
            score += 1
        
        return score
    
    def get_status(self) -> str:
        """"""
        if len(self.issues) == 0:
            return '✅ Clean'
        elif any(i['severity'] == 'HIGH' for i in self.issues):
            return '❌ Critical'
        elif len(self.issues) < 5:
            return '⚠️ Warning'
        else:
            return '❌ Failed'
    
    def print_report(self, results: Dict[str, Any]):
        """"""
        print("=" * 60)
        print("🔐 Security Scan Report")
        print("=" * 60)
        print()
        
        print(f"Files Scanned: {results['files_scanned']}")
        print(f"Issues Found: {results['issues_found']} {results['status']}")
        print(f".env in .gitignore: {'✅ Yes' if results['env_in_gitignore'] else '❌ No'}")
        print(f"Security Checks Passed: {results['security_checks_passed']}/4")
        print()
        
        if results['issues_found'] > 0:
            print("Issue Breakdown:")
            print(f"  - HIGH Severity: {results['high_severity_count']}")
            print(f"  - MEDIUM Severity: {results['medium_severity_count']}")
            print(f"  - LOW Severity: {results['low_severity_count']}")
            print()
            
            print("Sample Issues (top 10):")
            for issue in results['issues']:
                print(f"  [{issue['severity']}] {issue['file']}:{issue['line']}")
                print(f"        Type: {issue['type']}")
                print(f"        Match: {issue['match']}")
        else:
            print("🎉 No security issues found!")
        
        print()
        print("Recommendations:")
        if results['issues_found'] == 0:
            print("  • Continue following security best practices")
            print("  • Regular security audits recommended")
        else:
            if results['high_severity_count'] > 0:
                print("  • URGENT: Remove or rotate high-severity secrets immediately")
            if not results['env_in_gitignore']:
                print("  • Add .env files to .gitignore")
            print("  • Use environment variables for sensitive data")
            print("  • Consider using a secret management service")
            print("  • Rotate any exposed credentials")
        
        print()
        print("=" * 60)


def main():
    """"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Secret Scanner")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    scanner = SecretScanner()
    results = scanner.scan_repository()
    
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        scanner.print_report(results)
    
    # 
    if results['issues_found'] > 0 and results['high_severity_count'] > 0:
        return 1  # 
    return 0


if __name__ == "__main__":
    sys.exit(main())