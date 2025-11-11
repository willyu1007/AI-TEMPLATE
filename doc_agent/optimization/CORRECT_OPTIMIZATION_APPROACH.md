# Correct AI Orchestration Optimization Approach

## Core Understanding: The Essence of Context Routes

The previous optimization approach was incorrect. Here's the correct understanding:

### Incorrect Optimization Approach
```yaml
# Wrong: Simplified routes with only priority levels
context_routes:
  high_priority: [file1, file2]
  medium_priority: [file3, file4]
  
# Problem: AI cannot understand why these files are needed
```

### Correct Optimization Approach
```yaml
# Correct: Maintain complete purposeful descriptions
context_routes:
  on_demand:
    - topic: "Module development - classify or scaffold"
      when: "Selecting module type, scaffolding instances, or reviewing examples."
      paths: [...]
      
# Advantage: AI understands the specific purpose of each context
```

## 层次化导航的重要性

### 1. 逐层深入的智能编排

```
用户意图："创建新的认证模块"
    ↓
Layer 0: 基础上下文（always_read）
    - /doc_agent/index/AI_INDEX.md
    ↓
Layer 1: 任务相关路由（基于when条件匹配）
    - Module development routes
    - Project initialization routes
    ↓
Layer 2: 具体实现（从路由指向的文件深入）
    - MODULE_TYPES.md → 理解模块类型
    - module-init.md → 获取创建流程
    ↓
Layer 3: 代码生成（基于上层理解）
    - 生成符合规范的代码
```

### 2. 目的性驱动的选择机制

每个route的关键要素：
- **topic**: 主题标识（帮助分类）
- **when**: 使用场景（核心判断依据）
- **audience**: 受众（ai/human/both）
- **load_policy**: 加载策略
- **paths**: 具体文件

AI通过**when条件**理解：
1. 当前任务是否需要这个context
2. 什么时机加载最合适
3. 如何与其他context配合

## 优化的正确方向

### 1. 保持结构完整性，优化加载策略

```python
# smart_context_router.py 的设计理念
class SmartContextRouter:
    def select_routes(self, user_intent):
        # 1. 解析用户意图
        # 2. 匹配when条件
        # 3. 构建层次化加载计划
        # 4. 只加载相关context
```

### 2. 智能缓存（不破坏结构）

```python
# 缓存常用组合，而非简化结构
TASK_PRESETS = {
    "create_module": {
        "routes": [...],  # 完整route信息
        "cache_ttl": 3600
    }
}
```

### 3. 动态优先级调整

```python
# 基于使用频率动态调整，但保持when描述
def adjust_priority(route, usage_stats):
    if usage_stats[route.topic] > threshold:
        route.priority = "high"  # 只改优先级，不改结构
```

## 实践示例：创建模块的正确流程

### Step 1: 意图识别
```
用户："I need to create a new module for user authentication"
识别：task_type = "create_module", domain = "authentication"
```

### Step 2: 路由匹配（基于when条件）
```
匹配的routes:
1. "Module development - classify or scaffold"
   when: "Selecting module type, scaffolding instances..."
   ✅ 高度相关
   
2. "Testing & fixtures"
   when: "Define coverage gates, fixture etiquette..."
   ✅ 相关但次要
   
3. "Commit & PR workflow"
   when: "Human contributors ask for approval..."
   ❌ 当前不相关
```

### Step 3: 层次化加载
```
Layer 0: /doc_agent/index/AI_INDEX.md (130 tokens)
Layer 1: Module development routes (800 tokens)
Layer 2: Testing routes (如需要) (500 tokens)
Total: ~1430 tokens (在2000预算内)
```

## 关键洞察

### 1. Context Routes是认知地图
- 不仅是文件列表，而是AI理解代码库的地图
- when条件是导航的"路标"
- 层次结构反映了认知的深度

### 2. 目的性是核心
- 每个route都要回答："为什么需要这个context？"
- AI基于目的选择路径，而非简单的优先级
- 保持when描述的完整性至关重要

### 3. 优化不是简化
- 优化是让选择更智能，而非减少信息
- 缓存是为了速度，而非替代结构
- 层次化是为了效率，而非扁平化

## 总结：正确的优化原则

### DO
1. 保持完整的when条件描述
2. 实现智能的路由匹配算法
3. 使用缓存加速常用路径
4. 构建层次化的加载策略
5. 基于任务意图动态选择

### DON'T
1. 简化或删除when字段
2. 仅依赖priority分级
3. 将routes扁平化处理
4. 破坏topic的语义信息
5. 忽视audience区分

## 实施建议

1. **保持AGENTS.md的完整性**
   - 所有route信息都保留
   - 不要为了节省token而损失语义

2. **使用SmartContextRouter**
   - 智能匹配when条件
   - 构建层次化加载计划
   - 缓存常用路径组合

3. **监控和优化**
   - 追踪route使用频率
   - 识别常用任务模式
   - 预加载高频组合

记住：**AI需要理解"为什么"（when）和"如何"（层次），而不仅仅是"什么"（files）。**

优化应该让AI更智能地导航，而不是让地图变得更简单。
