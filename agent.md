---
spec_version: "1.0"
agent_id: "repo"
role: "AI-TEMPLATE仓库根编排配置，指导AI高效开发"

policies:
  goals_ref: /doc/policies/goals.md
  safety_ref: /doc/policies/safety.md
  roles_ref: /doc/policies/roles.md

merge_strategy: "child_overrides_parent"

context_routes:
  always_read:
    - /doc/policies/goals.md
    - /doc/policies/safety.md
    - /README.md
  on_demand:
    - topic: "目录结构"
      paths:
        - /doc/architecture/directory.md
    - topic: "安全详情"
      paths:
        - /doc/policies/security_details.md
        - /doc/policies/quality_standards.md
    - topic: "数据库操作"
      paths:
        - /doc/db/DB_SPEC.yaml
        - /doc/db/SCHEMA_GUIDE.md
        - /db/engines/README.md
    - topic: "数据库变更"
      paths:
        - /doc/process/DB_CHANGE_GUIDE.md
        - /db/engines/postgres/schemas/tables/runs.yaml
        - /db/engines/postgres/docs/DB_SPEC.yaml
    - topic: "数据库变更详细"
      paths:
        - /doc/process/resources/db-create-table.md
        - /doc/process/resources/db-alter-table.md
        - /doc/process/resources/db-migration-script.md
        - /doc/process/resources/db-test-data.md
    - topic: "模块开发"
      paths:
        - /doc/modules/MODULE_INIT_GUIDE.md
        - /doc/modules/MODULE_TYPES.md
        - /doc/modules/MODULE_TYPE_CONTRACTS.yaml
        - /doc/modules/MODULE_INSTANCES.md
        - /doc/modules/example/README.md
    - topic: "模块开发详细"
      paths:
        - /doc/modules/resources/init-planning.md
        - /doc/modules/resources/init-directory.md
        - /doc/modules/resources/init-documents.md
        - /doc/modules/resources/init-registration.md
        - /doc/modules/resources/init-validation.md
        - /doc/modules/resources/init-database.md
        - /doc/modules/resources/init-testdata.md
        - /doc/modules/resources/init-context.md
    - topic: "项目初始化"
      paths:
        - /doc/init/PROJECT_INIT_GUIDE.md
    - topic: "配置管理"
      paths:
        - /config/README.md
        - /doc/process/CONFIG_GUIDE.md
    - topic: "命令参考"
      paths:
        - /doc/reference/commands.md
    - topic: "测试规范"
      paths:
        - /doc/process/testing.md
    - topic: "提交与PR"
      paths:
        - /doc/process/pr_workflow.md
    - topic: "文档路由使用"
      paths:
        - /doc/orchestration/routing.md
    - topic: "智能触发系统"
      paths:
        - /doc/orchestration/agent-triggers.yaml
        - /doc/orchestration/triggers-guide.md
    - topic: "Workdocs任务管理"
      paths:
        - /ai/workdocs/README.md
        - /doc/process/WORKDOCS_GUIDE.md
        - /doc/templates/workdoc-plan.md
        - /doc/templates/workdoc-context.md
        - /doc/templates/workdoc-tasks.md
    - topic: "Guardrail防护机制"
      paths:
        - /doc/process/GUARDRAIL_GUIDE.md
        - /doc/orchestration/agent-triggers.yaml
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

## 重要提醒

在开始任何任务前，模型必须：

1. **阅读文档格式规范**：见§3，遵守语言一致性和结构化要求
2. **遵循工作流程**：见§0，按照S0-S6步骤执行
3. **理解职责边界**：参见`doc/policies/roles.md`
4. **遵循文档路由**：根据任务类型按需加载相关文档

---

## 0. 工作流程（6步法）

**适用：所有任务**。模型每次执行任务都遵循下列步骤：

### S0 - 刷新上下文（分层加载）

按优先级分层读取：

- **Tier-0（必须）**：`/.aicontext/snapshot.json`、`/.aicontext/module_index.json`
- **Tier-1（强烈建议）**：`/doc/flows/dag.yaml`、相关`tools/*/contract.json`、目标模块`plan.md`/`README.md`
- **Tier-2（建议）**：`/doc/db/DB_SPEC.yaml`、`/doc/process/ENV_SPEC.yaml`、`/config/*.yaml`
- **Tier-3（按需）**：`TEST_PLAN.md`、`RUNBOOK.md`、`PROGRESS.md`、`BUGS.md`

> 若`snapshot_hash`变化，必须先运行`make docgen`生成最新索引。

### S1 - 任务建模

更新`/modules/<name>/plan.md`，明确：
- 范围与切片
- 接口影响
- 数据变更
- 风险评估
- 验证命令
- 回滚方案

> **边界**: `plan.md`=未来计划，`PROGRESS.md`=历史记录（不可混用）

**新增模块**: 运行`make ai_begin MODULE=<name>`或参考`doc/modules/MODULE_INIT_GUIDE.md`

### S2 - 方案预审（AI-SR: Plan）

生成`/ai/sessions/<date>_<name>/AI-SR-plan.md`：
- 意图说明
- 影响面分析
- DAG/契约/DB变更点
- 测试计划
- 回滚方案

### S3 - 实现与验证

- 仅修改计划范围内的代码
- 保持向后兼容
- 更新或新增测试（覆盖率≥80%）
- 运行`make dev_check`（CI门禁）

**测试要求**: 参见`doc/process/testing.md`

### S4 - 文档更新

同步更新：
- `CONTRACT.md` / `contract.json`
- `TEST_PLAN.md`
- `RUNBOOK.md`
- `PROGRESS.md`
- `CHANGELOG.md`
- `doc/flows/dag.yaml`（如涉及）

运行`make docgen`刷新索引。

### S5 - 自审与PR

生成`/ai/sessions/<date>_<name>/AI-SR-impl.md`，提交PR附上plan和AI-SR。

**PR流程**: 参见`doc/process/pr_workflow.md`

**CI门禁**: 
- `make dev_check`（必须通过）
- 测试覆盖率≥80%
- 高风险需`make rollback_check`

### S6 - 自动维护

运行`make ai_maintenance`确保仓库状态良好。

---

## 1. 文档路由与上下文管理

### 按需加载（Context Routes）

根agent.md的YAML Front Matter定义了文档路由规则：

- **always_read**: 每次必读的策略文档（goals.md, safety.md）
- **on_demand**: 按主题按需读取，包括10个主题：
  - 目录结构、数据库操作、模块开发、项目初始化、配置管理
  - 命令参考、测试规范、提交与PR、文档路由使用
- **by_scope**: 按工作范围读取（如特定模块）

**工作原理**: 
1. AI启动时自动读取`always_read`文档
2. 根据任务类型（如"数据库操作"），AI读取对应的`on_demand`文档
3. 进入特定模块工作时，读取`by_scope`配置的模块文档

**详见**: `doc/orchestration/routing.md`

### 记忆机制

1. **AI Ledger**: `/ai/LEDGER.md`记录每次任务
2. **Sessions**: `/ai/sessions/<date>_<mod>/`保留AI-SR
3. **索引**: `/.aicontext/`自动生成索引

---

## 2. 质量检查清单

### 变更前检查

- [ ] 是否更新了`plan.md`？
- [ ] 是否明确了影响范围？
- [ ] 是否评估了回滚方案？
- [ ] 是否准备了测试用例？

### 实现中检查

- [ ] 代码改动最小化？
- [ ] 保持向后兼容？
- [ ] 测试是否覆盖？
- [ ] 是否有适当的日志？

### 提交前检查

- [ ] 所有文档已更新？
- [ ] `make dev_check`通过？
- [ ] 生成了AI-SR？
- [ ] 清理了临时文件？

---

## 3. 文档编写规范

**语言一致性**: 同一文档统一语言（中文简体或英文，不混用）  
**结构化输出**: 使用标题、列表、表格、代码块组织内容  
**禁用颜文字**: 仅允许状态标记（✅ ❌ ⚠️ ⏳）  
**版本追踪**: 文档头部注明版本和日期，变更记录入CHANGELOG.md

**详见**: `doc/process/CONVENTIONS.md`

---

## 4. 核心参考文档

### 编排与策略
- **全局目标**: `doc/policies/goals.md`
- **安全规范**: `doc/policies/safety.md`
- **角色与门禁**: `doc/policies/roles.md`
- **文档路由**: `doc/orchestration/routing.md`
- **模块注册表**: `doc/orchestration/registry.yaml`

### 初始化指南
- **项目初始化**: `doc/init/PROJECT_INIT_GUIDE.md`
- **模块初始化**: `doc/modules/MODULE_INIT_GUIDE.md`
- **模块类型**: `doc/modules/MODULE_TYPES.md`
- **文档模板**: `doc/modules/TEMPLATES/`

### 架构与参考
- **目录结构**: `doc/architecture/directory.md`
- **命令速查**: `doc/reference/commands.md`
- **数据库规范**: `db/engines/README.md`
- **Schema定义**: `schemas/`

### 过程文档
- **测试准则**: `doc/process/testing.md`
- **提交与PR**: `doc/process/pr_workflow.md`
- **开发约定**: `doc/process/CONVENTIONS.md`
- **配置指南**: `doc/process/CONFIG_GUIDE.md`
- **环境规范**: `doc/process/ENV_SPEC.yaml`

---

**版本**: 2.0  
**最后更新**: 2025-11-07  
**维护**: 项目团队

---

> **📖 给AI编排系统**:  
> 本文档定义工作流程和文档路由规则。详细的规范、指南、命令参考请通过`context_routes`按需加载。  
> 模块级配置参见各模块的`modules/<entity>/agent.md`。
