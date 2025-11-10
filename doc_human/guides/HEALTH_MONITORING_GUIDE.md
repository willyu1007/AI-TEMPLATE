---
audience: human
language: en
version: reference
purpose: Health monitoring playbook
---
# Health Monitoring Guide

## Objectives
- Track service health across availability, latency, error rate, and budget burn-down.
- Provide repeatable procedures for detecting and responding to regressions.

## Metrics
| Domain | Metric | Target |
|--------|--------|--------|
| Availability | SLO uptime | ¡Ý 99.5% |
| Latency | p50/p95/p99 | <1s / <2s / <3s |
| Errors | 4xx/5xx rate | <1% |
| Capacity | CPU/Mem usage | <70% sustained |

## Monitoring Stack
- Prometheus + Grafana dashboards (`observability/metrics/*`).
- Alertmanager routes (critical vs warning channels).
- Jaeger tracing for request-level debugging.
- Log pipelines (Logstash/Fluentd) for context.

## Runbook
1. Alert fires ¡ú check dashboard + logs.
2. Correlate with deployments/guardrail hits.
3. Capture findings in module `RUNBOOK.md` + workdoc.
4. File follow-up tasks if automation/gaps exist.

## Language Policy
Dashboards, alert titles, and runbook steps must match `config/language.yaml` so AI agents and humans stay aligned.

## References
- `observability/README.md`
- `modules/<name>/doc/RUNBOOK.md`
- `scripts/health_check.py`, `scripts/health_trend_analyzer.py`
