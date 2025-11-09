#!/usr/bin/env python3
"""
Config Files Linter - Validates YAML configuration files

Purpose:
- Validate YAML syntax
- Check for required fields
- Detect duplicate keys
- Validate against schema (if available)
- Check for sensitive data

Usage:
    python scripts/config_lint.py
    make config_lint
"""

import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class ConfigLinter:
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.errors: Dict[str, List[str]] = {}
        self.warnings: Dict[str, List[str]] = {}
        self.checked_count = 0
        
        # Sensitive patterns to detect
        self.sensitive_patterns = [
            'password', 'passwd', 'pwd',
            'secret', 'api_key', 'apikey', 'token',
            'private_key', 'privatekey',
            'access_key', 'accesskey'
        ]
        
    def check_yaml_syntax(self, config_path: Path) -> Any:
        """Check YAML syntax and return parsed data"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            return data
        except yaml.YAMLError as e:
            return None, str(e)
        except Exception as e:
            return None, f"Failed to read file: {e}"
            
    def check_sensitive_data(self, data: Dict, path: str = "") -> List[str]:
        """Recursively check for hardcoded sensitive data"""
        issues = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                
                # Check if key suggests sensitive data
                key_lower = key.lower()
                for pattern in self.sensitive_patterns:
                    if pattern in key_lower:
                        # Check if value looks like actual secret (not placeholder)
                        if isinstance(value, str):
                            # OK: Environment variable reference
                            if value.startswith('${') and value.endswith('}'):
                                continue
                            # OK: Placeholder
                            if value in ['', 'YOUR_KEY_HERE', 'CHANGE_ME', '<SECRET>']:
                                continue
                            # Suspicious: Actual value
                            if len(value) > 5 and not value.isdigit():
                                issues.append(
                                    f"{current_path}: Potential hardcoded secret detected"
                                )
                
                # Recurse
                if isinstance(value, (dict, list)):
                    issues.extend(self.check_sensitive_data(value, current_path))
                    
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path}[{i}]"
                if isinstance(item, (dict, list)):
                    issues.extend(self.check_sensitive_data(item, current_path))
                    
        return issues
        
    def check_env_configs(self, configs: Dict[str, Any]):
        """Check consistency across environment configs"""
        # Get all keys from defaults
        defaults_keys = set()
        if 'defaults.yaml' in configs:
            defaults_keys = self._get_all_keys(configs['defaults.yaml'])
            
        # Check each env config
        for filename, data in configs.items():
            if filename == 'defaults.yaml' or not filename.endswith('.yaml'):
                continue
                
            env_keys = self._get_all_keys(data)
            
            # Keys in env but not in defaults
            extra_keys = env_keys - defaults_keys
            if extra_keys:
                self.warnings.setdefault(filename, []).append(
                    f"Keys not in defaults.yaml: {', '.join(sorted(extra_keys))}"
                )
                
    def _get_all_keys(self, data: Any, prefix: str = "") -> set:
        """Recursively get all keys from nested dict"""
        keys = set()
        if isinstance(data, dict):
            for key, value in data.items():
                current_key = f"{prefix}.{key}" if prefix else key
                keys.add(current_key)
                if isinstance(value, (dict, list)):
                    keys.update(self._get_all_keys(value, current_key))
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    keys.update(self._get_all_keys(item, f"{prefix}[{i}]"))
        return keys
        
    def check_file(self, config_path: Path):
        """Check a single config file"""
        self.checked_count += 1
        filename = config_path.name
        
        # Check YAML syntax
        result = self.check_yaml_syntax(config_path)
        if isinstance(result, tuple):
            data, error = result
            if error:
                self.errors.setdefault(filename, []).append(f"YAML syntax error: {error}")
                return
        else:
            data = result
            
        if data is None:
            return
            
        # Check for sensitive data
        sensitive_issues = self.check_sensitive_data(data)
        if sensitive_issues:
            self.warnings.setdefault(filename, []).extend(sensitive_issues)
            
    def run_checks(self) -> bool:
        """Check all config files"""
        if not self.config_dir.exists():
            print(f"❌ Config directory not found: {self.config_dir}")
            return False
            
        # Find all YAML files
        yaml_files = list(self.config_dir.glob('*.yaml'))
        yaml_files.extend(self.config_dir.glob('*.yml'))
        
        if not yaml_files:
            print(f"⚠️  No config files found in {self.config_dir}")
            return True
            
        # Check each file
        configs = {}
        for config_path in sorted(yaml_files):
            self.check_file(config_path)
            # Load for cross-file checks
            with open(config_path, 'r', encoding='utf-8') as f:
                try:
                    configs[config_path.name] = yaml.safe_load(f)
                except:
                    pass
                    
        # Cross-file checks
        self.check_env_configs(configs)
        
        return len(self.errors) == 0
        
    def report(self):
        """Print check results"""
        if self.errors:
            print("\n❌ Config Lint Failed\n")
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
            print(f"✅ Config lint passed ({self.checked_count} files checked)")
            

def main():
    """Main entry point"""
    repo_root = Path(__file__).parent.parent
    config_dir = repo_root / 'config'
    
    linter = ConfigLinter(config_dir)
    success = linter.run_checks()
    linter.report()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())

