# 项目迁移指南

> **用途**: 指导将现有项目迁移到AI-TEMPLATE架构
> **适用场景**: 有现有项目需要升级架构、采用模块化开发
> **执行方式**: AI辅助（推荐）或手动执行
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## 概述

### 什么是项目迁移

将一个现有项目（任意架构）迁移到AI-TEMPLATE的模块化架构：
- 输入：现有项目代码、架构文档
- 过程：分析→映射→迁移→验证
- 输出：符合AI-TEMPLATE规范的项目结构

### 与项目初始化的区别

| 维度 | 项目初始化 | 项目迁移 |
|------|-----------|---------|
| 起点 | 空白 | 现有代码 |
| 难度 | 简单 | 中等-困难 |
| 耗时 | 15-60分钟 | 1-8小时 |
| 风险 | 低 | 中-高 |
| 测试 | 新功能测试 | 功能等价验证 |

---

## 前置条件

### 项目要求
- [ ] 有明确的项目代码（本地或Git仓库）
- [ ] 代码质量基本可控（可编译/运行）
- [ ] 有README或文档说明项目功能
- [ ] 愿意调整项目结构

### 工具要求
- [ ] Git（版本控制）
- [ ] Python/Go/Node（根据技术栈）
- [ ] make（运行校验命令）
- [ ] 测试框架（pytest/go test/jest）

### 时间预算

| 项目规模 | 预计时间 | 建议策略 |
|---------|---------|---------|
| 小型（<5000行） | 1-2小时 | 策略A（直接复制） |
| 中型（5000-20000行） | 2-4小时 | 策略B（AI重新实现） |
| 大型（>20000行） | 4-8小时 | 策略C（仅骨架+手动） |

---

## 迁移流程总览

```
Step 1: 分析现有项目（识别结构、模块、依赖）
  ↓
Step 2: 架构映射（旧结构→新结构）
  ↓
Step 3: 选择迁移策略（A/B/C）
  ↓
Step 4: 执行迁移（创建目录、迁移代码）
  ↓
Step 5: 生成文档和配置（agent.md、registry.yaml）
  ↓
Step 6: 迁移数据库（表YAML、迁移脚本）
  ↓
Step 7: 迁移测试（适配新结构）
  ↓
Step 8: 验证与修复（校验、测试、修复问题）
  ↓
Step 9: 清理与提交（删除旧文件、git commit）
```

---

## Step 1: 分析现有项目（15-30分钟）

### 1.1 AI引导对话

```
AI: 我将帮助您将现有项目迁移到AI-TEMPLATE架构。

首先，请提供以下信息：

1. 现有项目的位置？
   - 本地路径（如：/Users/xxx/my-project）
   - GitHub链接（如：github.com/user/repo）
   
   用户: [提供路径]

AI: 正在分析项目...
    [扫描目录、识别文件类型、统计代码量]
    
    分析完成！
```

### 1.2 项目信息识别

```
AI: 项目分析报告：

基本信息：
- 项目名称：<识别或推测>
- 技术栈：<语言和框架>
- 代码规模：<总行数>
- Git历史：<commits数量>

目录结构：
<当前目录树状图>

识别的组件/模块：
1. <component1>
   - 路径：<path>
   - 功能：<推测>
   - 代码量：<lines>
   
2. <component2>
   - 路径：<path>
   - 功能：<推测>
   - 代码量：<lines>

依赖关系：
<识别的依赖图>

数据库：
- 类型：<识别>
- 表数量：<N>
- 主要表：<tables>

测试覆盖：
- 测试文件：<N>个
- 覆盖率：<百分比>（如可识别）

2. 以上识别是否准确？请补充或修正：
   用户: [确认/修正]

3. 是否有架构文档、README、或PRD可以提供？
   这将帮助我更准确地理解项目。
   
   用户: [上传文档/没有]

[如上传文档]

AI: 正在分析文档...
    结合代码和文档，我现在对项目有了更清晰的理解。
```

### 1.3 确认迁移范围

```
AI: 请确认迁移范围：

要迁移的内容：
- [ ] 核心业务代码
- [ ] API/路由层
- [ ] 数据库模型/表结构
- [ ] 测试代码
- [ ] 前端代码（如有）
- [ ] 配置文件
- [ ] 文档

不迁移的内容：
- [ ] 旧的构建脚本
- [ ] 临时文件/缓存
- [ ] 旧的文档（将生成新文档）
- [ ] <其他>

用户: [确认/调整]
```

---

## Step 2: 架构映射（10-20分钟）

### 2.1 目录映射

```
AI: 我建议以下目录映射方案：

📐 目录映射表：

旧路径 → 新路径 | 映射类型 | 操作
───────────────────────────────────────
/src/users/              | 模块 | 
  → /modules/user/core/  | 核心业务 | 复制+调整
  
/src/api/users.py        | API | 
  → /modules/user/api/routes.py | HTTP接口 | 复制+调整
  
/src/models/user.py      | 数据模型 |
  → /modules/user/models/schemas.py | Pydantic | 复制+调整
  
/db/migrations/          | 迁移脚本 |
  → /db/engines/postgres/migrations/ | SQL | 复制
  
/tests/test_users.py     | 测试 |
  → /tests/user/test_service.py | 单元测试 | 复制+调整
  
/frontend/UserProfile.tsx | 前端 |
  → /modules/user/frontend/components/ | 组件 | 复制

/src/common/             | 公共层 |
  → /common/             | 公共工具 | 复制
  
/config/                 | 配置 |
  → /config/             | 配置 | 保留

请确认映射是否合理？

用户: [确认/调整]
```

### 2.2 模块划分

```
AI: 基于识别的组件，我建议以下模块划分：

模块划分方案：

模块名 | 模块类型 | 层级 | 包含内容 | 说明
──────────────────────────────────────────────
user   | 1_Assign | 1 | 用户注册、登录、权限 | 独立模块
order  | 1_Assign | 1 | 订单创建、查询、管理 | 独立模块  
product| 1_Assign | 1 | 商品管理、库存 | 独立模块
payment| 2_Select | 2 | 支付方式选择 | user的子模块
notification | 1_Assign | 1 | 通知发送 | 独立模块

模块关系：
- user → payment（用户选择支付方式）
- order → payment（订单关联支付）
- order → product（订单包含商品）

这个划分是否合理？

用户: [确认/调整]
```

### 2.3 数据库映射

```
AI: 数据库表映射方案：

表名 | 归属模块 | 操作 | 说明
────────────────────────────────────
users | user | 保留+生成YAML | 用户基础信息
user_profiles | user | 保留+生成YAML | 用户扩展信息
orders | order | 保留+生成YAML | 订单信息
order_items | order | 保留+生成YAML | 订单明细
products | product | 保留+生成YAML | 商品信息
payments | order | 保留+生成YAML | 支付记录

迁移操作：
1. 为每个表生成YAML（db/engines/postgres/schemas/tables/*.yaml）
2. 复制现有迁移脚本到db/engines/postgres/migrations/
3. 重新编号迁移脚本（保持顺序）

用户: [确认]
```

---

## Step 3: 选择迁移策略（5分钟）

### 策略对比

| 维度 | 策略A：直接复制 | 策略B：AI重新实现 | 策略C：仅骨架 |
|------|---------------|-----------------|-------------|
| 速度 | 快（30-60分钟） | 中（2-4小时） | 慢（1-3小时+手动） |
| 代码质量 | 保持原样 | 提升 | 取决于手动实现 |
| 风险 | 低 | 中 | 低 |
| 测试工作量 | 小 | 大 | 中 |
| 适用场景 | 代码质量好 | 想要重构 | 代码复杂 |

### AI建议

```
AI: 基于项目分析，我的建议：

项目规模：<small/medium/large>
代码质量：<good/fair/poor>
复杂度：<low/medium/high>

建议策略：<A/B/C>
理由：<说明>

您想使用哪种策略？

用户: [选择A/B/C]

AI: 好的，我将使用策略<X>执行迁移...
```

---

## Step 4: 执行迁移（30分钟-4小时）

### 策略A: 直接复制

#### 4A.1 创建新结构

```bash
# 克隆AI-TEMPLATE到新目录
git clone <AI-TEMPLATE> <project-name>-new
cd <project-name>-new

# 删除模板专用文件
rm -rf temp/ TEMPLATE_USAGE.md
```

#### 4A.2 复制代码文件

```bash
# AI执行（或手动）
# 用户模块
cp -r <old-project>/src/users/* modules/user/core/

# 订单模块
cp -r <old-project>/src/orders/* modules/order/core/

# 公共层
cp -r <old-project>/src/common/* common/

# 测试
cp -r <old-project>/tests/test_users* tests/user/
```

#### 4A.3 批量调整import路径

**AI自动执行** 或 **手动替换**：

```bash
# 示例：Python项目
# 旧：from src.users.service import UserService
# 新：from modules.user.core.service import UserService

find modules/ -name "*.py" -type f -exec sed -i 's/from src\./from modules./g' {} \;
find modules/ -name "*.py" -type f -exec sed -i 's/import src\./import modules./g' {} \;
```

**常见import调整**:

| 旧import | 新import |
|---------|---------|
| `from src.users` | `from modules.user.core` |
| `from models.user` | `from modules.user.models` |
| `from api.routes` | `from app.routes` |
| `from common` | `from common` (保持不变) |

#### 4A.4 调整配置文件

```bash
# 更新requirements.txt
cat <old-project>/requirements.txt >> requirements.txt

# 去重
sort -u requirements.txt -o requirements.txt

# 更新配置路径
vi config/*.yaml
# 调整路径引用
```

---

### 策略B: AI重新实现

#### 4B.1 逐模块重新实现

```
AI: 开始重新实现项目（策略B）...

我将按模块逐个重新实现，确保功能等价。

[模块 1/N] user模块

Step 1: 读取旧代码
  - 正在阅读：src/users/service.py
  - 正在阅读：src/users/models.py
  - 正在阅读：src/api/users.py

Step 2: 理解业务逻辑
  识别的功能：
  - 用户注册（register）
  - 用户登录（login）
  - 密码重置（reset_password）
  - 权限检查（check_permission）

Step 3: 按新架构实现
  - 创建：modules/user/core/service.py
  - 创建：modules/user/models/schemas.py
  - 创建：modules/user/api/routes.py

Step 4: 生成测试
  - 创建：tests/user/test_service.py
  - 覆盖所有功能点

Step 5: 验证功能等价
  - 运行测试：pytest tests/user/
  - 对比行为：✅ 功能一致

✅ user模块重新实现完成

用户: [确认继续下一模块/暂停调整]

[继续下一模块...]
```

#### 4B.2 保持API兼容性

**原则**: 保持外部接口不变，内部实现可优化

```python
# 旧代码
@app.post("/api/users/register")
def register_user(username: str, password: str):
    # 旧的实现
    pass

# 新代码 - 保持接口一致
# modules/user/api/routes.py
from fastapi import APIRouter
router = APIRouter()

@router.post("/register")  # app.include_router(router, prefix="/api/users")
async def register_user(username: str, password: str):
    # 新的实现（可能更好）
    service = UserService()
    return await service.register(username, password)
```

---

### 策略C: 仅骨架

#### 4C.1 生成完整骨架

```
AI: 开始生成骨架（策略C）...

[1/4] 创建目录结构
  ✅ modules/user/{core,api,models,doc}/
  ✅ modules/order/{core,api,models,doc}/
  ✅ modules/product/{core,api,models,doc}/

[2/4] 生成文档
  ✅ 每个模块的agent.md、README.md、doc/*
  ✅ registry.yaml

[3/4] 生成代码框架
  ✅ modules/user/core/service.py（空函数签名）
  ✅ modules/user/api/routes.py（空路由）
  ✅ modules/user/models/schemas.py（空模型）

[4/4] 生成测试框架
  ✅ tests/user/（空测试文件）

骨架生成完成！

接下来请您手动迁移代码。参考下方的手动迁移清单。

用户: [开始手动迁移]
```

#### 4C.2 手动迁移清单

**每个模块执行**:

1. **复制核心业务逻辑**
   ```bash
   # 将旧代码复制到modules/<entity>/core/
   cp <old-project>/src/<entity>/*.py modules/<entity>/core/
   ```

2. **调整import**
   ```bash
   # 打开每个文件，手动调整import语句
   vi modules/<entity>/core/*.py
   ```

3. **复制API层（如有）**
   ```bash
   cp <old-project>/api/<entity>*.py modules/<entity>/api/
   # 调整import和路由注册
   ```

4. **复制模型定义（如有）**
   ```bash
   cp <old-project>/models/<entity>*.py modules/<entity>/models/
   ```

5. **运行测试验证**
   ```bash
   pytest tests/<entity>/
   ```

6. **重复1-5**，直到所有模块完成

---

## Step 5: 生成文档和配置（30-60分钟）

### 5.1 生成agent.md

为每个模块创建agent.md（从example复制）：

```bash
# 为user模块
cp doc/modules/example/agent.md modules/user/agent.md

# 编辑，修改：
vi modules/user/agent.md
# - agent_id: "modules.user.v1"
# - role: "user模块的业务逻辑Agent"
# - ownership.code_paths: ["modules/user/", "tests/user/"]
# - io.inputs/outputs（根据实际接口）
# - dependencies（根据实际依赖）
```

### 5.2 生成README.md

为每个模块创建README.md：

```bash
# 从TEMPLATES复制
cp doc/modules/TEMPLATES/README.md.template modules/user/README.md

# 编辑填写
vi modules/user/README.md
# - 模块名称
# - 职责描述
# - 目录结构
# - 核心功能
# - API接口（如有）
# - 依赖关系
```

### 5.3 生成registry.yaml

```bash
# 自动生成草案
make registry_gen

# 审核并补充
vi doc/orchestration/registry.yaml.draft

# 补充信息：
# - 模块描述
# - 版本号
# - 责任人
# - 依赖关系

# 正式化
mv doc/orchestration/registry.yaml.draft \
   doc/orchestration/registry.yaml
```

---

## Step 6: 迁移数据库（30-60分钟）

### 6.1 分析现有数据库

**识别表结构**:

```sql
-- 如有现有数据库
psql -U postgres -d <old_db> -c "\dt"    # 列出所有表
psql -U postgres -d <old_db> -c "\d <table_name>"  # 查看表结构
```

**识别迁移脚本**（如有）:

```bash
# 查找现有迁移脚本
find <old-project> -name "*migration*" -o -name "*migrate*"
```

### 6.2 生成表YAML

为每个表生成YAML：

```bash
# 手动创建（参考runs.yaml）
vi db/engines/postgres/schemas/tables/<table>.yaml
```

**或AI辅助**:

```
AI: 我已识别表：users、orders、products

为users表生成YAML：

[显示生成的YAML]

请确认表结构是否正确？

用户: [确认/修改]

AI: 好的，已创建：
    db/engines/postgres/schemas/tables/users.yaml
    
    [继续下一个表...]
```

### 6.3 迁移和重新编号迁移脚本

```bash
# 复制旧的迁移脚本
cp <old-project>/db/migrations/* \
   db/engines/postgres/migrations/

# 重新编号（保持时间顺序）
cd db/engines/postgres/migrations/
ls -lt *.sql  # 查看按时间排序

# 重命名
mv old_001_create_users.sql 001_user_create_users_up.sql
mv old_001_rollback_users.sql 001_user_create_users_down.sql
# ... 依次重命名
```

### 6.4 校验

```bash
make db_lint
```

---

## Step 7: 迁移测试（30-60分钟）

### 7.1 调整测试文件结构

```bash
# 旧结构
tests/
├── test_users.py
├── test_orders.py
└── test_products.py

# 新结构
tests/
├── user/
│   ├── test_service.py
│   └── test_api.py
├── order/
│   └── test_service.py
└── product/
    └── test_service.py
```

### 7.2 调整import路径

```python
# 旧import
from src.users.service import UserService

# 新import
from modules.user.core.service import UserService
```

### 7.3 调整Fixtures加载

```python
# 旧方式
@pytest.fixture
def user_data():
    # 内联数据
    return {"id": 1, "name": "test"}

# 新方式（使用Fixtures文件）
@pytest.fixture
def user_data():
    load_fixture("user", "minimal")
    yield
    cleanup_fixture()
```

### 7.4 运行测试

```bash
# 运行所有测试
pytest tests/

# 检查失败的测试
pytest tests/ --tb=short

# 修复并重新运行
```

---

## Step 8: 验证与修复（30-60分钟）

### 8.1 运行完整校验

```bash
# 运行所有校验
make validate

# 逐个检查
make agent_lint
make registry_check
make doc_route_check
make type_contract_check
make db_lint
make doc_script_sync_check
```

### 8.2 常见问题修复

**问题1: import错误**
```
ModuleNotFoundError: No module named 'src'
```
**解决**: 
- 全局搜索替换：`from src.` → `from modules.`
- 检查__init__.py文件是否存在

**问题2: 路径引用错误**
```
FileNotFoundError: config/settings.yaml
```
**解决**:
- 检查配置文件路径
- 更新代码中的路径引用

**问题3: agent.md校验失败**
```
[error] modules/user/agent.md: missing required field 'role'
```
**解决**:
- 检查YAML Front Matter完整性
- 参考example/agent.md

**问题4: 测试失败**
```
AssertionError: Expected 200, got 404
```
**解决**:
- 检查路由注册
- 检查API路径是否变更
- 更新测试用例

### 8.3 功能验证

```bash
# 启动服务
make dev

# 手动测试主要功能
curl http://localhost:8000/api/users/
curl http://localhost:8000/api/orders/

# 检查响应是否正确
```

---

## Step 9: 清理与提交（10分钟）

### 9.1 删除旧项目引用

```bash
# 删除旧的构建产物
rm -rf __pycache__/ *.pyc .pytest_cache/

# 删除旧的配置（如不需要）
rm -rf old_deploy/ legacy_scripts/
```

### 9.2 更新README.md

```markdown
# <项目名称>

<项目描述>

## 架构升级说明

本项目已从旧架构迁移到AI-TEMPLATE模块化架构。

### 主要变更
- 采用模块化结构（modules/）
- 统一的文档规范（agent.md + README.md）
- 标准化的数据库管理（db/engines/）
- 完整的校验体系（make validate）

### 迁移时间
- 迁移日期：<YYYY-MM-DD>
- 旧架构版本：<version>
- 新架构版本：AI-TEMPLATE v1.0
```

### 9.3 Git提交

```bash
# 初始化git（如需要）
rm -rf .git/
git init

# 添加所有文件
git add .

# 提交
git commit -m "Migrate to AI-TEMPLATE architecture

- Migrated <N> modules
- Restructured to modular architecture  
- Generated agent.md for all modules
- Updated database structure
- All validation passed
"

# 推送到远程（如需要）
git remote add origin <your-repo-url>
git push -u origin main
```

---

## 迁移后检查清单

### 代码完整性

- [ ] 所有模块代码已迁移
- [ ] 所有API路由已迁移
- [ ] 所有数据模型已迁移
- [ ] 所有测试已迁移
- [ ] 所有配置文件已迁移

### 功能验证

- [ ] 服务可以启动
- [ ] 所有API可以访问
- [ ] 主要功能正常工作
- [ ] 测试全部通过（或已知失败原因）

### 文档完整性

- [ ] 每个模块有agent.md
- [ ] 每个模块有README.md
- [ ] 每个模块有doc/下6个文档
- [ ] registry.yaml已生成并审核
- [ ] 项目README.md已更新

### 数据库完整性

- [ ] 所有表有YAML定义
- [ ] 所有迁移脚本已迁移
- [ ] 迁移脚本重新编号
- [ ] make db_lint通过

### 校验通过

- [ ] make agent_lint: PASS
- [ ] make registry_check: PASS
- [ ] make doc_route_check: PASS
- [ ] make db_lint: PASS
- [ ] make validate: ALL PASS

### 测试验证

- [ ] pytest tests/: PASS（或已知失败）
- [ ] 测试覆盖率：>= 60%（逐步提升）
- [ ] 手动功能测试：主流程通过

---

## 迁移策略最佳实践

### 渐进式迁移（推荐）

**适用**: 大型项目、线上运行的项目

**策略**:
1. 先迁移1-2个核心模块
2. 验证迁移后的模块功能正常
3. 新旧代码并存，逐步切换
4. 继续迁移其他模块
5. 最后删除旧代码

**优点**:
- 风险可控
- 随时可以回滚
- 可以边迁移边验证

### 一次性迁移

**适用**: 小型项目、测试项目

**策略**:
1. 一次性迁移所有代码
2. 集中修复问题
3. 完整验证

**优点**:
- 快速
- 没有新旧代码混合

### 重构式迁移

**适用**: 代码质量不佳、想要大幅重构

**策略**:
1. 使用策略B（AI重新实现）
2. 以旧代码为参考，重写业务逻辑
3. 提升代码质量、测试覆盖率
4. 可能需要更长时间

**优点**:
- 代码质量提升
- 架构更清晰
- 技术债务减少

---

## 常见问题

### Q1: 迁移过程中可以保留旧代码吗？

**A**: 可以。建议：
- 创建新目录（<project>-new）
- 迁移到新目录
- 保留旧目录作为参考
- 验证通过后删除旧目录

### Q2: import路径调整有自动化工具吗？

**A**: 
- Python: 可以使用sed批量替换（见策略A）
- 也可以使用IDE的重构功能（PyCharm、VSCode）
- 建议：先自动替换，再人工Review

### Q3: 测试失败怎么办？

**A**: 
1. 分析失败原因（import错误/逻辑错误/环境问题）
2. 先修复import错误
3. 再修复逻辑错误
4. 最后修复环境问题
5. 接受短期测试失败，逐步修复

### Q4: 数据库迁移脚本要重新执行吗？

**A**: 
- **开发环境**: 可以重新执行（创建新的test_db）
- **生产环境**: 保持现有数据库，只迁移脚本文件
- **注意**: 迁移脚本只是文件迁移，不影响数据

### Q5: 迁移后性能会变化吗？

**A**: 
- 架构调整不应影响性能
- 如使用策略B重新实现，性能可能更好
- 建议迁移后做性能测试对比

### Q6: 前端代码如何迁移？

**A**: 
- 如果前端在同一repo：迁移到frontend/或modules/<entity>/frontend/
- 如果前后端分离：前端独立repo，不迁移
- 注意：调整API调用路径（如有变化）

### Q7: 配置文件如何处理？

**A**:
- config/*.yaml：保留并更新路径引用
- .env：复制并检查环境变量名
- 部署配置：根据新结构调整

---

## 迁移后优化建议

### 短期优化（1-2周）

1. **补全文档**
   - 为所有模块补全doc/下的6个文档
   - 更新CONTRACT.md（API契约）
   - 更新CHANGELOG.md

2. **提升测试覆盖率**
   - 补充缺失的测试
   - 目标：>= 80%

3. **性能优化**
   - 添加必要的索引
   - 优化慢查询

### 中期优化（1-2个月）

1. **模块拆分优化**
   - 识别职责不清的模块
   - 拆分或合并模块

2. **测试数据管理**
   - 创建Fixtures（doc/TEST_DATA.md）
   - 定义Mock规则

3. **CI/CD集成**
   - 配置GitHub Actions
   - 自动运行make validate

### 长期优化（3-6个月）

1. **智能体编排**
   - 完善所有agent.md
   - 实现模块间自动调度

2. **性能监控**
   - 添加metrics和tracing
   - 性能基线建立

3. **文档完善**
   - 补充架构文档
   - 编写最佳实践

---

## 回滚计划

### 如果迁移失败

**保留旧项目**:
- 在迁移前备份整个项目
- 迁移到新目录而非原地修改
- 保留旧代码至少2周

**回滚步骤**:
1. 停止新架构服务
2. 切换到旧项目目录
3. 启动旧服务
4. 分析迁移失败原因
5. 修复后重新尝试

---

## 相关文档

- **项目初始化总指南**: doc/init/PROJECT_INIT_GUIDE.md
- **AI辅助迁移**: PROJECT_INIT_GUIDE.md（方式4）
- **模块初始化**: doc/modules/MODULE_INIT_GUIDE.md
- **数据库变更**: doc/process/DB_CHANGE_GUIDE.md
- **参考示例**: doc/modules/example/

---

## 版本历史

- 2025-11-07: v1.0 创建手动迁移清单（Phase 6.5）

---

**维护责任**: 项目维护者
**更新频率**: 流程变更时更新

