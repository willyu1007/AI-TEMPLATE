---
audience: human
language: en
version: reference
purpose: Checklist for preparing DB test data
---
# DB Test Data Checklist

## Steps
1. Identify scenarios (happy path, edge cases, failure) and map them to fixtures or generators.
2. Create SQL/CSV fixtures or generation scripts under `tests/<module>/fixtures/`.
3. Document dataset metadata in `modules/<module>/doc/TEST_DATA.md` (owner, refresh cadence, dependencies).
4. Load data via `scripts/fixture_loader.py` or module-specific helpers.
5. Clean up after tests to avoid cross-suite interference.

## Quality Rules
- Only synthetic/anonymized data.
- Keep timestamps, locales, and text in the repository language.
- Provide rollback instructions for every fixture.
- Version datasets if schema evolves.

## References
- `doc_human/guides/TEST_DATA_STRATEGY.md`
- `modules/<module>/doc/TEST_DATA.md`
- `scripts/mock_generator.py`
