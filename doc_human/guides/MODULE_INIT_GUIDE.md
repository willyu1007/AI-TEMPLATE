---
audience: human
language: en
version: reference
purpose: Detailed instructions for initializing modules
---
# Module Initialization Guide

## Steps
1. **Plan** - create a workdoc, define scope, confirm language setting.
2. **Scaffold** - `make ai_begin MODULE=<name>` (generates agent file, docs, tests).
3. **Configure** - update `modules/<name>/AGENTS.md`, register contexts in root `AGENTS.md` if needed.
4. **Document** - fill in `doc/CONTRACT.md`, `RUNBOOK.md`, `TEST_PLAN.md`, `TEST_DATA.md`, `PROGRESS.md`.
5. **Wire Tests** - update `tests/<name>/` and CI targets.
6. **Register** - add module metadata to `doc_human/guides/MODULE_INSTANCES.md` and `doc_agent/orchestration/registry.yaml` if applicable.

## Best Practices
- Keep generated docs in English unless `language.yaml` dictates otherwise.
- Document guardrail coverage early (DB, contract, workflow).
- Establish logging/metrics hooks from day one.
- Schedule periodic module health reviews.

## References
- `doc_agent/quickstart/module-init.md`
- `doc_human/templates/module-templates/`
- `Makefile` targets (`ai_begin`, `module_doc_gen`).

