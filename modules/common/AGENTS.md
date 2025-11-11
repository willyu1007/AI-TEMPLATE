---
spec_version: "1.0"
agent_id: "modules.common.v1"
role: "Provide common utilities and infrastructure code - Shared across all modules"
level: 1
module_type: "0_Infrastructure/Common"

ownership:
  code_paths:
    include:
      - modules/common/utils/*
      - modules/common/models/*
      - modules/common/middleware/*
      - modules/common/constants/*
      - modules/common/interfaces/*
    exclude: []

io:
  inputs:
    - name: "function_call"
      type: "mixed"
      required: true
      description: "Other modules call common utility functions"
      schema_ref: "modules/common/doc/CONTRACT.md#API"
      examples:
        - "validate_email(email: str) -> bool"
        - "PaginationParams(page: int, page_size: int)"
        - "@require_auth decorator"
  
  outputs:
    - name: "function_result"
      type: "mixed"
      required: true
      description: "Return processed/validated data"
      schema_ref: "modules/common/doc/CONTRACT.md#API"
      examples:
        - "bool (validation functions)"
        - "formatted string (string utils)"
        - "model instance (models)"

contracts:
  apis:
    - modules/common/doc/CONTRACT.md

dependencies:
  upstream: []
  downstream: ["*"]  # All modules can use common

constraints:
  - "Zero business logic - only technical utilities"
  - "Test coverage >= 90%"
  - "Backward compatibility required"
  - "No dependencies on business modules"

tools_allowed:
  calls:
    - fs.read
    - fs.write

quality_gates:
  required_tests:
    - unit
  coverage_min: 0.90

policies:
  goals:
    - "Provide stable, reusable utilities"
    - "Maintain zero business logic principle"
    - "Ensure backward compatibility"
    - "Achieve ≥90% test coverage"
  
  safety:
    - "No dependencies on business modules (modules/*)"
    - "All public functions must have unit tests"
    - "Breaking changes require deprecation warnings"
    - "Version compatibility must be maintained"

context_routes:
  always_read:
    - /modules/common/README.md
  
  on_demand:
    - topic: "API Contract"
      when: "Check exported helpers and types before using or extending."
      paths:
        - /modules/common/doc/CONTRACT.md
    - topic: "Changelog"
      when: "Review deprecations or behavior changes impacting consumers."
      paths:
        - /modules/common/doc/CHANGELOG.md

merge_strategy: "child_overrides_parent"

---
# Common Module Agent Guide

> Shared technical helpers live in `modules/common`. This agent keeps scope narrow so business modules remain decoupled.

## Scope
- Provide reusable utilities, models, middleware, and constants.
- Enforce zero business logic and backward compatibility.
- Require >=90 percent unit test coverage across exported helpers.

## Context Shortcuts
| Need | Load | Purpose |
| --- | --- | --- |
| Quick reference | `/modules/common/README.md` | Lists available helpers |
| Contract | `/modules/common/doc/CONTRACT.md` | Supported APIs and types |
| Changelog | `/modules/common/doc/CHANGELOG.md` | Deprecations or upgrades |

## Working Rules
1. Add code only when at least two modules need the helper.
2. Update the contract and README whenever you add or deprecate symbols.
3. Keep imports one-way: business modules can depend on `modules.common`, not the other way around.

## Commands
```bash
pytest tests/common/ --cov=modules.common
make dev_check
```

## Safety
- No business rules, persistence logic, or network calls inside this module.
- Maintain backward compatible signatures; add wrappers when changing behavior.
- Document deprecation plans in the changelog and PR summary.

## References
- `/modules/common/README.md`
- `/modules/common/doc/CONTRACT.md`
- `/modules/common/doc/CHANGELOG.md`

Coverage targets and policies live in the contract; no extra version tag needed here.

