---
audience: human
language: en
version: reference
purpose: Define system boundaries
---
# System Boundary

## Scope
- **Included**: workflow automation, guardrails, module scaffolding, docs, scripts.
- **Excluded**: production deployments, proprietary services, secret storage.

## Actors
| Actor | Responsibilities |
|-------|------------------|
| AI Agents | Follow `AGENTS.md`, respect guardrails |
| Maintainers | Update docs, approve risky changes |
| Contributors | Implement features/tests per template |

## Interfaces
- APIs exposed by modules (see `modules/<name>/doc/CONTRACT.md`).
- CLI/Make targets documented in `doc_human/reference/commands.md`.
- Observability stack input/output (logging, metrics, tracing).

## Constraints
- Language consistency (`config/language.yaml`).
- Guardrails block high-risk changes.
- Documentation must stay lean for AI context budgets.

## Dependencies
- Postgres, Redis, CI/CD, observability stack.

Use this file when planning new work or evaluating integrations.
