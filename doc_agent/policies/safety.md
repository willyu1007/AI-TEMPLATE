---
audience: ai
language: en
version: summary
purpose: Safety constraints and quality standards (quick reference)
chinese_version: /doc/policies/safety.md
---

# Safety & Quality Standards

> **Purpose**: Define safety constraints and quality requirements (core principles)  
> **Version**: 2.1  
> **Created**: 2025-11-07  
> **Last Updated**: 2025-11-09 (Phase 14.3 optimization)

---

## Quick Reference

### Safety Constraints Quick Lookup

| Category | Principle | Details |
|----------|-----------|---------|
| **Path Access** | Read: context_routes, Write: ownership scope | security.md § 1 |
| **Tool Calls** | Whitelist mechanism, default deny | security.md § 2 |
| **Database Ops** | Semi-automated, human review | security.md § 3 |
| **Network Access** | Default deny, explicit declaration | security.md § 4 |

### Quality Standards Quick Lookup

| Category | Requirement | Details |
|----------|-------------|---------|
| **Test Coverage** | ≥80% | quality.md § 1 |
| **Doc Completeness** | 8 standard docs | quality.md § 2 |
| **Compatibility** | Backward compatible | quality.md § 3 |
| **Code Standards** | Naming + style + complexity | quality.md § 4 |

---

## 1. Safety Constraints

### 1.1 Path Access Control
- ✅ **Read Permission**: context_routes + current module + public docs
- ✅ **Write Permission**: Only paths declared in ownership.code_paths
- ❌ **No Unauthorized Access**: Undeclared paths denied by default

**Details**: `doc/policies/security.md` § 1

### 1.2 Tool & API Call Restrictions
- ✅ **Whitelist Mechanism**: Only tools declared in tools_allowed
- ❌ **Default Deny**: Undeclared tool calls intercepted
- ⚠️ **External API Requires Approval**: External network access needs security team approval

**Details**: `doc/policies/security.md` § 2

### 1.3 Database Safety
- ✅ **Semi-Automated**: AI generates + human reviews + human executes
- ❌ **No Direct DDL**: AI cannot directly execute CREATE/ALTER/DROP
- ⚠️ **Paired Migrations**: Every up.sql must have corresponding down.sql

**Details**: `doc/policies/security.md` § 3

### 1.4 Network Access Control
- ❌ **Default Deny**: Modules cannot access network by default
- ✅ **Explicit Declaration**: Must declare in tools_allowed when needed
- ⚠️ **Domain Whitelist**: Only allowed domains can be accessed

**Details**: `doc/policies/security.md` § 4

---

## 2. Quality Gates

### 2.1 Test Requirements
- ✅ **Required Tests**: Unit, integration, contract tests
- ✅ **Coverage**: ≥80% (configurable higher)
- **Validation**: `make test_coverage`

**Details**: `doc/policies/quality.md` § 1

### 2.2 Documentation Requirements
- ✅ **Required Docs**: 8 standard docs (README, agent.md, CONTRACT, CHANGELOG, RUNBOOK, BUGS, PROGRESS, TEST_PLAN)
- ✅ **Sync**: Code changes must update relevant docs
- **Validation**: `make consistency_check`

**Details**: `doc/policies/quality.md` § 2

### 2.3 Compatibility Requirements
- ✅ **API Compatibility**: No field removal, no type changes, no semantic changes
- ✅ **Database Compatibility**: Paired migration scripts, pass rollback tests
- **Validation**: `make contract_compat_check`, `make rollback_check`

**Details**: `doc/policies/quality.md` § 3

### 2.4 Code Standards
- ✅ **Naming**: Modules (snake_case), classes (PascalCase), functions (snake_case/camelCase), constants (UPPER_SNAKE_CASE)
- ✅ **Documentation**: Consistent language, no emoji, structured
- **Validation**: `make doc_style_check`

**Details**: `doc/policies/quality.md` § 4

---

## 3. Violation Handling

### 3.1 Staged Gates

**Development Stage** (Warning mode):
- Non-compliant → Display warning
- Allow continued development
- Prompt for fixes

**Commit Stage** (Strict mode):
- CI gate checks
- Fail → Block merge
- Must fix before resubmit

**Production Stage** (Enforced mode):
- Pre-deployment final check
- Any violation → Block deployment
- Human review for critical changes

---

### 3.2 CI Gates

**Must Pass Checks**:
```bash
make dev_check     # Aggregates 21 checks
pytest tests/      # All tests pass
# Coverage ≥80%    # Test coverage meets threshold
```

**Additional Checks for High-Risk Changes**:
```bash
make rollback_check    # Database changes must pass rollback test
make contract_compat_check  # API changes must be non-breaking
```

---

## 4. Exemption Mechanism

### 4.1 When to Request

**Applicable Scenarios**:
- Prototype validation phase (temporarily relax test coverage)
- Emergency fixes (skip some processes)
- Technical limitations (temporarily cannot meet)
- Migration transition period (new standards not fully adopted)

**Not Applicable**:
- ❌ Long-term bypass of standards
- ❌ Core security rules
- ❌ Data security related

---

### 4.2 Request Process

**Configure in agent.md**:
```yaml
exemptions:
  - rule: "coverage_min"
    reason: "Prototype validation phase"
    current_value: 0.60
    standard_value: 0.80
    expiry: "2025-12-31"
    approved_by: "tech_lead"
```

**Review Points**:
- ✅ Is exemption reason sufficient?
- ✅ Is exemption scope minimized?
- ✅ Is expiry date reasonable?
- ✅ Is there a fix plan?

**Expiry Handling**:
- Automatically expires after due date
- CI will report error
- Renewal requires new request

**Details**: `doc/policies/security.md` § 5

---

## 5. Audit & Monitoring

### 5.1 Audit Scope

**Recorded Content**:
- File operations (read/write/delete)
- Tool calls (http/db/shell)
- Database operations (DDL/DML/DQL)
- Unauthorized attempts (intercepted records)

**Details**: `doc/policies/security.md` § 6

---

### 5.2 Monitoring Metrics

**Key Metrics**:
- Documentation coverage (agent.md, CONTRACT.md presence rate)
- Test coverage (≥80% compliance rate)
- Validation pass rate (dev_check pass rate)
- Violation count (unauthorized attempts, tool misuse)

**Report Generation**:
```bash
make health_check
# Output: Failed checks, missing docs, issues to fix
```

**Details**: `doc/policies/security.md` § 6

---

## 6. Related Resources

### Core Policies
- **Global Goals**: doc/policies/goals-en.md
- **Roles & Gates**: doc/policies/roles.md

### Detailed Standards
- **Security Details**: doc/policies/security.md (path control, tool restrictions, audit monitoring)
- **Quality Standards**: doc/policies/quality.md (testing, documentation, compatibility, code standards)

### Process Guides
- **Database Changes**: doc/process/DB_CHANGE_GUIDE.md
- **PR Workflow**: doc/process/pr_workflow.md
- **Testing Standards**: doc/process/testing.md

### Tool Reference
- **Routing Rules**: doc/orchestration/routing.md
- **Project Initialization**: doc/init/PROJECT_INIT_GUIDE.md
- **Module Initialization**: doc/modules/MODULE_INIT_GUIDE.md

---

**Maintenance**: Update this document and detailed specs when new security risks are discovered  
**Review**: Quarterly review by security team

