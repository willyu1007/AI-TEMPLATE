---
audience: ai
language: en
version: summary
purpose: Fast reference for guardrail usage
---
# Guardrail Quickstart

> Keep this file loaded before touching risky areas. For the story-level explanation, see `doc_human/guides/GUARDRAIL_GUIDE.md`.

## Protection Levels
| Level | Action | Examples |
|-------|--------|----------|
| Block | Stop immediately | DB schema, prod config, contract removals |
| Warn | Require explicit confirmation | Staging config, fixture rewrites, agent routing |
| Suggest | Recommend best practice | Workflow patterns, test coverage nudges |

## Core Block Rules
1. **database-schema-change** - Requires paired up/down migrations, updated YAML schema, rollback plan.
2. **contract-breaking-change** - Requires compatibility review, baseline update, migration docs.
3. **production-config-change** - Needs change request + rollback instructions before editing `config/prod.yaml`.
4. **dependency-major-update** - Run regression tests + staged rollout before bumping major versions.

## Core Warn Rules
- **test-data-modification** - Verify fixtures and tests after changes.
- **staging-config-change** - Announce and validate in staging before merge.
- **agent-routing-change** - Re-run `make doc_route_check` and update doc roles.

## Suggest Rules
- Workflow pattern suggestions (module creation, bug fix, DB migration, etc.).
- Dataflow analysis reminder when refactoring modules.
- Documentation/test reminders when code changes lack updates.

## Trigger Sources
```yaml
file_triggers:
  - rule_id: database-schema-change
    execution_mode: block
    patterns:
      paths:
        - pattern: "db/engines/*/migrations/*.sql"
        - pattern: "db/engines/*/schemas/*.yaml"

prompt_triggers:
  - rule_id: workflow-pattern-suggestion
    execution_mode: suggest
    patterns:
      keywords: ["create", "scaffold", "migrate", "fix"]
```

## Commands
```bash
make agent_trigger FILE=db/engines/postgres/migrations/002.sql
make agent_trigger_prompt PROMPT="migrate the orders table"
make agent_trigger_test
```
`make dev_check` runs guardrails automatically.

## Working With Blockers
1. Read the error message and load the recommended docs.
2. Update the required artifacts (e.g., add down migration, document contract deprecation).
3. Re-run the trigger command to confirm the block is cleared.
4. Capture the guardrail outcome in your workdoc context so humans know what happened.

## Adding A Rule
1. Edit `doc_agent/orchestration/agent-triggers.yaml`.
2. Provide `rule_id`, description, severity, execution mode, and patterns.
3. Optional: `documents_to_load`, `skip_conditions`, `auto_actions`.
4. Validate with `make agent_trigger_test`.

Keep guardrail outputs in the configured language and avoid vague instructions¡ªalways point to the next action.

