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
    - topic: "Project Overview"
      priority: high
      paths:
        - /README.md
    - topic: "Full Objectives and Principles"
      priority: high
      paths:
        - /doc_agent/policies/goals.md
        - /doc_agent/policies/safety.md
    - topic: "Documentation Roles and Responsibilities"
      priority: high
      paths:
        - /doc_agent/policies/DOC_ROLES.md
    - topic: "Documentation Writing Standards"
      priority: medium
      paths:
        - /doc_human/guides/DOC_WRITING_STANDARDS.md
    - topic: "Contract Management"
      priority: medium
      paths:
        - /.contracts_baseline/README.md
    - topic: "Directory Structure"
      priority: medium
      paths:
        - /doc_human/architecture/directory.md
    - topic: "Security and Quality Standards"
      priority: medium
      paths:
        - /doc_agent/policies/security.md
        - /doc_agent/policies/quality.md
    - topic: "Temporary Files Management"
      priority: high
      paths:
        - /doc_human/policies/TEMP_FILES_POLICY.md
    - topic: "Common Module Usage"
      priority: high
      paths:
        - /modules/common/USAGE.md
        - /modules/common/agent.md
    - topic: "Database Operations"
      priority: high
      paths:
        - /doc_agent/specs/DB_SPEC.yaml
        - /doc_human/guides/SCHEMA_GUIDE.md
        - /db/engines/README.md
    - topic: "Database Changes"
      priority: high
      paths:
        - /doc_human/guides/DB_CHANGE_GUIDE.md
        - /db/engines/postgres/schemas/tables/runs.yaml
        - /db/engines/postgres/docs/DB_SPEC.yaml
    - topic: "Module Development"
      priority: high
      paths:    
        - /doc_agent/specs/MODULE_TYPES.md
        - /doc_agent/specs/MODULE_TYPE_CONTRACTS.yaml
        - /doc_human/guides/MODULE_INSTANCES.md
        - /doc_agent/quickstart/module-init.md
        - /doc_human/examples/module-example/README.md
    - topic: "Configuration Management"
      priority: high
      paths:
        - /config/AI_GUIDE.md
        - /doc_human/guides/CONFIG_GUIDE.md
    - topic: "Testing Standards"
      priority: medium
      paths:
        - /doc_agent/coding/TEST_STANDARDS.md
    - topic: "Commit and PR Workflow"
      priority: low
      audience: human
      paths:
        - /doc_human/reference/pr_workflow.md
    - topic: "Intelligent Trigger System"
      priority: medium
      paths:
        - /doc_agent/orchestration/agent-triggers.yaml
        - /doc_human/guides/triggers-guide.md
    - topic: "Workdocs Task Management"
      priority: high
      paths:
        - /doc_agent/quickstart/workdocs-quickstart.md
    - topic: "Guardrail Protection Mechanism"
      priority: high
      paths:
        - /doc_agent/quickstart/guardrail-quickstart.md
    - topic: "Mock Data Generation"
      priority: medium
      paths:
        - /doc_agent/coding/MOCK_RULES.md
        - /doc_human/guides/TEST_DATA_STRATEGY.md
    - topic: "AI Coding Standards"
      priority: high
      paths:
        - /doc_agent/coding/AI_CODING_GUIDE.md
    - topic: "Comprehensive Development Standards"
      priority: low
      audience: human
      skip_for_ai: true
      paths:
        - /doc_human/guides/CONVENTIONS.md
    - topic: "Workflow Patterns"
      priority: high
      paths:
        - /ai/workflow-patterns/README.md
        - /ai/workflow-patterns/catalog.yaml
    - topic: "Dataflow Analysis"
      priority: high
      paths:
        - /doc_agent/quickstart/dataflow-quickstart.md
    - topic: "Repository Health Check"
      priority: medium
      paths:
        - /ai/maintenance_reports/health-summary.md
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
  by_scope:
    - scope: "Module Development"
      read:
        - /doc_human/guides/MODULE_INIT_GUIDE.md
        - /doc_human/templates/module-templates/
    - scope: "Orchestration Management"
      read:
        - /doc_agent/orchestration/registry.yaml
        - /doc_agent/orchestration/routing.md
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

Load context by priority tiers (Tier-0 required, others as needed).

> If `snapshot_hash` changed, run `make docgen` first.
> **Details**: `/doc_human/guides/agent-workflow-details.md#s0---refresh-context-details`

### S1 - Task Modeling

Update `/modules/<name>/plan.md` with scope, impacts, risks, and rollback plan.

**New Module**: Run `make ai_begin MODULE=<name>`

> **Details**: `/doc_human/guides/agent-workflow-details.md#s1---task-modeling-details`

### S2 - Plan Review (AI-SR: Plan)

Generate `/ai/sessions/<date>_<name>/AI-SR-plan.md` with impact analysis and test plan.

> **Details**: `/doc_human/guides/agent-workflow-details.md#s2---plan-review-details`

### S3 - Implementation & Verification

Implement with tests (coverage ≥80%), run `make dev_check`.

> **Details**: `/doc_human/guides/agent-workflow-details.md#s3---implementation--verification-details`

### S4 - Documentation Update

Update CONTRACT, TEST_PLAN, CHANGELOG, and other docs. Run `make docgen`.

> **Details**: `/doc_human/guides/agent-workflow-details.md#s4---documentation-update-details`

### S5 - Self-Review & PR

Generate AI-SR-impl.md, submit PR. Must pass CI gates.

> **Details**: `/doc_human/guides/agent-workflow-details.md#s5---self-review--pr-details`

### S6 - Auto Maintenance

Run `make ai_maintenance` and cleanup commands.

**Report Generation Rules**:
- ✅ Health reports → `/ai/maintenance_reports/health-*.md`
- ✅ Optimization reports → `/ai/maintenance_reports/optimization-*.md`
- ✅ Session reviews → `/ai/sessions/<date>_<task>/`
- ❌ NEVER generate reports in root directory
- ❌ NEVER use `/tmp/` for permanent reports

> **Details**: `/doc_human/guides/agent-workflow-details.md#s6---auto-maintenance-details`

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

### 1.3 On-Demand Loading

Context routes in YAML front matter:
- **always_read**: AI_INDEX.md only (~130 tokens)
- **on_demand**: Load by task type and priority
- **by_scope**: Module-specific docs

**Memory**: LEDGER.md (tasks), sessions/ (AI-SR), .aicontext/ (index)

> **Details**: `doc_agent/orchestration/routing.md`

---

## 2. Quick Quality Checklist

**Pre-Change**: plan.md updated, impacts assessed  
**During**: tests added, backward compatible  
**Pre-Commit**: docs synced, dev_check passed, temp files cleaned

---

## 3. Quick Reference

**Key Documents**:
- AI Policies: `/doc_agent/policies/` (goals.md, safety.md, roles.md)
- AI Specs: `/doc_agent/specs/` (DB_SPEC.yaml, MODULE_TYPES.md)
- AI Guides: `/doc_agent/quickstart/` (module-init.md, workdocs.md)
- Human Guides: `/doc_human/guides/` (detailed guides for human reference)

**Commands**: See `/doc_human/guides/agent-workflow-details.md#command-reference`

---

**Version**: 2.1  
**Last Updated**: 2025-11-09 (Phase 14.0.3)  
**Maintained by**: Project Team

---

> **📖 For AI Orchestration Systems**:  
> This document defines workflow and document routing rules. For detailed specs, guides, and command references, load via `context_routes` on-demand.  
> For module-level config, see each module's `modules/<entity>/agent.md`.
