# AI工作流模式库 - 完整指南（人类文档）

> **完整参考文档** - 详细说明，约400行  
> **AI轻量版**: [README.md](./README.md)

---

## 目录

1. [概述](#概述)
2. [核心理念](#核心理念)
3. [8个核心模式](#8个核心模式)
4. [如何使用](#如何使用)
5. [模式结构说明](#模式结构说明)
6. [最佳实践](#最佳实践)
7. [创建新模式](#创建新模式)
8. [常见问题](#常见问题)

---

## 概述

AI工作流模式库是沉淀的常见开发场景最佳实践，帮助AI和开发者快速、规范地完成各类开发任务。

**核心价值**:
- ✅ 标准化工作流程
- ✅ 避免遗漏关键步骤
- ✅ 提供质量检查清单
- ✅ 沉淀团队最佳实践
- ✅ 加速新手上手

---

## 核心理念

### AI与人类文档分离

遵循Phase 11.1的设计理念：
- **AI文档（patterns/*.yaml）**: 轻量化，200-300行，结构化YAML
- **人类文档（examples/*.md）**: 完整版，300-500行，Markdown格式

### 模式优先级

- **P0（必须实施）**: module-creation, database-migration, api-development, bug-fix
- **P1（建议实施）**: refactoring, feature-development, performance-optimization, security-audit

---

## 8个核心模式

### P0: 高优先级模式

#### 1. module-creation（模块创建）
**适用场景**: 创建新的业务模块  
**复杂度**: medium  
**时间**: 2-4小时  
**步骤**: 9步（规划→目录→文档→注册→代码→数据库→测试数据→上下文→校验）

#### 2. database-migration（数据库变更）
**适用场景**: 表/字段/索引的创建、修改、删除  
**复杂度**: medium  
**时间**: 30-60分钟  
**步骤**: 6步（需求分析→表YAML→迁移脚本→测试数据→本地验证→自动化检查）

#### 3. api-development（API开发）
**适用场景**: RESTful或GraphQL接口开发  
**复杂度**: low  
**时间**: 1-2小时  
**步骤**: 6步（设计→路由→业务逻辑→测试→文档→集成测试）

#### 4. bug-fix（Bug修复）
**适用场景**: 系统化定位和修复Bug  
**复杂度**: low  
**时间**: 30-90分钟  
**步骤**: 6步（重现→根因分析→修复→回归测试→文档→验证）

### P1: 建议实施模式

#### 5. refactoring（重构）
**适用场景**: 不改变外部行为的代码重构  
**复杂度**: medium  
**时间**: 1-3小时  
**步骤**: 6步（计划→保存状态→小步重构→测试→审查→文档）

#### 6. feature-development（功能开发）
**适用场景**: 新功能从需求到上线  
**复杂度**: medium  
**时间**: 4-8小时  
**步骤**: 6步（需求理解→技术设计→任务拆分→迭代开发→集成测试→发布）

#### 7. performance-optimization（性能优化）
**适用场景**: 响应慢、吞吐低、资源占用高  
**复杂度**: medium  
**时间**: 2-4小时  
**步骤**: 6步（问题确认→瓶颈定位→优化实施→性能测试→监控配置→文档）

#### 8. security-audit（安全审计）
**适用场景**: 安全检查和漏洞修复  
**复杂度**: medium  
**时间**: 2-3小时  
**步骤**: 6步（范围确定→代码审查→配置检查→依赖扫描→修复→监控）

---

## 如何使用

### 命令行使用

```bash
# 1. 列出所有模式
make workflow_list

# 2. 推荐合适的模式
make workflow_suggest PROMPT="创建用户模块"

# 3. 查看模式详情
make workflow_show PATTERN=module-creation

# 4. 生成任务清单
make workflow_apply PATTERN=module-creation > TODO.md

# 5. 校验模式文件
make workflow_validate
```

### 集成使用

模式库已集成到智能触发系统。当你提到特定关键词时，会自动推荐相关模式：

```python
# 在开发中提到"创建模块"
# → 自动触发workflow-pattern-suggestion规则
# → 加载README.md和catalog.yaml
# → 推荐module-creation模式
```

---

## 模式结构说明

每个模式YAML文件包含以下部分：

### 1. 元数据
```yaml
pattern_id: "module-creation"
version: "1.0"
name: "模块创建标准工作流"
description: "从需求到上线的完整模块开发流程"
complexity: "medium"  # low|medium|high
estimated_time: "2-4 hours"
ai_optimized: true
category: "development"
```

### 2. 前置条件
```yaml
prerequisites:
  - "已有清晰的模块需求"
  - "已确定模块类型"
```

### 3. 工作流步骤
每个步骤包含：
- `step`: 步骤编号
- `name`: 步骤名称
- `description`: 简要描述
- `estimated_time`: 预估时间
- `ai_prompt_template`: AI执行的prompt模板
- `documents_to_load`: 需要加载的文档列表
- `expected_output`: 预期输出
- `validation`: 验证标准
- `common_issues`: 常见问题和解决方案

### 4. 常见陷阱
```yaml
pitfalls:
  - issue: "问题描述"
    impact: "影响说明"
    solution: "解决方案"
    severity: "critical|high|medium|low"
```

### 5. 质量检查清单
```yaml
quality_checklist:
  - "[ ] 检查项1"
  - "[ ] 检查项2"
```

### 6. 参考资源
```yaml
references:
  detailed_guide: "/ai/workflow-patterns/examples/xxx-example.md"
  related_patterns: ["pattern-id"]
```

---

## 最佳实践

### 1. 选择合适的模式

**决策流程**:
1. 明确你的目标（创建/修复/优化/审计等）
2. 使用`workflow_suggest`获取推荐
3. 查看模式详情确认适用性
4. 生成checklist开始执行

### 2. 遵循步骤顺序

模式步骤经过优化，建议按顺序执行：
- 每步完成后验证
- 遇到问题查看`common_issues`
- 使用`quality_checklist`自查

### 3. 自定义和扩展

**方式1: 使用现有模式作为基础**
- 生成checklist后根据实际情况调整
- 跳过不适用的步骤

**方式2: 创建新模式**
- 参考现有模式结构
- 遵循YAML Schema
- 运行`make workflow_validate`校验

### 4. 团队协作

- **标准化**: 团队统一使用模式库
- **Review**: Code Review时对照checklist
- **改进**: 持续更新模式内容

---

## 创建新模式

### 步骤

1. **创建YAML文件**
```bash
cd ai/workflow-patterns/patterns/
cp module-creation.yaml your-pattern.yaml
```

2. **编辑模式内容**
- 修改pattern_id和name
- 定义workflow步骤
- 添加常见陷阱
- 编写质量清单

3. **创建示例文档（可选）**
```bash
cd ../examples/
# 创建完整的Markdown示例
```

4. **校验**
```bash
make workflow_validate
```

5. **更新catalog.yaml**
手动或自动更新索引

---

## 常见问题

### Q1: 模式太长，能否简化？
A: 是的。每个模式都是完整版，实际使用时可根据场景跳过部分步骤。

### Q2: 能否组合多个模式？
A: 可以。如`feature-development`中可能包含`api-development`和`database-migration`。

### Q3: 如何处理模式不适用的情况？
A: 使用模式作为参考，根据实际情况调整。模式是指南而非强制规定。

### Q4: 团队如何共享自定义模式？
A: 将自定义模式提交到repo，团队成员pull后即可使用。

### Q5: 模式是否会更新？
A: 会。随着实践积累，模式会持续优化。查看pattern的`version`字段。

---

## 效果评估

### 预期收益（Phase 12目标）

- ✅ AI开发效率: +40%（有模式可循）
- ✅ 代码质量: +25%（标准化流程）
- ✅ 新手上手速度: +60%（有完整参考）
- ✅ Token节省: +15%（避免试错）

### 实际监控

使用以下指标监控效果：
- 模式使用频率（`make workflow_suggest`调用次数）
- 任务完成时间（对比使用前后）
- 代码质量指标（测试覆盖率、Bug率）

---

## 相关资源

- **模式文件**: [patterns/](./patterns/)
- **示例文档**: [examples/](./examples/)
- **模式索引**: [catalog.yaml](./catalog.yaml)
- **推荐引擎**: [scripts/workflow_suggest.py](/scripts/workflow_suggest.py)
- **触发规则**: [agent-triggers.yaml](/doc/orchestration/agent-triggers.yaml)

---

## 反馈和改进

如有建议或发现问题：
1. 在模块的BUGS.md中记录
2. 提交issue或PR
3. 团队讨论会上提出

持续改进模式库是提升团队效率的关键！

---

**最后更新**: 2025-11-09（Phase 12）

