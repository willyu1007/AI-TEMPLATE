---
audience: human
language: en
version: reference
purpose: Strategies for deterministic test data
---
# Test Data Strategy

## Goals
- Provide realistic datasets without leaking production data.
- Keep fixtures deterministic so AI agents can rely on them.

## Approaches
1. **Static Fixtures** - SQL/JSON files under `tests/<module>/fixtures/`. Use for <=50 rows.
2. **Mock Generators** - `scripts/mock_generator.py` or module-specific factories for large datasets.
3. **Scenario Packs** - Documented in `modules/<name>/doc/TEST_DATA.md` (happy path, edge cases, failure cases).

## Workflow
1. Define scenarios and acceptance criteria.
2. Choose the mechanism (fixture vs generator).
3. Store metadata (version, owner, refresh cadence) in the module test data doc.
4. Update workdocs/tests whenever data shape changes.

## Quality Checklist
- [ ] Data uses anonymized or synthetic values.
- [ ] Language (labels, descriptions) follows repository setting.
- [ ] Regeneration scripts documented.
- [ ] Cleanup steps provided (for DB fixtures).

## Tools
- `scripts/mock_generator.py`
- `scripts/mock_lifecycle.py`
- `scripts/fixture_loader.py`

## References
- `doc_agent/coding/TEST_STANDARDS.md`
- `doc_human/templates/module-templates/TEST_DATA.md.template`

