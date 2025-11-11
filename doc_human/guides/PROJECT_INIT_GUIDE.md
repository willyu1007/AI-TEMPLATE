---
audience: human
language: en
version: reference
purpose: Human checklist for coordinating repository initialization with AI agents
---

# Project Initialization Guide

This guide helps project owners collaborate with TemplateAI agents to bring a repository online.  
Use it whenever you request initialization support from the AI orchestrator.

---

## 1. Preparation

1. **Language & scope**  
   - Confirm the repository language in `config/language.yaml`.  
   - Decide which environments (dev/staging/prod) need configuration on day one.
2. **Baseline assets**  
   - Gather existing requirement or design documents.  
   - List expected modules/services and known dependencies.  
   - Identify compliance, security, or data constraints that must be reflected.
3. **Expectations**  
   - Decide whether initialization should scaffold actual code, just documentation, or a hybrid.  
   - Clarify which parts you prefer to edit manually.

Share the above context with the AI before asking it to modify files.

---

## 2. Choose an Initialization Mode

| Mode | When to use | What humans must provide | Output you should expect |
| --- | --- | --- | --- |
| **Document-driven** | You already have requirement docs | Upload / summarise docs; call out missing sections | Repo scaffold aligned with the supplied documentation |
| **Document creation first** | No existing docs | Participate in AI-led interviews to co-author the docs | Approved requirements that the AI can turn into repo structure |
| **Manual initialization** | You want to apply changes yourself | Confirm desired edits/deletions; request checklists/snippets | Action plan, templates, and verification steps (no auto edits) |
| **Import existing project** | Migrating another repo | Provide local path, architecture summary, desired migration style | Transferred structure plus documentation for divergence |

State the chosen mode explicitly to keep the agent on the correct path.

---

## 3. Collaboration Flow

1. **Discovery loop**  
   - Answer targeted questions about goals, architecture, modules, dependencies, and risks.  
   - Review AI summaries and confirm or correct them.  
   - Continue until the AI presents a consolidated plan that you approve.
2. **Approval gate**  
   - Review the file list and sample content before any edits run.  
   - Confirm automation commands (`make ai_begin`, `make docgen`, etc.) when proposed.
3. **Execution oversight**  
   - Monitor generated docs (`README.md`, `AGENTS.md`, module docs).  
   - Ensure sensitive information or secrets are not committed.
4. **Closure**  
   - Validate the completion checklist (below).  
   - Request follow-up tasks (feature implementation, testing) if needed.

---

## 4. Completion Checklist

- [ ] `README.md` rewritten with project vision, setup, and workflows.  
- [ ] Root `AGENTS.md` updated: accurate `context_routes`, module references, and role description.  
- [ ] Any agreed modules exist with docs (`AGENTS.md`, `README.md`, `doc/`, `tests/`).  
- [ ] Supporting docs updated (`doc_agent/`, `doc_human/`, `config/`).  
- [ ] Migration notes recorded if code was imported.  
- [ ] `TEMPLATE_USAGE.md` and the temporary initialization folder are removed or archived.  
- [ ] Outstanding items captured in workdocs or issue tracker.  
- [ ] Final confirmation sent to the AI agent (so it can stop editing).

---

## 5. References

- `doc_agent/init/project-init.md` – AI protocol for repo initialization  
- `doc_agent/init/module-init.md` – AI protocol for module initialization  
- `doc_human/guides/MODULE_INIT_GUIDE.md` – Module guide for humans  
- `doc_human/guides/MODULE_INSTANCES.md` – Registry of module instances  
- `doc_human/reference/pr_workflow.md` – Pull request process


