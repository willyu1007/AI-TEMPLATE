---
audience: ai
language: en
version: quickstart
purpose: Hands-on onboarding checklist for AI agents
---
# Quick Start For TemplateAI Agents

> This file is optimized for orchestration agents. It is short, command-first, and omits historical context.

## 1. Before You Touch The Repo
- Load `agent.md` so you understand routing rules, guardrails, and document responsibilities.
- Confirm the configured language in `config/language.yaml` (or defaults) and keep all notes/comments in that language.
- Make sure you have Python 3.11+, Docker, and Make available.

## 2. Install Tooling
```bash
pip install -r requirements.txt
make deps_check
```

## 3. Initialize Shared Assets
```bash
make docgen             # refresh documentation headers and AI index
make update_baselines   # sync API/contract snapshots
make dev_check          # health gate: lint + tests + docs + guardrails
```

## 4. Spin Up A Feature Module
```bash
make ai_begin MODULE=my_feature
ls modules/my_feature/
ls tests/my_feature/
```
Generated assets:
- `modules/<module>/agent.md` - module-scoped context routing.
- `modules/<module>/doc/*.md` - runbook, test plan, data notes, etc.
- `tests/<module>/` - starter tests wired into CI.

## 5. Daily Development Loop
| Step | Command | Notes |
|------|---------|-------|
| Sync dependencies | `pip install -r requirements.txt` | Run when requirements change |
| Run targeted tests | `make test MODULE=<name>` | Each module has its own target |
| Validate docs | `make doc_style_check` | Ensures headers + language compliance |
| Guardrail review | `make guardrail_stats` | Shows which guardrails block what |
| Contract audit | `make contract_compat_check` | Required before merging API changes |

## 6. Submitting Work
1. Update the relevant doc templates (`doc_human/templates/` or module docs) with factual progress and decisions.
2. Ensure every doc you touched includes `audience`, `language`, and `purpose` front-matter.
3. Run `make dev_check`.
4. Open a PR referencing the module or subsystem and attach logs from the checks above.

## 7. Troubleshooting
- `make workflow_doctor` (if available) surfaces the last 10 guardrail failures.
- `scripts/health_check.py --module <name>` inspects coverage and error budgets.
- `scripts/doc_route_check.py` ensures `agent.md` routes point to valid documents.

Keep every change small, reference the doc roles in `/doc_agent/policies/DOC_ROLES.md`, and prefer AI documents when acting automatically.

