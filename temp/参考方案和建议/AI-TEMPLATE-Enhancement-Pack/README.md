# AI-TEMPLATE Enhancement Pack (v1.0.0)

> 一套 **可直接落库** 的改造包：统一 `agent.md` Schema、模块级文档骨架、编排注册表、校验脚本与 CI。
> 目标：**AI 友好 + 模块化 + 自动化**，并适配智能体编排的可解析路由与门禁。

## 内容物（Overview）
- `agent.md`（根级轻量版；YAML Front Matter + Markdown）
- `schemas/agent.schema.yaml`（`agent.md` 统一 Schema）
- `doc/`（策略、路由、初始化规范、模块模板）
- `modules/example/`（模块实例样例：`agent.md / README.md / plan.md / doc/`）
- `scripts/`（`agent_lint.py / registry_check.py / doc_route_check.py`）
- `.github/workflows/ci.yml`（CI 门禁）
- `Makefile`（开发门禁与初始化命令）
- `requirements.txt`

## 快速试用（5 分钟）
```bash
# 复制到你的仓库根目录
cp -r AI-TEMPLATE-Enhancement-Pack/* <your-repo>/

cd <your-repo>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 运行校验
make dev_check
```

## 适用场景
- 你已有 Repo 模板（或项目），需要：
  1) **根 agent.md 轻量化**；
  2) 为 **每个模块实例**补齐 `agent.md/README/doc/`；
  3) 建立 **编排注册表** 与 **自动化校验**。
