#!/usr/bin/env python3
"""

 TEST_PLAN.md 
"""

import sys
import re
import pathlib
from typing import List, Dict, Tuple

# Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def find_test_plans(root_dir: pathlib.Path = pathlib.Path('.')) -> List[pathlib.Path]:
    """ TEST_PLAN.md """
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
    """ TEST_PLAN.md """
    try:
        content = test_plan_path.read_text(encoding='utf-8')
    except Exception as e:
        return False, [f": {e}"], 0
    
    issues = []
    
    # """Manual Test Tracking"
    has_section = bool(re.search(
        r'##\s+(|Manual Test Tracking||Manual Test Status)',
        content,
        re.IGNORECASE
    ))
    
    if not has_section:
        issues.append("")
        return False, issues, 0
    
    # 
    has_table = bool(re.search(
        r'\|.*.*\|.*.*\|.*.*\|',
        content,
        re.IGNORECASE | re.MULTILINE
    )) or bool(re.search(
        r'\|.*status.*\|.*tester.*\|.*date.*\|',
        content,
        re.IGNORECASE | re.MULTILINE
    ))
    
    if not has_table:
        issues.append("")
    
    # 
    pending_tests = re.findall(
        r'(|pending||testing|in progress)',
        content,
        re.IGNORECASE
    )
    
    return True, issues, len(pending_tests)


def check_test_status_format(test_plan_path: pathlib.Path) -> Tuple[bool, List[str]]:
    """"""
    try:
        content = test_plan_path.read_text(encoding='utf-8')
    except Exception:
        return False, [""]
    
    issues = []
    
    # 
    valid_statuses = ['', '', '', '', '',
                     'pending', 'testing', 'passed', 'failed', 'skipped',
                     'in progress', 'completed']
    
    # 
    status_pattern = r'\|[^|]+\|([^|]+)\|'  # 
    matches = re.finditer(status_pattern, content)
    
    for match in matches:
        status = match.group(1).strip().lower()
        if status and status not in [s.lower() for s in valid_statuses]:
            if status not in ['', '', 'status']:  # 
                issues.append(f": {status}")
    
    return len(issues) == 0, issues


def main():
    """"""
    print("...\n")
    
    test_plans = find_test_plans()
    
    if not test_plans:
        print(" TEST_PLAN.md ")
        print(":  modules/ ")
        sys.exit(0)
    
    print(f" {len(test_plans)} \n")
    
    all_passed = True
    total_pending = 0
    
    for test_plan in test_plans:
        module_name = test_plan.parent.name
        print(f": {module_name}")
        
        # 
        has_tracking, issues, pending_count = check_manual_test_tracking(test_plan)
        
        if not has_tracking:
            print(f"  ❌ {', '.join(issues)}")
            all_passed = False
        else:
            # 
            format_ok, format_issues = check_test_status_format(test_plan)
            
            if format_issues:
                print(f"  ⚠️  : {', '.join(format_issues)}")
            else:
                print(f"  ✓ ")
            
            if pending_count > 0:
                print(f"  ⚠️   {pending_count} /")
                total_pending += pending_count
        
        print()
    
    # 
    print("=" * 50)
    if all_passed:
        print("✅ ")
        if total_pending > 0:
            print(f"⚠️   {total_pending} ")
            print("💡 : ")
    else:
        print("❌ ")
        print("💡 :  TEST_PLAN.md ''")
    
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()

