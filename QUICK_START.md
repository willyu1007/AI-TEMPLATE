# 快速开始指南

## 目标
帮助新用户快速上手 Agent Repo 模板，在5分钟内完成项目初始化和第一个模块的创建。

## 适用场景
- 首次使用 Agent Repo 模板
- 需要快速了解核心功能
- 准备开始第一个开发任务

## 前置条件
- 已安装 Python 3.7+ 或 Node.js 16+
- 已克隆或下载 Agent Repo 模板
- 已阅读 README.md 了解项目概述

---

## 5 分钟快速启动

### 安装依赖
```
# Python 依赖（推荐）
pip install -r requirements.txt

# 或者只安装核心依赖
pip install pyyaml

# 自动检测并补全依赖（可选）
make deps_check
```

### 初始化项目
```
# 生成文档索引
make docgen

# 运行完整检查
make dev_check

# 初始化契约基线
make update_baselines
```

### 创建第一个模块
```
# 初始化模块（自动生成所有文档和测试）
make ai_begin MODULE=my_feature

# 查看生成的文件
ls -la modules/my_feature/
ls -la tests/my_feature/
```

### 开发流程
```
# 1. 编辑计划
vim modules/my_feature/plan.md

# 2. 实现功能
# ... 编写代码 ...

# 3. 运行检查
make dev_check

# 4. 提交前最后验证
make rollback_check PREV_REF=main
```

---

## 智能特性快速体验

### 智能触发器测试

```bash
# 测试智能触发器（自动推荐文档）
python scripts/agent_trigger.py --prompt "创建新模块" --dry-run

# 预期输出：
# ✅ 匹配规则: module-development
# 🔴 MODULE_INIT_GUIDE.md (主文件)
# 🟠 MODULE_TYPES.md
# 🟠 MODULE_TYPE_CONTRACTS.yaml
```

### Work Docs（工作文档）快速使用

```bash
# 创建工作文档（用于任务追踪）
make workdoc_create TASK=my-feature

# 查看活跃任务
make workdoc_list

# 更新进度（自动从git log提取）
make workdoc_update

# 归档完成的任务
make workdoc_archive TASK=my-feature
```

### Guardrail防护测试

```bash
# 测试Guardrail（防止破坏性操作）
# 尝试修改CONTRACT.md但未运行兼容性检查
# Guardrail会自动阻止并提示先运行 make contract_compat_check

# 查看Guardrail统计
make guardrail_stats

# 查看Guardrail覆盖率
make guardrail_coverage
```

### Resources检查

```bash
# 检查渐进式披露的resources完整性
make resources_check

# 预期输出：
# ✅ MODULE_INIT_GUIDE: 主文件285行 + 8个resources
# ✅ DB_CHANGE_GUIDE: 主文件273行 + 4个resources
# ✅ 所有resources文件存在且有效
```

---

## 常用命令速查

### 开发检查
```
make dev_check              # 完整检查（CI 门禁）
make quick_check            # 快速检查（跳过慢速检查）
make dag_check              # 仅检查 DAG
make consistency_check      # 仅检查一致性
```

### 模块管理
```
make ai_begin MODULE=<name>     # 初始化新模块
make tests_scaffold MODULE=<name>  # 生成测试脚手架
```

### 契约管理
```
make contract_compat_check  # 检查契约兼容性
make update_baselines       # 更新契约基线
```

### 配置与迁移
```
make runtime_config_check   # 检查配置
make migrate_check          # 检查迁移脚本
```

### 文档与索引
```
make docgen                 # 生成/更新文档索引
make deps_check             # 检查并自动补全依赖
```

### 编排与模块管理（新增）
```
make agent_lint             # 校验agent.md YAML前言
make registry_check         # 校验模块注册表
make doc_route_check        # 校验文档路由
make registry_gen           # 生成registry.yaml草案
make module_doc_gen         # 生成模块实例文档
```

### 回滚验证
```
make rollback_check PREV_REF=v1.0.0  # 验证可回滚到指定版本
```

## AI Agent 使用流程

### 作为 AI Agent，每次任务遵循：

#### S0 - 刷新上下文（分层加载）
```
# Tier-0（必须）
cat .aicontext/snapshot.json
cat .aicontext/module_index.json

# Tier-1（强烈建议）
cat doc/flows/dag.yaml
cat modules/<target>/plan.md
cat modules/<target>/README.md

# Tier-2（建议）
cat db/engines/postgres/docs/DB_SPEC.yaml
cat doc/process/ENV_SPEC.yaml

# Tier-3（按需）
cat modules/<target>/TEST_PLAN.md
```

#### S1 - 任务建模
```
# 更新计划
vim modules/<target>/plan.md

# 明确：
# - 目标和范围
# - 接口/DB 影响
# - 测试清单
# - 验证命令
# - 回滚计划
```

#### S2 - 方案预审
```
# 生成自审文档
mkdir -p ai/sessions/$(date +%Y%m%d)_<name>
vim ai/sessions/$(date +%Y%m%d)_<name>/AI-SR-plan.md

# 内容包括：
# - 意图
# - 影响面
# - DAG/契约/DB 变更点
# - 测试点
# - 回滚
```

#### S3 - 实现与验证
```
# 实现功能
# ... 编写代码 ...

# 更新测试
# ... 编写测试 ...

# 运行验证
make dev_check
```

#### S4 - 文档与索引更新
```
# 同步更新文档
vim modules/<target>/CONTRACT.md
vim modules/<target>/TEST_PLAN.md
vim modules/<target>/RUNBOOK.md
vim modules/<target>/PROGRESS.md
vim modules/<target>/CHANGELOG.md

# 如涉及 DAG/契约/配置
vim doc/flows/dag.yaml
vim tools/*/contract.json
vim config/*.yaml
vim doc/process/CONFIG_GUIDE.md

# 刷新索引
make docgen
```

#### S5 - 自审与 PR
```
# 生成实施自审
vim ai/sessions/$(date +%Y%m%d)_<name>/AI-SR-impl.md

# 最后检查
make dev_check

# 回滚验证（高风险变更）
make rollback_check PREV_REF=<previous-tag>

# 创建 PR（附上 plan 和 AI-SR）
```

## 目录结构速查

```text
.
├── .aicontext/              # AI 上下文索引
│   ├── index.json           # 文档索引（含 summary/keywords/deps/hash）
│   ├── snapshot.json        # 快照哈希
│   ├── module_index.json    # 模块索引
│   ├── project_onepager.md  # 项目概述
│   ├── style_guide.md       # 代码风格
│   └── banned_patterns.md   # 禁用模式
├── .contracts_baseline/     # 契约基线
├── .github/
│   └── pull_request_template.md
├── ai/
│   ├── LEDGER.md            # AI 任务清册
│   └── sessions/            # AI 自审记录
├── config/                  # 配置文件
│   ├── schema.yaml          # 配置 schema
│   ├── defaults.yaml        # 默认配置
│   ├── dev.yaml             # 开发环境
│   ├── staging.yaml         # 预发布环境
│   ├── prod.yaml            # 生产环境
│   └── loader/              # 配置加载器示例
├── db/                      # 数据库层（Phase 2新增）
│   └── engines/             # 数据库引擎
│       ├── postgres/        # PostgreSQL
│       └── redis/           # Redis
├── doc/                     # 文档层（Phase 2新增）
│   ├── orchestration/       # 编排配置
│   │   ├── registry.yaml    # 模块注册表
│   │   └── routing.md       # 路由规则
│   ├── policies/            # 全局策略
│   │   ├── goals.md         # 全局目标
│   │   └── safety.md        # 安全规范
│   ├── indexes/             # 索引规则
│   │   └── context-rules.md # 上下文索引规则
│   ├── init/                # 初始化指南
│   │   └── PROJECT_INIT_GUIDE.md
│   └── modules/             # 模块相关
│       ├── MODULE_TYPES.md  # 模块类型
│       ├── MODULE_INSTANCES.md  # 模块实例（自动生成）
│       ├── MODULE_INIT_GUIDE.md # 模块初始化
│       └── TEMPLATES/       # 文档模板
├── doc/                     # 项目文档（已统一）
│   ├── project/             # 项目文档
│   ├── process/             # 流程文档
│   ├── modules/             # 模块文档
│   ├── flows/               # 流程图和DAG配置
│   ├── orchestration/       # 编排配置
│   ├── db/                  # 数据库重定向
│   └── ux/                  # UX 文档
├── db/                      # 数据库治理（Phase 5统一）
│   └── engines/
│       └── postgres/
│           ├── migrations/  # 迁移脚本
│           ├── schemas/     # 表结构YAML
│           └── docs/        # DB文档
├── modules/                 # 业务模块
│   └── <module>/
│       ├── agent.md         # Agent配置（Phase 4添加YAML）
│       ├── README.md        # 模块概述
│       ├── plan.md          # 任务计划
│       ├── doc/             # 模块文档（Phase 4新增）
│       │   ├── CONTRACT.md      # 接口契约
│       │   ├── CHANGELOG.md     # 变更日志
│       │   ├── RUNBOOK.md       # 运维手册
│       │   ├── BUGS.md          # 缺陷管理
│       │   ├── PROGRESS.md      # 进度跟踪
│       │   └── TEST_PLAN.md     # 测试计划
│       ├── core/            # 核心逻辑（必需）
│       ├── api/             # API层（可选）
│       ├── frontend/        # 前端组件（可选）
│       └── models/          # 数据模型（可选）
├── schemas/                 # Schema定义（Phase 1新增）
│   ├── agent.schema.yaml    # agent.md的Schema
│   └── README.md            # Schema说明
├── scripts/                 # 工具脚本
│   ├── docgen.py            # 生成文档索引
│   ├── dag_check.py         # DAG 校验
│   ├── contract_compat_check.py  # 契约兼容性
│   ├── consistency_check.py # 一致性检查
│   ├── rollback_check.sh    # 回滚验证
│   ├── runtime_config_check.py   # 配置校验
│   ├── test_scaffold.py     # 测试脚手架
│   ├── migrate_check.py     # 迁移脚本检查
│   ├── ai_begin.sh          # 模块初始化
│   ├── agent_lint.py        # Agent校验（Phase 1）
│   ├── registry_check.py    # 注册表校验（Phase 1）
│   ├── doc_route_check.py   # 文档路由校验（Phase 1）
│   ├── registry_gen.py      # 生成注册表（Phase 1）
│   ├── module_doc_gen.py    # 生成模块文档（Phase 1）
│   └── validate.sh          # 聚合验证
├── tests/                   # 测试
├── tools/                   # 工具/服务契约
│   └── codegen/
│       └── contract.json
├── agent.md                 # AI Agent 工作指南（Phase 3添加YAML）
├── Makefile                 # 命令入口
├── requirements.txt         # Python 依赖
└── README.md                # 项目说明
```

## 最佳实践

### 1. 始终保持索引最新
```
# 每次修改文档后
make docgen
```

### 2. 提交前运行完整检查
```
make dev_check
```

### 3. 契约变更需验证兼容性
```
make contract_compat_check
# 通过后更新基线
make update_baselines
```

### 4. 高风险变更需回滚验证
```
make rollback_check PREV_REF=v1.0.0
```

### 5. 遵循文档边界
- `plan.md` = 未来计划
- `PROGRESS.md` = 历史记录

## 故障排查

### 问题：`make dev_check` 失败

#### 1. snapshot_hash 不一致
```
# 解决：重新生成索引
make docgen
```

#### 2. 模块文档缺失
```
# 解决：补齐文档或使用模板初始化
make ai_begin MODULE=<module>
```

#### 3. DAG 有环
```
# 解决：检查 doc/flows/dag.yaml，移除循环依赖
vim doc/flows/dag.yaml
make dag_check
```

#### 4. 契约不兼容
```
# 解决：修复契约或创建新版本
vim tools/*/contract.json
make contract_compat_check
```

### 问题：Python 脚本无法执行

```bash
# 检查依赖
pip install pyyaml

# 检查 Python 版本（需要 3.7+）
python --version
```

### 问题：Bash 脚本权限问题

```bash
# 添加执行权限
chmod +x scripts/*.sh
```

## 更多信息

### 核心文档
- **详细指南**：`agent.md`
- **改进方案**：`Agent-Repo-QA-Mapping.md`
- **实施摘要**：`doc/project/IMPLEMENTATION_SUMMARY.md`
- **示例模块**：`doc/modules/example/` - 参考文档

### 新增文档（Phase 1-2）
- **全局目标**：`doc/policies/goals.md`
- **安全规范**：`doc/policies/safety.md`
- **路由规则**：`doc/orchestration/routing.md`
- **模块注册表**：`doc/orchestration/registry.yaml`
- **项目初始化**：`doc/init/PROJECT_INIT_GUIDE.md`
- **模块初始化**：`doc/modules/MODULE_INIT_GUIDE.md`
- **模块类型**：`doc/modules/MODULE_TYPES.md`
- **模块实例**：`doc/modules/MODULE_INSTANCES.md`（自动生成）

## 提示

1. 使用 `make help` 查看所有可用命令。
2. 参考 `modules/example/` 了解文档最佳实践。
3. 使用 `make quick_check` 进行快速验证。
4. 生产部署前务必运行 `make rollback_check`。
5. 使用 `make deps_check` 自动检测并补全项目依赖。

## 依赖管理说明

### Python 项目
```
# 自动检测 imports 并补全 requirements.txt
make deps_check

# 或直接运行脚本
python scripts/deps_manager.py
```

**支持自动检测的包**：
- Web 框架：FastAPI, Flask, Django
- 数据库：SQLAlchemy, psycopg2, pymongo, redis
- 测试：pytest, pytest-cov, pytest-asyncio
- 工具：pyyaml, requests, httpx, python-dotenv
- 任务队列：celery
- AI/ML：openai, anthropic

### 其他技术栈
- **Node.js/Vue**: 使用 `package.json` 管理，运行 `npm install`
- **Go**: 使用 `go.mod` 管理，运行 `go mod tidy`
- **C/C++**: 使用 CMakeLists.txt / vcpkg / conan
- **C#**: 使用 `*.csproj` 管理，运行 `dotnet restore`

---

**祝开发愉快！** 🎉

