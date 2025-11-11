# Common Module - Change Log

> **Version**: 1.0.0  
> **Last Updated**: 2025-11-09

---

## [1.0.0] - 2025-11-09

### Added
- **Directory Structure**: Moved from `/common/` to `/modules/common/` (Phase 14.0.1)
- **Module Registration**: Added `AGENTS.md` for AI orchestration support
- **Documentation**: Created complete API contract (CONTRACT.md)
- **Initial Release**: Established as infrastructure module

### Features
- String utilities (camel_to_snake, snake_to_camel, truncate_string, normalize_string)
- Date/time utilities (now_utc, format_datetime, parse_datetime, time_ago)
- Validation utilities (validate_email, validate_phone, validate_url, validate_uuid)
- Encryption utilities (hash_password, verify_password, encrypt_data, decrypt_data)
- Data models (BaseModel, PaginationParams, PaginationResult, ApiResponse)
- Middleware (require_auth, rate_limit, setup_logging, logging functions)
- Constants (ErrorCode, Status, UserStatus, OrderStatus)
- Interfaces (Repository, CRUDRepository)

### Migration Guide
If you were importing from `common.*`, update to `modules.common.*`:

```python
# Old (before 1.0.0)
from common.utils import validate_email

# New (1.0.0+)
from modules.common.utils import validate_email
```

**Note**: Old import paths still work temporarily but will be removed in future versions.

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2025-11-09 | Initial release as modules.common |
| 0.x.x | < 2025-11-09 | Pre-release as /common/ (legacy) |

---

## Future Plans

### v1.1.0 (Planned)
- [ ] Add async versions of utility functions
- [ ] Enhance error handling with custom exceptions
- [ ] Add more date/time utilities (timezone conversion, etc.)
- [ ] Expand validation utilities (credit card, IBAN, etc.)

### v1.2.0 (Planned)
- [ ] Add caching utilities
- [ ] Add retry/circuit breaker middleware
- [ ] Add observability hooks (metrics, tracing)

### v2.0.0 (Breaking Changes - TBD)
- [ ] Remove deprecated `common.*` import paths
- [ ] Refactor encryption utilities with production-grade libraries
- [ ] Modernize type hints for Python 3.10+

---

## Deprecation Notices

### None Currently

All APIs in 1.0.0 are stable and supported.

---

## Contributing

When adding new features to common module:

1. **Follow Principles**:
   - Zero business logic
   - Generic and reusable
   - Backward compatible
   - ≥90% test coverage

2. **Update Documentation**:
   - Add to CONTRACT.md (API documentation)
   - Update README.md (usage examples)
   - Add entry to this CHANGELOG.md

3. **Testing**:
   - Write comprehensive unit tests
   - Verify coverage: `pytest tests/common/ --cov=modules.common`
   - Run full dev check: `make dev_check`

4. **Review Checklist**:
   - [ ] No dependencies on business modules
   - [ ] All public APIs documented
   - [ ] Tests cover ≥90% of new code
   - [ ] CHANGELOG.md updated
   - [ ] README.md quick reference updated
   - [ ] CONTRACT.md API documented

---

**Maintained by**: Project Team  
**Last Reviewed**: 2025-11-09

