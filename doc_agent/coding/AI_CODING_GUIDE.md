# AI编码指南（轻量版）

> **用途**: AI Agent编码时的核心规范（轻量化）  
> **适用对象**: 编程大模型、AI Agent  
> **完整版本**: [CONVENTIONS.md](./CONVENTIONS.md) - 人类开发者详细规范

---

## 核心原则

### 1. 代码质量优先
- 可读性 > 简洁性 > 性能
- 明确 > 隐式
- 安全 > 便利

### 2. 遵循现有规范
- 保持项目风格一致
- 遵循语言最佳实践
- 参考已有代码示例

---

## 快速规范

### 命名约定

```python
# Python
class UserService:          # PascalCase
    def get_user_by_id():   # snake_case
        MAX_RETRIES = 3     # UPPER_SNAKE_CASE

# TypeScript/JavaScript
class UserService {         // PascalCase
    getUserById()           // camelCase
    const MAX_RETRIES = 3;  // UPPER_SNAKE_CASE
}

# Go
type UserService struct {}  // PascalCase导出
func (s *UserService) GetUserByID()  // PascalCase导出
```

---

### 注释要求

**必须添加注释的情况**:
- 复杂算法和业务逻辑
- 非显而易见的代码
- TODO/FIXME/HACK标记
- 公开API和接口

**注释格式**:
```python
def calculate_discount(price: float, level: int) -> float:
    """
    计算折扣价格
    
    Args:
        price: 原价
        level: 用户等级(1-5)
    
    Returns:
        折扣后价格
    """
    return price * (1 - level * 0.1)
```

---

### 错误处理

**原则**:
- 明确的异常类型（不用bare except）
- 有意义的错误消息
- 失败时清理资源

```python
# ✅ 好
try:
    user = get_user(user_id)
except UserNotFoundError:
    logger.warning(f"User {user_id} not found")
    return None
except DatabaseError as e:
    logger.error(f"DB error: {e}")
    raise

# ❌ 不好
try:
    user = get_user(user_id)
except:
    pass
```

---

### 安全要求

**必须遵守**:
1. **输入验证**: 所有外部输入必须验证
2. **SQL注入防护**: 使用参数化查询
3. **密码处理**: 使用哈希，不存储明文
4. **权限检查**: 操作前检查权限

```python
# ✅ 好：参数化查询
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ❌ 不好：字符串拼接
cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
```

---

### 测试要求

**必须测试**:
- 新增功能：单元测试
- 修改逻辑：回归测试
- API变更：集成测试

**测试覆盖**:
- 正常情况
- 边界情况
- 异常情况

---

## 文件操作规范

### 创建新文件

**必须包含**:
1. 文件头注释（用途、作者、日期）
2. 必要的imports
3. 类型注解（如果语言支持）

```python
"""
user_service.py - 用户服务

提供用户管理核心逻辑。

Created: 2024-01-01
"""

from typing import Optional
from .models import User
```

---

### 修改现有文件

**规则**:
1. **保持原有风格**：缩进、命名、格式
2. **最小化改动**：只修改必要部分
3. **避免混合变更**：功能变更和格式调整分开

---

## Git提交规范

### Commit Message格式

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Type类型

| Type | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | feat(auth): 添加JWT认证 |
| fix | Bug修复 | fix(api): 修复500错误 |
| docs | 文档 | docs(readme): 更新说明 |
| refactor | 重构 | refactor(db): 优化查询 |
| test | 测试 | test(user): 添加单元测试 |

**示例**:
```
feat(user): 添加用户注册功能

- 实现注册API
- 添加邮箱验证
- 密码强度检查

Closes #123
```

---

## API设计规范

### RESTful原则

```
资源：复数名词
✅ GET  /users
✅ POST /users
✅ GET  /users/:id
✅ PUT  /users/:id
✅ DELETE /users/:id

❌ GET /getUser
❌ POST /createUser
```

### 响应格式

```json
{
    "code": 0,
    "message": "success",
    "data": { ... }
}
```

### HTTP状态码

- 200: 成功（GET/PUT/PATCH）
- 201: 创建成功（POST）
- 400: 请求参数错误
- 401: 未认证
- 404: 资源不存在
- 500: 服务器错误

---

## 性能考虑

### 必须避免

1. **N+1查询**: 使用批量查询或join
2. **循环中的I/O**: 提前批量处理
3. **无限制查询**: 添加分页和限制

```python
# ✅ 好：批量查询
users = User.objects.filter(id__in=user_ids)

# ❌ 不好：N+1
for user_id in user_ids:
    user = User.objects.get(id=user_id)
```

---

## 常见场景快速参考

### 场景1: 新增API接口

1. ✅ 定义路由和handler
2. ✅ 实现业务逻辑
3. ✅ 添加输入验证
4. ✅ 添加错误处理
5. ✅ 编写单元测试
6. ✅ 更新API文档

---

### 场景2: 修复Bug

1. ✅ 复现问题
2. ✅ 定位根因
3. ✅ 最小化修复
4. ✅ 添加回归测试
5. ✅ 验证修复效果

---

### 场景3: 数据库变更

1. ✅ 查看[DB_CHANGE_GUIDE.md](./DB_CHANGE_GUIDE.md)
2. ✅ 编写迁移脚本（up + down）
3. ✅ 本地测试
4. ✅ 更新TEST_DATA.md
5. ✅ Code Review

---

### 场景4: 添加测试数据

**小数据量(≤50条)**: 使用Fixtures
```sql
-- fixtures/test_users.sql
INSERT INTO users VALUES (...);
```

**大数据量(>50条)**: 使用Mock规则
```yaml
# TEST_DATA.md
mock_rules:
  users:
    count: 1000
    fields: ...
```

参考: [TEST_DATA_STRATEGY.md](./TEST_DATA_STRATEGY.md)

---

## 质量检查清单

### 提交代码前必查

- [ ] 代码符合命名规范
- [ ] 添加必要注释
- [ ] 错误处理完整
- [ ] 输入已验证
- [ ] 添加单元测试
- [ ] 本地测试通过
- [ ] 无lint错误

```bash
# 运行质量检查
make dev_check
```

---

## 智能触发提醒

### 触发相关文档

**数据库操作** → 自动触发 DB_CHANGE_GUIDE  
**测试数据** → 自动触发 TEST_DATA_STRATEGY  
**契约变更** → 自动触发 Guardrail检查  

系统会根据你的操作自动推荐相关文档，注意查看。

---

## 获取更多帮助

### 详细规范
- **完整版**: [CONVENTIONS.md](./CONVENTIONS.md) (611行详细规范)
- **安全详情**: [security_details.md](../policies/security_details.md)
- **质量标准**: [quality_standards.md](../policies/quality_standards.md)

### 快速查询
- **测试规范**: [testing.md](./testing.md)
- **PR流程**: [pr_workflow.md](./pr_workflow.md)
- **命令参考**: [commands.md](../reference/commands.md)

---

## 记住这些原则

1. **安全第一**: 输入验证、权限检查、防注入
2. **测试覆盖**: 新功能必须有测试
3. **错误处理**: 明确的异常类型和错误消息
4. **代码可读**: 清晰的命名和必要的注释
5. **保持一致**: 遵循项目现有风格

---

**需要详细说明？请查阅 [CONVENTIONS.md](./CONVENTIONS.md)**

---

## 维护历史

- 2025-11-09: 创建AI编码指南轻量版（Phase 11优化）

