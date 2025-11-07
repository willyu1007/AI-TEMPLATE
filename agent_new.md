---
spec_version: "1.0"
agent_id: "repo"
role: "AI-TEMPLATE仓库根编排配置，指导AI高效开发"

policies:
  goals_ref: /doc/policies/goals.md
  safety_ref: /doc/policies/safety.md

merge_strategy: "child_overrides_parent"

context_routes:
  always_read:
    - /doc/policies/goals.md
    - /doc/policies/safety.md
    - /README.md
  on_demand:
    - topic: "数据库操作"
      paths:
        - /docs/db/DB_SPEC.yaml
        - /docs/db/SCHEMA_GUIDE.md
        - /db/engines/README.md
    - topic: "模块开发"
      paths:
        - /doc/modules/MODULE_INIT_GUIDE.md
        - /doc/modules/MODULE_TYPES.md
        - /doc/modules/MODULE_INSTANCES.md
    - topic: "项目初始化"
      paths:
        - /doc/init/PROJECT_INIT_GUIDE.md
    - topic: "配置管理"
      paths:
        - /config/README.md
        - /docs/process/CONFIG_GUIDE.md
  by_scope:
    - scope: "模块开发"
      read:
        - /doc/modules/MODULE_INIT_GUIDE.md
        - /doc/modules/TEMPLATES/
    - scope: "编排管理"
      read:
        - /doc/orchestration/registry.yaml
        - /doc/orchestration/routing.md
---

# agent.md

> 本规程面向**让模型高效工作**、**降低重复思考**，并确保在每次任务中模型能**完整理解当前项目状态**。

---

## 重要提醒（在开始任何任务前必读）

在开始任何任务前，模型必须：

1. **阅读文档格式规范**：见 §5 文档编写规范，特别是：
   - 禁止使用颜文字（Emoji）
   - 语言一致性要求（中文简体）
   - 结构化输出要求

2. **遵循工作流程**：见 §0 快速开始，按照 S0-S6 步骤执行

3. **理解职责边界**：见 doc/policies/roles.md

---

## 0. 快速开始

**适用：项目初始化 / 新功能模块 / 日常开发与维护**。模型每次执行任务都遵循下列步骤：

### S0 - 刷新上下文（必做，分层）

读取以下"单一事实源（SSOT）与摘要"，按优先级分层：

- **Tier-0（必须）**：`/.aicontext/snapshot.json`、`/.aicontext/module_index.json`
- **Tier-1（强烈建议）**：`/flows/dag.yaml`、相关 `tools/*/contract.json`、目标模块 `plan.md` / `README.md`
- **Tier-2（建议）**：`/docs/db/DB_SPEC.yaml`、`/docs/process/ENV_SPEC.yaml`、`/config/*.yaml`
- **Tier-3（按需）**：`TEST_PLAN.md`、`RUNBOOK.md`、`PROGRESS.md`、`BUGS.md`、项目与 UX 文档

> 若 `/.aicontext/snapshot.json` 的 `snapshot_hash` 变化，必须先运行 `make docgen` 以生成最新索引。

### S1 - 任务建模

在目标模块下更新 `/modules/<name>/plan.md`：明确**范围/切片/接口/数据/风险/验证命令**。若新增模块，先运行：

```bash
make ai_begin MODULE=<name>
# 或参考：doc/modules/MODULE_INIT_GUIDE.md
```

> **重要边界区分**：
> - `plan.md` = **未来一次迭代**的计划/假设/验证/回滚（进入实现前**必须更新**）
> - `PROGRESS.md` = **历史**进度与里程碑/状态快照（完成/阻塞/延期）

### S2 - 方案预审（AI-SR: Plan）

生成 `/ai/sessions/<date>_<name>/AI-SR-plan.md`（自审：意图、影响面、DAG/契约/DB 变更点、测试点、回滚）。通过后进入实现。

### S3 - 实现与最小验证

仅在**计划范围内**修改代码；保持向后兼容。更新或新增测试，运行 `make dev_check`。

### S4 - 文档与索引更新

同步更新：`CONTRACT.md/contract.json`、`TEST_PLAN.md`、`RUNBOOK.md`、`PROGRESS.md`、`CHANGELOG.md`、`flows/dag.yaml`。运行 `make docgen` 刷新 `/.aicontext/`。

### S5 - 自审与 PR

生成 `/ai/sessions/<date>_<name>/AI-SR-impl.md`；提交 PR，附 plan 与 AI-SR。CI 门禁通过后合入。

### S6 - 自动维护（必做）

每次任务完成后运行 `make ai_maintenance`，确保仓库状态良好。

---

## 1. 目录规范（约定优于配置）

### 核心目录结构

```text
.
├── .aicontext/              # AI上下文索引（docgen生成）
├── ai/
│   ├── LEDGER.md            # 任务清册
│   └── sessions/            # 自审记录
├── doc/                     # 文档层（规范、指南）
│   ├── orchestration/       # 编排配置
│   ├── policies/            # 全局策略
│   ├── indexes/             # 索引规则
│   ├── init/                # 初始化指南
│   └── modules/             # 模块相关
├── docs/                    # 项目文档
│   ├── project/
│   ├── process/
│   ├── db/
│   └── ux/
├── config/                  # 配置文件
├── db/                      # 数据库层
│   └── engines/
├── modules/                 # 业务模块
│   └── <entity>/
│       ├── agent.md         # 模块Agent配置
│       ├── README.md
│       ├── plan.md
│       ├── doc/             # 6个文档
│       ├── core/            # 核心逻辑（必需）
│       ├── api/             # API层（可选）
│       ├── frontend/        # 前端组件（可选）
│       └── models/          # 数据模型（可选）
├── common/                  # 公共层
├── schemas/                 # Schema定义
├── scripts/                 # 工具脚本
├── tests/                   # 测试
└── tools/                   # 工具契约
```

### 应用层（可选）

根据项目需求选择：

#### 选项A: 无应用层
适用：微服务、库项目
```
modules/ + common/
```

#### 选项B: 仅后端应用层
适用：纯后端服务、API服务
```
app/routes/ + modules/
```

#### 选项C: 完整应用层
适用：全栈项目、单体应用
```
app/routes/ + frontend/ + modules/
```

---

## 1.3 应用层与模块层职责边界

### 核心原则

```
应用层 (app/frontend/) = 入口、路由、分发
模块层 (modules/<entity>/) = 业务逻辑实现
```

### 应用层职责

#### app/routes/ (后端应用入口)
- **职责**: 
  - 应用入口点
  - HTTP请求路由分发
  - 全局中间件（认证、日志、限流）
- **不包含**: 业务逻辑（应在modules/中）

#### frontend/ (前端应用入口)
- **职责**:
  - 前端入口点（main.ts/App.vue）
  - 应用级路由配置
  - 全局共享组件（Layout、Button、Modal）
  - 全局状态管理
- **不包含**: 业务组件（应在modules/<entity>/frontend/）

### 模块层职责

#### modules/<entity>/core/ (必需)
- **职责**: 核心业务逻辑
- **调用**: 被api/或其他core/调用

#### modules/<entity>/api/ (可选)
- **创建条件**: 模块对外提供HTTP接口
- **职责**: 定义路由、参数验证、调用core/
- **注册**: 在app/routes/中注册

#### modules/<entity>/frontend/ (可选)
- **创建条件**: 模块有特定的UI组件
- **职责**: 实现模块专属的前端组件
- **使用**: 在frontend/pages/中引入

### 决策树

```
代码应该放在哪里？

是否是业务逻辑？
├─ 否 → 是否是全局UI？
│   ├─ 是 → frontend/components/
│   └─ 否 → app/routes/ 或 frontend/pages/
└─ 是 → modules/<entity>/core/
    └─ 是否需要HTTP接口？
        ├─ 是 → modules/<entity>/api/ + 在app/routes/注册
        └─ 否 → 仅modules/<entity>/core/
    └─ 是否需要UI组件？
        ├─ 是 → modules/<entity>/frontend/
        └─ 否 → 无需frontend/
```

### 调用关系

```
app/routes/
    ↓ (路由分发)
modules/<entity>/api/
    ↓ (调用业务逻辑)
modules/<entity>/core/
    ↓ (使用公共层)
common/

frontend/pages/
    ↓ (使用业务组件)
modules/<entity>/frontend/
    ↓ (调用API)
modules/<entity>/api/
```

**详见**: temp/app_frontend_职责划分说明.md（Phase 3后将迁移到doc/）

---

## 2. 文档路由与上下文

### 记忆机制

1. **AI Ledger**：`/ai/LEDGER.md` 记录每次任务的：上下文引用、关键决策、变更范围、遗留项。
2. **Sessions**：每次任务在 `/ai/sessions/<date>_<mod>/` 保留 `AI-SR-plan.md` 与 `AI-SR-impl.md`。
3. **索引**：`/.aicontext/` 自动生成文档索引、依赖关系、哈希快照。

### 分层加载

按需加载文档，避免一次性加载全部：
- **always_read**: 每次必读（policies）
- **on_demand**: 按主题读取（数据库、配置）
- **by_scope**: 按范围读取（特定模块）

**详见**: doc/orchestration/routing.md

---

## 3. 提示词与清单

### 变更前检查

- [ ] 是否更新了`plan.md`？
- [ ] 是否明确了影响范围？
- [ ] 是否评估了回滚方案？
- [ ] 是否准备了测试用例？

### 实现中检查

- [ ] 代码改动最小化？
- [ ] 保持向后兼容？
- [ ] 测试是否覆盖？
- [ ] 是否有日志？

### 提交前检查

- [ ] 所有文档已更新？
- [ ] `make dev_check`通过？
- [ ] 生成了AI-SR？
- [ ] 清理了临时文件？

---

## 4. 命令速查

### 日常开发

```bash
# 初始化新模块
make ai_begin MODULE=<name>

# 开发检查（CI门禁）
make dev_check

# 生成文档索引
make docgen

# 自动维护
make ai_maintenance
```

### 编排与模块管理

```bash
# 校验agent.md
make agent_lint

# 校验模块注册表
make registry_check

# 校验文档路由
make doc_route_check

# 生成注册表草案
make registry_gen

# 生成模块实例文档
make module_doc_gen
```

### 数据库相关

```bash
# 生成DDL（半自动）
make db_gen_ddl TABLE=<table>

# 执行迁移（需确认）
make db_migrate

# 检查迁移
make migrate_check

# 回滚验证
make rollback_check PREV_REF=<tag>
```

**完整列表**: `make help`

---

## 5. 文档编写规范

### 禁止事项

❌ **禁止使用颜文字（Emoji）**
- 不要在文档中使用😀 🎉 ✨等
- 允许使用: ✅ ❌ ⚠️（状态标记）
- 允许使用: `# 井号注释`

❌ **禁止语言混用**
- 统一使用中文简体或英文
- 不要中英文混用在同一文档

❌ **禁止无结构**
- 必须使用标题层级
- 必须使用列表、表格组织信息
- 必须提供目录（长文档）

### 必须遵守

✅ **语言一致性**
- 同一文档统一语言
- 中文文档使用全角标点
- 英文文档使用半角标点

✅ **结构化**
- 使用Markdown标准语法
- 代码块指定语言
- 表格对齐

✅ **版本信息**
- 文档头部包含版本、日期、用途
- 重要变更记录在CHANGELOG.md

**详见**: docs/process/CONVENTIONS.md

---

## 6. 更多信息

### 核心规范

- **全局目标**: doc/policies/goals.md
- **安全规范**: doc/policies/safety.md
- **角色与门禁**: doc/policies/roles.md
- **路由规则**: doc/orchestration/routing.md

### 初始化指南

- **项目初始化**: doc/init/PROJECT_INIT_GUIDE.md
- **模块初始化**: doc/modules/MODULE_INIT_GUIDE.md
- **模块类型**: doc/modules/MODULE_TYPES.md
- **模块实例**: doc/modules/MODULE_INSTANCES.md（自动生成）

### 开发流程

- **代码审查**: doc/process/code_review.md（待创建）
- **测试准则**: doc/process/testing.md（待创建）
- **配置管理**: config/README.md
- **数据库规范**: db/engines/README.md

### 模板与工具

- **文档模板**: doc/modules/TEMPLATES/
- **Schema定义**: schemas/
- **工具脚本**: scripts/

---

**版本**: 1.0  
**最后更新**: 2025-11-07  
**维护**: 项目团队

---

> 📖 **编排系统请读本文档**: 本文档是根agent.md，定义了整个项目的工作规范和编排规则。
> 模块级的详细配置请参考各模块的agent.md。

