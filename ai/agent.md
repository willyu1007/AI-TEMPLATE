---
spec_version: "1.0"
agent_id: "ai_infrastructure"
role: "AI task management and knowledge infrastructure"

policies:
  goals_ref: /doc_agent/policies/goals.md
  safety_ref: /doc_agent/policies/safety.md

parent_agent: /agent.md
merge_strategy: "child_overrides_parent"

subdirectories:
  - path: /ai/workdocs
    role: Task context management for active development
    agent: /ai/workdocs/agent.md
  - path: /ai/workflow-patterns
    role: Standard workflow patterns library
    agent: /ai/workflow-patterns/agent.md
  - path: /ai/maintenance_reports
    role: Automated maintenance and health reports
    agent: /ai/maintenance_reports/agent.md
  - path: /ai/sessions
    role: Historical AI self-review records (archived)
    agent: N/A (lightweight, no agent needed)

context_routes:
  always_read:
    - /ai/LEDGER.md
  on_demand:
    - topic: "Task Context Recovery"
      priority: high
      paths:
        - /ai/workdocs/README.md
        - /ai/workdocs/active/<current-task>/context.md
    - topic: "Workflow Patterns"
      priority: high
      paths:
        - /ai/workflow-patterns/README.md
        - /ai/workflow-patterns/catalog.yaml
    - topic: "Repository Health"
      priority: medium
      paths:
        - /ai/maintenance_reports/health-summary.md
        - /ai/maintenance_reports/README.md
---
# AI Infrastructure Agent

> Coordinates task memory inside `ai/` so orchestration agents can resume work within minutes.

## Scope
- Track high level work in `LEDGER.md`.
- Keep active task context under `workdocs/`.
- Deliver reusable checklists inside `workflow-patterns/`.
- Store automated maintenance evidence under `maintenance_reports/`.
- Keep historical AI session reviews under `sessions/`.

## Component Map
| Component | When to load | Reference |
| --- | --- | --- |
| LEDGER | Always during S0 to recall recent tasks | `/ai/LEDGER.md` |
| Workdocs | Multi-session tasks that need fast resume | `/ai/workdocs/README.md` |
| Workflow patterns | When tasks map to known playbooks | `/ai/workflow-patterns/README.md`, `/ai/workflow-patterns/catalog.yaml` |
| Maintenance reports | Health investigations or guardrail checks | `/ai/maintenance_reports/README.md` |
| Sessions | Only when auditing past self-reviews | `/ai/sessions/<date>_<task>/` |

## Operating Notes
1. Register any task longer than one session in the ledger and create a workdoc via `make workdoc_create`.
2. Keep `context.md` current; that file is the primary resume surface.
3. Use `make workflow_suggest` before starting work to see if a pattern already covers the request.
4. Archive stale workdocs and clean maintenance reports with `make cleanup_reports_smart`.

## Commands
```bash
make workdoc_create TASK=<name>
make workflow_list
make workflow_suggest PROMPT="describe task"
make ai_maintenance
```

## Safety
- Never edit generated maintenance reports manually; rerun the script.
- Do not delete historical sessions unless retention policy demands it.
- Keep active workdocs under three files (plan, context, tasks) to stay token-friendly.

## References
- `/ai/LEDGER.md`
- `/ai/workdocs/README.md`
- `/ai/workflow-patterns/README.md`
- `/ai/maintenance_reports/README.md`

Version tracking lives in git history; no extra version field required here.

