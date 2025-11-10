---
audience: ai
language: en
version: summary
purpose: Documentation for AI_GUIDE
---
# Config Management - AI Quick Guide

> **For AI Agents** - Quick reference (~80 lines)  
> **Full Guide**: doc/process/CONFIG_GUIDE.md  
> **Language**: English (AI-optimized)

---

## Purpose

Centralized configuration with environment-specific overrides. Schema-validated, version-controlled.

---

## File Structure

```
config/
├── schema.yaml         # Configuration schema (validation rules)
├── defaults.yaml       # Default values (all environments)
├── dev.yaml           # Development overrides
├── staging.yaml       # Staging overrides (⚠️ needs approval)
├── prod.yaml          # Production overrides (🔴 blocked by guardrail)
└── loader/
    ├── python_loader.py   # Python config loader
    ├── ts_loader.ts       # TypeScript config loader
    └── go_loader.go       # Go config loader
```

---

## Loading Configuration

### Python
```python
from config.loader.python_loader import load_config

# Load for current environment (from ENV var or default to 'dev')
config = load_config()

# Load specific environment
config_prod = load_config(env='prod')

# Access values
db_host = config['database']['host']
api_key = config['services']['payment']['api_key']
```

### TypeScript
```typescript
import { loadConfig } from './config/loader/ts_loader';

// Load configuration
const config = loadConfig('dev');

// Access values
const dbHost = config.database.host;
const apiKey = config.services.payment.api_key;
```

### Go
```go
import "your-project/config/loader"

// Load configuration
config, err := loader.LoadConfig("dev")
if err != nil {
    log.Fatal(err)
}

// Access values
dbHost := config.Database.Host
apiKey := config.Services.Payment.ApiKey
```

---

## Configuration Priority

```
prod.yaml > staging.yaml > dev.yaml > defaults.yaml
  (highest)                            (lowest)
```

**Example**:
```yaml
# defaults.yaml
database:
  host: localhost
  port: 5432

# prod.yaml (overrides only host)
database:
  host: prod-db.example.com
  # port: 5432 (inherited from defaults)
```

---

## Schema Validation

`schema.yaml` defines required fields, types, and constraints:

```yaml
database:
  type: object
  required: [host, port, name]
  properties:
    host:
      type: string
      pattern: "^[a-zA-Z0-9.-]+$"
    port:
      type: integer
      minimum: 1
      maximum: 65535
    name:
      type: string
```

Validation runs automatically:
```bash
make runtime_config_check
# Validates all config files against schema.yaml
```

---

## Common Operations

### Add New Configuration
```bash
# 1. Update schema.yaml (define structure)
vim config/schema.yaml

# 2. Add default value
vim config/defaults.yaml

# 3. (Optional) Override for prod
vim config/prod.yaml  # ⚠️ Requires guardrail approval

# 4. Validate
make runtime_config_check
```

### Change Existing Configuration
```bash
# Dev/Staging: Direct edit
vim config/dev.yaml
make runtime_config_check

# Production: ⛔ Guardrail blocks direct edit
# Required: Change request + approval + rollback plan
```

### Environment-Specific Secrets
```yaml
# ❌ Don't store secrets directly:
# config/prod.yaml
database:
  password: "my-secret-password"  # WRONG!

# ✅ Use environment variables:
# config/prod.yaml
database:
  password: "${DB_PASSWORD}"  # Load from env var

# Set in deployment:
export DB_PASSWORD="actual-secret-value"
```

---

## Best Practices

1. **Minimal Overrides**: Only override what's different from defaults
2. **No Secrets**: Use env vars for sensitive data (passwords, API keys)
3. **Schema First**: Define schema before adding config
4. **Validate Always**: Run `make runtime_config_check` after changes
5. **Document Changes**: Update CHANGELOG.md for config changes

---

## Guardrail Protection

- `config/dev.yaml`: ✅ Free to edit
- `config/staging.yaml`: 🟠 Warns, requires confirmation
- `config/prod.yaml`: 🔴 Blocks, requires approval + change request

See: doc/process/guardrail-quickstart.md

---

## Telemetry Switches

- `telemetry.route_usage_logging` (bool, default `false`): toggles whether orchestrators should emit `python scripts/context_usage_tracker.py maybe-log --topic <topic> --path <path>` after loading docs. Keep it `false` for silent operation; set to `true` when you want automatic route usage logging.

---

## Commands

```bash
# Validate all configs
make runtime_config_check

# Load and print config (Python)
python -c "from config.loader.python_loader import load_config; print(load_config('dev'))"

# Check what would be loaded for prod
python -c "from config.loader.python_loader import load_config; print(load_config('prod'))"
```

---

## See Also

- **Full Guide**: doc/process/CONFIG_GUIDE.md (detailed examples, migration, troubleshooting)
- **Schema**: config/schema.yaml (validation rules)
- **Example Configs**: config/*.yaml (defaults, dev, staging, prod)
- **Loaders**: config/loader/*.{py,ts,go} (language-specific loaders)

