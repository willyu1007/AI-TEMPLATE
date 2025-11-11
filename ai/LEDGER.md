# AI Task Registry (LEDGER)

> **Purpose**: High-level index of all AI-participated tasks  
> **Audience**: AI agents (quick reference) + Human operators (historical tracking)  
> **Role**: Registry only - NOT for detailed progress tracking

---

## 🎯 What is LEDGER?

**LEDGER is a lightweight task registry** that provides:
- ✅ Chronological list of tasks
- ✅ Quick task metadata (type, module, date)
- ✅ Pointers to detailed documentation
- ✅ High-level outcomes and learnings

**LEDGER is NOT**:
- ❌ Detailed progress tracking → Use `workdocs/active/<task>/context.md`
- ❌ Session transcripts → Use `sessions/<date>_<name>/`
- ❌ Module history → Use `modules/<name>/PROGRESS.md`
- ❌ Code changes log → Use `modules/<name>/CHANGELOG.md`

---

## 📋 When to Use LEDGER

### For AI Agents

**Use LEDGER when**:
- 🔍 Looking for similar past tasks
- 🔍 Understanding project evolution
- 🔍 Finding related session records
- 🔍 Quick task overview (30 seconds)

**DON'T use LEDGER for**:
- ❌ Resuming interrupted tasks → Use `workdocs/active/<task>/context.md`
- ❌ Understanding implementation details → Use session docs or code
- ❌ Tracking current progress → Use `workdocs/` or module `plan.md`

### For Human Operators

**Use LEDGER when**:
- 📊 Reviewing project history
- 📊 Analyzing task patterns
- 📊 Generating reports
- 📊 Understanding AI contributions

---

## 📝 Entry Format

```markdown
### YYYY-MM-DD: <Brief Task Title>

**Metadata**:
- **Type**: feature | fix | refactor | docs | optimization | audit
- **Scope**: global | modules/<name> | doc/* | scripts/*
- **Complexity**: trivial | low | medium | high | critical
- **Duration**: <actual time spent>

**References**:
- **Workdoc**: `ai/workdocs/archive/<task-name>/` (if exists)
- **Sessions**: `ai/sessions/<date>_<name>/` (if exists)
- **Related Modules**: `modules/<name>/PROGRESS.md`

**Key Outcomes**:
- ✅ Outcome 1
- ✅ Outcome 2
- ⚠️ Known limitations or follow-ups

**Learnings**:
- 💡 Key insight or pattern discovered
- 💡 Best practice identified
```

---

## 🔀 Relationship with Other Mechanisms

| Document | Role | Granularity | Update Frequency |
|----------|------|-------------|------------------|
| **LEDGER.md** | Task registry | High-level (per task) | After task completion |
| **workdocs/** | Active task context | Detailed (per milestone) | Continuous during task |
| **sessions/** | AI self-review archive | Medium (per session) | One-time (AI-SR docs) |
| **modules/*/PROGRESS.md** | Module history | Medium (per module) | After module milestones |
| **modules/*/CHANGELOG.md** | Code changes | Detailed (per version) | With each release |
| **modules/*/plan.md** | Future plans | Detailed (next iteration) | Before changes |

### Clear Boundaries

```
Timeline: Past ←────────────────────────→ Future
         LEDGER  PROGRESS  CHANGELOG    plan.md
         (index) (history)  (versions)  (next)
         
Context: Active ←────────────────────────→ Archive
        workdocs/active/  workdocs/archive/  sessions/
        (current task)    (completed)        (historical)
```

---

## ✍️ Update Timing

### Required Updates

**When**: After completing any AI-participated task

**Who**: AI agent or human operator

**What**: Add single entry with:
- Date
- Brief title
- Metadata (type, scope, complexity, duration)
- References (workdoc, sessions, modules)
- Key outcomes
- Learnings

### Optional Updates

**When**: Discovering related historical context

**Who**: Usually human operator

**What**: Add cross-references or notes to existing entries

---

## 📊 Task Statistics

Track high-level metrics:

```markdown
## Monthly Summary

| Month | Total Tasks | By Type | By Complexity |
|-------|-------------|---------|---------------|
| 2025-11 | 5 | docs:2, feature:2, fix:1 | low:3, medium:2 |
```

---

## 🔍 Usage Examples

### Example 1: Find Similar Past Tasks

```bash
# AI searches LEDGER for "database migration"
grep -i "database" ai/LEDGER.md

# Finds entry from 2025-10-15
# Reads workdoc: ai/workdocs/archive/db-migration-users/
# Applies similar pattern
```

### Example 2: Understand Project Evolution

```bash
# Human reviews LEDGER to see recent optimizations
# Identifies trends: 3 performance tasks in Q4
# Plans follow-up work
```

### Example 3: AI Recovery After Long Break

```bash
# AI checks LEDGER for recent tasks
# Sees optimization work on 2025-11-09
# Loads: ai/maintenance_reports/temp-files-optimization-summary.md
# Quick context: 2-3 minutes
```

---

## 🚫 Anti-Patterns (What NOT to Do)

### ❌ Don't Use LEDGER as Progress Tracker

**Wrong**:
```markdown
### 2025-11-09: User Module Development

Progress:
- [x] Create plan
- [x] Implement model
- [ ] Add tests
- [ ] Write docs
```

**Right**: Use `workdocs/active/user-module/tasks.md` for this

---

### ❌ Don't Put Implementation Details

**Wrong**:
```markdown
Key Outcomes:
- Modified user.py line 45 to fix validation bug
- Changed database.yaml connection pool from 10 to 20
- Updated test_auth.py with 15 new test cases
```

**Right**: Reference detailed docs
```markdown
Key Outcomes:
- ✅ Fixed user authentication validation
- ✅ Optimized database connection pooling
- ✅ Improved test coverage (80% → 95%)

References:
- Sessions: ai/sessions/20251109_user_auth/
- Module: modules/users/PROGRESS.md
```

---

### ❌ Don't Duplicate Module PROGRESS.md

**Wrong**: Repeating all module progress in LEDGER

**Right**: LEDGER points to module docs
```markdown
Related Modules: modules/users/PROGRESS.md (see Phase 2.3)
```

---

## 📖 Example Entries

### Example: Feature Development

```markdown
### 2025-11-08: Workdocs Context Management

**Metadata**:
- **Type**: feature
- **Scope**: ai/workdocs/
- **Complexity**: medium
- **Duration**: 3 hours

**References**:
- **Workdoc**: `ai/workdocs/archive/workdocs-implementation/`
- **Sessions**: `ai/sessions/20251108_workdocs/`
- **Related Modules**: N/A (infrastructure)

**Key Outcomes**:
- ✅ Implemented three-file structure (plan/context/tasks)
- ✅ Created automation scripts (create/archive)
- ✅ Achieved 3-5x faster context recovery (2-5 min vs 15+ min)
- ⚠️ Follow-up: Add more templates for common scenarios

**Learnings**:
- 💡 context.md as primary recovery file significantly improves AI session continuity
- 💡 QUICK RESUME section is critical for fast task resumption
```

### Example: Bug Fix

```markdown
### 2025-11-07: Fix Database Migration Check

**Metadata**:
- **Type**: fix
- **Scope**: scripts/migrate_check.py
- **Complexity**: low
- **Duration**: 45 minutes

**References**:
- **Workdoc**: N/A (small fix)
- **Sessions**: N/A (direct fix)
- **Related Modules**: N/A (infrastructure)

**Key Outcomes**:
- ✅ Fixed false positive in up/down migration pairing check
- ✅ Added test case for edge case
- ✅ Updated error messages for clarity

**Learnings**:
- 💡 Always test migration checks with edge cases (timestamps, rollbacks)
```

### Example: Documentation

```markdown
### 2025-11-09: Temporary Files Management Policy

**Metadata**:
- **Type**: docs + optimization
- **Scope**: global (doc/policies/, Makefile, scripts/)
- **Complexity**: medium
- **Duration**: 4 hours

**References**:
- **Workdoc**: N/A (completed in single session)
- **Sessions**: N/A (conversation-based)
- **Report**: `ai/maintenance_reports/temp-files-optimization-summary.md`

**Key Outcomes**:
- ✅ Created TEMP_FILES_POLICY.md (comprehensive 400-line policy)
- ✅ Established temp/ directory structure
- ✅ Added 4 cleanup commands to Makefile
- ✅ Integrated temp_files_check into CI (22 checks total)
- ✅ Updated ai_maintenance.py with automatic checking

**Learnings**:
- 💡 Clear file classification (temporary/report/archive) prevents accumulation
- 💡 Smart cleanup (keep failed + recent N) balances disk space and debugging needs
- 💡 CI enforcement is critical for temporary file discipline
```

---

## 🔗 Related Documents

- **Workdocs Guide**: `ai/workdocs/README.md` (context management)
- **Sessions Archive**: `ai/sessions/` (AI self-review records)
- **Workflow Patterns**: `ai/workflow-patterns/` (standard workflows)
- **Module Progress**: `modules/*/PROGRESS.md` (module-specific history)
- **Parent Agent**: `ai/AGENTS.md` (workflow overview)

---

## 📈 Statistics Template

```markdown
## Task Statistics

| Month | Tasks | Types | Complexity Distribution |
|-------|-------|-------|------------------------|
| 2025-11 | 5 | docs:2, feature:2, fix:1 | trivial:0, low:1, medium:3, high:1, critical:0 |
| 2025-10 | 12 | feature:6, fix:3, refactor:2, docs:1 | trivial:2, low:4, medium:5, high:1, critical:0 |

## Insights

- **Peak productivity**: End of month (deadline-driven)
- **Common task types**: Feature development (50%), Bug fixes (25%)
- **Average duration**: Medium tasks = 3-4 hours
- **Success rate**: 95% (1 rollback in 2025-10)
```

---

## 📝 Task Record History

---

### 2025-11-09: Temporary Files Management Optimization

**Metadata**:
- **Type**: docs + optimization
- **Scope**: global (doc/policies/, Makefile, scripts/, ai/)
- **Complexity**: medium
- **Duration**: 4 hours

**References**:
- **Workdoc**: N/A
- **Sessions**: Current conversation
- **Report**: `ai/maintenance_reports/temp-files-optimization-summary.md`

**Key Outcomes**:
- ✅ Created comprehensive TEMP_FILES_POLICY.md (400 lines)
- ✅ Established temp/ directory with structure
- ✅ Added 4 cleanup commands (cleanup_reports, cleanup_reports_smart, cleanup_all, temp_files_check)
- ✅ Enhanced ai_maintenance.py with automatic checking
- ✅ Integrated temp_files_check into CI (dev_check now has 22 checks)
- ✅ Created AGENTS.md for all ai/ subdirectories
- ✅ Clarified LEDGER.md role and boundaries

**Learnings**:
- 💡 File classification (temporary/report/archive) prevents directory bloat
- 💡 Smart cleanup policies (keep failed + recent N) balance needs
- 💡 CI enforcement critical for file discipline
- 💡 Clear documentation boundaries reduce confusion

---

### 2025-11-05: Documentation Standards Enforcement

**Metadata**:
- **Type**: docs
- **Scope**: global
- **Complexity**: medium
- **Duration**: 3 hours

**References**:
- **Workdoc**: N/A
- **Sessions**: Previous conversation
- **Related**: `AGENTS.md` §13, `scripts/doc_style_check.py`

**Key Outcomes**:
- ✅ Prohibited decorative emojis in documentation
- ✅ Enforced language consistency rules
- ✅ Integrated doc_style_check into CI pipeline
- ✅ Updated all doc/ and modules/example/ documentation

**Learnings**:
- 💡 Consistent doc style improves AI parsing efficiency
- 💡 Automated checks better than manual review for style

---

### 2025-11-04: Project Initialization

**Metadata**:
- **Type**: init
- **Scope**: global
- **Complexity**: high
- **Duration**: Full day

**References**:
- **Workdoc**: N/A
- **Sessions**: `ai/sessions/20251104_init/`
- **Summary**: `doc/project/IMPLEMENTATION_SUMMARY.md`

**Key Outcomes**:
- ✅ Established modular directory structure
- ✅ Implemented layered context loading (S0-S6 workflow)
- ✅ Created comprehensive automation (DAG, contracts, config, migrations)
- ✅ Built example module with complete documentation

**Learnings**:
- 💡 Modular structure scales well with team growth
- 💡 Automation reduces cognitive load for AI agents
- 💡 Example modules accelerate onboarding

---

## 🔄 Version History

- **v1.0** (2025-11-09): Restructured LEDGER as task registry (removed detailed progress)
- **v0.1** (2025-11-04): Initial LEDGER creation

---

**Role**: Task Registry & Historical Index  
**NOT**: Progress Tracker (use workdocs/) or Session Archive (use sessions/)  
**Maintained by**: AI agents + Human operators after task completion
