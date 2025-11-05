# Agent Repo Makefile
# 提供统一的命令接口用于开发和 CI 门禁

.PHONY: help dev_check docgen ai_begin dag_check contract_compat_check \
        update_baselines runtime_config_check migrate_check consistency_check \
        rollback_check tests_scaffold deps_check doc_style_check ai_maintenance

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
	@echo "  make ai_maintenance         - AI 自动维护（检查并修复常见问题）"

# 完整开发检查（CI 门禁）
dev_check: docgen doc_style_check dag_check contract_compat_check runtime_config_check migrate_check consistency_check
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
