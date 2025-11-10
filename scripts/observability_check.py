#!/usr/bin/env python3
"""



Usage:
    python scripts/observability_check.py [--json]
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent


class ObservabilityChecker:
    """"""
    
    def __init__(self):
        self.repo_root = REPO_ROOT
        self.observability_path = self.repo_root / "observability"
        self.modules_path = self.repo_root / "modules"
        
    def check_logging(self) -> Dict[str, Any]:
        """"""
        checks_passed = []
        issues = []
        
        # 1
        logging_config_paths = [
            self.observability_path / "logging" / "fluentd.conf",
            self.observability_path / "logging" / "filebeat.yaml",
            self.observability_path / "logging" / "logstash.yaml",
        ]
        
        config_exists = any(p.exists() for p in logging_config_paths)
        if config_exists:
            checks_passed.append("Logging config exists")
        else:
            issues.append("No logging configuration found")
        
        # 2
        modules_with_logging = 0
        total_modules = 0
        
        for module_dir in self.modules_path.glob("*"):
            if module_dir.is_dir() and not module_dir.name.startswith('.'):
                total_modules += 1
                # 
                has_logging = False
                for py_file in module_dir.rglob("*.py"):
                    with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if 'import logging' in content or 'from logging' in content:
                            has_logging = True
                            break
                if has_logging:
                    modules_with_logging += 1
        
        if total_modules > 0 and modules_with_logging == total_modules:
            checks_passed.append("All modules have logging")
        elif modules_with_logging > 0:
            issues.append(f"Only {modules_with_logging}/{total_modules} modules have logging")
        else:
            issues.append("No modules have logging configured")
        
        return {
            'checks_passed': checks_passed,
            'issues': issues,
            'module_coverage': f"{modules_with_logging}/{total_modules}"
        }
    
    def check_metrics(self) -> Dict[str, Any]:
        """"""
        checks_passed = []
        issues = []
        
        # 1Prometheus
        prometheus_config = self.observability_path / "metrics" / "prometheus.yml"
        if prometheus_config.exists():
            checks_passed.append("Prometheus config exists")
            
            # 
            with open(prometheus_config, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'scrape_configs' in content:
                    checks_passed.append("Scrape configs defined")
        else:
            issues.append("No Prometheus configuration")
        
        # 2Grafana
        grafana_dashboards = self.observability_path / "metrics" / "grafana-dashboard.json"
        if grafana_dashboards.exists():
            checks_passed.append("Grafana dashboard exists")
        else:
            issues.append("No Grafana dashboard")
        
        return {
            'checks_passed': checks_passed,
            'issues': issues
        }
    
    def check_tracing(self) -> Dict[str, Any]:
        """"""
        checks_passed = []
        issues = []
        
        # 
        tracing_configs = [
            self.observability_path / "tracing" / "jaeger.yaml",
            self.observability_path / "tracing" / "zipkin.yaml",
            self.observability_path / "tracing" / "otel-collector.yaml"
        ]
        
        if any(p.exists() for p in tracing_configs):
            checks_passed.append("Tracing config exists")
        else:
            issues.append("No distributed tracing configuration")
        
        # OpenTelemetry
        otel_found = False
        for module_dir in self.modules_path.glob("*"):
            if module_dir.is_dir():
                for py_file in module_dir.rglob("*.py"):
                    with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if 'opentelemetry' in content.lower() or 'jaeger' in content.lower():
                            otel_found = True
                            break
                if otel_found:
                    break
        
        if otel_found:
            checks_passed.append("Tracing instrumentation found")
        else:
            issues.append("No tracing instrumentation in code")
        
        return {
            'checks_passed': checks_passed,
            'issues': issues
        }
    
    def check_alerts(self) -> Dict[str, Any]:
        """"""
        checks_passed = []
        issues = []
        
        # 1Prometheus
        alert_rules = self.observability_path / "alerts" / "prometheus_alerts.yml"
        if alert_rules.exists():
            checks_passed.append("Alert rules defined")
            
            # 
            try:
                with open(alert_rules, 'r', encoding='utf-8') as f:
                    alert_config = yaml.safe_load(f)
                    if 'groups' in alert_config:
                        total_rules = sum(len(g.get('rules', [])) for g in alert_config['groups'])
                        if total_rules > 0:
                            checks_passed.append(f"{total_rules} alert rules configured")
            except:
                issues.append("Alert rules file corrupted")
        else:
            issues.append("No alert rules defined")
        
        # 2AlertManager
        alertmanager_config = self.observability_path / "alerts" / "alertmanager.yml"
        if alertmanager_config.exists():
            checks_passed.append("AlertManager configured")
        else:
            issues.append("No AlertManager configuration")
        
        return {
            'checks_passed': checks_passed,
            'issues': issues
        }
    
    def check_dashboards(self) -> Dict[str, Any]:
        """"""
        checks_passed = []
        issues = []
        
        # Grafana
        dashboard_path = self.observability_path / "metrics"
        dashboard_files = list(dashboard_path.glob("*dashboard*.json")) if dashboard_path.exists() else []
        
        if dashboard_files:
            checks_passed.append(f"{len(dashboard_files)} dashboard(s) configured")
            
            # 
            for dashboard_file in dashboard_files:
                try:
                    with open(dashboard_file, 'r', encoding='utf-8') as f:
                        dashboard_data = json.load(f)
                        if 'panels' in dashboard_data:
                            panel_count = len(dashboard_data['panels'])
                            if panel_count > 0:
                                checks_passed.append(f"{panel_count} panels in {dashboard_file.name}")
                except:
                    issues.append(f"Cannot parse {dashboard_file.name}")
        else:
            issues.append("No dashboard templates found")
        
        return {
            'checks_passed': checks_passed,
            'issues': issues
        }
    
    def calculate_score(self, results: Dict[str, Any]) -> int:
        """5"""
        score = 0
        
        # 1
        for dimension in ['logging', 'metrics', 'tracing', 'alerts', 'dashboards']:
            if dimension in results:
                if len(results[dimension]['checks_passed']) > 0:
                    score += 1
        
        return min(score, 5)
    
    def run_all_checks(self) -> Dict[str, Any]:
        """"""
        results = {
            'logging': self.check_logging(),
            'metrics': self.check_metrics(),
            'tracing': self.check_tracing(),
            'alerts': self.check_alerts(),
            'dashboards': self.check_dashboards()
        }
        
        # 
        total_checks_passed = sum(len(r['checks_passed']) for r in results.values())
        total_issues = sum(len(r['issues']) for r in results.values())
        
        results['summary'] = {
            'total_checks_passed': total_checks_passed,
            'total_issues': total_issues,
            'checks_passed': min(self.calculate_score(results), 5),
            'max_score': 5,
            'status': self.get_status(total_checks_passed, total_issues)
        }
        
        return results
    
    def get_status(self, checks_passed: int, issues: int) -> str:
        """"""
        if issues == 0:
            return '✅ Excellent'
        elif checks_passed >= 10:
            return '✅ Good'
        elif checks_passed >= 5:
            return '⚠️ Fair'
        else:
            return '❌ Poor'
    
    def print_report(self, results: Dict[str, Any]):
        """"""
        print("=" * 60)
        print("👁️ Observability Check Report")
        print("=" * 60)
        print()
        
        print(f"Overall Status: {results['summary']['status']}")
        print(f"Score: {results['summary']['checks_passed']}/{results['summary']['max_score']}")
        print(f"Checks Passed: {results['summary']['total_checks_passed']}")
        print(f"Issues Found: {results['summary']['total_issues']}")
        print()
        
        for dimension in ['logging', 'metrics', 'tracing', 'alerts', 'dashboards']:
            if dimension in results:
                print(f"\n📊 {dimension.capitalize()}:")
                
                dim_results = results[dimension]
                
                if dim_results['checks_passed']:
                    print("  ✅ Passed:")
                    for check in dim_results['checks_passed']:
                        print(f"    • {check}")
                
                if dim_results['issues']:
                    print("  ❌ Issues:")
                    for issue in dim_results['issues']:
                        print(f"    • {issue}")
        
        print("\nRecommendations:")
        if results['summary']['total_issues'] > 0:
            if 'logging' in results and results['logging']['issues']:
                print("  • Configure centralized logging (Fluentd/Filebeat)")
            if 'metrics' in results and results['metrics']['issues']:
                print("  • Set up Prometheus metrics collection")
            if 'tracing' in results and results['tracing']['issues']:
                print("  • Implement distributed tracing (Jaeger/Zipkin)")
            if 'alerts' in results and results['alerts']['issues']:
                print("  • Define alert rules for critical metrics")
            if 'dashboards' in results and results['dashboards']['issues']:
                print("  • Create Grafana dashboards for visualization")
        else:
            print("  • Observability is well configured")
            print("  • Consider adding more detailed metrics")
            print("  • Regular review of alert thresholds recommended")
        
        print()
        print("=" * 60)


def main():
    """"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Observability Checker")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    checker = ObservabilityChecker()
    results = checker.run_all_checks()
    
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        checker.print_report(results)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())