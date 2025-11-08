# Workdocs使用指南

> **用途**: 详细说明如何使用ai/workdocs/机制  
> **目标受众**: AI Agent和开发者  
> **版本**: 1.0  
> **创建时间**: 2025-11-08

---

## 概述

### 什么是Workdocs

Workdocs是AI任务的上下文管理机制，为每个开发任务提供：
- **plan.md**: 战略计划和实施方案
- **context.md**: 关键上下文和进度追踪（**最重要**）
- **tasks.md**: 详细任务清单和验收标准

### 核心价值

**为AI提供**:
- ✅ 快速恢复任务上下文（2-5分钟 vs 15-30分钟）
- ✅ 清晰的进度追踪（SESSION PROGRESS）
- ✅ 错误记录避免重复（ERROR记录）
- ✅ 关键决策记录

**为开发者提供**:
- ✅ 任务进度可视化
- ✅ 关键决策可追溯
- ✅ 问题排查历史

---

## 快速开始

### 创建Workdoc

```bash
make workdoc_create TASK=implement-user-auth
```

这会在`ai/workdocs/active/implement-user-auth/`创建三个文件。

### 使用Workdoc

1. **编辑plan.md**: 制定实施计划
2. **持续更新context.md**: 每完成一个milestone就更新
3. **使用tasks.md**: 追踪任务状态

### 归档Workdoc

任务完成后：

```bash
make workdoc_archive TASK=implement-user-auth
```

---

## 三个核心文件详解

### 1. plan.md - 战略计划

**用途**: 任务的总体规划

**核心章节**:
- **执行摘要**: 目标、范围
- **当前状态分析**: 现状、问题
- **实施阶段**: Phase划分、任务清单
- **风险管理**: 风险识别和缓解
- **成功指标**: 可验证的指标
- **时间线**: 时间规划

**何时编写**: 任务开始前

**何时更新**: 计划调整时（较少更新）

**示例**: 参考`doc/templates/workdoc-plan.md`

---

### 2. context.md - 关键上下文⭐

**用途**: 上下文恢复和进度追踪（**最重要的文件**）

**核心章节**:

#### ⚡ SESSION PROGRESS（最关键）
记录所有任务的执行状态：
- **✅ COMPLETED**: 已完成的任务（带时间戳、文件、提交）
- **🟡 IN PROGRESS**: 进行中的任务（进度、下一步）
- **⏳ PENDING**: 待处理的任务
- **⚠️ BLOCKERS**: 阻塞项

#### 📁 关键文件
每个涉及的文件的状态、职责、关键函数

#### 🎯 关键决策
所有重要决策的记录（日期、决策、原因、影响）

#### ⚠️ 错误记录
所有犯过的错误（避免AI重复）

#### 🚀 Quick Resume
快速恢复指令（阅读顺序、当前状态、下一步）

**何时编写**: 任务开始时

**何时更新**: **每完成一个milestone**（频繁更新）

**示例**: 参考`doc/templates/workdoc-context.md`

**⚠️ 重要**: 这是AI恢复上下文的首选文件，**必须保持更新**！

---

### 3. tasks.md - 任务清单

**用途**: 详细的任务列表

**核心章节**:
- **任务总览**: 表格统计进度
- **Phase X**: 按Phase组织任务
- **Task X.X**: 每个任务的详细信息
  - 描述
  - 验收标准
  - 涉及文件
  - 依赖
  - 风险
  - 测试
- **阻塞任务**: 被阻塞的任务列表
- **风险任务**: 高风险任务列表
- **任务依赖图**: 可视化依赖关系

**何时编写**: 任务开始时

**何时更新**: 任务状态变化时

**示例**: 参考`doc/templates/workdoc-tasks.md`

---

## 完整工作流

### 阶段1: 任务开始

```bash
# 1. 创建workdoc
make workdoc_create TASK=my-feature

# 2. 进入目录
cd ai/workdocs/active/my-feature

# 3. 编辑plan.md制定计划
#    - 填写目标和范围
#    - 定义实施阶段
#    - 识别风险

# 4. 初始化context.md
#    - 填写当前状态分析
#    - 列出关键文件
#    - 设置Quick Resume

# 5. 初始化tasks.md
#    - 列出所有任务
#    - 定义验收标准
#    - 标记依赖关系
```

---

### 阶段2: 任务执行

**每完成一个milestone**，更新`context.md`:

1. **更新SESSION PROGRESS**
   ```markdown
   ### ✅ COMPLETED
   
   #### ✅ [2025-11-08 14:30] Task 1.1: 实现用户注册API
   - 文件: modules/user/api/routes.py
   - 提交: commit abc123
   - 说明: 添加POST /users/接口，支持username和email注册
   - 验证: 单元测试通过，集成测试通过
   ```

2. **更新关键文件状态**
   ```markdown
   ### modules/user/api/routes.py
   - 职责: 用户API路由
   - 状态: ✅ 完成
   - 关键函数:
     - create_user(): POST /users/，已实现验证逻辑
   ```

3. **记录关键决策**（如有）
   ```markdown
   ### Decision 1: 使用JWT而非Session
   - 日期: 2025-11-08
   - 决策: 使用JWT token进行认证
   - 原因: 无状态，便于水平扩展
   - 影响: 需要实现token刷新机制
   ```

4. **记录错误**（如有）
   ```markdown
   ### ERROR-001: 忘记验证email格式
   - 日期: 2025-11-08
   - 错误: 创建用户时未验证email格式
   - 后果: 允许插入无效email
   - 教训: 使用Pydantic的EmailStr类型
   - ⚠️ AI注意: 所有email字段必须使用EmailStr类型
   ```

5. **更新Quick Resume**
   ```markdown
   ### 2. 当前状态一句话
   已完成用户注册API（Task 1.1），正在实现JWT token生成逻辑（Task 1.2，70%）。
   文件：modules/user/core/jwt.py，待添加过期时间验证。
   
   ### 3. 下一步行动
   1. 在jwt.py添加token过期验证
   2. 编写unit test
   3. 更新context.md标记Task 1.2完成
   ```

**同时更新`tasks.md`**:
- 标记已完成任务为✅
- 更新进行中任务的进度
- 更新任务总览表格

---

### 阶段3: 任务完成

```bash
# 1. 最终验证
make validate

# 2. 更新文档
#    - README.md
#    - CHANGELOG.md
#    - 相关指南

# 3. 在context.md标记所有任务为✅

# 4. 归档workdoc
make workdoc_archive TASK=my-feature
```

---

## AI使用规范

### 任务开始时（必须做）

✅ **创建workdoc**
```bash
make workdoc_create TASK=<task-name>
```

✅ **编辑plan.md**
- 填写目标和范围
- 定义实施阶段
- 识别风险

✅ **初始化context.md**
- 填写当前状态
- 列出将要修改的关键文件

---

### 任务执行中（必须做）

✅ **每完成一个milestone，立即更新context.md**

必须更新的部分：
1. SESSION PROGRESS - 移动任务状态
2. 关键文件 - 更新文件状态
3. Quick Resume - 更新当前状态和下一步

可选更新的部分：
- 关键决策 - 如有重要决策
- 错误记录 - 如犯了错误

⚠️ **重要**: 不要等到任务全部完成才更新，要**持续更新**！

---

### 遇到错误时（强烈建议）

✅ **立即记录到context.md的错误记录**

```markdown
### ERROR-XXX: [错误标题]
- 日期: YYYY-MM-DD
- 错误: [具体做错了什么]
- 后果: [导致什么问题]
- 教训: [应该怎么做]
- ⚠️ AI注意: [警告AI不要重复]
```

**为什么重要**: 避免AI在后续开发中重复同样的错误。

---

### 上下文切换时（必须做）

如果会话中断或需要切换到其他任务：

✅ **更新context.md的Quick Resume**

```markdown
## 🚀 Quick Resume

### 2. 当前状态一句话
[一句话总结进度]

### 3. 下一步行动
1. [具体步骤1]
2. [具体步骤2]

### 4. 注意事项
- ⚠️ [重要提醒]
```

**新会话恢复时**:
1. 先读取`context.md`的Quick Resume
2. 再读取SESSION PROGRESS了解详细进度
3. 参考plan.md了解整体计划
4. 查看tasks.md了解任务清单

---

### 任务完成时（必须做）

✅ **归档workdoc**
```bash
make workdoc_archive TASK=<task-name>
```

✅ **确保context.md完整**
- 所有任务标记为✅
- 记录最终统计
- 记录经验教训

---

## 最佳实践

### DO ✅

**context.md管理**:
- ✅ 每完成一个任务立即更新SESSION PROGRESS
- ✅ 记录所有关键决策（避免遗忘）
- ✅ 记录所有错误（避免重复）
- ✅ 保持Quick Resume实时更新
- ✅ 使用时间戳标记每个完成项

**文件状态管理**:
- ✅ 详细记录每个关键文件的状态
- ✅ 标记文件的进度百分比
- ✅ 说明文件的下一步操作

**错误记录**:
- ✅ 每个错误都要记录
- ✅ 明确标记"⚠️ AI注意"
- ✅ 说明教训和正确做法

### DON'T ❌

- ❌ 不要等任务全部完成才更新context.md
- ❌ 不要忘记记录错误
- ❌ 不要忘记记录关键决策
- ❌ 不要在归档前留下TODO
- ❌ 不要在多个任务间共享workdoc

---

## 与其他机制的区别

### ai/workdocs/ vs ai/sessions/

| 维度 | ai/sessions/ | ai/workdocs/ |
|------|-------------|-------------|
| **组织方式** | 按日期+会话名 | 按任务名 |
| **主要文件** | AI-SR-plan.md, AI-SR-impl.md | plan.md, context.md, tasks.md |
| **上下文恢复** | 需要阅读多个文件 | context.md即可快速恢复 |
| **更新频率** | 会话结束后一次性 | 持续更新 |
| **任务追踪** | 无结构化追踪 | SESSION PROGRESS结构化追踪 |
| **错误记录** | 散落在文本中 | 专门章节记录 |
| **决策记录** | 无专门记录 | 关键决策章节 |

**使用建议**:
- 保留`sessions/`用于会话历史存档
- 使用`workdocs/`用于活跃任务管理
- 两者互补，不冲突

---

### ai/workdocs/ vs modules/.context/

| 维度 | modules/.context/ | ai/workdocs/ |
|------|------------------|-------------|
| **范围** | 单个模块的长期上下文 | 单个任务的开发上下文 |
| **时间跨度** | 长期（模块生命周期） | 短期（任务周期） |
| **更新频率** | 重大变更时 | 持续更新 |
| **主要用途** | 模块概览和快速理解 | 任务进度和上下文恢复 |

**使用建议**:
- 模块级上下文 → 使用`.context/context.md`
- 任务级上下文 → 使用`workdocs/*/context.md`

---

## 常见场景

### 场景1: 实现新功能

```bash
# 1. 创建workdoc
make workdoc_create TASK=add-payment-feature

# 2. 编辑plan.md
#    定义3个Phase，6个任务

# 3. 开始开发
#    每完成一个任务，更新context.md的SESSION PROGRESS

# 4. 完成后归档
make workdoc_archive TASK=add-payment-feature
```

---

### 场景2: 修复Bug

```bash
# 1. 创建workdoc
make workdoc_create TASK=fix-bug-123

# 2. 在plan.md记录
#    - Bug描述
#    - 根因分析
#    - 修复方案

# 3. 在context.md记录
#    - 关键文件（哪些文件需要修改）
#    - 修复过程（每个步骤）
#    - 如果修复过程中犯错，记录到ERROR记录

# 4. 完成后归档
make workdoc_archive TASK=fix-bug-123
```

---

### 场景3: 重构代码

```bash
# 1. 创建workdoc
make workdoc_create TASK=refactor-auth-module

# 2. 在plan.md说明
#    - 为什么重构
#    - 重构策略（大爆炸 vs 渐进式）
#    - 风险评估

# 3. 在context.md记录
#    - 重构的关键决策（如选择新的架构模式）
#    - 文件迁移清单
#    - 测试策略

# 4. 完成后归档
```

---

### 场景4: 上下文恢复

**情况**: AI会话中断，需要恢复任务

```bash
# 1. 列出active任务
make workdoc_list

# 2. 快速恢复
#    阅读 ai/workdocs/active/<task>/context.md
#    重点看：
#    - SESSION PROGRESS（了解进度）
#    - Quick Resume（了解下一步）
#    - 关键文件（了解涉及哪些文件）

# 3. 继续开发
#    根据Quick Resume的下一步行动继续
```

**AI恢复流程**:
1. 读取`context.md`的Quick Resume（30秒）
2. 读取SESSION PROGRESS了解详细进度（2分钟）
3. 如需要，读取plan.md了解整体计划（5分钟）
4. 开始工作

---

## 命令参考

### 创建workdoc
```bash
make workdoc_create TASK=<task-name>
```

**参数**:
- TASK: 任务名称（小写字母+连字符）

**示例**:
```bash
make workdoc_create TASK=implement-user-auth
make workdoc_create TASK=fix-bug-123
make workdoc_create TASK=refactor-db-layer
```

---

### 归档workdoc
```bash
make workdoc_archive TASK=<task-name>
```

**参数**:
- TASK: 要归档的任务名称

**示例**:
```bash
make workdoc_archive TASK=implement-user-auth
```

---

### 列出workdocs
```bash
make workdoc_list
```

**输出**:
```
📋 Active Workdocs:
  implement-user-auth
  fix-bug-123

📦 Archived Workdocs:
  refactor-db-layer
  add-payment-feature
```

---

## 常见问题

### Q1: 一定要使用workdocs吗？
**A**: 对于复杂任务，强烈建议使用。对于简单任务（如修复typo），可以不使用。

**判断标准**:
- 任务需要2小时以上 → 建议使用
- 涉及3个以上文件 → 建议使用
- 可能需要多个会话完成 → 必须使用

### Q2: context.md多久更新一次？
**A**: 每完成一个milestone就更新。建议：
- 完成一个任务 → 立即更新
- 做出关键决策 → 立即更新
- 犯了错误 → 立即更新
- 结束会话前 → 更新Quick Resume

### Q3: plan.md需要很详细吗？
**A**: 适度详细即可：
- 明确目标和范围
- Phase划分清晰
- 风险识别到位
- 不需要写每一行代码的计划

### Q4: tasks.md和context.md的SESSION PROGRESS有什么区别？
**A**: 
- **tasks.md**: 静态任务列表（任务定义、验收标准）
- **context.md SESSION PROGRESS**: 动态执行状态（已完成、进行中、待处理）

两者互补，tasks.md是"计划"，SESSION PROGRESS是"实际进度"。

### Q5: 归档后还能访问吗？
**A**: 可以。归档只是移动到archive/目录，文件仍然存在。

### Q6: 如何恢复归档的任务？
**A**: 手动移回active/目录：
```bash
mv ai/workdocs/archive/<task> ai/workdocs/active/
```

### Q7: 可以在workdoc中放代码吗？
**A**: 不要。workdoc只存放：
- 计划和上下文
- 代码片段的引用（文件路径+函数名）
- 关键代码片段的说明（不超过20行）

---

## 示例Workdoc

查看实际示例（待创建）：
- `ai/workdocs/active/example-task/`

---

## 工具和集成

### 与智能触发系统集成

workdocs可以与agent-triggers.yaml集成：

```yaml
triggers:
  - id: workdoc-context-required
    name: "Workdoc上下文需求"
    pattern:
      file_glob: ["ai/workdocs/active/**/context.md"]
    action:
      type: suggest
      message: "检测到workdoc，建议先阅读context.md恢复上下文"
      documents:
        - path: "{matched_dir}/context.md"
          priority: critical
```

### 与CI集成（可选）

可以添加CI检查：
- 检查active/中的workdoc是否更新（避免遗忘）
- 检查归档的workdoc是否完整

---

## 相关资源

- **模板文件**: `doc/templates/workdoc-*.md`
- **管理脚本**: `scripts/workdoc_*.sh`
- **workdocs目录**: `ai/workdocs/`
- **AI LEDGER**: `ai/LEDGER.md`

---

## 版本历史

- **1.0** (2025-11-08): 创建workdocs机制

