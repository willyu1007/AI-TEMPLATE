---
audience: human
language: zh
version: complete
purpose: Documentation for CONVENTIONS
---
# 开发约定

## 目标
规范团队开发流程，确保代码质量和可追溯性。

## 适用场景
- 团队协作开发
- AI Agent 辅助开发
- 需要严格代码审查的项目

## 前置条件
- 团队成员已阅读 `agent.md`
- Git 工作流已配置
- CI/CD 已就绪

## 核心约定

### 1. 分支策略
- **主分支模型**：Trunk-based Development
- **功能分支**：短生命周期（< 2天）
- **命名规范**：`feature/<name>`, `fix/<name>`, `hotfix/<name>`

### 2. Pull Request 要求
必须包含以下内容：
1. **AI-SR 文档**：自审文档（`ai/sessions/<date>_<name>/AI-SR-impl.md`）
2. **测试证明**：所有测试通过的截图或日志
3. **文档更新**：相关模块文档已同步更新

### 3. 代码审查
参考 `agent.md` §11 三粒度审查流程

---

## 编码规范

### 1. 命名约定

#### Python
```python
# ✅ 好
class UserService:
    def get_user_by_id(self, user_id: str) -> User:
        pass

# ❌ 不好
class userservice:
    def GetUserByID(self, userid: str) -> User:
        pass
```

**规则**:
- 类名：PascalCase
- 函数/方法名：snake_case
- 常量：UPPER_SNAKE_CASE
- 私有属性：_leading_underscore

#### TypeScript/JavaScript
```typescript
// ✅ 好
class UserService {
    getUserById(userId: string): User {
        return null;
    }
}

// ❌ 不好
class user_service {
    get_user_by_id(user_id: string): User {
        return null;
    }
}
```

**规则**:
- 类名：PascalCase
- 函数/方法名：camelCase
- 常量：UPPER_SNAKE_CASE
- 接口：PascalCase，可选I前缀

#### Go
```go
// ✅ 好
type UserService struct {}

func (s *UserService) GetUserByID(userID string) (*User, error) {
    return nil, nil
}

// ❌ 不好
type user_service struct {}

func (s *user_service) getUserById(userId string) (*User, error) {
    return nil, nil
}
```

**规则**:
- 导出类型：PascalCase（首字母大写）
- 非导出类型：camelCase（首字母小写）
- 函数/方法：PascalCase（导出）或camelCase（非导出）

---

### 2. 注释规范

#### 文件头注释
```python
"""
user_service.py - 用户服务模块

提供用户管理相关的核心业务逻辑。

Author: Team Name
Created: 2024-01-01
"""
```

#### 函数/方法注释
```python
def calculate_discount(price: float, user_level: int) -> float:
    """
    计算用户折扣价格
    
    Args:
        price: 商品原价
        user_level: 用户等级（1-5）
    
    Returns:
        折扣后价格
    
    Raises:
        ValueError: 当user_level不在1-5范围时
    """
    if not 1 <= user_level <= 5:
        raise ValueError("Invalid user level")
    return price * (1 - user_level * 0.1)
```

#### TODO注释
```python
# TODO(username): 添加缓存机制优化性能
# FIXME(username): 修复边界情况bug #123
# HACK(username): 临时解决方案，需要重构
# NOTE(username): 此处逻辑复杂，需要特别注意
```

---

### 3. 格式化规范

#### 缩进
- Python: 4空格
- JavaScript/TypeScript: 2空格
- Go: Tab
- YAML: 2空格

#### 行长度
- 最大行长: 120字符
- 注释行: 80字符
- 超长字符串: 可适当放宽

#### 空行
```python
# ✅ 好
class UserService:
    def __init__(self):
        self.users = {}
    
    def get_user(self, user_id: str) -> User:
        return self.users.get(user_id)
    
    def create_user(self, user: User) -> bool:
        if user.id in self.users:
            return False
        self.users[user.id] = user
        return True


# ❌ 不好
class UserService:
    def __init__(self):
        self.users = {}
    def get_user(self, user_id: str) -> User:
        return self.users.get(user_id)
    def create_user(self, user: User) -> bool:
        if user.id in self.users:
            return False
        self.users[user.id] = user
        return True
```

**规则**:
- 类/函数之间: 2个空行
- 方法之间: 1个空行
- 逻辑块之间: 1个空行

---

## 提交规范

### Commit Message格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type类型

| Type | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | feat(auth): 添加JWT认证 |
| fix | Bug修复 | fix(api): 修复用户查询500错误 |
| docs | 文档更新 | docs(readme): 更新安装说明 |
| style | 代码格式 | style(user): 修正缩进 |
| refactor | 重构 | refactor(db): 优化查询性能 |
| test | 测试相关 | test(user): 添加单元测试 |
| chore | 构建/工具 | chore(deps): 更新依赖版本 |

### 示例

```
feat(user): 添加用户注册功能

- 实现用户注册API
- 添加邮箱验证
- 添加密码强度检查

Closes #123
```

---

## 文档规范

### 1. README.md规范

每个模块必须包含README.md，结构如下：

```markdown
# 模块名称

> 一句话描述

## 功能概述
- 功能点1
- 功能点2

## 目录结构
...

## 快速开始
...

## API文档
...

## 测试
...
```

### 2. 文档风格

#### 标题层级
- 使用ATX风格（`#`符号）
- 最多4级标题
- 标题与内容间空一行

#### 列表
```markdown
✅ 好:
- 第一项
- 第二项
  - 子项1
  - 子项2

❌ 不好:
* 第一项
- 第二项
+ 第三项
```

#### 代码块
```markdown
✅ 好:
```python
def hello():
    print("Hello")
```

❌ 不好:
```
def hello():
    print("Hello")
```（没有语言标识）
```

---

## 测试规范

### 1. 测试覆盖率

| 代码类型 | 最低覆盖率 | 目标覆盖率 |
|---------|-----------|-----------|
| 核心业务逻辑 | 80% | 90%+ |
| API接口 | 70% | 85%+ |
| 工具函数 | 60% | 80%+ |
| UI组件 | 50% | 70%+ |

### 2. 测试类型

#### 单元测试
- 测试单个函数/方法
- 使用Mock隔离依赖
- 覆盖边界情况

```python
def test_calculate_discount():
    # 正常情况
    assert calculate_discount(100, 3) == 70
    
    # 边界情况
    assert calculate_discount(100, 1) == 90
    assert calculate_discount(100, 5) == 50
    
    # 异常情况
    with pytest.raises(ValueError):
        calculate_discount(100, 0)
    with pytest.raises(ValueError):
        calculate_discount(100, 6)
```

#### 集成测试
- 测试模块间交互
- 使用真实依赖或测试数据库
- 验证完整流程

#### E2E测试
- 测试完整用户场景
- 从UI到数据库的完整链路
- 关键功能必须覆盖

---

## 错误处理约定

### 1. 错误分类

```python
# 业务错误（预期内）
class BusinessError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message

# 系统错误（预期外）
class SystemError(Exception):
    pass

# 使用示例
if user.balance < amount:
    raise BusinessError("INSUFFICIENT_BALANCE", "余额不足")
```

### 2. 错误码规范

```
格式: <模块>_<类型>_<序号>

示例:
- USER_AUTH_001: 用户未登录
- USER_AUTH_002: 密码错误
- ORDER_PAYMENT_001: 支付失败
- ORDER_PAYMENT_002: 订单已支付
```

### 3. 错误处理

```python
# ✅ 好：具体的错误处理
try:
    user = get_user(user_id)
except UserNotFoundError:
    logger.warning(f"User not found: {user_id}")
    return None
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    raise

# ❌ 不好：捕获所有异常
try:
    user = get_user(user_id)
except Exception:
    pass
```

---

## 日志规范

### 1. 日志级别

| 级别 | 用途 | 示例 |
|------|------|------|
| DEBUG | 调试信息 | 变量值、函数调用 |
| INFO | 一般信息 | 请求开始、操作成功 |
| WARNING | 警告信息 | 重试操作、降级使用 |
| ERROR | 错误信息 | 操作失败、异常捕获 |
| CRITICAL | 严重错误 | 服务不可用、数据损坏 |

### 2. 日志格式

```python
# ✅ 好：结构化日志
logger.info(
    "User login successful",
    extra={
        "user_id": user.id,
        "ip": request.ip,
        "user_agent": request.user_agent
    }
)

# ❌ 不好：字符串拼接
logger.info(f"User {user.id} login from {request.ip}")
```

### 3. 敏感信息

```python
# ✅ 好：脱敏处理
logger.info(f"User phone: {mask_phone(user.phone)}")  # 138****5678

# ❌ 不好：直接记录
logger.info(f"User phone: {user.phone}")  # 13812345678
```

---

## API设计约定

### 1. RESTful API

```
资源命名：复数名词
✅ GET  /users
✅ GET  /users/:id
✅ POST /users
✅ PUT  /users/:id
✅ DELETE /users/:id

❌ GET /getUsers
❌ POST /createUser
```

### 2. 响应格式

```json
// 成功响应
{
    "code": 0,
    "message": "success",
    "data": {
        "id": "user-001",
        "name": "Alice"
    }
}

// 错误响应
{
    "code": "USER_NOT_FOUND",
    "message": "用户不存在",
    "data": null
}
```

### 3. HTTP状态码

| 状态码 | 含义 | 使用场景 |
|--------|------|---------|
| 200 | OK | 成功（GET/PUT/PATCH） |
| 201 | Created | 资源创建成功（POST） |
| 204 | No Content | 成功无返回（DELETE） |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证 |
| 403 | Forbidden | 无权限 |
| 404 | Not Found | 资源不存在 |
| 500 | Internal Server Error | 服务器错误 |

---

## 安全约定

### 1. 输入验证

```python
# ✅ 好：严格验证
def create_user(username: str, email: str):
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        raise ValueError("Invalid username")
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        raise ValueError("Invalid email")
    # 创建用户...

# ❌ 不好：无验证
def create_user(username: str, email: str):
    # 直接使用，可能有SQL注入风险
    db.execute(f"INSERT INTO users VALUES ('{username}', '{email}')")
```

### 2. 密码处理

```python
# ✅ 好：使用哈希
import hashlib
hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

# ❌ 不好：明文存储
db.save({"password": password})
```

### 3. SQL注入防护

```python
# ✅ 好：使用参数化查询
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ❌ 不好：字符串拼接
cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
```

---

## 性能约定

### 1. 数据库查询

```python
# ✅ 好：批量查询
user_ids = [1, 2, 3, 4, 5]
users = User.objects.filter(id__in=user_ids)

# ❌ 不好：循环查询（N+1问题）
users = []
for user_id in user_ids:
    users.append(User.objects.get(id=user_id))
```

### 2. 缓存使用

```python
# ✅ 好：使用缓存
def get_user(user_id: str) -> User:
    cache_key = f"user:{user_id}"
    user = cache.get(cache_key)
    if user is None:
        user = db.get_user(user_id)
        cache.set(cache_key, user, timeout=3600)
    return user
```

### 3. 分页

```python
# ✅ 好：使用分页
GET /users?page=1&page_size=20

# ❌ 不好：返回全部
GET /users  # 返回10000条记录
```

---

## 工具配置

### 1. 代码格式化

- Python: `black`
- JavaScript/TypeScript: `prettier`
- Go: `gofmt`

### 2. 代码检查

- Python: `pylint`, `flake8`
- JavaScript/TypeScript: `eslint`
- Go: `golangci-lint`

### 3. 类型检查

- Python: `mypy`
- TypeScript: `tsc --noEmit`

---

## 参考资料

- [doc/policies/safety.md](../policies/safety.md) - 安全规范
- [doc/process/testing.md](./testing.md) - 测试准则
- [doc/process/pr_workflow.md](./pr_workflow.md) - PR工作流程

---

## 维护历史

- 2024-XX-XX: v1.0 初始创建
- 2025-11-09: v2.0 完善编码、提交、测试等规范（Phase 11）

