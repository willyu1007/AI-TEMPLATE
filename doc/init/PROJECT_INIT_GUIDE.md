# 项目初始化指南

> **用途**: 指导基于AI-TEMPLATE创建新项目
> **适用场景**: 使用模板创建全新项目
> **执行方式**: 人工或AI辅助
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## 概述

### 什么是项目初始化

从AI-TEMPLATE模板创建一个具体的项目：
- 输入：需求描述、技术栈选择、质量要求
- 过程：AI辅助对话、生成骨架、定制化调整
- 输出：定制化的项目骨架，ready for开发

### 与模块初始化的区别

| 维度 | 项目初始化 | 模块初始化 |
|------|-----------|-----------|
| 时机 | 项目创建时（一次性） | 添加新模块时（多次） |
| 范围 | 整个项目结构 | 单个模块 |
| 产物 | 定制化的repo | modules/<entity>/子目录 |
| 指南 | 本文档 | MODULE_INIT_GUIDE.md |

---

## 初始化方式选择

### AI引导对话

```
AI: 欢迎使用AI-TEMPLATE！

我将帮助您创建新项目。首先，请选择初始化方式：

方式1: 📄 有开发文档（推荐）
  适用：已有PRD、需求文档、架构图等开发文档
  流程：上传文档 → AI解析 → 对齐方案 → 自动生成骨架
  耗时：15-30分钟
  优点：快速、准确、文档驱动

方式2: 💬 从零开始（AI对话式）
  适用：没有文档，通过对话逐步明确需求
  流程：AI问答 → 收集需求 → 生成文档 → 生成骨架
  耗时：25-45分钟
  优点：适合初期想法不清晰的项目

方式3: ✋ 手动初始化
  适用：熟悉本模板，想完全自主控制
  流程：提供操作清单 → 用户手动执行
  耗时：30-60分钟（取决于经验）
  优点：完全控制，学习模板结构

方式4: 📦 导入现有项目
  适用：从其他项目迁移到本模板
  流程：分析现有项目 → 架构映射 → 代码迁移
  耗时：1-4小时（取决于项目规模）
  优点：保留现有代码，升级到新架构

💡 提示：
- 如果您有明确的需求文档，建议选择方式1（最快）
- 如果您是初次使用本模板，建议选择方式2（有引导）
- 如果您想深入理解模板，可以选择方式3（学习）
- 如果您要迁移现有项目，选择方式4

用户: [选择1/2/3/4]
```

---

## 方式1: 有开发文档（文档驱动）

### 前置条件
- 已有PRD、需求文档、架构图、或详细的功能说明
- 文档格式：Markdown/PDF/Word/纯文本均可

### 流程

#### Step 1: 上传文档（2-5分钟）

```
AI: 好的，请上传您的开发文档。

支持的文档类型：
- PRD（产品需求文档）
- 技术架构文档
- 需求说明文档
- 功能列表
- 用户故事
- API设计文档
- 数据模型图

您可以上传多个文档，我会综合分析。

用户: [上传文档]

AI: 文档已接收！我正在分析...
    - 文档1: <文件名>（<大小>）
    - 文档2: <文件名>（<大小>）
    
    开始解析文档内容...
```

#### Step 2: AI解析文档（5-10分钟）

```
AI: 文档分析完成！我提取了以下信息：

📋 项目基本信息：
- 项目名称：<从文档提取>
- 项目类型：<Web应用/API服务/CLI工具/...>
- 技术栈：<从文档提取或推断>

📦 核心模块（共<N>个）：
1. <module1> - <描述>
2. <module2> - <描述>
3. <module3> - <描述>
...

🗄️ 数据库需求：
- 数据库类型：<PostgreSQL/MySQL/...>
- 主要数据表（<M>个）：
  - <table1>: <描述>
  - <table2>: <描述>
  ...

🔧 应用层结构建议：
基于文档分析，我建议使用：<选项B - 仅后端应用层>
理由：<说明>

⚙️ 其他关键信息：
- 认证方式：<JWT/OAuth/...>
- 预期流量：<低/中/高>
- 测试要求：<覆盖率要求>

请确认以上信息是否正确？如有遗漏或错误，请告诉我。

用户: [确认/修改/补充]
```

#### Step 3: 方案对齐与补充（5-10分钟）

```
AI: 我还需要确认几个文档中没有明确的信息：

[根据文档缺失的信息动态提问]

1. 技术栈具体框架？
   - Python: FastAPI / Flask / Django
   - Go: Gin / Echo / Fiber
   - TypeScript: Express / NestJS / Koa
   
   用户: [选择]

2. 前端是否与后端在同一repo？
   - 是（创建frontend/目录）
   - 否（前后端分离）
   
   用户: [选择]

3. [其他补充问题...]

AI: 好的，所有信息已收集完成！
    我现在将生成项目骨架...
```

#### Step 4: 自动生成骨架（10-15分钟）

AI自动执行：
1. 创建目录结构
2. 生成所有模块（从文档提取）
3. 生成数据库表YAML（从文档提取）
4. 生成registry.yaml
5. 更新README.md
6. 更新agent.md
7. 运行校验

```
AI: 骨架生成完成！

已创建：
  ✅ <N>个模块目录（modules/<module1-N>/）
  ✅ <M>个数据库表YAML
  ✅ registry.yaml（已注册所有模块）
  ✅ README.md（已更新）
  ✅ agent.md（已配置）

校验结果：
  ✅ make agent_lint: PASS
  ✅ make registry_check: PASS
  ✅ make db_lint: PASS

接下来进行代码迁移...

用户: [确认继续]
```

#### Step 5: 代码迁移（见PROJECT_MIGRATION_GUIDE.md）

详细的迁移策略和步骤，请查看专门文档：
- **`doc/init/PROJECT_MIGRATION_GUIDE.md`**

---

## 方式3: 手动初始化（详细清单）

详见：**`doc/init/MANUAL_INIT_CHECKLIST.md`**

---

## 方式4: 导入现有项目（项目迁移）

### 前置条件
- 有一个现有项目需要迁移到AI-TEMPLATE
- 愿意调整项目结构以符合模板规范
- 现有项目有清晰的模块划分（或愿意重新划分）

### 流程

#### Step 1: 分析现有项目（15-30分钟）

```
AI: 我将帮助您将现有项目迁移到AI-TEMPLATE架构。

请提供以下信息：

1. 现有项目的路径？（本地路径或GitHub链接）
   用户: [提供路径]

AI: 正在分析项目结构...
    
    [扫描目录、识别文件类型、分析依赖]

分析结果：

📁 项目结构：
<当前目录树>

📋 项目信息：
- 项目名称：<识别>
- 技术栈：<识别语言和框架>
- 代码行数：<统计>

📦 识别的模块/组件：
1. <component1> - <推测功能>
2. <component2> - <推测功能>
...

🗄️ 数据库：
- 类型：<PostgreSQL/MySQL/...>
- 表数量：<N>个
- 主要表：<table1>, <table2>, ...

⚙️ 依赖关系：
[识别的模块间依赖]

2. 以上识别是否正确？请补充或修正。
   用户: [确认/修正]

3. 是否有架构文档或README可以提供？
   （有助于更准确的理解项目结构）
   用户: [上传文档/没有]
```

#### Step 2: 架构映射（10-20分钟）

```
AI: 我将现有项目结构映射到AI-TEMPLATE架构：

📐 架构映射方案：

旧结构 → 新结构：
┌─────────────────────┬──────────────────────────┐
│ 旧路径              │ 新路径                   │
├─────────────────────┼──────────────────────────┤
│ /src/users/         │ /modules/user/           │
│ /src/orders/        │ /modules/order/          │
│ /src/products/      │ /modules/product/        │
│ /src/common/        │ /common/                 │
│ /api/routes/        │ /app/routes/             │
│ /db/models.py       │ /db/engines/postgres/... │
│ /tests/             │ /tests/                  │
│ /frontend/          │ /frontend/               │
└─────────────────────┴──────────────────────────┘

📦 模块划分与分类：
┌──────────┬──────────┬──────┬─────────────┐
│ 模块名   │ 模块类型 │ 层级 │ 说明        │
├──────────┼──────────┼──────┼─────────────┤
│ user     │ 1_Assign │ 1    │ 用户管理    │
│ order    │ 1_Assign │ 1    │ 订单管理    │
│ product  │ 1_Assign │ 1    │ 产品管理    │
│ payment  │ 2_Select │ 2    │ 支付选择    │
└──────────┴──────────┴──────┴─────────────┘

🗄️ 数据库表映射：
- users表 → db/engines/postgres/schemas/tables/users.yaml + 迁移脚本
- orders表 → db/engines/postgres/schemas/tables/orders.yaml + 迁移脚本
- products表 → db/engines/postgres/schemas/tables/products.yaml + 迁移脚本

这个映射方案是否合理？

用户: [确认/调整]

AI: [根据用户反馈调整映射方案]
```

#### Step 3: 选择迁移策略（5分钟）

```
AI: 请选择代码迁移策略：

策略A: 📋 直接复制（最快）
  - 直接复制代码文件到新结构
  - 批量调整import路径
  - 适合：结构相近、代码质量好
  - 耗时：30-60分钟
  - 风险：低

策略B: 🤖 AI重新实现（推荐）
  - AI读取旧代码逻辑
  - 按新架构重新实现
  - 保持API兼容性
  - 适合：想要代码重构、提升质量
  - 耗时：2-4小时
  - 风险：中（需充分测试）

策略C: 🏗️ 仅骨架（最灵活）
  - 只生成目录结构和文档
  - 代码由用户手动迁移
  - 适合：代码复杂、需要精细控制
  - 耗时：1-3小时（用户手动）
  - 风险：低

💡 建议：
- 小型项目（<5000行）：选A或B
- 中型项目（5000-20000行）：选B或C
- 大型项目（>20000行）：选C
- 代码质量不理想：选B

用户: [选择A/B/C]
```

#### Step 4: 执行迁移（30分钟-4小时）

**策略A: 直接复制**

```
AI: 开始执行迁移（策略A：直接复制）...

[1/6] 创建新结构目录...
  ✅ 已创建 modules/user/
  ✅ 已创建 modules/order/
  ...

[2/6] 复制代码文件...
  ✅ 复制 src/users/* → modules/user/core/
  ✅ 复制 src/orders/* → modules/order/core/
  ...

[3/6] 调整import路径...
  正在扫描并替换import语句...
  ✅ 更新了45个文件的import
  
[4/6] 生成文档...
  ✅ 生成 modules/user/agent.md
  ✅ 生成 modules/user/README.md
  ...

[5/6] 生成数据库YAML和迁移脚本...
  ✅ 生成 db/engines/postgres/schemas/tables/users.yaml
  ✅ 生成迁移脚本（001-005）
  
[6/6] 运行校验...
  ✅ make agent_lint: 3/3 PASS
  ✅ make registry_check: PASS
  ✅ make db_lint: PASS

迁移完成！请运行测试验证功能正确性。

用户: [确认]
```

**策略B: AI重新实现**

```
AI: 开始执行迁移（策略B：AI重新实现）...

我将逐个模块重新实现，保持功能等价但代码质量更高。

[模块1/3] user模块
  - 正在阅读旧代码：src/users/*.py
  - 理解业务逻辑：用户注册、登录、权限管理
  - 按新架构实现：modules/user/core/service.py
  - 生成测试：tests/user/test_service.py
  - 验证功能等价：运行测试对比
  ✅ user模块重新实现完成

[模块2/3] order模块
  ...

[模块3/3] product模块
  ...

迁移完成！所有模块已重新实现并通过测试。

用户: [确认]
```

**策略C: 仅骨架**

```
AI: 开始执行迁移（策略C：仅骨架）...

[1/3] 生成目录结构...
  ✅ modules/user/（空）
  ✅ modules/order/（空）
  ...

[2/3] 生成文档和配置...
  ✅ agent.md、README.md等
  ✅ registry.yaml
  ...

[3/3] 生成代码框架...
  ✅ modules/user/core/service.py（空函数签名）
  ...

骨架生成完成！

接下来请您手动迁移代码：
1. 将旧代码复制到对应的modules/<entity>/core/目录
2. 调整import路径
3. 实现空函数
4. 补充测试
5. 运行 make dev_check 验证

参考：doc/init/MANUAL_INIT_CHECKLIST.md

用户: [开始手动迁移]
```

#### Step 5: 验证与测试（10-30分钟）

```bash
# 运行完整校验
make validate

# 运行测试
pytest tests/

# 检查覆盖率
pytest --cov=modules tests/

# 启动服务验证
make dev
```

#### Step 6: 清理与提交（见下文"清理模板痕迹"）

**详细的迁移指南**: 请查看 **`doc/init/PROJECT_MIGRATION_GUIDE.md`**

---

## 初始化流程（方式2：从零开始）

**注意**: 以下是方式2的详细流程，也是Phase 6之前的默认流程。

### Phase 1: 需求收集（10-20分钟）

#### 1.1 AI对话式引导

**对话目标**: 通过结构化问答，全面收集项目初始化所需信息

**对话范式**:
```
AI: 您好！我将帮助您基于AI-TEMPLATE创建新项目。
    整个过程大约需要15-30分钟，我会询问一些关键问题。
    您随时可以说"不确定"或"跳过"，我会提供建议。
    
    让我们开始吧！
```

#### 1.2 核心问题清单（AI引导对话）

**第1组：项目基本信息**

```
AI: 首先，请告诉我项目的基本信息：

1. 项目名称是什么？（小写字母+连字符，如：my-awesome-api）
   用户: [回答]
   
2. 用一句话描述项目的核心功能？
   用户: [回答]
   
3. 技术栈选择：
   - Python（FastAPI/Flask）
   - Go（Gin/Echo）
   - TypeScript（Express/NestJS）
   - 混合（请说明组合）
   用户: [选择]
   
4. 预期项目规模？
   - 小型（<5个模块，单机部署）
   - 中型（5-15个模块，简单集群）
   - 大型（15+个模块，微服务架构）
   用户: [选择]
```

**第2组：业务需求**

```
AI: 接下来，让我了解您的业务需求：

1. 请列出3-5个核心功能（优先级从高到低）
   例如：用户认证、商品管理、订单处理、支付集成、数据分析
   用户: [列举]

2. 有哪些用户角色？每个角色的权限如何？
   例如：游客（只读）、普通用户（CRUD自己的数据）、管理员（全部权限）
   用户: [描述]

3. 预期的流量和性能要求？
   - 低流量（<1000 DAU）
   - 中等流量（1000-10万 DAU）
   - 高流量（>10万 DAU）
   - 不确定
   用户: [选择]
```

**第3组：质量要求**

```
AI: 关于质量和规范：

1. 测试覆盖率要求？
   - 严格（≥90%）
   - 标准（≥80%）
   - 宽松（≥60%）
   - 根据模块决定
   用户: [选择]

2. 文档完整度要求？
   - 严格（所有模块完整文档）
   - 标准（核心模块完整文档）
   - 宽松（README + 关键API文档）
   用户: [选择]

3. 是否需要CI/CD集成？
   - 是（GitHub Actions/GitLab CI）
   - 否（手动部署）
   - 后续添加
   用户: [选择]
```

**第4组：应用层结构选择**（关键决策）

```
AI: 现在是一个重要的架构决策——应用层结构：

您的项目需要哪种应用层结构？

选项A: 无应用层（纯模块组合）
  适用：微服务项目、库项目、CLI工具
  结构：modules/ + common/
  特点：每个模块独立部署，没有统一入口

选项B: 仅后端应用层（app/routes/）
  适用：纯后端服务、RESTful API、GraphQL服务
  结构：app/routes/ + modules/
  特点：统一的API入口，模块通过app/routes/暴露

选项C: 完整应用层（app/ + frontend/）
  适用：全栈单体应用、SSR项目、管理后台
  结构：app/routes/ + frontend/ + modules/
  特点：前后端在同一repo，完整的全栈结构

💡 提示：
- 如果不确定，建议选B（最常见）
- 前后端分离项目应选B（前端独立repo）
- 单体应用选C
- 微服务选A

用户: [选择A/B/C]

AI: [根据选择] 好的，我将创建<描述结构>。
```

**第5组：数据库与非功能需求**

```
AI: 最后几个问题：

1. 需要哪些数据库？
   - PostgreSQL（关系型，推荐）
   - MySQL（关系型）
   - Redis（缓存/队列）
   - MongoDB（文档型）
   - 多个（请说明）
   - 暂不需要
   用户: [选择]

2. 认证方式？
   - JWT（推荐，无状态）
   - Session（有状态）
   - OAuth 2.0（第三方登录）
   - 无需认证（公开API）
   - 后续添加
   用户: [选择]

3. 可观测性要求？
   - 基础（日志输出到文件）
   - 标准（日志 + 基础指标）
   - 完整（日志 + 指标 + 链路追踪）
   - 不需要
   用户: [选择]
```

#### 1.3 信息确认和补充

```
AI: 太好了！我已经收集了所有信息。让我总结一下：

项目名称: <project-name>
技术栈: <stack>
规模: <size>
核心功能: <features>
应用层结构: <选项>
数据库: <databases>
...

请确认以上信息是否正确？
如有需要修改的地方，请告诉我。

用户: [确认/修改]

AI: 好的！我现在开始生成项目骨架...
```

---

### Phase 2: 方案对齐（10-15分钟）

#### 2.1 AI生成项目规划

```
AI: 正在生成项目规划...

根据您的需求，我建议以下方案：
```

AI基于收集的信息生成：

**目录结构规划**:
```
<project-name>/
├── app/                    # 应用层（按需创建）
│   └── routes/            # 路由入口
├── frontend/               # 前端层（按需创建）
│   ├── pages/
│   └── components/
├── modules/                # 业务模块层
│   ├── <module1>/
│   └── <module2>/
├── common/                 # 公共层
├── db/                     # 数据库层
├── config/                 # 配置层
└── doc/                    # 文档层
```

**模块规划**:
```yaml
planned_modules:
  - name: user
    type: 1_Assign
    level: 1
    has_api: true
    has_frontend: true
    description: "用户认证和管理"
  - name: product
    type: 1_Assign
    level: 1
    has_api: true
    has_frontend: false
    description: "产品信息管理"
```

**技术栈清单**:
- 后端框架（FastAPI/Flask/Gin/Express）
- 前端框架（React/Vue/无）
- 数据库（PostgreSQL/Redis）
- ORM（SQLAlchemy/Gorm/Prisma）

#### 2.2 用户确认和调整

```
AI: 以上就是我的建议方案。请您审阅：

1. 目录结构是否符合预期？
2. 模块划分是否合理？
3. 技术栈选择是否正确？

如果有任何需要调整的地方，请告诉我。
例如："product模块不需要frontend"、"增加一个notification模块"等

用户: [确认/提出调整]

AI: [根据反馈调整] 好的，我已更新方案。
    现在开始生成项目骨架...
```

---

### Phase 3: 生成骨架（15-30分钟）

#### 3.1 基础目录创建

```bash
# 克隆模板
git clone <AI-TEMPLATE-repo> <project-name>
cd <project-name>

# 删除模板专用文件
rm -rf temp/ TEMPLATE_USAGE.md

# 根据选项创建应用层
# 选项A: 无应用层 → 跳过
# 选项B: 仅后端 → mkdir app/routes
# 选项C: 完整 → mkdir app/routes frontend/pages frontend/components
```

#### 3.2 更新根文档

**README.md**:
- 项目名称和描述
- 快速开始指南
- 核心功能列表
- 技术栈说明

**agent.md**（补充YAML Front Matter）:
```yaml
---
spec_version: "1.0"
agent_id: "repo"
role: "<项目名称>的根编排配置"
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
    - topic: "模块开发"
      paths:
        - /doc/modules/MODULE_INIT_GUIDE.md
---
```

#### 3.3 创建初始模块

为每个规划的模块运行：

```bash
make ai_begin MODULE=<module-name>
```

或AI手动创建：
```bash
mkdir -p modules/<module-name>/{core,doc}
# 如has_api: true
mkdir -p modules/<module-name>/api
# 如has_frontend: true
mkdir -p modules/<module-name>/frontend
```

并创建必需文件：
- agent.md（从TEMPLATES/复制并调整）
- README.md（从TEMPLATES/复制并调整）
- doc/下的6个文档（从TEMPLATES/复制）

#### 3.4 初始化registry.yaml

```bash
# 生成草案
make registry_gen

# 审核并补充信息
vi doc/orchestration/registry.yaml.draft

# 确认无误后正式化
mv doc/orchestration/registry.yaml.draft doc/orchestration/registry.yaml
```

#### 3.5 配置数据库（如需要）

```yaml
# db/engines/postgres/schemas/tables/users.yaml
table: users
columns:
  - name: id
    type: uuid
    primary_key: true
  - name: username
    type: varchar(100)
    unique: true
    not_null: true
  - name: email
    type: varchar(255)
    unique: true
    not_null: true
  - name: created_at
    type: timestamp
    default: now()
indexes:
  - columns: [username]
  - columns: [email]
```

#### 3.6 配置依赖

**requirements.txt**（Python）:
```
fastapi>=0.100.0
uvicorn>=0.23.0
sqlalchemy>=2.0.0
pyyaml>=6.0
pytest>=7.4.0
```

**package.json**（前端，如有）:
```json
{
  "dependencies": {
    "react": "^18.0.0",
    "axios": "^1.5.0"
  }
}
```

---

### Phase 4: 校验（5-10分钟）

#### 4.1 运行全量校验

```bash
# 文档校验
make agent_lint           # 校验agent.md
make registry_check       # 校验registry.yaml
make doc_route_check      # 校验文档路由
make doc_style_check      # 校验文档风格

# 一致性校验
make consistency_check    # 一致性检查
```

#### 4.2 检查清单

- [ ] 所有agent.md都有YAML Front Matter
- [ ] registry.yaml通过校验
- [ ] 所有模块有完整的doc/子目录
- [ ] 文档路由路径全部有效
- [ ] README.md包含必要信息

---

### Phase 5: 确认与清理（5分钟）

#### 5.1 展示成果

AI向用户展示：
- 创建的目录结构
- 生成的模块列表
- 核心文档摘要
- 待办事项（如有）

#### 5.2 清理模板痕迹

```bash
# 删除模板专用文件（如未删除）
rm -rf temp/
rm TEMPLATE_USAGE.md

# 删除示例模块（如不需要）
rm -rf modules/example/

# 初始化git（如需要）
rm -rf .git/
git init
git add .
git commit -m "Initial commit from AI-TEMPLATE"
```

#### 5.3 下一步指引

AI提示用户：
```
✅ 项目初始化完成！

接下来你可以：
1. 查看 README.md 了解项目结构
2. 阅读 QUICK_START.md 开始开发
3. 运行 make dev_check 确保一切正常
4. 开始实现业务逻辑

如需添加新模块，使用：
  make ai_begin MODULE=<name>
或参考：doc/modules/MODULE_INIT_GUIDE.md
```

---

## 决策点详解

### 决策1: 是否创建app/目录

**考虑因素**:
- 是否需要统一的路由入口？
- 是否有跨模块的应用逻辑？
- 是否是单体应用？

**决策树**:
```
是否需要HTTP入口？
├─ 否 → 选项A（无应用层）
└─ 是 → 是否有前端？
    ├─ 否 → 选项B（仅app/routes/）
    └─ 是 → 选项C（app/ + frontend/）
```

### 决策2: 是否创建frontend/目录

**考虑因素**:
- 是否需要前端页面？
- 前端是否与后端在同一repo？
- 是否有模块级的前端组件？

**建议**:
- 前后端分离项目 → 不创建frontend/（前端独立repo）
- 全栈单体项目 → 创建frontend/
- 仅后端API → 不创建frontend/

### 决策3: 模块是否需要api/子目录

**考虑因素**:
- 模块是否对外提供HTTP接口？
- 接口是否由app/routes/暴露？

**规则**:
```yaml
# modules/<entity>/
has_api: true    # 如果模块提供独立的HTTP接口
has_api: false   # 如果模块只被内部调用

# 示例
user模块: has_api=true  （提供/api/users/接口）
utils模块: has_api=false （只提供Python函数）
```

### 决策4: 模块是否需要frontend/子目录

**考虑因素**:
- 模块是否有特定的前端组件？
- 组件是否可复用？

**规则**:
```yaml
# modules/<entity>/
has_frontend: true    # 如果有模块特定的UI组件
has_frontend: false   # 如果只有通用组件

# 示例
user模块: has_frontend=true  （UserProfile组件）
product模块: has_frontend=true （ProductCard组件）
logger模块: has_frontend=false （无UI）
```

详见：`temp/app_frontend_职责划分说明.md`

---

## AI执行规范

### 必须做的事
✅ 询问所有关键决策（应用层结构、模块规划）
✅ 生成完整的目录结构
✅ 为所有agent.md补充YAML Front Matter
✅ 创建并验证registry.yaml
✅ 运行全量校验
✅ 提供下一步指引

### 不应做的事
❌ 跳过用户确认环节
❌ 假设用户需求（必须询问）
❌ 创建空的或无意义的模块
❌ 遗漏必需的文档
❌ 不运行校验就声称完成

---

## 常见问题

### Q1: 是否必须创建模块？
**A**: 不是必须的。如果是简单项目，可以只用common/和app/。但建议至少创建1个模块以保持结构清晰。

### Q2: 可以混用多种语言吗？
**A**: 可以。AI-TEMPLATE支持Python/Go/TypeScript混合。在registry.yaml中标注每个模块的语言即可。

### Q3: 初始化后可以修改结构吗？
**A**: 可以。初始化只是生成骨架，后续可以添加/删除/重构模块。但需要同步更新registry.yaml。

### Q4: 如何从已有项目迁移到AI-TEMPLATE？
**A**: 这是"项目迁移"而非"项目初始化"，需要单独的迁移指南（待补充）。

### Q5: 初始化后temp/目录可以删除吗？
**A**: 应该删除。temp/是AI-TEMPLATE自身的工作目录，具体项目不需要。

---

## 相关文档

- **模块初始化**: doc/modules/MODULE_INIT_GUIDE.md
- **模块类型说明**: doc/modules/MODULE_TYPES.md
- **应用层职责**: temp/app_frontend_职责划分说明.md（Phase 3迁移）
- **全局目标**: doc/policies/goals.md
- **安全规范**: doc/policies/safety.md

---

## 版本历史

- 2025-11-07: v1.0 创建，定义项目初始化流程

---

**维护责任**: 项目维护者
**更新频率**: 流程变更时更新

