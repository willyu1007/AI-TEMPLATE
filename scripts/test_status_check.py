#!/usr/bin/env python3
"""
人工测试状态检查脚本
检查模块的 TEST_PLAN.md 中是否包含人工测试跟踪章节，并验证测试状态
"""

import sys
import re
import pathlib
from typing import List, Dict, Tuple

# Windows控制台编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def find_test_plans(root_dir: pathlib.Path = pathlib.Path('.')) -> List[pathlib.Path]:
    """查找所有 TEST_PLAN.md 文件"""
    test_plans = []
    modules_dir = root_dir / 'modules'
    
    if not modules_dir.exists():
        return test_plans
    
    for module_dir in modules_dir.iterdir():
        if module_dir.is_dir():
            test_plan = module_dir / 'TEST_PLAN.md'
            if test_plan.exists():
                test_plans.append(test_plan)
    
    return test_plans


def check_manual_test_tracking(test_plan_path: pathlib.Path) -> Tuple[bool, List[str], int]:
    """检查 TEST_PLAN.md 是否包含人工测试跟踪章节"""
    try:
        content = test_plan_path.read_text(encoding='utf-8')
    except Exception as e:
        return False, [f"无法读取文件: {e}"], 0
    
    issues = []
    
    # 检查是否包含"人工测试跟踪"或"Manual Test Tracking"章节
    has_section = bool(re.search(
        r'##\s+(人工测试跟踪|Manual Test Tracking|人工测试状态|Manual Test Status)',
        content,
        re.IGNORECASE
    ))
    
    if not has_section:
        issues.append("缺少人工测试跟踪章节")
        return False, issues, 0
    
    # 检查是否包含测试状态表格
    has_table = bool(re.search(
        r'\|.*状态.*\|.*测试人员.*\|.*测试日期.*\|',
        content,
        re.IGNORECASE | re.MULTILINE
    )) or bool(re.search(
        r'\|.*status.*\|.*tester.*\|.*date.*\|',
        content,
        re.IGNORECASE | re.MULTILINE
    ))
    
    if not has_table:
        issues.append("缺少测试状态跟踪表格")
    
    # 检查是否有待测试的功能
    pending_tests = re.findall(
        r'(待测试|pending|测试中|testing|in progress)',
        content,
        re.IGNORECASE
    )
    
    return True, issues, len(pending_tests)


def check_test_status_format(test_plan_path: pathlib.Path) -> Tuple[bool, List[str]]:
    """检查测试状态格式是否正确"""
    try:
        content = test_plan_path.read_text(encoding='utf-8')
    except Exception:
        return False, ["无法读取文件"]
    
    issues = []
    
    # 检查状态值是否规范
    valid_statuses = ['待测试', '测试中', '已通过', '已失败', '已跳过',
                     'pending', 'testing', 'passed', 'failed', 'skipped',
                     'in progress', 'completed']
    
    # 查找状态表格
    status_pattern = r'\|[^|]+\|([^|]+)\|'  # 匹配状态列
    matches = re.finditer(status_pattern, content)
    
    for match in matches:
        status = match.group(1).strip().lower()
        if status and status not in [s.lower() for s in valid_statuses]:
            if status not in ['', '状态', 'status']:  # 忽略表头
                issues.append(f"发现非标准状态值: {status}")
    
    return len(issues) == 0, issues


def main():
    """主函数"""
    print("检查人工测试跟踪状态...\n")
    
    test_plans = find_test_plans()
    
    if not test_plans:
        print("未找到任何 TEST_PLAN.md 文件")
        print("提示: 确保 modules/ 目录下有模块")
        sys.exit(0)
    
    print(f"找到 {len(test_plans)} 个测试计划文件\n")
    
    all_passed = True
    total_pending = 0
    
    for test_plan in test_plans:
        module_name = test_plan.parent.name
        print(f"检查模块: {module_name}")
        
        # 检查是否包含人工测试跟踪章节
        has_tracking, issues, pending_count = check_manual_test_tracking(test_plan)
        
        if not has_tracking:
            print(f"  ❌ {', '.join(issues)}")
            all_passed = False
        else:
            # 检查格式
            format_ok, format_issues = check_test_status_format(test_plan)
            
            if format_issues:
                print(f"  ⚠️  格式问题: {', '.join(format_issues)}")
            else:
                print(f"  ✓ 人工测试跟踪章节存在")
            
            if pending_count > 0:
                print(f"  ⚠️  发现 {pending_count} 个待测试/测试中的功能")
                total_pending += pending_count
        
        print()
    
    # 总结
    print("=" * 50)
    if all_passed:
        print("✅ 所有模块都包含人工测试跟踪章节")
        if total_pending > 0:
            print(f"⚠️  共有 {total_pending} 个功能等待人工测试")
            print("💡 建议: 定期审查并更新测试状态")
    else:
        print("❌ 部分模块缺少人工测试跟踪章节")
        print("💡 建议: 在 TEST_PLAN.md 中添加'人工测试跟踪'章节")
    
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()

