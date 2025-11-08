# AI Workdocs

> **用途**: AI开发任务的上下文管理  
> **创建时间**: 2025-11-08  
> **版本**: 1.0

---

## 概述

`workdocs/`目录用于管理AI开发任务的上下文、计划和进度。每个任务都有独立的目录，包含三个核心文件。

---

## 目录结构

```
workdocs/
├── active/             # 进行中的任务
│   └── <task-name>/
│       ├── plan.md     # 战略计划
│       ├── context.md  # 关键上下文（最重要）
│       └── tasks.md    # 任务清单
└── archive/            # 已完成的任务
    └── <task-name>/
        └── ...
```

---

## 三个核心文件

### 1. plan.md（战略计划）

**用途**: 任务的总体规划和实施方案

**内容**:
- 执行摘要（目标、范围）
- 当前状态分析
- 实施阶段（Phase划分）
- 风险管理
- 成功指标
- 时间线
- 依赖关系

**何时创建**: 任务开始前
**何时更新**: 计划调整时

---

### 2. context.md（关键上下文）⭐

**用途**: 上下文恢复和进度追踪（**最重要**）

**内容**:
- SESSION PROGRESS（已完成/进行中/待处理/阻塞）
- 关键文件状态
- 关键决策记录
- 错误记录（避免重复）
- 技术约束
- Quick Resume（快速恢复指令）

**何时创建**: 任务开始时
**何时更新**: 每完成一个milestone

⚠️ **重要**: 这是AI恢复上下文的首选文件，必须保持更新！

---

### 3. tasks.md（任务清单）

**用途**: 详细的任务列表和验收标准

**内容**:
- 任务清单（待办/进行中/已完成）
- 每个任务的验收标准
- 依赖关系
- 风险评估

**何时创建**: 任务开始时
**何时更新**: 任务状态变化时

---

## 使用流程

### 1. 创建新workdoc

```bash
# 使用脚本创建
make workdoc_create TASK=<task-name>

# 或手动创建
mkdir -p ai/workdocs/active/<task-name>
cd ai/workdocs/active/<task-name>
# 从模板复制文件
```

### 2. 更新上下文

在每个重要节点更新`context.md`：
- 完成一个任务 → 更新SESSION PROGRESS
- 做出关键决策 → 添加到关键决策
- 遇到错误 → 记录到错误记录
- 完成一个milestone → 更新整体状态

### 3. 归档任务

任务完成后：

```bash
# 使用脚本归档
make workdoc_archive TASK=<task-name>

# 或手动归档
mv ai/workdocs/active/<task-name> ai/workdocs/archive/
```

---

## 与ai/sessions/的区别

| 维度 | ai/sessions/ | ai/workdocs/ |
|------|-------------|-------------|
| 用途 | 会话历史记录 | 任务上下文管理 |
| 组织方式 | 按日期+会话名 | 按任务名 |
| 主要文件 | AI-SR-*.md | plan/context/tasks |
| 上下文恢复 | 不便于恢复 | 专为恢复设计 |
| 更新频率 | 一次性 | 持续更新 |

**使用建议**:
- 保留`sessions/`用于会话历史
- 使用`workdocs/`用于任务管理和上下文恢复
- 两者互补，不冲突

---

## 最佳实践

### DO ✅

- ✅ 每个任务创建独立目录
- ✅ 保持`context.md`实时更新
- ✅ 记录所有关键决策
- ✅ 记录错误和教训
- ✅ 任务完成后及时归档

### DON'T ❌

- ❌ 不要在多个任务间共享workdoc
- ❌ 不要忘记更新SESSION PROGRESS
- ❌ 不要忘记记录错误
- ❌ 不要在active/中保留已完成的任务

---

## 示例

查看模板示例：
- `doc/templates/workdoc-plan.md`
- `doc/templates/workdoc-context.md`
- `doc/templates/workdoc-tasks.md`

---

## 相关文档

- [WORKDOCS_GUIDE.md](../../doc/process/WORKDOCS_GUIDE.md) - 详细使用指南
- [workdoc_create.sh](../../scripts/workdoc_create.sh) - 创建脚本
- [workdoc_archive.sh](../../scripts/workdoc_archive.sh) - 归档脚本

