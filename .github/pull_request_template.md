## 变更说明
[简要描述本次变更的目的和内容]

## 变更类型
- [ ] 新功能 (feature)
- [ ] Bug 修复 (fix)
- [ ] 重构 (refactor)
- [ ] 文档 (docs)
- [ ] 性能优化 (perf)
- [ ] 测试 (test)
- [ ] 构建/工具链 (chore)
- [ ] 其他: _____

## 影响范围

### 模块
- [ ] `modules/user` - 用户模块
- [ ] `modules/auth` - 认证模块
- [ ] 其他: _____

### 接口/契约
- [ ] 无变更
- [ ] `tools/api/contract.json` - API 契约变更
- [ ] 向后兼容 ✅ / 破坏性变更 ⚠️（说明原因）

### DAG
- [ ] 无变更
- [ ] 新增节点: `_____`
- [ ] 修改边: `_____`
- [ ] 删除节点: `_____`

### 数据库
- [ ] 无变更
- [ ] 新增迁移: `migrations/XXX_*_up.sql` / `migrations/XXX_*_down.sql`
- [ ] 影响表: `_____`
- [ ] 数据变更: 是 / 否

### 配置
- [ ] 无变更
- [ ] 新增配置项: `config/defaults.yaml` - `_____`
- [ ] 修改配置项: `_____`
- [ ] 需要更新环境变量: 是 / 否

## 测试

### 已添加的测试
- [ ] 单元测试: `tests/<module>/test_*.py`
- [ ] 集成测试: `tests/<module>/test_integration.py`
- [ ] 边界测试: 覆盖边界条件
- [ ] 回归测试: 验证未引入新问题

### 测试执行结果
```bash
# 粘贴测试输出
$ make dev_check
✅ 所有检查通过
```

## 覆盖率
- **当前覆盖率**: ___%
- **变更后覆盖率**: ___%
- **是否达标**: ✅ 是 (≥80%) / ❌ 否（说明原因）

## 性能影响

- [ ] 无性能影响
- [ ] 性能提升: [具体指标]
- [ ] 性能下降: [具体指标和原因]
- [ ] 需要性能测试: 是 / 否

## 安全影响

- [ ] 无安全影响
- [ ] 涉及敏感数据处理
- [ ] 涉及权限变更
- [ ] 需要安全审查: 是 / 否

## 自审（AI-SR）

**自审文档链接**: `ai/sessions/<date>_<name>/AI-SR-impl.md`

### 关键风险
- [列出主要风险点，或写"无"]

### 回滚方案
- **代码回滚**: `git revert <commit>` / `git checkout <previous-tag>`
- **数据库回滚**: `psql -f migrations/XXX_down.sql`
- **Feature Flag**: [如适用]
- **回滚验证**: ✅ 已验证 / ⚠️ 待验证

### 影响分析
- **影响范围**: [小/中/大]
- **用户影响**: [有/无]
- **数据影响**: [有/无]
- **兼容性**: [向后兼容/需要迁移]

## 文档更新

- [ ] README.md（如需要）
- [ ] modules/<module>/README.md
- [ ] modules/<module>/CONTRACT.md
- [ ] modules/<module>/TEST_PLAN.md
- [ ] modules/<module>/RUNBOOK.md
- [ ] modules/<module>/CHANGELOG.md
- [ ] flows/dag.yaml（如变更）
- [ ] docs/db/DB_SPEC.yaml（如变更）
- [ ] 索引已刷新：`make docgen` ✅

## 相关链接

- **计划文档**: `modules/<module>/plan.md`
- **相关 Issue**: #___
- **相关 PR**: #___
- **设计文档**: [链接]

## 截图/演示

[如适用，添加截图或 GIF 展示变更效果]

---

## 提交前检查清单

根据 `AGENTS.md` §10.5 PR 规则：

### 必须完成
- [ ] 所有测试通过（`make dev_check`）
- [ ] 代码覆盖率达标（核心模块 ≥80%）
- [ ] 文档已更新（README/CONTRACT/TEST_PLAN/CHANGELOG）
- [ ] 索引已刷新（`make docgen`）
- [ ] 无 linter 错误
- [ ] 契约兼容性检查通过（如涉及）
- [ ] 自审文档已生成（AI-SR-impl.md）
- [ ] 临时文件已清理（运行 `make cleanup_temp` 确认无 `*_temp.*` 文件）

### 高风险变更额外检查
- [ ] 回滚验证通过（`make rollback_check PREV_REF=<tag>`）
- [ ] 数据库迁移脚本（up/down）已编写
- [ ] Feature Flag 已配置（如需渐进发布）
- [ ] 性能测试通过（如涉及关键路径）

---

## Reviewer 清单

根据 `AGENTS.md` §11 代码审查流程，请审查者检查：

### 🏗️ Repo 级（如适用）
- [ ] 架构一致性
- [ ] 契约向后兼容
- [ ] 数据库迁移成对

### 模块级
- [ ] 模块职责单一
- [ ] 文档齐全
- [ ] 测试覆盖率达标

### ⚙️ 代码级
- [ ] 接口设计合理
- [ ] 代码逻辑清晰
- [ ] 错误处理完整
- [ ] 无明显性能/安全问题

---

**参考**：
- 完整 PR 规则：`AGENTS.md` §10.5
- 代码审查流程：`AGENTS.md` §11
- 测试准则：`AGENTS.md` §6
