---
audience: ai
language: en
version: summary
purpose: Testing standards for automation and contributors
---
# Testing Standards

## Strategy
```
        /\
       /E2\\      10% end-to-end
      /----\\
     /Integ\\    20% integration
    /------\\
   / Unit  \\   70% unit
  /----------\\
```
Default coverage: 80% overall, 90% for critical modules (override via `agent.md -> quality_gates.coverage_min`).

## Test Types
| Type | Goal | Examples |
|------|------|----------|
| Unit | Validate one function/class | services, utils, models |
| Integration | Validate module boundaries | API handlers + DB, external services |
| Contract | Enforce `CONTRACT.md` | schema validation, compatibility tests |
| E2E | Full workflows | smoke flows before release |

## General Rules
1. Tests must mirror the configured language (English) in names and comments.
2. Every bug fix includes a regression test.
3. Never skip guardrail or doc updates when tests imply workflow changes.

## Tooling
```bash
pytest tests/                          # Python
npm run test                           # TypeScript
go test ./...                          # Go
make test_coverage MODULE=<name>       # Coverage summary
make contract_compat_check             # Contract enforcement
make dev_check                         # Aggregate gate (lint + tests + docs)
```

## Writing Tests
- Use descriptive names: `test_user_service_creates_active_user`.
- Arrange/Act/Assert blocks or table-driven tests (Go).
- Keep fixtures deterministic; store reusable data under `tests/<module>/fixtures/`.
- Mock external services; integration tests should not hit production endpoints.

## Performance Targets
- `p50 < 1s`, `p95 < 2s`, `p99 < 3s` for latency-sensitive features.
- `QPS >= 100` in load tests with `<1%` error rate at moderate concurrency.

## Troubleshooting Checklist
1. Re-run failing tests with `-vv --maxfail=1` (pytest) or `-run` filters (Go).
2. Inspect fixtures/config for stale assumptions.
3. Use debuggers (`pytest --pdb`, `node --inspect`, `dlv test`).
4. Update docs/workdocs to reflect discovered risks.

## Mock & Test Data
- Reference `doc_human/guides/TEST_DATA_STRATEGY.md` for structure.
- Keep `modules/<name>/doc/TEST_DATA.md` synced when data shapes shift.
- Use `scripts/mock_generator.py` or `fixture_loader.py` for large datasets.

## Definition Of Done
- Tests green locally and in CI.
- Coverage threshold met.
- Guardrails (especially contract & DB) run without warnings.
- Workdocs updated with test outcomes.

These standards keep automation predictable and maintain the AI-friendly footprint.
