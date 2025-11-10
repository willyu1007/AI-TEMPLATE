# Routing Rules

> Defines how agents load and merge context from `agent.md` files.

## Principles
1. **Layered loading** - module `agent.md` ¡ú root `agent.md` ¡ú referenced policies.
2. **Merge strategy** - default is `child_overrides_parent` (set in root file). Children may override parent arrays/fields.
3. **On-demand context** - only load what `context_routes` specifies; never follow references recursively.

## `context_routes` Blocks
### `always_read`
Small documents loaded on every session start (e.g., `/doc_agent/index/AI_INDEX.md`). Keep under ~200 tokens.

### `on_demand`
Topic-based routes used when a task mentions a capability. Example:
```yaml
context_routes:
  on_demand:
    - topic: "Database Operations"
      priority: high
      paths:
        - /doc_agent/specs/DB_SPEC.yaml
        - /doc_human/guides/DB_CHANGE_GUIDE.md
```
Add `priority`, `audience`, and `language` metadata so orchestration can decide when to load.

### `by_scope`
Scope-specific documents, usually for modules:
```yaml
by_scope:
  - scope: "modules/user"
    read:
      - /modules/user/agent.md
      - /modules/user/doc/CONTRACT.md
      - /modules/user/doc/RUNBOOK.md
```

## Usage Scenarios
| Scenario | Must Load |
|----------|-----------|
| New module | `always_read` + `on_demand` topic ¡°Module Development¡± + `by_scope` for the module |
| Database change | `always_read` + ¡°Database Operations¡± topic + db scopes |
| Bug fix | `always_read` + module scope + relevant test scope |

## Validation
Run `make doc_route_check` to ensure every referenced path exists and has the correct headers.

## Guidelines
- Keep `always_read` tiny; move heavy docs to `on_demand` or `by_scope`.
- Use absolute POSIX-style paths.
- Respect `audience` and `skip_for_ai` flags in the target documents.

Update this file whenever you introduce new routing patterns or merge strategies.

