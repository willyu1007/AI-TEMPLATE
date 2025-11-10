---
spec_version: "1.0"
agent_id: "tests"
role: "Test infrastructure and test suites for all modules"

policies:
  goals_ref: /doc_agent/policies/goals.md
  safety_ref: /doc_agent/policies/safety.md

parent_agent: /agent.md
merge_strategy: "child_overrides_parent"

constraints:
  - "Test coverage >= 80% overall"
  - "Critical modules >= 90% coverage"
  - "All tests must be deterministic"
  - "Tests must respect language configuration"

quality_gates:
  coverage_min: 0.80
  critical_coverage_min: 0.90

context_routes:
  always_read:
    - /tests/README.md
  on_demand:
    - topic: "Testing Standards"
      priority: high
      paths:
        - /doc_agent/coding/TEST_STANDARDS.md
        - /doc_human/guides/TEST_DATA_STRATEGY.md
    - topic: "Mock Data Generation"
      priority: medium
      paths:
        - /doc_agent/coding/MOCK_RULES.md
---
# Tests Agent Guide

> Single-source reference for keeping repository tests deterministic, fast, and coverage-compliant.

## Scope
- Organize pytest/Jest/Go tests under `tests/` and mirror module structure.
- Guard required coverage (>=80% overall, >=90% for marked critical modules).
- Route AI agents to lightweight docs first (`tests/README.md`, `doc_agent/coding/TEST_STANDARDS.md`).

## Context Shortcuts
| Need | Load | Purpose |
| --- | --- | --- |
| Directory overview | `/tests/README.md` | Layout, language matrix, human escalation notes |
| AI testing rules | `/doc_agent/coding/TEST_STANDARDS.md` | Deterministic patterns, language policy |
| Test data strategy | `/doc_human/guides/TEST_DATA_STRATEGY.md` | Fixture ownership plus retention |

Keep context usage under 120 lines: skim README summary, then open module-specific docs only when requested.

## Standard Flow
1. **Plan** - Identify module scope, confirm coverage expectations, decide on fixtures or mocks.
2. **Build** - Scaffold via `make tests_scaffold MODULE=<name>` or copy existing suites.
3. **Execute** - Run focused language command first, then `make test_check` when stabilizing.
4. **Report** - Capture coverage gaps, update module-specific TEST_PLAN if deltas matter.

## Commands
```bash
make test_check                # All languages, deterministic gate
make test_coverage             # Coverage snapshot (aggregated)
pytest tests/<module>/ -q      # Python focus
npm run test -- <pattern>      # TypeScript focus
go test ./tests/...            # Go focus
```

## Coverage and Hygiene Rules
- Keep flaky tests out of mainline; quarantine under `tests/example/` if investigation is pending.
- Prefer fixtures plus builders over ad-hoc inline JSON.
- Record any skipped critical tests in the work summary (link to blocker or decision).
- Clean generated artifacts via `make cleanup_tmp` when suites emit reports.

## Hand-offs
- When changing contracts, update related module TEST_PLANs before merging.
- Coordinate with `scripts/test_status_check.py` owners if manual QA sign-off is required.

## References
- `/tests/README.md`
- `/doc_agent/coding/TEST_STANDARDS.md`
- `/doc_human/guides/TEST_DATA_STRATEGY.md`

Version: auto-aligned with repository main; no per-agent versioning tracked.

