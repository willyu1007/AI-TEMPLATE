---
audience: ai
language: en
version: quickstart
---
# Module Initialization Quickstart

> **For**: AI Agents initializing new modules  
> **Time**: 5 minutes  
> **Prerequisites**: Module type decided

---

## Quick Command

```bash
make ai_begin MODULE=<module_name>
```

This command automatically:
- Creates directory structure
- Generates required documents
- Updates registry
- Creates agent.md

---

## Manual Steps (if needed)

### 1. Create Structure

```bash
modules/<entity>/
├── agent.md           # AI configuration
├── README.md          # Module overview
├── __init__.py        # Python package
├── core/             # Core logic
├── models/           # Data models
├── services/         # Business services
├── doc/              # Documentation
│   ├── CONTRACT.md   # IO contract
│   ├── CHANGELOG.md  # Change history
│   ├── RUNBOOK.md   # Operations guide
│   ├── TEST_PLAN.md  # Test strategy
│   └── BUGS.md      # Known issues
└── tests/            # Test files
```

### 2. Define Contract

In `doc/CONTRACT.md`:

```yaml
module:
  name: <module_name>
  type: 1_Assign|2_Select|3_SelectMethod|4_Aggregator
  version: 1.0.0

input:
  # Type-specific input schema

output:
  # Type-specific output schema

errors:
  # Error codes and messages
```

### 3. Configure Agent

In `agent.md`:

```yaml
---
spec_version: "1.0"
agent_id: "modules.<entity>.<instance>"
role: "<module purpose>"

upstream:
  - <dependent_modules>

downstream:
  - <consuming_modules>

context_routes:
  always_read:
    - /modules/<entity>/README.md
    - /modules/<entity>/doc/CONTRACT.md
---
```

### 4. Register Module

Update `/doc_agent/orchestration/registry.yaml`:

```yaml
modules:
  <type>:
    <instance>:
      path: /modules/<entity>
      status: active
      dependencies: []
```

---

## Validation Checklist

```bash
# Run validation
make module_health_check MODULE=<module_name>

# Checks:
✓ Directory structure complete
✓ Required documents exist
✓ agent.md valid
✓ CONTRACT.md matches type
✓ Registry entry present
```

---

## Next Steps

1. Implement core logic
2. Add tests (coverage ≥80%)
3. Update CHANGELOG.md
4. Run `make dev_check`

---

**See Also**: 
- `/doc_agent/specs/MODULE_TYPES.md` - Type definitions
- `/doc_agent/specs/MODULE_TYPE_CONTRACTS.yaml` - IO contracts
- `/doc_human/guides/MODULE_INIT_GUIDE.md` - Detailed guide
