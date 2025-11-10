---
audience: human
language: en
version: reference
purpose: Safety policy
---
# Safety Policy

- Guardrails must block destructive operations (DB schema, production config, contract removals).
- Secrets stay outside git; never log or share them in docs.
- Follow language rules from `config/language.yaml` when writing comments, docs, or alerts.
- Document all overrides with owner, reason, and expiry.
- Run safety checks (`make agent_trigger_test`) before every release.
