# 模块初始化 - Phase 3: 生成文档

> **所属**: MODULE_INIT_GUIDE.md Phase 3  
> **用途**: Phase 3的详细执行指南  
> **目标**: 创建8个必备文档

---

## 目标

创建模块的8个必备文档：agent.md, README.md, plan.md, 和doc/下的6个文档

---

## 3.1 创建agent.md（关键）

**参考示例**：查看 `doc/modules/example/agent.md` 了解完整结构

从TEMPLATES/agent.md.template复制并调整YAML Front Matter：

```yaml
---
spec_version: "1.0"
agent_id: "modules.<entity>.v1"
role: "<entity>模块的业务逻辑Agent"
level: 1
module_type: "1_<entity>"

ownership:
  code_paths:
    include:
      - modules/<entity>/
      - tests/<entity>/
    exclude:
      - modules/<entity>/doc/CHANGELOG.md

io:
  inputs:
    - name: <input_name>
      schema_ref: schemas/<input>.yaml
      description: "<描述>"
  outputs:
    - name: <output_name>
      schema_ref: schemas/<output>.yaml
      description: "<描述>"

contracts:
  apis:
    - modules/<entity>/doc/CONTRACT.md

dependencies:
  upstream:
    - common.models.base
  downstream:
    - orchestrator.main

constraints:
  - "不得直接操作数据库，必须通过ORM"
  - "保持测试覆盖率≥80%"

tools_allowed:
  calls:
    - http.get
    - http.post
    - fs.read
    - db.query

quality_gates:
  required_tests:
    - unit
    - integration
  coverage_min: 0.80

context_routes:
  always_read:
    - /doc/policies/goals.md
    - /doc/policies/safety.md
  by_scope:
    - scope: "modules/<entity>"
      read:
        - /modules/<entity>/README.md
        - /modules/<entity>/doc/CONTRACT.md
---

# <Entity>模块Agent

## 1. 模块概述

### 1.1 功能描述
<简要描述模块的核心功能>

### 1.2 核心职责
- 职责1
- 职责2

### 1.3 不负责
- 非职责1（由XX模块负责）

## 2. 开发规范

### 2.1 代码规范
- 遵循PEP 8（Python）
- 函数名使用snake_case
- 类名使用PascalCase

### 2.2 测试要求
- 单元测试覆盖率 ≥ 80%
- 集成测试覆盖核心流程
- Contract测试验证接口契约

## 3. 质量检查清单

- [ ] 所有测试通过
- [ ] 覆盖率达标
- [ ] 文档已更新
- [ ] CHANGELOG已记录
```

**关键点**:
- `agent_id`: 格式为`modules.<entity>.v1`
- `ownership.code_paths`: 明确可改动的路径
- `io`: 定义输入输出schema
- `dependencies`: 明确上下游依赖
- `context_routes`: 配置文档路由

---

## 3.2 创建README.md

从TEMPLATES/README.md.template复制并填写：

**必需章节**:
1. 模块概述
2. 功能特性
3. **目录结构**（关键！必须有）
4. 快速开始
5. 文档索引

**示例**:

```markdown
# <Entity>模块

## 概述
<模块功能描述>

## 目录结构

\`\`\`
modules/<entity>/
├── agent.md              # Agent配置
├── README.md             # 本文档
├── plan.md               # 实施计划
├── doc/                  # 模块文档
│   ├── CONTRACT.md      # 接口契约
│   ├── CHANGELOG.md     # 变更日志
│   ├── RUNBOOK.md       # 运维手册
│   ├── BUGS.md          # 已知问题
│   ├── PROGRESS.md      # 进度追踪
│   └── TEST_PLAN.md     # 测试计划
├── core/                 # 核心逻辑
│   └── __init__.py
└── api/                  # HTTP接口（可选）
    └── routes.py
\`\`\`

## 文档索引

- [接口契约](doc/CONTRACT.md)
- [变更日志](doc/CHANGELOG.md)
- [运维手册](doc/RUNBOOK.md)
```

---

## 3.3 创建plan.md

从TEMPLATES/plan.md.template复制：

```markdown
# <Entity>模块实施计划

## Phase 1: 基础实现

### 任务清单
- [ ] 任务1
- [ ] 任务2

## Phase 2: 功能完善

### 任务清单
- [ ] 任务3
- [ ] 任务4
```

---

## 3.4 创建doc/下的6个文档

从`doc/modules/TEMPLATES/`复制模板：

```bash
MODULE=<entity>

cp doc/modules/TEMPLATES/CONTRACT.md.template modules/$MODULE/doc/CONTRACT.md
cp doc/modules/TEMPLATES/CHANGELOG.md.template modules/$MODULE/doc/CHANGELOG.md
cp doc/modules/TEMPLATES/RUNBOOK.md.template modules/$MODULE/doc/RUNBOOK.md
cp doc/modules/TEMPLATES/BUGS.md.template modules/$MODULE/doc/BUGS.md
cp doc/modules/TEMPLATES/PROGRESS.md.template modules/$MODULE/doc/PROGRESS.md
cp doc/modules/TEMPLATES/TEST_PLAN.md.template modules/$MODULE/doc/TEST_PLAN.md
```

**CONTRACT.md**（最重要）:
- 定义所有对外接口
- 区分API接口和前端组件
- 明确输入输出schema
- 参考：`doc/modules/example/doc/CONTRACT.md`

**其他文档**:
- CHANGELOG.md: 记录每次变更
- RUNBOOK.md: 部署和运维说明
- BUGS.md: 已知问题列表
- PROGRESS.md: 开发进度
- TEST_PLAN.md: 测试策略和用例

---

## AI执行规范

**必须做**:
- ✅ 从TEMPLATES/复制模板，不要从零编写
- ✅ 填写agent.md的所有必需字段
- ✅ README.md必须包含"目录结构"章节
- ✅ CONTRACT.md必须区分API和前端组件

**不要做**:
- ❌ 不要跳过任何一个文档
- ❌ 不要留空文档（至少填写模板内容）
- ❌ 不要忘记替换`<entity>`占位符

---

## 常见问题

### Q: agent.md的YAML字段太多了，哪些是必需的？
**A**: 必需字段：
- spec_version, agent_id, role, level, module_type
- ownership.code_paths
- context_routes

### Q: CONTRACT.md如何区分API和前端组件？
**A**: 分两个章节：
- § API接口契约（如有api/子目录）
- § 前端组件契约（如有frontend/子目录）

参考：`doc/modules/example/doc/CONTRACT.md`

### Q: CHANGELOG.md需要立即填写吗？
**A**: 不需要。创建后保留模板内容即可，等有变更时再记录。

---

## 下一步

完成文档创建后，进入 → [Phase 4: 注册模块](init-registration.md)

