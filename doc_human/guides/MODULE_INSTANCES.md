---
audience: human
language: en
version: reference
purpose: Document existing module instances
---
# Module Instances Guide

## Purpose
Track every module built from the template and describe its contracts, ownership, and health. This guide is referenced by `README.md`, `agent.md`, and `doc_agent/specs/MODULE_TYPES.md`, so treat it as the canonical checklist.

## Definition
- A **module instance** is a concrete implementation created from a module type (see `doc_agent/specs/MODULE_TYPES.md`) and kept under `modules/<name>/`.
- Each instance must include: `agent.md`, `doc/CONTRACT.md`, runbook (`doc/RUNBOOK.md`), active workdoc, tests, and health metrics hooks.
- Module types stay abstract; module instances apply those contracts to a domain such as `1_user` or `4_sales_aggregator`.
- Register new instances immediately after running `make ai_begin MODULE=<name>` and keep ownership plus escalation data current.

## Required Fields (per module)
- Name + directory path.
- Owners + escalation contacts.
- Contracts/interfaces (link to `CONTRACT.md`).
- Docs: runbook, progress log, test plan, test data.
- Guardrails enabled (db, contract, workflow).

## Maintenance Workflow
1. When scaffolding a module (`make ai_begin MODULE=name`), register it here.
2. Update entries whenever ownership or contracts change.
3. Link to workdocs for active initiatives.
4. Mark deprecated modules and describe migration plans.

## Checklist
- [ ] Module agent file updated.
- [ ] Documentation templates filled and referenced here.
- [ ] Tests + health metrics linked.
- [ ] Language consistency verified.

## References
- `modules/<name>/doc/*.md`
- `doc_human/templates/module-templates/`
- `doc_agent/policies/DOC_ROLES.md`
