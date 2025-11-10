---
spec_version: "1.0"
agent_id: "ai_workdocs"
role: "Task context management and recovery for AI development sessions"

policies:
  goals_ref: /doc/policies/goals.md
  safety_ref: /doc/policies/safety.md

parent_agent: /ai/agent.md
merge_strategy: "child_overrides_parent"

context_routes:
  always_read:
    - /ai/workdocs/README.md
  on_demand:
    - topic: "Workdocs Usage"
      paths:
        - /doc/process/workdocs-quickstart.md
---

# Workdocs Agent

> **Purpose**: Manage AI task context for seamless session recovery  
> **Primary Use**: Context restoration across AI sessions (2-5 min recovery time)  
> **Audience**: AI agents (primary), human operators (secondary)

---

## Directory Role

**Core Function**: Enable AI agents to quickly recover task context after interruption or session end.

**Problem Solved**: Without workdocs, AI needs to re-read entire codebase and history (15+ min). With workdocs, context recovery takes 2-5 minutes.

**Key Feature**: Three-file structure (plan, context, tasks) optimized for AI parsing and human review.

---

## File Structure

```
workdocs/
├── agent.md            # This file
├── README.md           # Usage guide (170 lines)
├── active/             # In-progress tasks
│   └── <task-name>/
│       ├── plan.md     # Strategic plan
│       ├── context.md  # ⭐ Context recovery (MOST IMPORTANT)
│       └── tasks.md    # Task checklist
└── archive/            # Completed tasks
    └── <task-name>/
        └── ...
```

---

## Three Core Files

### 1. plan.md (Strategic Plan)

**Purpose**: High-level task planning

**Content**:
- Executive summary (goals, scope)
- Current state analysis
- Implementation phases
- Risk management
- Success metrics
- Timeline
- Dependencies

**Update Frequency**: Beginning + when plan changes

**AI Usage**: Load once at task start

---

### 2. context.md (Context Recovery) ⭐ MOST IMPORTANT

**Purpose**: Fast context restoration (2-5 min)

**Content**:
```markdown
## SESSION PROGRESS
- ✅ Completed: [list]
- 🏗️ In Progress: [current work]
- ⏳ Pending: [next steps]
- 🚫 Blocked: [blockers]

## KEY FILES STATUS
- File1: [status and changes]
- File2: [status and changes]

## CRITICAL DECISIONS
1. Decision + rationale
2. Trade-offs chosen

## ERRORS TO AVOID
1. Error + how to prevent

## TECHNICAL CONSTRAINTS
- Constraint 1
- Constraint 2

## QUICK RESUME
[1-2 sentence instruction to resume work]
```

**Update Frequency**: After every milestone/session

**AI Usage**: 
- **PRIMARY recovery file** - read this first
- Update after each significant progress
- Critical for multi-session tasks

---

### 3. tasks.md (Task Checklist)

**Purpose**: Detailed task tracking

**Content**:
- Task list (TODO/IN_PROGRESS/DONE)
- Acceptance criteria per task
- Dependencies
- Risk assessment

**Update Frequency**: When task status changes

**AI Usage**: Track specific subtasks

---

## Ownership & Safety

### Read Access
- ✅ All AI agents
- ✅ All team members

### Write Access
- ✅ AI agents (during active development)
- ✅ Human operators (manual tasks)
- ⚠️ Must update `context.md` after each milestone

### Git Tracking
- ✅ Commit all files in `active/` (for context preservation)
- ✅ Commit `archive/` (historical reference)
- ❌ Never put secrets or credentials in workdocs

---

## Usage Guidelines

### For AI Agents

**Starting new task**:
```bash
# Create workdoc
make workdoc_create TASK=implement-user-auth

# System creates:
# - ai/workdocs/active/implement-user-auth/plan.md
# - ai/workdocs/active/implement-user-auth/context.md
# - ai/workdocs/active/implement-user-auth/tasks.md
```

**Resuming task** (Context Recovery):
```python
# STEP 1: Load context.md (PRIMARY)
context = read("ai/workdocs/active/<task>/context.md")
# Extract: SESSION PROGRESS, QUICK RESUME

# STEP 2: Check plan.md (if needed)
plan = read("ai/workdocs/active/<task>/plan.md")
# Extract: goals, scope, phases

# STEP 3: Load tasks.md
tasks = read("ai/workdocs/active/<task>/tasks.md")
# Extract: pending tasks, dependencies

# Total time: 2-5 minutes
```

**During development**:
- ✅ Update `context.md` after each milestone
- ✅ Update SESSION PROGRESS
- ✅ Record critical decisions
- ✅ Log errors to avoid
- ✅ Update QUICK RESUME

**Completing task**:
```bash
# Archive workdoc
make workdoc_archive TASK=implement-user-auth

# Moves to: ai/workdocs/archive/implement-user-auth/
```

---

### For Human Operators

**Create workdoc**:
```bash
make workdoc_create TASK=<task-name>
```

**List workdocs**:
```bash
make workdoc_list
```

**Archive completed task**:
```bash
make workdoc_archive TASK=<task-name>
```

**Manual creation**:
```bash
mkdir -p ai/workdocs/active/<task-name>
cd ai/workdocs/active/<task-name>
# Copy templates from doc/templates/workdoc-*.md
```

---

## Comparison with Other Mechanisms

| Mechanism | Purpose | Organization | Context Recovery | Update Frequency |
|-----------|---------|--------------|------------------|------------------|
| **workdocs/** | Task context mgmt | By task name | ⭐ Optimized (2-5 min) | Continuous |
| **sessions/** | Session history | By date + session | ❌ Not optimized | One-time |
| **LEDGER.md** | Task registry | Chronological | ❌ Index only | After task completion |
| **plan.md** (module) | Future plans | By module | Partial | Before changes |
| **PROGRESS.md** (module) | History | By module | Partial | After milestones |

**Key Difference**: 
- `workdocs/` = **Active task management** (continuous updates, fast recovery)
- `sessions/` = **Historical archive** (one-time record, AI-SR documents)
- `LEDGER.md` = **Task index** (high-level registry, reference only)

---

## Best Practices

### DO ✅

- ✅ Create workdoc for tasks spanning >2 sessions
- ✅ Update `context.md` after each milestone
- ✅ Record ALL critical decisions
- ✅ Log errors and lessons learned
- ✅ Keep QUICK RESUME up-to-date
- ✅ Archive completed tasks promptly

### DON'T ❌

- ❌ Share workdoc across multiple tasks
- ❌ Forget to update SESSION PROGRESS
- ❌ Skip recording errors (will repeat mistakes)
- ❌ Leave completed tasks in `active/`
- ❌ Store secrets or credentials

---

## Context Recovery Time

| Scenario | Without Workdocs | With Workdocs |
|----------|------------------|---------------|
| Simple task | 5-10 min | 2 min |
| Medium task | 15-20 min | 3-5 min |
| Complex task | 30+ min | 5-10 min |

**Savings**: 3-5x faster context recovery

---

## Automation Commands

```bash
# Create
make workdoc_create TASK=<task-name>

# List
make workdoc_list

# Archive
make workdoc_archive TASK=<task-name>
```

---

## Related Documents

- **Usage Guide**: `README.md` (170 lines)
- **Quickstart**: `/doc/process/workdocs-quickstart.md`
- **Templates**: `/doc/templates/workdoc-*.md`
- **Create Script**: `/scripts/workdoc_create.sh`
- **Archive Script**: `/scripts/workdoc_archive.sh`
- **Parent Agent**: `/ai/agent.md`

---

## Integration with Workflow

Workdocs integrate into standard workflow:

```
S0: Refresh Context
├─ Load active workdoc context.md (if exists)
└─ Fast recovery (2-5 min)

S1: Task Modeling
├─ Create/update workdoc plan.md
└─ Define scope, phases, risks

S3: Implementation
├─ Update workdoc context.md (after milestones)
└─ Record decisions, errors, progress

S6: Auto Maintenance
├─ Review workdoc status
└─ Archive completed tasks
```

---

**Version**: 1.0  
**Last Updated**: 2025-11-09  
**Recovery Time**: 2-5 minutes (vs 15+ min without)  
**Maintained by**: AI agents + Human operators

