# Postgres Migrations

Manage schema evolution with paired SQL scripts. Every change must be traceable and reversible.

## Naming
```
<version>_<description>_up.sql
<version>_<description>_down.sql
```
Example: `002_add_orders_table_up.sql`.

## Rules
1. Up/Down pairs are mandatory (`make migrate_check`).
2. Scripts must be idempotent (`IF EXISTS/IF NOT EXISTS`).
3. Wrap statements in transactions when possible.
4. Favor backward-compatible changes (add columns nullable, deprecate before delete).

## Workflow
1. Create paired files.
2. Write SQL (use `CONCURRENTLY` for large indexes, batch updates for huge datasets).
3. Run locally: `psql -d dev_db -f migrations/XXX_up.sql` and `..._down.sql`.
4. Update table YAML (`schemas/tables/*.yaml`) with the new version.
5. Execute in CI via `make migrate_check` and `make db_lint`.
6. In production, backup first, run during a window, and monitor metrics.

## Rollback
- Triggered by failures, regressions, or SLA breaches.
- Apply the `_down.sql` script, verify schema, restart services if required, and run smoke tests.
- Target <15 minutes total (execution + verification).

## Related Docs
- `../docs/SCHEMA_GUIDE.md`
- `../../../../scripts/rollback_check.sh`
- `doc_human/guides/DB_CHANGE_GUIDE.md`
