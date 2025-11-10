---
audience: human
language: en
version: reference
purpose: Migrating existing projects into the TemplateAI repo structure
---

# Project Migration Guide

Use this guide when you need to import an existing codebase into TemplateAI.  
It complements the AI playbook at `doc_agent/init/project-init.md`.

---

## 1. Preparation

1. **Source inventory**  
   - Identify the repository or local path to migrate.  
   - List core services/modules, data stores, and external integrations.  
   - Gather up-to-date documentation (architecture diagrams, API specs, runbooks).
2. **Target expectations**  
   - Decide whether to copy code verbatim, reimplement features, or bring across only a skeleton.  
   - Determine which modules map to TemplateAI module types and which require new implementations.  
   - Record known gaps or technical debt that should be addressed during migration.
3. **Logistics**  
   - Ensure you have permission to copy the source code.  
   - Note toolchains, dependencies, and environment differences that may affect setup.

---

## 2. Engage the AI Agent

When you request migration support:

1. Provide the source path and access instructions.  
2. Share architecture and functionality summaries so the AI can align modules.  
3. Clarify the chosen migration style:
   - **Direct copy** – preserve existing implementation.  
   - **Auto-implement** – rebuild functionality following template standards.  
   - **Skeleton only** – copy interfaces/directories, no business logic.
4. Confirm any components that should *not* be migrated (deprecated features, sensitive files).

The AI will mirror these decisions in the worklog and plan.

---

## 3. Migration Flow

1. **Assessment**  
   - Walk through each module/service with the AI.  
   - Decide whether it becomes a module instance, shared library, or external dependency.  
   - Identify documentation to update or rewrite.
2. **Scaffolding**  
   - Run `make ai_begin MODULE=<name>` for new modules.  
   - Map existing docs into `doc_human/` and `doc_agent/` folders.  
   - Update configuration files and secrets handling to match the template.
3. **Code transfer**  
   - Copy or re-implement code according to the agreed migration style.  
   - Preserve history via references to the original repo or change logs.
4. **Validation**  
   - Execute `make module_health_check` for each module.  
   - Run `make dev_check` for whole-repo verification.  
   - Document any temporary exceptions and timelines to resolve them.

---

## 4. Post-Migration Actions

- Update `README.md`, `agent.md`, and module docs with the new architecture.  
- Record migration decisions in `doc_human/project/CHANGES_SUMMARY.md`.  
- Ensure environment configuration (`config/`, `.env` samples) reflects migrated services.  
- Remove leftover scaffolding (`doc_human/init/`, `TEMPLATE_USAGE.md`) once the repo stabilises.  
- Schedule follow-up reviews for performance, security, and documentation completeness.

---

## 5. References

- `doc_agent/init/project-init.md` – AI orchestration steps  
- `doc_agent/init/module-init.md` – Module initialization protocol  
- `doc_agent/orchestration/registry.yaml` – Module registry  
- `doc_human/guides/MODULE_INIT_GUIDE.md` – Human-facing module setup  
- `doc_human/project/CHANGES_SUMMARY.md` – Record migration outcomes


