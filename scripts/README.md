# Scripts Directory

This folder contains every automation hook referenced by the Makefile or documentation. Each script prints friendly `[ok]`, `[warn]`, `[error]` messages and exits non-zero on failure.

## Categories
### Documentation
| Script | Purpose | Command |
|--------|---------|---------|
| `docgen.py` | Refresh headers and AI index | `make docgen` |
| `doc_style_check.py` | Validate language, headers, encoding | `make doc_style_check` |

### Contracts & DAGs
| Script | Purpose | Command |
|--------|---------|---------|
| `dag_check.py` | Validate DAG definitions / cycles | `make dag_check` |
| `contract_compat_check.py` | Compare contracts with baseline | `make contract_compat_check` |

### Database
| Script | Purpose | Command |
|--------|---------|---------|
| `migrate_check.py` | Ensure up/down pairs exist | `make migrate_check` |
| `rollback_check.sh` | Dry-run rollback | `make rollback_check PREV_REF=<tag>` |
| `db_lint.py` | Lint schemas, migrations, docs | `make db_lint` |

### Configuration & Consistency
| Script | Purpose | Command |
|--------|---------|---------|
| `runtime_config_check.py` | Validate runtime config vs schema | `make runtime_config_check` |
| `consistency_check.py` | Cross-doc consistency | `make consistency_check` |
| `app_structure_check.py` | Enforce folder layout | `make app_structure_check` |

### Dependencies & Testing
| Script | Purpose | Command |
|--------|---------|---------|
| `deps_manager.py` | Detect missing deps | `make deps_check` |
| `test_scaffold.py` | Generate test boilerplate | `make tests_scaffold MODULE=<name>` |
| `test_status_check.py` | Track manual test state | `make test_status_check` |
| `test_coverage_check.py` | Report coverage per module | `make test_coverage` |

### Frontend Types
`generate_openapi.py`, `generate_frontend_types.py`, `frontend_types_check.py` keep API and TS types in sync.

### Workflow & Guardrails
- `agent_lint.py`, `registry_check.py`, `doc_route_check.py`, `type_contract_check.py`, `doc_script_sync_check.py`, `registry_gen.py`, `module_doc_gen.py` enforce agent routing + module metadata.
- `agent_trigger.py` powers the intelligent trigger system.
- `workflow_suggest.py`, `workflow_suggest` Make targets, and pattern helpers live alongside the workflow catalog.

### Dataflow + Observability
- `dataflow_trace.py`, `dataflow_visualizer.py`, and `bottleneck_rules.yaml` analyze runtime flows.
- `observability_check.py`, `log`/`metrics` configs, and Jaeger/Prometheus helpers ensure telemetry readiness.

### Maintenance & Utilities
- `ai_maintenance.py` - scheduled maintenance aggregator.
- `workdoc_create.sh`, `workdoc_archive.sh` - manage AI workdocs.
- `mock_generator.py`, `mock_lifecycle.py`, `fixture_loader.py` - manage test data.
- `refactor_suggest.py`, `complexity_check.py`, `ai_friendliness_check.py`, `secret_scan.py` - code intelligence utilities.

## Adding A Script
1. Place it in `scripts/` with executable bit (if shell).
2. Include argparse/help text and `[ok]/[warn]/[error]` log helpers.
3. Update this README and `Makefile` with the new target.
4. Add tests where possible (unit for helpers, integration for pipelines).
5. Document any new guardrail, trigger, or doc dependency you introduce.

## Language Policy
Every script must:
- Print messages in the configured repository language (`config/language.yaml`).
- Keep inline comments/docstrings in that language as well.
- Fail fast if it needs localization data that is missing.

## Maintenance
Scripts are maintained by the repository owners. File an Issue for bugs or missing automation.

See also: `Makefile`, `agent.md` (automation section), and `doc_agent/orchestration/agent-triggers.yaml`.

