# 角色与门禁

> **用途**: 定义AI、人类、CI的职责边界和门禁规则
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## 角色职责

### AI模型的职责
- 产出最小补丁（仅修改必要的代码）
- 编写自审文档（AI-SR）
- 更新文档和索引
- 确保测试通过

### 人类的职责
- 计划预审与合入审核
- 把关安全、性能、复杂度
- 选择是否放量上线
- 处理复杂决策

### CI门禁
- 运行`make dev_check`聚合校验
- 检查：docgen/DAG/契约兼容/配置/迁移/一致性/测试
- 不通过禁止合入
- 高风险变更需执行`make rollback_check PREV_REF=<tag|branch>`

---

## 边界原则

### AI应该做的
✅ 代码实现  
✅ 测试编写  
✅ 文档更新  
✅ 自动化脚本  
✅ 常规重构

### AI不应该做的
❌ 架构级决策（需人类确认）  
❌ 安全策略变更（需人类审核）  
❌ 生产环境操作（需人类执行）  
❌ 删除关键数据（需人类确认）  
❌ 跳过测试或校验

---

## 决策权限

| 决策类型 | AI | 人类 | 说明 |
|---------|-----|------|------|
| 添加功能 | ✅ | ✅ | AI实现，人类审核 |
| 修改接口 | ⚠️ | ✅ | AI提议，人类决策 |
| 架构调整 | ❌ | ✅ | 人类主导 |
| 安全变更 | ❌ | ✅ | 人类决策 |
| 性能优化 | ✅ | ✅ | AI实现，人类验证 |
| 代码重构 | ✅ | ✅ | AI执行，人类审核 |
| 数据迁移 | ⚠️ | ✅ | AI设计，人类审核并执行 |
| 紧急修复 | ✅ | ✅ | AI快速修复，人类立即审核 |

---

## 审核流程

### 快速通道（Low Risk）
- 文档更新
- 测试补充
- Bug修复（无接口变更）
- 性能优化（无行为变更）

**审核**: AI自审 + 自动CI → 合入

---

### 常规通道（Medium Risk）
- 新增功能
- 接口扩展（向后兼容）
- 代码重构
- 配置调整

**审核**: AI自审 + 自动CI + 人类Code Review → 合入

---

### 严格通道（High Risk）
- 接口变更（不兼容）
- 数据库迁移
- 架构调整
- 安全相关

**审核**: AI自审 + 自动CI + 人类Code Review + 架构师审核 + 回滚测试 → 合入

---

## 质量门槛

### 必须通过的检查
```bash
make dev_check
```

包含：
- [x] docgen - 文档索引
- [x] doc_style_check - 文档风格
- [x] dag_check - DAG拓扑
- [x] contract_compat_check - 契约兼容
- [x] runtime_config_check - 配置校验
- [x] migrate_check - 迁移检查
- [x] consistency_check - 一致性
- [x] frontend_types_check - 前端类型
- [x] agent_lint - Agent校验（Phase 1）
- [x] registry_check - 注册表校验（Phase 1）
- [x] doc_route_check - 文档路由（Phase 1）

### 高风险额外检查
```bash
make rollback_check PREV_REF=v1.0.0
```

验证可以回滚到指定版本。

---

## 相关文档

- **安全规范**: doc/policies/safety.md
- **全局目标**: doc/policies/goals.md
- **代码审查**: doc/process/code_review.md（待创建）

---

**维护**: 角色职责变更时更新
**审核**: 每季度审核一次

