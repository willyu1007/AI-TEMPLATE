---
audience: human
language: en
version: reference
purpose: Validation checklist during module init
---
# Module Init - Validation

Before declaring a module ready:
- Tests run (`pytest`, `npm test`, `go test`).
- Guardrails executed (`make agent_trigger_test`).
- Docs updated (contract, runbook, test plan, test data, progress) in English.
- Workdoc statuses refreshed.

Record results in the module workdoc.

