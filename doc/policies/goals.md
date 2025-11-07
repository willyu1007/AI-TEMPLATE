# 全局目标与设计原则

> **用途**: 定义AI-TEMPLATE项目的核心目标和设计原则
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## 四大核心目标

### 1. AI友好 🤖
**目标**: 让智能体高效理解和操作项目

**实现**:
- 文档可解析：使用YAML Front Matter + Markdown
- 路由明确：通过`context_routes`按需加载文档
- 上下文可控：分层读取，避免一次性加载全部文档
- Schema规范：所有关键文档都有Schema定义（schemas/）

**检验标准**:
- ✅ 智能体能在5分钟内理解项目结构
- ✅ 智能体能自动找到相关文档
- ✅ 智能体能识别模块边界和依赖关系

---

### 2. 模块化 🧩
**目标**: 模块独立、可替换、依赖清晰

**实现**:
- 同类型可替换：通过MODULE_TYPES.md定义类型规范
- 实例独立：每个模块实例有独立的agent.md和doc/
- I/O稳定：通过CONTRACT.md定义输入输出契约
- 依赖声明：在agent.md中明确upstream/downstream

**检验标准**:
- ✅ 同类型模块可以互换（如Select的不同实现）
- ✅ 模块可以独立开发和测试
- ✅ 依赖关系可以用DAG可视化

---

### 3. 自动化 ⚙️
**目标**: 全流程可校验、可脚本化、可CI化

**实现**:
- 校验脚本：覆盖agent.md、registry、文档路由等
- 生成脚本：自动生成registry.yaml草案、MODULE_INSTANCES.md
- CI门禁：`make dev_check`聚合所有校验
- 半自动化：registry.yaml、数据库操作需人工确认

**检验标准**:
- ✅ CI能检测出不规范的文档和代码
- ✅ 新增模块时能自动更新注册表
- ✅ 数据库操作需人工审核才能执行

---

### 4. 可编排 🎯
**目标**: 支持智能体自动读取/合并/调度

**实现**:
- 注册表：doc/orchestration/registry.yaml维护模块关系
- 路由规则：doc/orchestration/routing.md定义读取策略
- 编排提示：agent.md中的orchestration_hints指导调度
- 优先级：通过priority字段控制调度顺序

**检验标准**:
- ✅ Orchestrator能自动发现所有模块
- ✅ 根据任务类型选择合适的模块
- ✅ 支持模块间的数据流转

---

## 设计原则

### 原则1: 显式优于隐式
- 依赖关系显式声明（不依赖代码扫描）
- 权限显式授予（ownership.code_paths）
- 约束显式列举（constraints）

### 原则2: 文档驱动开发
- 先写agent.md和CONTRACT.md
- 再写代码
- 文档与代码同步维护

### 原则3: 最小权限原则
- 默认禁止越权写入
- 工具调用需白名单（tools_allowed）
- 网络访问需显式申请

### 原则4: 渐进式验证
- 开发阶段：警告模式（允许不完整）
- 提交阶段：严格模式（CI门禁）
- 生产阶段：强制模式（必须完整）

### 原则5: 分层架构
```
应用层 (app/frontend/)
    ↓
业务模块层 (modules/<entity>/)
    ↓
公共层 (common/)
    ↓
基础设施层 (db/, config/, observability/)
```

---

## 质量目标

### 文档质量
- 所有模块有agent.md和完整的doc/子目录
- agent.md通过Schema校验
- 文档路由路径全部有效

### 代码质量
- 测试覆盖率≥80%（模块可配置更高）
- 所有API有CONTRACT.md
- 通过一致性检查

### 维护质量
- CHANGELOG.md记录所有变更
- 兼容性检查通过
- 依赖关系清晰

---

## 非目标

明确**不做**的事情：

❌ **不追求100%自动化**
- registry.yaml需人工审核
- 数据库操作需人工确认
- 关键决策需人工参与

❌ **不过度工程化**
- 不引入复杂的框架
- 不过度抽象
- 保持简单可理解

❌ **不强制技术栈**
- 支持Python/Go/TypeScript多语言
- 模块可以选择合适的技术
- 不限制实现方式

---

## 目标达成验收

完成以下验收即认为达到目标：

### Phase验收（Phase 0-9）
- ✅ Phase 1: Schema与基础设施（已完成）
- ⏳ Phase 2: 目录结构调整（进行中）
- ⏳ Phase 3-9: 待执行

### 整体验收
- [ ] 所有模块有agent.md（带YAML Front Matter）
- [ ] registry.yaml正式化且校验通过
- [ ] 根agent.md轻量化到≤500行
- [ ] 所有文档路由路径有效
- [ ] CI门禁全部通过
- [ ] 初始化指南完善

---

**维护**: 项目目标变更时，更新本文档并经团队评审
**相关**: doc/policies/safety.md, doc/orchestration/routing.md

