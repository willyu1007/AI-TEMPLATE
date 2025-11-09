# Workdocs - AI Quick Start

> **For AI Agents** - Quick reference (~100 lines)  
> **Full Guide**: WORKDOCS_GUIDE.md (653 lines)  
> **Language**: English (AI-optimized)

---

## Purpose

Manage task context for efficient session recovery. Resume work in 2-5 minutes instead of 15-30 minutes.

---

## Quick Commands

```bash
# Create new task
make workdoc_create TASK=implement-user-auth

# List all workdocs
make workdoc_list

# Archive completed task
make workdoc_archive TASK=implement-user-auth
```

---

## Directory Structure

```
ai/workdocs/
├── active/              # Current tasks
│   └── implement-user-auth/
│       ├── plan.md      # Task plan and scope
│       ├── context.md   # Technical context
│       └── tasks.md     # Task checklist
└── archive/             # Completed tasks
    └── implement-user-auth_20251109/
        └── ... (same files)
```

---

## 3 Core Files

### 1. plan.md - Task Plan
```markdown
# Task: Implement User Authentication

## Objective
Add JWT-based authentication to user module

## Scope
- [ ] Create auth middleware
- [ ] Add login/logout endpoints
- [ ] Update user model with password field
- [ ] Write tests (≥80% coverage)

## Out of Scope
- OAuth integration (Phase 2)
- 2FA (Phase 3)

## Dependencies
- modules/user (existing)
- JWT library (install)

## Risk
- Password storage security
- Token expiration handling
```

### 2. context.md - Technical Context
```markdown
# Technical Context

## Current State
- User module exists at modules/user/
- No authentication implemented
- API endpoints are public

## Key Decisions
1. Use JWT tokens (not sessions)
2. bcrypt for password hashing
3. Token expiry: 24 hours

## Related Files
- modules/user/service.py (add auth logic)
- modules/user/models.py (add password field)
- common/middleware/auth.py (create)

## References
- DB Schema: db/engines/postgres/schemas/users.yaml
- API Contract: modules/user/doc/CONTRACT.md
```

### 3. tasks.md - Task Checklist
```markdown
# Task Checklist

## Phase 1: Setup (1h)
- [ ] Install dependencies (jwt, bcrypt)
- [ ] Update requirements.txt
- [ ] Create migration for password field

## Phase 2: Implementation (3h)
- [ ] Implement password hashing in user model
- [ ] Create auth middleware
- [ ] Add login endpoint POST /api/auth/login
- [ ] Add logout endpoint POST /api/auth/logout
- [ ] Update existing endpoints with @require_auth

## Phase 3: Testing (2h)
- [ ] Unit tests for auth middleware
- [ ] Integration tests for login/logout
- [ ] Test coverage ≥80%

## Phase 4: Documentation (1h)
- [ ] Update CONTRACT.md
- [ ] Update README.md
- [ ] Update CHANGELOG.md
```

---

## Workflow

### Creating New Task

```bash
# 1. Create workdoc
make workdoc_create TASK=add-payment-module

# 2. System creates:
#    ai/workdocs/active/add-payment-module/
#    ├── plan.md (from template)
#    ├── context.md (from template)
#    └── tasks.md (from template)

# 3. Fill in the files:
vim ai/workdocs/active/add-payment-module/plan.md
vim ai/workdocs/active/add-payment-module/context.md
vim ai/workdocs/active/add-payment-module/tasks.md

# 4. Start working:
#    - AI reads these files for context
#    - Update tasks.md as you progress
#    - Add notes to context.md as needed
```

### Resuming Task (Context Recovery)

```bash
# 1. AI agent starts new session

# 2. List active tasks:
make workdoc_list
# Output: add-payment-module (active)

# 3. Read workdoc files:
#    - plan.md: What are we building?
#    - context.md: Technical decisions and current state
#    - tasks.md: What's done, what's next?

# 4. Resume work immediately (2-5 min recovery)
```

### Completing Task

```bash
# 1. Mark all tasks complete in tasks.md

# 2. Archive the workdoc:
make workdoc_archive TASK=add-payment-module

# 3. System moves to archive:
#    active/add-payment-module/ 
#    → archive/add-payment-module_20251109/
```

---

## Templates

Templates at `doc/templates/workdoc-*.md`:
- `workdoc-plan.md` - Task planning template
- `workdoc-context.md` - Technical context template
- `workdoc-tasks.md` - Task checklist template

Customize templates for your team's workflow.

---

## Best Practices

### 1. One Workdoc per Task
- Don't mix multiple features in one workdoc
- Keep scope focused
- Create separate workdocs for big features

### 2. Update Frequently
- Update tasks.md after each milestone
- Add notes to context.md when making decisions
- Keep plan.md in sync if scope changes

### 3. Archive Promptly
- Archive completed tasks within 1 day
- Don't leave stale workdocs in active/
- Archived workdocs serve as historical reference

### 4. Clear Naming
```bash
# Good names (clear, specific)
implement-user-auth
fix-payment-bug-123
refactor-order-service

# Bad names (vague, generic)
new-feature
bug-fix
update
```

---

## Integration with Development

### With Git Branches
```bash
# Create matching branch
git checkout -b feat/implement-user-auth

# Workdoc: ai/workdocs/active/implement-user-auth/
# Branch: feat/implement-user-auth
# Keep names aligned for easy tracking
```

### With CI/CD
```yaml
# .github/workflows/workdoc-check.yml
- name: Check Active Workdocs
  run: |
    # Warn if too many active tasks
    count=$(ls ai/workdocs/active/ | wc -l)
    if [ $count -gt 3 ]; then
      echo "Warning: $count active workdocs. Consider archiving completed ones."
    fi
```

### With PR
```markdown
# In PR description, link to workdoc

## Related Workdoc
See ai/workdocs/active/implement-user-auth/ for:
- Task plan and scope
- Technical decisions
- Checklist status
```

---

## Common Scenarios

### Multi-Session Task
```bash
# Day 1: Start task (Session 1)
make workdoc_create TASK=complex-feature
# ... work 4 hours, complete Phase 1 ...
# Update tasks.md: [x] Phase 1, [ ] Phase 2

# Day 2: Resume task (Session 2)
# Read: ai/workdocs/active/complex-feature/tasks.md
# See: Phase 1 done, Phase 2 next
# Continue from Phase 2 immediately (2-min recovery)
```

### Blocked Task
```markdown
# In tasks.md, mark blocked items:

## Phase 2: Implementation
- [x] Task A (done)
- [BLOCKED] Task B - Waiting for API key from ops team
- [ ] Task C (depends on B)

# In context.md, add note:
## Blockers
- API key request sent to ops@example.com on 2025-11-09
- Expected resolution: 2025-11-10
```

### Abandoned Task
```bash
# If task is canceled or deprioritized:
# 1. Add note to plan.md:
echo "## Status: Abandoned (2025-11-09)" >> plan.md
echo "Reason: Feature deprioritized by product team" >> plan.md

# 2. Archive (for record keeping):
make workdoc_archive TASK=abandoned-feature
```

---

## See Also

- **Full Guide**: doc/process/WORKDOCS_GUIDE.md (653 lines, detailed workflows)
- **Templates**: doc/templates/workdoc-*.md (3 template files)
- **Scripts**: scripts/workdoc_create.sh, scripts/workdoc_archive.sh
- **AI Ledger**: ai/LEDGER.md (high-level task tracking)

