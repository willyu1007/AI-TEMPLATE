---
audience: human
language: en
version: reference
purpose: Full rationale for workflow patterns
---
# Workflow Patterns Guide

This guide explains why each workflow pattern exists, how to adapt it, and how to extend the catalog without breaking the guardrail system.

## 1. Philosophy
- Patterns are **deterministic** checklists that agents can execute with minimal context.
- Each pattern must map to a tangible deliverable (code, docs, migration, etc.).
- Guardrails reference these patterns to enforce pre-checks (e.g., database migrations must follow the migration pattern).

## 2. Pattern Lifecycle
| Stage | Owner | Artifacts |
|-------|-------|-----------|
| Proposal | Maintainer | Draft YAML + rationale | 
| Review | Guardrail owners | Validate steps, risk levels, triggers |
| Pilot | Module team | Apply pattern in real workdoc |
| Publish | Repository maintainer | Merge YAML + update catalog |
| Retire | Maintainer | Archive YAML and remove triggers |

## 3. Pattern Structure (YAML)
```yaml
id: module-creation
name: Module Creation
category: development
complexity: medium
priority: P0
estimation:
  total_hours: 4
prechecks:
  - Ensure story/issue is linked
workflow:
  - step: Review requirements
    owner: module lead
    output: confirmed scope
pitfalls:
  - Incomplete contract baseline
quality_gates:
  - make dev_check
references:
  - /AGENTS.md#modules
```
Keep names machine friendly (kebab-case). Include `references` to docs so agents know what to load.

## 4. Pattern Library Notes
### Module Creation
- Validates module naming, scaffolding, and documentation templates.
- Requires updating `modules/<name>/AGENTS.md` and running `make docgen`.

### Database Migration
- Forces paired up/down SQL files and schema validation.
- Requires `make db_migrate` + `make rollback_check`.

### API Development
- Focuses on contract updates, tests, and doc sync.
- Guardrail ensures `.contracts_baseline` is updated.

### Bug Fix
- Lightweight, optimized for rapid fixes with root-cause references.
- Includes regression tests before merge.

### Refactoring
- Emphasizes safety nets: snapshots, coverage, and feature flags.

### Feature Development
- Combines planning, implementation, QA, and documentation tasks.

### Performance Optimization
- Adds profiling, benchmarking, and rollback plan steps.

### Security Audit
- Requires dependency scans, threat review, and access verification.

## 5. Extending The Catalog
1. Clone an existing YAML as a template.
2. Add or update guardrail triggers if the new workflow mitigates a new risk class.
3. Update `PATTERNS_GUIDE.md` with rationale: what problem it solves, anti-patterns, and metrics.
4. Ensure tests/examples exist (see `ai/workflow-patterns/examples/`).

## 6. Collaboration With Guardrails
- Guardrail quickstart references pattern IDs to auto-surface the right checklist.
- Patterns can mark **blockers** (hard stops) vs **warnings**; align with guardrail severity.

## 7. Maintenance Checklist
- [ ] Every YAML validated with `make workflow_validate`.
- [ ] `catalog.yaml` regenerated.
- [ ] README kept under 150 lines.
- [ ] PATTERNS_GUIDE remains objective (no anecdotes) and English-only.
- [ ] Deprecated patterns moved to `archive/` and removed from catalog.

## 8. FAQ
**Q: When to split a pattern?**
A: When two sets of steps differ by more than 30% or have different guardrails.

**Q: Can patterns trigger scripts?**
A: Yes. Add `automation` entries referencing `scripts/*.py` commands.

**Q: How to handle language variants?**
A: Do not duplicate patterns. Instead, enforce the repo language via `config/language.yaml` and note translation needs inside workdocs if required.

---
Keep this guide actionable. If content drifts toward storytelling, move it to the project wiki instead.
