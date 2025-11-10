---
spec_version: "1.0"
agent_id: "ai_infrastructure"
role: "AI task management and knowledge infrastructure"

policies:
  goals_ref: /doc/policies/goals.md
  safety_ref: /doc/policies/safety.md

parent_agent: /agent.md
merge_strategy: "child_overrides_parent"

subdirectories:
  - path: /ai/workdocs
    role: Task context management for active development
    agent: /ai/workdocs/agent.md
  - path: /ai/workflow-patterns
    role: Standard workflow patterns library
    agent: /ai/workflow-patterns/agent.md
  - path: /ai/maintenance_reports
    role: Automated maintenance and health reports
    agent: /ai/maintenance_reports/agent.md
  - path: /ai/sessions
    role: Historical AI self-review records (archived)
    agent: N/A (lightweight, no agent needed)

context_routes:
  always_read:
    - /ai/LEDGER.md
  on_demand:
    - topic: "Task Context Recovery"
      priority: high
      paths:
        - /ai/workdocs/README.md
        - /ai/workdocs/active/<current-task>/context.md
    - topic: "Workflow Patterns"
      priority: high
      paths:
        - /ai/workflow-patterns/README.md
        - /ai/workflow-patterns/catalog.yaml
    - topic: "Repository Health"
      priority: medium
      paths:
        - /ai/maintenance_reports/health-summary.md
        - /ai/maintenance_reports/README.md
---

# AI Infrastructure Agent

> **Purpose**: Manage AI-specific infrastructure for task management, patterns, and knowledge  
> **Audience**: AI agents (primary)  
> **Language**: English (AI-optimized)

---

## Directory Overview

The `ai/` directory contains **AI-specific infrastructure** separate from application code:

```
ai/
├── agent.md                    # This file (directory orchestrator)
├── LEDGER.md                   # Task registry (high-level index)
├── workdocs/                   # Active task context management
│   ├── agent.md
│   ├── active/                 # In-progress tasks
│   └── archive/                # Completed tasks
├── workflow-patterns/          # Standard workflow library (8 patterns)
│   ├── agent.md
│   ├── patterns/               # YAML pattern definitions
│   └── catalog.yaml
├── maintenance_reports/        # Automated reports
│   ├── agent.md
│   └── *.{json,md}
└── sessions/                   # Historical AI self-review records
    └── <date>_<name>/
        ├── AI-SR-plan.md
        └── AI-SR-impl.md
```

---

## Core Components

### 1. LEDGER.md (Task Registry) 📋

**Role**: High-level task index

**Use When**:
- 🔍 Finding similar past tasks
- 🔍 Understanding project history
- 🔍 Getting quick task overview (30 sec)

**NOT For**:
- ❌ Detailed progress tracking
- ❌ Active task management
- ❌ Session transcripts

**Read**: Always (part of context refresh)

---

### 2. workdocs/ (Task Context Management) ⭐

**Role**: Active task context for fast recovery

**Structure**: Three-file system (plan/context/tasks)

**Use When**:
- 🚀 Starting multi-session task
- 🚀 Resuming interrupted work (2-5 min recovery)
- 🚀 Tracking active progress

**Key File**: `active/<task>/context.md` (primary recovery file)

**Read**: When working on active tasks

**Agent**: `/ai/workdocs/agent.md`

---

### 3. workflow-patterns/ (Standard Workflows) 📚

**Role**: Reusable workflow templates

**Contents**: 8 patterns (4 P0, 4 P1)
- module-creation (P0, 2-4h)
- database-migration (P0, 30-60min)
- api-development (P0, 1-2h)
- bug-fix (P0, 30-90min)
- refactoring (P1, 1-3h)
- feature-development (P1, 4-8h)
- performance-optimization (P1, 2-4h)
- security-audit (P1, 2-3h)

**Use When**:
- 📖 Starting new task (check for pattern)
- 📖 Need structured workflow
- 📖 Want to avoid common pitfalls

**Auto-trigger**: Via `/doc/orchestration/agent-triggers.yaml`

**Agent**: `/ai/workflow-patterns/agent.md`

---

### 4. maintenance_reports/ (Automated Reports) 📊

**Role**: Store auto-generated maintenance and health reports

**Contents**:
- Health reports (JSON/Markdown)
- Optimization reports
- Audit reports
- Trend analysis

**Use When**:
- 📊 Checking repo health
- 📊 Understanding recent optimizations
- 📊 Reviewing maintenance history

**Cleanup**: `make cleanup_reports_smart` (monthly)

**Agent**: `/ai/maintenance_reports/agent.md`

---

### 5. sessions/ (Historical Archive) 🗄️

**Role**: Archive AI self-review documents

**Contents**:
- `AI-SR-plan.md` (plan self-review)
- `AI-SR-impl.md` (implementation self-review)

**Use When**:
- 🗄️ Historical reference only
- 🗄️ Rarely needed (workdocs preferred)

**NOT For**:
- ❌ Context recovery (use workdocs)
- ❌ Active development

**Note**: Lightweight, no agent.md needed

---

## Usage Guidelines

### For AI Agents

#### Report Generation Policy ⚠️ CRITICAL

**ALWAYS generate reports in `/ai/maintenance_reports/`**

```bash
# ✅ CORRECT:
/ai/maintenance_reports/health-summary-20251110.md
/ai/maintenance_reports/optimization-20251110.md

# ❌ WRONG:
/health-report.md              # NO! Root directory
/tmp/optimization.md           # NO! Temporary directory
```

#### Starting New Task

```bash
# 1. Check LEDGER for similar tasks
grep -i "keyword" ai/LEDGER.md

# 2. Check for applicable workflow pattern
make workflow_suggest PROMPT="task description"

# 3. Create workdoc (if multi-session)
make workdoc_create TASK=<task-name>

# 4. Follow recommended pattern
make workflow_show PATTERN=<pattern-id>
```

#### Resuming Task

```bash
# 1. Load workdoc context (PRIMARY)
cat ai/workdocs/active/<task>/context.md

# 2. Check LEDGER for related history
grep -i "<task-topic>" ai/LEDGER.md

# 3. Review recent health (if relevant)
cat ai/maintenance_reports/health-summary.md

# Recovery time: 2-5 minutes
```

#### Completing Task

```bash
# 1. Update LEDGER with task entry
vim ai/LEDGER.md

# 2. Archive workdoc (if exists)
make workdoc_archive TASK=<task-name>

# 3. Run maintenance
make ai_maintenance

# 4. Clean temporary files
make cleanup_tmp
```

---

### For Human Operators

#### Monitor Active Work

```bash
# List active workdocs
make workdoc_list

# Check latest health
cat ai/maintenance_reports/health-summary.md

# Review task history
cat ai/LEDGER.md
```

#### Maintenance

```bash
# Weekly: Clean old reports
make cleanup_reports_smart

# Monthly: Archive completed workdocs
ls ai/workdocs/active/
# Move old tasks to archive/

# Quarterly: Review LEDGER statistics
# Update project insights
```

---

## Document Boundaries (Critical Understanding)

| Document | Granularity | Timeline | Update Frequency | Primary Use |
|----------|-------------|----------|------------------|-------------|
| **LEDGER.md** | Task-level | Historical | After completion | Task index & history |
| **workdocs/context.md** | Milestone-level | Active | Continuous | Context recovery |
| **workdocs/plan.md** | Phase-level | Future+Active | Before phases | Strategic planning |
| **workdocs/tasks.md** | Subtask-level | Active | Task changes | Detailed tracking |
| **sessions/** | Session-level | Historical | One-time | AI self-review archive |
| **modules/*/PROGRESS.md** | Module-level | Historical | After milestones | Module history |
| **modules/*/plan.md** | Iteration-level | Future | Before changes | Next iteration plan |
| **modules/*/CHANGELOG.md** | Version-level | Historical | With releases | User-facing changes |

### Key Distinctions

```
Purpose:
├─ Task Registry → LEDGER.md
├─ Active Context → workdocs/active/<task>/
├─ Historical Archive → workdocs/archive/, sessions/
└─ Module History → modules/*/PROGRESS.md

Timeline:
├─ Future → workdocs/plan.md, modules/*/plan.md
├─ Present → workdocs/active/
└─ Past → LEDGER.md, sessions/, workdocs/archive/

Granularity:
├─ High-level → LEDGER.md (task index)
├─ Medium → workdocs/ (task details)
└─ Detailed → modules/* (code-level)
```

---

## Integration with Workflow

The `ai/` infrastructure integrates with standard workflow (S0-S6):

### S0: Refresh Context
```
1. Load LEDGER.md (30 sec) → Check for related tasks
2. Load active workdoc context.md (2 min) → Resume work
3. Check workflow pattern (1 min) → Understand structure
4. Review health summary (30 sec) → Know repo state

Total: ~5 minutes (vs 15+ min without infrastructure)
```

### S1: Task Modeling
```
1. Create/update workdoc plan.md → Define strategy
2. Select workflow pattern → Follow structure
3. Create module plan.md → Detail implementation
```

### S2: Plan Review
```
1. Generate AI-SR-plan.md → Self-review
2. Save to sessions/ → Archive
3. Update workdoc context.md → Record decision
```

### S3-S5: Implementation
```
1. Update workdoc context.md → Track progress
2. Follow workflow pattern → Ensure quality
3. Generate AI-SR-impl.md → Self-review
```

### S6: Auto Maintenance
```
1. Update LEDGER.md → Register task
2. Archive workdoc → Move to archive/
3. Run make ai_maintenance → Generate reports
4. Clean temp files → make cleanup_tmp
```

---

## Safety & Access Control

### Read Access
- ✅ All AI agents
- ✅ All team members

### Write Access

| Directory | Who | Rules |
|-----------|-----|-------|
| **LEDGER.md** | AI + Human | Add entry after task completion |
| **workdocs/active/** | AI + Human | Create/update during task |
| **workdocs/archive/** | AI + Human | Archive only, no edits |
| **workflow-patterns/** | Human | Must validate (`make workflow_validate`) |
| **maintenance_reports/** | Automated scripts | No manual writes |
| **sessions/** | AI only | During S2 & S5 (self-review) |

### Git Tracking

- ✅ Commit: LEDGER.md, workdocs/, workflow-patterns/
- ⚠️ Selective: maintenance_reports/ (archive only, not auto-reports)
- ❌ Ignore: Temporary reports if >20 files

---

## Automation Commands

```bash
# Task Management
make workdoc_create TASK=<name>       # Create workdoc
make workdoc_list                     # List active workdocs
make workdoc_archive TASK=<name>      # Archive completed task

# Workflow Patterns
make workflow_list                    # List all patterns
make workflow_suggest PROMPT="..."    # Recommend pattern
make workflow_show PATTERN=<id>       # View pattern details
make workflow_apply PATTERN=<id>      # Generate checklist

# Maintenance & Reports
make ai_maintenance                   # Run maintenance checks
make health_check                     # Repository health
make cleanup_reports_smart            # Clean old reports

# Cleanup
make cleanup_tmp                      # Clean temporary files
make cleanup_all                      # Clean everything
```

---

## Best Practices

### DO ✅

- ✅ Update LEDGER after every task
- ✅ Create workdoc for multi-session tasks
- ✅ Use workflow patterns for standard tasks
- ✅ Keep workdoc context.md updated
- ✅ Archive completed workdocs promptly
- ✅ Clean reports monthly
- ✅ Review health summary weekly

### DON'T ❌

- ❌ Use LEDGER for detailed progress
- ❌ Skip updating workdoc context.md
- ❌ Create custom workflows (use patterns)
- ❌ Manually edit maintenance reports
- ❌ Leave completed tasks in workdocs/active/
- ❌ Let reports accumulate (>20 files)

---

## Metrics & Goals

### Context Recovery Time
- **Target**: <5 minutes
- **Current**: 2-5 minutes (achieved)
- **Without**: 15+ minutes

### Task Registry Coverage
- **Target**: 100% of AI tasks
- **Current**: Tracking since 2025-11-04

### Pattern Utilization
- **Target**: 80% of tasks use patterns
- **Current**: 8 patterns available (P0 & P1)

### Report Cleanup
- **Target**: <20 files in maintenance_reports/
- **Automation**: `make cleanup_reports_smart`

---

## Related Documents

- **Root Agent**: `/agent.md` (S0-S6 workflow)
- **Workflow Patterns**: `/ai/workflow-patterns/README.md`
- **Workdocs Guide**: `/ai/workdocs/README.md`
- **Task Registry**: `/ai/LEDGER.md`
- **Cleanup Policy**: `/doc/policies/TEMP_FILES_POLICY.md`

---

## Subdirectory Agents

Each subdirectory has its own agent.md for detailed configuration:

- **workdocs**: `/ai/workdocs/agent.md`
- **workflow-patterns**: `/ai/workflow-patterns/agent.md`
- **maintenance_reports**: `/ai/maintenance_reports/agent.md`

---

**Version**: 1.0  
**Last Updated**: 2025-11-09  
**Coverage**: 4 subdirectories + LEDGER  
**Maintained by**: AI agents + Human operators

