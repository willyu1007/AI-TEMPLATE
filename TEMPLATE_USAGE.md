# 模板使用指南

## 目标
提供详细的使用说明，帮助用户基于 Agent Repo 模板快速创建新项目，并完成必要的定制配置。

## 适用场景
- 基于模板创建新项目
- 需要了解哪些文件必须修改
- 需要定制技术栈或数据库
- 需要了解模板的定制选项

## 前置条件
- 已克隆或下载 Agent Repo 模板
- 了解项目基本需求（技术栈、数据库等）

---

## 目录

1. [快速开始](#快速开始)
2. [必须修改的文件](#必须修改的文件)
3. [可选配置](#可选配置)
4. [定制指南](#定制指南)
5. [检查清单](#检查清单)

---

## 快速开始

### 方式 1: 使用模板创建新项目（GitHub）

```bash
# 1. 点击 "Use this template" 按钮（GitHub）
# 2. 克隆你的新仓库
git clone https://github.com/your-username/your-project.git
cd your-project

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化
make docgen
make update_baselines
make dev_check
```

### 方式 2: 克隆并修改

```bash
# 1. 克隆模板
git clone https://github.com/your-org/agent-repo-template.git my-project
cd my-project

# 2. 删除原有 git 历史
rm -rf .git
git init

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化
make docgen
make update_baselines

# 5. 第一次提交
git add .
git commit -m "chore: init project from template"
```

---

## 必须修改的文件

### 第一优先级（立即修改）

#### 1. `README.md`
```
当前：通用模板说明
需要：替换为你的项目说明

修改内容：
- 项目名称
- 项目描述
- 技术栈
- 维护者信息
```

#### 2. `agent.md`（Phase 3将添加YAML Front Matter）
```
当前：模板通用Agent指南
需要：添加YAML Front Matter和项目特定配置

修改内容（Phase 3）：
- spec_version, agent_id, role
- policies引用
- context_routes（文档路由）
- merge_strategy
```

#### 3. `doc/orchestration/registry.yaml`
```
当前：仅包含example模块
需要：注册你的项目模块

修改内容：
- 添加项目的模块类型
- 添加模块实例
- 定义依赖关系
- 设置责任人和标签

使用命令：
  make registry_gen  # 生成草案
  vi doc/orchestration/registry.yaml  # 审核并补充
  make registry_check  # 验证
```

#### 4. `.aicontext/project_onepager.md`
```
当前：目标：以最小成本，用大模型提升开发效率...
需要：你的项目一页综述

修改内容：
- 项目目标
- 成功指标
- 当前日期
```

#### 5. `doc/project/PRD_ONEPAGER.md`
```
当前：空模板
需要：填写你的项目 PRD

必填项：
- 问题/目标
- 成功指标
- 范围（包含/不包含）
- 约束（性能/安全/合规）
- 里程碑
```

#### 4. `doc/project/SYSTEM_BOUNDARY.md`
```
当前：空模板
需要：定义系统边界

必填项：
- 外部依赖
- 入口/出口
- 非功能需求
```

#### 5. `doc/process/ENV_SPEC.yaml`
```
当前：vue3, fastapi, postgres...
需要：你的实际技术栈

修改：
frontend: { framework: ?, bundler: ?, language: ? }
backend: { language: ?, web: ?, orm: ? }
infra: { db: ?, cache: ?, search: ? }
```

#### 6. `config/*.yaml`
```
修改所有配置文件以匹配你的项目：
- config/schema.yaml    # 配置结构定义
- config/defaults.yaml  # 默认值
- config/dev.yaml       # 开发环境
```

---

### 🟡 第二优先级（开发前修改）

#### 7. `db/engines/postgres/doc/DB_SPEC.yaml`
```
当前：示例 runs 表
需要：你的数据库结构

根据项目需求定义：
- 表结构
- 索引
- PII 字段标记
```

#### 8. `doc/flows/dag.yaml`
```
当前：示例 web.frontend -> api.codegen
需要：你的实际 DAG 拓扑

定义：
- 系统节点
- 依赖关系
- SLA 要求
```

#### 9. `tools/codegen/contract.json`
```
当前：示例 codegen 工具契约
需要：你的工具/API 契约

选项：
A. 修改现有契约
B. 删除并创建新的
C. 添加更多工具契约
```

---

### 🟢 第三优先级（按需修改）

#### 10. `modules/example/`
```
当前：示例模块（保留作为参考）
需要：你的实际模块

选项：
A. 保留作为参考（推荐新项目）
B. 删除并创建新模块：
   rm -rf modules/example
   make ai_begin MODULE=your_module
```

#### 11. `docker-compose.yml`
```
当前：postgres + redis
需要：你需要的服务

根据需求调整服务
```

#### 12. 删除模板相关文件
```
# 可选：删除这些文件（如果不需要）
rm TEMPLATE_USAGE.md  # 本文件
rm doc/project/IMPLEMENTATION_SUMMARY.md  # 模板实施记录
rm CHANGES_SUMMARY.md  # 模板变更记录（如果还在根目录）
```

---

## 可选配置

### 技术栈定制

#### Python 项目
```
# 1. 修改 requirements.txt
vim requirements.txt

# 2. 自动检测依赖
make deps_check

# 3. 更新 ENV_SPEC.yaml
backend: { language: python3.11, web: fastapi, ... }
```

#### Go 项目
```
# 1. 初始化 go.mod
go mod init github.com/your-org/your-project

# 2. 更新 ENV_SPEC.yaml
backend: { language: go1.21, ... }

# 3. 添加 Go 测试示例
# 参考 agent.md §6.3 Go 测试
```

#### Vue/TypeScript 项目
```
# 1. 创建 package.json
npm init -y

# 2. 安装依赖
npm install vue@3 vite typescript

# 3. 更新 ENV_SPEC.yaml
frontend: { framework: vue3, bundler: vite, language: ts }
```

### 数据库定制

#### PostgreSQL（默认）
```
# db/engines/postgres/doc/DB_SPEC.yaml
defaults:
  primary: postgresql
  version: "16"
  vector: true  # 如需 pgvector
```

#### MySQL
```
# db/engines/mysql/doc/DB_SPEC.yaml（需创建）
defaults:
  primary: mysql
  version: "8.0"

# docker-compose.yml
db:
  image: mysql:8.0
  environment:
    MYSQL_ROOT_PASSWORD: dev
    MYSQL_DATABASE: app
```

#### MongoDB
```
# db/engines/mongo/doc/DB_SPEC.yaml（需创建）
defaults:
  primary: mongodb
  version: "7.0"

# docker-compose.yml
db:
  image: mongo:7.0
  ports: ["27017:27017"]
```

---

## 🎨 定制指南

### 调整文档结构

#### 添加新的文档类型
```
# 示例：添加 API 文档目录
mkdir -p doc/api
echo "# API 文档" > doc/api/README.md

# 更新 agent.md §1 目录规范（可选）
```

#### 调整模块文档要求
```
# 如果 8 个文档太多，可以简化
# 修改 scripts/consistency_check.py

# 最小要求（建议至少保留）：
- README.md
- plan.md
- CONTRACT.md
- TEST_PLAN.md
- CHANGELOG.md
```

### 调整自动化门禁

#### 放宽覆盖率要求
```
# agent.md §6 测试准则
当前：核心模块 ≥80%

# 修改为你的标准（如 70%）
# 并更新 Makefile 或 CI 配置
pytest --cov --cov-fail-under=70
```

#### 禁用某些检查
```
# Makefile - 修改 dev_check 目标
dev_check: docgen dag_check consistency_check
    # 移除了 contract_compat_check (如果不需要)
```

### 添加新的检查

#### 示例：添加代码风格检查
```
# 1. 添加脚本
cat > scripts/style_check.py <<'EOF'
#!/usr/bin/env python3
import sys
# ... 你的检查逻辑 ...
EOF

# 2. 更新 Makefile
# 在 dev_check 中添加：
make style_check
```

---

## Phase 1-2新增文件（无需修改）

以下文件在Phase 1-2中已创建，**无需修改**（除非定制）：

### Schema与脚本（Phase 1）
- ✅ `schemas/agent.schema.yaml` - agent.md的Schema定义
- ✅ `schemas/README.md` - Schema说明
- ✅ `scripts/agent_lint.py` - Agent校验脚本
- ✅ `scripts/registry_check.py` - 注册表校验脚本
- ✅ `scripts/doc_route_check.py` - 文档路由校验脚本
- ✅ `scripts/registry_gen.py` - 注册表生成脚本
- ✅ `scripts/module_doc_gen.py` - 模块文档生成脚本

### 目录结构（Phase 2）
- ✅ `doc/orchestration/routing.md` - 路由规则说明
- ✅ `doc/policies/goals.md` - 全局目标
- ✅ `doc/policies/safety.md` - 安全规范
- ✅ `doc/indexes/context-rules.md` - 上下文索引规则
- ✅ `doc/init/PROJECT_INIT_GUIDE.md` - 项目初始化指南
- ✅ `doc/modules/MODULE_INIT_GUIDE.md` - 模块初始化指南
- ✅ `doc/modules/MODULE_TYPES.md` - 模块类型说明
- ✅ `doc/modules/TEMPLATES/` - 文档模板（6个）
- ✅ `db/engines/postgres/` - PostgreSQL目录
- ✅ `db/engines/redis/` - Redis目录

### 自动生成文件（Phase 2）
- 🔄 `doc/orchestration/registry.yaml` - 模块注册表（需审核）
- 🔄 `doc/modules/MODULE_INSTANCES.md` - 模块实例（自动生成）

---

## Phase 10新增特性（智能功能）

Phase 10引入了4个智能特性，提升AI工作效率和安全性。这些功能开箱即用，无需额外配置。

### 1. 智能触发系统

**功能**: 根据文件路径和操作意图，自动推荐相关文档

**相关文件**:
- ✅ `doc/orchestration/agent-triggers.yaml` - 13个触发规则定义
- ✅ `scripts/agent_trigger.py` - 触发器引擎（536行）
- ✅ `doc/orchestration/triggers-guide.md` - 使用指南

**使用方法**:
```bash
# 测试触发器
python scripts/agent_trigger.py --prompt "创建新模块" --dry-run

# 查看所有触发规则
cat doc/orchestration/agent-triggers.yaml
```

**定制方法**:
```yaml
# 在 agent-triggers.yaml 中添加新规则
triggers:
  custom-operation:
    priority: high
    file_triggers:
      path_patterns:
        - "your/path/**"
    load_documents:
      - path: /doc/your-guide.md
        priority: critical
```

---

### 2. 渐进式披露

**功能**: 大文档拆分为主文件+resources，按需加载，节省70% Token

**相关文件**:
- ✅ `doc/modules/MODULE_INIT_GUIDE.md` - 主文件（285行）
  - `doc/modules/resources/init-*.md` - 8个resources（详细步骤）
- ✅ `doc/process/DB_CHANGE_GUIDE.md` - 主文件（273行）
  - `doc/process/resources/db-*.md` - 4个resources（详细指南）
- ✅ `scripts/resources_check.py` - Resources完整性检查

**使用方法**:
```bash
# 检查resources完整性
make resources_check

# 查看主文件（快速概览）
cat doc/modules/MODULE_INIT_GUIDE.md

# 按需查看详细步骤
cat doc/modules/resources/init-planning.md
```

**定制方法**:
- 如需拆分其他大文档（>500行），参考MODULE_INIT_GUIDE.md的结构
- 主文件包含：快速概览、Resources索引表、常见问题
- Resources文件：每个≤250行，聚焦单一主题

---

### 3. Dev Docs机制

**功能**: 三层上下文管理，2-5分钟快速恢复工作状态

**相关文件**:
- ✅ `ai/workdocs/` - 工作文档目录
  - `active/` - 活跃任务
  - `archive/` - 已完成任务
- ✅ `doc/templates/workdoc-*.md` - 3个模板（plan/context/tasks）
- ✅ `scripts/workdoc_create.sh` - 创建工作文档
- ✅ `scripts/workdoc_archive.sh` - 归档工作文档
- ✅ `doc/process/WORKDOCS_GUIDE.md` - 详细指南（653行）

**使用方法**:
```bash
# 创建新任务的work doc
make workdoc_create TASK=feature-auth

# 查看活跃任务
make workdoc_list

# 更新任务进度（自动从git log提取）
make workdoc_update

# 归档完成的任务
make workdoc_archive TASK=feature-auth
```

**最佳实践**:
- 每个任务创建一个work doc
- 及时更新SESSION PROGRESS（关键！）
- 记录错误和决策（避免重复踩坑）
- 完成后归档（保留历史记录）

---

### 4. Guardrail防护

**功能**: 事前阻止破坏性操作，100%关键领域覆盖

**相关文件**:
- ✅ `doc/orchestration/agent-triggers.yaml` - Guardrail规则定义
  - 4个Block规则（数据库变更、契约变更、生产配置、安全操作）
  - 3个Warn规则（根agent.md变更、关键文件删除、依赖版本升级）
  - 6个Suggest规则（文档更新、测试覆盖、性能优化等）
- ✅ `scripts/guardrail_stats.py` - Guardrail统计工具
- ✅ `doc/process/GUARDRAIL_GUIDE.md` - 详细指南（782行）

**使用方法**:
```bash
# 查看Guardrail覆盖率
make guardrail_coverage

# 查看Guardrail统计
make guardrail_stats

# 测试Guardrail（会被阻止）
# 修改CONTRACT.md但未运行 contract_compat_check
```

**Guardrail规则示例**:
```yaml
contract-changes:
  priority: critical
  enforcement: block  # 阻止操作
  file_triggers:
    path_patterns:
      - "**/CONTRACT.md"
  check_enforcement:
    required_command: "make contract_compat_check"
    block_if_failed: true
```

**豁免机制**:
```yaml
# 紧急情况下使用skip_conditions
skip_conditions:
  - file_contains: "# SKIP_CONTRACT_CHECK"
  - env_var: "SKIP_CONTRACT_GUARD=true"
```

---

### Phase 10验证清单

```markdown
- [ ] make agent_trigger_test 触发器测试通过
- [ ] make resources_check resources完整性检查通过
- [ ] make workdoc_create TASK=test 可以创建work doc
- [ ] make guardrail_coverage 显示100%覆盖
- [ ] make dev_check 包含16个检查（新增resources_check）
- [ ] doc/orchestration/agent-triggers.yaml 包含13个规则
- [ ] agent.md context_routes 包含49个路由
```

---

## 检查清单

### 项目初始化清单

```markdown
- [ ] README.md 已更新为项目说明
- [ ] .aicontext/project_onepager.md 已填写
- [ ] doc/project/PRD_ONEPAGER.md 已完成
- [ ] doc/project/SYSTEM_BOUNDARY.md 已定义
- [ ] doc/process/ENV_SPEC.yaml 匹配技术栈
- [ ] config/*.yaml 已配置
- [ ] db/engines/postgres/doc/DB_SPEC.yaml 已定义
- [ ] doc/flows/flows/*.yaml 已更新
- [ ] tools/ 下的契约已定义或删除
- [ ] modules/example 已删除或保留
- [ ] docker-compose.yml 已调整
- [ ] requirements.txt 已更新（Python）
- [ ] package.json 已创建（Node.js）
- [ ] go.mod 已创建（Go）
- [ ] .gitignore 已检查
- [ ] LICENSE 已更新（作者/年份）
```

### 首次运行清单

```markdown
- [ ] make docgen 成功
- [ ] make update_baselines 成功
- [ ] make dev_check 全部通过
- [ ] make ai_begin MODULE=test 可以创建模块
- [ ] tests/ 下有测试示例
- [ ] CI 配置已创建（如使用）
```

### 团队协作清单

```markdown
- [ ] 团队成员已阅读 agent.md
- [ ] 团队成员已阅读 QUICK_START.md
- [ ] 明确了 PR 规则（agent.md §10.5）
- [ ] 明确了代码审查流程（agent.md §11）
- [ ] 配置了 CI/CD
- [ ] 设置了代码仓库保护规则
```

---

## 常见问题

### Q1: 我只用 Python，需要保留 Go/Vue 的配置吗？
**A**: 不需要。删除 `config/loader/go_loader.go` 和 `ts_loader.ts`，只保留 `python_loader.py`。同时更新 `ENV_SPEC.yaml`。

### Q2: 文档太多了，可以简化吗？
**A**: 可以。最小保留：
- agent.md（核心指南）
- README.md
- QUICK_START.md
- modules/*/README.md
- modules/*/plan.md
- modules/*/CONTRACT.md

### Q3: 我不需要 DAG，可以删除吗？
**A**: 可以。删除 `doc/flows/dag.yaml`，并在 `Makefile` 的 `dev_check` 中移除 `dag_check`。

### Q4: 如何添加多语言支持？
**A**: 
1. 在 `doc/process/ENV_SPEC.yaml` 中添加语言配置。
2. 在 `agent.md` §6 测试准则中参考示例添加测试指导。
3. 更新 `scripts/deps_manager.py` 支持新语言依赖检测。

### Q5: 模板更新了，如何合并到已有项目？
**A**:
```
# 1. 添加模板作为远程仓库
git remote add template https://github.com/your-org/agent-repo-template.git

# 2. 拉取模板更新
git fetch template

# 3. 选择性合并
git cherry-pick <commit-hash>  # 选择特定更新

# 或使用 diff 查看变更
git diff template/main -- agent.md
```

---

## 下一步

1. ✅ 完成检查清单
2. 📖 阅读 [agent.md](agent.md) 了解完整工作流程
3. 🚀 创建第一个模块：`make ai_begin MODULE=my_feature`
4. 🧪 编写测试并运行：`make dev_check`
5. 📝 提交第一个 PR（遵循 PR 规则）

---

## 获取帮助

- **文档**：查看 `agent.md` 和 `QUICK_START.md`
- **示例**：参考 `modules/example/`
- **问题**：提交 Issue
- **讨论**：团队内部讨论或提 PR

---

**祝使用愉快！** 🎉

