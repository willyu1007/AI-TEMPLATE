# Common Module

Shared utilities, models, middleware, constants, and interfaces used by multiple feature modules. Keep it small, stable, and business-agnostic.

## Layout
```text
modules/common/
|-- utils/         # string/date/validation/encryption helpers
|-- models/        # base models + DTOs
|-- middleware/    # auth/logging/rate limit middleware
|-- constants/     # error codes, statuses
`-- interfaces/    # shared protocols (e.g., repository interface)
```

## Principles
1. **Minimal surface** - only add code used by >=2 modules.
2. **No business logic** - keep domain-specific rules inside each module.
3. **Compatibility** - changes must be backward compatible or include deprecation paths.
4. **Tests first** - coverage ¡Ý90% for this package.

## Contribution Checklist
- [ ] Confirm at least two modules need the helper.
- [ ] Implement feature with clear function/class docstrings.
- [ ] Export helpers via the relevant `__init__.py`.
- [ ] Add/extend tests under `tests/common/` and keep coverage high.
- [ ] Update docs (`modules/common/doc/*.md`) and this README.
- [ ] Run `pytest tests/common/ -v` and `make dev_check`.

## Example Helpers
- `utils.string_utils` - slugify, normalize, case conversion.
- `utils.validation` - email/user validators, schema helpers.
- `middleware.auth` - shared auth decorator/middleware for services.
- `constants.error_codes` - canonical error codes used by APIs.

## Guardrails
- No imports from `modules/<feature>` (prevents cycles).
- Heavy IO operations belong in feature modules, not here.
- Document breaking changes in `modules/common/doc/CHANGELOG.md` before merging.

## References
- `modules/common/doc/*.md` - contract, test plan, runbook, etc.
- `tests/common/` - coverage examples.
- `agent.md` - module policies.

