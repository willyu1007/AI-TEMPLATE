---
audience: human
language: en
version: reference
purpose: UX handoff and best practices
---
# UX Guide

## Goals
Align product, design, and engineering so experiences remain consistent while AI agents execute tasks.

## Process
1. Capture UX briefs (problem, audience, success metrics) in workdocs.
2. Store design artifacts (Figma links, screenshots) in the same folder.
3. Translate UX decisions into acceptance criteria inside module `TEST_PLAN.md`.
4. Reference `ai/workflow-patterns` when automating UI-heavy work.

## Guidelines
- Keep copy, labels, and error messages in the repository language (English by default).
- Document accessibility requirements (contrast, keyboard flows, ARIA roles).
- Describe responsive behavior (breakpoints, layout changes) succinctly.
- Provide states for loading, empty, error, and success flows.

## Handoff Checklist
- [ ] UX brief approved.
- [ ] Components mapped to existing design system tokens.
- [ ] Measurements/specs linked.
- [ ] Acceptance criteria in tests/workdocs.

## References
- `doc_human/reference/commands.md` for CLI references embedded in docs.
- `modules/example/` for sample UX-to-code mapping.
