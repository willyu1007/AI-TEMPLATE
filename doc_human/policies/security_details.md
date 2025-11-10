---
audience: human
language: en
version: reference
purpose: Security implementation details
---
# Security Details

## Principles
- Least privilege for configs, services, and CI tokens.
- Secrets stay outside git; use vaults or environment-specific secret stores.
- Guardrails block risky operations (production config, schema changes, contract removals).
- Logs and docs never include sensitive values; redact before sharing.

## Checklist
- [ ] Run `scripts/secret_scan.py`.
- [ ] Validate access controls in table YAML (`access_control` field).
- [ ] Review permissions for CI runners and automation scripts.
- [ ] Document incidents + mitigations in workdocs/runbooks.

## Language Policy
Security documentation, alerts, and runbooks must match `config/language.yaml`. Update that file during initialization and remind teams when onboarding.

## References
- `config/README.md`
- `doc_agent/quickstart/guardrail-quickstart.md`
- `modules/<name>/doc/RUNBOOK.md`
