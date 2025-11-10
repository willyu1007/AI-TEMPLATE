# Schema Guide

## Goals
- Provide consistent rules for Postgres schema design.
- Keep migrations safe, reversible, and well documented.

## Core Rules
1. **Primary Keys** - UUID v7 (globally unique + sortable).
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```
2. **Timestamps** - Always use `TIMESTAMPTZ`. Maintain `created_at`/`updated_at` via trigger `update_updated_at_column()`.
3. **Index Names** - `idx_<table>_<columns>` (e.g., `idx_orders_user_id_status`).
4. **Foreign Keys** - Specify cascading behavior explicitly.
5. **Naming** - snake_case everywhere; booleans prefixed with `is_`/`has_`; foreign keys `<table>_id`.

## Change Process
1. Update table YAML (`schemas/tables/*.yaml`) and `DB_SPEC.yaml`.
2. Create paired migrations (`<version>_<desc>_up.sql`/`down.sql`).
3. Run `make migrate_check` and test SQL in dev DB.
4. Update this guide (if rules changed) and regenerate docs with `make docgen`.
5. Capture impacts in relevant module docs/workdocs.

## Validation
```bash
make migrate_check
psql -d test_db -f migrations/<version>_up.sql
psql -d test_db -f migrations/<version>_down.sql
```
Check table details with `\d+ table_name`.

## Rollback
- Execute the down script.
- Revert application changes if necessary.
- Run smoke tests and monitor metrics.

## Performance Tips
- Build indexes concurrently on large tables.
- Use phased migrations for heavy updates (backfill, then enforce constraints).
- Limit the number of indexes to balance read vs write performance.

## References
- `DB_SPEC.yaml`
- `../migrations/README.md`
- `doc_human/guides/DB_CHANGE_GUIDE.md`

