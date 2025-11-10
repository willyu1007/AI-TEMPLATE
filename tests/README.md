# Tests Directory

This folder keeps every automated test harness used by the template. The structure is language-agnostic and works for Python, TypeScript, and Go.

## Layout
```text
tests/
|-- README.md
|-- conftest.py          # global pytest fixtures
|-- example/             # sample module tests
|   |-- test_smoke.py
|   |-- Button.spec.ts
|   |-- user_test.go
|   `-- ...
`-- e2e/                 # optional end-to-end suites
```
Create `tests/<module>/` for each module so ownership stays obvious.

## Test Types
| Type | Purpose | Location | Frequency |
|------|---------|----------|-----------|
| Unit | Validate a single function/class | `test_unit.py`, `*_test.go` | Every change |
| Integration | Exercise module boundaries + mocks | `test_integration.py` | Every change |
| Smoke | Ensure main flows run | `test_smoke.py` | Every push |
| E2E | Full-stack stories | `tests/e2e/` | Before release |

## Commands
**Python / pytest**
```bash
pytest tests/                      # full suite
pytest tests/example/test_smoke.py  # targeted
pytest --cov=modules tests/         # coverage
pytest --lf                         # rerun last failures
```

**TypeScript / Vitest**
```bash
npm run test
npm run test -- Button.spec.ts
npm run test:coverage
```

**Go**
```bash
go test ./...
go test -race ./tests/example/
go test -bench=. ./tests/example/
```

## Quality Gates
- Coverage target: 80% per module (configurable in CI).
- Tests must honor the repository language in comments and assertions.
- Use fixtures/test data from `doc_human/templates` to keep scenarios realistic.

## Performance Targets (if applicable)
- Latency: `p50 < 1000ms`, `p95 < 2000ms`, `p99 < 3000ms`.
- Throughput: `QPS >= 100` under synthetic load.
- Error rate: `<1%` at moderate concurrency, `<5%` at peak.

## Troubleshooting Checklist
1. Rerun with verbose output: `pytest -vv --tb=long`.
2. Execute the single failing test with `pytest path::TestClass::test_case`.
3. Inspect fixtures/mocks for stale data.
4. Use `pytest --pdb` or language-specific debuggers for deep dives.
5. Update docs (`modules/<name>/doc/TEST_PLAN.md`) if acceptance criteria change.

## CI Integration
- GitHub Actions executes `make dev_check` on push/PR.
- Add new language/tooling by extending `.github/workflows/ci.yml` and corresponding Make targets.

## References
- `agent.md` ¡ì6 - testing standards.
- `modules/*/doc/TEST_PLAN.md` - module-level expectations.
- `doc_human/guides/TEST_DATA_STRATEGY.md` - how to craft fixtures.

