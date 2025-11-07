# DoR / DoD（Definition of Ready / Definition of Done）

## 目标
明确任务开始和完成的标准，确保交付质量。

## 适用场景
- 所有开发任务
- 功能迭代
- Bug 修复

## Definition of Ready（就绪定义）

任务在开始实施前必须满足以下条件：

### 1. 计划明确
- [ ] `modules/<name>/plan.md` 已更新
- [ ] 目标和范围清晰定义
- [ ] 接口/DB 影响已分析
- [ ] 测试清单已列出

### 2. 契约齐备
- [ ] 涉及的接口有 `contract.json` 或 `CONTRACT.md`
- [ ] 契约版本明确
- [ ] 破坏性变更已标识

### 3. 验证命令可执行
- [ ] 提供了具体的验证命令
- [ ] 验证命令已测试可用
- [ ] 回滚计划已制定

### 4. 依赖就绪
- [ ] 依赖的模块/服务已就绪
- [ ] 环境配置已准备
- [ ] 测试数据已准备

## Definition of Done（完成定义）

任务完成并可合入主分支前必须满足：

### 1. 代码质量
- [ ] 代码已实现计划的所有功能
- [ ] 代码遵循项目风格指南
- [ ] 无 linter 错误
- [ ] 代码已通过审查

### 2. 测试覆盖
- [ ] 单元测试已编写并通过
- [ ] 测试覆盖率达标（≥80%）
- [ ] 边界条件已测试
- [ ] `make dev_check` 通过

### 3. 文档完整
- [ ] `CONTRACT.md` 已更新
- [ ] `TEST_PLAN.md` 已更新
- [ ] `RUNBOOK.md` 已更新
- [ ] `PROGRESS.md` 已更新
- [ ] `CHANGELOG.md` 已更新
- [ ] `make docgen` 已执行

### 4. 回滚验证
- [ ] 回滚步骤已测试
- [ ] `make rollback_check` 通过（高风险变更）
- [ ] 数据库迁移有 down 脚本

### 5. CI 门禁
- [ ] 所有 CI 检查通过
- [ ] 无安全漏洞告警
- [ ] 性能指标在可接受范围

## 验证步骤

### 检查 DoR
```
# 1. 确认 plan.md 已更新
cat modules/<name>/plan.md

# 2. 确认契约存在
cat modules/<name>/CONTRACT.md

# 3. 确认验证命令可用
# 执行 plan.md 中列出的验证命令
```

## 检查 DoD
```
# 1. 运行完整检查
make dev_check

# 2. 确认文档已更新
git diff --name-only | grep -E "\.md$"

# 3. 回滚验证（高风险）
make rollback_check PREV_REF=<tag>
```

## 相关文档
- 开发流程：`agent.md` §5
- PR 规则：`agent.md` §10.5
- 代码审查：`agent.md` §11

