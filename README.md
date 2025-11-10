---
audience: both
language: en
version: summary
purpose: Repository overview for AI systems and humans
---
# TemplateAI Repository

> Opinionated AI-first project skeleton that keeps every automation, document, and guardrail lightweight enough for large language models.

---

## Goals And Fit
- Provide a reusable, enforcement-heavy template for AI-assisted delivery teams.
- Keep routing metadata and documentation roles predictable so orchestration agents stay within safe context windows.
- Ship with batteries-included automation (quality gates, database tooling, observability) so teams can focus on features.
- Scale across multiple modules, contributors, and long-running product phases.

**Use This Template When**
- You are building AI-assisted software with strict documentation and compliance gates.
- Multiple modules or squads collaborate and share the same set of guardrails.
- You need deterministic automation around database migrations, contracts, and documentation hygiene.

**Avoid It When**
- The effort is a throwaway spike or a one-person prototype.
- Documentation traceability is not required.

---

## Core Capabilities
1. **Agent-Oriented Documentation** - `agent.md` defines routing, context budgets, and document roles so coders and orchestrators can load only what they need.
2. **Workflow Automation** - `Makefile` recipes wrap quality checks (`dev_check`, `docgen`, `contract_compat_check`, etc.) and can be chained inside CI or manual sessions.
3. **Module Scaffolding** - `make ai_begin MODULE=name` spins up code, docs, and tests that already conform to the repository policies.
4. **Guardrail System** - Trigger definitions plus guardrail quickstarts prevent destructive operations (database, contracts, secrets) before they happen.
5. **Observability And Health** - Scripts inside `observability/` and `scripts/` automate tracing, metrics, health checks, and maintenance reporting.
6. **AI Workflow Patterns** - `ai/workflow-patterns/` contains ready-made task patterns and catalog entries a coordinator agent can recommend.

## Module Instances (Critical Definition)
See the canonical guide in `doc_human/guides/MODULE_INSTANCES.md` for the latest requirements.

At a glance:
- Run `make ai_begin MODULE=<name>` to scaffold a compliant directory under `modules/<name>/`.
- Complete the eight required docs (agent, CONTRACT, RUNBOOK, TEST_PLAN, CHANGELOG, BUGS, PROGRESS) and register ownership in the module instances guide plus the orchestration registry.
- Module *types* stay abstract (`doc_agent/specs/MODULE_TYPES.md`), while module *instances* wire those contracts into a domain (e.g., `1_user`, `4_sales_aggregator`).

---

## Quick Start
### 1. Install Dependencies
```bash
pip install -r requirements.txt
make deps_check        # optional consolidated verification
```

### 2. Initialize Project Assets
```bash
make docgen            # refresh documentation index and headers
make update_baselines  # sync contract baselines
make dev_check         # run the full repository health suite
```

### 3. Create A Module
```bash
make ai_begin MODULE=my_feature
ls -la modules/my_feature/
ls -la tests/my_feature/
```

---

## Repository Layout
```text
.
|-- agent.md                     # Root orchestrator contract
|-- QUICK_START.md               # Fast onboarding for agents
|-- TEMPLATE_USAGE.md            # Checklist for tailoring the template
|-- ai/                          # Workflow patterns, ledgers, and maintenance notes
|-- config/                      # Runtime configuration schema + defaults
|-- doc_agent/                   # AI-facing specs, quickstarts, and policies
|-- doc_human/                   # Human deep dives, templates, and historical notes
|-- modules/                     # Feature modules (shared scaffolding in modules/common)
|-- observability/               # Logging, tracing, metrics, and alerting configs
|-- db/engines/                  # Database schemas, migrations, and specs
|-- scripts/                     # Automation scripts used by Makefile targets
`-- tests/                       # Example Go/Python/TypeScript tests
```

---

## Documents That Matter Most
- `agent.md` - single source of truth for routing rules, guardrails, and priorities.
- `QUICK_START.md` - pragmatic cheat sheet for AI coders.
- `TEMPLATE_USAGE.md` - how to fork, rebrand, and configure the repo.
- `doc_agent/policies/DOC_ROLES.md` - authoritative responsibilities and ownership of every doc class.
- `doc_agent/quickstart/guardrail-quickstart.md` + `doc_human/guides/GUARDRAIL_GUIDE.md` - split pair of guardrail docs (light vs deep dive).

Keep AI docs lean (<=150 lines, command oriented) and keep human docs detailed but still actionable. Use the headers (`audience`, `language`, `purpose`) to prevent routing ambiguity.

---

## Workflows And Automation
- `make dev_check` - runs lint, tests, documentation freshness, routing checks, and guardrail stats.
- `make contract_compat_check` - validates interface contracts and `.contracts_baseline/` snapshots.
- `make docgen` - rewrites documentation headers and regenerates AI context indexes.
- `make db_migrate` / `make rollback_check` - executes database migrations with mandatory down scripts.
- `scripts/*.py` and `scripts/*.sh` - single-purpose utilities for docs, health, observability, and workflow triage. Each file contains its own CLI help.
- `python scripts/context_usage_tracker.py report --limit 10` - audit high-traffic docs/topics before tuning `context_routes`.

---

## Contribution Notes
1. Discuss large changes in an issue first (especially guardrails, contracts, or doc routing).
2. Keep AI-facing docs concise and English-only; heavy material lives in the human guides, still written in English for consistency.
3. Run `make dev_check` before opening a PR.
4. Update the relevant doc templates or quickstarts if the workflow or tooling changes.

---

## License
This project is distributed under the [MIT License](LICENSE).

