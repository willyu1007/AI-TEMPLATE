# always_read Token成本深度分析

> **分析日期**: 2025-11-09  
> **问题**: always_read不能只看入口文件，需要深入一层分析实际Token成本

---

## 问题说明

**用户发现**: AI_INDEX.md只有30行，但它引用了其他文档（goals.md, safety.md等），AI阅读时会"向下深入一层"，实际Token成本远高于30行。

**这是正确的观察！** ⭐

---

## 当前always_read配置

```yaml
context_routes:
  always_read:
    - /doc/policies/AI_INDEX.md  # 30行
```

---

## 深度分析：AI_INDEX.md引用了什么？

### AI_INDEX.md内容结构

```markdown
# AI Index - Quick Reference (~30 lines)

## Core Goals (4)
- Reference: See goals.md

## Safety Constraints (5)
| Constraint | Details |
| Path Access | security_details.md § 1 |
| Tool Calls | security_details.md § 2 |
| DB Changes | safety.md § 2 |
| Contract Breaking | safety.md § 3 |
| Production Config | safety.md § 4 |

## Key Workflows (6)
- Module Creation → MODULE_INIT_GUIDE.md
- Database Change → DB_CHANGE_GUIDE.md
- ...

## See Also
- goals.md (full goals)
- safety.md (full safety rules)
- agent.md (complete workflow)
```

### AI阅读行为分析

**情况A: AI只读AI_INDEX.md** (理想情况)
- 行数: 30行
- Token: ~39 tokens
- **这是我们Phase 14.0的假设**

**情况B: AI深入阅读引用文档** (实际情况)
- AI_INDEX.md: 30行
- AI看到"See goals.md" → 可能加载goals.md: 172行
- AI看到"See safety.md" → 可能加载safety.md: 234行
- AI看到"See security_details.md" → 可能加载: 537行
- **实际Token**: 30 + 172 + 234 + 537 = **973行** ⚠️

**结论**: 如果AI自动深入一层，Token节省从-95.7%变为**仅-40%** ！

---

## 实际Token成本计算

### v2.3 (Phase 14.0之前)

```yaml
always_read:
  - /doc/policies/goals.md        # 172行
  - /doc/policies/safety.md       # 234行
  - /README.md                     # 287行

Total: 693行 ≈ 900 tokens
```

### v2.4 (Phase 14.0 - 乐观估算)

```yaml
always_read:
  - /doc/policies/AI_INDEX.md     # 30行

Total: 30行 ≈ 39 tokens
节省: -95.7% ✅
```

### v2.4 (Phase 14.0 - 悲观估算)

```yaml
always_read:
  - /doc/policies/AI_INDEX.md     # 30行

AI可能自动深入读取:
  - goals.md (引用)                # 172行
  - safety.md (引用)               # 234行
  - security_details.md (表格引用) # 537行
  - quality_standards.md (表格引用) # 402行

Total: 30 + 172 + 234 + 537 + 402 = 1,375行 ≈ 1,787 tokens
节省: -98% → +98% ❌ (更差了！)
```

---

## 解决方案

### 方案A: 彻底的AI_INDEX.md (自包含) ⭐ 推荐

**理念**: AI_INDEX.md应该是**完全自包含**的快速参考，不依赖"深入阅读"

**优化AI_INDEX.md**:
```markdown
# AI Index - Complete Quick Reference

> **For AI Agents** - Self-contained reference (~100 lines)  
> **No need to read other docs** - All essentials here  
> **Full details**: Load on-demand via context_routes

## Core Goals (Complete List)
1. AI-Friendly
   - Parseable docs (YAML + Markdown)
   - Clear routes (context_routes in agent.md)
   - Controlled context (load on-demand)
   - Auto-discovery (registry.yaml for modules)

2. Modular
   - Interchangeable (same type = replaceable)
   - Independent (modules can be developed separately)
   - Stable I/O (CONTRACT.md defines interfaces)
   - Clear dependencies (upstream/downstream in agent.md)

3. Automated
   - Verifiable (16+ automated checks in make dev_check)
   - Scriptable (85+ make commands)
   - CI-ready (GitHub Actions integration)
   - Semi-automated (registry, DB ops need human review)

4. Orchestrable
   - Auto-discovery (modules/*/agent.md)
   - Document routing (context_routes)
   - Intelligent triggers (agent-triggers.yaml)
   - Task scheduling (workflow patterns)

## Safety Constraints (Complete List)

### Path Access Control
- ✅ Read: context_routes + current module + public docs
- ✅ Write: ownership.code_paths only
- ❌ Forbidden: undeclared paths

### Database Operations
- ✅ Semi-automated: AI generates → human reviews → human executes
- ❌ No direct DDL: AI cannot execute CREATE/ALTER/DROP
- ✅ Migration paired: Every up.sql must have down.sql
- ✅ Rollback ready: Test rollback locally before merge

### Contract Changes
- ⚠️ Breaking change detection: Check .contracts_baseline/
- ⚠️ Baseline update required: Run make update_baselines
- ❌ Remove field: Blocked, use @deprecated first
- ❌ Change type: Blocked, add migration guide

### Production Config
- 🔴 Blocked: Direct edit of config/prod.yaml
- ✅ Required: Change request + approval + rollback plan
- ✅ Alternative: Use environment variables

### Tool Calls
- ✅ Whitelist: tools_allowed in agent.md
- ❌ Default deny: Unlisted tools blocked

## Quality Requirements (Complete List)

- Test coverage ≥80%
- 6 standard docs per module (README, CONTRACT, TEST_PLAN, RUNBOOK, CHANGELOG, BUGS/PROGRESS)
- Backward compatibility maintained
- Code follows CONVENTIONS.md or AI_CODING_GUIDE.md
- CI gate must pass (make dev_check)

## Essential Workflows

### Create Module
```bash
make ai_begin MODULE=<name>
# Generates: agent.md, README.md, doc/, tests/
# Auto-registers to registry.yaml (draft)
```

### Database Change
```bash
# 1. Check DB_CHANGE_GUIDE.md (on-demand)
# 2. Create paired migrations (up/down)
# 3. Update schema YAML
# 4. Test rollback: make rollback_check
```

### Update Contract
```bash
# 1. Check compatibility: make contract_compat_check
# 2. Update CONTRACT.md
# 3. Update baseline: make update_baselines
# 4. Provide migration guide if breaking
```

## Document Loading Strategy

- **Always**: AI_INDEX.md only (this file)
- **On-Demand**: 19 topics in agent.md (load as task requires)
- **Module-Specific**: modules/*/agent.md (load when working in module)

**Priority Loading**:
- High priority: Goals, safety, module dev, workflows
- Medium priority: Database, config, testing, triggers
- Low priority: Directory structure, routing usage, conventions

---

**行数**: ~100行 (vs 30行)
**Token**: ~130 tokens (vs 39 tokens)
**深度**: 0层 (自包含，不引用外部)
```

**优点**:
- ✅ 完全自包含，无需深入阅读
- ✅ Token成本可控（130 vs 1,787）
- ✅ AI加载后立即可用

**缺点**:
- ⚠️ 从30行增加到100行（仍比693行少86%）
- ⚠️ 需要维护同步（但更可控）

**节省**: 693行 → 100行 = **-85.6%** (仍超额完成-84%目标)

### 方案B: 明确引导AI不要深入 (引导策略)

**在AI_INDEX.md中明确说明**:
```markdown
> **For AI Agents** - Essential context (30 lines)  
> **⚠️ DO NOT auto-load referenced docs** - Load on-demand only  
> **Full Details**: Load via context_routes when needed
```

**在agent.md中添加规则**:
```markdown
## Document Loading Rules

1. **always_read**: Load ONLY the listed files, do NOT follow references
2. **on_demand**: Load based on task type (consult context_routes)
3. **Deep dive**: Only when explicitly needed for task
```

**优点**:
- ✅ 保持AI_INDEX.md简短（30行）
- ✅ 明确引导AI行为

**缺点**:
- ⚠️ 依赖AI遵守引导（不保证100%）
- ⚠️ 不同AI实现可能行为不同

### 方案C: 混合方案 (推荐) ⭐

**AI_INDEX.md扩展到80-100行**:
- 包含最关键的Goals和Safety摘要（自包含）
- 明确标注"Full details: on-demand"
- 引导AI不要自动深入

**内容**:
- Core Goals (4个，展开1-2句话) - 20行
- Safety Constraints (5个，核心原则) - 20行
- Quality Requirements (5个) - 15行
- Essential Workflows (6个，命令+简述) - 25行
- Document Loading Strategy - 10行
- **Total**: ~90行

**优点**:
- ✅ 自包含核心信息
- ✅ Token可控（~117 tokens）
- ✅ 节省仍显著（-83%）
- ✅ 明确引导AI行为

---

## 推荐行动

### 立即执行

1. **扩展AI_INDEX.md**: 30行 → 90行（自包含核心Goals和Safety）
2. **添加加载规则**: 在agent.md § 1明确"不要自动深入"
3. **重新测算**: 实际Token成本

### 验证方法

测试AI实际加载行为:
1. 启动新AI会话
2. 观察AI是否只读AI_INDEX.md
3. 还是自动深入读取goals.md等
4. 根据实际行为调整策略

---

**结论**: 用户观察正确！需要扩展AI_INDEX.md为自包含文档（80-100行），确保Token节省真实有效。

