# 手动初始化操作清单

> **用途**: 提供详细的手动初始化步骤清单（不依赖AI辅助）
> **适用场景**: 熟悉模板结构，想完全自主控制初始化过程
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## 概述

### 适用人群
- 熟悉AI-TEMPLATE结构的开发者
- 想要完全控制初始化过程
- 希望深入理解模板机制
- 不依赖AI辅助

### 预计时间
- 最小化初始化：30分钟（清理+基础配置）
- 标准初始化：60分钟（+创建2-3个模块）
- 完整初始化：2-3小时（+数据库配置+测试数据）

---

## 准备工作

### 工具检查

```bash
# 必需工具
git --version        # >= 2.0
python --version     # >= 3.7
make --version       # GNU Make

# 可选工具（根据技术栈）
node --version       # 如有前端
go version           # 如使用Go
psql --version       # 如使用PostgreSQL
```

### 信息准备

在开始前，准备好以下信息：
- [ ] 项目名称（小写+连字符）
- [ ] 技术栈（Python/Go/TypeScript）
- [ ] 应用层结构（无/仅后端/完整）
- [ ] 计划的模块列表（3-5个）
- [ ] 数据库需求（有/无）

---

## 步骤1: 克隆与清理（5分钟）

### 1.1 克隆模板

```bash
# 克隆AI-TEMPLATE
git clone <AI-TEMPLATE-repo-url> <your-project-name>
cd <your-project-name>

# 或者：下载ZIP并解压
```

### 1.2 删除模板专用文件

```bash
# 删除temp/工作目录（模板开发用）
rm -rf temp/

# 删除模板使用说明
rm TEMPLATE_USAGE.md

# 删除模板的git历史（可选）
rm -rf .git/

# 检查清理结果
ls -la
```

**检查点**: 
- [ ] temp/目录已删除
- [ ] TEMPLATE_USAGE.md已删除

---

## 步骤2: 更新项目基本信息（10分钟）

### 2.1 更新README.md

编辑`README.md`，修改以下内容：

```markdown
# <项目名称>

<项目一句话描述>

---

## 声明

**本项目使用AI-TEMPLATE模板构建，编排系统和AI Agent请优先阅读`agent.md`。**

---

## 快速开始

<修改为项目的快速开始说明>

## 核心功能

- 功能1
- 功能2
- ...

## 技术栈

- <具体框架和版本>
```

### 2.2 更新agent.md

编辑`agent.md`的YAML Front Matter：

```yaml
---
spec_version: "1.0"
agent_id: "repo"
role: "<项目名称>的根编排配置"  # ← 修改这里

policies:
  goals_ref: /doc/policies/goals.md
  safety_ref: /doc/policies/safety.md
  roles_ref: /doc/policies/roles.md

# ... 其他保持不变
---
```

### 2.3 更新doc/policies/goals.md

编辑`doc/policies/goals.md`：

```markdown
# 全局目标

## 项目定位

**项目名称**: <your-project>
**核心目标**: <描述项目的主要目标>

## 关键指标

- 性能：<要求>
- 质量：<要求>
- 可维护性：<要求>
```

**检查点**:
- [ ] README.md已更新（项目名称、描述）
- [ ] agent.md已更新（role字段）
- [ ] goals.md已更新（项目定位）

---

## 步骤3: 选择应用层结构（5分钟）

### 3.1 决策

根据项目类型选择：

**选项A: 无应用层**（微服务、库项目）
```bash
# 无需创建，保持当前结构
```

**选项B: 仅后端应用层**（API服务）
```bash
mkdir -p app/routes
mkdir -p app/middleware
```

**选项C: 完整应用层**（全栈应用）
```bash
mkdir -p app/routes
mkdir -p app/middleware
mkdir -p frontend/pages
mkdir -p frontend/components
mkdir -p frontend/assets
```

### 3.2 创建应用层入口文件（如选B或C）

**app/routes/__init__.py**:
```python
"""应用路由注册"""
from fastapi import FastAPI

def register_routes(app: FastAPI):
    """注册所有模块的路由"""
    # 在这里注册模块路由
    # from modules.<entity>.api.routes import router as <entity>_router
    # app.include_router(<entity>_router, prefix="/api/<entity>")
    pass
```

**检查点**:
- [ ] 应用层目录已创建（如需要）
- [ ] 入口文件已创建

---

## 步骤4: 创建业务模块（每个10-15分钟）

### 4.1 使用脚本（推荐）

```bash
# 为每个模块执行
make ai_begin MODULE=<module-name>
```

脚本会自动创建：
- modules/<module>/agent.md
- modules/<module>/README.md
- modules/<module>/plan.md
- modules/<module>/doc/（6个文档）
- modules/<module>/core/
- tests/<module>/

### 4.2 手动创建（如不使用脚本）

```bash
MODULE=user

# 创建目录
mkdir -p modules/$MODULE/{core,doc}
mkdir -p tests/$MODULE

# 从模板复制文档
cp doc/modules/TEMPLATES/*.template modules/$MODULE/doc/
# 手动重命名去掉.template后缀

# 创建agent.md（从example复制并修改）
cp doc/modules/example/agent.md modules/$MODULE/agent.md
# 编辑modules/$MODULE/agent.md，修改：
#   - agent_id: "modules.<module>.v1"
#   - role: "<module>模块的业务逻辑Agent"
#   - ownership.code_paths
#   - 其他字段

# 创建README.md
vi modules/$MODULE/README.md

# 创建plan.md
vi modules/$MODULE/plan.md
```

### 4.3 模块信息清单

为每个模块准备：
- [ ] 模块名称（entity）
- [ ] 模块类型（1_Assign / 2_Select / ...）
- [ ] 模块层级（1-4级）
- [ ] 是否需要api/子目录
- [ ] 是否需要frontend/子目录
- [ ] 输入输出定义
- [ ] 依赖关系

**检查点**（每个模块）:
- [ ] agent.md已创建并正确配置
- [ ] README.md已创建
- [ ] doc/下6个文档已创建
- [ ] core/目录已创建

---

## 步骤5: 配置数据库（如需要，15-30分钟）

### 5.1 确定数据库表

列出项目需要的所有表：
- [ ] <table1> - <用途>
- [ ] <table2> - <用途>
- [ ] ...

### 5.2 创建表YAML

为每个表创建：`db/engines/postgres/schemas/tables/<table>.yaml`

**参考**: `db/engines/postgres/schemas/tables/runs.yaml`

```bash
# 从示例复制
cp db/engines/postgres/schemas/tables/runs.yaml \
   db/engines/postgres/schemas/tables/<table>.yaml

# 编辑
vi db/engines/postgres/schemas/tables/<table>.yaml
```

### 5.3 创建迁移脚本

```bash
# 确定编号
NEXT_NUM=$(printf "%03d" $(($(ls db/engines/postgres/migrations/*_up.sql | wc -l) + 1)))

# 创建UP脚本
vi db/engines/postgres/migrations/${NEXT_NUM}_<module>_create_<table>_up.sql

# 创建DOWN脚本
vi db/engines/postgres/migrations/${NEXT_NUM}_<module>_create_<table>_down.sql
```

**参考**: `db/engines/postgres/migrations/001_example_create_runs_table_up.sql`

### 5.4 校验

```bash
make db_lint
```

**检查点**:
- [ ] 所有表YAML已创建
- [ ] 所有迁移脚本已创建（成对的up/down）
- [ ] make db_lint通过

---

## 步骤6: 生成模块注册表（5-10分钟）

### 6.1 自动生成草案

```bash
make registry_gen
```

生成文件：`doc/orchestration/registry.yaml.draft`

### 6.2 审核和补充

```bash
vi doc/orchestration/registry.yaml.draft
```

补充TODO标记的内容：
- [ ] 模块描述
- [ ] 版本号
- [ ] 责任人
- [ ] 依赖关系

### 6.3 正式化

```bash
# 确认无误后
mv doc/orchestration/registry.yaml.draft \
   doc/orchestration/registry.yaml
```

### 6.4 校验

```bash
make registry_check
```

**检查点**:
- [ ] registry.yaml已生成
- [ ] 所有TODO已补充
- [ ] make registry_check通过

---

## 步骤7: 运行完整校验（5-10分钟）

### 7.1 运行所有校验

```bash
# Schema校验
make agent_lint          # 校验agent.md

# 编排校验
make registry_check      # 校验registry.yaml
make doc_route_check     # 校验文档路由

# 类型校验
make type_contract_check # 校验模块契约

# 数据库校验
make db_lint             # 校验数据库文件

# 文档同步
make doc_script_sync_check

# 聚合验证
make validate            # 运行所有检查
```

### 7.2 检查清单

- [ ] make agent_lint: PASS
- [ ] make registry_check: PASS
- [ ] make doc_route_check: PASS
- [ ] make type_contract_check: PASS
- [ ] make db_lint: PASS（如有数据库）
- [ ] make doc_script_sync_check: PASS

### 7.3 修复问题

如有错误：
1. 查看错误信息
2. 修复文件
3. 重新运行校验
4. 重复直到全部通过

---

## 步骤8: 配置依赖（10-20分钟）

### 8.1 Python依赖（如使用Python）

编辑`requirements.txt`：

```
# Web框架
fastapi>=0.100.0
uvicorn>=0.23.0

# ORM
sqlalchemy>=2.0.0
alembic>=1.12.0

# 工具
pyyaml>=6.0
pydantic>=2.0.0

# 测试
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-asyncio>=0.21.0

# 项目特定依赖
# <添加其他依赖>
```

### 8.2 前端依赖（如使用前端）

创建`frontend/package.json`：

```json
{
  "name": "<project-name>-frontend",
  "version": "0.1.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.5.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "typescript": "^5.0.0",
    "vite": "^4.5.0"
  }
}
```

### 8.3 安装依赖

```bash
# Python
pip install -r requirements.txt

# 前端（如有）
cd frontend && npm install
```

**检查点**:
- [ ] requirements.txt已更新
- [ ] package.json已创建（如需要）
- [ ] 依赖已安装

---

## 步骤9: 清理模板痕迹（5分钟）

### 9.1 删除示例模块（可选）

```bash
# 如果不需要example作为参考
rm -rf doc/modules/example/
```

### 9.2 删除.git历史（可选）

```bash
rm -rf .git/
git init
git add .
git commit -m "Initial commit from AI-TEMPLATE"
```

### 9.3 配置git

```bash
git config user.name "<Your Name>"
git config user.email "<your@email.com>"

# 创建.gitignore（如需要补充）
cat >> .gitignore <<EOF
# 项目特定忽略
*.pyc
__pycache__/
.env
.venv/
node_modules/
dist/
EOF
```

**检查点**:
- [ ] 不需要的文件已删除
- [ ] git已初始化（如需要）
- [ ] .gitignore已配置

---

## 步骤10: 初始化测试（10-20分钟）

### 10.1 运行测试

```bash
# 运行所有测试
pytest tests/

# 检查覆盖率
pytest --cov=modules tests/
```

### 10.2 启动开发服务器

```bash
# Python/FastAPI
uvicorn app.main:app --reload

# 或使用Makefile命令
make dev
```

### 10.3 手动验证

- [ ] 服务可以启动
- [ ] 基础API可以访问
- [ ] 没有明显错误

---

## 可选步骤

### 配置CI/CD

编辑`.github/workflows/ci.yml`（如使用GitHub）：

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run validation
        run: make validate
      - name: Run tests
        run: pytest tests/
```

### 配置Docker

编辑`docker-compose.yml`：

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...
```

### 配置环境变量

创建`.env.example`：

```bash
# 数据库
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# 认证
JWT_SECRET=your-secret-key

# 其他配置
DEBUG=true
```

---

## 完整检查清单

### 最终验收

- [ ] **项目信息**
  - [ ] README.md已更新
  - [ ] agent.md已更新
  - [ ] goals.md已更新

- [ ] **应用层**
  - [ ] app/目录已创建（如需要）
  - [ ] frontend/目录已创建（如需要）

- [ ] **业务模块**
  - [ ] 所有模块目录已创建
  - [ ] 每个模块有agent.md + README.md
  - [ ] 每个模块有doc/下6个文档

- [ ] **数据库**（如需要）
  - [ ] 表YAML已创建
  - [ ] 迁移脚本已创建（成对）
  - [ ] make db_lint通过

- [ ] **编排配置**
  - [ ] registry.yaml已生成并审核
  - [ ] make registry_check通过

- [ ] **校验通过**
  - [ ] make agent_lint: PASS
  - [ ] make registry_check: PASS
  - [ ] make doc_route_check: PASS
  - [ ] make type_contract_check: PASS
  - [ ] make validate: ALL PASS

- [ ] **依赖安装**
  - [ ] requirements.txt已安装
  - [ ] npm packages已安装（如需要）

- [ ] **测试验证**
  - [ ] pytest tests/: PASS
  - [ ] 服务可以启动
  - [ ] 基础功能可用

- [ ] **清理完成**
  - [ ] temp/已删除
  - [ ] TEMPLATE_USAGE.md已删除
  - [ ] example模块已删除（如不需要）
  - [ ] git已初始化（如需要）

---

## 常见问题

### Q1: 必须创建模块吗？

**A**: 不是必须的。如果是简单项目，可以只用common/和app/。但建议至少创建1个模块以保持结构清晰。

### Q2: 可以保留example模块吗？

**A**: 可以。example模块在doc/modules/example/，可以作为开发参考。如果觉得混乱，也可以删除。

### Q3: 手动初始化比AI辅助快吗？

**A**: 
- 如果熟悉模板：手动可能更快（30分钟）
- 如果不熟悉：AI辅助更快（有引导）
- 如果想学习：手动初始化是好方式

### Q4: 可以跳过某些步骤吗？

**A**: 
- 必须：步骤1、2、4、6、7（核心流程）
- 可选：步骤3（如无应用层）、步骤5（如无数据库）、步骤8、9、10

### Q5: 初始化后发现问题怎么办？

**A**: 
- 查看错误信息（make validate输出）
- 参考example模块（doc/modules/example/）
- 查看相关指南（MODULE_INIT_GUIDE.md等）
- 重新运行校验直到通过

---

## 下一步

初始化完成后：

1. **开始开发**
   - 实现modules/<entity>/core/中的业务逻辑
   - 补充测试

2. **添加新模块**
   - 使用`make ai_begin MODULE=<name>`
   - 或参考MODULE_INIT_GUIDE.md手动创建

3. **数据库变更**
   - 参考doc/process/DB_CHANGE_GUIDE.md
   - 在plan.md中标记

4. **持续维护**
   - 更新CHANGELOG.md
   - 更新registry.yaml
   - 运行make validate

---

## 相关文档

- **AI辅助初始化**: doc/init/PROJECT_INIT_GUIDE.md（方式1、2、4）
- **模块初始化**: doc/modules/MODULE_INIT_GUIDE.md
- **数据库变更**: doc/process/DB_CHANGE_GUIDE.md
- **参考示例**: doc/modules/example/

---

## 版本历史

- 2025-11-07: v1.0 创建手动初始化清单（Phase 6.5）

---

**维护责任**: 项目维护者
**更新频率**: 流程变更时更新

