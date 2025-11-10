---
audience: human
language: en
version: reference
purpose: Release planning template
---
# Release Train

## Cadence
- Two-week iterations (adjust as needed).
- Code freeze 2 days before release.
- Guardrail + doc reviews on day -1.

## Checklist
1. `make dev_check` clean on release branch.
2. Guardrail stats reviewed (`scripts/guardrail_stats.py`).
3. Docs updated (README, QUICK_START, workdocs).
4. Release notes drafted (include language reminder and guardrail changes).
5. Rollback plan validated.

## Roles
- Release Manager: coordinates schedule.
- Module Owners: verify readiness.
- QA/Reviewers: run manual/automated tests as needed.

## Communication
- Publish status in workdoc.
- Notify stakeholders (Slack/email) with release notes.

Keep this document short and adapt per project.
