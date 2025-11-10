---
audience: human
language: en
version: reference
purpose: Explain the dataflow analysis workflow
---
# Dataflow Analysis Guide

## Objectives
- Understand how data moves through services, queues, and databases.
- Use automation to visualize and validate flows before risky changes.

## Toolkit
- `scripts/dataflow_trace.py` - static + dynamic analysis, bottleneck detection.
- `scripts/dataflow_visualizer.py` - Mermaid, DOT, HTML outputs.
- `scripts/bottleneck_rules.yaml` - tunable heuristics.

## Process
1. Update `doc_human/templates/dataflow-summary.md` for the task/module.
2. Run `make dataflow_trace DAG=doc/flows/dag.yaml`.
3. Review output (JSON + Markdown) and attach to workdoc.
4. Generate visual assets via `make dataflow_visualize`.
5. Address warnings (cycles, missing contracts, throughput limits).

## Best Practices
- Keep DAG definitions current; outdated graphs mislead guardrails.
- Annotate critical paths with owners and SLOs.
- Capture throughput/latency budgets in module runbooks.
- Use consistent naming so guardrails recognize components.

## References
- `doc_agent/quickstart/dataflow-quickstart.md`
- `doc_human/templates/dataflow-summary.md`
- `ai/workflow-patterns/` (patterns suggest when to run analysis).

