#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
registry_check.py - 模块注册表校验工具

功能：
1. 校验doc/orchestration/registry.yaml的完整性
2. 检查模块实例ID唯一性
3. 检查引用的agent_md路径存在性
4. 检查依赖关系无环（DAG检测）
5. 检查module_type引用的类型已定义

用法：
    python scripts/registry_check.py
    make registry_check
"""

import os
import sys
import yaml
from pathlib import Path
from collections import defaultdict

# 设置Windows控制台UTF-8输出
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 路径设置
HERE = Path(__file__).parent.absolute()
REPO_ROOT = HERE.parent
REGISTRY_PATH = REPO_ROOT / "doc" / "orchestration" / "registry.yaml"


def load_registry():
    """加载registry.yaml"""
    if not REGISTRY_PATH.exists():
        # 如果在docs/下查找（兼容Phase 3之前）
        alt_path = REPO_ROOT / "docs" / "orchestration" / "registry.yaml"
        if alt_path.exists():
            registry_path = alt_path
        else:
            print(f"[error] registry.yaml未找到", file=sys.stderr)
            print(f"  期望位置: {REGISTRY_PATH.relative_to(REPO_ROOT)}", file=sys.stderr)
            return None
    else:
        registry_path = REGISTRY_PATH
    
    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        print(f"✓ Registry已加载: {registry_path.relative_to(REPO_ROOT)}")
        return data
    except Exception as e:
        print(f"[error] 加载registry.yaml失败: {e}", file=sys.stderr)
        return None


def check_module_types(registry):
    """检查模块类型定义"""
    if "module_types" not in registry:
        print("[warn] registry.yaml缺少module_types定义", file=sys.stderr)
        return {}, []
    
    types = registry["module_types"]
    type_map = {}
    issues = []
    
    for t in types:
        if "id" not in t:
            issues.append("模块类型缺少id字段")
            continue
        
        type_id = t["id"]
        
        # 检查重复
        if type_id in type_map:
            issues.append(f"模块类型ID重复: {type_id}")
        
        type_map[type_id] = t
        
        # 检查必填字段
        required = ["name", "level"]
        missing = [f for f in required if f not in t]
        if missing:
            issues.append(f"类型'{type_id}'缺少字段: {', '.join(missing)}")
        
        # 检查level范围
        if "level" in t:
            level = t["level"]
            if not isinstance(level, int) or level < 1 or level > 4:
                issues.append(f"类型'{type_id}'的level必须在1-4之间: {level}")
    
    return type_map, issues


def check_module_instances(registry, type_map):
    """检查模块实例"""
    if "module_instances" not in registry:
        print("[warn] registry.yaml缺少module_instances定义", file=sys.stderr)
        return {}, []
    
    instances = registry["module_instances"]
    instance_map = {}
    issues = []
    
    for inst in instances:
        if "id" not in inst:
            issues.append("模块实例缺少id字段")
            continue
        
        inst_id = inst["id"]
        
        # 检查重复
        if inst_id in instance_map:
            issues.append(f"模块实例ID重复: {inst_id}")
        
        instance_map[inst_id] = inst
        
        # 检查必填字段
        required = ["type", "path", "level", "status"]
        missing = [f for f in required if f not in inst]
        if missing:
            issues.append(f"实例'{inst_id}'缺少字段: {', '.join(missing)}")
        
        # 检查type引用
        if "type" in inst:
            inst_type = inst["type"]
            if type_map and inst_type not in type_map:
                issues.append(f"实例'{inst_id}'引用的类型'{inst_type}'未定义")
        
        # 检查agent_md路径
        if "agent_md" in inst:
            agent_md_path = REPO_ROOT / inst["agent_md"]
            if not agent_md_path.exists():
                issues.append(f"实例'{inst_id}'的agent_md路径不存在: {inst['agent_md']}")
        
        # 检查path路径
        if "path" in inst:
            path = REPO_ROOT / inst["path"]
            if not path.exists():
                issues.append(f"实例'{inst_id}'的path路径不存在: {inst['path']}")
        
        # 检查status值
        if "status" in inst:
            status = inst["status"]
            valid_status = ["active", "deprecated", "wip", "archived"]
            if status not in valid_status:
                issues.append(f"实例'{inst_id}'的status值无效: {status}（有效值: {', '.join(valid_status)}）")
    
    return instance_map, issues


def check_dependencies_dag(instance_map):
    """检查依赖关系是否有环（DAG检测）"""
    if not instance_map:
        return []
    
    issues = []
    
    # 构建依赖图
    graph = defaultdict(list)
    for inst_id, inst in instance_map.items():
        if "upstream" in inst and inst["upstream"]:
            for upstream_id in inst["upstream"]:
                # upstream_id依赖于inst_id，所以边是 inst_id -> upstream_id
                # 实际上应该是 upstream_id -> inst_id（数据流向）
                # 这里我们检查upstream是否存在
                if upstream_id not in instance_map:
                    issues.append(f"实例'{inst_id}'的upstream'{upstream_id}'未定义")
                else:
                    graph[upstream_id].append(inst_id)
    
    # DFS检测环
    def has_cycle():
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {inst_id: WHITE for inst_id in instance_map}
        
        def dfs(node, path):
            if color[node] == GRAY:
                # 找到环
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                return cycle
            if color[node] == BLACK:
                return None
            
            color[node] = GRAY
            path.append(node)
            
            for neighbor in graph.get(node, []):
                result = dfs(neighbor, path[:])
                if result:
                    return result
            
            color[node] = BLACK
            return None
        
        for node in instance_map:
            if color[node] == WHITE:
                result = dfs(node, [])
                if result:
                    return result
        return None
    
    cycle = has_cycle()
    if cycle:
        cycle_str = " → ".join(cycle)
        issues.append(f"检测到循环依赖: {cycle_str}")
    
    return issues


def main():
    """主函数"""
    print("=" * 60)
    print("模块注册表校验")
    print("=" * 60)
    
    # 加载registry
    registry = load_registry()
    if not registry:
        print("[error] 无法加载registry.yaml", file=sys.stderr)
        return 1
    
    all_issues = []
    
    # 检查模块类型
    print("\n检查模块类型定义...")
    type_map, type_issues = check_module_types(registry)
    if type_issues:
        all_issues.extend(type_issues)
        for issue in type_issues:
            print(f"  [error] {issue}", file=sys.stderr)
    else:
        print(f"  ✓ 模块类型定义正常（{len(type_map)}个类型）")
    
    # 检查模块实例
    print("\n检查模块实例...")
    instance_map, inst_issues = check_module_instances(registry, type_map)
    if inst_issues:
        all_issues.extend(inst_issues)
        for issue in inst_issues:
            print(f"  [error] {issue}", file=sys.stderr)
    else:
        print(f"  ✓ 模块实例定义正常（{len(instance_map)}个实例）")
    
    # 检查依赖关系（DAG）
    print("\n检查依赖关系...")
    dag_issues = check_dependencies_dag(instance_map)
    if dag_issues:
        all_issues.extend(dag_issues)
        for issue in dag_issues:
            print(f"  [error] {issue}", file=sys.stderr)
    else:
        print(f"  ✓ 依赖关系无环")
    
    # 汇总
    print()
    print("=" * 60)
    if all_issues:
        print(f"校验失败: 发现{len(all_issues)}个问题")
        print("\n问题列表:")
        for i, issue in enumerate(all_issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("✅ 校验通过")
    print("=" * 60)
    
    return 1 if all_issues else 0


if __name__ == "__main__":
    sys.exit(main())

