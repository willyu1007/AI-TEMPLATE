---
audience: human
language: en
version: reference
purpose: Operational guide for database changes
---
# Database Change Guide

## Scope
Covers schema changes, data backfills, and performance-related migrations.

## Workflow
1. **Plan** - define impact, downtime requirements, rollback plan. Document in workdoc.
2. **Design** - update table YAML + `DB_SPEC.yaml`. Consider feature flags or dual writes if needed.
3. **Implement** - create paired migrations, run `make migrate_check` + `make db_lint`.
4. **Test** - apply to staging, run smoke + regression tests, record metrics.
5. **Deploy** - schedule change window, backup data, execute migrations, monitor.
6. **Verify** - run post-change checks (queries, dashboards) and capture results.

## Best Practices
- Prefer additive changes; mark columns deprecated before removal.
- Use concurrent index creation for large tables.
- Split large updates into batches to avoid locks.
- Always document language/localization expectations for generated data.

## Tools
- `scripts/db_lint.py`
- `scripts/migrate_check.py`
- `scripts/rollback_check.sh`
- `doc_agent/quickstart/guardrail-quickstart.md` (block rules).

## References
- `db/engines/README.md`
- `db/engines/postgres/migrations/README.md`
- `doc_human/guides/SCHEMA_GUIDE.md`

