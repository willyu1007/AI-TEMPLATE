# Common Module - API Contract

> **Language**: English (AI-optimized documentation)  
> **Last Updated**: 2025-11-09  
> **Version**: 1.0.0

---

## Overview

The `common` module provides shared utilities, models, middleware, and constants used across all modules. This module contains zero business logic - only generic technical infrastructure.

**Key Principle**: No dependencies on business modules. Common is imported by others, never imports from others.

---

## API Categories

### 1. String Utilities (`utils.string_utils`)

#### `camel_to_snake(text: str) -> str`
Convert camelCase/PascalCase to snake_case.

```python
from modules.common.utils import camel_to_snake

camel_to_snake("UserProfile")  # => "user_profile"
camel_to_snake("getUserName")  # => "get_user_name"
```

#### `snake_to_camel(text: str, capitalize_first: bool = False) -> str`
Convert snake_case to camelCase or PascalCase.

```python
from modules.common.utils import snake_to_camel

snake_to_camel("user_profile")  # => "userProfile"
snake_to_camel("user_profile", capitalize_first=True)  # => "UserProfile"
```

#### `truncate_string(text: str, max_length: int, suffix: str = "...") -> str`
Truncate string to maximum length with optional suffix.

```python
from modules.common.utils import truncate_string

truncate_string("Hello World", 8)  # => "Hello..."
truncate_string("Short", 10)  # => "Short"
```

#### `normalize_string(text: str, *, trim: bool = True, lowercase: bool = False) -> str`
Normalize string (trim whitespace, optionally lowercase).

```python
from modules.common.utils import normalize_string

normalize_string("  Hello  ")  # => "Hello"
normalize_string("  HELLO  ", lowercase=True)  # => "hello"
```

---

### 2. Date/Time Utilities (`utils.date_utils`)

#### `now_utc() -> datetime`
Get current UTC datetime.

```python
from modules.common.utils import now_utc

current_time = now_utc()  # datetime object in UTC
```

#### `format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str`
Format datetime to string.

```python
from modules.common.utils import format_datetime

formatted = format_datetime(dt, "%Y-%m-%d")  # => "2025-11-09"
```

#### `parse_datetime(date_str: str, format_str: str = "%Y-%m-%d") -> datetime`
Parse string to datetime.

```python
from modules.common.utils import parse_datetime

dt = parse_datetime("2025-11-09")  # => datetime object
```

#### `time_ago(past_time: datetime, locale: str = "en") -> str`
Calculate relative time (e.g., "5 minutes ago").

```python
from modules.common.utils import time_ago

relative = time_ago(past_dt)  # => "5 minutes ago"
relative_zh = time_ago(past_dt, locale="zh")  # => "5分钟前"
```

---

### 3. Validation Utilities (`utils.validation`)

#### `validate_email(email: str) -> bool`
Validate email format using regex.

```python
from modules.common.utils import validate_email

validate_email("user@example.com")  # => True
validate_email("invalid-email")  # => False
```

#### `validate_phone(phone: str, country: str = "CN") -> bool`
Validate phone number (default: China mobile).

```python
from modules.common.utils import validate_phone

validate_phone("13800138000")  # => True
validate_phone("1234")  # => False
```

#### `validate_url(url: str) -> bool`
Validate URL format.

```python
from modules.common.utils import validate_url

validate_url("https://example.com")  # => True
validate_url("not-a-url")  # => False
```

#### `validate_uuid(uuid_str: str) -> bool`
Validate UUID format.

```python
from modules.common.utils import validate_uuid

validate_uuid("123e4567-e89b-12d3-a456-426614174000")  # => True
validate_uuid("invalid")  # => False
```

---

### 4. Encryption Utilities (`utils.encryption`)

> **Warning**: Example implementations only. Use production-grade libraries (bcrypt/argon2) in production.

#### `hash_password(password: str) -> str`
Hash password using secure algorithm.

```python
from modules.common.utils import hash_password

hashed = hash_password("password123")  # => hashed string
```

#### `verify_password(password: str, hashed: str) -> bool`
Verify password against hash.

```python
from modules.common.utils import verify_password

is_valid = verify_password("password123", hashed)  # => True/False
```

#### `encrypt_data(data: str, key: Optional[str] = None) -> str`
Encrypt sensitive data.

#### `decrypt_data(encrypted: str, key: Optional[str] = None) -> str`
Decrypt encrypted data.

---

### 5. Data Models (`models`)

#### `BaseModel`
Base class for all data models with serialization support.

```python
from modules.common.models import BaseModel
from dataclasses import dataclass

@dataclass
class User(BaseModel):
    id: str
    name: str

user = User(id="123", name="Alice")
user_dict = user.to_dict()  # Serialize to dict
```

#### `TimestampMixin`
Mixin providing `created_at` and `updated_at` fields.

```python
from modules.common.models import BaseModel, TimestampMixin

@dataclass
class User(BaseModel, TimestampMixin):
    id: str
    name: str
```

#### `PaginationParams`
Standard pagination parameters.

```python
from modules.common.models import PaginationParams

params = PaginationParams(page=1, page_size=20)
offset = params.get_offset()  # => 0
limit = params.get_limit()  # => 20
```

**Fields**:
- `page: int` - Page number (1-indexed)
- `page_size: int` - Items per page (default: 20, max: 100)

**Methods**:
- `get_offset() -> int` - Calculate SQL offset
- `get_limit() -> int` - Get page size limit

#### `PaginationResult[T]`
Standard pagination result wrapper.

```python
from modules.common.models import PaginationResult

result = PaginationResult(
    items=[...],
    total=100,
    page=1,
    page_size=20
)
```

**Fields**:
- `items: List[T]` - Page items
- `total: int` - Total item count
- `page: int` - Current page
- `page_size: int` - Items per page
- `total_pages: int` - Total pages (computed)
- `has_next: bool` - Has next page (computed)
- `has_prev: bool` - Has previous page (computed)

#### `ApiResponse`
Standard API response format.

```python
from modules.common.models import ApiResponse

# Success response
response = ApiResponse.success_response(
    data={"user": {...}},
    message="Success"
)

# Error response
response = ApiResponse.error_response(
    message="Invalid parameter",
    code=400,
    error_code="INVALID_PARAM"
)
```

**Methods**:
- `success_response(data, message="Success", meta=None) -> dict`
- `error_response(message, code=500, error_code=None, details=None) -> dict`

---

### 6. Middleware (`middleware`)

#### `require_auth` (Decorator)
Require authentication for function/endpoint.

```python
from modules.common.middleware import require_auth

@require_auth
def protected_api():
    return {"data": "sensitive"}
```

#### `get_current_user(token: str) -> Optional[dict]`
Extract user info from authentication token.

#### `setup_logging(level: str = "INFO", format: Optional[str] = None)`
Configure application logging.

```python
from modules.common.middleware import setup_logging

setup_logging(level="DEBUG")
```

#### `log_request(method: str, path: str, **kwargs)`
Log incoming HTTP request.

#### `log_response(status_code: int, path: str, duration_ms: float)`
Log HTTP response with timing.

#### `rate_limit` (Decorator)
Apply rate limiting to function/endpoint.

```python
from modules.common.middleware import rate_limit

@rate_limit(max_requests=10, window_seconds=60)
def api_endpoint():
    return {"data": "response"}
```

#### `RateLimiter` (Class)
Rate limiter implementation.

```python
from modules.common.middleware import RateLimiter

limiter = RateLimiter(max_requests=100, window_seconds=60)
if limiter.is_allowed(user_id):
    # Process request
    pass
else:
    # Reject (rate limit exceeded)
    pass
```

---

### 7. Constants (`constants`)

#### `ErrorCode` (Enum)
Standard error codes.

```python
from modules.common.constants import ErrorCode

error = ErrorCode.INVALID_EMAIL
error.value  # => "INVALID_EMAIL"
error.get_message('en')  # => "Invalid email format"
error.get_message('zh')  # => "邮箱格式无效"
```

**Available Codes**:
- `INVALID_PARAMETER` - Invalid parameter
- `INVALID_EMAIL` - Invalid email format
- `INVALID_PHONE` - Invalid phone format
- `UNAUTHORIZED` - Authentication required
- `FORBIDDEN` - Access denied
- `NOT_FOUND` - Resource not found
- `INTERNAL_ERROR` - Internal server error

#### `Status` (Enum)
Generic status constants.

```python
from modules.common.constants import Status

Status.ACTIVE.value  # => "active"
Status.INACTIVE.value  # => "inactive"
Status.DELETED.value  # => "deleted"
```

#### `UserStatus` (Enum)
User-specific status constants.

#### `OrderStatus` (Enum)
Order-specific status constants.

---

### 8. Interfaces (`interfaces`)

#### `Repository[T, ID]` (Protocol)
Base repository interface for data access.

```python
from modules.common.interfaces import Repository
from typing import Optional

class UserRepository(Repository[User, str]):
    def find_by_id(self, id: str) -> Optional[User]:
        # Implementation
        pass
    
    def save(self, entity: User) -> User:
        # Implementation
        pass
    
    def delete(self, id: str) -> bool:
        # Implementation
        pass
```

#### `CRUDRepository[T, ID]` (Protocol)
Extended repository with pagination and query.

**Additional Methods**:
- `find_all(params: PaginationParams) -> PaginationResult[T]`
- `find_by_criteria(criteria: dict, params: PaginationParams) -> PaginationResult[T]`
- `count() -> int`

---

## Import Conventions

### Recommended Import Style
```python
# Utils (import specific functions)
from modules.common.utils import validate_email, now_utc, camel_to_snake

# Models (import classes)
from modules.common.models import BaseModel, PaginationParams, ApiResponse

# Middleware (import decorators/functions)
from modules.common.middleware import require_auth, rate_limit, setup_logging

# Constants (import enums)
from modules.common.constants import ErrorCode, Status, UserStatus
```

### Package-Level Imports
All public APIs are exported from `__init__.py`:

```python
# Direct import from common
from modules.common.utils import validate_email
# Same as
from modules.common.utils.validation import validate_email
```

---

## Versioning & Compatibility

### Version Format
`MAJOR.MINOR.PATCH` (Semantic Versioning)

### Compatibility Rules
1. **PATCH** (1.0.X): Bug fixes, no API changes
2. **MINOR** (1.X.0): New features, backward compatible
3. **MAJOR** (X.0.0): Breaking changes

### Deprecation Policy
1. Mark as `@deprecated` with migration guide
2. Keep for at least one MINOR version
3. Remove in next MAJOR version

Example:
```python
import warnings
from functools import wraps

def deprecated(message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@deprecated("Use validate_email_v2() instead. Will be removed in 2.0.0")
def validate_email_old(email: str) -> bool:
    # Old implementation
    pass
```

---

## Testing Requirements

### Coverage Requirement
**All common module code must have ≥90% test coverage.**

### Test Structure
```
tests/
└── common/
    ├── test_string_utils.py
    ├── test_date_utils.py
    ├── test_validation.py
    ├── test_encryption.py
    ├── test_models.py
    ├── test_middleware.py
    ├── test_constants.py
    └── test_interfaces.py
```

### Running Tests
```bash
# Run all common tests
pytest tests/common/ -v

# Check coverage
pytest tests/common/ --cov=modules.common --cov-report=html

# Coverage report at: htmlcov/index.html
```

---

## Change Log

See `/modules/common/doc/CHANGELOG.md` for version history.

---

**Contract Version**: 1.0.0  
**Last Updated**: 2025-11-09  
**Maintained by**: Project Team

