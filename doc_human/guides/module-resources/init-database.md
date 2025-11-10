---
audience: human
language: en
version: reference
purpose: Database checklist during module init
---
# Module Init - Database

- Define tables in `schemas/tables/*.yaml`.
- Create paired migrations.
- Document data classification, retention, and access control.
- Run guardrails (`make migrate_check`, `make agent_trigger FILE=...`).
- Note language requirements for seeded data and comments.

