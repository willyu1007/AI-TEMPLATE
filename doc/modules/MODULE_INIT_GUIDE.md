# 模块初始化指南

> **用途**: 指导在现有项目中添加新模块
> **适用场景**: 项目已初始化，需要添加新的业务模块
> **执行方式**: 人工或AI辅助
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## 概述

### 什么是模块初始化

在已有项目中添加一个新的业务模块：
- 输入：模块需求、类型、接口定义
- 过程：创建目录、生成文档、注册到registry
- 输出：符合规范的模块骨架，ready for开发

### 与项目初始化的区别

| 维度 | 项目初始化 | 模块初始化 |
|------|-----------|-----------|
| 时机 | 项目创建时 | 添加新模块时 |
| 范围 | 整个项目 | 单个模块 |
| 指南 | PROJECT_INIT_GUIDE.md | 本文档 |

---

## 快速开始

### 📚 参考示例

在开始前，建议先查看 **`doc/modules/example/`** 完整的模块示例：

```
doc/modules/example/      ← 完整的参考实现
├── agent.md              ← YAML Front Matter示例
├── README.md             ← 模块文档结构
├── plan.md               ← 实施计划模板
└── doc/                  ← 6个标准文档
    ├── BUGS.md
    ├── CHANGELOG.md
    ├── CONTRACT.md
    ├── PROGRESS.md
    ├── RUNBOOK.md
    └── TEST_PLAN.md
```

**何时参考**：
- ✅ 创建agent.md时，查看YAML Front Matter怎么写
- ✅ 不确定README.md结构时，查看example/README.md
- ✅ 填写CONTRACT.md时，参考example的格式

### 方式1: 使用脚本（推荐）

```bash
make ai_begin MODULE=<module-name>
```

脚本会：
1. 询问模块信息（类型、层级、是否需要api/frontend/）
2. 创建目录结构
3. 从TEMPLATES/复制文档模板
4. 更新registry.yaml
5. 运行校验

### 方式2: 手动创建

如果不使用脚本，按照本文档的"完整流程"部分操作，参考 `doc/modules/example/` 的实际实现。

---

## 完整流程

### Phase 1: 规划（5-10分钟）

#### 1.1 确定模块信息

AI应询问并记录：

**基本信息**:
- 模块名称（entity）：小写字母+下划线，如`user_auth`
- 模块描述：一句话说明模块功能
- 模块类型：1_Assign / 2_Select / 3_SelectMethod / 4_Aggregator
- 模块层级：1-4级

**类型和层级说明**，参考：`MODULE_TYPES.md`

**接口信息**:
- 是否对外提供HTTP接口？→ 决定是否创建`api/`子目录
- 是否有特定的前端组件？→ 决定是否创建`frontend/`子目录
- 输入和输出是什么？

**依赖关系**:
- 依赖哪些上游模块？（upstream）
- 输出到哪些下游？（downstream）
- 依赖哪些公共模块？（common/）

#### 1.2 决策树：是否需要api/和frontend/

```
模块是否对外提供HTTP接口？
├─ 是 → 创建 api/ 子目录
│   └─ 在 api/routes.py 中定义接口
└─ 否 → 不创建 api/（模块只提供Python/Go函数）

模块是否有特定的UI组件？
├─ 是 → 创建 frontend/ 子目录
│   └─ 在 frontend/components/ 中实现组件
└─ 否 → 不创建 frontend/（只有通用UI）
```

**详细说明**：参考`temp/app_frontend_职责划分说明.md`（Phase 3将迁移）

#### 1.3 确认模块结构

展示将要创建的结构，用户确认：

```
modules/<entity>/
├── agent.md             ✅ 必须
├── README.md            ✅ 必须
├── plan.md              ✅ 必须
├── doc/                 ✅ 必须
│   ├── CONTRACT.md
│   ├── CHANGELOG.md
│   ├── RUNBOOK.md
│   ├── BUGS.md
│   ├── PROGRESS.md
│   └── TEST_PLAN.md
├── core/                ✅ 必须（业务逻辑）
│   └── __init__.py
├── api/                 ⚠️ 可选（如提供HTTP接口）
│   ├── routes.py
│   └── __init__.py
├── frontend/            ⚠️ 可选（如有特定UI）
│   └── components/
└── models/              ⚠️ 可选（如有专属模型）
    └── schemas.py
```

---

### Phase 2: 创建目录（2-3分钟）

#### 2.1 创建基础目录

```bash
MODULE=<entity>

# 必需目录
mkdir -p modules/$MODULE/{core,doc}

# 可选：如has_api=true
mkdir -p modules/$MODULE/api

# 可选：如has_frontend=true
mkdir -p modules/$MODULE/frontend/components

# 可选：如有专属模型
mkdir -p modules/$MODULE/models
```

#### 2.2 创建__init__.py（Python项目）

```bash
# 使core/和api/成为Python包
touch modules/$MODULE/core/__init__.py
touch modules/$MODULE/api/__init__.py
touch modules/$MODULE/models/__init__.py
```

---

### Phase 3: 生成文档（10-15分钟）

#### 3.1 创建agent.md（关键）

**参考示例**：查看 `doc/modules/example/agent.md` 了解完整结构

从TEMPLATES/agent.md.template复制并调整：

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
    # - modules.<other>.v1  # 如有依赖
  downstream:
    - orchestrator.main    # 或其他下游

constraints:
  - "不得直接操作数据库，必须通过ORM"
  - "保持测试覆盖率≥80%"

tools_allowed:
  calls:
    - http.get
    - http.post
    - fs.read
    - db.query
  models:
    - gpt-4
    - claude-3-sonnet

quality_gates:
  required_tests:
    - unit
    - integration
    - contract
  coverage_min: 0.80

orchestration_hints:
  triggers:
    - on_http_request
  routing_tags:
    - "module:<entity>"
    - "level:1"
  priority: 5

context_routes:
  always_read:
    - /doc/policies/goals.md
    - /doc/policies/safety.md
  by_scope:
    - scope: "modules/<entity>"
      read:
        - /modules/<entity>/README.md
        - /modules/<entity>/doc/CONTRACT.md
        - /modules/<entity>/doc/CHANGELOG.md
---

# <Entity>模块Agent

## 1. 模块概述

### 1.1 功能描述
<简要描述模块的核心功能>

### 1.2 核心职责
- 职责1
- 职责2
- 职责3

### 1.3 不负责
- 非职责1（由XX模块负责）
- 非职责2（由XX模块负责）

---

## 2. 目录结构

参见：`modules/<entity>/README.md`

---

## 3. 接口契约

详见：`modules/<entity>/doc/CONTRACT.md`

---

## 4. 依赖关系

### 4.1 上游依赖
- common.models.base: 基础模型定义
- <其他模块>: <说明>

### 4.2 下游输出
- orchestrator.main: 编排器调度

---

## 5. 使用示例

### 5.1 API调用（如has_api=true）
```bash
curl -X POST http://localhost:8000/api/<entity>/ \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

### 5.2 内部调用（如has_api=false）
```python
from modules.<entity>.core.service import <Entity>Service

service = <Entity>Service()
result = service.main_function(input_data)
```

---

## 6. 开发规范

参见：`doc/policies/safety.md`

---

## 7. 测试要求

参见：`modules/<entity>/doc/TEST_PLAN.md`

---

## 8. 运维手册

参见：`modules/<entity>/doc/RUNBOOK.md`
```

#### 3.2 创建README.md

**参考示例**：查看 `doc/modules/example/README.md` 了解完整结构

```markdown
# <Entity>模块

> **功能**: <一句话功能描述>
> **类型**: 1_<entity>
> **层级**: 1
> **状态**: 开发中

---

## 概述

<详细功能描述>

---

## 目录结构

\`\`\`
modules/<entity>/
├── agent.md              # Agent配置（AI可读）
├── README.md             # 本文档（人类可读）
├── plan.md               # 实施计划
├── doc/                  # 详细文档
│   ├── CONTRACT.md       # API契约
│   ├── CHANGELOG.md      # 变更记录
│   ├── RUNBOOK.md        # 运维手册
│   ├── BUGS.md           # 已知问题
│   ├── PROGRESS.md       # 进度追踪
│   └── TEST_PLAN.md      # 测试计划
├── core/                 # 核心业务逻辑 ✅ 必需
│   ├── service.py        # 主要服务类
│   └── utils.py          # 工具函数
├── api/                  # HTTP接口层 ⚠️ 可选
│   ├── routes.py         # 路由定义
│   └── middleware.py     # 模块级中间件
├── frontend/             # 前端组件 ⚠️ 可选
│   └── components/
│       └── <Entity>Card.tsx
└── models/               # 数据模型 ⚠️ 可选
    └── schemas.py        # Pydantic模型
\`\`\`

### 子目录说明

#### core/（必需）
- **职责**: 核心业务逻辑
- **包含**: Service类、业务函数、算法实现
- **不包含**: HTTP处理、数据库直接操作

#### api/（可选）
- **创建条件**: 模块对外提供HTTP接口
- **职责**: 定义路由、参数验证、调用core/
- **不包含**: 业务逻辑（应在core/中）

#### frontend/（可选）
- **创建条件**: 模块有特定的UI组件
- **职责**: 实现模块专属的前端组件
- **不包含**: 通用组件（应在根frontend/components/）

#### models/（可选）
- **创建条件**: 模块有专属的数据模型
- **职责**: 定义Pydantic/数据类
- **不包含**: 数据库表定义（应在db/中）

---

## 核心功能

### 功能1: <名称>
<描述>

### 功能2: <名称>
<描述>

---

## API接口（如has_api=true）

详见：`doc/CONTRACT.md`

---

## 前端组件（如has_frontend=true）

详见：`doc/CONTRACT.md` 前端部分

---

## 依赖

### 上游依赖
- common.models.base
- <其他>

### 被依赖
- <其他模块>

---

## 快速开始

### 开发
\`\`\`bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest tests/<entity>/

# 运行服务
make dev MODULE=<entity>
\`\`\`

### 部署
参见：`doc/RUNBOOK.md`

---

## 文档索引

| 文档 | 说明 |
|------|------|
| agent.md | Agent配置（AI可读） |
| README.md | 模块概览（本文档） |
| plan.md | 实施计划 |
| doc/CONTRACT.md | API契约 |
| doc/CHANGELOG.md | 变更记录 |
| doc/RUNBOOK.md | 运维手册 |
| doc/BUGS.md | 已知问题 |
| doc/PROGRESS.md | 进度追踪 |
| doc/TEST_PLAN.md | 测试计划 |

---

**维护者**: <姓名>
**创建时间**: <日期>
**最后更新**: <日期>
```

#### 3.3 创建doc/下的6个文档

**参考示例**：查看 `doc/modules/example/doc/` 了解文档内容和格式

从`doc/modules/TEMPLATES/`复制并调整：

- CONTRACT.md（API契约）- 参考 `example/doc/CONTRACT.md`
- CHANGELOG.md（变更记录）- 参考 `example/doc/CHANGELOG.md`
- RUNBOOK.md（运维手册）- 参考 `example/doc/RUNBOOK.md`
- BUGS.md（已知问题）- 参考 `example/doc/BUGS.md`
- PROGRESS.md（进度追踪）- 参考 `example/doc/PROGRESS.md`
- TEST_PLAN.md（测试计划）- 参考 `example/doc/TEST_PLAN.md`

#### 3.4 创建plan.md

```markdown
# <Entity>模块实施计划

## 目标
<模块要实现的目标>

## 里程碑
- [ ] M1: 核心逻辑实现（Week 1-2）
- [ ] M2: API接口开发（Week 3）
- [ ] M3: 测试覆盖（Week 4）
- [ ] M4: 文档完善（Week 5）
- [ ] M5: 上线部署（Week 6）

## 风险
- 风险1: <描述>
  - 缓解措施: <方案>
- 风险2: <描述>
  - 缓解措施: <方案>

---

详细计划参见：`doc/PROGRESS.md`
```

---

### Phase 4: 注册模块（5分钟）

#### 4.1 更新registry.yaml

手动添加到`doc/orchestration/registry.yaml`：

```yaml
module_instances:
  # ... 现有模块 ...
  
  - id: <entity>.v1
    type: 1_<entity>
    path: modules/<entity>
    level: 1
    status: dev  # dev/active/deprecated
    version: 1.0.0
    owners:
      - <your-name>
    agent_md: modules/<entity>/agent.md
    readme: modules/<entity>/README.md
    contracts:
      - modules/<entity>/doc/CONTRACT.md
    upstream:
      - common.models.base
      # - <other-module>
    downstream:
      - orchestrator.main
    tags:
      - <entity>
      - level:1
      - domain:<domain>
    description: "<一句话描述>"
```

或重新生成：

```bash
make registry_gen
# 审核并合并到正式版
```

#### 4.2 添加模块类型（如是新类型）

在`MODULE_TYPES.md`中添加类型定义（见Phase 3部分）。

---

### Phase 5: 校验（3-5分钟）

#### 5.1 运行校验脚本

```bash
# 校验agent.md
make agent_lint
# 应通过：modules/<entity>/agent.md

# 校验registry
make registry_check
# 应通过：新模块已注册

# 校验文档路由
make doc_route_check
# 应通过：所有路径有效

# 一致性检查
make consistency_check
# 应通过：文档完整
```

#### 5.2 检查清单

- [ ] agent.md通过Schema校验
- [ ] agent.md的YAML Front Matter完整
- [ ] README.md包含"目录结构"章节
- [ ] doc/下6个文档全部存在
- [ ] registry.yaml包含新模块
- [ ] 如has_api=true，api/目录存在
- [ ] 如has_frontend=true，frontend/目录存在

---

### Phase 6: 数据库变更（可选，如不确定可跳过）

#### 重要说明 ⚠️

数据库变更**不一定要在模块初始化时完成**。多数情况下：
- **如果不确定**：跳过本Phase，在功能开发过程中再添加
- **如果明确需要**：继续本Phase的基础流程
- **完整流程**：请查看 → **`doc/process/DB_CHANGE_GUIDE.md`** ⭐

**何时需要数据库变更**：
- ✅ 明确知道需要哪些表（如：用户模块需要users表）
- ✅ 有具体的数据结构需求
- ❌ 不确定是否需要表 → **跳过，开发时再说**
- ❌ 不确定表结构 → **跳过，开发时再说**

---

#### 6.1 快速引导（基础流程）

**如果明确需要数据库变更，可以简单了解基础步骤**：

```
AI: 这个模块是否需要新建数据库表或修改现有表？

选项：
A. 明确需要新建表 → 继续6.2
B. 明确需要修改现有表 → 查看DB_CHANGE_GUIDE.md
C. 不确定 / 暂不需要 → 跳过本Phase（推荐）

用户: [选择]
```

**提示**: 完整的数据库变更流程（包括修改表、删除表、索引优化等）请查看：
- 📖 **`doc/process/DB_CHANGE_GUIDE.md`**（完整指南）
- 📖 `db/engines/postgres/schemas/tables/runs.yaml`（表YAML示例）

#### 6.2 创建表结构YAML（如选A）

**参考示例**: 查看 `db/engines/postgres/schemas/tables/runs.yaml`

```bash
# 创建表结构定义
vi db/engines/postgres/schemas/tables/<table_name>.yaml
```

**表YAML结构**:
```yaml
table: <table_name>
description: "<表的用途说明>"
ownership:
  module: modules.<entity>
  maintainer: "<维护者>"

columns:
  - name: id
    type: uuid
    primary_key: true
    not_null: true
    description: "主键"
  
  - name: <field_name>
    type: varchar(255)
    not_null: true
    unique: false
    description: "<字段说明>"
  
  - name: created_at
    type: timestamp
    default: now()
    not_null: true
    description: "创建时间"
  
  - name: updated_at
    type: timestamp
    default: now()
    not_null: true
    description: "更新时间"

indexes:
  - columns: [<field_name>]
    unique: false
  - columns: [created_at]

foreign_keys:
  - column: <fk_field>
    references:
      table: <other_table>
      column: id
    on_delete: CASCADE

metadata:
  partition_key: null
  estimated_rows: 10000
```

#### 6.3 创建迁移脚本（如选A或B）

```bash
# 生成迁移脚本编号
NEXT_NUM=$(ls db/engines/postgres/migrations/*_up.sql | wc -l | awk '{print $1+1}')
NEXT_NUM=$(printf "%03d" $NEXT_NUM)

# 创建up迁移
cat > db/engines/postgres/migrations/${NEXT_NUM}_<entity>_create_<table>_up.sql << 'EOF'
-- 创建<table_name>表
CREATE TABLE <table_name> (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    <field_name> VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 创建索引
CREATE INDEX idx_<table>_<field> ON <table_name>(<field_name>);
CREATE INDEX idx_<table>_created ON <table_name>(created_at);

-- 添加注释
COMMENT ON TABLE <table_name> IS '<表说明>';
COMMENT ON COLUMN <table_name>.<field_name> IS '<字段说明>';
EOF

# 创建down迁移（回滚）
cat > db/engines/postgres/migrations/${NEXT_NUM}_<entity>_create_<table>_down.sql << 'EOF'
-- 删除<table_name>表
DROP TABLE IF EXISTS <table_name> CASCADE;
EOF
```

#### 6.4 校验数据库文件

```bash
# 运行数据库校验
make db_lint
```

---

#### 6.5 开发过程中的数据库变更

**本Phase只是基础引导！** 实际开发中的数据库变更更加复杂，包括：

**更多场景**:
- 修改表结构（增加/删除/修改字段）
- 删除表（高风险操作）
- 优化索引
- 数据迁移
- 外键调整

**触发机制**:
1. 在`plan.md`中标记"涉及数据库变更"
2. 开发过程中发现需要
3. Code Review时识别

**完整流程**: 
请查看 → **`doc/process/DB_CHANGE_GUIDE.md`** 
- 包含AI引导对话
- 详细的表YAML编写指南
- 迁移脚本模板
- 测试数据更新流程
- 常见场景示例
- 常见问题解答

---

### Phase 7: 定义测试数据需求（10-15分钟，推荐）

#### 7.1 AI引导对话

**对话目标**: 确定模块的测试数据策略

```
AI: 现在我们定义测试数据需求。这将帮助后续的测试和开发。

首先，这个模块需要测试数据吗？

选项：
A. 需要（推荐，大多数模块）
B. 不需要（如纯计算模块、工具模块）

用户: [选择]

[如选A，继续]

AI: 好的，让我了解测试数据需求：

1. 需要哪些测试场景的数据？
   - 最小集（minimal）：单元测试用，<10条记录
   - 标准集（standard）：集成测试用，10-100条记录
   - 完整集（full）：性能测试用，>1000条记录

   建议至少提供 minimal 和 standard。

用户: [选择场景]

2. 数据来源策略？
   - Fixtures（手工维护的精确数据，适合小数据量）
   - Mock（自动生成的随机数据，适合大数据量）
   - 混合（小场景用Fixtures，大场景用Mock）

   💡 建议：minimal和standard用Fixtures，full用Mock

用户: [选择策略]

3. 是否有特殊的数据要求？
   - 边界值测试数据（如空字符串、最大长度）
   - 异常数据（如特殊字符、SQL注入测试）
   - 时间分布要求（如最近30天）
   - 状态分布（如70%活跃、30%不活跃）

用户: [描述要求]
```

#### 7.2 创建TEST_DATA.md

**参考模板**: `doc/modules/TEMPLATES/TEST_DATA.md.template`
**参考示例**: `doc/modules/example/doc/TEST_DATA.md`（Phase 6创建）

```bash
# 从模板复制
cp doc/modules/TEMPLATES/TEST_DATA.md.template \
   modules/<entity>/doc/TEST_DATA.md

# 编辑并填写
vi modules/<entity>/doc/TEST_DATA.md
```

**必须定义的内容**:
1. **测试数据需求概览**
   - 数据量级（minimal/standard/full）
   - 数据来源（Fixtures/Mock）

2. **Fixtures定义**（如使用Fixtures）
   - 每个场景的数据表和记录数
   - 具体的数据内容（YAML格式）
   - 数据依赖关系和加载顺序

3. **Mock规则定义**（如使用Mock）
   - 每个表的字段生成规则
   - 数据分布规则
   - 数量配置

4. **测试场景映射**
   - 单元测试用哪个场景
   - 集成测试用哪个场景
   - 性能测试用哪个场景

5. **环境配置**
   - dev环境用什么数据
   - test环境用什么数据
   - demo环境用什么数据

#### 7.3 创建Fixtures目录结构（如使用Fixtures）

```bash
# 创建fixtures目录
mkdir -p modules/<entity>/fixtures

# 创建场景文件
touch modules/<entity>/fixtures/minimal.sql
touch modules/<entity>/fixtures/standard.sql
```

**编写minimal.sql示例**:
```sql
-- Fixtures: minimal (最小测试集)
-- 用途: 单元测试
-- 记录数: <10条

-- 插入<table_name>数据
INSERT INTO <table_name> (id, name, status, created_at) VALUES
('test-001', 'Test User 1', 'active', '2024-01-01 00:00:00'),
('test-002', 'Test User 2', 'inactive', '2024-01-02 00:00:00'),
('test-003', 'Test User 3', 'active', '2024-01-03 00:00:00');
```

#### 7.4 更新agent.md添加test_data字段

```yaml
# 在modules/<entity>/agent.md的YAML Front Matter中添加

test_data:
  enabled: true
  spec: "doc/TEST_DATA.md"
```

#### 7.5 AI引导确认

```
AI: 测试数据定义完成！

创建的文件：
  ├── modules/<entity>/doc/TEST_DATA.md
  ├── modules/<entity>/fixtures/minimal.sql (如选Fixtures)
  └── modules/<entity>/fixtures/standard.sql (如选Fixtures)

更新的文件：
  └── modules/<entity>/agent.md (添加test_data字段)

测试数据策略：
  - minimal: <描述>
  - standard: <描述>
  - 数据来源: <Fixtures/Mock/混合>

这样配置后，后续可以：
  - 使用 `make load_fixture MODULE=<entity> FIXTURE=minimal` 加载测试数据
  - 使用 `make generate_mock MODULE=<entity> COUNT=1000` 生成Mock数据
  - 在测试中自动加载对应场景的数据

请确认测试数据定义是否满足需求？

用户: [确认/修改]
```

---

### Phase 8: 初始代码（10-15分钟，可选）

#### 8.1 创建core/service.py（示例）

```python
# modules/<entity>/core/service.py
"""<Entity>模块核心服务"""
from typing import Any, Dict
from common.models.base import BaseModel

class <Entity>Service:
    """<Entity>核心业务逻辑"""
    
    def __init__(self):
        """初始化服务"""
        pass
    
    async def main_function(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        主要功能函数
        
        Args:
            input_data: 输入数据
            
        Returns:
            处理结果
            
        Raises:
            ValueError: 输入无效
        """
        # TODO: 实现业务逻辑
        return {"status": "success"}
```

#### 8.2 创建api/routes.py（如has_api=true）

```python
# modules/<entity>/api/routes.py
"""<Entity>模块的API路由"""
from fastapi import APIRouter, HTTPException
from modules.<entity>.core.service import <Entity>Service
from modules.<entity>.models.schemas import <Entity>Request, <Entity>Response

router = APIRouter()

@router.post("/", response_model=<Entity>Response)
async def create_<entity>(request: <Entity>Request):
    """创建<entity>"""
    service = <Entity>Service()
    try:
        result = await service.main_function(request.dict())
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

#### 8.3 在app/routes/注册（如has_api=true）

```python
# app/routes/__init__.py
def register_routes(app: FastAPI):
    # ... 现有路由 ...
    
    # 新增<entity>模块路由
    from modules.<entity>.api.routes import router as <entity>_router
    app.include_router(<entity>_router, prefix="/api/<entity>", tags=["<entity>"])
```

---

### Phase 9: 完成与验收（2-3分钟）

#### 9.1 展示成果

AI向用户展示：
```
✅ 模块<entity>初始化完成！

创建的文件：
  ├── modules/<entity>/agent.md
  ├── modules/<entity>/README.md
  ├── modules/<entity>/plan.md
  ├── modules/<entity>/doc/ (6个文档)
  ├── modules/<entity>/core/service.py
  ├── modules/<entity>/api/routes.py (可选)
  └── modules/<entity>/frontend/components/ (可选)

更新的文件：
  ├── doc/orchestration/registry.yaml
  └── app/routes/__init__.py (如has_api=true)

校验结果：
  ✅ make agent_lint: PASS
  ✅ make registry_check: PASS
  ✅ make doc_route_check: PASS
```

#### 9.2 验收清单

- [ ] 所有Phase完成
- [ ] 所有文档齐全
- [ ] 校验全部通过
- [ ] 模块注册成功

#### 9.3 下一步指引

```
接下来你可以：
1. 实现 modules/<entity>/core/service.py 的业务逻辑
2. 补充 doc/CONTRACT.md 的接口定义
3. 编写测试用例（tests/<entity>/）
4. 运行 make dev_check 确保质量

文档参考：
- API契约: modules/<entity>/doc/CONTRACT.md
- 运维手册: modules/<entity>/doc/RUNBOOK.md
- 测试计划: modules/<entity>/doc/TEST_PLAN.md
```

---

## AI执行规范

### 必须做的事
✅ 询问是否需要api/和frontend/子目录
✅ 创建完整的doc/子目录（6个文档）
✅ agent.md包含完整的YAML Front Matter
✅ 更新registry.yaml
✅ 运行全部校验
✅ 提供下一步指引

### 不应做的事
❌ 假设模块结构（必须询问）
❌ 创建空的或无意义的文档
❌ 不更新registry.yaml
❌ 跳过校验步骤
❌ 不提供初始代码骨架

---

## 常见问题

### Q1: 如何判断是否需要api/子目录？
**A**: 询问用户：该模块是否对外提供HTTP接口？如果是，创建api/。如果模块只被内部调用，不创建。

### Q2: api/和app/routes/有什么区别？
**A**: 
- `api/`: 模块特定的API实现（业务逻辑）
- `app/routes/`: 应用级路由分发（不含业务逻辑）

详见：`temp/app_frontend_职责划分说明.md`

### Q3: frontend/和根目录frontend/有什么区别？
**A**: 
- `modules/<entity>/frontend/`: 模块特定的组件（如UserProfile）
- 根`frontend/`: 通用组件（如Button、Modal）

### Q4: 模块类型和层级如何选择？
**A**: 参考`MODULE_TYPES.md`中的定义。常见：
- 1_Assign: 基础业务模块（用户、订单）
- 2_Select: 选择/查询模块
- 3_SelectMethod: 算法选择模块
- 4_Aggregator: 聚合模块

### Q5: 初始化后可以修改结构吗？
**A**: 可以。初始化只是生成骨架，后续可以调整。但需要：
1. 更新agent.md
2. 更新README.md
3. 更新registry.yaml
4. 重新运行校验

---

## 相关文档

- **模块类型说明**: doc/modules/MODULE_TYPES.md
- **项目初始化**: doc/init/PROJECT_INIT_GUIDE.md
- **应用层职责**: temp/app_frontend_职责划分说明.md（Phase 3迁移）
- **文档模板**: doc/modules/TEMPLATES/
- **全局目标**: doc/policies/goals.md
- **安全规范**: doc/policies/safety.md

---

## 版本历史

- 2025-11-07: v1.0 创建，定义模块初始化流程

---

**维护责任**: 项目维护者
**更新频率**: 流程变更时更新

