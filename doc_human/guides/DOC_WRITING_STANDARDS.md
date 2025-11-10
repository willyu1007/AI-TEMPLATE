---
audience: human
language: en
version: reference
purpose: Documentation writing standards
---
# Documentation Writing Standards

## Goals
- Keep every document objective, actionable, and AI-friendly.
- Enforce consistent headers (`audience`, `language`, `purpose`).
- Avoid duplicate or fluffy content.

## Language Policy
- Repository default lives in `config/language.yaml`.
- Comments, docs, reports, and templates must follow that language.
- Mention the configured language during project initialization and in workdoc templates.

## Structure
1. Front matter (audience/language/version/purpose).
2. Title + short description.
3. Sections ordered from high-level context to detailed steps.
4. Checklists/tables for actionable work.
5. References/links at the end.

## Writing Tips
- Use active voice and precise verbs.
- Replace anecdotes with measurements or commands.
- Link to scripts/docs rather than duplicating instructions.
- Keep AI docs ¡Ü150 lines; human docs can be longer but still focused.

## Maintenance Checklist
- [ ] Headers present and accurate.
- [ ] Language matches config.
- [ ] Content still relevant (remove deprecated sections).
- [ ] Linked files exist.
- [ ] Guardrail references up to date.

## Tools
- `make doc_style_check`
- `scripts/doc_route_check.py`
- `scripts/docgen.py`

## References
- `doc_agent/policies/DOC_ROLES.md`
- `doc_agent/policies/roles.md`
- `doc_human/templates/*.md`
