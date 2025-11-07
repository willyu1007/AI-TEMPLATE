SHELL := /bin/bash

.PHONY: init\:project init\:module dev_check

init\:project:
	@echo "[init] project" 
	@echo "请参考 doc/init/PROJECT_INIT_GUIDE.md 并更新根 agent.md / registry.yaml"

init\:module:
	@echo "[init] module" 
	@echo "请参考 doc/modules/MODULE_INIT_GUIDE.md 并在 modules/<entity>/ 下生成实例骨架"

dev_check:
	python scripts/agent_lint.py
	python scripts/registry_check.py
	python scripts/doc_route_check.py
