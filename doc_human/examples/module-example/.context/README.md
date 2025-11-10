# .context/ - 上下文恢复（精简版）

> **读者**: AI/智能编排系统  
> **用途**: 模块背景、决策和错误记录

---

## 快速恢复

**5分钟**: `overview.md` + `../plan.md`  
**15分钟**: 上述 + `decisions.md`（含错误记录）

---

## 文件说明（精简结构，仅3个文件）

- **overview.md**: 背景、目标、约束（<200行）
- **decisions.md**: 设计决策 + **错误经验**（持续追加）
- **prd.md**: 原始需求（可选，如有）

**禁止**: ❌ 不要创建子目录！扁平结构即可！

---

## 路由配置

在`../agent.md`的`context_routes.on_demand`中：

```yaml
- topic: "模块背景和决策"
  paths: [".context/overview.md", ".context/decisions.md"]
  when: "上下文丢失或需要避免重复错误"
```

---

## 写入原则

**何时写**:
- 模块初始化
- 重大决策后
- **踩坑后**（⭐ 记录错误）

**写什么**:
- 背景和目标（overview.md）
- 技术决策和原因（decisions.md）
- **走过的弯路和错误**（decisions.md）⭐

**详见**: `doc/process/CONTEXT_GUIDE.md`

