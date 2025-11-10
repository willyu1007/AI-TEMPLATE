---
audience: human
language: en
version: reference
purpose: Human-friendly schema governance playbook
---
# Schema Guide (Human)

## Purpose
Document the why behind our Postgres schema rules, supplementing the AI quick references.

## Key Policies
- UUID v7 primary keys, TIMESTAMPTZ timestamps.
- One migration per logical change, always paired up/down.
- Table YAMLs kept in sync with SQL.
- Document sensitivity, retention, and access requirements for every table.

## Change Process
1. Propose change in a workdoc (include risk analysis, rollout, rollback).
2. Update YAML + `DB_SPEC.yaml`.
3. Create migrations and run `make migrate_check` + `make rollback_check`.
4. Update affected module docs (contracts, runbooks).
5. Communicate via release notes.

## Governance
- DB reviewer must approve structural changes.
- Sensitive data requires sign-off from security owner.
- Keep metrics on migration duration and failures.

## References
- `db/engines/README.md`
- `db/engines/postgres/docs/SCHEMA_GUIDE.md`
- `doc_human/guides/DB_CHANGE_GUIDE.md`
