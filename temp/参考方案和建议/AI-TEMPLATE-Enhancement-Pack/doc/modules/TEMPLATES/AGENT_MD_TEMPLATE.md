---
spec_version: "1.0"
agent_id: "modules.<entity>.<instance>"
role: "API layer coordinator"
level: 3
module_type: "3_SelectMethod"
ownership:
  code_paths:
    include: ["modules/<entity>/"]
    exclude: ["modules/*/doc/CHANGELOG.md"]
io:
  inputs:
    - name: "request"
      schema_ref: "schemas/request.json"
  outputs:
    - name: "response"
      schema_ref: "schemas/response.json"
contracts:
  apis: ["openapi://modules/<entity>/openapi.yaml"]
dependencies:
  upstream: ["modules.data.query"]
  downstream: ["orchestrator.main"]
constraints:
  - "must not access DB directly"
tools_allowed:
  calls: ["http", "fs.read", "queue.publish"]
  models: ["gpt-4.1-mini", "reranker-v2"]
quality_gates:
  required_tests: ["unit", "contract", "e2e"]
  coverage_min: 0.75
orchestration_hints:
  triggers: ["on_http_request", "batch_nightly"]
  routing_tags: ["io:json", "domain:assign"]
  priority: 5
context_routes:
  always_read:
    - "/doc/policies/goals.md"
    - "/doc/policies/safety.md"
  on_demand:
    - topic: "api"
      paths: ["./doc/CONTRACT.md"]
    - topic: "ops"
      paths: ["./doc/RUNBOOK.md"]
---

# Summary
简述该 Agent 能力边界与使用前提。

## Responsibilities
- Route requests
- Validate payloads
- Delegate to core logic

## Limitations
- 不允许直连数据库；必须通过 Data Agent。

## I/O Examples
```json
{{ "input": { "foo": "..." } }}
```

## Test & SLO
- 必须通过 CONTRACT/TEST_PLAN；P95 延迟 < 200ms（示例）。

## Runbook
- 故障定位→旁路→回滚→恢复：见 `./doc/RUNBOOK.md`
