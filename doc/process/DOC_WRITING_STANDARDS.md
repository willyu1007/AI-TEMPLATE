# Documentation Writing Standards

> **Purpose**: Define documentation writing rules and standards  
> **Version**: 1.0  
> **Created**: 2025-11-09 (Phase 14.0)  
> **Language**: English

---

## Language Rules

### Language Consistency
**Principle**: Single language per document (Simplified Chinese OR English, no mixing)

**Examples**:
- Good: Entire doc in English OR entire doc in Chinese
- Bad: English sections mixed with Chinese sections in same doc

### AI Documents
- **Language**: English ONLY (better AI parsing, international compatibility)
- **Files**: agent.md (body), *-quickstart.md, AI_*.md, *.yaml (configs)
- **Key Fields**: role, action, tool, trigger, priority, severity must be English

### Human Documents
- **Language**: Chinese or English (team preference)
- **Files**: README.md, *_GUIDE.md (complete versions), tutorials
- **Flexibility**: Can include both languages in different sections if needed for clarity

### Mixed Content
- **Keywords for Triggers**: Chinese + English (both for matching)
- **Code Comments**: English preferred
- **YAML Comments**: Chinese allowed for clarity

---

## Document Structure

### Structured Output
Use these elements for organization:
- Headings (H1, H2, H3)
- Lists (ordered and unordered)
- Tables (for comparisons and data)
- Code blocks (with language tags)

### Emoji Policy
**Status Markers Only**: Check mark (pass), X mark (fail), Warning (caution), Clock (pending)

**Prohibited**: Decorative emojis, faces, icons (except in code examples)

**Reason**: Cleaner docs, better parsing, professional appearance

---

## AI Document Writing Standards

### When Creating AI-Facing Documents

**Required Elements**:
1. **Language**: English ONLY
2. **Header**: Must include `> **For AI Agents** - Purpose and scope`
3. **Length**: Maximum 150 lines (keep focused and fast to load)
4. **Format**: Commands first, concepts second (action-oriented)
5. **Examples**: Runnable code snippets with expected output
6. **File Naming**: *-quickstart.md, AI_*.md, or README.md in ai/ subdirs
7. **Cross-Reference**: Always link to human doc for full details

**Example AI Document Header**:
```markdown
# Guardrail - AI Quick Start

> **For AI Agents** - Quick reference (120 lines)  
> **Full Guide**: GUARDRAIL_GUIDE.md (782 lines)  
> **Language**: English (AI-optimized)
```

**Content Structure**:
1. Purpose (1-2 lines)
2. Quick Commands (code blocks)
3. Key Concepts (tables or lists)
4. Common Scenarios (3-5 examples)
5. See Also (link to human doc)

---

## Human Document Writing Standards

### When Creating Human-Facing Documents

**Required Elements**:
1. **Language**: Chinese or English (team choice, can be mixed)
2. **Length**: No limit (be comprehensive, include all details)
3. **Format**: Concepts first, examples second (understanding-oriented)
4. **Content**: Full explanations, edge cases, troubleshooting, best practices
5. **File Naming**: *_GUIDE.md, CONVENTIONS.md, or descriptive docs

**Example Human Document Header**:
```markdown
# Guardrail防护指南

> **用途**: Guardrail机制完整说明（人类参考）  
> **AI快速参考**: guardrail-quickstart.md (120行)  
> **版本**: 1.0
```

**Content Structure**:
1. Overview and Purpose
2. Core Concepts (detailed)
3. Architecture/Design
4. Usage Guide (step-by-step)
5. Examples (comprehensive)
6. Troubleshooting
7. Best Practices
8. FAQ

---

## Version Tracking

### Document Headers
All documents should include:
```markdown
> **Version**: 1.0  
> **Created**: 2025-11-09  
> **Last Updated**: 2025-11-09
```

### Change Tracking
- All changes recorded in CHANGELOG.md (if applicable)
- Breaking changes clearly marked
- Migration guides provided for major changes

---

## Code Comments

### Language Standards

**Python/Go**:
- English comments preferred (international teams)
- Class/function docstrings: English
- Inline comments: English for technical, Chinese for business logic

**Business Logic**:
- Chinese comments OK for domain-specific terms
- Business rule explanations: Chinese acceptable

**API Documentation**:
- English only (for auto-generated docs and international users)

---

## Code Blocks

### Language Tags Required
Always specify language for code blocks:

```python
# Good: Language specified
def example():
    pass
```

```
# Bad: No language specified
def example():
    pass
```

### Supported Languages
- python, javascript, typescript, go, sql, yaml, json, bash, sh

---

## Markdown Best Practices

### Links
- Use relative paths for internal docs
- Use absolute URLs for external resources
- Verify all links work (run doc_route_check)

### Tables
- Use for comparisons and structured data
- Keep columns reasonable (<6 columns)
- Align properly with pipes

### Lists
- Use ordered lists for sequential steps
- Use unordered lists for items without order
- Keep nesting to maximum 3 levels

---

## Verification

### Before Committing

Run these checks:
```bash
make doc_style_check     # Format and style
make doc_route_check     # Links and routes
make consistency_check   # Cross-document consistency
```

### Common Issues
1. Mixed languages in single doc
2. Broken internal links
3. Missing code block language tags
4. Decorative emojis
5. Inconsistent heading levels

---

## See Also

- **AI Coding Guide**: doc/process/AI_CODING_GUIDE.md (AI quick reference)
- **Full Conventions**: doc/process/CONVENTIONS.md (Human complete guide)
- **Document Roles**: doc/policies/DOC_ROLES.md (AI vs Human classification)

---

**Version**: 1.0  
**Last Updated**: 2025-11-09  
**Maintained by**: Project Team

