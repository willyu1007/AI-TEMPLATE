# 共享代码库（Common Code）

## 目标
提供跨模块共享的通用代码，避免代码重复，提高代码复用性和可维护性。

## 适用场景
- 多个模块需要使用的工具函数
- 共享的数据模型和接口定义
- 通用的中间件和拦截器
- 全局常量和配置辅助函数

## 前置条件
- 已确定需要共享的代码范围
- 已评估代码对模块间依赖的影响

---

## 目录结构

```text
common/
├── utils/          # 通用工具函数
│   ├── __init__.py
│   ├── string_utils.py    # 字符串处理
│   ├── date_utils.py      # 日期时间处理
│   ├── validation.py      # 数据验证
│   └── encryption.py      # 加密解密
├── models/         # 共享数据模型
│   ├── __init__.py
│   ├── base.py            # 基础模型类
│   └── common.py          # 通用数据结构
├── middleware/     # 共享中间件
│   ├── __init__.py
│   ├── auth.py            # 认证中间件
│   ├── logging.py         # 日志中间件
│   └── rate_limit.py      # 限流中间件
├── constants/      # 全局常量
│   ├── __init__.py
│   ├── error_codes.py     # 错误码定义
│   └── status.py          # 状态常量
└── interfaces/     # 共享接口定义
    ├── __init__.py
    └── repository.py      # 仓储接口
```

---

## 核心原则

### 1. 最小化原则
**规则**：只将真正需要跨模块共享的代码放入 `common/`。

**判断标准**：
- 至少 2 个模块需要使用
- 代码逻辑稳定，不会频繁变更
- 功能单一，职责明确

**示例**：
```
# ❌ 错误：仅一个模块使用
# common/utils/user_validator.py  # 只有 user 模块需要

# ✅ 正确：多个模块使用
# common/utils/email_validator.py  # user, auth, notification 都需要
```

---

## 2. 无业务逻辑原则
**规则**：`common/` 中不应包含业务逻辑，只包含通用技术能力。

**禁止事项**：
- ❌ 业务规则判断
- ❌ 领域特定逻辑
- ❌ 模块特定的数据模型

**允许事项**：
- ✅ 通用工具函数（字符串、日期、验证等）
- ✅ 技术中间件（认证、日志、限流等）
- ✅ 基础数据结构（分页、响应格式等）

**示例**：
```
# ❌ 错误：包含业务逻辑
def calculate_order_total(order):
    """计算订单总价（业务逻辑）"""
    # 应该放在 modules/order/ 中

# ✅ 正确：通用工具
def format_currency(amount, currency='CNY'):
    """格式化货币金额（通用工具）"""
    # 可以放在 common/utils/ 中
```

---

## 3. 版本兼容原则
**规则**：`common/` 的变更必须向后兼容，或提供明确的迁移路径。

**要求**：
- 新增函数/类：直接添加（向后兼容）
- 修改函数签名：保留旧版本，标记为 `@deprecated`
- 删除函数/类：至少保留一个发布周期，并更新调用方

---

### 4. 测试覆盖要求
**规则**：`common/` 中的所有代码必须有完整的单元测试，覆盖率 ≥90%。

**验证命令**：
```
# 运行 common 的测试
pytest tests/common/ -v --cov=common --cov-report=html

# 覆盖率要求
# common/utils/*: ≥90%
# common/models/*: ≥90%
# common/middleware/*: ≥90%
```

---

## 快速参考（AI 使用指南）

### 函数列表总览

#### 1. 字符串工具 (`common.utils`)
| 函数名 | 功能 | 使用示例 |
|--------|------|----------|
| `camel_to_snake` | 驼峰转蛇形 | `camel_to_snake("UserProfile")` → `"user_profile"` |
| `snake_to_camel` | 蛇形转驼峰 | `snake_to_camel("user_profile")` → `"userProfile"` |
| `truncate_string` | 截断字符串 | `truncate_string("Hello", 3)` → `"Hel..."` |
| `normalize_string` | 规范化字符串 | `normalize_string("  Hello  ", trim=True)` → `"Hello"` |

**导入方式**：
```
from common.utils import camel_to_snake, snake_to_camel, truncate_string, normalize_string
# 或
from common.utils.string_utils import camel_to_snake
```

---

## 2. 日期时间工具 (`common.utils`)
| 函数名 | 功能 | 使用示例 |
|--------|------|----------|
| `now_utc` | 获取当前 UTC 时间 | `now_utc()` → `datetime(2025, 11, 5, ...)` |
| `format_datetime` | 格式化日期时间 | `format_datetime(dt, '%Y-%m-%d')` → `"2025-11-05"` |
| `parse_datetime` | 解析日期字符串 | `parse_datetime("2025-11-05")` → `datetime` 对象 |
| `time_ago` | 计算相对时间 | `time_ago(past_time)` → `"5分钟前"` |

**导入方式**：
```
from common.utils import now_utc, format_datetime, parse_datetime, time_ago
# 或
from common.utils.date_utils import now_utc
```

---

## 3. 数据验证工具 (`common.utils`)
| 函数名 | 功能 | 使用示例 |
|--------|------|----------|
| `validate_email` | 验证邮箱格式 | `validate_email("user@example.com")` → `True` |
| `validate_phone` | 验证手机号 | `validate_phone("13800138000")` → `True` |
| `validate_url` | 验证 URL | `validate_url("https://example.com")` → `True` |
| `validate_uuid` | 验证 UUID | `validate_uuid("123e4567-...")` → `True` |

**导入方式**：
```
from common.utils import validate_email, validate_phone, validate_url, validate_uuid
# 或
from common.utils.validation import validate_email
```

---

## 4. 加密解密工具 (`common.utils`)
| 函数名 | 功能 | 使用示例 |
|--------|------|----------|
| `hash_password` | 哈希密码 | `hash_password("password123")` → `"hashed_string"` |
| `verify_password` | 验证密码 | `verify_password("pwd", hashed)` → `True/False` |
| `encrypt_data` | 加密数据 | `encrypt_data("sensitive")` → `"encrypted_string"` |
| `decrypt_data` | 解密数据 | `decrypt_data(encrypted)` → `"sensitive"` |

**导入方式**：
```
from common.utils import hash_password, verify_password, encrypt_data, decrypt_data
# 或
from common.utils.encryption import hash_password
```

**注意**：生产环境应使用 `bcrypt` 或 `argon2` 替代示例实现。

---

## 5. 数据模型 (`common.models`)
| 类名 | 功能 | 使用示例 |
|------|------|----------|
| `BaseModel` | 基础模型类 | 继承用于序列化/反序列化 |
| `TimestampMixin` | 时间戳混入 | 提供 `created_at`、`updated_at` |
| `PaginationParams` | 分页参数 | `PaginationParams(page=1, page_size=20)` |
| `PaginationResult` | 分页结果 | `PaginationResult(items=[...], total=100, ...)` |
| `ApiResponse` | API 响应 | `ApiResponse.success_response(data={...})` |

**导入方式**：
```
from common.models import BaseModel, TimestampMixin, PaginationParams, PaginationResult, ApiResponse
# 或
from common.models.base import BaseModel
from common.models.common import PaginationParams
```

**使用示例**：
```
from common.models import BaseModel, TimestampMixin, PaginationParams

@dataclass
class User(BaseModel, TimestampMixin):
    id: str
    name: str

# 分页查询
params = PaginationParams(page=1, page_size=20)
offset = params.get_offset()  # 0
limit = params.get_limit()    # 20
```

---

## 6. 中间件 (`common.middleware`)
| 函数/类名 | 功能 | 使用示例 |
|-----------|------|----------|
| `require_auth` | 认证装饰器 | `@require_auth` 装饰需要认证的函数 |
| `get_current_user` | 获取当前用户 | `get_current_user(token)` → 用户信息 |
| `setup_logging` | 配置日志 | `setup_logging(level="INFO")` |
| `log_request` | 记录请求日志 | `log_request("GET", "/api/users")` |
| `log_response` | 记录响应日志 | `log_response(200, "/api/users", 150.5)` |
| `rate_limit` | 限流装饰器 | `@rate_limit(max_requests=10)` |
| `RateLimiter` | 限流器类 | `RateLimiter(max_requests=100, window_seconds=60)` |

**导入方式**：
```
from common.middleware import require_auth, rate_limit, setup_logging
from common.middleware import RateLimiter
# 或
from common.middleware.auth import require_auth
from common.middleware.rate_limit import rate_limit
```

**使用示例**：
```
from common.middleware import require_auth, rate_limit

@require_auth
@rate_limit(max_requests=10, window_seconds=60)
def api_endpoint():
    return {"data": "response"}
```

---

## 7. 常量定义 (`common.constants`)
| 类名 | 功能 | 使用示例 |
|------|------|----------|
| `ErrorCode` | 错误码枚举 | `ErrorCode.INVALID_EMAIL` |
| `Status` | 通用状态 | `Status.ACTIVE` |
| `UserStatus` | 用户状态 | `UserStatus.ACTIVE` |
| `OrderStatus` | 订单状态 | `OrderStatus.PENDING` |

**导入方式**：
```
from common.constants import ErrorCode, Status, UserStatus, OrderStatus
# 或
from common.constants.error_codes import ErrorCode
from common.constants.status import UserStatus
```

**使用示例**：
```
from common.constants import ErrorCode, UserStatus

# 错误码
if not validate_email(email):
    raise ValueError(ErrorCode.INVALID_EMAIL.value)
    # 或使用消息
    message = ErrorCode.INVALID_EMAIL.get_message('zh')  # "参数无效"

# 状态
user.status = UserStatus.ACTIVE.value  # "active"
```

---

## 8. 接口定义 (`common.interfaces`)
| 类名 | 功能 | 使用示例 |
|------|------|----------|
| `Repository` | 基础仓储接口 | 定义 `find_by_id`, `save`, `delete` |
| `CRUDRepository` | CRUD 仓储接口 | 扩展分页、查询等功能 |

**导入方式**：
```
from common.interfaces import Repository, CRUDRepository
# 或
from common.interfaces.repository import Repository
```

**使用示例**：
```
from common.interfaces import CRUDRepository
from common.models import User

class UserRepository(CRUDRepository[User, str]):
    def find_by_id(self, id: str) -> Optional[User]:
        # 实现查找逻辑
        pass
    
    def save(self, entity: User) -> User:
        # 实现保存逻辑
        pass
    # ... 实现其他方法
```

---

## 使用指南

### 在模块中引用 common 代码

**Python 示例**：
```
# modules/user/service.py
from common.utils.validation import validate_email
from common.middleware.auth import require_auth
from common.constants.error_codes import ErrorCode

def create_user(email: str):
    if not validate_email(email):
        raise ValueError(ErrorCode.INVALID_EMAIL.value)
    # ...
```

**Go 示例**：
```
// modules/user/service.go
import (
    "github.com/your-org/project/common/utils"
    "github.com/your-org/project/common/middleware"
)

func CreateUser(email string) error {
    if !utils.ValidateEmail(email) {
        return errors.New("invalid email")
    }
    // ...
}
```

**TypeScript 示例**：
```
// modules/user/service.ts
import { validateEmail } from '@/common/utils/validation'
import { requireAuth } from '@/common/middleware/auth'

export function createUser(email: string) {
  if (!validateEmail(email)) {
    throw new Error('Invalid email')
  }
  // ...
}
```

---

## AI 操作指南

### 如何查找和使用 common 函数

1. **按功能查找**：
   - 需要验证数据？→ 查看 `common.utils.validation`
   - 需要处理字符串？→ 查看 `common.utils.string_utils`
   - 需要日期时间？→ 查看 `common.utils.date_utils`
   - 需要加密？→ 查看 `common.utils.encryption`
   - 需要分页？→ 查看 `common.models.common.PaginationParams`
   - 需要认证？→ 查看 `common.middleware.auth`
   - 需要限流？→ 查看 `common.middleware.rate_limit`
   - 需要错误码？→ 查看 `common.constants.error_codes`

2. **快速导入模板**：
```
# 验证数据
from common.utils import validate_email, validate_phone, validate_url

# 处理字符串
from common.utils import camel_to_snake, snake_to_camel, truncate_string

# 日期时间
from common.utils import now_utc, format_datetime, parse_datetime, time_ago

# 加密解密（注意：生产环境应使用专业库）
from common.utils import hash_password, verify_password

# 数据模型
from common.models import BaseModel, PaginationParams, ApiResponse

# 中间件
from common.middleware import require_auth, rate_limit, setup_logging

# 常量
from common.constants import ErrorCode, UserStatus
```

3. **常见使用场景**：

**场景 1：用户注册验证**
```
from common.utils import validate_email, validate_phone
from common.constants import ErrorCode

def register_user(email: str, phone: str):
    if not validate_email(email):
        raise ValueError(ErrorCode.INVALID_PARAMETER.value)
    if not validate_phone(phone):
        raise ValueError(ErrorCode.INVALID_PARAMETER.value)
    # 继续注册逻辑
```

**场景 2：分页查询**
```
from common.models import PaginationParams, PaginationResult

def get_users(page: int = 1, page_size: int = 20):
    params = PaginationParams(page=page, page_size=page_size)
    offset = params.get_offset()
    limit = params.get_limit()
    
    # 查询数据库
    items = db.query(User).offset(offset).limit(limit).all()
    total = db.query(User).count()
    
    return PaginationResult(items=items, total=total, page=page, page_size=page_size)
```

**场景 3：API 响应**
```
from common.models import ApiResponse

def get_user_api(user_id: str):
    try:
        user = get_user(user_id)
        return ApiResponse.success_response(data=user.to_dict())
    except Exception as e:
        return ApiResponse.error_response(message=str(e), code=500)
```

**场景 4：认证和限流**
```
from common.middleware import require_auth, rate_limit

@require_auth
@rate_limit(max_requests=10, window_seconds=60)
def sensitive_api():
    return {"data": "sensitive information"}
```

---

## 验证步骤

在添加新代码到 `common/` 后，必须：

1. **更新本 README**：在"快速参考"章节添加新函数说明。
2. **更新 `__init__.py`**：确保新函数可从包级别导入。
3. **编写测试**：覆盖率达到 ≥90%
4. **更新文档**：确保函数有完整的文档字符串

---

## 不同语言的命名习惯

| 语言 | 常用命名 | 说明 |
|------|---------|------|
| Python | `common/`, `shared/`, `utils/` | 很少使用 `lib/` |
| Go | `pkg/`, `internal/`, `common/` | `lib/` 不常见 |
| JavaScript/TypeScript | `common/`, `shared/`, `src/` | `lib/` 可能用于编译输出 |
| C/C++ | `lib/`, `src/` | `lib/` 很常见 |
| Java | `common/`, `shared/`, `src/main/java/` | `lib/` 通常指依赖库 |

**本模板使用 `common/`**，因为：
- 跨语言通用
- Python/Go/JS 项目都常用
- 语义清晰（"通用代码"）

---

## 添加新代码到 common/

### 流程

1. **评估需求**
   ```
   # 检查是否有多个模块需要此功能
   grep -r "similar_function" modules/
```

2. **创建功能分支**
   ```
   git checkout -b feat/common-add-email-validator
```

3. **实现代码**
   ```
   # 创建文件
   touch common/utils/email_validator.py
   
   # 编写代码和测试
   touch tests/common/test_email_validator.py
```

4. **编写测试**
   ```
   # 确保覆盖率 ≥90%
   pytest tests/common/test_email_validator.py --cov=common/utils/email_validator --cov-report=term
```

5. **更新文档**
   ```
   # 更新 common/README.md 说明新功能
   # 更新相关模块的文档引用
```

6. **提交 PR**
   ```
   # PR 标题：feat(common): 添加邮箱验证工具函数
   # PR 描述：说明为什么需要此功能，哪些模块将使用
```

---

## 验证步骤

### 开发环境验证
```
# 1. 运行 common 测试
pytest tests/common/ -v

# 2. 检查覆盖率
pytest tests/common/ --cov=common --cov-report=html

# 3. 检查导入是否正常
python -c "from common.utils.validation import validate_email; print('OK')"

# 4. 运行完整检查
make dev_check
```

---

## 回滚逻辑

如果 `common/` 的变更导致问题：

### 代码回滚
```
# 1. 回滚到上一个版本
git revert <commit-hash>

# 2. 验证受影响模块
pytest tests/modules/ -v

# 3. 重新部署
make deploy
```

## 依赖回滚
如果某个模块依赖了有问题的 `common/` 函数：

```bash
# 1. 在模块中临时复制函数（短期方案）
# 2. 修复 common/ 中的问题
# 3. 移除模块中的临时复制
```

---

## 注意事项

### 1. 避免循环依赖
**问题**：`common/` 不应依赖任何 `modules/` 中的代码。

**检查**：
```
# 检查 common/ 中的导入
grep -r "from modules" common/
grep -r "import modules" common/
```

## 2. 性能考虑
- `common/` 中的函数会被频繁调用，需要关注性能
- 避免在 `common/` 中进行重 IO 操作
- 考虑使用缓存机制

### 3. 文档要求
- 所有公共函数必须有文档字符串
- 提供使用示例
- 说明参数和返回值

---

## AI 维护检查清单

每次修改 `common/` 代码后，AI 应执行以下检查：

1. **更新文档**
   - [ ] 在 `common/README.md` 的"快速参考"章节更新函数列表
   - [ ] 确保所有新函数都有使用示例
   - [ ] 更新导入方式说明

2. **更新导出**
   - [ ] 在对应的 `__init__.py` 中添加新函数到 `__all__`
   - [ ] 确保可以从包级别导入

3. **测试验证**
   - [ ] 运行 `pytest tests/common/ -v`
   - [ ] 检查覆盖率 ≥90%
   - [ ] 验证导入测试通过

4. **向后兼容**
   - [ ] 检查是否破坏现有接口
   - [ ] 如需修改签名，标记 `@deprecated` 并保留旧版本

5. **运行维护脚本**
   ```
   make ai_maintenance
```

---

## 相关文档
- 模块开发指南：`modules/example/README.md`
- 测试规范：`tests/README.md`
- 代码审查：`agent.md` §11
- AI 维护机制：`agent.md` §14

