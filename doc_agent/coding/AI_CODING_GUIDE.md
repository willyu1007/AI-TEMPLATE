# AI Coding Guide

> Lightweight rulebook for coding agents. Keep it concise, actionable, and aligned with the human `CONVENTIONS.md` guide.

## Principles
1. Clarity > cleverness; explicit > implicit.
2. Follow existing patterns before inventing new ones.
3. Security and tests are non-negotiable.

## Naming Patterns
- Python: `PascalCase` classes, `snake_case` functions, `UPPER_SNAKE` constants.
- TypeScript: `PascalCase` classes, `camelCase` methods, `UPPER_SNAKE` constants.
- Go: exported identifiers use `PascalCase`; private ones use `camelCase`.

## Comment & Docstring Policy
Add context for:
- Non-trivial algorithms or business rules.
- Public APIs/interfaces.
- TODO/FIXME/HACK markers with owners + deadlines.
Keep docstrings short and English only; reference design docs instead of repeating them.

## Error Handling
- Catch specific exceptions/errors.
- Provide actionable log messages.
- Clean up resources (files, DB sessions) on failure.

## Security Checklist
- Validate all external input.
- Use parameterized queries and ORM helpers.
- Hash secrets; never log them.
- Enforce authorization before mutating state.

## Testing Expectations
- Unit + integration tests for every meaningful change.
- Cover success, edge, and failure paths.
- Update module `TEST_PLAN.md` when acceptance criteria shift.

## Pull Request Ready Checklist
- [ ] Code styled (linters pass).
- [ ] Inputs validated.
- [ ] Errors handled intentionally.
- [ ] Tests added/updated and green.
- [ ] Docs updated with correct language headers.
- [ ] Guardrails reviewed if risky areas touched.

## Common Scenarios
- **New API**: scaffold route ¡ú validate payload ¡ú implement logic ¡ú tests ¡ú update OpenAPI + docs.
- **Bug fix**: reproduce ¡ú test first ¡ú minimal fix ¡ú regression test ¡ú update workdoc.
- **DB change**: follow `doc_human/guides/DB_CHANGE_GUIDE.md`, create migration pair, run `make migrate_check` and `make rollback_check`.
- **Test data**: prefer fixtures for <50 records; use mock generators for larger data sets.

## Performance Tips
- Avoid N+1 queries; batch or prefetch related data.
- Cache expensive calculations when safe.
- Measure first; do not micro-optimize blindly.

## Automation Hooks
- `make dev_check` runs lint, tests, doc checks, and guardrails.
- `scripts/ai_friendliness_check.py` verifies language + structure.
- `scripts/refactor_suggest.py` offers hints before large cleanups.

Stay within the configured language (English by default) for comments, docstrings, and log messages.
