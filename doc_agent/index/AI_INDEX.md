# AI Index - Quick Reference

> **For AI Agents** - Self-contained essential context (~120 lines)  
> **⚠️ DO NOT auto-load referenced docs** - All essentials included here  
> **Full Details**: [AI_INDEX_DETAILS.md](AI_INDEX_DETAILS.md) (for humans)  
> **Language**: English (AI-optimized)

---

## Core Goals (4)

### 1. AI-Friendly
Make AI agents work efficiently with parseable docs, clear routes, and controlled context loading.

### 2. Modular
Modules are independent and replaceable with stable I/O defined in CONTRACT.md.

### 3. Automated
Full validation via `make dev_check` (21 checks). CI-ready with semi-automated critical ops.

### 4. Orchestrable
Auto-discovery via agent.md, intelligent triggers (16 rules), and workflow patterns (8 standard).

---

## Safety Constraints (5 Critical Rules)

### 1. Path Access
- ✅ Read: context_routes + current module
- ✅ Write: Only ownership.code_paths
- ❌ Other paths: Denied

### 2. Tools & APIs
- ✅ Whitelist only (tools_allowed)
- ❌ Default deny

### 3. Database Ops
- ✅ AI generates → Human reviews → Human executes
- ❌ No direct DDL
- ✅ Every up.sql needs down.sql

### 4. Contracts
- ⚠️ Breaking detection: auto-check .contracts_baseline/
- ❌ Remove field/change type: Blocked
- ✅ Use @deprecated for 1+ release first

### 5. Production Config
- 🔴 config/prod.yaml: Blocked (needs approval)
- ⚠️ config/staging.yaml: Warning
- ✅ config/dev.yaml: Free

---

## Essential Workflows (7)

### 0. Lifecycle Overview
```bash
load /doc_agent/flows/repo-lifecycle.md  # Stage map + handoff rules
```

### 1. Initialization
```bash
# Read protocols before scaffolding
load /doc_agent/init/project-init.md
load /doc_agent/init/module-init.md

make ai_begin MODULE=<name>  # Generates 8 docs + tests
```

### 2. Database Change
```bash
# Create: migrations/*_up.sql + *_down.sql
# Update: schemas/*.yaml
# Verify: make db_lint && make migrate_check
```

### 3. Contract Update
```bash
make contract_compat_check  # Detect breaking changes
make update_baselines       # If non-breaking
```

### 4. Dataflow Analysis
```bash
make dataflow_analyze  # Detect 7 bottleneck types
```

### 5. Task Management
```bash
make workdoc_create TASK=<name>  # Context recovery: 2-5min
```

### 6. Health Check
```bash
make health_check        # 5-dimension check (100 points)
make health_show_quick_wins  # Quick improvements
```

### 7. Maintenance Loop
```bash
load /doc_agent/flows/maintenance-loop.md
make health_report_detailed
```

---

## Key Commands

### Validation (Run before commit)
```bash
make dev_check           # All 21 checks (CI gate)
make agent_lint          # Validate agent.md
make contract_compat_check  # Check API changes
make rollback_check      # Test rollback (high-risk changes)
```

### Generation
```bash
make docgen              # Generate doc indexes
make registry_gen        # Draft registry.yaml
make workflow_suggest PROMPT="task"  # Suggest workflow pattern
```

### Analysis
```bash
make dataflow_visualize FORMAT=html  # Interactive visualization
make health_analyze_issues           # Issue aggregation
make coupling_check                  # Module coupling analysis
```

---

## Document Loading Strategy

### Always Read (Automatic)
- **This file only** (AI_INDEX.md)
- **Token cost**: ~130 tokens

### On-Demand (Load via context_routes)
- **High priority**: goals.md, safety.md, MODULE_TYPES.md, DB_SPEC.yaml, guardrails, flows/repo-lifecycle.md
- **Medium priority**: testing.md, triggers.yaml, AI_CODING_GUIDE.md, dataflow
- **Low priority**: CONVENTIONS.md, directory.md (rarely needed)

### Module-Specific
- Load `modules/<name>/agent.md` when working in that module

---

## Quality Standards

### Required
- Test coverage ≥80% (common module ≥90%)
- All 8 docs per module: README, agent.md, CONTRACT, TEST_PLAN, RUNBOOK, CHANGELOG, BUGS, PROGRESS
- Backward compatible (use @deprecated for changes)
- CI must pass (`make dev_check`)

### Standards
- Python: PEP 8, complexity <10
- Go: gofmt
- TypeScript: ESLint
- Comments: English

---

## Quick Links (Load on-demand only)

- **Full Goals**: goals.md (171 lines)
- **Full Safety**: safety.md (233 lines)
- **Complete Workflows**: agent.md (350 lines)
- **Module Development**: MODULE_INIT_GUIDE.md (~25 lines + linked templates)
- **Initialization Protocols**: init/project-init.md & init/module-init.md (load before scaffolding)
- **Maintenance Loop**: flows/maintenance-loop.md (post-release cadence)
- **Database Changes**: DB_CHANGE_GUIDE.md (split into resources/)
- **Full Reference**: [AI_INDEX_DETAILS.md](AI_INDEX_DETAILS.md) (complete version)

---

**Version**: 2.0  
**Last Updated**: 2025-11-09 (Phase 14.3 optimization)  
**Token Cost**: ~130 tokens  
**Lines**: 120 (target met ✅)
