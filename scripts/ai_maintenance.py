#!/usr/bin/env python3
"""
AI 



1.  AI 
2. /
3. python scripts/ai_maintenance.py
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
import io

# Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 
MAINTENANCE_TASKS = [
    'doc_style_check',      # 
    'encoding_check',       # 
    'consistency_check',    # 
    'docgen',               # 
    'deps_check',           # 
    'dag_check',            # DAG 
    'contract_compat_check', # 
    'temp_files_check',     # 
]

# 
class MaintenanceReport:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.tasks: List[Dict] = []
        self.summary = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'warnings': 0
        }
    
    def add_task(self, task_name: str, status: str, message: str, details: str = ''):
        """"""
        self.tasks.append({
            'task': task_name,
            'status': status,  # 'passed', 'failed', 'warning'
            'message': message,
            'details': details
        })
        self.summary['total'] += 1
        if status == 'passed':
            self.summary['passed'] += 1
        elif status == 'failed':
            self.summary['failed'] += 1
        else:
            self.summary['warnings'] += 1
    
    def to_json(self) -> str:
        """ JSON"""
        return json.dumps({
            'timestamp': self.timestamp,
            'summary': self.summary,
            'tasks': self.tasks
        }, indent=2, ensure_ascii=False)
    
    def save(self, file_path: Path):
        """"""
        file_path.write_text(self.to_json(), encoding='utf-8')


def run_make_command(target: str) -> Tuple[int, str, str]:
    """ make """
    try:
        result = subprocess.run(
            ['make', target],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=300  # 5 
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, '', f': make {target}'
    except FileNotFoundError:
        return 1, '', f'make '
    except Exception as e:
        return 1, '', f': {str(e)}'


def check_doc_style(report: MaintenanceReport):
    """"""
    print("...")
    returncode, stdout, stderr = run_make_command('doc_style_check')
    
    if returncode == 0:
        report.add_task('doc_style_check', 'passed', '')
    else:
        # 
        issues = stdout.count('') if stdout else 0
        report.add_task(
            'doc_style_check',
            'warning' if issues < 10 else 'failed',
            f' {issues} ',
            stdout[:500]  # 
        )


def check_encoding(report: MaintenanceReport):
    """"""
    print("...")
    #  make target
    try:
        result = subprocess.run(
            [sys.executable, 'scripts/encoding_check.py'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60
        )
        if result.returncode == 0:
            report.add_task('encoding_check', 'passed', ' UTF-8 ')
        else:
            #  UTF-8 
            non_utf8 = result.stdout.count(':') if result.stdout else 0
            report.add_task(
                'encoding_check',
                'warning' if non_utf8 < 5 else 'failed',
                f' {non_utf8}  UTF-8 ',
                result.stdout[:500]
            )
    except Exception as e:
        report.add_task('encoding_check', 'failed', f': {str(e)}')


def update_docgen(report: MaintenanceReport):
    """"""
    print("...")
    returncode, stdout, stderr = run_make_command('docgen')
    
    if returncode == 0:
        report.add_task('docgen', 'passed', '')
    else:
        report.add_task('docgen', 'failed', '', stderr[:500])


def check_consistency(report: MaintenanceReport):
    """"""
    print("...")
    returncode, stdout, stderr = run_make_command('consistency_check')
    
    if returncode == 0:
        report.add_task('consistency_check', 'passed', '')
    else:
        report.add_task('consistency_check', 'warning', '', stdout[:500])


def check_deps(report: MaintenanceReport):
    """"""
    print("...")
    returncode, stdout, stderr = run_make_command('deps_check')
    
    if returncode == 0:
        report.add_task('deps_check', 'passed', '')
    else:
        report.add_task('deps_check', 'warning', '', stdout[:500])


def check_dag(report: MaintenanceReport):
    """ DAG"""
    print(" DAG...")
    returncode, stdout, stderr = run_make_command('dag_check')
    
    if returncode == 0:
        report.add_task('dag_check', 'passed', 'DAG ')
    else:
        report.add_task('dag_check', 'failed', 'DAG ', stderr[:500])


def check_contract_compat(report: MaintenanceReport):
    """"""
    print("...")
    returncode, stdout, stderr = run_make_command('contract_compat_check')
    
    if returncode == 0:
        report.add_task('contract_compat_check', 'passed', '')
    else:
        report.add_task('contract_compat_check', 'warning', '', stdout[:500])


def check_test_status(report: MaintenanceReport):
    """"""
    print("...")
    try:
        result = subprocess.run(
            [sys.executable, 'scripts/test_status_check.py'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60
        )
        if result.returncode == 0:
            report.add_task('test_status_check', 'passed', '')
        else:
            # 
            pending = result.stdout.count('') + result.stdout.count('pending')
            report.add_task(
                'test_status_check',
                'warning',
                f' {pending} ',
                result.stdout[:500]
            )
    except Exception as e:
        report.add_task('test_status_check', 'warning', f': {str(e)}')


def check_app_structure(report: MaintenanceReport):
    """"""
    print("...")
    try:
        result = subprocess.run(
            [sys.executable, 'scripts/app_structure_check.py'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60
        )
        if result.returncode == 0:
            report.add_task('app_structure_check', 'passed', '')
        else:
            # 
            issues = result.stdout.count('❌') + result.stdout.count('⚠️')
            report.add_task(
                'app_structure_check',
                'warning' if issues < 5 else 'failed',
                f' {issues} ',
                result.stdout[:500]
            )
    except Exception as e:
        report.add_task('app_structure_check', 'warning', f': {str(e)}')


def check_temp_files(report: MaintenanceReport):
    """"""
    print("...")
    try:
        #  *_temp.*  temp/ gitnode_modules 
        result = subprocess.run(
            [
                'find', '.', 
                '-type', 'f',
                '-name', '*_temp.*',
                '-not', '-path', './.git/*',
                '-not', '-path', './node_modules/*',
                '-not', '-path', './.venv/*',
                '-not', '-path', './venv/*',
                '-not', '-path', './temp/*'
            ],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )
        
        temp_files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        
        if not temp_files:
            report.add_task('temp_files_check', 'passed', '')
        else:
            file_list = '\n'.join(temp_files[:10])  # 10
            if len(temp_files) > 10:
                file_list += f'\n...  {len(temp_files) - 10} '
            
            report.add_task(
                'temp_files_check',
                'warning',
                f' {len(temp_files)} : make cleanup_temp',
                file_list
            )
        
        # 
        report_dirs = [
            Path('ai/maintenance_reports'),
            Path('ai/dataflow_reports')
        ]
        
        for report_dir in report_dirs:
            if report_dir.exists():
                json_files = list(report_dir.glob('*.json'))
                html_files = list(report_dir.glob('*.html'))
                total_reports = len(json_files) + len(html_files)
                
                if total_reports > 20:
                    report.add_task(
                        f'{report_dir.name}_cleanup',
                        'warning',
                        f'{report_dir}  {total_reports} : make cleanup_reports_smart',
                        f'JSON: {len(json_files)}, HTML: {len(html_files)}'
                    )
    
    except subprocess.TimeoutExpired:
        report.add_task('temp_files_check', 'warning', '')
    except FileNotFoundError:
        # Windows  find  Python 
        try:
            temp_files = []
            for root, dirs, files in Path('.').rglob('*_temp.*'):
                if not any(p in str(root) for p in ['.git', 'node_modules', '.venv', 'venv', 'temp']):
                    temp_files.append(str(root))
            
            if not temp_files:
                report.add_task('temp_files_check', 'passed', '')
            else:
                file_list = '\n'.join(temp_files[:10])
                if len(temp_files) > 10:
                    file_list += f'\n...  {len(temp_files) - 10} '
                
                report.add_task(
                    'temp_files_check',
                    'warning',
                    f' {len(temp_files)} : make cleanup_temp',
                    file_list
                )
        except Exception as e:
            report.add_task('temp_files_check', 'warning', f': {str(e)}')
    except Exception as e:
        report.add_task('temp_files_check', 'warning', f': {str(e)}')


def main():
    """"""
    print("=" * 70)
    print("AI ")
    print("=" * 70)
    print()
    
    report = MaintenanceReport()
    
    # 
    check_doc_style(report)
    check_encoding(report)
    check_consistency(report)
    update_docgen(report)
    check_deps(report)
    check_dag(report)
    check_contract_compat(report)
    check_test_status(report)
    check_app_structure(report)
    check_temp_files(report)
    
    # 
    print()
    print("=" * 70)
    print("")
    print("=" * 70)
    print(f": {report.summary['total']}")
    print(f": {report.summary['passed']}")
    print(f": {report.summary['failed']}")
    print(f": {report.summary['warnings']}")
    print()
    
    # 
    for task in report.tasks:
        status_icon = {
            'passed': '✓',
            'failed': '✗',
            'warning': '⚠'
        }.get(task['status'], '?')
        print(f"{status_icon} {task['task']}: {task['message']}")
        if task['details']:
            print(f"  : {task['details'][:100]}...")
    
    print()
    print("=" * 70)
    
    # 
    report_dir = Path('ai/maintenance_reports')
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"maintenance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report.save(report_file)
    print(f": {report_file}")
    
    # 
    if report.summary['failed'] > 0:
        print("\n[ERROR] ")
        return 1
    elif report.summary['warnings'] > 0:
        print("\n[WARNING] ")
        return 0
    else:
        print("\n[OK] ")
        return 0


if __name__ == '__main__':
    sys.exit(main())

