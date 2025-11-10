---
audience: ai
language: en
version: reference
purpose: Map documentation types to owners, formats, and guardrails
---
# Documentation Roles & Responsibilities

This file tells every contributor (human or agent) what each document class does, who owns it, and how it should be written.

## 1. Classification
| Type | Identifier | Purpose | Typical Length | Owner |
|------|------------|---------|----------------|-------|
| AI Doc | `audience: ai` or "For AI Agents" banner | Fast execution guidance | <=150 lines | Feature team / agent maintainer |
| Human Doc | `audience: human` | Deep-dive background, reasoning, postmortems | 200-1000 lines | Feature team lead |
| Dual Doc | `audience: both` | Mixed audience (e.g., README) | <=300 lines | Repo maintainer |

## 2. Language & Format
- Default language is stored in `config/language.yaml`. All docs, comments, and generated reports must follow it.
- AI docs: English only, command-first, include front matter (`audience`, `language`, `purpose`).
- Human docs: still English (per policy), but may include detailed rationale, tables, math, or diagrams.
- Templates must clearly mark placeholder fields.

## 3. Ownership
| Document | Owner | Expectations |
|----------|-------|--------------|
| `agent.md` | Repo maintainers | Update routes/roles when docs change. |
| `doc_agent/*` | Automation owners | Keep concise, runnable, AI-friendly. |
| `doc_human/guides/*` | Domain experts | Capture rationale, risks, examples. |
| `modules/<name>/doc/*` | Module leads | Reflect real progress/tests/contracts. |
| Templates | Documentation guild | Keep placeholders consistent with policies. |

## 4. When To Update
- Any code change that alters workflow, guardrails, or interfaces must update both AI and human docs.
- Workdoc templates must be refreshed when initialization flow changes.
- Add doc references to `context_routes` only after confirming the doc header is accurate.

## 5. Quality Checklist
1. Audience + language header present.
2. Content matches the declared audience (no heavy prose in AI docs).
3. Links resolve and point to English documents.
4. No redundant sections¡ªremove marketing fluff, keep actionable facts.
5. Tests/automation referencing the doc have been updated (e.g., `doc_route_check`).

## 6. Enforcement
- `make doc_style_check` - verifies headers, length, non-English characters.
- `make doc_route_check` - ensures `context_routes` target real files.
- Guardrails - block merges if AI docs exceed length or use the wrong language.

## 7. Escalation Path
- Missing doc? Create it with a short AI-friendly version first, then schedule the human deep dive.
- Conflicting ownership? Default to the module owner; escalate to repo maintainers if unresolved.
- Translation required? Adjust `config/language.yaml` and regenerate docs; avoid mixing languages inside a single file.

## 8. Reference Table
| Topic | AI Doc | Human Doc |
|-------|--------|-----------|
| Guardrails | `doc_agent/quickstart/guardrail-quickstart.md` | `doc_human/guides/GUARDRAIL_GUIDE.md` |
| Workdocs | `ai/workdocs/README.md` | `doc_human/guides/WORKDOCS_GUIDE.md` |
| Configuration | `config/README.md` | `doc_human/guides/CONFIG_GUIDE.md` |
| Testing | `doc_agent/coding/TEST_STANDARDS.md` | `doc_human/guides/TEST_DATA_STRATEGY.md` |
| Modules | `doc_agent/specs/MODULE_TYPES.md` | `doc_human/guides/MODULE_INSTANCES.md` |

Keep this document updated whenever a new doc type is introduced or retired.

