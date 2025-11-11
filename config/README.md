# Configuration Directory

## Purpose
Keep runtime configuration deterministic across environments and easy for agents to load.

## Layering Order (lowest to highest)
1. `defaults.yaml` - shared defaults.
2. `<env>.yaml` - env-specific overrides (`dev`, `staging`, `prod`).
3. Environment variables - injected at runtime.
4. Secrets - stored outside git (see `.secrets.yaml` sample, never commit real secrets).

## Files
| File | Purpose | Committed |
|------|---------|-----------|
| `schema.yaml` | Strongly typed schema definition | ? |
| `defaults.yaml` | Baseline values | ? |
| `<env>.yaml` | Environment overrides | ? |
| `language.yaml` | Repository language + localization hints | ? |
| `.secrets.yaml` | Local secrets | ? |

## Language Configuration
`language.yaml` defines the canonical language for documentation, comments, and generated reports. Update it during project initialization and remind contributors to follow the setting. Automation scripts can read this file to enforce consistency.

## Loaders
See `loader/` for examples in Python (`python_loader.py`), Go (`go_loader.go`), and TypeScript (`ts_loader.ts`). Each loader validates against `schema.yaml` and falls back to `defaults.yaml` when a key is missing.

## Related Docs
- `doc_human/guides/CONFIG_GUIDE.md` - deep dive.
- `AGENTS.md` ¡ì4 - configuration guardrails.

