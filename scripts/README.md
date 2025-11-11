# Scripts Directory

This directory contains automation scripts used by Makefile targets and CI/CD workflows.

## Script Organization

### Health & Quality Checks
- `health_check.py` - Repository health assessment
- `module_health_check.py` - Module-specific health checks
- `ai_friendliness_check.py` - AI compatibility verification

### Linting & Validation
- `agent_lint.py` - Validate AGENTS.md files
- `config_lint.py` - Configuration validation
- `python_scripts_lint.py` - Python code linting
- `shell_scripts_lint.sh` - Shell script validation
- `makefile_check.py` - Makefile syntax check

### Documentation
- `docgen.py` - Generate documentation headers and indexes
- `doc_style_check.py` - Documentation format validation
- `doc_freshness_check.py` - Check documentation currency
- `doc_route_check.py` - Validate context routes
- `doc_script_sync_check.py` - Ensure doc/script synchronization

### Database & Migration
- `db_lint.py` - Database schema validation
- `migrate_check.py` - Migration pair verification
- `db_env.py` - Database environment management

### Testing
- `test_scaffold.py` - Generate test templates
- `test_status_check.py` - Track test completion
- `test_coverage_check.py` - Coverage reporting

### Contract & Compatibility
- `contract_compat_check.py` - API contract validation
- `type_contract_check.py` - Type contract verification

### Workflow & Automation
- `ai_begin.sh` - Module scaffolding
- `ai_maintenance.py` - Automated maintenance tasks
- `workflow_suggest.py` - Workflow recommendations
- `agent_trigger.py` - Trigger validation

### Analysis & Reporting
- `complexity_check.py` - Code complexity analysis
- `coupling_check.py` - Module coupling detection
- `dag_check.py` - Dependency graph validation
- `consistency_check.py` - Cross-repo consistency
- `dataflow_trace.py` - Data flow analysis
- `dataflow_visualizer.py` - Flow visualization

### Utilities
- `deps_manager.py` - Dependency management
- `registry_gen.py` - Registry generation
- `registry_check.py` - Registry validation
- `secret_scan.py` - Security scanning
- `fixture_loader.py` - Test fixture management

### Documentation Wrapper
- `doc_tools.py` - Unified entry for docs checks (`style`, `freshness`, `sync`, `all`)
  - When to use: run a complete docs check suite from one entrypoint
  - How: `python scripts/doc_tools.py all` or a single task like `style`

### Telemetry & Optimization
- `context_usage_tracker.py` - Log/report/optimize context route usage
- `ai_chain_optimizer.py` - Emit route optimization suggestions based on telemetry
  - When to use: before changing `context_routes` ordering or adding new topics
  - How:
    - Log: `python scripts/context_usage_tracker.py maybe-log --topic "<topic>" --path <path>`
    - Report: `python scripts/context_usage_tracker.py report --limit 10`
    - Suggest: `python scripts/ai_chain_optimizer.py --optimize --limit 10`

## Usage

Most scripts are invoked through Makefile targets:

```bash
make health_check        # Run health assessment
make doc_style_check    # Check documentation
make dev_check          # Full CI gate
```

Direct invocation:
```bash
python scripts/health_check.py --format json
python scripts/module_health_check.py --module common
python scripts/doc_tools.py all
python scripts/context_usage_tracker.py report --limit 10
python scripts/ai_chain_optimizer.py --optimize --limit 10
```

## Script Requirements

All Python scripts should:
1. Include clear docstring with purpose
2. Define when/how to invoke
3. Handle errors gracefully
4. Return appropriate exit codes (0=success, 1=failure)
5. Support `--help` flag where applicable

## Adding New Scripts

1. Place script in appropriate category
2. Add Makefile target if needed
3. Update this README
4. Ensure clear invocation documentation