---
audience: human
language: en
version: reference
purpose: PR workflow reference
---
# Pull Request Workflow

## Steps
1. Create an issue/workdoc describing the change.
2. Open a feature branch (`git checkout -b feature/<topic>`).
3. Make changes, update docs/tests, run `make dev_check`.
4. Push branch and open PR with template:
```
## Summary
- ...

## Testing
- [ ] make dev_check
- [ ] Other checks

## Docs
- Updated files: ...

## Guardrails
- Blocks/warnings and resolutions
```
5. Address review comments, keep commits tidy.
6. Merge after approvals and green checks.

## Rules
- At least one maintainer approval + CI green.
- No force push to `main`.
- Keep PRs small (<400 lines touched when possible).
- Document language reminders when onboarding contributors.

## References
- `CONTRIBUTING.md`
- `agent.md` (code review section)
