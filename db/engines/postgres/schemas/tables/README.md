# Table Schema YAMLs

Use this folder to describe every Postgres table in YAML so automation can lint, document, and reason about schemas.

## Naming
- `<table>.yaml` (snake_case, matches real table name).
- One file per table.

## Minimal Structure
```yaml
meta:
  table_name: runs
  description: "Execution history"
  migration_version: "001"
  owner: "observability"

table:
  name: runs
  schema: public
  columns:
    - name: id
      type: uuid
      nullable: false
      description: "Primary key"
  indexes:
    - name: idx_runs_created_at
      columns: [created_at]

migrations:
  up: "../migrations/001_create_runs_up.sql"
  down: "../migrations/001_create_runs_down.sql"
```
Add `relationships`, `sensitivity`, `retention_days`, and `access_control` as needed.

## Workflow
1. Create the YAML file when you add/alter a table.
2. Update it whenever the schema changes.
3. Keep `migration_version` aligned with the latest SQL migration.
4. Run `make db_lint` to validate formatting and references.

## Best Practices
- Every column/index needs a description.
- Document foreign keys in `relationships`.
- Track data governance fields (sensitivity, retention, access_control).
- Include sample queries or performance notes in `example_queries` if helpful.

See `runs.yaml` for a full example and `../../docs/SCHEMA_GUIDE.md` for detailed guidance.
