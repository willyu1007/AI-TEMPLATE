---
spec_version: "1.0"
agent_id: "config"
role: "Runtime configuration and environment management"

policies:
  goals_ref: /doc_agent/policies/goals.md
  safety_ref: /doc_agent/policies/safety.md

parent_agent: /AGENTS.md
merge_strategy: "child_overrides_parent"

context_routes:
  always_read:
    - /config/README.md
  on_demand:
    - topic: "Configuration Management"
      priority: high
      paths:
        - /config/AI_GUIDE.md
        - /doc_human/guides/CONFIG_GUIDE.md
    - topic: "Language Configuration"
      priority: high
      paths:
        - /config/language.yaml
---
# Config Agent Guide

> Deterministic runtime configs live under `config/`. This page keeps AI context short while pointing to deeper docs.

## Scope
- Layer defaults plus environment overrides plus runtime secrets.
- Publish schema-backed documentation so loaders stay in sync.
- Enforce language rules through `config/language.yaml`.

## Context Shortcuts
| Need | Load | Purpose |
| --- | --- | --- |
| Quick orientation | `/config/README.md` | Directory map and conventions |
| AI focused guide | `/config/AI_GUIDE.md` | When agents need detailed instructions |
| Human deep dive | `/doc_human/guides/CONFIG_GUIDE.md` | Long form explanations |
| Language policy | `/config/language.yaml` | Enforced language and locale |

## Workflow
1. Edit `defaults.yaml` for cross-environment values, then override per env file.
2. Update `schema.yaml` when adding new keys and describe types.
3. Run `make runtime_config_check` and `make config_lint`.
4. Touch loaders (`config/loader/*`) only after schema changes are merged.

## Commands
```bash
make runtime_config_check      # Schema validation
make config_lint               # YAML style checks
python config/loader/python_loader.py --env dev --validate
```

## Principles
- No secrets in git; rely on environment variables or ignored `.secrets.yaml`.
- Keep key names descriptive (snake_case, include units).
- Document breaking changes inside README plus workdoc summary.

## References
- `/config/README.md`
- `/config/AI_GUIDE.md`
- `/doc_human/guides/CONFIG_GUIDE.md`
- `/config/language.yaml`

Version metadata is implied by git history; this agent stays versionless.

