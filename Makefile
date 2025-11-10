# Agent Repo Makefile
# Provides a unified command interface for development and CI gates

.PHONY: help dev_check docgen ai_begin dag_check contract_compat_check \
        update_baselines runtime_config_check migrate_check consistency_check \
        rollback_check tests_scaffold deps_check doc_style_check ai_maintenance \
        test_status_check dataflow_check app_structure_check cleanup_tmp \
        generate_openapi generate_frontend_types frontend_types_check \
        agent_lint registry_check doc_route_check registry_gen module_doc_gen \
        type_contract_check doc_script_sync_check validate db_lint \
        load_fixture cleanup_fixture db_env list_modules list_fixtures \
        dataflow_trace dataflow_visualize dataflow_analyze bottleneck_detect dataflow_report \
        makefile_check python_scripts_lint shell_scripts_lint config_lint \
        trigger_show trigger_check trigger_coverage trigger_matrix \
        health_check health_report health_trend module_health_check ai_friendliness_check \
        health_check_strict health_report_detailed health_analyze_issues health_show_quick_wins \
        doc_freshness_check coupling_check observability_check secret_scan \
        test_coverage code_complexity type_check \
        cleanup_reports cleanup_reports_smart cleanup_all temp_files_check

help:
	@echo "Available targets:"
	@echo "  make dev_check              - Full CI gate"
	@echo "  make docgen                 - Regenerate doc headers/index"
	@echo "  make ai_begin MODULE=<name> - Scaffold a module"
	@echo "  make dag_check              - DAG validation"
	@echo "  make contract_compat_check  - Contract compatibility"
	@echo "  make update_baselines       - Update contract baselines"
	@echo "  make runtime_config_check   - Runtime config lint"
	@echo "  make migrate_check          - Migration pair check"
	@echo "  make consistency_check      - Consistency checks"
	@echo "  make rollback_check         - Rollback validation (PREV_REF)"
	@echo "  make tests_scaffold         - Generate test scaffold (MODULE)"
	@echo "  make deps_check             - Dependency verification"
	@echo "  make doc_style_check        - Doc header/language lint"
	@echo "  make test_status_check      - Manual test tracker"
	@echo "  make dataflow_check         - UX dataflow consistency"
	@echo "  make app_structure_check    - App structure lint"
	@echo "  make ai_maintenance         - Automated maintenance"
	@echo "  make cleanup_tmp            - Remove temporary files"
	@echo "  make cleanup_reports        - Remove old reports (AGE=days)"
	@echo "  make cleanup_reports_smart  - Keep failed + latest 10 reports"
	@echo "  make cleanup_all            - Remove temp + reports"
	@echo "  make temp_files_check       - Ensure temp files removed"
	@echo "  make generate_openapi       - Build OpenAPI from contract.json"
	@echo "  make generate_frontend_types - Build TS types from OpenAPI"
	@echo "  make frontend_types_check    - Verify frontend types"
	@echo "  make agent_lint             - Lint agent.md"
	@echo "  make registry_check         - Validate registry entries"
	@echo "  make doc_route_check        - Validate context routes"
	@echo "  make type_contract_check    - Validate module type contracts"
	@echo "  make doc_script_sync_check  - Doc/script sync check"
	@echo "  make registry_gen           - Draft registry updates"
	@echo "  make module_doc_gen         - Generate module instance docs"
	@echo "  make validate               - Aggregated validation"
	@echo "  make agent_trigger_test     - Guardrail trigger tests"
	@echo "  make agent_trigger FILE=<path> - File trigger check"
	@echo "  make agent_trigger_prompt PROMPT=\"text\" - Prompt trigger check"
	@echo "  make db_lint                - DB lint (migrations + schema)"
	@echo "  make load_fixture MODULE=<name> FIXTURE=<scenario> - Load fixtures"
	@echo "  make cleanup_fixture MODULE=<name>                 - Cleanup fixtures"
	@echo "  make db_env ENV=<env>                              - Switch DB env"
	@echo "  make dataflow_trace          - Dataflow trace"
	@echo "  make dataflow_visualize      - Render dataflow (Mermaid)"
	@echo "  make dataflow_visualize FORMAT=html - Render interactive HTML"
	@echo "  make dataflow_analyze        - Full analysis (trace + viz + bottlenecks)"
	@echo "  make bottleneck_detect       - Detect bottlenecks"
	@echo "  make dataflow_report         - JSON/Markdown/HTML report"
	@echo "  make makefile_check          - Makefile lint"
	@echo "  make python_scripts_lint     - Python script lint"
	@echo "  make shell_scripts_lint      - Shell script lint"
	@echo "  make config_lint             - Config lint"
	@echo "  make trigger_show            - Show triggers"
	@echo "  make trigger_check           - Validate trigger config"
	@echo "  make trigger_coverage        - Trigger coverage report"
	@echo "  make trigger_matrix          - Trigger matrix"
	@echo "  make health_check            - Repository health check"
	@echo "  make health_check_strict     - Strict health gate"
	@echo "  make health_report           - Health report"
	@echo "  make health_report_detailed  - Detailed health report"
	@echo "  make health_trend            - Health trend"
	@echo "  make health_analyze_issues   - Issue aggregation"
	@echo "  make health_show_quick_wins  - Quick wins"
	@echo "  make module_health_check     - Module health check"
	@echo "  make ai_friendliness_check   - AI friendliness check"
	@echo "  make doc_freshness_check     - Doc freshness check"
	@echo "  make coupling_check          - Coupling check"
	@echo "  make observability_check     - Observability coverage"
	@echo "  make secret_scan             - Secret scan"
	@echo "  make test_coverage           - Coverage summary"
	@echo "  make code_complexity         - Complexity report"
	@echo "  make type_check              - Static type check"


# CI ?# Phase 14.322?dev_check: docgen doc_style_check agent_lint registry_check doc_route_check type_contract_check doc_script_sync_check db_lint resources_check dag_check contract_compat_check deps_check runtime_config_check migrate_check consistency_check frontend_types_check doc_freshness_check coupling_check observability_check secret_scan test_coverage temp_files_check
	@echo ""
	@echo "================================"
	@echo "? (22/22)"
	@echo "================================"

#  summary/keywords/deps/hash?docgen:
	@echo " ..."
	@python scripts/docgen.py

# ?ai_begin:
	@if [ -z "$(MODULE)" ]; then \
		echo "??MODULE "; \
		echo ": make ai_begin MODULE=<name>"; \
		exit 1; \
	fi
	@bash scripts/ai_begin.sh $(MODULE)

# DAG //?dag_check:
	@echo " DAG ..."
	@python scripts/dag_check.py

# 
contract_compat_check:
	@echo " ?.."
	@python scripts/contract_compat_check.py

# ?update_baselines:
	@echo " ..."
	@mkdir -p .contracts_baseline
	@find tools -name "contract.json" -exec sh -c 'mkdir -p .contracts_baseline/$$(dirname {}) && cp {} .contracts_baseline/{}' \;
	@echo "? .contracts_baseline/"

# //?runtime_config_check:
	@echo " ?.."
	@python scripts/runtime_config_check.py

# up/down?migrate_check:
	@echo " ?.."
	@python scripts/migrate_check.py

# /
consistency_check:
	@echo " ?.."
	@python scripts/consistency_check.py

# ?Feature Flag/
rollback_check:
	@if [ -z "$(PREV_REF)" ]; then \
		echo "??PREV_REF "; \
		echo ": make rollback_check PREV_REF=<tag|branch>"; \
		exit 1; \
	fi
	@bash scripts/rollback_check.sh $(PREV_REF)

# ?tests_scaffold:
	@if [ -z "$(MODULE)" ]; then \
		echo "??MODULE "; \
		echo ": make tests_scaffold MODULE=<name>"; \
		exit 1; \
	fi
	@python scripts/test_scaffold.py $(MODULE)

# 
quick_check: dag_check consistency_check
	@echo "?"

# ?deps_check:
	@echo " ?.."
	@python scripts/deps_manager.py

# 
doc_style_check:
	@echo " ..."
	@python scripts/doc_style_check.py

# ?test_status_check:
	@echo " ?.."
	@python scripts/test_status_check.py

# UX ?dataflow_check:
	@echo " UX?.."
	@python scripts/dataflow_trace.py

# ?app_structure_check:
	@echo " ..."
	@python scripts/app_structure_check.py

# AI ?ai_maintenance:
	@echo " AI ..."
	@python scripts/ai_maintenance.py

# 
cleanup_tmp:
	@echo " ..."
	@find . -type f -name "*_tmp.*" -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./.venv/*" -not -path "./venv/*" -delete 2>/dev/null || true
	@find . -type d -name "*_tmp" -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./.venv/*" -not -path "./venv/*" -exec rm -rf {} + 2>/dev/null || true
	@if [ -d "tmp" ]; then \
		find tmp -type f -name "*_tmp.*" -delete 2>/dev/null || true; \
	fi
	@echo "?"

#  OpenAPI 3.0  contract.json?generate_openapi:
	@echo "  OpenAPI 3.0 ..."
	@python scripts/generate_openapi.py

#  TypeScript  OpenAPI?generate_frontend_types: generate_openapi
	@echo "  TypeScript ..."
	@python scripts/generate_frontend_types.py

# ?frontend_types_check:
	@echo " ?.."
	@python scripts/frontend_types_check.py

# Phase 1?# agent.md YAML
agent_lint:
	@echo " agent.md..."
	@python scripts/agent_lint.py || echo "  ?

# ?registry_check:
	@echo " ?.."
	@python scripts/registry_check.py || echo "  ?

# 
doc_route_check:
	@echo " ..."
	@python scripts/doc_route_check.py || echo "  ?

# 
type_contract_check:
	@echo " ..."
	@python scripts/type_contract_check.py || echo "  ?

# 
doc_script_sync_check:
	@echo " ..."
	@python scripts/doc_script_sync_check.py || echo "  ?

# ?
validate:
	@bash scripts/validate.sh

# registry.yaml
registry_gen:
	@echo " registry.yaml..."
	@python scripts/registry_gen.py

# 
module_doc_gen:
	@echo " ..."
	@python scripts/module_doc_gen.py

# Phase 5?# YAML?db_lint:
	@echo " ?.."
	@python scripts/db_lint.py || echo "  ?

# Phase 7?# ?list_modules:
	@python scripts/fixture_loader.py --list-modules

# Fixtures
list_fixtures:
	@if [ -z "$(MODULE)" ]; then \
		echo "??MODULE "; \
		echo ": make list_fixtures MODULE=<name>"; \
		exit 1; \
	fi
	@python scripts/fixture_loader.py --module $(MODULE) --list-fixtures

# Fixtures
load_fixture:
	@if [ -z "$(MODULE)" ]; then \
		echo "??MODULE "; \
		echo ": make load_fixture MODULE=<name> FIXTURE=<scenario>"; \
		exit 1; \
	fi
	@if [ -z "$(FIXTURE)" ]; then \
		echo "??FIXTURE "; \
		echo ": make load_fixture MODULE=$(MODULE) FIXTURE=<scenario>"; \
		echo ":  'make list_fixtures MODULE=$(MODULE)' "; \
		exit 1; \
	fi
	@python scripts/fixture_loader.py --module $(MODULE) --fixture $(FIXTURE) $(if $(DRY_RUN),--dry-run)

# 
cleanup_fixture:
	@if [ -z "$(MODULE)" ]; then \
		echo "??MODULE "; \
		echo ": make cleanup_fixture MODULE=<name>"; \
		exit 1; \
	fi
	@python scripts/fixture_loader.py --module $(MODULE) --cleanup $(if $(DRY_RUN),--dry-run)

# ?db_env:
	@if [ -z "$(ENV)" ]; then \
		python scripts/db_env.py; \
	else \
		python scripts/db_env.py --env $(ENV); \
	fi

# MockPhase 8.5+?# Mock
generate_mock:
	@if [ -z "$(MODULE)" ]; then \
		echo "??MODULE "; \
		echo ": make generate_mock MODULE=<name> TABLE=<table> COUNT=<num>"; \
		exit 1; \
	fi
	@if [ -z "$(TABLE)" ]; then \
		echo "??TABLE "; \
		echo ": make generate_mock MODULE=$(MODULE) TABLE=<table> COUNT=<num>"; \
		exit 1; \
	fi
	@if [ -z "$(COUNT)" ]; then \
		echo "??COUNT "; \
		echo ": make generate_mock MODULE=$(MODULE) TABLE=$(TABLE) COUNT=<num>"; \
		exit 1; \
	fi
	@python scripts/mock_generator.py --module $(MODULE) --table $(TABLE) --count $(COUNT) \
		$(if $(LIFECYCLE),--lifecycle $(LIFECYCLE)) \
		$(if $(DRY_RUN),--dry-run) \
		$(if $(SEED),--seed $(SEED))

# Mock
list_mocks:
	@python scripts/mock_lifecycle.py --list $(if $(MODULE),--module $(MODULE))

# Mock
cleanup_mocks:
	@python scripts/mock_lifecycle.py --cleanup $(if $(DRY_RUN),--dry-run)

# Mock
mock_stats:
	@python scripts/mock_lifecycle.py --stats $(if $(MODULE),--module $(MODULE))

# Mock
delete_mock:
	@if [ -z "$(ID)" ]; then \
		echo "??ID "; \
		echo ": make delete_mock ID=<mock_id>"; \
		echo ":  'make list_mocks' ID"; \
		exit 1; \
	fi
	@python scripts/mock_lifecycle.py --delete $(ID) $(if $(DRY_RUN),--dry-run)

# Phase 10?# ?agent_trigger_test:
	@echo " ?.."
	@echo ""
	@echo "1: ?
	@python scripts/agent_trigger.py --prompt ""
	@echo ""
	@echo "2: ?
	@python scripts/agent_trigger.py --prompt ""
	@echo ""
	@echo "??

# ?agent_trigger:
	@if [ -z "$(FILE)" ]; then \
		echo "??FILE "; \
		echo ": make agent_trigger FILE=<path>"; \
		exit 1; \
	fi
	@python scripts/agent_trigger.py --file $(FILE) --verbose

# prompt
agent_trigger_prompt:
	@if [ -z "$(PROMPT)" ]; then \
		echo "??PROMPT "; \
		echo ": make agent_trigger_prompt PROMPT=\"your prompt here\""; \
		exit 1; \
	fi
	@python scripts/agent_trigger.py --prompt "$(PROMPT)" --verbose

# ============================================================
# WorkdocPhase 10.3?# ============================================================

# workdoc
workdoc_create:
	@if [ -z "$(TASK)" ]; then \
		echo "??TASK "; \
		echo ": make workdoc_create TASK=<task-name>"; \
		echo ": make workdoc_create TASK=implement-user-auth"; \
		exit 1; \
	fi
	@bash scripts/workdoc_create.sh $(TASK)

# workdoc
workdoc_archive:
	@if [ -z "$(TASK)" ]; then \
		echo "??TASK "; \
		echo ": make workdoc_archive TASK=<task-name>"; \
		echo ""; \
		echo ":"; \
		@ls -1 ai/workdocs/active/ 2>/dev/null || echo "  (?"; \
		exit 1; \
	fi
	@bash scripts/workdoc_archive.sh $(TASK)

# workdocs
workdoc_list:
	@echo " Active Workdocs:"
	@ls -1 ai/workdocs/active/ 2>/dev/null || echo "  (?"
	@echo ""
	@echo " Archived Workdocs:"
	@ls -1 ai/workdocs/archive/ 2>/dev/null || echo "  (?"

# ============================================================
# GuardrailPhase 10.4?# ============================================================

# Guardrail
guardrail_stats:
	@python scripts/guardrail_stats.py

# 
guardrail_stats_detailed:
	@python scripts/guardrail_stats.py --detailed

# Guardrail
guardrail_coverage:
	@python scripts/guardrail_stats.py --check-coverage

# ============================================================
# ResourcesPhase 10.5?# ============================================================

# resources?resources_check:
	@python scripts/resources_check.py

# ============================================================
# Phase 12?# ============================================================

# 
workflow_list:
	@python scripts/workflow_suggest.py --analyze-context

# 
workflow_suggest:
	@python scripts/workflow_suggest.py --context "$(PROMPT)"

# 
workflow_show:
	@python scripts/workflow_suggest.py --show $(PATTERN)

# checklist?workflow_apply:
	@python scripts/workflow_suggest.py --generate-checklist $(PATTERN)

# ?workflow_validate:
	@echo "?.."
	@for file in ai/workflow-patterns/patterns/*.yaml; do \
		echo "?$$file..."; \
		python -c "import yaml; yaml.safe_load(open('$$file', encoding='utf-8'))" || exit 1; \
	done
	@echo "??

# ============================================================
# Phase 13?# ============================================================

# ?dataflow_trace:
	@echo " ?.."
	@python scripts/dataflow_trace.py

# Mermaid?dataflow_visualize:
	@if [ -z "$(FORMAT)" ]; then \
		FORMAT=mermaid; \
	else \
		FORMAT=$(FORMAT); \
	fi; \
	echo " ? $$FORMAT?.."; \
	python scripts/dataflow_visualizer.py --format $$FORMAT

# ?dataflow_analyze:
	@echo " ?.."
	@echo ""
	@echo "1 ?.."
	@python scripts/dataflow_trace.py
	@echo ""
	@echo "2 Mermaid?.."
	@python scripts/dataflow_visualizer.py --format mermaid --output ai/maintenance_reports/dataflow-$$(date +%Y%m%d).mermaid
	@echo ""
	@echo "3 HTML..."
	@python scripts/dataflow_visualizer.py --format html --output ai/maintenance_reports/dataflow-report-$$(date +%Y%m%d).html
	@echo ""
	@echo "??
	@echo "   - Mermaid: doc/templates/dataflow.mermaid"
	@echo "   - HTML: doc/templates/dataflow-report.html"

# ?bottleneck_detect:
	@echo " ?.."
	@echo " dataflow_trace.py?
	@python scripts/dataflow_trace.py

# JSON+Markdown+HTML?dataflow_report:
	@echo " ?.."
	@mkdir -p ai/dataflow_reports
	@echo "  HTML..."
	@python scripts/dataflow_visualizer.py --format html --output ai/dataflow_reports/report_$$(date +%Y%m%d_%H%M%S).html
	@echo "? ai/dataflow_reports/"
	@ls -lh ai/dataflow_reports/ | tail -5
# Quality Check Tools (Phase 14.0)
makefile_check:
	@echo " Checking Makefile..."
	@python scripts/makefile_check.py

python_scripts_lint:
	@echo " Linting Python scripts..."
	@python scripts/python_scripts_lint.py

shell_scripts_lint:
	@echo " Linting shell scripts..."
	@bash scripts/shell_scripts_lint.sh

config_lint:
	@echo " Linting config files..."
	@python scripts/config_lint.py

# Trigger Management (Phase 14.0)
trigger_show:
	@echo " Displaying trigger configuration..."
	@python scripts/trigger_manager.py show

trigger_check:
	@echo " Validating trigger configuration..."
	@python scripts/trigger_manager.py check

trigger_coverage:
	@echo " Displaying automation coverage..."
	@python scripts/trigger_manager.py coverage

trigger_matrix:
	@echo " Generating trigger matrix..."
	@python scripts/trigger_visualizer.py matrix

# ==============================================================================
# Repository Health Check (Phase 14.2 - Fully Implemented)
# ==============================================================================

health_check:
	@echo " Running repository health check..."
	@python scripts/health_check.py

health_report:
	@echo " Generating health report..."
	@python scripts/health_check.py --format all --output ai/maintenance_reports/health-summary.md

health_trend:
	@echo " Analyzing health trends..."
	@python scripts/health_trend_analyzer.py

test_coverage:
	@echo " Checking test coverage..."
	@python scripts/test_coverage_check.py

test_coverage_json:
	@echo " Generating test coverage report (JSON)..."
	@python scripts/test_coverage_check.py --json

complexity_check:
	@echo " Checking code complexity..."
	@python scripts/complexity_check.py

complexity_check_json:
	@echo " Generating complexity report (JSON)..."
	@python scripts/complexity_check.py --json

# Code refactoring suggestions
refactor_suggest:
	@echo " Generating refactoring suggestions..."
	@python scripts/refactor_suggest.py || true

refactor_plan:
	@echo " Creating refactoring plan..."
	@python scripts/refactor_suggest.py --output-plan

# Report location check
check_report_locations:
	@echo " Checking report file locations..."
	@python scripts/report_location_check.py

fix_report_locations:
	@echo " Fixing misplaced reports..."
	@python scripts/report_location_check.py --fix

# Phase 14.2+ Enhanced Health Check Commands
health_check_strict:
	@echo " Running strict mode health check..."
	@python scripts/health_check.py --strict --output ai/maintenance_reports/health-check-strict-$$(date +%Y%m%d).md

health_report_detailed:
	@echo " Generating detailed health report (all formats)..."
	@python scripts/health_check.py --detailed --format all --output ai/maintenance_reports/health-report-detailed-$$(date +%Y%m%d).md

health_analyze_issues:
	@echo " Analyzing issue patterns and root causes..."
	@python scripts/issue_aggregator.py --input ai/maintenance_reports/health-report-latest.json

health_show_quick_wins:
	@echo " Identifying quick win improvements..."
	@python scripts/issue_aggregator.py --quick-wins --max 10

module_health_check:
	@echo " Checking module health..."
	@python scripts/module_health_check.py

ai_friendliness_check:
	@echo " Checking AI friendliness..."
	@python scripts/ai_friendliness_check.py

doc_freshness_check:
	@echo " Checking documentation freshness..."
	@python scripts/doc_freshness_check.py

coupling_check:
	@echo " Checking module coupling..."
	@python scripts/coupling_check.py

observability_check:
	@echo " Checking observability coverage..."
	@python scripts/observability_check.py

secret_scan:
	@echo " Scanning for secrets..."
	@python scripts/secret_scan.py

# ==============================================================================
# Code Quality Tools (Phase 14.3)
# ==============================================================================

# test_coverage command moved to line 598 with the new test_coverage_check.py script

code_complexity:
	@echo " Analyzing code complexity..."
	@if command -v radon > /dev/null 2>&1; then \
		echo ""; \
		echo " Cyclomatic Complexity (modules/):"; \
		radon cc modules/ -a -s || true; \
		echo ""; \
		echo " Maintainability Index (modules/):"; \
		radon mi modules/ -s || true; \
		echo ""; \
		echo " Raw Metrics (modules/):"; \
		radon raw modules/ -s || true; \
	else \
		echo "  radon not installed. Install with: pip install radon"; \
		exit 1; \
	fi

type_check:
	@echo " Running static type check..."
	@if command -v mypy > /dev/null 2>&1; then \
		mypy modules/ scripts/ --ignore-missing-imports --no-strict-optional || true; \
		echo ""; \
		echo "?Type check completed"; \
	else \
		echo "  mypy not installed. Install with: pip install mypy"; \
		exit 1; \
	fi

# ==============================================================================
# Temporary Files & Reports Management (Phase 14.3+)
# ==============================================================================

# Check for uncleaned temporary files (CI gate)
temp_files_check:
	@echo " ?.."
	@FOUND=0; \
	if find . -type f -name "*_tmp.*" -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./.venv/*" -not -path "./venv/*" -not -path "./tmp/*" 2>/dev/null | grep -q .; then \
		echo ""; \
		echo "??; \
		find . -type f -name "*_tmp.*" -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./.venv/*" -not -path "./venv/*" -not -path "./tmp/*" 2>/dev/null; \
		echo ""; \
		echo "? make cleanup_tmp"; \
		FOUND=1; \
	fi; \
	if [ $$FOUND -eq 1 ]; then \
		exit 1; \
	fi
	@echo "??

# Clean old report files (default: 30 days)
cleanup_reports:
	@echo " ?.."
	@AGE=$${AGE:-30}; \
	echo " $$AGE ?.."; \
	DELETED=0; \
	if [ -d "ai/maintenance_reports" ]; then \
		for file in $$(find ai/maintenance_reports -name "*.json" -o -name "*.html" -type f -mtime +$$AGE 2>/dev/null); do \
			if ! grep -q "failed" "$$file" 2>/dev/null; then \
				echo "  : $$file"; \
				rm "$$file"; \
				DELETED=$$((DELETED + 1)); \
			fi; \
		done; \
	fi; \
	if [ -d "ai/dataflow_reports" ]; then \
		for file in $$(find ai/dataflow_reports -name "*.html" -type f -mtime +$$AGE 2>/dev/null); do \
			echo "  : $$file"; \
			rm "$$file"; \
			DELETED=$$((DELETED + 1)); \
		done; \
	fi; \
	echo "??$$DELETED "

# Smart cleanup: keep failed reports and last N reports
cleanup_reports_smart:
	@echo " ..."
	@KEEP=$${KEEP:-10}; \
	echo "?$$KEEP ?.."; \
	DELETED=0; \
	if [ -d "ai/maintenance_reports" ]; then \
		cd ai/maintenance_reports && \
		for pattern in "health-report-*.json" "health-summary-*.md"; do \
			FILES=$$(ls -t $$pattern 2>/dev/null | tail -n +$$((KEEP + 1))); \
			for file in $$FILES; do \
				if [ -f "$$file" ] && ! grep -q "failed" "$$file" 2>/dev/null; then \
					echo "  : ai/maintenance_reports/$$file"; \
					rm "$$file"; \
					DELETED=$$((DELETED + 1)); \
				fi; \
			done; \
		done; \
	fi; \
	echo "??$$DELETED ?$$KEEP ?

# Clean all temporary files and old reports
cleanup_all: cleanup_tmp cleanup_reports_smart
	@echo ""
	@echo "================================"
	@echo "?"
	@echo "================================"
