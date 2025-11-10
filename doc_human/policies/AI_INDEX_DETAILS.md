# AI Index - Complete Reference

> **For Humans** - Full detailed documentation  
> **Quick Version**: [AI_INDEX.md](AI_INDEX.md) (120 lines, AI-optimized)  
> **Language**: English

---

## Core Goals (4) - Detailed

### 1. AI-Friendly
**Make AI agents work efficiently**

#### Key Principles
- **Parseable Docs**: YAML Front Matter + Markdown structure
- **Clear Routes**: `context_routes` in agent.md for on-demand loading
- **Controlled Context**: Layer loading (Tier 0-3), avoid loading everything
- **Schema Standards**: All key docs have schema definitions (schemas/)

#### Success Criteria
- AI understands project in <5 minutes
- AI finds relevant docs automatically
- AI identifies module boundaries and dependencies
- AI can navigate 90% of tasks without human clarification

#### Implementation Details
1. **Document Structure**:
   - Every doc starts with YAML front matter
   - Clear sections with ## headers
   - Code examples in fenced blocks
   - Links use relative paths

2. **Routing Strategy**:
   - always_read: Only AI_INDEX.md (self-contained)
   - on_demand: Load based on task relevance
   - priority: high/medium/low for smart loading

3. **Context Control**:
   - Tier 0: AI_INDEX.md only (~130 tokens)
   - Tier 1: + High priority routes (~1000 tokens)
   - Tier 2: + Medium priority routes (~3000 tokens)
   - Tier 3: + Low priority + module-specific (~10000 tokens)

---

### 2. Modular
**Modules are independent, replaceable, with clear dependencies**

#### Key Principles
- **Interchangeable**: Same type modules can replace each other (MODULE_TYPES.md)
- **Independent**: Each module has its own agent.md and doc/
- **Stable I/O**: CONTRACT.md defines input/output interfaces
- **Dependencies Declared**: upstream/downstream in agent.md

#### Success Criteria
- Same-type modules are interchangeable
- Modules can be developed and tested independently
- Dependencies visualized in DAG
- Module replacement takes <1 day

#### Module Types
1. **Data Module**: Handles entity CRUD
2. **Service Module**: Business logic processing
3. **API Module**: External interface
4. **Integration Module**: Third-party connections

#### Contract Requirements
- Input/output schemas defined
- Error codes documented
- Performance SLAs specified
- Backward compatibility guaranteed

---

### 3. Automated
**Full process verifiable, scriptable, CI-ready**

#### Key Principles
- **Validation Scripts**: Cover agent.md, registry, doc routes, etc.
- **Generation Scripts**: Auto-generate registry.yaml drafts, MODULE_INSTANCES.md
- **CI Gates**: `make dev_check` aggregates all validations (21 checks)
- **Semi-Automated**: registry.yaml, DB ops require human review

#### Success Criteria
- All changes validated before merge
- Documentation auto-generated where possible
- CI pipeline enforces quality gates
- Zero-downtime deployments

#### Automation Coverage
- **100% Automated**: Linting, testing, doc validation
- **Semi-Automated**: Registry updates, migrations, contract changes
- **Manual**: Production config, security reviews, architecture decisions

---

### 4. Orchestrable
**Auto-discovery, routing, scheduling**

#### Key Principles
- **Auto-Discovery**: Modules register via agent.md
- **Document Routing**: context_routes for intelligent loading
- **Intelligent Triggers**: agent-triggers.yaml (16 rules, 100% accuracy)
- **Task Scheduling**: Workflow patterns for standard procedures

#### Success Criteria
- AI discovers modules automatically
- AI loads correct docs for each task
- Standard workflows available for common tasks
- Task completion time reduced by 70%

#### Orchestration Features
1. **Smart Triggers**: Detect task type from files/prompt
2. **Workflow Patterns**: 8 standard patterns (module-creation, db-migration, etc.)
3. **Context Recovery**: workdocs for 2-5 min recovery (vs 15-30 min)
4. **Guardrails**: Block/warn/suggest for safety

---

## Safety Constraints (5) - Detailed

### 1. Path Access Control

#### Rules
- ✅ **Read Permission**: context_routes + current module + public docs
- ✅ **Write Permission**: Only paths in ownership.code_paths
- ❌ **Forbidden**: Undeclared paths denied by default
- **Principle**: Principle of least privilege

#### Examples
```yaml
# Good - Declared in ownership
code_paths:
  - modules/example/**
# Can write to modules/example/

# Bad - Not declared
# Cannot write to modules/other/
```

---

### 2. Tool & API Calls

#### Rules
- ✅ **Whitelist Mechanism**: Only tools in tools_allowed
- ❌ **Default Deny**: Unlisted tools blocked
- ⚠️ **External API**: Requires security team approval
- **Principle**: Explicit is better than implicit

#### Tool Categories
1. **Always Allowed**: File read, grep, list_dir
2. **Module-Specific**: Declared in tools_allowed
3. **Never Allowed**: System commands, network access (without approval)

---

### 3. Database Operations

#### Rules
- ✅ **Semi-Automated**: AI generates → human reviews → human executes
- ❌ **No Direct DDL**: AI cannot execute CREATE/ALTER/DROP commands
- ✅ **Migration Paired**: Every up.sql must have down.sql
- ✅ **Rollback Ready**: Test rollback with `make rollback_check`
- **Principle**: Human-in-the-loop for critical ops

#### Workflow
1. AI generates migration scripts
2. Human reviews for correctness
3. Human runs `make migrate_check`
4. Human executes migration
5. Rollback tested before production

---

### 4. Contract Changes

#### Rules
- ⚠️ **Breaking Detection**: Check .contracts_baseline/ automatically
- ⚠️ **Baseline Update**: Run `make update_baselines` after changes
- ❌ **Remove Field**: Blocked, use @deprecated first (keep 1+ release)
- ❌ **Change Type**: Blocked, provide migration guide
- **Principle**: Backward compatibility by default

#### Breaking Changes (Forbidden)
- Removing fields
- Changing field types
- Renaming fields (without alias)
- Adding required fields

#### Non-Breaking Changes (Allowed)
- Adding optional fields
- Adding new endpoints
- Deprecating (with @deprecated tag)

---

### 5. Production Configuration

#### Rules
- 🔴 **Blocked**: Direct edit of config/prod.yaml (guardrail)
- ✅ **Required**: Change request + approval + rollback plan
- ✅ **Alternative**: Use environment variables for secrets
- ⚠️ **Staging Config**: Warning level, requires confirmation
- **Principle**: Protect production environment

#### Config Hierarchy
1. **Dev**: Free to edit
2. **Staging**: Warning, requires confirmation
3. **Production**: Blocked, needs formal approval process

---

## Quality Requirements (Detailed)

### Test Coverage

#### Requirements
- **Minimum**: ≥80% for all modules
- **Common Module**: ≥90% (infrastructure code)
- **New Code**: 100% for new features
- **Legacy Code**: Improve gradually, no decrease

#### Verification
```bash
pytest --cov=modules --cov-report=term --cov-fail-under=80
```

#### CI Enforcement
- Blocks merge if below threshold
- Reports coverage trend
- Highlights uncovered lines

---

### Documentation Completeness

#### 8 Standard Docs per Module
1. **README.md** - Overview and usage (for humans)
2. **agent.md** - Orchestration config (for AI)
3. **CONTRACT.md** - API interfaces
4. **TEST_PLAN.md** - Test strategy
5. **RUNBOOK.md** - Operations guide
6. **CHANGELOG.md** - Version history
7. **BUGS.md** - Issue tracking
8. **PROGRESS.md** - Development progress

#### Verification
```bash
make module_health_check
# Checks all 8 docs present and up-to-date
```

---

### Backward Compatibility

#### Rules
- **New Features**: OK (minor version bump)
- **Modify Signature**: Use @deprecated, keep old version 1+ release
- **Remove API**: Major version only, with migration guide
- **Verification**: `make contract_compat_check`

#### Deprecation Process
1. Add @deprecated tag with removal version
2. Update docs with migration guide
3. Keep deprecated version for 1+ release
4. Remove in next major version

---

### Code Standards

#### Naming Conventions
- **Files**: snake_case for Python, kebab-case for configs
- **Functions**: snake_case (Python), camelCase (TS/JS)
- **Classes**: PascalCase
- **Constants**: UPPER_SNAKE_CASE

#### Style Guidelines
- **Python**: PEP 8
- **Go**: gofmt
- **TypeScript**: ESLint + Prettier
- **YAML**: 2-space indent

#### Complexity
- Keep functions simple
- Cyclomatic complexity <10
- Function length <50 lines
- Class length <500 lines

#### Comments
- **Code**: English
- **Business Logic**: Chinese OK
- **APIs**: English (for international use)

---

### CI Gates

#### Required Checks (21)
1. docgen
2. doc_style_check
3. agent_lint
4. registry_check
5. doc_route_check
6. type_contract_check
7. doc_script_sync_check
8. db_lint
9. resources_check
10. dag_check
11. contract_compat_check
12. deps_check
13. runtime_config_check
14. migrate_check
15. consistency_check
16. frontend_types_check
17. doc_freshness_check
18. coupling_check
19. observability_check
20. secret_scan
21. test_coverage

#### High-Risk Changes
Additional check: `make rollback_check`

---

## Essential Workflows (Detailed)

### 1. Module Creation

#### Command
```bash
make ai_begin MODULE=<name>
```

#### What It Does
- Creates directory structure
- Generates 8 standard docs (templates)
- Sets up test scaffolding
- Registers in registry.yaml (draft)

#### Files Generated
```
modules/<name>/
├── agent.md
├── README.md
├── doc/
│   ├── CONTRACT.md
│   ├── CHANGELOG.md
│   ├── RUNBOOK.md
│   ├── BUGS.md
│   ├── PROGRESS.md
│   └── TEST_PLAN.md
└── tests/
    └── test_<name>.py
```

#### Next Steps
1. Read: doc/modules/MODULE_INIT_GUIDE.md
2. Define type in MODULE_TYPES.md
3. Implement CONTRACT.md
4. Write tests
5. Update registry.yaml

---

### 2. Database Change

#### Guide
Read: DB_CHANGE_GUIDE.md (on-demand)

#### Steps
1. **Design**: Plan schema changes
2. **Create Migrations**:
   ```bash
   migrations/001_add_users_up.sql
   migrations/001_add_users_down.sql
   ```
3. **Update Schemas**:
   ```bash
   db/engines/postgres/schemas/tables/users.yaml
   ```
4. **Verify**:
   ```bash
   make db_lint
   make migrate_check
   make rollback_check PREV_REF=main
   ```

#### Guardrails
- AI generates SQL → Human reviews → Human executes
- Must have both up and down scripts
- Must test rollback before production

---

### 3. Contract Update

#### Steps
1. **Update CONTRACT.md**
2. **Check Compatibility**:
   ```bash
   make contract_compat_check
   # Detects breaking changes
   ```
3. **If Non-Breaking**:
   ```bash
   make update_baselines
   ```
4. **If Breaking**:
   - Add @deprecated tag
   - Write migration guide
   - Plan for next major version

---

### 4. Dataflow Analysis

#### Command
```bash
make dataflow_analyze
```

#### What It Detects (7 Bottleneck Types)
1. 🔴 Circular dependencies (Critical)
2. 🟠 Deep call chains (High)
3. 🟠 N+1 queries (High)
4. 🟡 Missing indexes (Medium)
5. 🟡 Parallelization opportunities (Medium)
6. 🟢 Cache recommendations (Low)
7. 🟢 Duplicate computations (Low)

#### Visualization Formats
- **Mermaid**: Lightweight, embeddable
- **Graphviz DOT**: Professional quality
- **D3.js HTML**: Interactive, drag-and-drop

---

### 5. Task Management (Workdocs)

#### Command
```bash
make workdoc_create TASK=<name>
```

#### Benefits
- Context recovery: 2-5 min (vs 15-30 min manual)
- Structured approach: plan → implement → review
- History tracking: archive for future reference

#### Files Created
```
ai/workdocs/active/<task>/
├── plan.md      # Scope, risks, rollback
├── context.md   # Current state, decisions
└── tasks.md     # Checklist, progress
```

#### Lifecycle
1. **Create**: `make workdoc_create`
2. **Update**: Edit files during work
3. **Archive**: `make workdoc_archive` when done

---

### 6. Configuration Management

#### Files
- `config/dev.yaml` - Free to edit
- `config/staging.yaml` - Warning level
- `config/prod.yaml` - Blocked by guardrail

#### Editing
```bash
# Dev - No restrictions
vim config/dev.yaml

# Staging - Warning
vim config/staging.yaml
# ⚠️ Confirm: Are you sure? [y/N]

# Production - Blocked
vim config/prod.yaml
# 🔴 BLOCKED: Use change request process
```

#### Secrets Management
- NEVER commit secrets
- Use environment variables
- Use secret management service
- Rotate regularly (every 90 days)

---

## Document Routing (Detailed)

### Always Read (Tier 0)
- **Files**: AI_INDEX.md only
- **Load Time**: On AI startup
- **Token Cost**: ~130 tokens
- **Content**: Self-contained essentials

### High Priority (Tier 1)
Load when task highly relevant:
- Project Overview (README.md)
- Full Goals & Safety (goals.md, safety.md)
- Module Development (MODULE_TYPES.md, MODULE_INIT_GUIDE.md)
- Database Operations (DB_SPEC.yaml, DB_CHANGE_GUIDE.md)
- Configuration (CONFIG_GUIDE.md)
- Guardrails (guardrail-quickstart.md)
- Workflow Patterns (workflow-patterns/)

### Medium Priority (Tier 2)
Load when mentioned in prompt:
- Testing Standards (testing.md)
- Intelligent Triggers (agent-triggers.yaml)
- Coding Standards (AI_CODING_GUIDE.md)
- Dataflow Analysis (dataflow-quickstart.md)
- Mock Data (MOCK_RULES.md)
- Health Monitoring (health-summary.md)

### Low Priority (Tier 3)
Only if explicitly requested:
- Directory Structure (directory.md)
- Conventions (CONVENTIONS.md)
- Project Initialization (PROJECT_INIT_GUIDE.md)

### Module-Specific
Load when working in module:
- `modules/<name>/agent.md`
- `modules/<name>/README.md`
- `modules/<name>/doc/CONTRACT.md`

---

## Quality Gates (Detailed Checklist)

### Before Any Change

#### 1. Context Loading
- [ ] Read AI_INDEX.md (always loaded)
- [ ] Identify task type (module? database? config?)
- [ ] Load relevant on-demand docs via context_routes
- [ ] Check if similar task done before (CHANGELOG, workdocs/archive)

#### 2. Planning
- [ ] Create or update plan.md
- [ ] Define scope clearly
- [ ] Identify risks
- [ ] Plan rollback strategy
- [ ] Estimate impact (breaking? high-risk?)

#### 3. Guardrail Check
- [ ] Will this trigger any blocks?
- [ ] Will this trigger any warnings?
- [ ] Do I need special approval?
- [ ] Is rollback tested?

---

### During Implementation

#### 4. Code Changes
- [ ] Minimize changes (smallest diff possible)
- [ ] Maintain backward compatibility
- [ ] Follow code standards (PEP 8, gofmt, ESLint)
- [ ] Keep complexity low (CC <10)

#### 5. Testing
- [ ] Add unit tests (coverage ≥80%)
- [ ] Add integration tests if needed
- [ ] Test edge cases
- [ ] Test error scenarios

#### 6. Documentation
- [ ] Update README.md if behavior changes
- [ ] Update CONTRACT.md if API changes
- [ ] Update CHANGELOG.md
- [ ] Update RUNBOOK.md if ops impact

---

### Before Commit

#### 7. Validation
- [ ] Run `make dev_check` (must pass all 21 checks)
- [ ] Check test coverage: `pytest --cov`
- [ ] Check linter: `pylint`, `mypy`
- [ ] Check contracts: `make contract_compat_check`

#### 8. Documentation Complete
- [ ] All 8 standard docs updated
- [ ] No broken links
- [ ] No TODO comments (move to BUGS.md or tasks.md)
- [ ] Code comments in English

#### 9. Self-Review
- [ ] Generate AI-SR (AI self-review)
- [ ] Check diff one more time
- [ ] Verify no secrets committed
- [ ] Clean temp files: `make cleanup_tmp`

#### 10. Commit
- [ ] Write clear commit message
- [ ] Reference issue/task if applicable
- [ ] Push and create PR
- [ ] Request human review if high-risk

---

## Health Monitoring

### 5 Dimensions (100 points)

1. **Code Quality** (25 points)
   - Linter pass rate (8)
   - Test coverage (10)
   - Code complexity (4)
   - Type safety (3)

2. **Documentation** (20 points)
   - Module doc coverage (8)
   - Doc freshness (5)
   - Doc quality (4)
   - Doc sync (3)

3. **Architecture** (20 points)
   - Dependency clarity (6)
   - Module coupling (6)
   - Contract stability (4)
   - Registry consistency (4)

4. **AI Friendliness** (20 points) ⭐
   - agent.md lightweight (5)
   - Doc role clarity (5)
   - Module doc complete (4)
   - Workflow AI-friendly (3)
   - Script automation (3)

5. **Operations** (15 points)
   - Migration completeness (5)
   - Config compliance (3)
   - Observability coverage (4)
   - Security hygiene (3)

### Commands
```bash
make health_check              # Full check
make health_check_strict       # Zero-tolerance mode
make health_report_detailed    # Detailed report
make health_analyze_issues     # Issue aggregation
make health_show_quick_wins    # Quick improvements
```

---

**Version**: 1.0  
**Last Updated**: 2025-11-09  
**Status**: Complete reference (for humans)  
**AI Version**: [AI_INDEX.md](AI_INDEX.md) (120 lines)

