---
spec_version: "1.0"
agent_id: "modules.common.v1"
role: "Provide common utilities and infrastructure code - Shared across all modules"
level: 1
module_type: "0_Infrastructure/Common"

ownership:
  code_paths:
    include:
      - modules/common/utils/*
      - modules/common/models/*
      - modules/common/middleware/*
      - modules/common/constants/*
      - modules/common/interfaces/*
    exclude: []

io:
  inputs:
    - name: "function_call"
      type: "mixed"
      required: true
      description: "Other modules call common utility functions"
      schema_ref: "modules/common/doc/CONTRACT.md#API"
      examples:
        - "validate_email(email: str) -> bool"
        - "PaginationParams(page: int, page_size: int)"
        - "@require_auth decorator"
  
  outputs:
    - name: "function_result"
      type: "mixed"
      required: true
      description: "Return processed/validated data"
      schema_ref: "modules/common/doc/CONTRACT.md#API"
      examples:
        - "bool (validation functions)"
        - "formatted string (string utils)"
        - "model instance (models)"

contracts:
  apis:
    - modules/common/doc/CONTRACT.md

dependencies:
  upstream: []
  downstream: ["*"]  # All modules can use common

constraints:
  - "Zero business logic - only technical utilities"
  - "Test coverage >= 90%"
  - "Backward compatibility required"
  - "No dependencies on business modules"

tools_allowed:
  calls:
    - fs.read
    - fs.write

quality_gates:
  required_tests:
    - unit
  coverage_min: 0.90

policies:
  goals:
    - "Provide stable, reusable utilities"
    - "Maintain zero business logic principle"
    - "Ensure backward compatibility"
    - "Achieve ≥90% test coverage"
  
  safety:
    - "No dependencies on business modules (modules/*)"
    - "All public functions must have unit tests"
    - "Breaking changes require deprecation warnings"
    - "Version compatibility must be maintained"

context_routes:
  always_read:
    - /modules/common/README.md
  
  on_demand:
    - topic: "API Contract"
      paths:
        - /modules/common/doc/CONTRACT.md
    - topic: "Changelog"
      paths:
        - /modules/common/doc/CHANGELOG.md

merge_strategy: "child_overrides_parent"

---

# Common Module - Agent Guide

## Purpose
Provides cross-module shared utilities, models, middleware, and constants. This module contains no business logic, only technical infrastructure.

## Key Principles
1. **Zero Business Logic**: Only generic, reusable technical utilities
2. **Backward Compatibility**: All changes must maintain API stability
3. **High Test Coverage**: ≥90% required for all code
4. **No Module Dependencies**: Cannot import from any business module

## Quick Reference

### Available Utilities
- **String Utils**: `camel_to_snake`, `snake_to_camel`, `truncate_string`, `normalize_string`
- **Date Utils**: `now_utc`, `format_datetime`, `parse_datetime`, `time_ago`
- **Validation**: `validate_email`, `validate_phone`, `validate_url`, `validate_uuid`
- **Encryption**: `hash_password`, `verify_password`, `encrypt_data`, `decrypt_data`
- **Models**: `BaseModel`, `PaginationParams`, `PaginationResult`, `ApiResponse`
- **Middleware**: `require_auth`, `rate_limit`, `setup_logging`
- **Constants**: `ErrorCode`, `Status`, `UserStatus`, `OrderStatus`

### Usage Example
```python
# Import utilities
from modules.common.utils import validate_email, now_utc
from modules.common.models import PaginationParams
from modules.common.constants import ErrorCode

# Use in your code
if not validate_email(email):
    raise ValueError(ErrorCode.INVALID_EMAIL.value)

params = PaginationParams(page=1, page_size=20)
```

## Modification Guidelines

### When to Add Code
✅ **Add to common/** when:
- At least 2 modules need this functionality
- Code is stable and generic
- No business logic involved

❌ **Don't add** when:
- Only one module uses it
- Contains business rules
- Module-specific logic

### Adding New Functions
1. Determine the category (utils/models/middleware/constants/interfaces)
2. Implement with full unit tests (≥90% coverage)
3. Update `/modules/common/README.md` quick reference
4. Update `/modules/common/doc/CONTRACT.md` API documentation
5. Add entry to `__init__.py` for easy import
6. Run `pytest tests/common/ --cov=modules.common`

### Deprecation Process
1. Mark function with `@deprecated` decorator
2. Keep old version for at least one release cycle
3. Document migration path in CHANGELOG.md
4. Update all known callers
5. Remove in next major version

## Verification Commands
```bash
# Run common module tests
pytest tests/common/ -v --cov=modules.common

# Check coverage
pytest tests/common/ --cov=modules.common --cov-report=html

# Verify no circular dependencies
grep -r "from modules\." modules/common/
# (Should return no results)

# Run full dev check
make dev_check
```

## Related Documents
- Full Documentation: `/modules/common/README.md`
- API Contract: `/modules/common/doc/CONTRACT.md`
- Change History: `/modules/common/doc/CHANGELOG.md`
- Testing Guide: `/doc/process/testing.md`

