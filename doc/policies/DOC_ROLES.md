# Document Roles - AI vs Human Documentation

> **Purpose**: Define document roles and responsibilities (AI-facing vs Human-facing)  
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

### Core AI Documents

| Document | Lines | Purpose | Load When |
|----------|-------|---------|-----------|
| doc/policies/AI_INDEX.md | 100 | Super-lightweight index | Always (startup) |
| doc/process/dataflow-quickstart.md | 100 | Dataflow commands | Dataflow analysis task |
| doc/process/guardrail-quickstart.md | 120 | Guardrail rules | Before risky operations |
| doc/process/workdocs-quickstart.md | 100 | Task management | Creating/managing workdocs |
| config/AI_GUIDE.md | 80 | Config commands | Config operations |
| doc/process/AI_CODING_GUIDE.md | 150 | Coding standards | Writing code |
| ai/workflow-patterns/README.md | 150 | Workflow catalog | Starting new task |
| ai/workflow-patterns/catalog.yaml | 80 | Pattern index | Workflow recommendation |
| doc/templates/dataflow-summary.md | 86 | Dataflow template | Generating dataflow doc |
| modules/common/agent.md | 154 | Common module guide | Using common utilities |
| modules/common/doc/CONTRACT.md | 490 | Common module API | Common API reference |

**Total AI Docs**: 11 docs, ~1,610 lines

### Core Human Documents

| Document | Lines | Purpose |
|----------|-------|---------|
| doc/policies/goals.md | 171 | Full goals and principles |
| doc/policies/safety.md | 233 | Full safety rules |
| doc/policies/security_details.md | 537 | Security implementation details |
| doc/policies/quality_standards.md | 402 | Quality requirements details |
| doc/process/DATAFLOW_ANALYSIS_GUIDE.md | 519 | Dataflow complete guide |
| doc/process/GUARDRAIL_GUIDE.md | 782 | Guardrail complete guide |
| doc/process/WORKDOCS_GUIDE.md | 653 | Workdocs complete guide |
| doc/process/CONFIG_GUIDE.md | - | Config complete guide |
| doc/process/CONVENTIONS.md | 611 | Full coding conventions |
| ai/workflow-patterns/PATTERNS_GUIDE.md | 400 | Workflow patterns human guide |

**Total Human Docs**: 10+ docs, ~4,300+ lines

---

## Loading Strategy

### Always Read (Startup)
```yaml
always_read:
  - /doc/policies/AI_INDEX.md  # 100 lines, self-contained
```

**Token Cost**: ~130 tokens  
**Depth**: 0 (DO NOT follow references in AI_INDEX.md)

### On-Demand Loading

**Priority Levels**:
- **High**: Load AI quickstart first, then human guide if needed
- **Medium**: Load AI quickstart only (sufficient for most tasks)
- **Low**: Load human guide directly (rare)

**Example Decision Tree**:
```
Task: Implement guardrail check
├─ Is it a quick operation? YES
│  └─ Load: guardrail-quickstart.md (120 lines) ✅
├─ Need deep understanding? NO
│  └─ Skip: GUARDRAIL_GUIDE.md (782 lines) ⏭️
└─ Proceed with task
```

```
Task: Design new guardrail rules
├─ Is it a quick operation? NO
│  └─ Skip quickstart
├─ Need deep understanding? YES
│  └─ Load: GUARDRAIL_GUIDE.md (782 lines) ✅
└─ Also load: agent-triggers.yaml, examples
```

### Module-Specific Loading

```yaml
# When working in modules/user/
by_scope:
  - scope: "模块开发"
    read:
      - modules/user/agent.md      # AI document (English)
      - modules/user/README.md     # Human document (CN/EN)
      - modules/user/doc/CONTRACT.md  # API reference
```

---

## Document Creation Checklist

### Creating AI Document

- [ ] File name: *-quickstart.md or AI_*.md
- [ ] Language: English only
- [ ] Header: Include `> **For AI Agents** - Purpose`
- [ ] Length: ≤150 lines
- [ ] Format: Commands → Quick guide → See also
- [ ] Examples: Runnable code snippets
- [ ] Cross-reference: Link to human doc for full details
- [ ] Add to context_routes if applicable

### Creating Human Document

- [ ] File name: *_GUIDE.md or descriptive name
- [ ] Language: Chinese or English (team choice)
- [ ] Header: Include purpose, version, date
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
# Find all AI documents
grep -r "For AI Agents" doc/ ai/ config/

# Check AI doc length (should be ≤150 lines)
find doc/ ai/ config/ -name "*-quickstart.md" -o -name "AI_*.md" | \
  while read f; do 
    lines=$(wc -l < "$f")
    echo "$f: $lines lines"
  done

# Check language consistency
# AI docs should be English, human docs can be CN/EN
```

### Verify agent.md References

```bash
# Check if agent.md routes to correct doc types
python scripts/doc_route_check.py

# Verify priority fields exist
grep "priority:" agent.md | wc -l  # Should be 19
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
# guardrail-quickstart.md (500 lines)

# Good: Split into AI + human
# guardrail-quickstart.md (120 lines) - AI
# GUARDRAIL_GUIDE.md (782 lines) - Human
```

### ❌ Mistake 3: No Role Identifier
```markdown
# Bad: Can't tell if AI or human doc
# some-guide.md (no header)

# Good: Clear identifier
> **For AI Agents** - Quick reference
# or
> **用途**: 完整指南（人类参考）
```

### ❌ Mistake 4: Routing to Wrong Doc
```yaml
# Bad: Route AI to heavy human doc
- topic: "Guardrail防护机制"
  paths:
    - /doc/process/GUARDRAIL_GUIDE.md  # 782 lines!

# Good: Route AI to quickstart first
- topic: "Guardrail防护机制"
  priority: high
  paths:
    - /doc/process/guardrail-quickstart.md  # 120 lines
    - /doc/process/GUARDRAIL_GUIDE.md       # Full details
```

---

## Maintenance

### Adding New AI Document

1. Create file: `doc/process/xxx-quickstart.md`
2. Add header: `> **For AI Agents** - Purpose`
3. Keep length: ≤150 lines
4. Use English only
5. Add to agent.md context_routes
6. Set priority: high/medium/low
7. Verify: `make doc_route_check`

### Adding New Human Document

1. Create file: `doc/process/XXX_GUIDE.md`
2. Add header with purpose and version
3. No length limit (be comprehensive)
4. Chinese or English (team choice)
5. Add to agent.md context_routes (after AI doc)
6. Set priority: typically low (deep dive)
7. Verify: `make doc_route_check`

### Splitting Existing Doc

If a document is too long (>500 lines):

1. Create AI quickstart (~100 lines):
   - Extract commands and quick references
   - English only
   - Add "For AI Agents" header

2. Keep human complete guide:
   - Retain all details and examples
   - Keep existing language
   - Add reference to quickstart

3. Update agent.md routes:
   - Add AI doc first
   - Add human doc second
   - Set appropriate priorities

---

## See Also

- **agent.md § 3**: Documentation Standards (writing rules)
- **AI_CODING_GUIDE.md**: AI-specific coding standards
- **CONVENTIONS.md**: Full coding conventions (human)

---

**Version**: 1.0  
**Last Updated**: 2025-11-09  
**Maintained by**: Project Team

