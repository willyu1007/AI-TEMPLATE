---
audience: ai
language: en
version: sample
purpose: Example module agent config
---
spec_version: "1.0"
agent_id: "module.example"
role: "demo module"
merge_strategy: "child_overrides_parent"
context_routes:
  always_read:
    - /modules/example/doc/CONTRACT.md
  on_demand:
    - topic: "Example Module"
      priority: medium
      paths:
        - /modules/example/doc/RUNBOOK.md
        - /modules/example/doc/TEST_PLAN.md
ownership:
  code_paths:
    - /modules/example/
