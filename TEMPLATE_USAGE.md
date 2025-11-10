---
audience: both
language: en
version: playbook
purpose: Explain how to adapt the template to a new project
---
# Template Usage Guide

This guide is intentionally pragmatic. It tells you exactly what to change when cloning this repository for a new initiative.

## 1. Rename And Rebrand
1. Update the repository name everywhere (`README.md`, `agent.md`, `doc_human/project/*.md`).
2. Change the maintainer/contact references in `README.md` and `doc_human/project/IMPLEMENTATION_SUMMARY.md`.
3. Review license requirements; keep MIT unless legal says otherwise.

## 2. Configure Language And Audience Defaults
- Set `config/language.yaml` (see `config/README.md`) to the language your team uses.
- During project initialization remind contributors that code comments, reports, and docs must follow the configured language.
- Update `agent.md` `context_routes` so they only point to docs that exist in that language.

## 3. Customize Modules
- Edit `modules/common` to reflect shared utilities or delete what you do not plan to support.
- Generate the first module with `make ai_begin MODULE=my_feature` and adjust the produced templates.
- Populate `modules/<module>/doc/*.md` with real plans, progress, and tests; those docs double as guardrail inputs.

## 4. Tailor Automation
| Area | File | What To Modify |
|------|------|----------------|
| Contracts | `.contracts_baseline/` | Replace example contracts with your APIs |
| Database | `db/engines/postgres/` | Drop demo migrations and create your own up/down scripts |
| Observability | `observability/*` | Point to the real Grafana, Jaeger, logging stacks |
| Scripts | `scripts/*.py` | Keep only the health/guardrail checks you need |
| CI | `.github/workflows/` | Map Make targets to CI jobs |

## 5. Documentation Policy
- `doc_agent/` stays lean and English.
- `doc_human/` can hold long-form background, but still keep it actionable and in the configured language.
- Maintain `doc_agent/policies/DOC_ROLES.md` when you add or delete document types.

## 6. Quality And Guardrails
- Revisit guardrail triggers inside `doc_agent/orchestration/agent-triggers.yaml` to match your risk model.
- Update `scripts/guardrail_stats.py` thresholds if your pipeline has different tolerance.
- Align `Makefile` quality gates with whatever your CI/CD pipeline expects.

## 7. Checklist Before First Sprint
- [ ] `agent.md` updated with your modules and docs.
- [ ] `config/defaults.yaml` (and secrets) filled with correct endpoints.
- [ ] `README.md`, `QUICK_START.md`, and `TEMPLATE_USAGE.md` mention the correct product name.
- [ ] Language configuration verified and pinned.
- [ ] Guardrails tested via `make dev_check`.
- [ ] First workdoc created using `doc_human/templates/workdoc-plan.md`.

Keep the template opinionated: remove anything you will not maintain, and do not add fluffy narrative. Every paragraph should either instruct a person/agent or describe a guardrail.
