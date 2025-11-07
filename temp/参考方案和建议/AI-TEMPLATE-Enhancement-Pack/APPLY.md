# APPLY: 将改造包合入现有仓库

## 步骤 1：拷贝文件
- 在你的仓库根目录执行：
```bash
cp -r AI-TEMPLATE-Enhancement-Pack/* .
```

## 步骤 2：安装依赖
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## 步骤 3：审阅并最小改动
1. `agent.md`（根）：确认全局目标、质量门槛与路由列表；
2. `doc/orchestration/registry.yaml`：登记现有模块类型/实例/上下游；
3. `modules/`：为每个模块**复制** `modules/example` 的骨架并填写内容（尤其是 `agent.md` 的 YAML 头部）。

## 步骤 4：运行校验与 CI
```bash
make dev_check        # 本地校验
# 推送后 GitHub Actions 会自动运行 .github/workflows/ci.yml
```

## 步骤 5：落地初始化规范
- `doc/init/PROJECT_INIT_GUIDE.md`
- `doc/modules/MODULE_INIT_GUIDE.md`

> 完成上述步骤后，你就具备“**可解析、可校验、可调度**”的仓库骨架。
