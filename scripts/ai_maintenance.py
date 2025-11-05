"""
AI 自动维护脚本
定期检查和维护仓库，确保文档、代码、配置的一致性

使用场景：
1. 每次 AI 任务执行后自动运行
2. 定期（每日/每周）自动维护
3. 手动触发：python scripts/ai_maintenance.py
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
import io

# Windows控制台编码修复
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 维护任务类型
MAINTENANCE_TASKS = [
    'doc_style_check',      # 文档风格检查
    'encoding_check',       # 编码检查
    'consistency_check',    # 一致性检查
    'docgen',               # 文档索引更新
    'deps_check',           # 依赖检查
    'dag_check',            # DAG 检查
    'contract_compat_check', # 契约兼容性检查
]

# 维护报告
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
        """添加任务结果"""
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
        """转换为 JSON"""
        return json.dumps({
            'timestamp': self.timestamp,
            'summary': self.summary,
            'tasks': self.tasks
        }, indent=2, ensure_ascii=False)
    
    def save(self, file_path: Path):
        """保存报告"""
        file_path.write_text(self.to_json(), encoding='utf-8')


def run_make_command(target: str) -> Tuple[int, str, str]:
    """运行 make 命令"""
    try:
        result = subprocess.run(
            ['make', target],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=300  # 5 分钟超时
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, '', f'命令超时: make {target}'
    except FileNotFoundError:
        return 1, '', f'make 命令未找到'
    except Exception as e:
        return 1, '', f'执行错误: {str(e)}'


def check_doc_style(report: MaintenanceReport):
    """检查文档风格"""
    print("检查文档风格...")
    returncode, stdout, stderr = run_make_command('doc_style_check')
    
    if returncode == 0:
        report.add_task('doc_style_check', 'passed', '文档风格检查通过')
    else:
        # 提取问题数量
        issues = stdout.count('第') if stdout else 0
        report.add_task(
            'doc_style_check',
            'warning' if issues < 10 else 'failed',
            f'发现 {issues} 个文档风格问题',
            stdout[:500]  # 限制输出长度
        )


def check_encoding(report: MaintenanceReport):
    """检查文件编码"""
    print("检查文件编码...")
    # 直接运行脚本（因为可能没有 make target）
    try:
        result = subprocess.run(
            [sys.executable, 'scripts/encoding_check.py'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60
        )
        if result.returncode == 0:
            report.add_task('encoding_check', 'passed', '所有文件都是 UTF-8 编码')
        else:
            # 提取非 UTF-8 文件数量
            non_utf8 = result.stdout.count('文件:') if result.stdout else 0
            report.add_task(
                'encoding_check',
                'warning' if non_utf8 < 5 else 'failed',
                f'发现 {non_utf8} 个非 UTF-8 编码文件',
                result.stdout[:500]
            )
    except Exception as e:
        report.add_task('encoding_check', 'failed', f'编码检查失败: {str(e)}')


def update_docgen(report: MaintenanceReport):
    """更新文档索引"""
    print("更新文档索引...")
    returncode, stdout, stderr = run_make_command('docgen')
    
    if returncode == 0:
        report.add_task('docgen', 'passed', '文档索引更新成功')
    else:
        report.add_task('docgen', 'failed', '文档索引更新失败', stderr[:500])


def check_consistency(report: MaintenanceReport):
    """检查一致性"""
    print("检查一致性...")
    returncode, stdout, stderr = run_make_command('consistency_check')
    
    if returncode == 0:
        report.add_task('consistency_check', 'passed', '一致性检查通过')
    else:
        report.add_task('consistency_check', 'warning', '发现一致性问题', stdout[:500])


def check_deps(report: MaintenanceReport):
    """检查依赖"""
    print("检查依赖...")
    returncode, stdout, stderr = run_make_command('deps_check')
    
    if returncode == 0:
        report.add_task('deps_check', 'passed', '依赖检查通过')
    else:
        report.add_task('deps_check', 'warning', '发现依赖问题', stdout[:500])


def check_dag(report: MaintenanceReport):
    """检查 DAG"""
    print("检查 DAG...")
    returncode, stdout, stderr = run_make_command('dag_check')
    
    if returncode == 0:
        report.add_task('dag_check', 'passed', 'DAG 检查通过')
    else:
        report.add_task('dag_check', 'failed', 'DAG 检查失败', stderr[:500])


def check_contract_compat(report: MaintenanceReport):
    """检查契约兼容性"""
    print("检查契约兼容性...")
    returncode, stdout, stderr = run_make_command('contract_compat_check')
    
    if returncode == 0:
        report.add_task('contract_compat_check', 'passed', '契约兼容性检查通过')
    else:
        report.add_task('contract_compat_check', 'warning', '发现契约兼容性问题', stdout[:500])


def check_test_status(report: MaintenanceReport):
    """检查人工测试状态"""
    print("检查人工测试状态...")
    try:
        result = subprocess.run(
            [sys.executable, 'scripts/test_status_check.py'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60
        )
        if result.returncode == 0:
            report.add_task('test_status_check', 'passed', '人工测试跟踪检查通过')
        else:
            # 提取待测试功能数量
            pending = result.stdout.count('待测试') + result.stdout.count('pending')
            report.add_task(
                'test_status_check',
                'warning',
                f'发现 {pending} 个待测试功能，建议定期审查',
                result.stdout[:500]
            )
    except Exception as e:
        report.add_task('test_status_check', 'warning', f'测试状态检查失败: {str(e)}')


def check_app_structure(report: MaintenanceReport):
    """检查应用层结构"""
    print("检查应用层结构...")
    try:
        result = subprocess.run(
            [sys.executable, 'scripts/app_structure_check.py'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60
        )
        if result.returncode == 0:
            report.add_task('app_structure_check', 'passed', '应用层结构检查通过')
        else:
            # 提取问题数量
            issues = result.stdout.count('❌') + result.stdout.count('⚠️')
            report.add_task(
                'app_structure_check',
                'warning' if issues < 5 else 'failed',
                f'发现 {issues} 个应用层结构问题',
                result.stdout[:500]
            )
    except Exception as e:
        report.add_task('app_structure_check', 'warning', f'应用层结构检查失败: {str(e)}')


def main():
    """主函数"""
    print("=" * 70)
    print("AI 自动维护脚本")
    print("=" * 70)
    print()
    
    report = MaintenanceReport()
    
    # 执行维护任务
    check_doc_style(report)
    check_encoding(report)
    check_consistency(report)
    update_docgen(report)
    check_deps(report)
    check_dag(report)
    check_contract_compat(report)
    check_test_status(report)
    check_app_structure(report)
    
    # 生成报告
    print()
    print("=" * 70)
    print("维护报告摘要")
    print("=" * 70)
    print(f"总任务数: {report.summary['total']}")
    print(f"通过: {report.summary['passed']}")
    print(f"失败: {report.summary['failed']}")
    print(f"警告: {report.summary['warnings']}")
    print()
    
    # 详细任务结果
    for task in report.tasks:
        status_icon = {
            'passed': '✓',
            'failed': '✗',
            'warning': '⚠'
        }.get(task['status'], '?')
        print(f"{status_icon} {task['task']}: {task['message']}")
        if task['details']:
            print(f"  详情: {task['details'][:100]}...")
    
    print()
    print("=" * 70)
    
    # 保存报告
    report_dir = Path('ai/maintenance_reports')
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"maintenance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report.save(report_file)
    print(f"报告已保存: {report_file}")
    
    # 返回退出码
    if report.summary['failed'] > 0:
        print("\n[ERROR] 发现失败项，请检查并修复")
        return 1
    elif report.summary['warnings'] > 0:
        print("\n[WARNING] 发现警告项，建议检查")
        return 0
    else:
        print("\n[OK] 所有检查通过")
        return 0


if __name__ == '__main__':
    sys.exit(main())

