---
audience: human
language: en
version: template
purpose: Module README template
---
# <Module Name>

## Summary
- **Owner(s)**: <team/member>
- **Purpose**: <short description>
- **Status**: active / maintenance / deprecated

## Capabilities
- Feature 1
- Feature 2

## Interfaces
- APIs: link to `doc/CONTRACT.md`
- Events/Queues: <list>
- Dependencies: <services/modules>

## Documentation
| Doc | Path |
|-----|------|
| Contract | `modules/<name>/doc/CONTRACT.md` |
| Runbook | `modules/<name>/doc/RUNBOOK.md` |
| Test Plan | `modules/<name>/doc/TEST_PLAN.md` |
| Test Data | `modules/<name>/doc/TEST_DATA.md` |
| Progress Log | `modules/<name>/doc/PROGRESS.md` |

## Setup
```
make module_bootstrap MODULE=<name>
```
Add extra instructions if the module requires additional services or feature flags.

Keep language consistent with `config/language.yaml`.
