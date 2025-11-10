# Common Module - AI Optimization Guide

## Token-Efficient Usage (100 tokens)

### Import Strategy
```python
# ❌ Avoid: Import everything
from modules.common import *

# ✅ Preferred: Specific imports
from modules.common.utils.validation import validate_email
from modules.common.models.base import BaseModel
```

### Quick Reference Table

| Need | Import | Tokens |
|------|--------|--------|
| Validation | `utils.validation` | ~50 |
| Base Models | `models.base` | ~30 |
| Auth | `middleware.auth` | ~80 |
| Encryption | `utils.encryption` | ~60 |
| Rate Limit | `middleware.rate_limit` | ~40 |

## Minimal Examples (150 tokens)

### 1. Data Validation
```python
from modules.common.utils.validation import validate_email, validate_url

# Quick validation
is_valid = validate_email("user@example.com")
```

### 2. Model Creation
```python
from modules.common.models.base import BaseModel

@dataclass
class MyModel(BaseModel):
    name: str
    value: int
```

### 3. Auth Middleware
```python
from modules.common.middleware.auth import require_auth

@require_auth
def protected_endpoint(*, current_user=None):
    return {"user": current_user["user_id"]}
```

## Pattern Library (100 tokens)

### Error Handling Pattern
```python
from modules.common.constants.error_codes import ErrorCode

def safe_operation():
    try:
        # operation
        return {"success": True}
    except Exception as e:
        return {"error": ErrorCode.INTERNAL_ERROR}
```

### Pagination Pattern
```python
from modules.common.models.common import PaginationParams

def list_items(pagination: PaginationParams):
    offset = (pagination.page - 1) * pagination.page_size
    return items[offset:offset + pagination.page_size]
```

## Testing Quick Guide (50 tokens)

```bash
# Run common module tests
pytest tests/common/ -v

# Check coverage
pytest tests/common/ --cov=modules.common

# Type checking
mypy modules/common/
```

## Dependencies Map
```
common/
├── utils/       # No dependencies
├── models/      # Depends on: utils
├── middleware/  # Depends on: models, utils
└── constants/   # No dependencies
```

---
*Total: ~400 tokens - Optimized for AI context loading*
