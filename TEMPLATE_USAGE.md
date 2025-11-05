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

#### 2. `.aicontext/project_onepager.md`
```
当前：目标：以最小成本，用大模型提升开发效率...
需要：你的项目一页综述

修改内容：
- 项目目标
- 成功指标
- 当前日期
```

#### 3. `docs/project/PRD_ONEPAGER.md`
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

#### 4. `docs/project/SYSTEM_BOUNDARY.md`
```
当前：空模板
需要：定义系统边界

必填项：
- 外部依赖
- 入口/出口
- 非功能需求
```

#### 5. `docs/process/ENV_SPEC.yaml`
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

#### 7. `docs/db/DB_SPEC.yaml`
```
当前：示例 runs 表
需要：你的数据库结构

根据项目需求定义：
- 表结构
- 索引
- PII 字段标记
```

#### 8. `flows/dag.yaml`
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
rm docs/project/IMPLEMENTATION_SUMMARY.md  # 模板实施记录
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
# docs/db/DB_SPEC.yaml
defaults:
  primary: postgresql
  version: "16"
  vector: true  # 如需 pgvector
```

#### MySQL
```
# docs/db/DB_SPEC.yaml
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
# docs/db/DB_SPEC.yaml
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
mkdir -p docs/api
echo "# API 文档" > docs/api/README.md

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

## 检查清单

### 项目初始化清单

```markdown
- [ ] README.md 已更新为项目说明
- [ ] .aicontext/project_onepager.md 已填写
- [ ] docs/project/PRD_ONEPAGER.md 已完成
- [ ] docs/project/SYSTEM_BOUNDARY.md 已定义
- [ ] docs/process/ENV_SPEC.yaml 匹配技术栈
- [ ] config/*.yaml 已配置
- [ ] docs/db/DB_SPEC.yaml 已定义
- [ ] flows/dag.yaml 已更新
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
**A**: 可以。删除 `flows/dag.yaml`，并在 `Makefile` 的 `dev_check` 中移除 `dag_check`。

### Q4: 如何添加多语言支持？
**A**: 
1. 在 `docs/process/ENV_SPEC.yaml` 中添加语言配置。
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

