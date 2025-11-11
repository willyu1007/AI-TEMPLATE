---
audience: ai
language: en
version: summary
purpose: Quick quality standards reference for AI agents
full_version: /doc/policies/quality_standards.md
---

# Quality Standards - Quick Reference

> **For AI Agents** - Essential quality rules (~100 lines)  
> **Full Guide**: [quality_standards.md](quality_standards.md) (402 lines, for humans)

---

## Core Standards (4)

### 1. Code Quality
- Test coverage ≥80% (common module ≥90%)
- Linter pass rate 100%
- Cyclomatic complexity <10
- Type annotations for public APIs

### 2. Documentation
- 8 standard docs per module (README, AGENTS.md, CONTRACT, TEST_PLAN, RUNBOOK, CHANGELOG, BUGS, PROGRESS)
- All docs <90 days old
- No broken links
- Clear structure with headers

### 3. Architecture
- No circular dependencies
- Module coupling <3 dependencies
- Contract backward compatible
- DAG acyclic

### 4. Operations
- All migrations have rollback scripts
- Config files schema-valid
- Observability: logging + metrics + tracing
- No secrets in code

---

## Required Checks (Before Commit)

### Must Pass
```bash
make dev_check  # All 21 checks must pass
```

### Individual Checks
```bash
make agent_lint              # Agent.md validation
make contract_compat_check   # No breaking changes
make test_coverage           # Coverage ≥80%
make secret_scan             # No secrets
make db_lint                 # Database files valid
```

---

## Test Coverage Requirements

### Minimum Coverage
- **All modules**: ≥80%
- **Common module**: ≥90% (infrastructure)
- **New code**: 100% (new features must be fully tested)

### Test Types
```
70% Unit tests    - Function/class level
20% Integration   - Module interactions
10% E2E           - User workflows
```

### Commands
```bash
pytest tests/ --cov=. --cov-fail-under=80
```

---

## Documentation Standards

### 8 Standard Docs (Required)
1. **README.md** - Overview (for humans, can be Chinese)
2. **AGENTS.md** - Orchestration config (for AI, English)
3. **CONTRACT.md** - API interfaces
4. **TEST_PLAN.md** - Test strategy
5. **RUNBOOK.md** - Operations guide
6. **CHANGELOG.md** - Version history
7. **BUGS.md** - Issue tracking
8. **PROGRESS.md** - Development progress

### Freshness
- Update within 90 days
- Mark outdated sections with `⚠️ OUTDATED`
- Archive old docs to `archive/`

### Quality
- No broken links (`make doc_style_check`)
- Clear structure (## headers)
- Code examples tested
- Consistent terminology

---

## Backward Compatibility

### Allowed Changes (Non-Breaking)
- ✅ Add new optional fields
- ✅ Add new endpoints/methods
- ✅ Deprecate (with @deprecated tag, keep 1+ release)
- ✅ Fix bugs (behavior correction)

### Forbidden Changes (Breaking)
- ❌ Remove fields
- ❌ Rename fields (without alias)
- ❌ Change field types
- ❌ Add required fields
- ❌ Remove endpoints/methods

### Process for Breaking Changes
1. Add @deprecated tag
2. Document migration in CHANGELOG
3. Keep deprecated version for 1+ release
4. Coordinate with downstream modules
5. Only remove in next major version

---

## Code Standards

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Files | snake_case | `user_service.py` |
| Functions | snake_case | `get_user()` |
| Classes | PascalCase | `UserService` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY` |
| Private | _prefix | `_internal_helper()` |

### Complexity Limits
- Functions: <50 lines
- Classes: <500 lines
- Cyclomatic complexity: <10
- Nesting depth: <4 levels

### Code Organization
```python
# Order:
1. Imports (stdlib, third-party, local)
2. Constants
3. Classes
4. Functions
5. Main block (if __name__ == "__main__")
```

---

## CI/CD Quality Gates

### Pre-Commit
- Linter passes
- Local tests pass
- No secrets committed

### CI Pipeline
```yaml
gates:
  - lint: must_pass
  - test: must_pass (coverage ≥80%)
  - security_scan: must_pass
  - contract_check: must_pass (if API changes)
  - doc_check: must_pass
```

### Blocking Conditions
- Test coverage <80%
- Any linter errors
- Secrets detected
- Breaking contract changes (without approval)
- Missing required docs

---

## Common Issues & Solutions

### Issue: Test coverage below 80%
```bash
# Check coverage
pytest --cov=. --cov-report=html

# View report
open htmlcov/index.html

# Add tests for uncovered lines
```

### Issue: Linter errors
```bash
# Check errors
pylint modules/

# Auto-fix (if possible)
black modules/
isort modules/
```

### Issue: Breaking contract changes
```bash
# Check compatibility
make contract_compat_check

# If breaking:
# 1. Add @deprecated tag
# 2. Document in CHANGELOG
# 3. Keep for 1+ release
```

---

## Related Docs

- **Full Standards**: [quality_standards.md](quality_standards.md) (402 lines)
- **Security Details**: [security_details.md](security_details.md) (537 lines)
- **AI Coding Guide**: [AI_CODING_GUIDE.md](../process/AI_CODING_GUIDE.md) (371 lines)
- **Health Model**: [HEALTH_CHECK_MODEL.yaml](../process/HEALTH_CHECK_MODEL.yaml)

---

**Version**: 1.0  
**Last Updated**: 2025-11-09  
**Lines**: ~100

