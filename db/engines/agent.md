---
spec_version: "1.0"
agent_id: "db_engines"
role: "Database schema, migration, and engine management"

policies:
  goals_ref: /doc_agent/policies/goals.md
  safety_ref: /doc_agent/policies/safety.md

parent_agent: /agent.md
merge_strategy: "child_overrides_parent"

context_routes:
  always_read:
    - /db/engines/README.md
  on_demand:
    - topic: "Database Operations"
      priority: high
      paths:
        - /doc_agent/specs/DB_SPEC.yaml
        - /doc_human/guides/SCHEMA_GUIDE.md
    - topic: "Database Changes"
      priority: high
      paths:
        - /doc_human/guides/DB_CHANGE_GUIDE.md
        - /db/engines/postgres/schemas/tables/runs.yaml
        - /db/engines/postgres/docs/DB_SPEC.yaml
    - topic: "Redis Operations"
      priority: medium
      paths:
        - /db/engines/redis/README.md
        - /db/engines/redis/docs/CACHE_GUIDE.md

constraints:
  - "Never touch production manually"
  - "Every change must have up/down migrations"
  - "All migrations must be idempotent"
  - "Must pass migrate_check before merging"
---
# Database Engines Agent Guide

> Template-controlled schemas, migrations, and engine configs live here. Follow these notes to keep database work safe.

## Scope
- PostgreSQL is the primary engine; Redis templates live alongside if needed.
- Every migration must ship with up and down scripts plus YAML schema updates.
- Never touch production manually; always go through make targets.

## Context Shortcuts
| Need | Load | Purpose |
| --- | --- | --- |
| Directory overview | `/db/engines/README.md` | Layout plus guardrails |
| DB spec (AI) | `/doc_agent/specs/DB_SPEC.yaml` | Field level rules and tooling hooks |
| Change process (human) | `/doc_human/guides/DB_CHANGE_GUIDE.md` | Approval steps |
| Schema reference | `/db/engines/postgres/docs/DB_SPEC.yaml` | Engine specific details |

## Working Sequence
1. Model the change in `postgres/schemas/tables/*.yaml`.
2. Generate timestamped migrations (up plus down) under `postgres/migrations/`.
3. Run `make db_migrate` locally, followed by `make rollback_check PREV_REF=<target>` if risky.
4. Commit schema YAML plus migrations together and update docs if APIs change.

## Commands
```bash
make db_migrate
make db_schema_diff
make db_rollback VERSION=<timestamp>
make rollback_check PREV_REF=<timestamp>
```

## Safety Rules
- Migrations must be idempotent (use IF EXISTS or IF NOT EXISTS).
- Do not edit applied migrations; create a follow-up fix.
- Record destructive operations inside workdocs plus the PR description.
- Keep long running data updates batched and monitored.

## References
- `/db/engines/README.md`
- `/doc_agent/specs/DB_SPEC.yaml`
- `/doc_human/guides/DB_CHANGE_GUIDE.md`
- `/db/engines/postgres/docs/DB_SPEC.yaml`

Versioning follows git and migration timestamps; no extra agent version needed.

