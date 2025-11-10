# Database Engines

> Structure and guardrails for PostgreSQL/Redis assets.

## Layout
```text
db/engines/
├── agent.md                 # Database orchestration agent
├── README.md                # This overview
├── postgres/
│   ├── migrations/          # SQL up/down pairs
│   ├── schemas/             # YAML table definitions
│   └── docs/                # Engine-specific docs
└── redis/
    ├── docs/                # Cache/session guidelines
    ├── schemas/             # Key pattern specifications
    └── scripts/             # Health + housekeeping utilities
```

## Operating Principles
1. Never touch production manually.
2. Every change ships as a pair of migrations (`*_up.sql` / `*_down.sql`).
3. Run `make migrate_check` before merging.
4. Validate rollback with `make rollback_check PREV_REF=<tag>` for high-risk releases.

## PostgreSQL Conventions
- Tables: lowercase snake_case plural (`runs`, `audit_logs`).
- Columns: lowercase snake_case (`user_id`).
- Indexes: `idx_<table>_<column>`.
- Foreign keys: `fk_<table>_<ref_table>`.
- Mandatory columns: `id uuid PRIMARY KEY`, `created_at`, `updated_at`.

### Workflow
1. Describe schema in YAML under `schemas/tables/`.
2. Run `make db_gen_ddl TABLE=<table>` to draft SQL.
3. Review SQL manually (types, indexes, constraints).
4. Apply with `make db_migrate` and capture logs.
5. Run `make rollback_check` against the previous release.

## Redis Conventions
- Keys: `<namespace>:<entity>:<id>[:<attribute>]`.
- TTL: 3600s for cache, 86400s for sessions; document overrides in `schemas/keys/`.
- Data types: prefer String/Hash for cache, List for queues, ZSet for rate limiting.
- Health checks: run `python db/engines/redis/scripts/health_check.py --url redis://localhost:6379`.

## Migration Tips
- Use `IF EXISTS`/`IF NOT EXISTS` to keep scripts idempotent.
- Down scripts must fully revert the up change.
- Keep migrations small; large rewrites require phased plans documented in `doc_human/project/`.

## Helpful Commands
```bash
make db_gen_ddl TABLE=runs
make db_migrate
make db_rollback VERSION=20231110120000
make migrate_check
make db_shell
make db_backup
make db_restore FILE=backup.sql
python db/engines/redis/scripts/health_check.py --url redis://localhost:6379
```

## References
- `db/engines/postgres/docs/SCHEMA_GUIDE.md`
- `db/engines/redis/docs/CACHE_GUIDE.md`
- `doc_human/guides/DB_CHANGE_GUIDE.md`
- `doc_agent/quickstart/dataflow-quickstart.md` (for data lineage context)

