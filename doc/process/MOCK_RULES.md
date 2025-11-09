---
audience: ai
language: en
version: summary
purpose: Quick reference for mock data generation rules
full_version: /doc/process/MOCK_RULES_GUIDE.md
---

# Mock Rules - Quick Reference

> **For AI Agents** - Essential mock rules (~180 lines)  
> **Full Guide**: [MOCK_RULES_GUIDE.md](MOCK_RULES_GUIDE.md) (836 lines, for humans)  
> **Tool**: `scripts/mock_generator.py`

---

## Core Concept

Mock rules are YAML configurations in `TEST_DATA.md` that drive `mock_generator.py` to auto-generate test data.

**When to Use**:
- Large datasets (100+ records)
- Performance/stress testing
- Randomized testing

**When NOT to Use**:
- Unit tests (use fixtures instead)
- Precise test cases (use hand-crafted data)

---

## Basic Syntax

```yaml
mock_rules:
  <table_name>:
    count: 100                    # Number of records
    seed: 12345                   # Random seed (optional)
    lifecycle: ephemeral          # Data lifecycle
    fields:
      <field_name>:
        type: <generator_type>
        # generator-specific params
```

---

## Lifecycle Types

| Type | Duration | Use Case | Example |
|------|----------|----------|---------|
| `ephemeral` | Test duration only | Unit tests | Auto-deleted after test |
| `temporary` | <24 hours | Integration tests | Auto-cleanup daily |
| `persistent` | Manual delete | Demo environment | Kept until manually removed |
| `fixture` | Long-term | Shared fixtures | Kept across test runs |

**Recommendation**: Use `ephemeral` for most tests.

---

## Field Generator Types

### Common Generators

#### 1. UUID
```yaml
id:
  type: uuid
  version: 4  # Default: 4
```

#### 2. Integer
```yaml
age:
  type: int
  min: 18
  max: 65
```

#### 3. String
```yaml
name:
  type: string
  pattern: "[A-Z][a-z]{5,10}"  # Regex pattern
```

#### 4. Email
```yaml
email:
  type: email
  domain: example.com  # Optional
```

#### 5. Datetime
```yaml
created_at:
  type: datetime
  start: "2025-01-01"
  end: "2025-12-31"
```

#### 6. Choice (Enum)
```yaml
status:
  type: choice
  choices: ["pending", "active", "completed"]
  weights: [0.2, 0.6, 0.2]  # Optional probabilities
```

#### 7. Foreign Key
```yaml
user_id:
  type: foreign_key
  table: users
  field: id
  nullable: true  # Optional
```

---

## Quick Examples

### Example 1: Simple User Table
```yaml
mock_rules:
  users:
    count: 100
    lifecycle: ephemeral
    fields:
      id:
        type: uuid
      name:
        type: string
        pattern: "[A-Z][a-z]{4,10} [A-Z][a-z]{4,10}"
      email:
        type: email
      age:
        type: int
        min: 18
        max: 80
      status:
        type: choice
        choices: ["active", "inactive", "suspended"]
```

### Example 2: Orders with Foreign Keys
```yaml
mock_rules:
  orders:
    count: 500
    lifecycle: temporary
    fields:
      id:
        type: uuid
      user_id:
        type: foreign_key
        table: users
        field: id
      total:
        type: decimal
        min: 10.00
        max: 1000.00
        precision: 2
      status:
        type: choice
        choices: ["pending", "paid", "shipped", "completed"]
      created_at:
        type: datetime
        start: "2025-01-01"
        end: "2025-12-31"
```

---

## Commands

### Generate Mock Data
```bash
python scripts/mock_generator.py \
  --module <module> \
  --scenario <scenario> \
  --count <number>
```

### With Makefile
```bash
# Generate from TEST_DATA.md
make load_fixture MODULE=example FIXTURE=performance

# Cleanup
make cleanup_fixture MODULE=example
```

---

## Best Practices

### DO ✅
1. Use `ephemeral` lifecycle for tests
2. Set `seed` for reproducible tests
3. Use `foreign_key` for relationships
4. Keep `count` reasonable (<10000)
5. Define realistic constraints (min/max/pattern)

### DON'T ❌
1. Don't use for unit tests (use fixtures)
2. Don't generate millions of records (performance)
3. Don't mix mock and fixture data
4. Don't forget to cleanup (especially `persistent`)
5. Don't use in production (test only)

---

## Validation

### Check Mock Rules
```bash
make test_status_check  # Validates TEST_DATA.md format
```

### Test Generation
```bash
# Dry-run (no DB insert)
python scripts/mock_generator.py --dry-run \
  --module example --scenario default

# Actually generate
python scripts/mock_generator.py \
  --module example --scenario default --count 100
```

---

## Common Patterns

### Pattern 1: User-Content Relationship
```yaml
users:
  count: 100
  fields:
    id: { type: uuid }
    name: { type: string }
    
posts:
  count: 500  # 5 posts per user on average
  fields:
    id: { type: uuid }
    user_id: { type: foreign_key, table: users, field: id }
    title: { type: string, pattern: ".{10,100}" }
    created_at: { type: datetime }
```

### Pattern 2: Status Workflow
```yaml
orders:
  fields:
    status:
      type: choice
      choices: ["pending", "processing", "shipped", "delivered"]
      weights: [0.1, 0.2, 0.3, 0.4]  # More at later stages
```

### Pattern 3: Nullable Fields
```yaml
users:
  fields:
    phone:
      type: string
      pattern: "\\d{11}"
      nullable: true
      null_rate: 0.2  # 20% will be null
```

---

## Related Docs

- **Full Guide**: [MOCK_RULES_GUIDE.md](MOCK_RULES_GUIDE.md) (836 lines, all generator types)
- **Test Strategy**: [TEST_DATA_STRATEGY.md](TEST_DATA_STRATEGY.md) (677 lines)
- **Example**: [doc/modules/example/doc/TEST_DATA.md](../modules/example/doc/TEST_DATA.md)
- **Tool**: `scripts/mock_generator.py`

---

**Version**: 1.0  
**Last Updated**: 2025-11-09 (Phase 14.3 optimization)  
**Lines**: ~180

