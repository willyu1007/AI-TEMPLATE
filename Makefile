# Agent Repo Makefile
# 提供统一的命令接口用于开发和 CI 门禁

.PHONY: help dev_check docgen ai_begin dag_check contract_compat_check \
        update_baselines runtime_config_check migrate_check consistency_check \
        rollback_check tests_scaffold deps_check doc_style_check ai_maintenance \
        test_status_check dataflow_check app_structure_check cleanup_tmp \
        generate_openapi generate_frontend_types frontend_types_check \
        agent_lint registry_check doc_route_check registry_gen module_doc_gen \
        type_contract_check doc_script_sync_check validate db_lint

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
	@echo "数据库管理（Phase 5新增）："
	@echo "  make db_lint                - 校验数据库文件（迁移脚本、表YAML）"

# 完整开发检查（CI 门禁）
dev_check: docgen doc_style_check dag_check contract_compat_check deps_check runtime_config_check migrate_check consistency_check frontend_types_check
	@echo ""
	@echo "================================"
	@echo "✅ 全部检查通过"
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
