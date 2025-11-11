# Schemas Directory

## Purpose
Collect every schema used to validate configuration, documentation front matter, or database definitions.

## Contents
### `agent.schema.yaml`
- Describes required fields for `AGENTS.md` (`spec_version`, `agent_id`, `role`, etc.).
- Consumed by `scripts/agent_lint.py`.
- Update when you add new front-matter fields or context routes.

### Upcoming Schemas
- `db/table.schema.yaml` (planned) - normalize table YAML structure for Postgres specs.
- Add more schemas as automation grows (e.g., guardrail configs, workflow patterns).

## Usage Pattern
1. Create the schema under `schemas/`.
2. Load it inside a script (`yaml.safe_load`).
3. Validate data with `jsonschema` or a custom validator.
4. Document the schema here and note which script uses it.

## Dependencies
Install `pyyaml` and `jsonschema` to validate schemas:
```bash
pip install pyyaml jsonschema
```

## Maintenance Checklist
- Update this README whenever you add/change a schema.
- Keep schema files versioned (use a `version` field if breaking changes are possible).
- Add tests for scripts that consume schemas.

Schemas are configuration assets, so they do not require individual `AGENTS.md` files.

