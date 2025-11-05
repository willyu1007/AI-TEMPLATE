# 快速开始指南

## 5 分钟快速启动

### 1. 安装依赖
```bash
# Python 依赖（推荐）
pip install -r requirements.txt

# 或者只安装核心依赖
pip install pyyaml

# 自动检测并补全依赖（可选）
make deps_check
```

### 2. 初始化项目
```bash
# 生成文档索引
make docgen

# 运行完整检查
make dev_check

# 初始化契约基线
make update_baselines
```

### 3. 创建第一个模块
```bash
# 初始化模块（自动生成所有文档和测试）
make ai_begin MODULE=my_feature

# 查看生成的文件
ls -la modules/my_feature/
ls -la tests/my_feature/
```

### 4. 开发流程
```bash
# 1. 编辑计划
vim modules/my_feature/plan.md

# 2. 实现功能
# ... 编写代码 ...

# 3. 运行检查
make dev_check

# 4. 提交前最后验证
make rollback_check PREV_REF=main
```

## 常用命令速查

### 开发检查
```bash
make dev_check              # 完整检查（CI 门禁）
make quick_check            # 快速检查（跳过慢速检查）
make dag_check              # 仅检查 DAG
make consistency_check      # 仅检查一致性
```

### 模块管理
```bash
make ai_begin MODULE=<name>     # 初始化新模块
make tests_scaffold MODULE=<name>  # 生成测试脚手架
```

### 契约管理
```bash
make contract_compat_check  # 检查契约兼容性
make update_baselines       # 更新契约基线
```

### 配置与迁移
```bash
make runtime_config_check   # 检查配置
make migrate_check          # 检查迁移脚本
```

### 文档与索引
```bash
make docgen                 # 生成/更新文档索引
make deps_check             # 检查并自动补全依赖
```

### 回滚验证
```bash
make rollback_check PREV_REF=v1.0.0  # 验证可回滚到指定版本
```

## AI Agent 使用流程

### 作为 AI Agent，每次任务遵循：

#### S0 - 刷新上下文（分层加载）
```bash
# Tier-0（必须）
cat .aicontext/snapshot.json
cat .aicontext/module_index.json

# Tier-1（强烈建议）
cat flows/dag.yaml
cat modules/<target>/plan.md
cat modules/<target>/README.md

# Tier-2（建议）
cat docs/db/DB_SPEC.yaml
cat docs/process/ENV_SPEC.yaml

# Tier-3（按需）
cat modules/<target>/TEST_PLAN.md
```

#### S1 - 任务建模
```bash
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
```bash
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
```bash
# 实现功能
# ... 编写代码 ...

# 更新测试
# ... 编写测试 ...

# 运行验证
make dev_check
```

#### S4 - 文档与索引更新
```bash
# 同步更新文档
vim modules/<target>/CONTRACT.md
vim modules/<target>/TEST_PLAN.md
vim modules/<target>/RUNBOOK.md
vim modules/<target>/PROGRESS.md
vim modules/<target>/CHANGELOG.md

# 如涉及 DAG/契约/配置
vim flows/dag.yaml
vim tools/*/contract.json
vim config/*.yaml
vim docs/process/CONFIG_GUIDE.md

# 刷新索引
make docgen
```

#### S5 - 自审与 PR
```bash
# 生成实施自审
vim ai/sessions/$(date +%Y%m%d)_<name>/AI-SR-impl.md

# 最后检查
make dev_check

# 回滚验证（高风险变更）
make rollback_check PREV_REF=<previous-tag>

# 创建 PR（附上 plan 和 AI-SR）
```

## 目录结构速查

```
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
├── docs/                    # 文档
│   ├── project/             # 项目文档
│   ├── process/             # 流程文档
│   ├── db/                  # 数据库文档
│   ├── flows/               # 流程图
│   └── ux/                  # UX 文档
├── flows/
│   └── dag.yaml             # DAG 配置
├── migrations/              # 数据库迁移
├── modules/                 # 业务模块
│   └── <module>/
│       ├── README.md        # 模块概述
│       ├── plan.md          # 任务计划
│       ├── CONTRACT.md      # 接口契约
│       ├── TEST_PLAN.md     # 测试计划
│       ├── RUNBOOK.md       # 运维手册
│       ├── PROGRESS.md      # 进度跟踪
│       ├── BUGS.md          # 缺陷管理
│       └── CHANGELOG.md     # 变更日志
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
│   └── validate.sh          # 聚合验证
├── tests/                   # 测试
├── tools/                   # 工具/服务契约
│   └── codegen/
│       └── contract.json
├── agent.md                 # AI Agent 工作指南
├── Makefile                 # 命令入口
├── requirements.txt         # Python 依赖
└── README.md                # 项目说明
```

## 最佳实践

### 1. 始终保持索引最新
```bash
# 每次修改文档后
make docgen
```

### 2. 提交前运行完整检查
```bash
make dev_check
```

### 3. 契约变更需验证兼容性
```bash
make contract_compat_check
# 通过后更新基线
make update_baselines
```

### 4. 高风险变更需回滚验证
```bash
make rollback_check PREV_REF=v1.0.0
```

### 5. 遵循文档边界
- `plan.md` = 未来计划
- `PROGRESS.md` = 历史记录

## 故障排查

### 问题：`make dev_check` 失败

#### 1. snapshot_hash 不一致
```bash
# 解决：重新生成索引
make docgen
```

#### 2. 模块文档缺失
```bash
# 解决：补齐文档或使用模板初始化
make ai_begin MODULE=<module>
```

#### 3. DAG 有环
```bash
# 解决：检查 flows/dag.yaml，移除循环依赖
vim flows/dag.yaml
make dag_check
```

#### 4. 契约不兼容
```bash
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

- **详细指南**：`agent.md`
- **改进方案**：`Agent-Repo-QA-Mapping.md`
- **实施摘要**：`docs/project/IMPLEMENTATION_SUMMARY.md`
- **示例模块**：`modules/example/`

## 提示

1. 使用 `make help` 查看所有可用命令
2. 参考 `modules/example/` 了解文档最佳实践
3. 使用 `make quick_check` 进行快速验证
4. 生产部署前务必运行 `make rollback_check`
5. 使用 `make deps_check` 自动检测并补全项目依赖

## 依赖管理说明

### Python 项目
```bash
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

