# 模块初始化 - Phase 1: 规划

> **所属**: MODULE_INIT_GUIDE.md Phase 1  
> **用途**: Phase 1的详细执行指南  
> **目标**: 确定模块信息、类型、层级和接口定义

---

## 目标

确定模块的基本信息、类型、层级和接口定义

---

## 1.1 确定模块信息

AI应询问并记录：

**基本信息**:
- 模块名称（entity）：小写字母+下划线，如`user_auth`
- 模块描述：一句话说明模块功能
- 模块类型：1_Assign / 2_Select / 3_SelectMethod / 4_Aggregator
- 模块层级：1-4级

**类型和层级说明**，参考：`MODULE_TYPES.md`

**接口信息**:
- 是否对外提供HTTP接口？→ 决定是否创建`api/`子目录
- 是否有特定的前端组件？→ 决定是否创建`frontend/`子目录
- 输入和输出是什么？

**依赖关系**:
- 依赖哪些上游模块？（upstream）
- 输出到哪些下游？（downstream）
- 依赖哪些公共模块？（common/）

---

## 1.2 决策树：是否需要api/和frontend/

```
模块是否对外提供HTTP接口？
├─ 是 → 创建 api/ 子目录
│   └─ 在 api/routes.py 中定义接口
└─ 否 → 不创建 api/（模块只提供Python/Go函数）

模块是否有特定的UI组件？
├─ 是 → 创建 frontend/ 子目录
│   └─ 在 frontend/components/ 中实现组件
└─ 否 → 不创建 frontend/（只有通用UI）
```

**详细说明**：参考`temp/app_frontend_职责划分说明.md`

---

## 1.3 确认模块结构

展示将要创建的结构，用户确认：

```
modules/<entity>/
├── agent.md             ✅ 必须
├── README.md            ✅ 必须
├── plan.md              ✅ 必须
├── doc/                 ✅ 必须
│   ├── CONTRACT.md
│   ├── CHANGELOG.md
│   ├── RUNBOOK.md
│   ├── BUGS.md
│   ├── PROGRESS.md
│   └── TEST_PLAN.md
├── core/                ✅ 必须（业务逻辑）
│   └── __init__.py
├── api/                 ⚠️ 可选（如提供HTTP接口）
│   ├── routes.py
│   └── __init__.py
├── frontend/            ⚠️ 可选（如有特定UI）
│   └── components/
└── models/              ⚠️ 可选（如有专属模型）
    └── schemas.py
```

---

## AI对话脚本示例

```
AI: 让我们创建一个新模块。首先需要了解基本信息：

Q1: 模块名称？（小写+下划线，如user_auth）
用户: [输入]

Q2: 模块功能？（一句话描述）
用户: [输入]

Q3: 模块类型？
  - 1_Assign: 基础业务模块（用户、订单）
  - 2_Select: 选择/查询模块
  - 3_SelectMethod: 算法选择
  - 4_Aggregator: 聚合模块
  
详见: MODULE_TYPES.md

用户: [选择]

Q4: 模块层级？（1-4）
用户: [输入]

Q5: 该模块是否对外提供HTTP接口？
  - 是：创建 api/ 子目录
  - 否：仅内部调用，不创建

用户: [是/否]

Q6: 该模块是否有特定的UI组件？
  - 是：创建 frontend/ 子目录
  - 否：使用通用UI组件

用户: [是/否]

Q7: 输入和输出？
用户: [描述]

Q8: 依赖的上游模块？
用户: [列表]

Q9: 输出的下游模块？
用户: [列表]
```

---

## 信息记录表

| 字段 | 值 | 备注 |
|------|---|------|
| entity | _______ | 模块名 |
| description | _______ | 功能描述 |
| type | _______ | 模块类型 |
| level | _______ | 层级 |
| has_api | true/false | 是否创建api/ |
| has_frontend | true/false | 是否创建frontend/ |
| has_models | true/false | 是否创建models/ |
| inputs | _______ | 输入 |
| outputs | _______ | 输出 |
| upstream | [列表] | 上游依赖 |
| downstream | [列表] | 下游输出 |

---

## 常见问题

### Q: 如何判断是否需要api/子目录？
**A**: 询问用户是否对外提供HTTP接口。如果模块只提供Python/Go函数供其他模块调用，则不需要。

### Q: 如何判断是否需要frontend/子目录？
**A**: 询问用户是否有特定的UI组件。如果只是使用通用的列表、表单等，不需要创建。

### Q: 模块类型不确定怎么办？
**A**: 参考`MODULE_TYPES.md`的决策树和示例。大部分业务模块都是1_Assign类型。

### Q: 层级如何确定？
**A**: 
- Level 1: 基础服务（auth, config）
- Level 2: 核心业务（user, order）
- Level 3: 组合业务（workflow, analytics）
- Level 4: 聚合服务（dashboard, report）

---

## 下一步

完成规划后，进入 → [Phase 2: 创建目录](init-directory.md)

