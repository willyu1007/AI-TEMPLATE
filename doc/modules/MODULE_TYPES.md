---
audience: ai
language: zh
version: summary
purpose: ⚠️ To be translated to English
---
# 模块类型说明

> **用途**: 定义模块的分类标准和命名规范
> **版本**: 2.0
> **最后更新**: 2025-11-07

---

## 快速参考

### 4种核心类型

| 类型 | 命名 | Level | 职责 | 典型实例 |
|------|------|-------|------|---------|
| **Assign** | `1_<entity>` | 1-2 | CRUD基础操作 | user, order, product |
| **Select** | `2_<domain>` | 1-2 | 查询/筛选数据 | user_query, data_filter |
| **SelectMethod** | `3_<strategy>` | 2-3 | 策略选择/执行 | payment_method, shipping_method |
| **Aggregator** | `4_<domain>_aggregator` | 3-4 | 数据聚合 | dashboard, report |

### 快速决策

```
需要CRUD操作？ → 1_Assign
需要查询筛选？ → 2_Select
需要策略选择？ → 3_SelectMethod
需要数据聚合？ → 4_Aggregator
```

**详细IO契约**: 参见 `MODULE_TYPE_CONTRACTS.yaml`

---

## 1. 核心概念

### 1.1 什么是模块类型

模块类型（Module Type）是对模块功能的抽象分类：
- **同类型模块遵循相同的IO契约** - 确保可替换性
- **同类型模块可以互相替换** - 不影响系统运行
- **类型决定模块在编排中的角色** - 定义职责边界

### 1.2 类型 vs 实例

```
类型（Type）：抽象定义（1_Assign）
  ↓
实例（Instance）：具体实现
  ├─ user.v1
  ├─ order.v1
  └─ product.v1
```

**关键**: 同类型的不同实例必须可以互相替换。

---

## 2. 模块层级（Level）

### 层级定义

```
Level 1: 基础模块 - 不依赖其他业务模块
Level 2: 组合模块 - 组合Level 1
Level 3: 编排模块 - 编排Level 1-2
Level 4: 聚合模块 - 聚合Level 1-3
```

### 依赖规则

```
✅ 允许: 高层级 → 低层级（Level 3 → Level 1）
❌ 禁止: 低层级 → 高层级（Level 1 → Level 2）
⚠️ 谨慎: 同层级互相调用（需检查循环依赖）
```

---

## 3. 类型详解

### 3.1 类型1: Assign（分配型）⭐

**定义**: 单一实体的CRUD操作

**命名**: `1_<entity>`（如 1_user, 1_order）

**IO契约**:
```yaml
输入: entity_id, action(CRUD), payload
输出: result{status, data}, metadata
```

**典型场景**: 用户管理、订单管理、商品管理

**完整契约**: 见 `MODULE_TYPE_CONTRACTS.yaml` § Assign

---

### 3.2 类型2: Select（选择型）🔍

**定义**: 查询和筛选数据

**命名**: `2_<domain>_<action>`（如 2_user_query, 2_data_filter）

**IO契约**:
```yaml
输入: query{filters, sort, pagination}, data_source
输出: results[], total_count
```

**典型场景**: 用户查询、订单搜索、数据过滤

**完整契约**: 见 `MODULE_TYPE_CONTRACTS.yaml` § Select

---

### 3.3 类型3: SelectMethod（方法选择型）⚙️

**定义**: 策略选择和执行（策略模式）

**命名**: `3_<strategy>_method`（如 3_payment_method）

**IO契约**:
```yaml
输入: context, options[]
输出: selected_method, execution_result
```

**典型场景**: 支付方式选择、配送方式选择、定价策略

**完整契约**: 见 `MODULE_TYPE_CONTRACTS.yaml` § SelectMethod

---

### 3.4 类型4: Aggregator（聚合型）📊

**定义**: 聚合多个模块的输出

**命名**: `4_<domain>_aggregator`（如 4_dashboard_aggregator）

**IO契约**:
```yaml
输入: module_outputs[{module_id, output}]
输出: aggregated_data
```

**典型场景**: 仪表盘、业务报表、指标汇总

**完整契约**: 见 `MODULE_TYPE_CONTRACTS.yaml` § Aggregator

---

## 4. 类型选择

### 决策树

```
├─ 操作单一实体（CRUD）？ → 1_Assign
├─ 查询/筛选数据？ → 2_Select
├─ 根据条件选择方法？ → 3_SelectMethod
└─ 聚合多个模块输出？ → 4_Aggregator
```

### 典型组合

```
用户订单查询:
  1_order → 2_order_search → 4_dashboard

支付流程:
  1_order → 3_payment_method → 1_payment

业务报表:
  [1_user, 1_order, 1_product] → 4_business_overview
```

---

## 5. 类型关系

### 数据流向

```
1_Assign ──→ 2_Select ──→ 3_SelectMethod ──→ 4_Aggregator
    └────────────┴─────────────┴──────────────┘
           （可直接流向高层级）
```

**详细关系**: 见 `MODULE_TYPE_CONTRACTS.yaml` 的 `type_relations` 和 `data_flows`

---

## 6. 可替换性

### 替换规则

**同类型模块可以互相替换**，前提是：
- ✅ IO契约相同
- ✅ 行为兼容
- ✅ 无副作用

### 版本管理

```
新增可选字段 → minor（v1.1）✅ 兼容
修改必需字段 → major（v2.0）❌ 不兼容
删除字段     → major（v2.0）❌ 不兼容
```

---

## 7. 自定义类型

### 创建步骤

1. 在 `MODULE_TYPE_CONTRACTS.yaml` 添加定义
2. 在 `registry.yaml` 注册类型
3. 在本文档添加说明
4. 运行 `make registry_check` 验证

### 何时需要

- 现有4种类型无法描述模块
- 项目有特定业务模式
- 需要新的契约规范

---

## 8. 常见问题

**Q: 如何判断模块Level？**  
A: 看依赖关系。不依赖其他业务模块 = Level 1，依赖Level 1 = Level 2，以此类推。

**Q: 同类型不同Level可以替换吗？**  
A: 谨慎替换，需评估IO契约和依赖链。

**Q: 如何确保IO契约统一？**  
A: 参考 `MODULE_TYPE_CONTRACTS.yaml`，在agent.md中引用contracts，运行 `make agent_lint`。

**Q: 模块可以属于多个类型吗？**  
A: 不建议。功能复杂时考虑拆分或创建自定义类型。

---

## 9. 相关文档

| 文档 | 用途 | 何时阅读 |
|------|------|---------|
| **MODULE_TYPE_CONTRACTS.yaml** | IO契约详细定义 | 创建模块时必读 ⭐ |
| **MODULE_INIT_GUIDE.md** | 模块初始化指南 | 创建新模块时 |
| **MODULE_INSTANCES.md** | 现有模块列表 | 查看已有模块时 |
| **example/** | 完整模块示例 | 学习模块结构时 |
| **registry.yaml** | 模块注册表 | 了解模块关系时 |

---

## 10. 维护说明

### 更新时机
- 添加新的模块类型
- 修改类型定义或IO契约
- 更新命名规范

### 同步更新
1. `MODULE_TYPE_CONTRACTS.yaml` - IO契约定义
2. `registry.yaml` - 类型注册
3. `example/agent.md` - 示例模块

### 版本历史
- **v2.0** (2025-11-07): 精简版本，添加快速参考，IO契约移至CONTRACTS.yaml
- **v1.0** (2025-11-07): 初始版本

---

**📌 提示**: 本文档是概念说明，详细的IO契约、数据流向、包含关系请查看 `MODULE_TYPE_CONTRACTS.yaml`
