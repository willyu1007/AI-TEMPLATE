---
audience: human
language: en
version: reference
purpose: Checklist for altering existing tables
---
# Alter Table Guide

## Workflow
1. Document motivation + risk in workdoc.
2. Update table YAML (`columns`, `indexes`, governance fields).
3. Write additive migrations first (add nullable column, backfill data, enforce constraints later).
4. Validate in staging; capture metrics.
5. Plan rollback (drop column, revert data, remove constraints).

## Tips
- Use feature flags or dual writes when changing critical fields.
- Avoid locking large tables; batch updates or use background jobs.
- Communicate with downstream consumers about schema changes.

## Checklist
- [ ] Migration pair created.
- [ ] Data backfill plan documented.
- [ ] Tests updated (unit, integration, contract).
- [ ] Docs updated (CONTRACT, TEST_DATA, RUNBOOK).

## References
- `doc_human/guides/DB_CHANGE_GUIDE.md`
- `db/engines/postgres/migrations/README.md`
