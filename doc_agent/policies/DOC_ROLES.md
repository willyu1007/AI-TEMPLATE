---
audience: ai
language: en
version: reference
purpose: Canonical document roles for AI orchestration
---
# Document Roles

## Types
- **AI Docs** - ¡Ü150 lines, English-only, command-oriented (`agent.md`, quickstarts, specs in `doc_agent/`).
- **Human Docs** - detailed references (`doc_human/`, module templates, project reports); still written in English per repository policy.
- **Dual Docs** - shared references such as `README.md`.

## Routing
- `context_routes.always_read` must include only lightweight AI docs.
- `context_routes.on_demand` references AI docs first; link to human docs only when deep dives are necessary.
- Respect `audience`, `language`, `priority`, and `skip_for_ai` headers before loading a file.

## Responsibilities
| Area | AI Doc Owner | Human Doc Owner |
|------|--------------|-----------------|
| Policies & guardrails | Maintainers | Security/quality owners |
| Module docs | Module leads | Module leads |
| Templates | Documentation guild | Documentation guild |
| Workdocs | Task owners | Task owners |

## Standards
1. Every doc must include front matter (`audience`, `language`, `purpose`).
2. Keep content objective and actionable; remove fluff.
3. Update module docs whenever code or guardrails change.
4. Mention the configured language (`config/language.yaml`) in onboarding docs and templates.
5. Run `make doc_style_check` to enforce headers, encoding, and language.

## Verification
```bash
make doc_style_check
make doc_route_check
```

Use this file along with `doc_agent/policies/roles.md` when adding or retiring documentation.

