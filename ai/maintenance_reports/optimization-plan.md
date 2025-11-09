# Project Optimization Plan

> **Based on**: project-audit-report.md  
> **Priority**: P0 (Critical) - Immediate execution  
> **Estimated Effort**: 16-20 hours

---

## 🎯 Phase 1 Critical Optimizations (P0)

### Task 1: Compress AI_INDEX.md (238 → 120 lines) ⚡

**Current**: 238 lines (58% over target)  
**Target**: 120 lines  
**Reduction**: -118 lines (-50%)

**Action Plan**:

1. **Core Goals section** (53 lines → 20 lines):
   - Remove detailed bullets, keep 1-liner summary
   - Remove "Success Criteria" subsections
   - Keep essence only

2. **Safety Constraints** (34 lines → 25 lines):
   - Keep all 5 rules (critical for safety)
   - Compress descriptions to 3-4 lines each

3. **Quality Requirements** (30+ lines → REMOVE):
   - Move to separate doc: `AI_INDEX_DETAILS.md`

4. **Essential Workflows** (40+ lines → 15 lines):
   - Title + command only
   - Remove descriptions

5. **Document Routing** (30+ lines → REMOVE):
   - Already in agent.md, redundant

6. **Quality Gates** (20+ lines → REMOVE):
   - Move to HEALTH_CHECK_MODEL.yaml

**New Structure** (120 lines):
```
Header (7 lines)
Core Goals (20 lines) - 4 goals × 5 lines
Safety Constraints (25 lines) - 5 rules × 5 lines
Essential Workflows (15 lines) - 6 workflows × 2.5 lines
Key Commands (20 lines)
Quick Reference Links (10 lines)
Footer (3 lines)
Whitespace/formatting (20 lines)
---
Total: 120 lines
```

**Files to Create**:
- `doc/policies/AI_INDEX_DETAILS.md` - Full version with all content

---

### Task 2: Optimize agent.md Routes (404 → 350 lines) ⚡

**Current**: 404 lines (15% over target)  
**Target**: 350 lines  
**Reduction**: -54 lines (-13%)

**Action Plan**:

**2.1 Remove Redundant Routes** (-30 lines):
```yaml
# REMOVE (已有quickstart版本):
- topic: "Workdocs Task Management"
  paths:
    - /doc/process/WORKDOCS_GUIDE.md  # Remove, keep quickstart only
    
- topic: "Guardrail Protection Mechanism"
  paths:
    - /doc/process/GUARDRAIL_GUIDE.md  # Remove, keep quickstart only
    
- topic: "Dataflow Analysis"
  paths:
    - /doc/process/DATAFLOW_ANALYSIS_GUIDE.md  # Remove, keep quickstart only
```

**2.2 Merge Similar Routes** (-15 lines):
```yaml
# BEFORE (2 routes):
- topic: "Module Development"
  ...
- topic: "Detailed Module Development"
  ...

# AFTER (1 route):
- topic: "Module Development"
  priority: high
  paths:
    - /doc/modules/MODULE_TYPES.md
    - /doc/modules/MODULE_INIT_GUIDE.md  # Combined
```

**2.3 Remove Low-value Routes** (-9 lines):
```yaml
# REMOVE:
- topic: "Documentation Routing Usage"  # Meta, rarely used
- topic: "Project Initialization"  # Rarely used after setup
```

**New Route Count**:
- Current: 28 routes
- Target: 22 routes (-6 routes, -21%)

---

### Task 3: Create AI/Human Doc Splits ⚡

**Priority Documents** (Create lightweight AI versions):

| Document | Current | AI Version | Human Version |
|----------|---------|------------|---------------|
| MOCK_RULES_GUIDE.md | 836 lines | MOCK_RULES.md (150 lines) | MOCK_RULES_GUIDE.md (keep) |
| HEALTH_MONITORING_GUIDE.md | 565 lines | health-summary.md (103 lines, ✅ exists) | HEALTH_MONITORING_GUIDE.md (keep) |
| security_details.md | 537 lines | security.md (120 lines) | security_details.md (keep) |
| quality_standards.md | 402 lines | quality.md (100 lines) | quality_standards.md (keep) |
| MODULE_INIT_GUIDE.md | 1049 lines | ✅ Already split (resources/) | (keep) |

**Template for AI Version**:
```markdown
---
audience: ai
language: en
version: summary
purpose: Quick reference for AI agents
full_version: /doc/path/to/complete.md
---

# Title

> **For AI Agents** - Essential info only (~150 lines)
> **Full Details**: See [complete version](full_version.md)

## Core Concepts (3-5 items)
...

## Quick Commands
```bash
make command1
make command2
```

## Key Rules (3-5 rules)
...

## Related Docs
- Full version: [link]
- Related: [link]
```

---

### Task 4: Englishize Critical AI Docs ⚡

**Phase 1 - Core AI Docs** (P0):

| Chinese Doc | English Version | Priority | Lines |
|------------|-----------------|----------|-------|
| goals.md | goals-en.md | 🔴 P0 | 171 |
| safety.md | safety-en.md | 🔴 P0 | 233 |
| DOC_ROLES.md | DOC_ROLES-en.md | 🔴 P0 | 306 |
| DB_SPEC.yaml | DB_SPEC-en.yaml | 🔴 P0 | - |
| MODULE_TYPES.md | MODULE_TYPES-en.md | 🔴 P0 | - |

**Translation Guidelines**:
1. Keep structure identical
2. Translate content accurately
3. Keep code examples as-is
4. Keep formatting
5. Update agent.md routes to new paths

---

### Task 5: Add Doc Audience Headers ⚡

**Add to ALL documents**:
```yaml
---
audience: ai | human | both
language: en | zh
version: summary | complete
purpose: [one-line description]
related:
  full_version: /path/to/complete.md
  ai_version: /path/to/summary.md
---
```

**Priority**:
1. P0: All docs in agent.md routes
2. P1: All docs in /doc/policies/
3. P2: All docs in /doc/process/
4. P3: All other docs

---

### Task 6: Update agent.md Rules ⚡

**Add to § 1.2**:
```markdown
## §1.2 Context Loading Rules

**AI MUST**:
- Only read `always_read` docs automatically
- Skip routes marked `audience: human`
- Skip routes marked `skip_for_ai: true`
- Load `priority: high` only when task highly relevant
- Load `priority: medium` only when explicitly mentioned
- NEVER auto-load `priority: low`
- Always check `audience` field in doc header

**Loading Priority**:
1. always_read (automatic)
2. priority: high + task-relevant
3. priority: medium + mentioned-in-prompt
4. priority: low (only if explicitly requested)

**Skip Conditions**:
- `audience: human`
- `skip_for_ai: true`
- `language: zh` (unless README.md)
```

---

## 📊 Expected Impact

### Metrics Improvement:

| Metric | Before | After P1 | Improvement |
|--------|--------|----------|-------------|
| AI_INDEX.md | 238 lines | 120 lines | -50% |
| agent.md | 404 lines | 350 lines | -13% |
| Route count | 28 | 22 | -21% |
| AI docs in English | 20% | 40% | +100% |
| Docs with audience | 10% | 80% | +700% |
| AI Token cost | 100% | 40% | -60% |
| AI load time | 100% | 30% | -70% |

---

## 🚀 Execution Order

### Day 1 (6 hours):
1. ✅ Create AI_INDEX_DETAILS.md (full version)
2. ✅ Compress AI_INDEX.md (238 → 120 lines)
3. ✅ Optimize agent.md routes (404 → 350 lines)
4. ✅ Test: `make agent_lint`

### Day 2 (8 hours):
5. ✅ Create 4 AI doc versions (MOCK_RULES.md, security.md, quality.md, etc.)
6. ✅ Update agent.md routes to new docs
7. ✅ Add audience headers to 20 critical docs
8. ✅ Test: Run AI with new structure

### Day 3 (6 hours):
9. ✅ Translate 3 critical docs to English (goals, safety, DOC_ROLES)
10. ✅ Update agent.md routes to English versions
11. ✅ Add new rules to agent.md § 1.2
12. ✅ Full validation: `make dev_check`

**Total**: 20 hours

---

## ✅ Validation Checklist

After completion:

- [ ] AI_INDEX.md ≤ 120 lines
- [ ] agent.md ≤ 350 lines
- [ ] All critical AI docs in English
- [ ] All route docs have audience headers
- [ ] agent.md has clear skip rules
- [ ] make agent_lint passes
- [ ] make dev_check passes
- [ ] AI can load context <5 seconds
- [ ] Test AI understanding (spot check)

---

## 🎯 Success Criteria

**P0 Complete When**:
1. ✅ Token cost reduced by 50%+
2. ✅ AI load time reduced by 60%+
3. ✅ All critical docs in English
4. ✅ Clear audience separation
5. ✅ agent.md routes optimized

---

**Plan Created**: 2025-11-09  
**Ready for Execution**: ✅ YES


