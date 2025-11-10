---
audience: human
language: en
version: reference
purpose: Configuration governance guide
---
# Configuration Guide

## Purpose
Explain how to manage environment-specific configuration safely.

## Files
- `config/schema.yaml` - canonical schema.
- `config/defaults.yaml` - baseline values.
- `<env>.yaml` - overrides (dev/staging/prod).
- `.secrets.yaml` - local secrets (never commit).
- `config/language.yaml` - repository language + localization notes.

## Workflow
1. Update schema before touching values.
2. Modify the relevant `<env>.yaml`; keep production changes blocked behind approvals.
3. Run `make runtime_config_check` and `make doc_style_check`.
4. Document changes in workdocs + release notes.
5. Communicate language changes during project initialization.

## Guardrails
- Production config edits require change request + rollback plan.
- Keep comments/logs/docs aligned with `language.yaml`.
- Secrets live in vault solutions; `.secrets.yaml` is only for local mocks.

## References
- `config/README.md`
- `doc_agent/quickstart/guardrail-quickstart.md`
- `doc_human/guides/PROJECT_INIT_GUIDE.md`

