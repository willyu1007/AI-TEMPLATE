---
audience: ai
language: en
version: summary
purpose: Quick usage guide for common module
full_version: /modules/common/README.md
---

# Common Module - Quick Usage Guide

> **For AI Agents** - Essential APIs and usage (~150 lines)  
> **Full Guide**: [README.md](README.md) (648 lines, for humans)  
> **Contract**: [doc/CONTRACT.md](doc/CONTRACT.md)

---

## Module Overview

**Purpose**: Shared utilities, models, middleware, and constants across all modules.

**Key Principle**: Only truly reusable code (used by 2+ modules), no business logic.

---

## Core APIs

### 1. Utils (Utility Functions)

#### string_utils.py
```python
from modules.common.utils.string_utils import sanitize, validate_email

# Sanitize user input
safe_text = sanitize(user_input)

# Validate email
is_valid = validate_email("user@example.com")
```

#### date_utils.py
```python
from modules.common.utils.date_utils import format_datetime, parse_datetime

# Format datetime
formatted = format_datetime(dt, "%Y-%m-%d")

# Parse datetime
dt = parse_datetime("2025-11-09 12:00:00")
```

#### encryption.py
```python
from modules.common.utils.encryption import encrypt, decrypt

# Encrypt sensitive data
encrypted = encrypt("sensitive data")

# Decrypt
decrypted = decrypt(encrypted)
```

#### validation.py
```python
from modules.common.utils.validation import validate_schema, check_range

# Validate against schema
errors = validate_schema(data, schema)

# Check numeric range
is_valid = check_range(value, min=0, max=100)
```

---

### 2. Models (Shared Data Models)

#### base.py
```python
from modules.common.models.base import BaseModel

class User(BaseModel):
    """All models inherit from BaseModel"""
    id: str
    name: str
    created_at: datetime
```

**BaseModel provides**:
- `to_dict()` - Convert to dictionary
- `from_dict()` - Create from dictionary
- `validate()` - Validate fields
- `__str__()` - String representation

---

### 3. Middleware (Request/Response Interceptors)

#### auth.py
```python
from modules.common.middleware.auth import AuthMiddleware

# Add authentication
app.add_middleware(AuthMiddleware, secret_key=SECRET_KEY)
```

#### logging.py
```python
from modules.common.middleware.logging import LoggingMiddleware

# Add request/response logging
app.add_middleware(LoggingMiddleware, level="INFO")
```

#### rate_limit.py
```python
from modules.common.middleware.rate_limit import RateLimitMiddleware

# Add rate limiting (100 requests/min)
app.add_middleware(RateLimitMiddleware, max_requests=100, window=60)
```

---

### 4. Constants (Global Constants)

#### error_codes.py
```python
from modules.common.constants.error_codes import E001, E002, E_VALIDATION

# Use in error responses
return {"status": "error", "error_code": E001, "message": "Invalid input"}
```

**Common Error Codes**:
- `E001` - Validation error
- `E002` - Not found
- `E003` - Unauthorized
- `E004` - Forbidden
- `E500` - Internal server error

#### status.py
```python
from modules.common.constants.status import STATUS_PENDING, STATUS_ACTIVE

# Use in business logic
if order.status == STATUS_PENDING:
    process_order(order)
```

---

### 5. Interfaces (Repository Pattern)

#### repository.py
```python
from modules.common.interfaces.repository import Repository

class UserRepository(Repository):
    """Implement standard CRUD operations"""
    
    def find_by_id(self, id: str) -> Optional[User]:
        pass
    
    def find_all(self, filter: dict) -> List[User]:
        pass
    
    def create(self, entity: User) -> User:
        pass
    
    def update(self, id: str, entity: User) -> User:
        pass
    
    def delete(self, id: str) -> bool:
        pass
```

---

## Usage Patterns

### Pattern 1: Input Validation
```python
from modules.common.utils.validation import validate_schema, sanitize

def create_user(data: dict):
    # 1. Sanitize
    safe_data = {k: sanitize(v) for k, v in data.items()}
    
    # 2. Validate
    errors = validate_schema(safe_data, USER_SCHEMA)
    if errors:
        return {"status": "error", "errors": errors}
    
    # 3. Process
    user = User.from_dict(safe_data)
    return repository.create(user)
```

### Pattern 2: Error Handling
```python
from modules.common.constants.error_codes import E001, E500

try:
    result = process_data(data)
except ValidationError:
    return {"status": "error", "error_code": E001}
except Exception as e:
    log.error(f"Unexpected error: {e}")
    return {"status": "error", "error_code": E500}
```

### Pattern 3: Middleware Stack
```python
from modules.common.middleware import AuthMiddleware, LoggingMiddleware, RateLimitMiddleware

app.add_middleware(AuthMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=100)
```

---

## Important Notes

### Dependencies
- **common depends on**: Nothing (no upstream)
- **All modules depend on common**: Universal downstream

### Version Compatibility
- Common module uses SemVer
- Breaking changes require major version bump
- All modules must update together when major version changes

### Performance
- All utils optimized for speed
- Encryption/decryption: P95 <10ms
- Validation: P95 <1ms
- Middleware: P95 <5ms overhead

---

## Commands

```bash
# Run common module tests
pytest tests/common/ -v

# Check module health
make module_health_check

# View contract
cat modules/common/doc/CONTRACT.md
```

---

## Related Docs

- **Full README**: [README.md](README.md) (648 lines)
- **Contract**: [doc/CONTRACT.md](doc/CONTRACT.md) (517 lines)
- **Agent Config**: [AGENTS.md](AGENTS.md) (detailed orchestration)
- **Test Plan**: [doc/TEST_PLAN.md](doc/TEST_PLAN.md)

---

**Version**: 1.0  
**Last Updated**: 2025-11-09  
**Lines**: ~150

