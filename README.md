# Agent Repo - AI 辅助开发项目模板

> 为 AI Agent 优化的项目骨架，支持模块化开发、自动化质量门禁、完整的文档体系。

## 目标
提供一个可复用的项目模板，帮助团队快速建立AI辅助开发环境，实现高质量的软件交付。

## 适用场景
- AI Agent 辅助的软件开发项目
- 需要严格文档管理的企业项目
- 多模块、多团队协作项目
- 需要长期维护和演进的系统

## 核心能力

本模板提供以下能力：
- 为 AI Agent 提供清晰的上下文结构
- 提供完整的自动化工具链
- 建立统一的文档规范
- 实现质量门禁自动化
- 支持模块化开发流程

## 快速开始

### 安装依赖
```
# Python 依赖
pip install -r requirements.txt

# 或使用自动检测
make deps_check
```

## 初始化项目
```
# 生成文档索引
make docgen

# 创建契约基线
make update_baselines

# 运行完整检查
make dev_check
```

## 创建第一个模块
```
# 初始化模块（自动生成所有文档和测试）
make ai_begin MODULE=my_feature

# 查看生成的文件
ls -la modules/my_feature/
ls -la tests/my_feature/
```

详细指南请查看 [QUICK_START.md](QUICK_START.md)。

---

## 项目结构

```text
.
├── agent.md                 # AI Agent 工作指南（核心文档）
├── QUICK_START.md           # 快速开始指南
├── TEMPLATE_USAGE.md        # 模板使用说明
│
├── .aicontext/              # AI 上下文索引
├── .contracts_baseline/     # 契约基线
├── ai/                      # AI 会话记录
│   ├── LEDGER.md           # 任务清册
│   └── sessions/           # 会话历史
│
├── config/                  # 配置文件
│   ├── schema.yaml         # 配置 Schema
│   ├── defaults.yaml       # 默认配置
│   └── <env>.yaml          # 环境配置
│
├── docs/                    # 项目文档
│   ├── project/            # 项目级文档
│   ├── process/            # 流程规范
│   ├── db/                 # 数据库文档
│   ├── flows/              # 流程图
│   └── ux/                 # UX 文档
│
├── flows/                   # DAG 配置
│   └── dag.yaml
│
├── migrations/              # 数据库迁移
│   ├── *_up.sql
│   └── *_down.sql
│
├── modules/                 # 业务模块
│   └── <module>/
│       ├── README.md       # 模块说明
│       ├── plan.md         # 开发计划
│       ├── CONTRACT.md     # 接口契约
│       ├── TEST_PLAN.md    # 测试计划
│       ├── RUNBOOK.md      # 运维手册
│       ├── PROGRESS.md     # 进度跟踪
│       ├── BUGS.md         # 缺陷管理
│       └── CHANGELOG.md    # 变更日志
│
├── scripts/                 # 自动化脚本
│   ├── docgen.py           # 文档索引生成
│   ├── dag_check.py        # DAG 校验
│   ├── contract_compat_check.py  # 契约兼容性
│   ├── deps_manager.py     # 依赖管理
│   └── ...
│
├── tests/                   # 测试
│   └── <module>/
│
└── tools/                   # 工具契约
    └── <tool>/
        └── contract.json
```

---

## 核心功能

### 自动化工具链
```
make help                   # 查看所有命令
make dev_check              # 完整检查（CI 门禁）
make dag_check              # DAG 拓扑校验
make contract_compat_check  # 契约兼容性检查
make deps_check             # 依赖自动检测
make docgen                 # 更新文档索引
make rollback_check         # 回滚验证
```

### 模块化开发
- **一键初始化**：`make ai_begin MODULE=name`
- **8 个必备文档**：自动生成模板
- **测试脚手架**：自动创建测试结构
- **文档索引**：自动维护上下文

### 质量门禁
- ✅ DAG 无环检测
- ✅ 契约兼容性验证
- ✅ 数据库迁移成对检查
- ✅ 配置 Schema 校验
- ✅ 文档一致性检查
- ✅ 测试覆盖率要求

---

## 核心文档

### 必读文档
- [agent.md](agent.md) - **AI Agent 完整工作指南**（1350+ 行）
  - 开发流程（S0-S5）
  - 测试准则（Python/Vue/Go）
  - PR 规则
  - 代码审查流程（三粒度）
  - 命令与脚本

- [QUICK_START.md](QUICK_START.md) - **快速开始指南**
  - 5 分钟快速启动
  - 常用命令速查
  - AI Agent 使用流程
  - 故障排查

- [TEMPLATE_USAGE.md](TEMPLATE_USAGE.md) - **模板使用说明**
  - 如何基于模板创建项目
  - 需要修改的文件清单
  - 自定义配置指南

### 技术文档
- `docs/project/` - 项目级文档（PRD、架构、发布）
- `docs/process/` - 流程规范（约定、DoR/DoD、环境）
- `docs/db/` - 数据库规范（Schema、迁移）

---

## 使用场景

### 适合使用的项目
- AI Agent 辅助开发的项目
- 需要严格文档管理的企业项目
- 多模块、多团队协作项目
- 需要长期维护的系统
- 重视代码质量和可追溯性

### 不太适合
- 快速原型项目（文档开销较大）
- 单人短期项目
- 文档要求不高的项目

---

## 技术栈支持

### 已验证支持
- **Python** 3.7+（FastAPI/Flask/Django）
- **Vue/TypeScript**（Vite/Nuxt）
- **Go** 1.18+
- **数据库**：PostgreSQL, MySQL, MongoDB, Redis
- **任务队列**：Celery

### 扩展支持
- **C/C++**（CMake）
- **C#/.NET**
- **Rust**

---

## 贡献与反馈

### 问题反馈
- 发现 Bug：提交 Issue
- 功能建议：提交 Issue 或 PR

### 改进贡献
1. Fork 本仓库
2. 创建特性分支
3. 提交 PR（遵循 `agent.md` 中的 PR 规则）

---

## 许可证

见 [LICENSE](LICENSE) 文件

---

## 相关资源

- [改进实施摘要](docs/project/IMPLEMENTATION_SUMMARY.md)
- [示例模块](modules/example/)
- [测试示例](tests/example/)

---

**当前版本**: 1.0.0  
**最后更新**: 2025-11-04  
**维护者**: [在此填写]

---

## 下一步

按照以下顺序开始使用模板：

1. **首先**，阅读 [TEMPLATE_USAGE.md](TEMPLATE_USAGE.md) 了解如何使用模板。
2. **然后**，阅读 [QUICK_START.md](QUICK_START.md) 快速上手。
3. **接着**，阅读 [agent.md](agent.md) 了解完整开发流程。
4. **随后**，创建第一个模块：`make ai_begin MODULE=my_feature`。
5. **最后**，根据项目需求定制配置和文档。
