# 目录结构规范

> **用途**: 定义项目的目录组织规范
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## 核心目录结构

```text
.
├── .aicontext/              # AI上下文索引（docgen生成）
│   ├── snapshot.json        # 快照哈希
│   ├── module_index.json    # 模块索引
│   └── index.json           # 文档索引
├── ai/
│   ├── LEDGER.md            # 任务清册
│   └── sessions/            # 自审记录
├── doc/                     # 文档层（统一）
│   ├── orchestration/       # 编排配置
│   │   ├── registry.yaml    # 模块注册表
│   │   └── routing.md       # 路由规则
│   ├── policies/            # 全局策略
│   │   ├── goals.md         # 全局目标
│   │   ├── safety.md        # 安全规范
│   │   └── roles.md         # 角色与门禁
│   ├── indexes/             # 索引规则
│   ├── init/                # 初始化指南
│   ├── modules/             # 模块相关
│   ├── architecture/        # 架构文档
│   ├── reference/           # 参考文档
│   ├── project/             # 项目文档
│   ├── process/             # 过程文档
│   ├── db/                  # 数据库文档
│   ├── ux/                  # UX文档
│   └── flows/               # DAG配置
├── config/                  # 配置文件
│   ├── schema.yaml          # 配置Schema
│   ├── defaults.yaml        # 默认配置
│   ├── dev.yaml             # 开发环境
│   ├── staging.yaml         # 预发布
│   └── prod.yaml            # 生产环境
├── db/                      # 数据库层
│   └── engines/
│       ├── postgres/        # PostgreSQL
│       └── redis/           # Redis
├── modules/                 # 业务模块层
│   └── <entity>/
│       ├── agent.md         # 模块Agent配置
│       ├── README.md        # 模块概述
│       ├── plan.md          # 实施计划
│       ├── doc/             # 模块文档（6个）
│       ├── core/            # 核心逻辑（必需）
│       ├── api/             # API层（可选）
│       ├── frontend/        # 前端组件（可选）
│       └── models/          # 数据模型（可选）
├── common/                  # 公共层
│   ├── constants/           # 常量
│   ├── interfaces/          # 接口定义
│   ├── middleware/          # 中间件
│   ├── models/              # 公共模型
│   └── utils/               # 工具函数
├── schemas/                 # Schema定义
│   ├── agent.schema.yaml    # Agent Schema
│   └── README.md
├── scripts/                 # 工具脚本
│   ├── agent_lint.py        # Agent校验
│   ├── registry_check.py    # 注册表校验
│   ├── docgen.py            # 文档索引生成
│   └── ...
├── tests/                   # 测试
│   └── <entity>/
│       ├── test_*.py
│       └── conftest.py
├── tools/                   # 工具契约
│   └── codegen/
├── observability/           # 可观测性
│   ├── alerts/              # 告警配置
│   ├── logging/             # 日志配置
│   ├── metrics/             # 指标配置
│   └── tracing/             # 追踪配置
├── migrations/              # 数据库迁移（遗留，Phase 5迁移）
├── agent.md                 # 根Agent配置
├── README.md                # 项目说明
├── Makefile                 # 命令入口
├── requirements.txt         # Python依赖
└── docker-compose.yml       # 本地环境
```

---

## 应用层（可选）

根据项目需求选择是否创建应用层：

### 选项A: 无应用层
**适用**: 微服务、库项目、纯模块组合

**结构**:
```
modules/ + common/
```

**特点**: 
- 每个模块独立运行
- 无统一入口
- 模块间通过RPC/消息队列通信

---

### 选项B: 仅后端应用层
**适用**: 纯后端服务、API服务

**结构**:
```
app/
├── main.py              # 应用入口点
├── routes/              # 路由分发（不含业务逻辑）
└── middleware/          # 应用级中间件
modules/                 # 业务模块
```

**特点**:
- 统一的HTTP入口
- app/routes/分发到modules/
- 无前端

---

### 选项C: 完整应用层
**适用**: 全栈项目、单体应用

**结构**:
```
app/
├── main.py              # 后端入口
└── routes/              # 路由分发
frontend/
├── main.ts              # 前端入口
├── pages/               # 页面路由
└── components/          # 全局组件
modules/                 # 业务模块
```

**特点**:
- 前后端都有统一入口
- 适合单体应用

---

### 选项D: 多应用层
**适用**: 多端应用（客户端+管理端）

**结构**:
```
apps/
├── client/              # 客户端应用
│   ├── main.py
│   └── routes/
└── admin/               # 管理端应用
    ├── main.py
    └── routes/
frontends/
├── client/              # 客户端前端
└── admin/               # 管理端前端
modules/                 # 共享业务模块
```

**特点**:
- 多个独立应用
- 共享业务模块

---

## 应用层与模块层职责边界

**详见**: temp/app_frontend_职责划分说明.md（Phase 4后迁移到doc/architecture/）

### 核心原则

```
应用层 (app/frontend/) = 入口、路由、分发
    ↓ 调用
模块层 (modules/<entity>/) = 业务逻辑
    ↓ 使用
公共层 (common/) = 工具和基础
```

### 决策树

```
代码应该放在哪里？

是否是业务逻辑？
├─ 是 → modules/<entity>/core/
│   └─ 需要HTTP接口？
│       ├─ 是 → modules/<entity>/api/ + 在app/routes/注册
│       └─ 否 → 仅core/
│   └─ 需要UI组件？
│       ├─ 是 → modules/<entity>/frontend/
│       └─ 否 → 无需frontend/
│
└─ 否 → 是否是全局UI？
    ├─ 是 → frontend/components/
    └─ 否 → app/routes/ 或 frontend/pages/
```

**详细说明**: 参见"应用层与模块层职责边界"专门文档

---

## 不需要agent.md的目录

以下目录**不需要**agent.md（只需README.md）：

- schemas/ - 配置/规范
- scripts/ - 工具脚本
- doc/ - 文档
- config/ - 配置
- tests/ - 测试
- db/ - 数据库
- common/ - 公共层
- observability/ - 可观测性

**原因**: 这些目录不是业务模块，不需要被Orchestrator调度。

**详见**: temp/agent.md使用规范.md

---

## 模块实例标准结构

```
modules/<entity>/
├── agent.md             ✅ 必须（带YAML Front Matter）
├── README.md            ✅ 必须（含目录结构章节）
├── plan.md              ✅ 必须
├── doc/                 ✅ 必须（6个文档）
│   ├── CONTRACT.md      # API契约
│   ├── CHANGELOG.md     # 变更记录
│   ├── RUNBOOK.md       # 运维手册
│   ├── BUGS.md          # 已知问题
│   ├── PROGRESS.md      # 进度追踪
│   └── TEST_PLAN.md     # 测试计划
├── core/                ✅ 必须（业务逻辑）
├── api/                 ⚠️ 可选（如提供HTTP接口）
├── frontend/            ⚠️ 可选（如有特定UI）
└── models/              ⚠️ 可选（如有专属模型）
```

**详见**: doc/modules/MODULE_INIT_GUIDE.md

---

## 目录约定

### 目录命名
- 小写字母 + 下划线
- 复数形式（如modules/, tests/）
- 见名知意

### 文件命名
- README.md - 目录说明（所有目录都应有）
- agent.md - Agent配置（仅根目录和模块实例）
- *.md - Markdown文档
- *.yaml/.yml - YAML配置

---

## 相关文档

- **应用层职责**: temp/app_frontend_职责划分说明.md
- **agent.md使用**: temp/agent.md使用规范.md
- **模块初始化**: doc/modules/MODULE_INIT_GUIDE.md
- **项目初始化**: doc/init/PROJECT_INIT_GUIDE.md

---

**维护**: 目录结构变更时更新

