---
audience: ai
language: en
version: flow
purpose: End-to-end orchestration lifecycle for TemplateAI repositories
---

# Repository Orchestration Lifecycle

> **Objective**: Provide a single-hop view for AI agents covering the full delivery loop—from intake to maintenance—so that every action stays aligned with TemplateAI guardrails.

---

## 1. Stage Overview

| Stage | Goal | Key Outputs | Primary References |
| --- | --- | --- | --- |
| **S0 Intake** | Capture the request, confirm scope, choose workflow pattern | Workdoc stub, selected pattern, initialization mode | `/ai/workflow-patterns/catalog.yaml`, `/doc_agent/init/project-init.md` |
| **S1 Model** | Structure requirements and plans | Approved requirements, `plan.md`, updated workdoc sections | `/doc_human/guides/PROJECT_INIT_GUIDE.md`, `/doc_human/guides/MODULE_INIT_GUIDE.md` |
| **S2 Align** | Validate guardrails, dependencies, and risks | Registry updates, dependency matrix, risk log | `/doc_agent/orchestration/registry.yaml`, `/doc_agent/policies/safety.md` |
| **S3 Build** | Implement code/docs/tests | Feature branches, updated modules, passing checks | `/doc_agent/coding/AI_CODING_GUIDE.md`, `/doc_agent/coding/TEST_STANDARDS.md` |
| **S4 Verify** | Run validations + peer review | `make dev_check` results, review notes, test artifacts | `/doc_agent/quickstart/guardrail-quickstart.md`, `/tests/agent.md` |
| **S5 Release** | Finalize docs, handover, tagging | Updated `README.md`, release notes, deployment checklist | `/doc_human/project/RELEASE_TRAIN.md`, `/doc_human/reference/pr_workflow.md` |
| **S6 Maintain** | Continuous health monitoring + backlog grooming | Health reports, issue tracker sync, archived workdocs | `/doc_agent/flows/maintenance-loop.md`, `/ai/maintenance_reports/health-summary.md` |

---

## 2. Flow Narrative

1. **Capture & Pattern Match**  
   - Load `AI_INDEX.md` and context routes to verify safety limitations.  
   - Choose an orchestration pattern (`ai/workflow-patterns/`) or default to the initialization playbooks.

2. **Information Expansion**  
   - Use conversational loops to gather requirements, summarise after each exchange, and confirm readiness before editing.  
   - Store drafts in workdocs and mark decisions explicitly.

3. **Guardrail Alignment**  
   - Check module registry impacts, database touchpoints, and security policies.  
   - Update routing tables or registry entries only after obtaining approval and logging the change.

4. **Execution & Validation**  
   - Make incremental edits; after each milestone, run targeted validations (`make agent_lint`, `make module_health_check`, etc.).  
   - Keep diffs scoped to the task; defer unrelated refactors.

5. **Release & Documentation**  
   - Prepare release artifacts (PR description, change summaries, updated docs).  
   - Confirm language consistency and ensure guardrail checks are green.

6. **Maintenance Feedback Loop**  
   - Schedule health scans and analyse outcomes (see `maintenance-loop.md`).  
   - Record follow-up actions in workdocs or backlog tooling, keeping AI-friendly breadcrumbs.

---

## 3. Role of Agents

- **Root orchestrator (`agent.md`)**: maintains routing, scope, and priority rules.  
- **Module agents (`modules/<name>/agent.md`)**: enforce local guardrails and context for module tasks.  
- **Service agents (e.g., `/schemas/agent.md`, `/db/engines/agent.md`)**: provide domain-specific protocols for schema or database work.

When adding a new agent, ensure it declares clear `context_routes`, `tools_allowed`, and ownership boundaries consistent with this lifecycle.

---

## 4. Handover Checklist

Before transitioning between stages or agents, verify:

- Workdoc updated with decisions and next steps.  
- Registry and routing files reflect new modules/services.  
- Tests and validations recorded with timestamps and commands.  
- Pending risks or TODOs explicitly assigned or documented.

Following this lifecycle keeps all agents aligned, prevents context drift, and preserves auditability across the TemplateAI ecosystem.


