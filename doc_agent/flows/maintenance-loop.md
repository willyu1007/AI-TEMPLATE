---
audience: ai
language: en
version: flow
purpose: Operational protocol for ongoing health checks and maintenance tasks
---

# Maintenance & Health Loop

> **Objective**: Provide a reusable sequence for AI agents to monitor repository health, triage findings, and schedule follow-up actions.

---

## 1. Cadence & Triggers

| Frequency | Trigger | Typical Command Set | Notes |
| --- | --- | --- | --- |
| **Per PR / Feature** | Post-build validation | `make dev_check`, targeted module checks | Ensure regressions are caught before merge |
| **Daily** | Scheduled maintenance window | `make health_check`, `make health_show_quick_wins` | Capture trend deltas for dashboards |
| **Weekly** | Release planning | `make health_report_detailed`, `make ai_friendliness_check` | Review outstanding issues and guardrail drifts |
| **Ad-hoc** | Incident, audit, or anomaly | Custom subsets (`make module_health_check MODULE=<name>`) | Document rationale in workdocs and issue tracker |

Always log the cadence in `/ai/maintenance_reports/health-summary.md` or the relevant workdoc.

---

## 2. Workflow Steps

1. **Preparation**  
   - Load `/doc_agent/index/AI_INDEX.md` and this playbook.  
   - Confirm scope (entire repo vs specific modules) and environment (dev/staging/prod).

2. **Run Checks**  
   - Execute agreed commands sequentially to avoid noisy output.  
   - Capture command output snippets or artifacts for evidence.

3. **Analyse Findings**  
   - Classify results: blockers, warnings, informational.  
   - Map each issue to an owner (module, doc, workflow) and link existing tickets if any.

4. **Plan Remediation**  
   - Create or update workdocs with the remediation plan.  
   - Assign due dates and note dependencies (e.g., waiting for schema approval).

5. **Communicate & Archive**  
   - Summarise outcomes in `ai/maintenance_reports/` (update `health-summary.md`).  
   - Notify stakeholders if blockers remain, referencing command outputs.  
   - Archive raw logs if needed in the observability folder.

---

## 3. Integration Points

- **Registry alignment**: check whether modules flagged by health reports are correctly registered in `/doc_agent/orchestration/registry.yaml`.  
- **Schema compliance**: if data inconsistencies surface, consult `/schemas/AGENTS.md` and relevant schema files.  
- **Guardrail stats**: `make agent_trigger_test` and `make doc_route_check` help ensure automation remains compliant.  
- **Observability**: link Prometheus/Grafana alerts (`observability/`) to the health findings for traceability.

---

## 4. Follow-up Checklist

- [ ] Health report updated with latest run timestamp and summary.  
- [ ] High-priority issues converted into actionable tasks/workdocs.  
- [ ] Related docs (`README`, module docs, runbooks) refreshed if processes changed.  
- [ ] Stakeholders notified of blockers or scheduled maintenance.  
- [ ] Next scheduled run recorded.

Use this loop to keep the repository in a “near-ready” state and to provide predictable signals for future automation or human interventions.

---

## 5. Context Usage Telemetry

- `python scripts/context_usage_tracker.py log --topic "<route topic>" --path /doc_agent/index/AI_INDEX.md`  
  记录一次文档加载事件（可在 orchestrator hook 中调用）。
- `python scripts/context_usage_tracker.py report --limit 10`  
  查看最常被读取的文档 / topic，辅助判断哪些路由应保留或压缩。
- `python scripts/context_usage_tracker.py optimize --agent AGENTS.md --limit 5`  
  基于实际使用频率建议重新排序 `context_routes`，优先展示高频、移除长期未使用的路径。
- 通过 `config/*.yaml` 中的 `telemetry.route_usage_logging` 全局开关控制是否允许自动记录（默认关闭，置为 `true` 后再调用 `maybe-log`）。

将运行结果附在 `ai/maintenance_reports/` 中，便于后续审计或复盘。
