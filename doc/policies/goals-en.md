---
audience: ai
language: en
version: summary
purpose: Core goals and design principles for AI-TEMPLATE project
chinese_version: /doc/policies/goals.md
---

# Global Goals and Design Principles

> **Purpose**: Define core objectives and design principles for AI-TEMPLATE project  
> **Version**: 1.0  
> **Created**: 2025-11-07

---

## Four Core Goals

### 1. AI-Friendly
**Goal**: Enable AI agents to efficiently understand and operate the project

**Implementation**:
- **Parseable Docs**: Use YAML Front Matter + Markdown
- **Clear Routing**: Load docs on-demand via `context_routes`
- **Controlled Context**: Layered loading, avoid loading everything at once
- **Schema Standards**: All key docs have schema definitions (schemas/)

**Success Criteria**:
- ✅ AI understands project structure in <5 minutes
- ✅ AI automatically finds relevant docs
- ✅ AI identifies module boundaries and dependencies

---

### 2. Modular
**Goal**: Modules are independent, replaceable, with clear dependencies

**Implementation**:
- **Interchangeable Types**: MODULE_TYPES.md defines type specifications
- **Independent Instances**: Each module has its own agent.md and doc/
- **Stable I/O**: CONTRACT.md defines input/output contracts
- **Explicit Dependencies**: agent.md declares upstream/downstream

**Success Criteria**:
- ✅ Same-type modules are interchangeable (e.g., different Select implementations)
- ✅ Modules can be developed and tested independently
- ✅ Dependencies visualized in DAG

---

### 3. Automated
**Goal**: Full process validation, scriptable, CI-ready

**Implementation**:
- **Validation Scripts**: Cover agent.md, registry, doc routes, etc.
- **Generation Scripts**: Auto-generate registry.yaml drafts, MODULE_INSTANCES.md
- **CI Gates**: `make dev_check` aggregates all validations (21 checks)
- **Semi-Automated**: registry.yaml and database operations require human review

**Success Criteria**:
- ✅ CI detects non-compliant docs and code
- ✅ Registry auto-updates when adding modules
- ✅ Database operations require human review before execution

---

### 4. Orchestrable
**Goal**: Support AI agent auto-discovery, merging, and scheduling

**Implementation**:
- **Registry**: doc/orchestration/registry.yaml maintains module relationships
- **Routing Rules**: doc/orchestration/routing.md defines loading strategy
- **Orchestration Hints**: orchestration_hints in agent.md guide scheduling
- **Priority**: Control scheduling order via priority field

**Success Criteria**:
- ✅ Orchestrator auto-discovers all modules
- ✅ Selects appropriate modules based on task type
- ✅ Supports data flow between modules

---

## Design Principles

### Principle 1: Explicit Over Implicit
- Declare dependencies explicitly (don't rely on code scanning)
- Grant permissions explicitly (ownership.code_paths)
- List constraints explicitly

### Principle 2: Documentation-Driven Development
- Write agent.md and CONTRACT.md first
- Then write code
- Keep docs and code in sync

### Principle 3: Principle of Least Privilege
- Deny unauthorized writes by default
- Tool calls require whitelist (tools_allowed)
- Network access requires explicit request

### Principle 4: Progressive Validation
- **Development**: Warning mode (allows incomplete)
- **Commit**: Strict mode (CI gates)
- **Production**: Enforced mode (must be complete)

### Principle 5: Layered Architecture
```
Application Layer (app/frontend/)
    ↓
Business Module Layer (modules/<entity>/)
    ↓
Common Layer (common/)
    ↓
Infrastructure Layer (db/, config/, observability/)
```

---

## Quality Goals

### Documentation Quality
- All modules have agent.md and complete doc/ subdirectory
- agent.md passes schema validation
- All doc route paths are valid

### Code Quality
- Test coverage ≥80% (modules can configure higher)
- All APIs have CONTRACT.md
- Pass consistency checks

### Maintenance Quality
- CHANGELOG.md records all changes
- Compatibility checks pass
- Dependencies are clear

---

## Non-Goals

Explicitly **NOT doing**:

❌ **Not Pursuing 100% Automation**
- registry.yaml requires human review
- Database operations require human confirmation
- Critical decisions require human involvement

❌ **Not Over-Engineering**
- Don't introduce complex frameworks
- Don't over-abstract
- Keep it simple and understandable

❌ **Not Mandating Tech Stack**
- Support multiple languages (Python/Go/TypeScript)
- Modules can choose appropriate technology
- Don't restrict implementation approaches

---

## Goal Achievement Acceptance

Goals are considered achieved when:

### Phase Acceptance (Phase 0-9)
- ✅ Phase 1: Schema and infrastructure (completed)
- ⏳ Phase 2: Directory structure adjustment (in progress)
- ⏳ Phase 3-9: To be executed

### Overall Acceptance
- [ ] All modules have agent.md (with YAML Front Matter)
- [ ] registry.yaml formalized and validated
- [ ] Root agent.md lightweight (≤350 lines)
- [ ] All doc route paths valid
- [ ] All CI gates pass
- [ ] Initialization guide complete

---

**Maintenance**: Update this document when project goals change, with team review  
**Related**: doc/policies/safety.md, doc/orchestration/routing.md

