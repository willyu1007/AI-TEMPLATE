# 模块实例目录

> 自动生成时间: 2025-11-07 17:59:18
> 来源: doc/orchestration/registry.yaml
> 生成命令: `make module_doc_gen`

---

## 目标

本文档提供所有模块实例的索引和简介，包括：
- 模块类型定义
- 模块实例列表（按层级分组）
- 实例状态、版本、责任人
- 依赖关系图

---

## 模块类型

### 1级模块类型
#### 1_example - 示例模块类型
- **描述**: 一级基础模块，用于演示模块结构和规范
- **I/O契约**: 标准HTTP请求/响应，详见modules/example/doc/CONTRACT.md

---

## 模块实例

（暂无模块实例）
---

## 依赖关系图

---

## 说明

### 状态标记
- 🟢 active: 活跃开发中
- 🟡 wip: 工作进行中（未完成）
- 🔴 deprecated: 已弃用
- ⚫ archived: 已归档

### 更新方式
1. 修改`doc/orchestration/registry.yaml`
2. 运行`make module_doc_gen`重新生成本文档

### 相关文档
- 模块类型详细说明: [MODULE_TYPES.md](MODULE_TYPES.md)
- 模块初始化规范: [MODULE_INIT_GUIDE.md](MODULE_INIT_GUIDE.md)
- 编排注册表: [../orchestration/registry.yaml](../orchestration/registry.yaml)
