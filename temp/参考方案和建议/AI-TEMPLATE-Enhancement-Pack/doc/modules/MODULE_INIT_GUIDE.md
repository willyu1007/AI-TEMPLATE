# MODULE_INIT_GUIDE

## 1. 目录生成
- `modules/<entity>/` 下创建：
  - `agent.md`（按模板）
  - `README.md`
  - `plan.md`
  - `doc/`：`CHANGELOG.md / CONTRACT.md / PROGRESS.md / BUGS.md / RUNBOOK.md / TEST_PLAN.md`

## 2. 需求收集与冻结
- 若存在需求文档，放入 `doc/`
- 沟通迭代直至冻结，再继续初始化

## 3. 编排注册
- 在 `doc/orchestration/registry.yaml` 登记：
  - `type / instance / path / level / upstream / downstream / status / version`

## 4. 校验与门禁
- 运行 `make dev_check`；若失败，按提示修复

## 5. 开发起步
- 先提交 `plan.md` 并获批，才允许写代码
