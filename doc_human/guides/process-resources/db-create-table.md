---
audience: human
language: en
version: reference
purpose: Checklist for creating new tables
---
# Create Table Guide

## Steps
1. Define table structure in `schemas/tables/<name>.yaml` (columns, indexes, governance fields).
2. Generate paired migrations and ensure they reference the YAML version.
3. Include mandatory columns: `id uuid`, `created_at`, `updated_at`.
4. Plan indexes/foreign keys with naming convention `idx_<table>_<columns>` / `fk_<table>_<ref>`.
5. Test locally and document in workdoc/runbook.

## Review Criteria
- Adheres to naming, UUID, TIMESTAMPTZ standards.
- Data classification + retention noted.
- Access control list defined.
- Rollback documented.
- Language in comments/logs matches config.

## References
- `db/engines/README.md`
- `doc_human/guides/SCHEMA_GUIDE.md`
- `doc_human/guides/DB_CHANGE_GUIDE.md`
