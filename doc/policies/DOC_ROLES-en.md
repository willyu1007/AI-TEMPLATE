---
audience: ai
language: en
version: summary
purpose: Define document roles and responsibilities (AI-facing vs Human-facing)
chinese_version: /doc/policies/DOC_ROLES.md
---

# Document Roles - AI vs Human Documentation

> **Purpose**: Define document roles and responsibilities  
> **Version**: 1.0  
> **Created**: 2025-11-09 (Phase 14.0)  
> **Language**: English

---

## Document Classification

### AI Documents (Quick Reference)

**Purpose**: Fast loading, action-oriented, command-focused

**Characteristics**:
- **Language**: English ONLY
- **Length**: ≤150 lines (typically 80-120 lines)
- **Header**: Must include `> **For AI Agents** - Purpose`
- **Format**: Commands first, concepts second
- **Examples**: Runnable code snippets
- **File Naming**: *-quickstart.md, AI_*.md, README.md in ai/

**When AI Should Load**:
- For quick operations and task execution
- When speed is important
- When command reference is needed

### Human Documents (Complete Reference)

**Purpose**: Deep understanding, comprehensive guidance, troubleshooting

**Characteristics**:
- **Language**: Chinese or English (team preference)
- **Length**: No limit (300-1000+ lines typical)
- **Format**: Concepts first, examples second
- **Content**: Full explanations, edge cases, best practices, troubleshooting
- **File Naming**: *_GUIDE.md, CONVENTIONS.md, detailed docs

**When AI Should Load**:
- For deep understanding of complex topics
- When troubleshooting edge cases
- When learning new concepts
- When human explicitly requests detailed explanation

---

## Document Inventory

### Core AI Documents (11)

| Document | Lines | Purpose | Load When |
|----------|-------|---------|-----------|
| AI_INDEX.md | 164 | Super-lightweight index | Always (startup) |
| dataflow-quickstart.md | 100 | Dataflow commands | Dataflow analysis task |
| guardrail-quickstart.md | 120 | Guardrail rules | Before risky operations |
| workdocs-quickstart.md | 100 | Task management | Creating workdocs |
| AI_GUIDE.md | 80 | Config commands | Config operations |
| AI_CODING_GUIDE.md | 371 | Coding standards | Writing code |
| MOCK_RULES.md | 288 | Mock data generation | Creating test data |
| security.md | 203 | Security guidelines | Security concerns |
| quality.md | 235 | Quality standards | Quality checks |
| workflow-patterns/README.md | 150 | Workflow catalog | Starting tasks |
| workflow-patterns/catalog.yaml | 80 | Pattern index | Workflow recommendation |
| modules/common/USAGE.md | 269 | Common module API | Using common |

**Total**: 12 docs, ~2,160 lines (avg 180 lines/doc)

### Core Human Documents (10+)

| Document | Lines | Purpose |
|----------|-------|---------|
| goals.md | 176 | Full goals and principles (Chinese) |
| safety.md | 244 | Full safety rules (Chinese/English mixed) |
| security_details.md | 537 | Security implementation details |
| quality_standards.md | 402 | Quality requirements details |
| DATAFLOW_ANALYSIS_GUIDE.md | 623 | Dataflow complete guide |
| GUARDRAIL_GUIDE.md | 782 | Guardrail complete guide |
| WORKDOCS_GUIDE.md | 653 | Workdocs complete guide |
| CONFIG_GUIDE.md | - | Config complete guide |
| CONVENTIONS.md | 611 | Full coding conventions |
| PATTERNS_GUIDE.md | 400 | Workflow patterns guide |
| HEALTH_MONITORING_GUIDE.md | 565 | Health monitoring guide |

**Total**: 11+ docs, ~5,000+ lines (avg 450 lines/doc)

---

## Loading Strategy

### Always Read (Startup)
```yaml
always_read:
  - /doc/policies/AI_INDEX.md  # 164 lines, self-contained
```

**Token Cost**: ~235 tokens  
**Depth**: 0 (DO NOT follow references in AI_INDEX.md)

### On-Demand Loading (Priority-based)

**High Priority** (Load AI version first):
- Database operations → DB_SPEC.yaml, DB_CHANGE_GUIDE.md
- Module development → MODULE_TYPES.md, MODULE_INIT_GUIDE.md
- Guardrails → guardrail-quickstart.md
- Workflow patterns → workflow-patterns/README.md, catalog.yaml

**Medium Priority** (Load AI version only):
- Mock data → MOCK_RULES.md
- Security → security.md
- Testing → testing.md (consider creating testing-quickstart.md)
- Triggers → agent-triggers.yaml

**Low Priority** (Human docs, load only if explicitly needed):
- CONVENTIONS.md
- *_GUIDE.md docs
- Detailed troubleshooting docs

---

## Document Pairing

### Recommended Pairs (AI + Human)

| AI Version | Human Version | Split? |
|------------|---------------|--------|
| dataflow-quickstart.md (100) | DATAFLOW_ANALYSIS_GUIDE.md (623) | ✅ Good |
| guardrail-quickstart.md (120) | GUARDRAIL_GUIDE.md (782) | ✅ Good |
| workdocs-quickstart.md (100) | WORKDOCS_GUIDE.md (653) | ✅ Good |
| MOCK_RULES.md (288) | MOCK_RULES_GUIDE.md (836) | ✅ Good |
| security.md (203) | security_details.md (537) | ✅ Good |
| quality.md (235) | quality_standards.md (402) | ✅ Good |
| AI_CODING_GUIDE.md (371) | CONVENTIONS.md (611) | ✅ Good |
| AI_INDEX.md (164) | AI_INDEX_DETAILS.md (630) | ✅ Good |
| health-summary.md (103) | HEALTH_MONITORING_GUIDE.md (565) | ✅ Good |

**Coverage**: 9/9 major topics split ✅

---

## Document Creation Checklist

### Creating AI Document

- [ ] Filename: *-quickstart.md or AI_*.md
- [ ] Language: English only
- [ ] Header: Include `> **For AI Agents** - Purpose`
- [ ] Front matter: `audience: ai, language: en, version: summary`
- [ ] Length: ≤150 lines (target), ≤200 lines (max)
- [ ] Format: Commands → Quick guide → See also
- [ ] Examples: Runnable code snippets
- [ ] Cross-reference: Link to human doc for full details
- [ ] Add to context_routes if applicable

### Creating Human Document

- [ ] Filename: *_GUIDE.md or descriptive name
- [ ] Language: Chinese or English (team choice)
- [ ] Header: Include purpose, version, date
- [ ] Front matter: `audience: human, language: zh/en, version: complete`
- [ ] Length: No limit (be comprehensive)
- [ ] Format: Overview → Concepts → Examples → Troubleshooting
- [ ] Content: All details, edge cases, best practices
- [ ] Cross-reference: Link to AI doc for quick reference
- [ ] Add to context_routes if applicable

### Updating Existing Document

- [ ] Check document role (AI or human?)
- [ ] Follow corresponding standards (§ 3 in agent.md)
- [ ] Keep language consistent (no mixing)
- [ ] Update CHANGELOG.md
- [ ] Verify with `make doc_style_check`

---

## Verification

### Check Document Classification

```bash
# Check documents with audience headers
grep -r "^audience:" doc/ ai/ config/ modules/ | wc -l

# Check AI documents are English
grep -l "audience: ai" -r doc/ ai/ config/ modules/ | \
  while read f; do
    lang=$(grep "^language:" "$f" | awk '{print $2}')
    echo "$f: $lang"
  done

# Check document lengths
find doc/ ai/ -name "*-quickstart.md" -o -name "AI_*.md" | \
  while read f; do
    lines=$(wc -l < "$f")
    status="✅"
    [ $lines -gt 150 ] && status="⚠️"
    [ $lines -gt 200 ] && status="🔴"
    echo "$status $f: $lines lines"
  done
```

### Verify agent.md Routes

```bash
# Check if routes point to correct doc types
make doc_route_check

# Verify priority fields exist
grep "priority:" agent.md | wc -l
```

---

## Common Mistakes

### ❌ Mistake 1: Mixing Languages
```markdown
# Bad: AI doc with Chinese
> **For AI Agents** - 快速参考

# Good: AI doc fully English
> **For AI Agents** - Quick reference
```

### ❌ Mistake 2: AI Doc Too Long
```markdown
# Bad: AI doc 500 lines
guardrail-quickstart.md (500 lines)

# Good: Split into AI + human
guardrail-quickstart.md (120 lines) - AI
GUARDRAIL_GUIDE.md (782 lines) - Human
```

### ❌ Mistake 3: No Role Identifier
```markdown
# Bad: Can't tell if AI or human doc
some-guide.md (no header)

# Good: Clear identifier
> **For AI Agents** - Quick reference
# or
> **用途**: 完整指南（人类参考）
```

### ❌ Mistake 4: Routing to Wrong Doc
```yaml
# Bad: Route AI to heavy human doc
- topic: "Guardrail Protection"
  paths:
    - /doc/process/GUARDRAIL_GUIDE.md  # 782 lines!

# Good: Route AI to quickstart
- topic: "Guardrail Protection"
  paths:
    - /doc/process/guardrail-quickstart.md  # 120 lines ✅
```

---

## Document Statistics

### Current Status (After Phase 14.3)

| Category | Count | Avg Lines | Total Lines |
|----------|-------|-----------|-------------|
| AI Docs | 12 | 180 | ~2,160 |
| Human Docs | 11 | 545 | ~6,000 |
| Both | 1 (README.md) | 287 | 287 |

### Coverage

| Metric | Value | Status |
|--------|-------|--------|
| Docs with audience headers | 31/42 | 74% ✅ |
| AI docs in English | 12/12 | 100% ✅ |
| AI docs ≤200 lines | 12/12 | 100% ✅ |
| Major topics split (AI/Human) | 9/9 | 100% ✅ |

---

## Related Docs

- **Goals**: goals-en.md (core objectives)
- **Safety**: safety-en.md (safety constraints)
- **AI Index**: AI_INDEX.md (super-lightweight index)
- **Routing**: doc/orchestration/routing.md

---

**Version**: 1.0  
**Last Updated**: 2025-11-09 (Phase 14.3 optimization)  
**Lines**: ~306 (same as Chinese version)

