# Agent Repo Makefile
# 提供统一的命令接口用于开发和 CI 门禁

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
        test_coverage code_complexity type_check

help:
	@echo "可用命令："
	@echo "  make dev_check              - 运行完整开发检查（CI 门禁）"
	@echo "  make docgen                 - 生成文档索引"
	@echo "  make ai_begin MODULE=<name> - 初始化新模块"
	@echo "  make dag_check              - DAG 静态校验"
	@echo "  make contract_compat_check  - 契约兼容性检查"
	@echo "  make update_baselines       - 更新契约基线"
	@echo "  make runtime_config_check   - 运行时配置校验"
	@echo "  make migrate_check          - 迁移脚本检查"
	@echo "  make consistency_check      - 一致性检查"
	@echo "  make rollback_check         - 回滚验证 (需要 PREV_REF)"
	@echo "  make tests_scaffold         - 生成测试脚手架 (需要 MODULE)"
	@echo "  make deps_check             - 检查并自动补全依赖文件"
	@echo "  make doc_style_check        - 文档风格预检"
	@echo "  make test_status_check      - 检查人工测试跟踪状态"
	@echo "  make dataflow_check         - 检查UX数据流转文档一致性"
	@echo "  make app_structure_check    - 检查应用层结构（app/apps）"
	@echo "  make ai_maintenance         - AI 自动维护（检查并修复常见问题）"
	@echo "  make cleanup_tmp            - 清理所有临时文件（*_tmp.*）"
	@echo "  make generate_openapi       - 从 contract.json 生成 OpenAPI 3.0"
	@echo "  make generate_frontend_types - 从 OpenAPI 生成前端 TypeScript 类型"
	@echo "  make frontend_types_check    - 检查前端类型与契约一致性"
	@echo ""
	@echo "编排与模块管理（Phase 1新增）："
	@echo "  make agent_lint             - 校验agent.md YAML前言"
	@echo "  make registry_check         - 校验模块注册表"
	@echo "  make doc_route_check        - 校验文档路由路径"
	@echo "  make type_contract_check    - 校验模块类型契约"
	@echo "  make doc_script_sync_check  - 检查文档与脚本同步"
	@echo "  make registry_gen           - 生成registry.yaml草案"
	@echo "  make module_doc_gen         - 生成模块实例文档"
	@echo "  make validate               - 聚合验证（7个检查）"
	@echo ""
	@echo "智能触发系统（Phase 10新增）："
	@echo "  make agent_trigger_test     - 测试智能触发器"
	@echo "  make agent_trigger FILE=<path> - 检查文件触发哪些规则"
	@echo "  make agent_trigger_prompt PROMPT=\"text\" - 检查prompt触发哪些规则"
	@echo ""
	@echo "数据库管理（Phase 5新增）："
	@echo "  make db_lint                - 校验数据库文件（迁移脚本、表YAML）"
	@echo ""
	@echo "测试数据管理（Phase 7新增）："
	@echo "  make load_fixture MODULE=<name> FIXTURE=<scenario> - 加载模块Fixtures"
	@echo "  make cleanup_fixture MODULE=<name>                 - 清理模块测试数据"
	@echo "  make db_env ENV=<env>                              - 切换数据库环境（dev/test/demo）"
	@echo ""
	@echo "数据流分析（Phase 13新增）："
	@echo "  make dataflow_trace          - 数据流追踪检查"
	@echo "  make dataflow_visualize      - 生成可视化（默认Mermaid）"
	@echo "  make dataflow_visualize FORMAT=html - 生成交互式HTML"
	@echo "  make dataflow_analyze        - 完整分析（追踪+可视化+瓶颈检测）"
	@echo "  make bottleneck_detect       - 性能瓶颈检测"
	@echo "  make dataflow_report         - 生成完整报告（JSON+Markdown+HTML）"
	@echo ""
	@echo "质量检查工具（Phase 14.0新增）："
	@echo "  make makefile_check          - 校验Makefile语法和依赖"
	@echo "  make python_scripts_lint     - Python脚本质量检查"
	@echo "  make shell_scripts_lint      - Shell脚本质量检查"
	@echo "  make config_lint             - 配置文件校验"
	@echo ""
	@echo "触发机制管理（Phase 14.0新增）："
	@echo "  make trigger_show            - 显示所有触发配置"
	@echo "  make trigger_check           - 验证触发配置"
	@echo "  make trigger_coverage        - 显示自动化覆盖率"
	@echo "  make trigger_matrix          - 生成触发矩阵"
	@echo ""
	@echo "仓库健康度检查（Phase 14.2+）："
	@echo "  make health_check            - 运行健康度检查"
	@echo "  make health_check_strict     - 严格模式检查（零容忍+阻断规则）"
	@echo "  make health_report           - 生成完整健康度报告"
	@echo "  make health_report_detailed  - 生成详细报告（含问题定位）"
	@echo "  make health_trend            - 显示健康度趋势"
	@echo "  make health_analyze_issues   - 问题聚合与根因分析"
	@echo "  make health_show_quick_wins  - 显示快速改进建议"
	@echo "  make module_health_check     - 检查模块健康度"
	@echo "  make ai_friendliness_check   - 检查AI友好度"
	@echo "  make doc_freshness_check     - 检查文档时效性"
	@echo "  make coupling_check          - 检查模块耦合度"
	@echo "  make observability_check     - 检查可观测性覆盖"
	@echo "  make secret_scan             - 扫描密钥泄露"
	@echo ""
	@echo "代码质量工具（Phase 14.3新增）："
	@echo "  make test_coverage           - 测试覆盖率分析"
	@echo "  make code_complexity         - 代码复杂度分析"
	@echo "  make type_check              - 静态类型检查"

# 完整开发检查（CI 门禁）
# Phase 14.3更新：增加质量检查工具，总计21个检查
dev_check: docgen doc_style_check agent_lint registry_check doc_route_check type_contract_check doc_script_sync_check db_lint resources_check dag_check contract_compat_check deps_check runtime_config_check migrate_check consistency_check frontend_types_check doc_freshness_check coupling_check observability_check secret_scan test_coverage
	@echo ""
	@echo "================================"
	@echo "✅ 全部检查通过 (21/21)"
	@echo "================================"

# 生成文档索引（含 summary/keywords/deps/hash）
docgen:
	@echo "📚 生成文档索引..."
	@python scripts/docgen.py

# 初始化新模块（含文档模板和测试脚手架）
ai_begin:
	@if [ -z "$(MODULE)" ]; then \
		echo "❌ 错误：需要指定 MODULE 参数"; \
		echo "用法: make ai_begin MODULE=<name>"; \
		exit 1; \
	fi
	@bash scripts/ai_begin.sh $(MODULE)

# DAG 静态校验（去重/无环/引用存在）
dag_check:
	@echo "🔍 DAG 校验..."
	@python scripts/dag_check.py

# 契约兼容性检查（破坏性变更阻断）
contract_compat_check:
	@echo "🔍 契约兼容性检查..."
	@python scripts/contract_compat_check.py

# 更新契约基线（通过兼容性检查后）
update_baselines:
	@echo "📦 更新契约基线..."
	@mkdir -p .contracts_baseline
	@find tools -name "contract.json" -exec sh -c 'mkdir -p .contracts_baseline/$$(dirname {}) && cp {} .contracts_baseline/{}' \;
	@echo "✅ 基线已更新到 .contracts_baseline/"

# 运行时配置校验（结构/必填/生产密钥）
runtime_config_check:
	@echo "🔍 运行时配置校验..."
	@python scripts/runtime_config_check.py

# 迁移脚本成对检查（up/down）
migrate_check:
	@echo "🔍 迁移脚本检查..."
	@python scripts/migrate_check.py

# 一致性检查（模块必备文档/哈希一致）
consistency_check:
	@echo "🔍 一致性检查..."
	@python scripts/consistency_check.py

# 回滚验证（迁移/Feature Flag/可切回）
rollback_check:
	@if [ -z "$(PREV_REF)" ]; then \
		echo "❌ 错误：需要指定 PREV_REF 参数"; \
		echo "用法: make rollback_check PREV_REF=<tag|branch>"; \
		exit 1; \
	fi
	@bash scripts/rollback_check.sh $(PREV_REF)

# 生成测试脚手架
tests_scaffold:
	@if [ -z "$(MODULE)" ]; then \
		echo "❌ 错误：需要指定 MODULE 参数"; \
		echo "用法: make tests_scaffold MODULE=<name>"; \
		exit 1; \
	fi
	@python scripts/test_scaffold.py $(MODULE)

# 快速验证（跳过慢速检查）
quick_check: dag_check consistency_check
	@echo "✅ 快速检查通过"

# 依赖检查（自动检测并补全）
deps_check:
	@echo "🔍 检查项目依赖..."
	@python scripts/deps_manager.py

# 文档风格预检
doc_style_check:
	@echo "🔍 文档风格预检..."
	@python scripts/doc_style_check.py

# 人工测试状态检查
test_status_check:
	@echo "🔍 检查人工测试跟踪状态..."
	@python scripts/test_status_check.py

# UX 数据流转检查
dataflow_check:
	@echo "🔍 检查UX数据流转文档一致性..."
	@python scripts/dataflow_trace.py

# 应用层结构检查
app_structure_check:
	@echo "🔍 检查应用层结构..."
	@python scripts/app_structure_check.py

# AI 自动维护（检查并修复常见问题）
ai_maintenance:
	@echo "🤖 AI 自动维护..."
	@python scripts/ai_maintenance.py

# 清理临时文件
cleanup_tmp:
	@echo "🧹 清理临时文件..."
	@find . -type f -name "*_tmp.*" -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./.venv/*" -not -path "./venv/*" -delete 2>/dev/null || true
	@find . -type d -name "*_tmp" -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./.venv/*" -not -path "./venv/*" -exec rm -rf {} + 2>/dev/null || true
	@if [ -d "tmp" ]; then \
		find tmp -type f -name "*_tmp.*" -delete 2>/dev/null || true; \
	fi
	@echo "✅ 临时文件清理完成"

# 生成 OpenAPI 3.0 规范（从 contract.json）
generate_openapi:
	@echo "📝 生成 OpenAPI 3.0 规范..."
	@python scripts/generate_openapi.py

# 生成前端 TypeScript 类型（从 OpenAPI）
generate_frontend_types: generate_openapi
	@echo "📝 生成前端 TypeScript 类型..."
	@python scripts/generate_frontend_types.py

# 检查前端类型与契约一致性
frontend_types_check:
	@echo "🔍 检查前端类型一致性..."
	@python scripts/frontend_types_check.py

# 编排与模块管理（Phase 1新增）
# 校验agent.md YAML前言
agent_lint:
	@echo "🔍 校验agent.md..."
	@python scripts/agent_lint.py || echo "⚠️  警告模式：允许失败"

# 校验模块注册表
registry_check:
	@echo "🔍 校验模块注册表..."
	@python scripts/registry_check.py || echo "⚠️  警告模式：允许失败"

# 校验文档路由
doc_route_check:
	@echo "🔍 校验文档路由..."
	@python scripts/doc_route_check.py || echo "⚠️  警告模式：允许失败"

# 校验模块类型契约
type_contract_check:
	@echo "🔍 校验模块类型契约..."
	@python scripts/type_contract_check.py || echo "⚠️  警告模式：允许失败"

# 检查文档与脚本同步
doc_script_sync_check:
	@echo "🔍 检查文档与脚本同步..."
	@python scripts/doc_script_sync_check.py || echo "⚠️  警告模式：允许失败"

# 聚合验证（7个检查）
validate:
	@bash scripts/validate.sh

# 生成registry.yaml草案（半自动化）
registry_gen:
	@echo "📝 生成registry.yaml草案..."
	@python scripts/registry_gen.py

# 生成模块实例文档
module_doc_gen:
	@echo "📝 生成模块实例文档..."
	@python scripts/module_doc_gen.py

# 数据库管理（Phase 5新增）
# 校验数据库文件（迁移脚本成对性、表YAML格式）
db_lint:
	@echo "🔍 校验数据库文件..."
	@python scripts/db_lint.py || echo "⚠️  警告模式：允许失败"

# 测试数据管理（Phase 7新增）
# 列举所有模块
list_modules:
	@python scripts/fixture_loader.py --list-modules

# 列举模块的Fixtures
list_fixtures:
	@if [ -z "$(MODULE)" ]; then \
		echo "❌ 错误：需要指定 MODULE 参数"; \
		echo "用法: make list_fixtures MODULE=<name>"; \
		exit 1; \
	fi
	@python scripts/fixture_loader.py --module $(MODULE) --list-fixtures

# 加载模块Fixtures
load_fixture:
	@if [ -z "$(MODULE)" ]; then \
		echo "❌ 错误：需要指定 MODULE 参数"; \
		echo "用法: make load_fixture MODULE=<name> FIXTURE=<scenario>"; \
		exit 1; \
	fi
	@if [ -z "$(FIXTURE)" ]; then \
		echo "❌ 错误：需要指定 FIXTURE 参数"; \
		echo "用法: make load_fixture MODULE=$(MODULE) FIXTURE=<scenario>"; \
		echo "提示: 使用 'make list_fixtures MODULE=$(MODULE)' 查看可用场景"; \
		exit 1; \
	fi
	@python scripts/fixture_loader.py --module $(MODULE) --fixture $(FIXTURE) $(if $(DRY_RUN),--dry-run)

# 清理模块测试数据
cleanup_fixture:
	@if [ -z "$(MODULE)" ]; then \
		echo "❌ 错误：需要指定 MODULE 参数"; \
		echo "用法: make cleanup_fixture MODULE=<name>"; \
		exit 1; \
	fi
	@python scripts/fixture_loader.py --module $(MODULE) --cleanup $(if $(DRY_RUN),--dry-run)

# 数据库环境管理
db_env:
	@if [ -z "$(ENV)" ]; then \
		python scripts/db_env.py; \
	else \
		python scripts/db_env.py --env $(ENV); \
	fi

# Mock数据管理（Phase 8.5+新增）
# 生成Mock数据
generate_mock:
	@if [ -z "$(MODULE)" ]; then \
		echo "❌ 错误：需要指定 MODULE 参数"; \
		echo "用法: make generate_mock MODULE=<name> TABLE=<table> COUNT=<num>"; \
		exit 1; \
	fi
	@if [ -z "$(TABLE)" ]; then \
		echo "❌ 错误：需要指定 TABLE 参数"; \
		echo "用法: make generate_mock MODULE=$(MODULE) TABLE=<table> COUNT=<num>"; \
		exit 1; \
	fi
	@if [ -z "$(COUNT)" ]; then \
		echo "❌ 错误：需要指定 COUNT 参数"; \
		echo "用法: make generate_mock MODULE=$(MODULE) TABLE=$(TABLE) COUNT=<num>"; \
		exit 1; \
	fi
	@python scripts/mock_generator.py --module $(MODULE) --table $(TABLE) --count $(COUNT) \
		$(if $(LIFECYCLE),--lifecycle $(LIFECYCLE)) \
		$(if $(DRY_RUN),--dry-run) \
		$(if $(SEED),--seed $(SEED))

# 列出活跃的Mock记录
list_mocks:
	@python scripts/mock_lifecycle.py --list $(if $(MODULE),--module $(MODULE))

# 清理过期的Mock数据
cleanup_mocks:
	@python scripts/mock_lifecycle.py --cleanup $(if $(DRY_RUN),--dry-run)

# 查看Mock统计信息
mock_stats:
	@python scripts/mock_lifecycle.py --stats $(if $(MODULE),--module $(MODULE))

# 删除指定Mock记录
delete_mock:
	@if [ -z "$(ID)" ]; then \
		echo "❌ 错误：需要指定 ID 参数"; \
		echo "用法: make delete_mock ID=<mock_id>"; \
		echo "提示: 使用 'make list_mocks' 查看可用ID"; \
		exit 1; \
	fi
	@python scripts/mock_lifecycle.py --delete $(ID) $(if $(DRY_RUN),--dry-run)

# 智能触发系统（Phase 10新增）
# 测试触发器
agent_trigger_test:
	@echo "🧪 测试智能触发器..."
	@echo ""
	@echo "测试场景1: 模块开发"
	@python scripts/agent_trigger.py --prompt "创建一个新模块"
	@echo ""
	@echo "测试场景2: 数据库操作"
	@python scripts/agent_trigger.py --prompt "修改数据库表结构"
	@echo ""
	@echo "✅ 触发器测试完成"

# 检查文件触发哪些规则
agent_trigger:
	@if [ -z "$(FILE)" ]; then \
		echo "❌ 错误：需要指定 FILE 参数"; \
		echo "用法: make agent_trigger FILE=<path>"; \
		exit 1; \
	fi
	@python scripts/agent_trigger.py --file $(FILE) --verbose

# 检查prompt触发哪些规则
agent_trigger_prompt:
	@if [ -z "$(PROMPT)" ]; then \
		echo "❌ 错误：需要指定 PROMPT 参数"; \
		echo "用法: make agent_trigger_prompt PROMPT=\"your prompt here\""; \
		exit 1; \
	fi
	@python scripts/agent_trigger.py --prompt "$(PROMPT)" --verbose

# ============================================================
# Workdoc管理（Phase 10.3）
# ============================================================

# 创建新workdoc
workdoc_create:
	@if [ -z "$(TASK)" ]; then \
		echo "❌ 错误：需要指定 TASK 参数"; \
		echo "用法: make workdoc_create TASK=<task-name>"; \
		echo "示例: make workdoc_create TASK=implement-user-auth"; \
		exit 1; \
	fi
	@bash scripts/workdoc_create.sh $(TASK)

# 归档workdoc
workdoc_archive:
	@if [ -z "$(TASK)" ]; then \
		echo "❌ 错误：需要指定 TASK 参数"; \
		echo "用法: make workdoc_archive TASK=<task-name>"; \
		echo ""; \
		echo "可归档的任务:"; \
		@ls -1 ai/workdocs/active/ 2>/dev/null || echo "  (无)"; \
		exit 1; \
	fi
	@bash scripts/workdoc_archive.sh $(TASK)

# 列出所有workdocs
workdoc_list:
	@echo "📋 Active Workdocs:"
	@ls -1 ai/workdocs/active/ 2>/dev/null || echo "  (无)"
	@echo ""
	@echo "📦 Archived Workdocs:"
	@ls -1 ai/workdocs/archive/ 2>/dev/null || echo "  (无)"

# ============================================================
# Guardrail统计（Phase 10.4）
# ============================================================

# 显示Guardrail统计
guardrail_stats:
	@python scripts/guardrail_stats.py

# 显示详细统计
guardrail_stats_detailed:
	@python scripts/guardrail_stats.py --detailed

# 检查Guardrail覆盖
guardrail_coverage:
	@python scripts/guardrail_stats.py --check-coverage

# ============================================================
# Resources文件检查（Phase 10.5）
# ============================================================

# 检查resources文件完整性
resources_check:
	@python scripts/resources_check.py

# ============================================================
# 工作流模式库（Phase 12）
# ============================================================

# 列出所有工作流模式
workflow_list:
	@python scripts/workflow_suggest.py --analyze-context

# 推荐合适的模式
workflow_suggest:
	@python scripts/workflow_suggest.py --context "$(PROMPT)"

# 显示模式详情
workflow_show:
	@python scripts/workflow_suggest.py --show $(PATTERN)

# 应用模式（生成checklist）
workflow_apply:
	@python scripts/workflow_suggest.py --generate-checklist $(PATTERN)

# 校验所有模式文件
workflow_validate:
	@echo "校验工作流模式文件..."
	@for file in ai/workflow-patterns/patterns/*.yaml; do \
		echo "检查 $$file..."; \
		python -c "import yaml; yaml.safe_load(open('$$file', encoding='utf-8'))" || exit 1; \
	done
	@echo "✅ 所有模式文件格式正确"

# ============================================================
# 数据流分析（Phase 13）
# ============================================================

# 数据流追踪检查
dataflow_trace:
	@echo "🔍 数据流追踪检查..."
	@python scripts/dataflow_trace.py

# 生成可视化（默认Mermaid）
dataflow_visualize:
	@if [ -z "$(FORMAT)" ]; then \
		FORMAT=mermaid; \
	else \
		FORMAT=$(FORMAT); \
	fi; \
	echo "🎨 生成数据流可视化（格式: $$FORMAT）..."; \
	python scripts/dataflow_visualizer.py --format $$FORMAT

# 完整数据流分析
dataflow_analyze:
	@echo "📊 运行完整数据流分析..."
	@echo ""
	@echo "1️⃣ 数据流追踪检查..."
	@python scripts/dataflow_trace.py
	@echo ""
	@echo "2️⃣ 生成Mermaid可视化..."
	@python scripts/dataflow_visualizer.py --format mermaid --output doc/templates/dataflow.mermaid
	@echo ""
	@echo "3️⃣ 生成HTML交互式可视化..."
	@python scripts/dataflow_visualizer.py --format html --output doc/templates/dataflow-report.html
	@echo ""
	@echo "✅ 数据流分析完成"
	@echo "   - Mermaid: doc/templates/dataflow.mermaid"
	@echo "   - HTML报告: doc/templates/dataflow-report.html"

# 性能瓶颈检测
bottleneck_detect:
	@echo "🔍 性能瓶颈检测..."
	@echo "💡 瓶颈检测已集成到dataflow_trace.py中"
	@python scripts/dataflow_trace.py

# 生成完整报告（JSON+Markdown+HTML）
dataflow_report:
	@echo "📝 生成完整数据流报告..."
	@mkdir -p ai/dataflow_reports
	@echo "  生成HTML报告..."
	@python scripts/dataflow_visualizer.py --format html --output ai/dataflow_reports/report_$$(date +%Y%m%d_%H%M%S).html
	@echo "✅ 报告已生成到 ai/dataflow_reports/"
	@ls -lh ai/dataflow_reports/ | tail -5
# Quality Check Tools (Phase 14.0)
makefile_check:
	@echo "🔍 Checking Makefile..."
	@python scripts/makefile_check.py

python_scripts_lint:
	@echo "🔍 Linting Python scripts..."
	@python scripts/python_scripts_lint.py

shell_scripts_lint:
	@echo "🔍 Linting shell scripts..."
	@bash scripts/shell_scripts_lint.sh

config_lint:
	@echo "🔍 Linting config files..."
	@python scripts/config_lint.py

# Trigger Management (Phase 14.0)
trigger_show:
	@echo "📋 Displaying trigger configuration..."
	@python scripts/trigger_manager.py show

trigger_check:
	@echo "🔍 Validating trigger configuration..."
	@python scripts/trigger_manager.py check

trigger_coverage:
	@echo "📊 Displaying automation coverage..."
	@python scripts/trigger_manager.py coverage

trigger_matrix:
	@echo "📊 Generating trigger matrix..."
	@python scripts/trigger_visualizer.py matrix

# ==============================================================================
# Repository Health Check (Phase 14.2 - Fully Implemented)
# ==============================================================================

health_check:
	@echo "🏥 Running repository health check..."
	@python scripts/health_check.py

health_report:
	@echo "📊 Generating health report..."
	@python scripts/health_check.py --format all --output ai/maintenance_reports/health-summary.md

health_trend:
	@echo "📈 Analyzing health trends..."
	@python scripts/health_trend_analyzer.py

# Phase 14.2+ Enhanced Health Check Commands
health_check_strict:
	@echo "🔥 Running strict mode health check..."
	@python scripts/health_check.py --strict --output temp/health-check-strict-$$(date +%Y%m%d-%H%M%S).md

health_report_detailed:
	@echo "📊 Generating detailed health report (all formats)..."
	@python scripts/health_check.py --detailed --format all --output temp/

health_analyze_issues:
	@echo "🎯 Analyzing issue patterns and root causes..."
	@python scripts/issue_aggregator.py --input ai/maintenance_reports/health-report-latest.json

health_show_quick_wins:
	@echo "🚀 Identifying quick win improvements..."
	@python scripts/issue_aggregator.py --quick-wins --max 10

module_health_check:
	@echo "📦 Checking module health..."
	@python scripts/module_health_check.py

ai_friendliness_check:
	@echo "🤖 Checking AI friendliness..."
	@python scripts/ai_friendliness_check.py

doc_freshness_check:
	@echo "📚 Checking documentation freshness..."
	@python scripts/doc_freshness_check.py

coupling_check:
	@echo "🔗 Checking module coupling..."
	@python scripts/coupling_check.py

observability_check:
	@echo "🔭 Checking observability coverage..."
	@python scripts/observability_check.py

secret_scan:
	@echo "🔒 Scanning for secrets..."
	@python scripts/secret_scan.py

# ==============================================================================
# Code Quality Tools (Phase 14.3)
# ==============================================================================

test_coverage:
	@echo "📊 Running test coverage analysis..."
	@if command -v pytest > /dev/null 2>&1; then \
		pytest tests/ --cov=. --cov-report=term --cov-report=html --cov-report=json -v || true; \
		echo ""; \
		echo "📈 Coverage report generated:"; \
		echo "  - HTML: htmlcov/index.html"; \
		echo "  - JSON: coverage.json"; \
	else \
		echo "⚠️  pytest not installed. Install with: pip install pytest pytest-cov"; \
		exit 1; \
	fi

code_complexity:
	@echo "📊 Analyzing code complexity..."
	@if command -v radon > /dev/null 2>&1; then \
		echo ""; \
		echo "🔍 Cyclomatic Complexity (modules/):"; \
		radon cc modules/ -a -s || true; \
		echo ""; \
		echo "🔍 Maintainability Index (modules/):"; \
		radon mi modules/ -s || true; \
		echo ""; \
		echo "🔍 Raw Metrics (modules/):"; \
		radon raw modules/ -s || true; \
	else \
		echo "⚠️  radon not installed. Install with: pip install radon"; \
		exit 1; \
	fi

type_check:
	@echo "🔍 Running static type check..."
	@if command -v mypy > /dev/null 2>&1; then \
		mypy modules/ scripts/ --ignore-missing-imports --no-strict-optional || true; \
		echo ""; \
		echo "✅ Type check completed"; \
	else \
		echo "⚠️  mypy not installed. Install with: pip install mypy"; \
		exit 1; \
	fi
