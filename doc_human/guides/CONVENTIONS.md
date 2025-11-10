---
audience: human
language: en
version: reference
purpose: Comprehensive coding conventions for TemplateAI
---
# Coding Conventions

## Purpose
Provide a single reference for humans when making non-trivial design or implementation decisions. AI agents should use `doc_agent/coding/AI_CODING_GUIDE.md` instead.

## Language & Style
- Follow the repository language (English) for comments, docstrings, commits, and docs.
- Prefer explicit names, consistent casing, and descriptive commit titles (`type(scope): summary`).
- Avoid duplicated explanations¡ªlink to guides when needed.

## Python
- PEP 8 + project linters.
- Async code uses `asyncio` or framework event loops; never mix blocking IO.
- Use type hints everywhere; run `mypy` when modules expose public APIs.

## TypeScript / Vue
- Use Composition API + `<script setup>` in Vue components.
- Keep components <200 lines; extract composables when logic repeats.
- ESLint + Prettier enforce formatting; do not bypass.

## Go
- Keep packages focused; avoid cross-package global state.
- `context.Context` must be the first parameter in exported functions.
- Use structured logging (`log/slog` or `zap`).

## Database
- Use migrations for every schema change; never edit tables manually.
- UUID v7 primary keys, TIMESTAMPTZ timestamps, snake_case columns.
- Document schema updates in `schemas/tables/*.yaml` and module docs.

## Testing & Docs
- Tests mirror the change size; update module `TEST_PLAN.md`.
- Workdocs capture context, blockers, and decisions.
- Keep doc headers (`audience/language/purpose`) accurate.

## Review Checklist
- Code matches module conventions.
- Comments/logs/docstrings are in English and objective.
- Guardrails run cleanly.
- Documentation responsibilities respected (AI vs human docs).

Use this file as the human deep dive; keep AI references lean.
