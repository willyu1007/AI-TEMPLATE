---
audience: human
language: en
version: reference
purpose: Walkthrough for writing DB migration scripts
---
# Migration Script Guide

## Template
```
BEGIN;
-- change
COMMIT;
```
Include paired `_up.sql` and `_down.sql` files with sequential versions.

## Steps
1. Update schema YAML + DB spec.
2. Create paired files (`touch 003_add_orders_up.sql` etc.).
3. Write idempotent SQL (use `IF EXISTS/IF NOT EXISTS`).
4. Test locally + staging (`psql -d <db> -f file.sql`).
5. Run `make migrate_check` + `make rollback_check`.
6. Attach output/logs to workdoc.

## Checklist
- [ ] Transactions wrap statements.
- [ ] Uses concurrent index creation when needed.
- [ ] Down script fully reverses changes.
- [ ] Comments explain complex steps (in English).
- [ ] Guardrail rules updated if new file patterns introduced.

## References
- `db/engines/postgres/migrations/README.md`
- `doc_human/guides/DB_CHANGE_GUIDE.md`
