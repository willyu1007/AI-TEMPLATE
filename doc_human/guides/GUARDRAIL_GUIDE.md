---
audience: human
language: en
version: reference
purpose: Full explanation of guardrail governance
---
# Guardrail Guide

## Purpose
Provide human operators with the full context behind guardrail rules, escalation paths, and exceptions.

## Structure
- **Overview** - goals, severity levels, reporting metrics.
- **Rule Catalog** - for each rule capture ID, scope, detection method, required remediation, owner.
- **Override Process** - who can grant exceptions, how to document them, expiry dates.
- **Monitoring** - dashboards/scripts that track guardrail hits (`scripts/guardrail_stats.py`).

## Workflow
1. Propose rule changes via workdoc (include risk, trigger logic, affected files).
2. Update `doc_agent/orchestration/agent-triggers.yaml` and this guide simultaneously.
3. Communicate via release notes and ensure `guardrail-quickstart` stays <=150 lines.
4. Review metrics weekly; tune keywords/paths to reduce false positives.

## Escalation
- Block ¡ú requires maintainer approval + documented mitigation.
- Warn ¡ú developer confirms they read the warning; maintainers spot-check logs.
- Suggest ¡ú optional but log usage to improve automation.

## Language Policy
All guardrail messages, docs, and comments follow `config/language.yaml`. Update the config if your project needs a different language and regenerate docs/scripts accordingly.

## References
- `doc_agent/quickstart/guardrail-quickstart.md`
- `scripts/agent_trigger.py`
- `doc_human/templates/workdoc-context.md` (record guardrail outcomes).

