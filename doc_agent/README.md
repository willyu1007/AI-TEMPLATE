---
audience: ai
language: en
---
# doc_agent/ - AI Agent Documentation

> **Purpose**: Lightweight, English documentation optimized for AI agents
> **Principle**: Token-efficient, routable, structured

---

## Directory Structure

```
doc_agent/
├── policies/         # Core execution policies
├── specs/            # Technical specifications
├── orchestration/    # Module orchestration configs
├── flows/            # Lifecycle + DAG definitions
├── init/             # Initialization playbooks
├── quickstart/       # Quick reference guides
├── coding/           # Coding standards
└── index/            # AI context indexes
```

## Usage Guidelines

### For AI Agents

1. **Always start with index/**
   - AI_INDEX.md provides overview
   - context-rules.md explains routing

2. **Load via context_routes**
   - Use agent.md routing configuration
   - Load only what's needed for the task

3. **Reference specs/ for contracts**
   - MODULE_TYPES.md for module types
   - DB_SPEC.yaml for database schema
   - HEALTH_CHECK_MODEL.yaml for metrics

4. **Use flows/ + init/ + quickstart/**
   - flows/repo-lifecycle.md for end-to-end orchestration view
   - flows/maintenance-loop.md for recurring health checks
   - init/project-init.md for repo initialization protocol
   - init/module-init.md for module initialization protocol
   - quickstart/module-init.md for command cheatsheet
   - quickstart/workdocs-quickstart.md for task management
   - quickstart/guardrail-quickstart.md for guardrail validation

## Key Documents

| Document | Purpose | When to Load |
|----------|---------|--------------|
| index/AI_INDEX.md | Repository overview | Always |
| specs/MODULE_TYPES.md | Module classification | Module work |
| init/project-init.md | Repo initialization protocol | Before scaffolding |
| init/module-init.md | Module initialization protocol | Before scaffolding |
| flows/repo-lifecycle.md | Full orchestration lifecycle | Planning & handoff |
| flows/maintenance-loop.md | Health & maintenance loop | Post-release |
| quickstart/module-init.md | Module command checklist | After protocol |
| coding/AI_CODING_GUIDE.md | Coding standards | Implementation |
| orchestration/registry.yaml | Module registry | Dependencies |

## Document Standards

- **Language**: English only
- **Format**: Markdown with YAML front matter
- **Length**: <200 lines preferred
- **Structure**: Clear sections with headers

---

**Note**: For detailed human guides, see `/doc_human/`
