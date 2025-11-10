---
spec_version: "1.0"
agent_id: "ai_workflow_patterns"
role: "Standard workflow patterns library for common development tasks"

policies:
  goals_ref: /doc/policies/goals.md
  safety_ref: /doc/policies/safety.md

parent_agent: /ai/agent.md
merge_strategy: "child_overrides_parent"

context_routes:
  always_read:
    - /ai/workflow-patterns/README.md
  on_demand:
    - topic: "Pattern Details"
      paths:
        - /ai/workflow-patterns/PATTERNS_GUIDE.md
    - topic: "Pattern Catalog"
      paths:
        - /ai/workflow-patterns/catalog.yaml
---

# Workflow Patterns Agent

> **Purpose**: Provide reusable workflow patterns for common development tasks  
> **Audience**: AI agents (primary)  
> **Language**: English (AI-optimized)

---

## Directory Role

This directory contains **8 standardized workflow patterns** for common development scenarios:

1. **module-creation** - Create new module (P0, 2-4h)
2. **database-migration** - Database changes (P0, 30-60min)
3. **api-development** - API development (P0, 1-2h)
4. **bug-fix** - Bug fixing (P0, 30-90min)
5. **refactoring** - Code refactoring (P1, 1-3h)
6. **feature-development** - Feature development (P1, 4-8h)
7. **performance-optimization** - Performance tuning (P1, 2-4h)
8. **security-audit** - Security review (P1, 2-3h)

---

## File Structure

```
workflow-patterns/
├── agent.md                    # This file
├── README.md                   # Quick reference (AI-optimized, 140 lines)
├── PATTERNS_GUIDE.md           # Complete guide (human reference, 400 lines)
├── catalog.yaml                # Pattern metadata (auto-generated)
└── patterns/
    ├── module-creation.yaml    # P0: Module creation workflow
    ├── database-migration.yaml # P0: DB change workflow
    ├── api-development.yaml    # P0: API development workflow
    ├── bug-fix.yaml            # P0: Bug fix workflow
    ├── refactoring.yaml        # P1: Refactoring workflow
    ├── feature-development.yaml # P1: Feature workflow
    ├── performance-optimization.yaml # P1: Performance workflow
    └── security-audit.yaml     # P1: Security workflow
```

---

## Pattern Structure

Each pattern YAML contains:

```yaml
id: pattern-name
name: Pattern Display Name
description: Brief description
complexity: low|medium|high
estimated_time: Duration
category: development|maintenance|debugging|optimization
priority: P0|P1|P2

triggers:
  keywords: [list of trigger words]
  file_patterns: [file patterns that suggest this workflow]

prerequisites:
  - Condition 1
  - Condition 2

workflow:
  - step: 1
    name: Step Name
    description: What to do
    commands: [make commands]
    estimated_time: 15min
    critical: true|false

common_pitfalls:
  - issue: Common mistake
    solution: How to avoid

quality_checklist:
  - item: Quality check
    command: make command

references:
  - path: /doc/path
    description: Reference doc
```

---

## Ownership & Safety

### Read Access
- ✅ All AI agents (via auto-trigger system)
- ✅ All team members

### Write Access
- ✅ Add new patterns (follow schema)
- ✅ Update existing patterns (preserve structure)
- ⚠️ Must run `make workflow_validate` after changes

### Git Tracking
- ✅ All pattern files committed
- ✅ catalog.yaml auto-generated (should commit after updates)

---

## Usage Guidelines

### For AI Agents

**Auto-trigger**:
When user message contains pattern keywords, system recommends relevant pattern automatically via `/doc/orchestration/agent-triggers.yaml`.

**Manual selection**:
```bash
# Recommend pattern based on task
make workflow_suggest PROMPT="create user module"

# View pattern details
make workflow_show PATTERN=module-creation

# Apply pattern (generate checklist)
make workflow_apply PATTERN=module-creation
```

**Context loading**:
- Load `README.md` for quick reference (AI-optimized, 140 lines)
- Load specific pattern YAML when applying workflow
- Load `PATTERNS_GUIDE.md` only if detailed explanation needed (human doc, 400 lines)

---

### For Human Contributors

**Add new pattern**:
1. Create `/ai/workflow-patterns/patterns/new-pattern.yaml`
2. Follow existing pattern schema
3. Run `make workflow_validate` to verify
4. Update `catalog.yaml` (auto-generated via validation)
5. Update README.md pattern table

**Update existing pattern**:
1. Edit pattern YAML file
2. Run `make workflow_validate`
3. Test with `make workflow_show PATTERN=<name>`
4. Commit changes

---

## Pattern Selection Guide

### Decision Tree

```
Task type?
├─ New module → module-creation (P0, 2-4h)
├─ New feature → feature-development (P1, 4-8h)
├─ Bug → bug-fix (P0, 30-90min)
├─ API → api-development (P0, 1-2h)
├─ Database → database-migration (P0, 30-60min)
├─ Refactor → refactoring (P1, 1-3h)
├─ Performance → performance-optimization (P1, 2-4h)
└─ Security → security-audit (P1, 2-3h)
```

### Priority Levels

- **P0**: Critical patterns, must use for these tasks
  - module-creation, database-migration, api-development, bug-fix
- **P1**: Recommended patterns, improve quality
  - refactoring, feature-development, performance-optimization, security-audit
- **P2**: Optional patterns (future)

---

## Integration Points

### Trigger System
Patterns automatically suggested via:
- **File change triggers**: `/doc/orchestration/agent-triggers.yaml`
- **Keyword triggers**: Pattern `triggers.keywords` field
- **Context analysis**: `make workflow_suggest` analyzes task description

### Quality Gates
Patterns reference quality checks:
- `make dev_check` - Always required
- Pattern-specific checks in `quality_checklist`
- Coverage requirements in workflow steps

### Documentation
Patterns link to:
- Module docs: `/doc/modules/MODULE_INIT_GUIDE.md`
- DB docs: `/doc/db/DB_SPEC.yaml`
- Testing: `/doc/process/testing.md`
- Coding standards: `/doc/process/AI_CODING_GUIDE.md`

---

## Automation Commands

```bash
# Pattern discovery
make workflow_list                     # List all patterns
make workflow_suggest PROMPT="task"    # AI recommends pattern

# Pattern usage
make workflow_show PATTERN=<id>        # View pattern details
make workflow_apply PATTERN=<id>       # Generate checklist

# Pattern validation
make workflow_validate                 # Validate all patterns
```

---

## Related Documents

- **Quick Reference**: `README.md` (AI-optimized, 140 lines)
- **Complete Guide**: `PATTERNS_GUIDE.md` (human doc, 400 lines)
- **Trigger Rules**: `/doc/orchestration/agent-triggers.yaml`
- **Parent Agent**: `/ai/agent.md`
- **Workflow Script**: `/scripts/workflow_suggest.py`

---

## Quality Standards

### Pattern Quality
- ✅ Clear prerequisites
- ✅ Step-by-step workflow (6-9 steps)
- ✅ Estimated times
- ✅ Common pitfalls documented
- ✅ Quality checklist
- ✅ Reference links

### Pattern Coverage
- P0 patterns: 100% of critical paths
- P1 patterns: Common scenarios
- P2 patterns: Nice-to-have (future)

---

**Version**: 1.0  
**Last Updated**: 2025-11-09  
**Pattern Count**: 8 (4 P0, 4 P1)  
**Maintained by**: Project team

