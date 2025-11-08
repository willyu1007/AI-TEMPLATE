# Example模块概览（精简版）

> **读者**: AI/智能编排系统  
> **限制**: <200行

---

## 背景

AI-TEMPLATE项目模板需要完整的模块示例，展示标准结构和文档体系。

---

## 目标

1. **参考示例**: 展示模块结构（agent.md, doc/6个, fixtures/）
2. **测试数据**: 验证工具链（agent_lint等）
3. **模板来源**: 为新模块提供可复制结构

---

## 关键约束

1. **定位**: example是参考文档，不是业务模块
   - 位置：doc/modules/example/（Phase 4移入）
   - 注册：registry.yaml的reference_modules

2. **内容**: 保持简单，不过度复杂
   - 仅展示结构，无业务逻辑
   - 测试数据最小化

3. **阅读**: 不应被频繁读取
   - 仅在需要参考时查阅

---

## 演进里程碑

- Phase 4: 标准化，移至doc/modules/
- Phase 6: 添加测试数据（TEST_DATA.md, fixtures/）
- Phase 8.5: 添加.context/机制

---

## 参考链接

**模块文档**:
- `../agent.md` - AI配置（完整YAML示例）
- `../doc/CONTRACT.md` - 接口契约示例
- `../doc/TEST_DATA.md` - 测试数据规格
- `decisions.md` - 设计决策和**错误记录**

**规范文档**:
- `doc/modules/MODULE_INIT_GUIDE.md`
- `doc/modules/MODULE_TYPES.md`
- `doc/process/CONTEXT_GUIDE.md`

---

**最后更新**: 2025-11-08

