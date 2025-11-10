---
audience: ai
language: en
version: playbook
purpose: Conversation and execution protocol for initializing module instances
---

# Module Initialization Protocol

> **Scope**: Creating or refreshing `modules/<entity>/` instances inside TemplateAI  
> **Goal**: Partner with the user to capture requirements, scaffold the module, and align documentation/tests.

---

## 1. Trigger & Preflight

1. Confirm the user wants to initialize a *module instance* (not the whole repo).  
2. Identify the target module type (see `/doc_agent/specs/MODULE_TYPES.md`).  
3. Ask whether requirement docs already exist.  
4. Clarify expectations: deliverables, coding language, integration points, deadlines.

Do not scaffold files until the user validates the collected information.

---

## 2. Requirement Document Handling

### If the user has documents

1. Request the file(s) and target location (`modules/<entity>/doc/`).  
2. Summarise the content and highlight missing sections (goals, features, dependencies, contracts).  
3. Obtain confirmation that the documents are authoritative.

### If no documents exist

1. Create `modules/<entity>/doc/REQUIREMENTS.md` (or enrich an existing placeholder).  
2. Guide the user through structured prompts:
   - Purpose and business value  
   - Target users / upstream modules / downstream consumers  
   - Functional requirements and workflow  
   - Data contracts (inputs, outputs, error handling)  
   - Non-functional constraints (performance, security, compliance)  
   - Open questions and risks
3. Iterate until the user confirms the requirement document is complete.

Always log the document status (`draft`, `ready`) and gain explicit approval before moving to scaffolding.

---

## 3. Interaction Loop

Use short question/summary cycles:

1. Ask focused questions about one area at a time (e.g., “List the main API endpoints”).  
2. Reflect the answer back, note remaining gaps, and confirm accuracy.  
3. Capture todos for unresolved topics.  
4. Repeat until every checklist item for requirements is addressed.

Signal clearly when the requirement document moves from draft → ready.

---

## 4. Scaffolding & Updates

Once requirements are approved:

1. **Generate structure**  
   - Use `make ai_begin MODULE=<entity>` when possible.  
   - Otherwise, create the directory layout manually (README, agent, doc/, tests/).
2. **Update key documents**  
   - `modules/<entity>/agent.md`: role, context routes, upstream/downstream dependencies.  
   - `modules/<entity>/README.md`: purpose, capabilities, integration notes.  
   - `modules/<entity>/doc/CONTRACT.md`: IO schema aligned with module type.  
   - `modules/<entity>/doc/RUNBOOK.md`, `TEST_PLAN.md`, `CHANGELOG.md`, `BUGS.md`, `PROGRESS.md`.  
   - `modules/<entity>/doc/REQUIREMENTS.md`: mark as “approved” with timestamp/owner.  
   - Update `requirements.txt` / dependency manifests if new packages are agreed.
3. **Registry & orchestration**  
   - Register the module in `/doc_agent/orchestration/registry.yaml`.  
   - Update `/doc_human/guides/MODULE_INSTANCES.md` with summary details.  
   - Adjust root `agent.md` context routes if the module should be auto-loaded.
4. **Interface documentation**  
   - Update any relevant API/interface specs (e.g., `/doc_agent/specs/` files, OpenAPI fragments).

Confirm each modification plan with the user before applying it.

---

## 5. Post-Requirement Options

After scaffolding, ask whether the user wants to implement functionality immediately:

- **If yes**:  
  1. Draft `modules/<entity>/plan.md` outlining backlog items and sequencing.  
  2. Review the plan with the user and obtain approval.  
  3. Execute coding tasks in agreed order, running targeted tests.

- **If no**:  
  - Document pending work in `modules/<entity>/doc/PROGRESS.md` or the workdoc system.  
  - Provide recommendations for next steps (testing, integration, reviews).

---

## 6. Completion Checklist

Before closing module initialization, verify with the user that:

- Requirement document is complete, approved, and stored under `modules/<entity>/doc/`.  
- All mandatory docs exist and are linked (README, agent, CONTRACT, RUNBOOK, TEST_PLAN, CHANGELOG, BUGS, PROGRESS).  
- Tests directory exists with at least placeholder suites.  
- Dependencies and interfaces are documented.  
- Root docs (README, agent, module registries) reference the new module correctly.  
- Follow-up actions (implementation, integration tests, deployment) are recorded.

Obtain explicit user confirmation that the module initialization phase is finished.

---

## 7. Handover Note

Summarise the module’s purpose, key capabilities, dependencies, and unresolved tasks.  
Recommend validation commands (`make module_health_check`, `make dev_check`) and next steps for development or review.


