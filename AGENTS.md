---
spec_version: "1.0"
agent_id: "repo"
role: "root level orchestrator, improve AI development efficiency"

policies:
  goals_ref: /doc_agent/policies/goals.md
  safety_ref: /doc_agent/policies/safety.md
  roles_ref: /doc_agent/policies/roles.md

merge_strategy: "child_overrides_parent"

context_routes:
  always_read:
    - /doc_agent/index/AI_INDEX.md
  on_demand:
    - topic: "S0 Orientation - Explain TemplateAI"
      priority: high
      audience: both
      when: "Need an elevator pitch, onboarding summary, or cross-team briefing."
      load_policy: default
      paths:
        - /README.md
    - topic: "S0 Orientation - Kick off a new project"
      priority: high
      audience: both
      when: "First-time setup or migration planning."
      load_policy: default
      paths:
        - /doc_agent/init/project-init.md
        - /doc_human/guides/PROJECT_INIT_GUIDE.md
    - topic: "Governance - Goals, safety, and roles"
      priority: high
      audience: ai
      when: "Clarify objectives, risk posture, or responsibilities."
      load_policy: default
      paths:
        - /doc_agent/policies/goals.md
        - /doc_agent/policies/safety.md
        - /doc_agent/policies/DOC_ROLES.md
    - topic: "Docs - writing standards and directory map"
      priority: medium
      audience: human
      when: "Need to assign docs or confirm style expectations."
      load_policy: human_only
      skip_for_ai: true
      paths:
        - /doc_human/guides/DOC_WRITING_STANDARDS.md
        - /doc_human/architecture/directory.md
    - topic: "Contract management"
      priority: medium
      audience: ai
      when: "Manage `.contracts_baseline/` snapshots or interface reviews."
      load_policy: task_specific
      paths:
        - /.contracts_baseline/README.md
    - topic: "Security & quality policies"
      priority: high
      audience: ai
      when: "Security reviews or enforcing repo-wide quality bars."
      load_policy: task_specific
      paths:
        - /doc_agent/policies/security.md
        - /doc_agent/policies/quality.md
    - topic: "Temporary file guardrails"
      priority: medium
      audience: human
      when: "Need retention rules for generated logs/reports."
      load_policy: human_only
      skip_for_ai: true
      paths:
        - /doc_human/policies/TEMP_FILES_POLICY.md
    - topic: "Common module usage"
      priority: medium
      audience: ai
      when: "Sharing or extending `modules/common` utilities."
      load_policy: default
      paths:
        - /modules/common/USAGE.md
        - /modules/common/AGENTS.md
    - topic: "Database - operate existing engines"
      priority: medium
      audience: both
      when: "Querying or troubleshooting DB assets."
      load_policy: default
      paths:
        - /doc_agent/specs/DB_SPEC.yaml
        - /doc_human/guides/SCHEMA_GUIDE.md
        - /db/engines/README.md
    - topic: "Database - plan schema or migration changes"
      priority: medium
      audience: both
      when: "Authoring migrations, reviewing table specs, or ensuring rollback plans."
      load_policy: default
      paths:
        - /doc_human/guides/DB_CHANGE_GUIDE.md
        - /db/engines/postgres/schemas/tables/runs.yaml
        - /db/engines/postgres/docs/DB_SPEC.yaml
    - topic: "Module development - classify or scaffold"
      priority: high
      audience: both
      when: "Selecting module type, scaffolding instances, or reviewing examples."
      load_policy: default
      paths:
        - /doc_agent/specs/MODULE_TYPES.md
        - /doc_agent/specs/MODULE_TYPE_CONTRACTS.yaml
        - /doc_agent/init/module-init.md
        - /doc_agent/quickstart/module-init.md
        - /doc_human/guides/MODULE_INSTANCES.md
        - /doc_human/examples/module-example/README.md
    - topic: "Configuration management"
      priority: medium
      audience: both
      when: "Modify config schema, defaults, or environment overrides."
      load_policy: default
      paths:
        - /config/AI_GUIDE.md
        - /doc_human/guides/CONFIG_GUIDE.md
    - topic: "Testing & fixtures"
      priority: medium
      audience: both
      when: "Define coverage gates, fixture etiquette, or mock strategy."
      load_policy: default
      paths:
        - /doc_agent/coding/TEST_STANDARDS.md
        - /doc_agent/coding/MOCK_RULES.md
        - /doc_human/guides/TEST_DATA_STRATEGY.md
    - topic: "Commit & PR workflow"
      priority: medium
      audience: human
      when: "Human contributors ask for approval or PR policy."
      load_policy: human_only
      skip_for_ai: true
      paths:
        - /doc_human/reference/pr_workflow.md
    - topic: "Trigger system & orchestration hooks"
      priority: medium
      audience: both
      when: "Configure or debug intelligent triggers."
      load_policy: task_specific
      paths:
        - /doc_agent/orchestration/agent-triggers.yaml
        - /doc_human/guides/triggers-guide.md
      commands:
        - "make trigger_show"
        - "make trigger_check"
        - "make trigger_coverage"
        - "make trigger_matrix"
    - topic: "Workdocs task management"
      priority: medium
      audience: ai
      when: "Create, update, or recover active workdocs."
      load_policy: default
      paths:
        - /doc_agent/quickstart/workdocs-quickstart.md
    - topic: "Guardrail quickstart"
      priority: medium
      audience: ai
      when: "Need guardrail bootstrapping or reminder of allowed operations."
      load_policy: default
      paths:
        - /doc_agent/quickstart/guardrail-quickstart.md
    - topic: "AI coding standards"
      priority: medium
      audience: ai
      when: "Ensure AI-written code stays inside repo conventions."
      load_policy: default
      paths:
        - /doc_agent/coding/AI_CODING_GUIDE.md
    - topic: "Human conventions (deep dive)"
      priority: low
      audience: human
      when: "Human reviewers request the comprehensive standards."
      load_policy: human_only
      skip_for_ai: true
      paths:
        - /doc_human/guides/CONVENTIONS.md
    - topic: "Workflow patterns"
      priority: medium
      audience: ai
      when: "Need a reusable checklist for a standard task."
      load_policy: default
      paths:
        - /ai/workflow-patterns/README.md
        - /ai/workflow-patterns/catalog.yaml
    - topic: "Lifecycle orchestration"
      priority: medium
      audience: ai
      when: "Clarify end-to-end stages or handoffs between agents."
      load_policy: default
      paths:
        - /doc_agent/flows/repo-lifecycle.md
    - topic: "Dataflow analysis"
      priority: medium
      audience: ai
      when: "Model UX/feature flows or run the quickstart."
      load_policy: default
      paths:
        - /doc_agent/quickstart/dataflow-quickstart.md
    - topic: "Repository health & maintenance"
      priority: high
      audience: ai
      when: "Produce health summaries or investigate quality drift."
      load_policy: task_specific
      paths:
        - /doc_agent/flows/maintenance-loop.md
        - /ai/maintenance_reports/README.md
        - /doc_agent/specs/HEALTH_CHECK_MODEL.yaml
      commands:
        - "make health_check"
        - "make health_check_strict"
        - "make health_report_detailed"
        - "make health_trend"
        - "make ai_friendliness_check"
        - "make module_health_check"
        - "make test_coverage"
        - "make code_complexity"
        - "make health_analyze_issues"
        - "make health_show_quick_wins"
        - "python scripts/context_usage_tracker.py report --limit 10"
        - "python scripts/ai_chain_optimizer.py --optimize --limit 10"
    - topic: "Automation - Scripts and commands"
      priority: medium
      audience: ai
      when: "Run repository automation via Makefile or one-shot helpers."
      load_policy: default
      paths:
        - /scripts/AGENTS.md
        - /scripts/README.md
    - topic: "Context routing optimization"
      priority: medium
      audience: ai
      when: "Optimizing context loading strategies and understanding routing principles."
      load_policy: task_specific
      paths:
        - /doc_agent/optimization/CONTEXT_ROUTING_PRINCIPLES.md
        - /doc_agent/optimization/CORRECT_OPTIMIZATION_APPROACH.md
    - topic: "Evaluation baselines"
      priority: low
      audience: ai
      when: "Refresh or compare baseline JSON before a release."
      load_policy: task_specific
      paths:
        - /evals/AGENTS.md
      commands:
        - "make contract_compat_check"
  by_scope:
    - scope: "Project Initialization"
      read:
        - /doc_agent/init/project-init.md
        - /doc_human/guides/PROJECT_INIT_GUIDE.md
    - scope: "Module Development"
      read:
        - /doc_agent/init/module-init.md
        - /doc_human/guides/MODULE_INIT_GUIDE.md
    - scope: "Maintenance & Health"
      read:
        - /doc_agent/flows/maintenance-loop.md
        - /ai/maintenance_reports/health-summary.md
    - scope: "Orchestration Management"
      read:
        - /doc_agent/orchestration/registry.yaml
        - /doc_agent/orchestration/routing.md
---
# Repository Orchestrator

> Root routing contract for TemplateAI. Keep context lean and deterministic so downstream agents stay inside budget.

This repository adopts `AGENTS.md` as the canonical orchestrator entry point. It is functionally equivalent to model-specific entry files such as `claude.md`、`gemini.md`、`agnets.md`、`CLAUDE.md`、`GEMINI.md`, so any guidance here applies uniformly across supported model families.

## Minimal Loading Plan
- `always_read` already loads `/doc_agent/index/AI_INDEX.md` (~130 tokens).
- Use `context_routes` (YAML above) to pull only the topics you need.
- Stop after the first hop; do not follow secondary links inside referenced docs.

## Critical Rules
1. **Audience check**: skip files marked `audience: human` unless the human explicitly requested them.
2. **Language**: follow `/config/language.yaml`; AI docs stay English only.
3. **Load policy**: follow the `load_policy` field:
   - `default` -> load when the described scenario matches your task.
   - `task_specific` -> load only if the user/task explicitly asks for that body of knowledge.
   - `human_only` -> skip unless a human author requests it in the prompt.
4. **Topic intent**: topic names already encode stage + action ("S0 Orientation - Explain TemplateAI"). Do not load the bundle unless that intent fits the active task.
5. **Depth**: one hop maximum from the route list; no recursive fetching.
6. **Provenance**: never auto-load "See also" links; treat them as manual options.

## Module Instance Definition (must know)
- Use `/doc_human/guides/MODULE_INSTANCES.md` as the single source of truth after running `make ai_begin MODULE=<name>`.
- Instances conform to one type contract (`/doc_agent/specs/MODULE_TYPES.md` + `MODULE_TYPE_CONTRACTS.yaml`) and inherit guardrails from both the template and their local `AGENTS.md`.
- Register ownership + escalation details in the guide and `/doc_agent/orchestration/registry.yaml` immediately after scaffolding.

## Workflow Hooks
| Stage | What to do | References |
| --- | --- | --- |
| S0 Refresh | Load LEDGER, workdoc, and relevant agents | `/ai/LEDGER.md`, `/ai/workdocs/README.md` |
| S1 Model | Build or update workdoc plan, check workflow patterns | `/ai/workflow-patterns/catalog.yaml` |
| S3 Build | Follow module/tests/config agents for the target area | See respective agent files |
| S6 Maintenance | Clean temp files, archive workdocs, sync docs | `make cleanup_temp`, `make workdoc_archive` |

## Quick Checklist
- Maintain plan and workdoc alignment.
- Run targeted tests before opening a PR.
- Update doc headers via `make docgen` when touching docs.
- Leave breadcrumbs (commit message, workdoc) for future context recovery.

## References
- `/README.md`
- `/doc_agent/policies/goals.md`
- `/doc_agent/policies/safety.md`
- `/doc_agent/policies/DOC_ROLES.md`
- `/doc_agent/specs/MODULE_TYPES.md`
- `/doc_human/guides/MODULE_INSTANCES.md`

Version metadata belongs to workdocs and the ledger; this orchestrator file stays versionless.

