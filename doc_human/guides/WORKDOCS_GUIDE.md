---
audience: human
language: en
version: reference
purpose: End-to-end instructions for AI workdocs
---
# Workdocs Guide

## Purpose
Teach humans how to capture task context so AI agents can resume work in minutes instead of hours.

## Structure
Each workdoc folder (`ai/workdocs/active/<task>/`) contains:
1. `plan.md` - scope, phases, success metrics.
2. `context.md` - progress log, blockers, quick resume, language setting reminder.
3. `tasks.md` - checklist with owners, status, acceptance criteria.

## Workflow
1. **Create** - `make workdoc_create TASK=<name>` or copy templates from `doc_human/templates/`.
2. **Maintain** - update `context.md` after every milestone, log blockers + mitigations, mention guardrail outcomes.
3. **Close** - move to `archive/` via `make workdoc_archive TASK=<name>` and summarize learnings.

## Best Practices
- Keep bullet points short; link to PRs/tests instead of embedding logs.
- Use the configured language (see `config/language.yaml`) for every section.
- Record guardrail blocks/warnings and how you resolved them.
- Attach references (docs, scripts, dashboards) instead of duplicating content.

## Quality Checklist
- [ ] `plan.md` updated when scope changes.
- [ ] `context.md` shows latest status, blockers, and next step.
- [ ] `tasks.md` statuses match actual progress.
- [ ] Archive includes success/failure summary and follow-up tasks.

## Related Files
- Templates under `doc_human/templates/workdoc-*.md`.
- Scripts: `scripts/workdoc_create.sh`, `scripts/workdoc_archive.sh`.
- AI quick reference: `ai/workdocs/README.md`.

