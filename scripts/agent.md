---
spec_version: "1.0"
agent_id: "scripts"
role: "Automation scripts for validation, maintenance, and development workflows"

policies:
  goals_ref: /doc_agent/policies/goals.md
  safety_ref: /doc_agent/policies/safety.md

parent_agent: /agent.md
merge_strategy: "child_overrides_parent"

context_routes:
  always_read:
    - /scripts/README.md
  on_demand:
    - topic: "Makefile Commands"
      priority: high
      when: "Need concrete make targets or command references."
      paths:
        - /doc_human/reference/commands.md
    - topic: "Context Usage Telemetry"
      priority: medium
      when: "Review high-traffic docs/topics or tune on_demand ordering."
      paths:
        - /doc_agent/flows/maintenance-loop.md
---
# Scripts Agent Guide

> Lean catalog for automation entrypoints. Use this when orchestrating doc, lint, db, or workflow helpers.

## Scope
- Keep CLI automation discoverable and idempotent.
- Prefer `make <target>` wrappers so humans and AI share the same surface.
- Point heavier explanations to `/scripts/README.md` or the command reference.

## Context Shortcuts
| Need | Load | Purpose |
| --- | --- | --- |
| Directory map | `/scripts/README.md` | Lists every helper grouped by purpose |
| Make targets | `/doc_human/reference/commands.md` | Human sized command reference |
| Quality policy | `/doc_agent/policies/quality.md` | Expectations for automation output |

## Categories
- Documentation and routing (docgen, doc_tools, doc_route_check)
- Validation and lint (agent_lint, config_lint, python_scripts_lint, shell_scripts_lint)
- Contracts and DB (contract_compat_check, migrate_check, rollback_check)
- Workflow and triggers (workflow_suggest, agent_trigger, registry_check)
- Maintenance (ai_maintenance, health_check, cleanup scripts)
- Telemetry and optimization (context_usage_tracker, ai_chain_optimizer)

## Typical Flow
1. Identify the script or target via README or `make help`.
2. Run the script with `--help` before executing real work.
3. Wrap repeated usage inside a Make target if none exists yet.
4. Capture non standard options inside workdoc context for traceability.

## Commands
```bash
make docgen                   # Refresh headers and AI index
make agent_lint               # Validate every agent.md
make dev_check                # Full repo lint + tests
python scripts/<name>.py --help
```

## Safety
- Scripts must be idempotent and avoid destructive defaults.
- Never hard code absolute paths or secrets.
- When a script generates artifacts, clean them with `make cleanup_tmp`.

## References
- `/scripts/README.md`
- `/doc_human/reference/commands.md`
- `/doc_agent/policies/quality.md`

Version: follows repository main; no separate version tagging required.

