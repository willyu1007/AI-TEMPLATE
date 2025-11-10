# Agent Workflow Details

> **Purpose**: Detailed workflow explanations moved from main agent.md  
> **For**: Reference when needing detailed implementation guidance

---

## S0 - Refresh Context Details

### Tier Loading Strategy

**Tier-0 (Required)**:
- `/.aicontext/snapshot.json` - Project structure snapshot
- `/.aicontext/module_index.json` - Module index

**Tier-1 (Strongly Recommended)**:
- `/doc/flows/dag.yaml` - DAG dependencies
- `tools/*/contract.json` - Tool contracts
- Target module `plan.md`/`README.md`

**Tier-2 (Recommended)**:
- `/doc/db/DB_SPEC.yaml` - Database specs
- `/doc/process/ENV_SPEC.yaml` - Environment specs
- `/config/*.yaml` - Configuration files

**Tier-3 (As Needed)**:
- `TEST_PLAN.md` - Test plans
- `RUNBOOK.md` - Operations guide
- `PROGRESS.md` - Progress tracking
- `BUGS.md` - Bug tracking

### Context Loading Decision Tree

```
1. Check snapshot_hash changed?
   ├─ YES → Run make docgen first
   └─ NO → Continue
   
2. Check task type:
   ├─ Module development → Load module docs
   ├─ Database work → Load DB specs
   ├─ API work → Load contracts
   └─ Bug fix → Load BUGS.md
```

---

## S1 - Task Modeling Details

### Plan.md Structure

```markdown
## Scope
- What will be changed
- What will NOT be changed

## Interface Impact
- [ ] API changes
- [ ] Contract changes
- [ ] Database changes
- [ ] UI changes

## Data Changes
- Migration requirements
- Backward compatibility

## Risk Assessment
- High: [risks]
- Medium: [risks]
- Low: [risks]

## Verification Commands
make dev_check
make test MODULE=<name>

## Rollback Plan
- Step 1: ...
- Step 2: ...
```

### Boundary Rules

- `plan.md` = Future plans (before implementation)
- `PROGRESS.md` = Historical records (after completion)
- Don't mix future and past in same document

---

## S2 - Plan Review Details

### AI-SR Plan Structure

Generate `/ai/sessions/<date>_<name>/AI-SR-plan.md`:

```markdown
# AI Self-Review: Plan

## Intent
[Clear description of what we're trying to achieve]

## Impact Analysis
### Changed Components
- Component 1: [impact]
- Component 2: [impact]

### DAG Changes
- [ ] No cycle introduced
- [ ] Dependencies clear

### Contract Changes
- [ ] Backward compatible
- [ ] Version bumped if breaking

### Database Changes
- [ ] Migration script ready
- [ ] Rollback script ready

## Test Plan
1. Unit tests for...
2. Integration tests for...
3. Manual verification of...

## Rollback Plan
1. If failure at step X...
2. Run rollback command...
3. Verify with...
```

---

## S3 - Implementation & Verification Details

### Test Requirements Matrix

| Component Type | Coverage Requirement | Test Types |
|----------------|---------------------|------------|
| Core Logic | ≥80% | Unit + Integration |
| API Endpoints | ≥90% | Unit + Contract + E2E |
| Database | 100% migrations | Migration + Rollback |
| Common Module | ≥90% | Unit + Integration |
| UI Components | ≥70% | Unit + Snapshot |

### Verification Checklist

```bash
# Basic checks
make dev_check          # Must pass
make test               # Coverage ≥80%
make contract_compat    # No breaking changes

# Additional for high-risk
make rollback_check PREV_REF=v1.0.0
make security_scan
make performance_test
```

---

## S4 - Documentation Update Details

### Document Update Priority

1. **Critical (Block PR)**:
   - CONTRACT.md / contract.json
   - Migration scripts (up/down)
   - CHANGELOG.md

2. **Important (Same PR)**:
   - TEST_PLAN.md
   - README.md (if API changed)
   - RUNBOOK.md (if ops changed)

3. **Follow-up OK**:
   - PROGRESS.md
   - Performance docs
   - Architecture diagrams

### Documentation Sync Rules

- Code change → Update CONTRACT.md
- Bug fix → Update BUGS.md + CHANGELOG.md
- New feature → Update README.md + CHANGELOG.md
- Performance → Update benchmarks
- Security → Update security.md

---

## S5 - Self-Review & PR Details

### AI-SR Implementation Structure

Generate `/ai/sessions/<date>_<name>/AI-SR-impl.md`:

```markdown
# AI Self-Review: Implementation

## Changes Summary
- Files changed: X
- Lines added: Y
- Lines deleted: Z

## Quality Checklist
- [ ] All tests pass
- [ ] Coverage ≥80%
- [ ] No lint errors
- [ ] Docs updated
- [ ] Contracts compatible

## Risk Assessment
### Identified Risks
1. Risk: [description]
   Mitigation: [how we handled it]

### Rollback Tested
- [ ] Can rollback to previous version
- [ ] Data migration reversible

## PR Description Template
### What
[Concise description]

### Why
[Business/technical reason]

### How
[Technical approach]

### Testing
[How it was tested]

### Breaking Changes
[None | List them]
```

---

## S6 - Auto Maintenance Details

### Maintenance Checklist

```bash
# 1. Update task registry
echo "Task entry" >> ai/LEDGER.md

# 2. Archive workdocs
make workdoc_archive TASK=<name>

# 3. Run maintenance
make ai_maintenance

# 4. Clean temporary files
make cleanup_tmp

# 5. Clean old reports (monthly)
make cleanup_reports_smart
```

### Cleanup Priority

1. **Immediate** (after task):
   - `*_tmp.*` files
   - Debug scripts
   - Test data

2. **Daily**:
   - Old log files
   - Cache files

3. **Weekly**:
   - Old reports (>30 days)
   - Archived workdocs

4. **Monthly**:
   - Full report cleanup
   - Archive review

---

## Quality Gate Details

### CI Gates Configuration

```yaml
# Required checks (block merge)
required:
  - docgen
  - doc_style_check
  - dag_check
  - contract_compat_check
  - runtime_config_check
  - migrate_check
  - consistency_check
  - frontend_types_check
  - agent_lint
  - registry_check
  - doc_route_check

# High-risk additional checks
high_risk:
  - rollback_check
  - security_scan
  - performance_regression
  - data_integrity_check
```

### Test Coverage Requirements

```yaml
coverage:
  global_minimum: 70
  target: 80
  by_module:
    common: 90      # Critical shared code
    auth: 85        # Security critical
    api: 80         # Public interfaces
    ui: 70          # Frontend code
    utils: 75       # Utility functions
```

---

## Command Reference

### Development Commands

```bash
# Module creation
make ai_begin MODULE=<name>          # Initialize module structure

# Development cycle
make dev_check                        # Run all checks
make test MODULE=<name>               # Run module tests
make test_coverage MODULE=<name>      # Check coverage

# Documentation
make docgen                           # Update indexes
make doc_style_check                  # Check doc style
make module_doc_gen MODULE=<name>     # Generate module docs
```

### Maintenance Commands

```bash
# Health checks
make health_check                     # Basic health check
make health_report                    # Detailed report
make health_trend                     # Trend analysis

# Cleanup
make cleanup_tmp                      # Clean temp files
make cleanup_reports AGE=30           # Clean old reports
make cleanup_reports_smart            # Smart cleanup

# Maintenance
make ai_maintenance                   # Full maintenance
make deps_check                       # Check dependencies
make security_scan                    # Security check
```

### Workflow Commands

```bash
# Workdocs
make workdoc_create TASK=<name>       # Create workdoc
make workdoc_list                     # List workdocs
make workdoc_archive TASK=<name>      # Archive workdoc

# Patterns
make workflow_list                    # List patterns
make workflow_suggest PROMPT="..."    # Suggest pattern
make workflow_show PATTERN=<id>       # Show pattern
make workflow_apply PATTERN=<id>      # Apply pattern
```

---

**End of Detailed Documentation**
