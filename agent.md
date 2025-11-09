---
spec_version: "1.0"
agent_id: "repo"
role: "root level orchestrator, improve AI development efficiency"

policies:
  goals_ref: /doc/policies/goals.md
  safety_ref: /doc/policies/safety.md
  roles_ref: /doc/policies/roles.md

merge_strategy: "child_overrides_parent"

context_routes:
  always_read:
    - /doc/policies/AI_INDEX.md
  on_demand:
    - topic: "Project Overview"
      priority: high
      paths:
        - /README.md
    - topic: "Full Objectives and Principles"
      priority: high
      paths:
        - /doc/policies/goals-en.md
        - /doc/policies/safety-en.md
    - topic: "Documentation Roles and Responsibilities"
      priority: high
      paths:
        - /doc/policies/DOC_ROLES-en.md
    - topic: "Documentation Writing Standards"
      priority: medium
      paths:
        - /doc/process/DOC_WRITING_STANDARDS.md
    - topic: "Contract Management"
      priority: medium
      paths:
        - /.contracts_baseline/README.md
    - topic: "Directory Structure"
      priority: medium
      paths:
        - /doc/architecture/directory.md
    - topic: "Security and Quality Standards"
      priority: medium
      paths:
        - /doc/policies/security.md
        - /doc/policies/quality.md
    - topic: "Common Module Usage"
      priority: high
      paths:
        - /modules/common/USAGE.md
        - /modules/common/agent.md
    - topic: "Database Operations"
      priority: high
      paths:
        - /doc/db/DB_SPEC.yaml
        - /doc/db/SCHEMA_GUIDE.md
        - /db/engines/README.md
    - topic: "Database Changes"
      priority: high
      paths:
        - /doc/process/DB_CHANGE_GUIDE.md
        - /db/engines/postgres/schemas/tables/runs.yaml
        - /db/engines/postgres/docs/DB_SPEC.yaml
    - topic: "Module Development"
      priority: high
      paths:    
        - /doc/modules/MODULE_TYPES.md
        - /doc/modules/MODULE_TYPE_CONTRACTS.yaml
        - /doc/modules/MODULE_INSTANCES.md
        - /doc/modules/MODULE_INIT_GUIDE.md
        - /doc/modules/example/README.md
    - topic: "Configuration Management"
      priority: high
      paths:
        - /config/AI_GUIDE.md
        - /doc/process/CONFIG_GUIDE.md
    - topic: "Testing Standards"
      priority: medium
      paths:
        - /doc/process/testing.md
    - topic: "Commit and PR Workflow"
      priority: low
      audience: human
      paths:
        - /doc/process/pr_workflow.md
    - topic: "Intelligent Trigger System"
      priority: medium
      paths:
        - /doc/orchestration/agent-triggers.yaml
        - /doc/orchestration/triggers-guide.md
    - topic: "Workdocs Task Management"
      priority: high
      paths:
        - /doc/process/workdocs-quickstart.md
    - topic: "Guardrail Protection Mechanism"
      priority: high
      paths:
        - /doc/process/guardrail-quickstart.md
    - topic: "Mock Data Generation"
      priority: medium
      paths:
        - /doc/process/MOCK_RULES.md
        - /doc/process/TEST_DATA_STRATEGY.md
    - topic: "AI Coding Standards"
      priority: high
      paths:
        - /doc/process/AI_CODING_GUIDE.md
    - topic: "Comprehensive Development Standards"
      priority: low
      audience: human
      skip_for_ai: true
      paths:
        - /doc/process/CONVENTIONS.md
    - topic: "Workflow Patterns"
      priority: high
      paths:
        - /ai/workflow-patterns/README.md
        - /ai/workflow-patterns/catalog.yaml
    - topic: "Dataflow Analysis"
      priority: high
      paths:
        - /doc/process/dataflow-quickstart.md
    - topic: "Repository Health Check"
      priority: medium
      paths:
        - /ai/maintenance_reports/health-summary.md
        - /doc/process/HEALTH_CHECK_MODEL.yaml
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
  by_scope:
    - scope: "Module Development"
      read:
        - /doc/modules/MODULE_INIT_GUIDE.md
        - /doc/modules/TEMPLATES/
    - scope: "Orchestration Management"
      read:
        - /doc/orchestration/registry.yaml
        - /doc/orchestration/routing.md
---

# agent.md

> **Purpose**: Enable AI agents to work efficiently with reduced cognitive load, ensuring complete understanding of project state in every session.

---

## Important Reminders

Before starting any task, AI agents must:

1. **Follow Workflow**: See Section 0, execute steps S0-S6 in sequence
2. **Understand Role Boundaries**: Refer to `doc/policies/roles.md`
3. **Follow Document Routing**: Load relevant docs based on task type (Section 1)
4. **Check Documentation Standards**: Load DOC_WRITING_STANDARDS.md when creating/editing docs

---

## 0. Workflow (6-Step Process)

**Applies to**: All tasks. AI agents follow these steps for every task execution:

### S0 - Refresh Context (Layered Loading)

Load by priority tiers:

- **Tier-0 (Required)**: `/.aicontext/snapshot.json`, `/.aicontext/module_index.json`
- **Tier-1 (Strongly Recommended)**: `/doc/flows/dag.yaml`, relevant `tools/*/contract.json`, target module `plan.md`/`README.md`
- **Tier-2 (Recommended)**: `/doc/db/DB_SPEC.yaml`, `/doc/process/ENV_SPEC.yaml`, `/config/*.yaml`
- **Tier-3 (As Needed)**: `TEST_PLAN.md`, `RUNBOOK.md`, `PROGRESS.md`, `BUGS.md`

> If `snapshot_hash` changed, run `make docgen` first to generate latest index.

### S1 - Task Modeling

Update `/modules/<name>/plan.md`, specify:
- Scope and slicing
- Interface impact
- Data changes
- Risk assessment
- Verification commands
- Rollback plan

> **Boundary**: `plan.md` = future plans, `PROGRESS.md` = historical records (don't mix)

**New Module**: Run `make ai_begin MODULE=<name>` or refer to `doc/modules/MODULE_INIT_GUIDE.md`

### S2 - Plan Review (AI-SR: Plan)

Generate `/ai/sessions/<date>_<name>/AI-SR-plan.md`:
- Intent description
- Impact analysis
- DAG/Contract/DB change points
- Test plan
- Rollback plan

### S3 - Implementation & Verification

- Modify only planned scope
- Maintain backward compatibility
- Update or add tests (coverage ≥80%)
- Run `make dev_check` (CI gate)

**Test Requirements**: See `doc/process/testing.md`

### S4 - Documentation Update

Synchronize updates:
- `CONTRACT.md` / `contract.json`
- `TEST_PLAN.md`
- `RUNBOOK.md`
- `PROGRESS.md`
- `CHANGELOG.md`
- `doc/flows/dag.yaml` (if applicable)

Run `make docgen` to refresh index.

### S5 - Self-Review & PR

Generate `/ai/sessions/<date>_<name>/AI-SR-impl.md`, submit PR with plan and AI-SR.

**PR Process**: See `doc/process/pr_workflow.md`

**CI Gates**: 
- `make dev_check` (must pass)
- Test coverage ≥80%
- High-risk changes need `make rollback_check`

### S6 - Auto Maintenance

Run `make ai_maintenance` to ensure repo health.

---

## 1. Document Routing & Context Management

### 1.1 Document Selection Guide

**AI Documents vs Human Documents**:

| Type | Identifier | Format | When to Use |
|------|-----------|--------|-------------|
| **AI Docs** | "For AI Agents" in header | English, ~100 lines, commands | Quick operations, reference |
| **Human Docs** | Full guides (*_GUIDE.md) | CN/EN, 300+ lines, detailed | Deep learning, troubleshooting |

**Loading Priority**:
1. **For Operations**: Load AI quickstart (*-quickstart.md, AI_*.md)
2. **For Learning**: Load human complete guide (*_GUIDE.md, CONVENTIONS.md)
3. **Check Priority**: Refer to `priority` field in context_routes (high/medium/low)

**Examples**:
- Need guardrail info? → Load `guardrail-quickstart.md` (120 lines) first
- Need deep understanding? → Load `GUARDRAIL_GUIDE.md` (782 lines) second
- Need coding rules? → Load `AI_CODING_GUIDE.md` (150 lines), not `CONVENTIONS.md` (611 lines)

### 1.2 Context Loading Rules ⚠️ Critical

**Rule 1: DO NOT auto-load referenced documents**
- `always_read` loads ONLY AI_INDEX.md (self-contained)
- DO NOT follow "See also" or "Details: xxx.md" references
- Those are on-demand documents, load explicitly only when needed

**Rule 2: Maximum depth = 1 level**
- Load explicitly listed documents only
- Do not recursively follow references
- Example: AI_INDEX.md mentions goals.md → Do NOT auto-load goals.md

**Rule 3: Respect audience field** ⭐ NEW
- Check YAML front matter `audience` field in documents
- **Skip if `audience: human`** (unless explicitly requested by user)
- **Skip if `skip_for_ai: true`** field is present
- **Load if `audience: ai`** or `audience: both`
- If no audience field, assume `both` (load conditionally)

**Rule 4: Language preference** ⭐ NEW
- **AI docs MUST be English** (`language: en`)
- **Prefer English docs** when available (e.g., goals-en.md over goals.md)
- **Chinese docs acceptable** only for:
  - README.md (project overview)
  - Human-only docs (`audience: human`)
  - When no English version exists (temporary)
- **When updating docs**: Keep AI docs in English, human docs can be Chinese

**Rule 5: Priority-based loading** ⭐ NEW
- **priority: high** → Load when task is highly relevant
- **priority: medium** → Load only when explicitly mentioned in prompt
- **priority: low** → Load only if user explicitly requests
- **No priority field** → Treat as medium

**Loading Decision Tree**:
```
1. Check `audience` field
   ├─ human? → Skip (unless user requests)
   ├─ ai? → Continue to step 2
   └─ both? → Continue to step 2

2. Check `language` field
   ├─ en? → Continue to step 3
   ├─ zh? → Skip if English version exists
   └─ no field? → Continue to step 3

3. Check `priority` field
   ├─ high? → Load if task relevant
   ├─ medium? → Load if mentioned
   ├─ low? → Skip (unless requested)
   └─ Load conditionally
```

**Rule 3: On-demand loading**
- Check `context_routes` for task-specific topics
- Load based on `priority` field (high → medium → low)
- Stop after loading listed files, no further recursion

### 1.3 On-Demand Loading (Context Routes)

Root agent.md's YAML Front Matter defines document routing rules:

- **always_read**: AI_INDEX.md only (self-contained, ~130 tokens)
- **on_demand**: 19 topics with priority (load based on task type)
  - High: Project overview, goals, database, modules, workflows, config, guardrails
  - Medium: Testing, triggers, common module, coding standards, dataflow
  - Low: Directory, routing usage, conventions, project init
- **by_scope**: Module-specific (load when working in that module)

**How It Works**: 
1. AI loads `always_read` on startup (AI_INDEX.md → self-contained quick reference)
2. Based on task type (e.g., "database ops"), AI loads corresponding `on_demand` docs
3. When entering specific module, load `by_scope` configured module docs
4. **STOP** - Do not recursively follow references in loaded docs

**Details**: `doc/orchestration/routing.md`

### Memory Mechanism

1. **AI Ledger**: `/ai/LEDGER.md` records all tasks
2. **Sessions**: `/ai/sessions/<date>_<mod>/` preserves AI-SR files
3. **Index**: `/.aicontext/` auto-generated index

---

## 2. Quality Checklist

### Pre-Change Checks

- Updated `plan.md`?
- Clarified impact scope?
- Assessed rollback plan?
- Prepared test cases?

### During Implementation

- Code changes minimized?
- Backward compatibility maintained?
- Tests cover changes?
- Appropriate logging added?

### Pre-Commit Checks

- All docs updated?
- `make dev_check` passed?
- AI-SR generated?
- Temp files cleaned?

---

## 3. Core Reference Documents

### Orchestration & Policies
- **Global Goals**: `doc/policies/goals.md`
- **Safety Rules**: `doc/policies/safety.md`
- **Roles & Gates**: `doc/policies/roles.md`
- **Document Routing**: `doc/orchestration/routing.md`
- **Module Registry**: `doc/orchestration/registry.yaml`

### Initialization Guides
- **Project Init**: `doc/init/PROJECT_INIT_GUIDE.md`
- **Module Init**: `doc/modules/MODULE_INIT_GUIDE.md`
- **Module Types**: `doc/modules/MODULE_TYPES.md`
- **Doc Templates**: `doc/modules/TEMPLATES/`

### Architecture & Reference
- **Directory Structure**: `doc/architecture/directory.md`
- **Command Quick Reference**: `doc/reference/commands.md`
- **Database Specs**: `db/engines/README.md`
- **Schema Definitions**: `schemas/`

### Process Documents
- **Testing Standards**: `doc/process/testing.md`
- **PR Workflow**: `doc/process/pr_workflow.md`
- **Coding Conventions**: `doc/process/CONVENTIONS.md`
- **Config Guide**: `doc/process/CONFIG_GUIDE.md`
- **Environment Spec**: `doc/process/ENV_SPEC.yaml`

---

**Version**: 2.1  
**Last Updated**: 2025-11-09 (Phase 14.0.3)  
**Maintained by**: Project Team

---

> **📖 For AI Orchestration Systems**:  
> This document defines workflow and document routing rules. For detailed specs, guides, and command references, load via `context_routes` on-demand.  
> For module-level config, see each module's `modules/<entity>/agent.md`.
