# AI工作流模式库

> **AI优化文档** - 轻量化设计，约150行  
> **人类完整参考**: [PATTERNS_GUIDE.md](./PATTERNS_GUIDE.md)

---

## 快速开始

### 1. 查看所有模式
```bash
make workflow_list
```

### 2. 推荐合适的模式
```bash
make workflow_suggest PROMPT="创建用户模块"
```

### 3. 查看模式详情
```bash
make workflow_show PATTERN=module-creation
```

### 4. 应用模式（生成checklist）
```bash
make workflow_apply PATTERN=module-creation
```

---

## 可用模式（8个）

| ID | 名称 | 复杂度 | 时间 | 类别 | 优先级 |
|----|------|--------|------|------|--------|
| module-creation | 模块创建标准工作流 | medium | 2-4h | development | P0 |
| database-migration | 数据库变更标准工作流 | medium | 30-60min | maintenance | P0 |
| api-development | API开发标准工作流 | low | 1-2h | development | P0 |
| bug-fix | Bug修复标准工作流 | low | 30-90min | debugging | P0 |
| refactoring | 重构标准工作流 | medium | 1-3h | maintenance | P1 |
| feature-development | 功能开发标准工作流 | medium | 4-8h | development | P1 |
| performance-optimization | 性能优化标准工作流 | medium | 2-4h | optimization | P1 |
| security-audit | 安全审计标准工作流 | medium | 2-3h | maintenance | P1 |

---

## 如何选择模式

### 决策树

```
你想做什么？
├─ 创建新模块 → module-creation
├─ 开发新功能 → feature-development
├─ 修复Bug → bug-fix
├─ 开发API → api-development
├─ 数据库变更 → database-migration
├─ 重构代码 → refactoring
├─ 优化性能 → performance-optimization
└─ 安全审计 → security-audit
```

### 使用示例

#### 示例1: 创建用户模块
```bash
# 1. 推荐模式
make workflow_suggest PROMPT="创建用户管理模块"
# 输出: module-creation (匹配度0.90)

# 2. 查看详情
make workflow_show PATTERN=module-creation

# 3. 生成checklist
make workflow_apply PATTERN=module-creation > modules/users/TODO.md

# 4. 按checklist开发
```

#### 示例2: 修复登录Bug
```bash
# 1. 推荐模式
make workflow_suggest PROMPT="修复登录失败的bug"
# 输出: bug-fix (匹配度0.90)

# 2. 查看详情
make workflow_show PATTERN=bug-fix

# 3. 按工作流步骤执行
```

---

## 模式结构

每个模式包含：
- **前置条件**: 开始前需要满足的条件
- **工作流步骤**: 详细的执行步骤（6-9步）
- **常见陷阱**: 常见错误和解决方案
- **质量检查清单**: 完成前必须检查的项目
- **估时参考**: 每个步骤的时间估算
- **参考资源**: 相关文档和示例

---

## 自动触发

当你提到以下关键词时，系统会自动推荐相关模式：
- **创建/开发/添加** → 建议查看相关模式
- **修复/解决** → bug-fix模式
- **重构/优化** → refactoring或performance-optimization模式
- **数据库/表/SQL** → database-migration模式

---

## 相关资源

- **完整指南**: [PATTERNS_GUIDE.md](./PATTERNS_GUIDE.md) (人类文档，400行)
- **模式目录**: [catalog.yaml](./catalog.yaml) (自动生成)
- **示例参考**: [examples/](./examples/) (完整示例)
- **触发规则**: [/doc/orchestration/agent-triggers.yaml](/doc/orchestration/agent-triggers.yaml)

---

## 贡献新模式

如需添加新模式，参考现有模式结构：
1. 在`patterns/`目录创建YAML文件
2. 遵循模式Schema（见任意现有模式）
3. 运行`make workflow_validate`验证
4. 更新catalog.yaml（自动生成）

---

**💡 提示**: 这是AI优化文档，完整详细说明请查看[PATTERNS_GUIDE.md](./PATTERNS_GUIDE.md)

