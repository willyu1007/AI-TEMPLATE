# AI Index - Quick Reference

> **For AI Agents** - Self-contained essential context (~100 lines)  
> **⚠️ DO NOT auto-load referenced docs** - All essentials included here  
> **Full Details**: Load on-demand via `context_routes` only when needed  
> **Language**: English (AI-optimized)

---

## Core Goals (4) - Complete

### 1. AI-Friendly
**Make AI agents work efficiently**

- **Parseable Docs**: YAML Front Matter + Markdown structure
- **Clear Routes**: `context_routes` in agent.md for on-demand loading
- **Controlled Context**: Layer loading (Tier 0-3), avoid loading everything
- **Schema Standards**: All key docs have schema definitions (schemas/)

**Success Criteria**:
- AI understands project in <5 minutes
- AI finds relevant docs automatically
- AI identifies module boundaries and dependencies

### 2. Modular
**Modules are independent, replaceable, with clear dependencies**

- **Interchangeable**: Same type modules can replace each other (MODULE_TYPES.md)
- **Independent**: Each module has its own agent.md and doc/
- **Stable I/O**: CONTRACT.md defines input/output interfaces
- **Dependencies Declared**: upstream/downstream in agent.md

**Success Criteria**:
- Same-type modules are interchangeable
- Modules can be developed and tested independently
- Dependencies visualized in DAG

### 3. Automated
**Full process verifiable, scriptable, CI-ready**

- **Validation Scripts**: Cover agent.md, registry, doc routes, etc.
- **Generation Scripts**: Auto-generate registry.yaml drafts, MODULE_INSTANCES.md
- **CI Gates**: `make dev_check` aggregates all validations (20 checks)
- **Semi-Automated**: registry.yaml, DB ops require human review

**Success Criteria**:
- All changes validated before merge
- Documentation auto-generated where possible
- CI pipeline enforces quality gates

### 4. Orchestrable
**Auto-discovery, routing, scheduling**

- **Auto-Discovery**: Modules register via agent.md
- **Document Routing**: context_routes for intelligent loading
- **Intelligent Triggers**: agent-triggers.yaml (15 rules, 100% accuracy)
- **Task Scheduling**: Workflow patterns for standard procedures

**Success Criteria**:
- AI discovers modules automatically
- AI loads correct docs for each task
- Standard workflows available for common tasks

---

## Safety Constraints (5) - Critical Rules

### 1. Path Access Control
- ✅ **Read Permission**: context_routes + current module + public docs
- ✅ **Write Permission**: Only paths in ownership.code_paths
- ❌ **Forbidden**: Undeclared paths denied by default
- **Principle**: Principle of least privilege

### 2. Tool & API Calls
- ✅ **Whitelist Mechanism**: Only tools in tools_allowed
- ❌ **Default Deny**: Unlisted tools blocked
- ⚠️ **External API**: Requires security team approval
- **Principle**: Explicit is better than implicit

### 3. Database Operations
- ✅ **Semi-Automated**: AI generates → human reviews → human executes
- ❌ **No Direct DDL**: AI cannot execute CREATE/ALTER/DROP commands
- ✅ **Migration Paired**: Every up.sql must have down.sql
- ✅ **Rollback Ready**: Test rollback with `make rollback_check`
- **Principle**: Human-in-the-loop for critical ops

### 4. Contract Changes
- ⚠️ **Breaking Detection**: Check .contracts_baseline/ automatically
- ⚠️ **Baseline Update**: Run `make update_baselines` after changes
- ❌ **Remove Field**: Blocked, use @deprecated first (keep 1+ release)
- ❌ **Change Type**: Blocked, provide migration guide
- **Principle**: Backward compatibility by default

### 5. Production Configuration
- 🔴 **Blocked**: Direct edit of config/prod.yaml (guardrail)
- ✅ **Required**: Change request + approval + rollback plan
- ✅ **Alternative**: Use environment variables for secrets
- ⚠️ **Staging Config**: Warning level, requires confirmation
- **Principle**: Protect production environment

---

## Quality Requirements (Complete)

### Test Coverage
- **Requirement**: ≥80% for all modules
- **Exception**: Common module ≥90% (infrastructure code)
- **Verification**: Run `pytest --cov` in CI
- **Enforcement**: CI gate blocks merge if below threshold

### Documentation Completeness
**6 Standard Docs per Module**:
1. README.md - Overview and usage
2. CONTRACT.md - API interfaces
3. TEST_PLAN.md - Test strategy
4. RUNBOOK.md - Operations guide
5. CHANGELOG.md - Version history
6. BUGS.md or PROGRESS.md - Issue tracking or progress

### Backward Compatibility
- **New Features**: OK (minor version bump)
- **Modify Signature**: Use @deprecated, keep old version 1+ release
- **Remove API**: Major version only, with migration guide
- **Verification**: `make contract_compat_check`

### Code Standards
- **Naming**: Follow CONVENTIONS.md or AI_CODING_GUIDE.md
- **Style**: Consistent within language (Python: PEP 8, Go: gofmt, TS: ESLint)
- **Complexity**: Keep functions simple, cyclomatic complexity <10
- **Comments**: English for code, Chinese for business logic docs

### CI Gates
- `make dev_check` must pass (20 checks)
- All tests pass
- Test coverage ≥80%
- No linter errors
- High-risk changes need `make rollback_check`

---

## Essential Workflows (6)

### 1. Module Creation
```bash
make ai_begin MODULE=<name>
# Generates: agent.md, README.md, doc/, tests/
# Guide: doc/modules/MODULE_INIT_GUIDE.md
```

### 2. Database Change
```bash
# Read: DB_CHANGE_GUIDE.md (on-demand)
# Create: migrations/<num>_<name>_up.sql + down.sql
# Update: schemas/*.yaml
# Verify: make db_lint, make migrate_check
```

### 3. Contract Update
```bash
# Update: CONTRACT.md
# Check: make contract_compat_check
# Update baseline: make update_baselines
# If breaking: Add migration guide
```

### 4. Dataflow Analysis
```bash
make dataflow_analyze
# Detects: 7 bottleneck types (circular deps, N+1, etc.)
# Visualizes: 3 formats (Mermaid, Graphviz, D3.js)
```

### 5. Task Management
```bash
make workdoc_create TASK=<name>
# Context recovery: 2-5 min (vs 15-30 min)
# Files: plan.md, context.md, tasks.md
```

### 6. Configuration
```bash
# Edit: config/dev.yaml (free)
# Edit: config/staging.yaml (warning)
# Edit: config/prod.yaml (blocked, needs approval)
```

---

## Document Routing (Load Strategy)

### Always Read
- **AI_INDEX.md** - This file only (self-contained)
- **Load time**: On AI startup
- **Token cost**: ~130 tokens

### On-Demand (19 Topics)
Load via `context_routes` based on task:
- **High Priority**: Project overview, goals, safety, module dev, workflows, config, guardrails
- **Medium Priority**: Database ops, testing, triggers, coding standards, dataflow
- **Low Priority**: Directory structure, routing usage, conventions, project init

### Module-Specific
- Load `modules/<name>/agent.md` when working in that module
- Load `modules/<name>/README.md` for quick reference

---

## Quality Gates (Checklist)

**Before Any Change**:
- [ ] Read relevant on-demand docs (context_routes)
- [ ] Update plan.md (scope, risks, rollback)
- [ ] Check guardrails (will this trigger block/warn?)

**During Implementation**:
- [ ] Minimize code changes
- [ ] Maintain backward compatibility
- [ ] Add/update tests (coverage ≥80%)

**Before Commit**:
- [ ] Update all 6 standard docs
- [ ] Run `make dev_check` (must pass)
- [ ] Generate AI-SR (self-review)
- [ ] Clean temp files

---

**Version**: 1.0  
**Last Updated**: 2025-11-09 (Phase 14.0)  
**Token Cost**: ~130 tokens  
**Depth**: 0 (self-contained, no references to load)

---

> **📖 Quick Links** (load on-demand only):  
> - Full goals → goals.md (171 lines)  
> - Full safety → safety.md (233 lines)  
> - Complete workflow → agent.md (356 lines)
