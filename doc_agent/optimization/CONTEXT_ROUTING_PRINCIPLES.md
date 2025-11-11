# Context Routing Principles for AI Orchestration

## 核心理念：层次化的目的驱动导航

### 1. 为什么Context Routes必须保持完整

Context routes不仅仅是文件列表，而是AI理解和导航代码库的**认知地图**。每个route包含：

- **Topic**: 明确的主题标识（如"S0 Orientation - Explain TemplateAI"）
- **When**: 清晰的使用场景描述
- **Priority**: 重要性层级
- **Audience**: 目标受众（ai/human/both）
- **Load Policy**: 加载策略
- **Paths**: 具体文件路径

这些信息共同构成了AI的**决策树**，使其能够：
1. 理解当前任务的上下文需求
2. 选择合适的文档路径
3. 避免加载无关内容
4. 遵循正确的深度探索策略

### 2. 层次化导航模式

```
Level 0: AGENTS.md (根编排器)
    ↓ [根据topic选择路由]
Level 1: 模块级AGENTS.md
    ↓ [根据具体需求深入]
Level 2: 特定文档（CONTRACT.md, README.md等）
    ↓ [按需加载实现细节]
Level 3: 源代码文件
```

### 3. 目的性明确的重要性

每个context route的`when`字段是关键，它告诉AI：
- 什么情况下需要这个context
- 如何判断是否相关
- 加载的优先级如何

例如：
```yaml
- topic: "Module development - classify or scaffold"
  when: "Selecting module type, scaffolding instances, or reviewing examples."
  # AI可以明确理解：这是在创建新模块时需要的
```

对比简化版本：
```yaml
- topic: "Module development"
  priority: high
  # AI无法准确判断何时需要这个context
```

### 4. 优化策略（不破坏完整性）

#### 4.1 缓存常用路由组合
```python
# 预定义常见任务的context组合
TASK_CONTEXT_PRESETS = {
    "create_module": [
        "/doc_agent/specs/MODULE_TYPES.md",
        "/doc_agent/init/module-init.md",
        "/doc_human/guides/MODULE_INSTANCES.md"
    ],
    "fix_bug": [
        "/doc_agent/coding/TEST_STANDARDS.md",
        "/doc_agent/coding/AI_CODING_GUIDE.md"
    ]
}
```

#### 4.2 动态优先级调整
```python
# 基于使用频率动态调整priority
def adjust_route_priority(route, usage_stats):
    if usage_stats[route.topic] > threshold:
        route.priority = "high"
```

#### 4.3 Context预加载
```python
# 在任务开始时预加载高概率使用的contexts
def preload_likely_contexts(task_type):
    likely_routes = predict_routes(task_type)
    cache.preload(likely_routes)
```

### 5. 智能编排的核心要素

1. **目的驱动**: 每个route都有明确的使用目的
2. **层次清晰**: 从高层抽象到具体实现
3. **按需加载**: 只在需要时加载相关内容
4. **缓存友好**: 高频内容缓存，低频内容按需加载
5. **可追溯性**: 每次加载都能追溯到具体原因

### 6. 最佳实践

#### DO ✅
- 保持完整的context_routes结构
- 使用明确的`when`条件
- 按任务类型组织routes
- 实现智能缓存策略
- 维护路由的层次关系

#### DON'T ❌
- 简化或删除`when`字段
- 仅依赖priority进行选择
- 破坏路由的层次结构
- 过度压缩route信息
- 忽视audience区分

### 7. 优化示例：保持完整性的同时提升效率

```yaml
# 优化前：所有信息内联
context_routes:
  on_demand:
    - topic: "Very long topic description..."
      when: "Very detailed when condition..."
      paths: [many, paths, listed, here]

# 优化后：保持结构，优化加载
context_routes:
  on_demand:
    - topic: "Module development"
      when: "Creating or modifying modules"
      ref: "#module_dev_routes"  # 引用详细配置
      cache: true  # 标记为可缓存
```

### 8. Token优化的正确方向

不是减少route信息，而是：
1. **智能缓存**: 缓存常用route组合
2. **延迟加载**: 只在确认需要时加载详细paths
3. **压缩传输**: 使用简短的引用替代重复内容
4. **预测加载**: 基于任务类型预测需要的routes

### 总结

Context routing是AI编排的**神经系统**，必须保持其完整性和目的性。优化应该着重于：
- 提高路由选择的智能性
- 优化加载和缓存策略
- 保持信息的完整性和可理解性

记住：**AI需要理解"为什么"和"何时"，而不仅仅是"什么"。**
