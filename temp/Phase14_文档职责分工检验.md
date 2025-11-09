# 文档职责分工与引导完整性检验

> **检验日期**: 2025-11-09  
> **检验范围**: 文档职责、agent.md引导、模块初始化流程

---

## 检验问题

1. **文档是否有明确的阅读职责分工说明**（AI文档 vs 人类文档）
2. **agent.md是否有必要的引导**（如AI文档使用英文）
3. **模块初始化流程是否引导生成正确的agent.md**

---

## 1. 文档职责分工检验

### 1.1 AI文档 vs 人类文档分类

**AI文档（已创建）**:
| 文档 | 行数 | 语言 | 用途 | 标识 |
|------|------|------|------|------|
| doc/policies/AI_INDEX.md | 100 | 英文 | 超轻量总索引 | ✅ 有"For AI Agents" |
| doc/process/dataflow-quickstart.md | 100 | 英文 | 数据流快速参考 | ✅ 有"For AI Agents" |
| doc/process/guardrail-quickstart.md | 120 | 英文 | 防护机制快速参考 | ✅ 有"For AI Agents" |
| doc/process/workdocs-quickstart.md | 100 | 英文 | 任务管理快速参考 | ✅ 有"For AI Agents" |
| config/AI_GUIDE.md | 80 | 英文 | 配置管理快速参考 | ✅ 有"For AI Agents" |
| doc/process/AI_CODING_GUIDE.md | 150 | 英文 | AI编码规范 | ✅ 文件名标识 |
| ai/workflow-patterns/README.md | 150 | 英文 | 工作流模式目录 | ⚠️ 无明确标识 |
| doc/templates/dataflow-summary.md | 86 | 英文 | 数据流模板 | ⚠️ 无明确标识 |

**人类文档（完整版）**:
| 文档 | 行数 | 语言 | 用途 |
|------|------|------|------|
| doc/process/DATAFLOW_ANALYSIS_GUIDE.md | 519 | 中文 | 数据流完整指南 |
| doc/process/GUARDRAIL_GUIDE.md | 782 | 中文 | Guardrail完整指南 |
| doc/process/WORKDOCS_GUIDE.md | 653 | 中文 | Workdocs完整指南 |
| doc/process/CONFIG_GUIDE.md | - | 中文 | 配置管理完整指南 |
| doc/process/CONVENTIONS.md | 611 | 中文 | 开发规范完整版 |
| ai/workflow-patterns/PATTERNS_GUIDE.md | 400 | 中文 | 工作流模式人类指南 |

### 1.2 问题发现

**缺失职责标识**:
- ⚠️ ai/workflow-patterns/README.md: 无"For AI Agents"标识
- ⚠️ doc/templates/dataflow-summary.md: 无"For AI Agents"标识
- ⚠️ 其他AI文档: 部分缺少明确标识

**缺少职责说明文档**:
- ❌ 无统一的文档职责分工说明（哪些给AI，哪些给人类）
- ❌ AI在选择文档时可能不清楚应该读哪个版本

**建议**: 创建 `doc/policies/DOC_ROLES.md` 统一说明

---

## 2. agent.md引导完整性检验

### 2.1 当前agent.md的引导

**已有引导**:
```markdown
## 3. Documentation Standards

### Language Rules
**Language Consistency**: Single language per document
**AI Documents**: English preferred for better AI parsing
**Human Documents**: Chinese or English based on team preference
**Code Comments**: Follow team language standards
```

**问题**:
- ✅ 有语言一致性要求
- ✅ 说明AI文档用英文
- ⚠️ 但没有说明"哪些是AI文档"
- ⚠️ 没有说明"AI应该优先读quickstart还是完整版"

### 2.2 缺失的引导

**应该添加的引导**:

1. **文档选择引导** (§ 1.1)
```markdown
## 1.1 Document Selection Guide

When loading on-demand documents:

1. **AI Documents (Quickstart)**: Load first for quick tasks
   - Identified by: "For AI Agents" in header
   - Format: English, ~100 lines, command-focused
   - Location: *-quickstart.md, AI_*.md
   - Examples: dataflow-quickstart.md, AI_CODING_GUIDE.md

2. **Human Documents (Complete)**: Load for deep understanding
   - Format: Chinese/English, 300-800 lines, detailed examples
   - Location: Full guides (*_GUIDE.md)
   - Examples: DATAFLOW_ANALYSIS_GUIDE.md, CONVENTIONS.md

3. **Loading Priority**:
   - For operations: Load AI quickstart only
   - For learning: Load human complete guide
   - When unsure: Check priority field in context_routes
```

2. **AI文件编写规范** (§ 3.1)
```markdown
## 3.1 AI Document Writing Standards

When creating AI-facing documents:

1. **Language**: English only (better parsing)
2. **Header**: Must include "> **For AI Agents** - Purpose"
3. **Length**: ≤150 lines (keep focused)
4. **Format**: Commands first, concepts second
5. **Examples**: Runnable code snippets
6. **Cross-Reference**: Link to human doc for details

When creating human-facing documents:
1. **Language**: Chinese or English (team choice)
2. **Length**: No limit (be comprehensive)
3. **Format**: Concepts first, examples second
4. **Details**: Full explanations, edge cases, troubleshooting
```

3. **Context Loading Rules** (§ 0.1)
```markdown
### S0.1 - Context Loading Rules

**Critical**: DO NOT auto-load referenced documents

1. **always_read**: Load ONLY AI_INDEX.md
   - DO NOT follow "See also" references
   - DO NOT auto-load goals.md, safety.md
   - Those are on-demand documents

2. **on_demand**: Load based on task type
   - Check context_routes for topic
   - Load based on priority field
   - Prefer *-quickstart.md over *_GUIDE.md

3. **Depth Limit**: Maximum 1 level
   - Load explicitly listed documents only
   - Do not recursively follow references
```

---

## 3. 模块初始化流程检验

### 3.1 当前初始化流程

**命令**: `make ai_begin MODULE=<name>`

**生成文件** (检查 scripts/ai_begin.sh):
- modules/<name>/README.md
- modules/<name>/plan.md
- modules/<name>/doc/ (6个文档)
- tests/<name>/

**问题**: 是否生成 `modules/<name>/agent.md`？

### 3.2 检查ai_begin.sh

需要验证：
- [ ] 是否生成agent.md
- [ ] 生成的agent.md是否符合根agent.md要求
- [ ] 是否包含必需字段（module_type, io, etc.）
- [ ] 是否有英文引导

### 3.3 检查MODULE_INIT_GUIDE.md

需要验证：
- [ ] 是否说明agent.md是必需的
- [ ] 是否提供agent.md模板
- [ ] 是否说明必需字段
- [ ] 是否说明AI文档用英文

---

## 检验结论

### 发现的问题

**P0 - 高优先级**:
1. ❌ agent.md缺少"文档选择引导"（§ 1.1）
2. ❌ agent.md缺少"上下文加载规则"（§ 0.1，防止自动深入）
3. ❌ 缺少统一的文档职责分工说明文档

**P1 - 中优先级**:
4. ⚠️ agent.md的§ 3只有简单的语言规则，缺少AI文档编写规范
5. ⚠️ 部分AI文档缺少"For AI Agents"标识
6. ⚠️ 需要检验ai_begin.sh是否正确生成agent.md

**P2 - 低优先级**:
7. 💡 建议创建DOC_ROLES.md统一说明文档职责

---

## 推荐修复方案

### Phase 14.0补充（立即执行）

1. **扩展AI_INDEX.md** (30→100行)
   - ✅ 已完成：自包含核心Goals和Safety
   - 包含明确的"DO NOT auto-load"警告

2. **增强agent.md § 1.1** (新增)
   - 添加"Document Selection Guide"
   - 说明AI文档 vs 人类文档
   - 加载优先级规则

3. **增强agent.md § 0** (S0开头)
   - 添加"Context Loading Rules"
   - 明确"DO NOT follow references"
   - 深度限制（Maximum 1 level）

4. **增强agent.md § 3** (文档规范)
   - 添加"AI Document Writing Standards"
   - 必须英文、必须标识、长度限制

5. **创建DOC_ROLES.md** (可选)
   - 统一的文档职责分工说明
   - AI文档清单 vs 人类文档清单

6. **检验ai_begin.sh** (必须)
   - 确保生成agent.md
   - 确保包含必需字段
   - 确保符合规范

---

**预估时间**: 1-1.5小时  
**收益**: 确保AI友好度优化真实有效，防止Token成本隐性增加

