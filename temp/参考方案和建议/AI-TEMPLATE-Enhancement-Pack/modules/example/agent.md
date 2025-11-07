---
spec_version: "1.0"
agent_id: "modules.example.M_AI_Select"
role: "API layer coordinator"
level: 3
module_type: "3_SelectMethod"
ownership:
  code_paths:
    include: ["modules/example/"]
    exclude: ["modules/*/doc/CHANGELOG.md"]
io:
  inputs:
    - name: "request"
      schema_ref: "schemas/request.json"
  outputs:
    - name: "response"
      schema_ref: "schemas/response.json"
contracts:
  apis: []
dependencies:
  upstream: ["M_Assign_Select"]
  downstream: []
constraints:
  - "must not access DB directly"
tools_allowed:
  calls: ["http", "fs.read", "queue.publish"]
  models: ["gpt-4.1-mini", "reranker-v2"]
quality_gates:
  required_tests: ["unit", "contract", "e2e"]
  coverage_min: 0.75
orchestration_hints:
  triggers: ["on_http_request"]
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
AI 自动选题实例。

## Responsibilities
- 接收请求，校验参数，转发至核心逻辑

## Limitations
- 不直连 DB

## I/O Examples
```json
{ "input": { "foo": "bar" } }
```

## Test & SLO
- 必须通过 CONTRACT/TEST_PLAN；P95 < 200ms。
