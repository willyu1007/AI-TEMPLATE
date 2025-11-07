# agent.md使用规范

> 创建日期：2025-11-07
> 目的：明确repo中哪些目录需要agent.md，哪些不需要

---

## 核心原则

**agent.md的设计用途**：
- 为智能体编排系统提供**角色定义**和**行为约束**
- 定义**I/O接口**、**依赖关系**、**调度信息**
- 提供**文档路由**，指引模型按需读取

**适用对象**：
- 需要被Orchestrator调度的模块/组件
- 有明确角色和职责边界的实体
- 需要定义输入输出和依赖关系的模块

---

## 需要agent.md的目录

### ✅ 1. 根目录（必需）
**位置**: `/agent.md`

**用途**: 
- 全局策略和路由
- 合并策略声明（子级覆盖父级）
- 全局目标、安全和质量门槛引用
- 文档路由（context_routes）

**YAML必填字段**:
```yaml
spec_version: "1.0"
agent_id: "repo"
role: "policy_router"
policies: {goals_ref, safety_ref}
merge_strategy: "child_overrides_parent"
context_routes: {...}
```

---

### ✅ 2. 模块实例目录（必需）
**位置**: `/modules/<entity>/agent.md`

**用途**:
- 模块角色定义
- I/O接口规范
- 依赖关系声明
- 权限范围（ownership.code_paths）
- 调度提示（orchestration_hints）
- 文档路由

**YAML必填字段**:
```yaml
spec_version: "1.0"
agent_id: "modules.<entity>.<instance>"
role: "模块角色描述"
level: 1|2|3|4
module_type: "类型标识"
ownership: {code_paths: {include, exclude}}
io: {inputs, outputs}
dependencies: {upstream, downstream}
context_routes: {...}
```

**示例**: 
- ✅ `/modules/example/agent.md`
- ✅ `/modules/user/agent.md`
- ✅ `/modules/order/agent.md`

---

### ✅ 3. 应用层目录（可选，按需）
**位置**: 
- `/app/agent.md` (单一后端入口)
- `/apps/<name>/agent.md` (多后端入口)
- `/frontend/agent.md` (单一前端入口)
- `/frontends/<name>/agent.md` (多前端入口)

**用途**: 
- 应用层的编排信息
- 路由分发规则
- 全局中间件策略

**是否需要**:
- 如果应用层仅做简单的路由分发 → **不需要**
- 如果应用层有复杂的编排逻辑 → **可选**

**建议**: 
- 小型项目：app/和frontend/不需要agent.md
- 大型项目：如有复杂编排需求可添加

---

## 不需要agent.md的目录

### ❌ 1. 配置目录
**目录**: 
- `/schemas/` - Schema定义
- `/config/` - 配置文件
- `/evals/` - 评测基线

**原因**: 
- 不是业务模块
- 不需要被调度
- 不需要定义I/O和依赖

**应该有**: 
- ✅ README.md - 说明目录用途

---

### ❌ 2. 工具目录
**目录**:
- `/scripts/` - 自动化脚本
- `/tools/` - 工具契约定义

**原因**:
- 工具集合，不是模块
- 不参与业务编排
- 脚本通过Makefile调用，不需要编排

**应该有**:
- ✅ README.md - 脚本列表和使用说明

---

### ❌ 3. 文档目录
**目录**:
- `/doc/` (或`/docs/`)
- `/doc/orchestration/`
- `/doc/policies/`
- `/doc/init/`
- `/doc/modules/`等

**原因**:
- 存放文档，不是模块
- 被agent.md引用，而不是包含agent.md
- 通过context_routes访问

**应该有**:
- ✅ README.md - 文档目录说明

---

### ❌ 4. 测试和数据目录
**目录**:
- `/tests/` - 测试文件
- `/db/` - 数据库定义
- `/migrations/` - 迁移脚本

**原因**:
- 辅助目录，不是模块
- 不需要编排调度

**应该有**:
- ✅ README.md - 说明和使用指南

---

### ❌ 5. 共享代码目录
**目录**:
- `/common/` - 共享代码库
- `/observability/` - 可观测性配置

**原因**:
- 共享资源，不是独立模块
- 被其他模块使用，不独立调度

**应该有**:
- ✅ README.md - 说明可用的工具/组件

---

### ❌ 6. 其他辅助目录
**目录**:
- `/ai/` - AI会话记录
- `/.aicontext/` - AI上下文索引
- `/.github/` - GitHub配置
- `/temp/` - 临时文件

**原因**:
- 辅助或临时目录
- 不参与业务逻辑

---

## 决策树

```
问：某个目录是否需要agent.md？

该目录是业务模块（modules/下）？
├─ 是 → ✅ 需要agent.md
└─ 否 → 继续判断

该目录是应用入口（app/frontend/）且有复杂编排逻辑？
├─ 是 → 🟡 可选agent.md
└─ 否 → 继续判断

该目录是配置/工具/文档/测试/共享代码？
├─ 是 → ❌ 不需要agent.md，仅需README.md
└─ 否 → 特殊情况，咨询团队
```

---

## 目录与文档对照表

| 目录 | agent.md | README.md | 说明 |
|------|---------|-----------|------|
| `/` | ✅ 必需 | ✅ 必需 | 根目录策略 |
| `/modules/<entity>/` | ✅ 必需 | ✅ 必需 | 业务模块 |
| `/app/` 或 `/apps/<name>/` | 🟡 可选 | ✅ 必需 | 应用入口 |
| `/frontend/` 或 `/frontends/<name>/` | 🟡 可选 | ✅ 必需 | 前端入口 |
| `/schemas/` | ❌ 不需要 | ✅ 必需 | Schema定义 |
| `/scripts/` | ❌ 不需要 | ✅ 必需 | 自动化脚本 |
| `/doc/` (或`/docs/`) | ❌ 不需要 | ✅ 建议 | 文档目录 |
| `/config/` | ❌ 不需要 | ✅ 建议 | 配置文件 |
| `/common/` | ❌ 不需要 | ✅ 必需 | 共享代码 |
| `/tests/` | ❌ 不需要 | ✅ 建议 | 测试文件 |
| `/db/` | ❌ 不需要 | ✅ 建议 | 数据库定义 |
| `/tools/` | ❌ 不需要 | ✅ 建议 | 工具契约 |
| `/observability/` | ❌ 不需要 | ✅ 必需 | 可观测性 |
| `/evals/` | ❌ 不需要 | ✅ 建议 | 评测基线 |
| `/ai/` | ❌ 不需要 | ✅ 建议 | AI会话记录 |
| `/.aicontext/` | ❌ 不需要 | ❌ 不需要 | 自动生成 |

---

## 实施指南

### Phase 1（已完成）
- [x] 创建`/schemas/README.md` ✅
- [x] 确认`/scripts/README.md`已存在 ✅

### Phase 2（待执行）
- [ ] 创建`/doc/README.md`（说明文档目录结构）
- [ ] 创建`/db/README.md`（说明数据库治理结构）

### Phase 3（待执行）
- [ ] 为根目录`/agent.md`添加YAML Front Matter

### Phase 4（待执行）
- [ ] 为`/modules/example/`创建agent.md

### Phase 9（待执行）
- [ ] 检查所有目录的README.md是否齐全
- [ ] 验证agent.md仅在应该有的目录中存在
- [ ] 清理多余的agent.md（如有）

---

## 常见问题

### Q1: config/目录为什么不需要agent.md？
**A**: config/存放配置文件（YAML/JSON），不是业务模块，不需要被Orchestrator调度。仅需README.md说明配置结构。

### Q2: common/目录为什么不需要agent.md？
**A**: common/是共享代码库，被其他模块使用，本身不是独立的业务模块。它的"角色"是提供工具函数和共享组件，通过README.md说明即可。

### Q3: 是否每个子目录都需要README.md？
**A**: 建议所有一级目录都有README.md，但不强制。关键目录（modules/, common/, doc/, schemas/, scripts/等）必须有。

### Q4: app/和frontend/什么时候需要agent.md？
**A**: 
- 简单项目（仅做路由分发）→ 不需要
- 复杂项目（有编排逻辑、多步骤处理）→ 可选
- 建议：先不创建，如有需要再补充

---

## 模板说明

### modules/<entity>/应该有的文档
```
modules/<entity>/
├── agent.md          ✅ 必需（Phase 4补充）
├── README.md         ✅ 必需
├── plan.md           ✅ 必需
└── doc/              
    ├── CHANGELOG.md  ✅ 必需
    ├── CONTRACT.md   ✅ 必需
    ├── PROGRESS.md   ✅ 必需
    ├── BUGS.md       ✅ 必需
    ├── RUNBOOK.md    ✅ 必需
    └── TEST_PLAN.md  ✅ 必需
```

### 其他目录应该有的文档
```
/schemas/           ✅ README.md（Phase 1已创建）
/scripts/           ✅ README.md（Phase 1已创建）
/doc/               ✅ README.md（Phase 2创建）
/db/                ✅ README.md（Phase 5创建）
/common/            ✅ README.md（已有）
/config/            ✅ README.md（已有）
/observability/     ✅ README.md（已有）
/tests/             ✅ README.md（已有）
```

---

## 总结

**需要agent.md**:
- ✅ 根目录（1个）
- ✅ 每个模块实例（modules/<entity>/，N个）
- 🟡 应用层（app/frontend/，可选）

**不需要agent.md**:
- ❌ 配置目录（schemas/, config/, evals/）
- ❌ 工具目录（scripts/, tools/）
- ❌ 文档目录（doc/及其子目录）
- ❌ 辅助目录（tests/, db/, ai/, .aicontext/等）
- ❌ 共享代码（common/, observability/）

**关键区别**:
- **业务模块** = 需要agent.md
- **辅助目录/工具** = 不需要agent.md，仅需README.md

---

**此规范将在Phase 9验收时检查！**


