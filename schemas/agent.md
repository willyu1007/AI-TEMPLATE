---
spec_version: "1.0"
agent_id: "schemas"
role: "Schema definitions and validation rules for configuration and documentation"

policies:
  goals_ref: /doc_agent/policies/goals.md
  safety_ref: /doc_agent/policies/safety.md

parent_agent: /agent.md
merge_strategy: "child_overrides_parent"

context_routes:
  always_read:
    - /schemas/README.md
  on_demand:
    - topic: "Agent Configuration Schema"
      priority: high
      paths:
        - /schemas/agent.schema.yaml
---
# Schemas Agent Guide

> Schemas keep structured assets machine-checkable. Start here before editing agent files, config, or workflow specs.

## Scope
- Maintain JSON or YAML schemas that guard docs, config, and orchestration metadata.
- Provide a single validation surface (`scripts/agent_lint.py`, `scripts/config_lint.py`, etc).
- Document future schema additions inside `/schemas/README.md`.

## Context Shortcuts
| Need | Load | Purpose |
| --- | --- | --- |
| Directory overview | `/schemas/README.md` | Explains active vs planned schemas |
| Agent schema | `/schemas/agent.schema.yaml` | Contract for every agent.md |
| Quality expectations | `/doc_agent/policies/quality.md` | Rules for schema coverage |

## Working Cycle
1. Update or add schema YAML inside `schemas/`.
2. Re-run the relevant lint (`make agent_lint`, `make config_lint`, or custom script).
3. Fix the offending files or relax the schema with justification.
4. Document the addition in `/schemas/README.md`.

## Commands
```bash
make agent_lint                # Validate all agent.md files
make config_lint               # Validate config YAML
python scripts/agent_lint.py --file path/to/agent.md
```

## Good Practices
- Use descriptive property names and clear enums.
- Mark optional fields explicitly; do not rely on implicit defaults.
- Keep schemas language-agnostic so Python, Go, and TypeScript loaders stay in sync.
- Version bump schemas only when semantics change, not when comments update.

## References
- `/schemas/README.md`
- `/schemas/agent.schema.yaml`
- `/doc_agent/policies/quality.md`

Version control is inherited from git; this agent file stays unversioned.

