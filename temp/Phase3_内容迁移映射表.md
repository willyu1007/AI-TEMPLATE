# Phase 3 - 根agent.md内容迁移映射表

> **当前行数**: 2434行
> **目标行数**: ≤500行
> **需精简**: 约1934行 (79%)

---

## 章节分析与迁移计划

### 保留在根agent.md的内容（精简版）

| 章节 | 当前行数 | 目标行数 | 操作 |
|------|----------|----------|------|
| 标题与重要提醒 | 24 | 20 | 精简 |
| § 0 快速开始 | 48 | 80 | 保留并补充§1.3 |
| § 1 目录规范 | 268 | 100 | 精简，仅保留关键目录 |
| § 3 记忆机制 | 10 | 30 | 保留并补充文档路由 |
| § 10 提示词清单 | 50 | 50 | 保留 |
| § 12 命令速查 | 22 | 50 | 保留并补充Phase 1-2命令 |
| § 13 文档规范 | 43 | 70 | 保留核心规范 |
| YAML Front Matter | 0 | 50 | 新增 |
| § 1.3 应用层职责 | 0 | 50 | 新增 |
| **合计** | **465** | **500** | |

---

### 需要迁移的内容

#### 1. § 2 角色与门禁 (7行)
**迁移目标**: `doc/policies/roles.md`（新建）
**内容**: 角色定义、权限范围

---

#### 2. § 4 DAG与接口契约 (98行)
**迁移目标**: 拆分到多个文件
- `doc/orchestration/dag.md` - DAG规范和验证
- `doc/process/contract.md` - 契约管理规范
**内容**: DAG定义、契约兼容性、验证规则

---

#### 3. § 5 模块化开发流程 (465行)
**迁移目标**: 已有相关文档，只需引用
- 引用: `doc/modules/MODULE_INIT_GUIDE.md`
- 引用: `doc/init/PROJECT_INIT_GUIDE.md`
**内容**: 模块创建、文档结构、最佳实践

---

#### 4. § 6 测试准则 (337行)
**迁移目标**: `doc/process/testing.md`（新建）
**内容**: 测试策略、覆盖率要求、多语言测试

---

#### 5. § 7 数据库规范 (8行)
**迁移目标**: `db/engines/README.md`（新建）
**内容**: 数据库操作规范、迁移流程

---

#### 6. § 8 统一配置 (20行)
**迁移目标**: `config/README.md`（已有，补充）
**内容**: 配置规范、环境区分

---

#### 7. § 9 UX流程 (37行)
**迁移目标**: `docs/ux/UX_GUIDE.md`（已有，补充）
**内容**: UX规范、流程设计

---

#### 8. § 11 代码审查 (571行)
**迁移目标**: `doc/process/code_review.md`（新建）
**内容**: 审查流程、检查清单、多语言审查

---

#### 9. § 13.0 临时文件管理 (128行)
**迁移目标**: `doc/process/temp_files.md`（新建）
**内容**: 临时文件规范、清理机制

---

## 迁移执行顺序

### Phase 1: 创建新文档（迁移内容）
1. `doc/policies/roles.md` - 角色与门禁
2. `doc/orchestration/dag.md` - DAG规范
3. `doc/process/contract.md` - 契约管理
4. `doc/process/testing.md` - 测试准则
5. `doc/process/code_review.md` - 代码审查
6. `doc/process/temp_files.md` - 临时文件
7. `db/engines/README.md` - 数据库规范

### Phase 2: 补充现有文档
8. `config/README.md` - 补充配置规范
9. `docs/ux/UX_GUIDE.md` - 补充UX流程

### Phase 3: 重写根agent.md
10. 添加YAML Front Matter
11. 精简§0-§1，添加§1.3
12. 精简§3、§10、§12、§13
13. 替换已迁移章节为引用链接
14. 验证行数≤500

### Phase 4: 目录改名
15. docs/ → doc/（合并）
16. flows/ → doc/flows/（移动）

### Phase 5: 更新引用
17. 根README.md添加声明
18. 更新所有文档中的路径引用

---

## 预期成果

### 根agent.md（≤500行）
```markdown
---
spec_version: "1.0"
agent_id: "repo"
role: "AI-TEMPLATE根编排配置"
...
---

# agent.md

> 本规程面向让模型高效工作...

## 0. 快速开始
（保留S0-S6流程，~80行）

### 1.3 应用层与模块层职责边界
（新增，~50行）

## 1. 目录规范
（精简，仅保留关键目录，~100行）

## 2. 文档路由与上下文
（保留§3，改名，~30行）

## 3. 提示词与清单
（保留§10，改名，~50行）

## 4. 命令速查
（保留§12，改名，~50行）

## 5. 文档规范
（保留§13.1，改名，~70行）

## 6. 更多信息
- 角色与门禁: doc/policies/roles.md
- DAG规范: doc/orchestration/dag.md
- 契约管理: doc/process/contract.md
- 测试准则: doc/process/testing.md
- 代码审查: doc/process/code_review.md
- 临时文件: doc/process/temp_files.md
- 模块初始化: doc/modules/MODULE_INIT_GUIDE.md
- 项目初始化: doc/init/PROJECT_INIT_GUIDE.md
...
```

---

## 验收标准

- [ ] 根agent.md ≤ 500行
- [ ] 所有迁移的文档已创建
- [ ] docs/ 已改名并合并到doc/
- [ ] flows/ 已移动到doc/flows/
- [ ] `make agent_lint` 通过
- [ ] 所有路径引用已更新
- [ ] README.md添加了声明

---

**执行开始时间**: 2025-11-07

