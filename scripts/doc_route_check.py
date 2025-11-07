#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_route_check.py - 文档路由校验工具

功能：
1. 遍历所有agent.md文件
2. 提取context_routes中的文档路径
3. 检查路径指向的文档是否存在
4. 输出缺失文档列表

用法：
    python scripts/doc_route_check.py
    make doc_route_check
"""

import os
import sys
import re
import yaml
from pathlib import Path

# 设置Windows控制台UTF-8输出
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent

# YAML Front Matter正则
YAML_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL | re.MULTILINE)


def extract_yaml_front_matter(md_text):
    """从Markdown文件中提取YAML Front Matter"""
    match = YAML_FRONT_MATTER_RE.match(md_text)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def find_agent_md_files():
    """查找所有agent.md文件"""
    agent_files = []
    
    # 根目录agent.md
    root_agent = REPO_ROOT / "agent.md"
    if root_agent.exists():
        agent_files.append(root_agent)
    
    # modules/下的agent.md
    modules_dir = REPO_ROOT / "modules"
    if modules_dir.exists():
        for agent_path in modules_dir.rglob("agent.md"):
            agent_files.append(agent_path)
    
    # 排除temp目录
    agent_files = [f for f in agent_files if "temp" not in str(f)]
    
    return agent_files


def extract_routes_from_context_routes(context_routes, agent_file_path):
    """从context_routes中提取所有路径"""
    routes = []
    
    if not context_routes:
        return routes
    
    # always_read
    if "always_read" in context_routes:
        for path in context_routes["always_read"]:
            routes.append(("always_read", path, agent_file_path))
    
    # on_demand
    if "on_demand" in context_routes:
        for item in context_routes["on_demand"]:
            topic = item.get("topic", "unknown")
            if "paths" in item:
                for path in item["paths"]:
                    routes.append(("on_demand", path, agent_file_path, topic))
    
    # by_scope
    if "by_scope" in context_routes:
        for item in context_routes["by_scope"]:
            scope = item.get("scope", "unknown")
            if "read" in item:
                for path in item["read"]:
                    routes.append(("by_scope", path, agent_file_path, scope))
    
    return routes


def resolve_path(path, agent_file_path):
    """解析路径（支持相对路径和绝对路径）"""
    # 相对路径（./开头）
    if path.startswith("./"):
        base_dir = agent_file_path.parent
        resolved = (base_dir / path).resolve()
        return resolved
    
    # 绝对路径（/开头）
    return REPO_ROOT / path.lstrip("/")


def check_path_exists(route_info):
    """检查路径是否存在"""
    route_type = route_info[0]
    path = route_info[1]
    agent_file = route_info[2]
    
    # 解析路径
    full_path = resolve_path(path, agent_file)
    
    # 检查存在性
    if full_path.exists():
        return True, None
    
    # 构建错误信息
    rel_agent = agent_file.relative_to(REPO_ROOT)
    
    if route_type == "always_read":
        error = f"always_read路径不存在: {path}"
    elif route_type == "on_demand":
        topic = route_info[3] if len(route_info) > 3 else "unknown"
        error = f"on_demand路径不存在: {path} (topic: {topic})"
    elif route_type == "by_scope":
        scope = route_info[3] if len(route_info) > 3 else "unknown"
        error = f"by_scope路径不存在: {path} (scope: {scope})"
    else:
        error = f"路径不存在: {path}"
    
    return False, {"agent": str(rel_agent), "error": error, "path": path}


def check_wildcard_paths(routes):
    """检查通配符路径（如modules/*/agent.md）"""
    issues = []
    
    for route_info in routes:
        path = route_info[1]
        
        # 检查是否包含通配符
        if "*" in path:
            agent_file = route_info[2]
            rel_agent = agent_file.relative_to(REPO_ROOT)
            
            # 尝试展开通配符
            pattern = path.lstrip("/")
            matches = list(REPO_ROOT.glob(pattern))
            
            if not matches:
                issues.append({
                    "agent": str(rel_agent),
                    "error": f"通配符路径无匹配: {path}",
                    "path": path
                })
    
    return issues


def main():
    """主函数"""
    print("=" * 60)
    print("文档路由校验")
    print("=" * 60)
    
    # 查找所有agent.md
    agent_files = find_agent_md_files()
    print(f"✓ 找到{len(agent_files)}个agent.md文件")
    
    if not agent_files:
        print("[warn] 未找到任何agent.md文件", file=sys.stderr)
        return 0
    
    # 提取所有routes
    all_routes = []
    files_with_routes = 0
    files_without_meta = 0
    
    for agent_file in agent_files:
        rel_path = agent_file.relative_to(REPO_ROOT)
        
        try:
            with open(agent_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            meta = extract_yaml_front_matter(content)
            if not meta:
                files_without_meta += 1
                continue
            
            if "context_routes" not in meta:
                continue
            
            routes = extract_routes_from_context_routes(meta["context_routes"], agent_file)
            if routes:
                all_routes.extend(routes)
                files_with_routes += 1
        
        except Exception as e:
            print(f"[warn] 读取{rel_path}失败: {e}", file=sys.stderr)
    
    print(f"✓ {files_with_routes}个文件包含context_routes")
    if files_without_meta > 0:
        print(f"  [info] {files_without_meta}个文件缺少YAML Front Matter（将在后续Phase补齐）")
    
    print(f"✓ 共提取{len(all_routes)}个路由")
    print()
    
    if not all_routes:
        print("[info] 暂无需要检查的路由")
        return 0
    
    # 检查路径
    print("检查路由路径...")
    missing_paths = []
    checked = 0
    
    for route_info in all_routes:
        exists, error_info = check_path_exists(route_info)
        checked += 1
        if not exists and error_info:
            missing_paths.append(error_info)
    
    # 检查通配符路径
    wildcard_issues = check_wildcard_paths(all_routes)
    
    # 汇总结果
    print()
    print("=" * 60)
    
    total_issues = len(missing_paths) + len(wildcard_issues)
    
    if total_issues == 0:
        print(f"✅ 校验通过: 所有{checked}个路由路径都存在")
    else:
        print(f"校验完成: {checked - total_issues}个路径存在, {total_issues}个路径缺失")
        print()
        
        if missing_paths:
            print("缺失的路径:")
            for item in missing_paths:
                print(f"  文件: {item['agent']}")
                print(f"  问题: {item['error']}")
                print()
        
        if wildcard_issues:
            print("通配符路径问题:")
            for item in wildcard_issues:
                print(f"  文件: {item['agent']}")
                print(f"  问题: {item['error']}")
                print()
    
    print("=" * 60)
    
    # 返回状态码（允许失败，仅警告）
    return 1 if total_issues > 0 else 0


if __name__ == "__main__":
    sys.exit(main())

