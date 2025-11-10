# 模块初始化 - Phase 8: 建立上下文恢复机制

> **所属**: MODULE_INIT_GUIDE.md Phase 8  
> **用途**: Phase 8的详细执行指南  
> **目标**: 建立.context/目录，便于AI快速恢复模块上下文（推荐）

---

## 目标

建立.context/目录，存放模块上下文摘要文件

---

## 8.1 创建.context/目录

```bash
MODULE=<entity>

mkdir -p modules/$MODULE/.context
```

---

## 8.2 创建context.md

```markdown
# <Entity>模块上下文摘要

> **用途**: 帮助AI快速恢复模块上下文  
> **更新频率**: 每次重大变更后更新  
> **最后更新**: $(date +%Y-%m-%d)

---

## 快速概览

### 模块信息
- **名称**: <entity>
- **类型**: 1_Assign/<entity>
- **层级**: 1
- **状态**: planning
- **功能**: <一句话描述>

### 关键文件
- agent.md: 模块Agent配置
- README.md: 模块文档
- doc/CONTRACT.md: 接口契约
- doc/TEST_PLAN.md: 测试计划

---

## 核心概念

### 主要实体
- **Entity 1**: <描述>
- **Entity 2**: <描述>

### 关键流程
1. 流程1: <描述>
2. 流程2: <描述>

### 依赖关系
- **上游**: common.models.base
- **下游**: orchestrator.main

---

## 当前状态

### 已完成
- [x] 目录结构创建
- [x] 文档生成
- [x] 注册到registry
- [x] 校验通过

### 进行中
- [ ] 核心逻辑实现
- [ ] 单元测试编写

### 待办事项
- [ ] 集成测试
- [ ] 性能优化
- [ ] 文档完善

---

## 开发注意事项

### 约束
- 不得直接操作数据库，必须通过ORM
- 保持测试覆盖率≥80%

### 常见陷阱
- 注意XX情况
- 避免YY操作

---

## 快速命令

\`\`\`bash
# 运行测试
make test MODULE=<entity>

# 加载测试数据
make load_fixture MODULE=<entity> FIXTURE=minimal

# 校验模块
make validate
\`\`\`
```

---

## 8.3 创建decisions.md（可选）

记录重要决策：

```markdown
# <Entity>模块设计决策

## 决策001: 选择XXX方案

**日期**: 2025-XX-XX  
**问题**: <描述问题>  
**方案**: <选择的方案>  
**理由**: <为什么选择>  
**影响**: <对模块的影响>

## 决策002: ...
```

---

## 8.4 更新agent.md

在agent.md的Markdown正文部分添加：

```markdown
## 上下文恢复

如果需要快速了解本模块：
1. 阅读`.context/context.md`获取概览
2. 查看`README.md`了解功能
3. 参考`doc/CONTRACT.md`了解接口
4. 如有疑问，查阅`.context/decisions.md`

---
```

---

## .context/与其他文档的区别

| 文档 | 用途 | 受众 | 更新频率 |
|------|------|------|---------|
| agent.md | Agent配置 | AI Agent | 初始化时 |
| README.md | 模块文档 | 开发者 | 功能变更时 |
| .context/context.md | 上下文摘要 | AI恢复上下文 | 重大变更时 |
| .context/decisions.md | 设计决策 | 开发者+AI | 决策时 |

**关键区别**:
- README.md: 面向人类的完整文档
- .context/context.md: 面向AI的快速摘要（≤200行）

---

## 常见问题

### Q: .context/一定要创建吗？
**A**: 推荐创建。它能显著加快AI恢复上下文的速度，特别是在模块逐渐复杂后。

### Q: context.md应该包含什么？
**A**: 核心信息：
- 模块概览
- 关键文件索引
- 核心概念
- 当前状态
- 快速命令

### Q: context.md如何更新？
**A**: 每次重大变更后更新：
- 新增核心功能
- 重构架构
- 添加重要依赖
- 完成重要Phase

### Q: .context/会被git跟踪吗？
**A**: 是的。.context/文件应该提交到git，与代码一起版本控制。

---

## AI执行规范

**必须做**:
- ✅ 创建.context/目录
- ✅ 创建context.md（从模板复制并填写）
- ✅ 在agent.md中添加"上下文恢复"章节

**可选做**:
- 创建decisions.md
- 添加其他有助于上下文恢复的文件

**不要做**:
- ❌ 不要在.context/中放置代码
- ❌ 不要复制完整文档内容（只需摘要）
- ❌ 不要添加到.gitignore（应该被跟踪）

---

## 下一步

完成上下文机制后，模块初始化基本完成。可以：
- 开始编写核心代码（Phase 9）
- 或进行最终验收（Phase 9完成与验收）

