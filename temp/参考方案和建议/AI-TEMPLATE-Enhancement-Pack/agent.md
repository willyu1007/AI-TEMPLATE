---
spec_version: "1.0"
agent_id: "root"
role: "orchestration-policy"
merge_strategy: "child_overrides_parent"
policies:
  goals_ref: "/doc/policies/goals.md"
  safety_ref: "/doc/policies/safety.md"
context_routes:
  always_read:
    - "/doc/policies/goals.md"
    - "/doc/policies/safety.md"
  by_scope:
    - scope: "repo"
      read:
        - "/doc/orchestration/registry.yaml"
        - "/doc/indexes/context-rules.md"
    - scope: "module"
      read:
        - "modules/*/agent.md"
---

# Root Agent Guide (Light)

- 合并策略：**子级覆盖父级**（`merge_strategy = child_overrides_parent`）。
- 质量门槛与安全策略：见 `policies` 引用的文档。
- 文档路由建议：Orchestrator 读取 `context_routes` 并按需加载。
