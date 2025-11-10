---
audience: ai
language: en
version: playbook
purpose: Conversation and execution protocol for repository initialization
---

# Project Initialization Protocol

> **Scope**: Root-level repo setup inside TemplateAI  
> **Goal**: Collect requirements through dialogue, align with orchestration rules, and scaffold the project accordingly.

---

## 1. Preflight

1. **Confirm intent**: Ask the user to confirm that they want to initialize a repo using this template.  
2. **Check constraints**: Clarify language expectations (`config/language.yaml`), tooling limitations, and whether existing files must be preserved.  
3. **Inventory docs**: Ask if the user already has requirement or design documents to upload/share.  
4. **Align expectations**: Summarise what initialization will deliver (directory scaffolding, baseline docs, module registry impact) and obtain explicit approval before continuing.

---

## 2. Select an Initialization Mode

| Mode | When to choose | Key questions | Exit criteria |
| --- | --- | --- | --- |
| **Document-driven** | User already has development docs | Request uploaded files, validate scope, capture missing metadata | User confirms documents are complete enough to proceed |
| **Document creation first** | No existing docs | Guide the user to co-author development docs (vision, scope, features, constraints) | Shared doc reaches “ready” state and user approves |
| **Manual initialization** | User wants handcrafted setup | Clarify which files will be edited/deleted and desired structure | User approves the manual plan |
| **Import existing project** | User wants to migrate another repo | Collect path, architecture summary, functional overview, and migration preference (copy / auto-implement / skeleton) | Migration strategy confirmed |

Always recap the chosen mode and record it in the worklog/context before moving on.

---

## 3. Information Gathering Loop

Perform iterative questioning tailored to the chosen mode:

- **Context**: goals, stakeholders, success metrics, delivery timeline.  
- **Architecture**: modules/services, external systems, data stores, compliance rules.  
- **Module plan**: required initial module instances, their roles, dependencies.  
- **Docs & guardrails**: which docs must exist on day one (README, agent.md, contracts, policies).  
- **Risks & open items**: unknown requirements, approvals, or third-party blockers.

Summarise the collected information after each round and invite corrections. Continue until the user explicitly confirms completeness.

---

## 4. Execution Blueprint

1. **Generate/change docs only after confirmation**. Provide the intended file list and preview key sections.  
2. **Scaffold structure**:
   - Base folders (e.g. `modules/`, `doc_agent/`, `doc_human/`, `config/`, `ai/`).
   - Optional sample module skeletons if they were approved.
3. **Doc updates**:
   - Rewrite root `README.md` with project summary, getting started, workflows.
   - Update root `agent.md` context routes and metadata to reflect actual modules and docs.
   - Produce any initial specs or policies requested (e.g., `doc_human/project/` documents).
4. **Config alignment**: Draft entries for `config/` files, `.env` templates, and Make targets if required.
5. **Registry alignment**: Update `/doc_agent/orchestration/registry.yaml` and relevant indexes if modules were created.

If automation scripts (`make ai_begin`, `make docgen`, etc.) are needed, mention them and request approval before invocation.

---

## 5. Mode-specific Notes

### Document-driven
- Ingest the supplied docs and map them to template sections (project summary, architecture, module specs).
- Highlight any mismatches or missing details.
- Confirm the final doc set that will live in the repo (`doc_human/`, `doc_agent/`, `/README.md`).

### Document creation first
- Facilitate doc drafting using templates (`doc_human/templates/`, `doc_agent/index/AI_INDEX.md` cues).
- Keep sections short and verifiable: objectives, scope, architecture, module list, risks.
- Only move to execution after the user marks the doc “ready”.

### Manual initialization
- Provide a checklist covering files to edit, sections to fill, and files safe to delete.
- Offer examples/snippets instead of direct edits when the user prefers to handle modifications manually.
- Summarise agreed actions for the user to execute.

### Import existing project
- Request: absolute/local path, high-level architecture, core features, confirmed requirements, repo structure.
- Ask which migration method to use:
  1. **Direct copy** – copy files as-is and adapt paths.
  2. **Auto-implement** – re-create functionality following the template style.
  3. **Skeleton only** – copy directories/interfaces without business logic.
- Flag any incompatible components (e.g., unsupported tech stack) before migrating.

---

## 6. Post-Initialization Checklist

Before closing the task, confirm with the user that:

- Root `README.md` reflects the configured project.  
- Root `agent.md` routes only to actual docs and modules.  
- Module instances, if any, include `agent.md`, `README.md`, `doc/` contracts, and `tests/`.  
- Supporting docs (`doc_human/project/`, `doc_agent/`, `config/`) are updated.  
- Temporary scaffolding (`doc_human/init/`, `TEMPLATE_USAGE.md`, placeholder templates) is removed or archived.  
- Follow-up tasks (e.g., implement features, write tests) are captured in workdocs or TODOs.

Always obtain explicit user confirmation that initialization is complete and documented.

---

## 7. Handover

Provide:

- Summary of what was initialized and why.  
- Outstanding open questions or risks.  
- Recommended next steps (testing, module development, deployment prep).  
- Commands the user should run (e.g., `make dev_check`, `make docgen`).

Record the outcome in the worklog and update any orchestration metadata if required.


