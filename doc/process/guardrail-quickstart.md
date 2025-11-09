# Guardrail - AI Quick Start

> **For AI Agents** - Quick reference (~120 lines)  
> **Full Guide**: GUARDRAIL_GUIDE.md (782 lines)  
> **Language**: English (AI-optimized)

---

## Purpose

Prevent destructive operations through automated pre-checks. Block/warn/suggest before executing risky actions.

---

## 3 Protection Levels

| Level | Action | Use Case | Can Override |
|-------|--------|----------|--------------|
| **Block** 🔴 | Stop execution | Critical operations (DB schema, contract breaking, prod config) | No (must fix) |
| **Warn** 🟠 | Show warning, require confirmation | Medium risk (test data, config change, dependency update) | Yes (explicit confirm) |
| **Suggest** 🟢 | Show recommendation | Best practices (workflow patterns, documentation, code style) | Yes (optional) |

---

## 15 Guardrail Rules

### Block Rules (4) - Must Fix

1. **database-schema-change** 🔴
   - Detects: CREATE TABLE, ALTER TABLE, DROP TABLE
   - Requires: Migration script (up/down), rollback plan, review
   - Files: `db/engines/*/migrations/*.sql`, `db/engines/*/schemas/*.yaml`

2. **contract-breaking-change** 🔴
   - Detects: Removed fields, changed types, deleted endpoints
   - Requires: Compatibility check, baseline update, migration guide
   - Files: `*/CONTRACT.md`, `tools/*/contract.json`

3. **production-config-change** 🔴
   - Detects: Changes to `config/prod.yaml`
   - Requires: Explicit approval, change request, rollback plan
   - Files: `config/prod.yaml`

4. **dependency-major-update** 🔴
   - Detects: Major version bumps in dependencies
   - Requires: Compatibility test, regression test, gradual rollout
   - Files: `requirements.txt`, `package.json`, `go.mod`

### Warn Rules (3) - Confirm Before Proceed

5. **test-data-modification** 🟠
   - Detects: Changes to test fixtures
   - Warns: May break existing tests
   - Files: `*/fixtures/*.sql`, `*/fixtures/*.json`

6. **staging-config-change** 🟠
   - Detects: Changes to `config/staging.yaml`
   - Warns: Verify with staging environment
   - Files: `config/staging.yaml`

7. **agent-routing-change** 🟠
   - Detects: Changes to agent.md routing
   - Warns: May affect AI context loading
   - Files: `agent.md`, `*/agent.md`

### Suggest Rules (6) - Best Practices

8. **workflow-pattern-suggestion** 🟢
   - Triggers: Keywords like "创建模块", "修复bug"
   - Suggests: Load relevant workflow pattern
   - Patterns: module-creation, bug-fix, database-migration, etc.

9. **dataflow-analysis** 🟢
   - Triggers: New module, major refactoring
   - Suggests: Run `make dataflow_analyze`

10. **documentation-update** 🟢
    - Triggers: Code changes without doc updates
    - Suggests: Update README.md, CONTRACT.md

11-15. **Other Suggestions** 🟢
    - Module initialization guide
    - DB change checklist
    - Test coverage reminder
    - Security review
    - Performance review

---

## How It Works

### 1. File Triggers
```yaml
# In agent-triggers.yaml
file_triggers:
  - rule_id: database-schema-change
    priority: critical
    execution_mode: block
    patterns:
      paths:
        - pattern: "db/engines/*/migrations/*.sql"
        - pattern: "db/engines/*/schemas/*.yaml"
```

### 2. Prompt Triggers
```yaml
# In agent-triggers.yaml
prompt_triggers:
  - rule_id: workflow-pattern-suggestion
    priority: medium
    execution_mode: suggest
    patterns:
      keywords: ["创建", "开发", "修复"]
      intents:
        - pattern: "^(我想|如何|怎么).*(创建|开发).*模块"
```

### 3. Auto-Check
```bash
# Runs automatically in:
make dev_check          # CI gate
make agent_trigger_test # Manual test

# Check specific file
make agent_trigger FILE=db/engines/postgres/migrations/001_create_users.sql
# Output: ⛔ BLOCK - database-schema-change triggered
```

---

## Bypass Mechanisms

### Skip Conditions (Exemptions)
```yaml
skip_conditions:
  - "migration paired"      # up/down migrations exist
  - "rollback tested"       # rollback script verified
  - "review approved"       # PR approved by 2+ reviewers
```

### Emergency Override
```bash
# In extreme emergency only (document reason in commit)
export GUARDRAIL_OVERRIDE=true
make deploy
```

---

## Common Scenarios

### Scenario 1: Add Database Table
```bash
# 1. Create migration files
touch db/engines/postgres/migrations/002_create_orders_up.sql
touch db/engines/postgres/migrations/002_create_orders_down.sql

# 2. Guardrail checks:
#    ⛔ BLOCK if only up.sql exists
#    ✅ PASS if both up+down exist

# 3. Add to checklist:
#    - [ ] Migration paired (up/down)
#    - [ ] Rollback tested locally
#    - [ ] Schema YAML updated
#    - [ ] Review approved
```

### Scenario 2: Modify API Contract
```bash
# 1. Update CONTRACT.md
vim modules/user/doc/CONTRACT.md

# 2. Guardrail checks:
#    ⛔ BLOCK if field removed/type changed
#    🟠 WARN if new required field added
#    ✅ PASS if optional field added

# 3. If blocked:
#    - Add to DEPRECATED section
#    - Keep old field for 1+ release
#    - Provide migration guide
```

### Scenario 3: Change Production Config
```bash
# 1. Attempt to edit config/prod.yaml
vim config/prod.yaml

# 2. Guardrail blocks:
#    ⛔ BLOCK - production-config-change triggered
#    Required: Approval + Change Request + Rollback Plan

# 3. Proper workflow:
#    - Create change request (JIRA/Ticket)
#    - Get approval from tech lead
#    - Prepare rollback plan
#    - Document in CHANGELOG.md
```

---

## Configuration

### Add Custom Rule

Edit `doc/orchestration/agent-triggers.yaml`:

```yaml
file_triggers:
  - rule_id: my-custom-rule
    description: "Prevent direct changes to sensitive files"
    priority: high
    execution_mode: block
    patterns:
      paths:
        - pattern: "config/secrets/*.yaml"
    actions:
      documents_to_load:
        - /doc/process/SECRET_MANAGEMENT.md
    skip_conditions:
      - "encrypted"
      - "review approved"
```

---

## Testing Guardrails

```bash
# Test all rules
make agent_trigger_test

# Test specific file
make agent_trigger FILE=config/prod.yaml
# Expected: ⛔ BLOCK - production-config-change

# Test specific prompt
make agent_trigger_prompt PROMPT="我想修改数据库表结构"
# Expected: ⛔ BLOCK - database-schema-change
#           🟢 SUGGEST - Load DB_CHANGE_GUIDE.md
```

---

## Integration

### In CI/CD
```yaml
# .github/workflows/guardrail-check.yml
- name: Guardrail Check
  run: |
    # Check all changed files
    git diff --name-only HEAD~1 | while read file; do
      make agent_trigger FILE="$file"
    done
```

### In Git Hooks
```bash
# .git/hooks/pre-commit
#!/bin/bash
git diff --cached --name-only | while read file; do
  result=$(make agent_trigger FILE="$file")
  if echo "$result" | grep -q "⛔ BLOCK"; then
    echo "Guardrail blocked: $file"
    exit 1
  fi
done
```

---

## See Also

- **Full Guide**: doc/process/GUARDRAIL_GUIDE.md (782 lines, detailed rules and examples)
- **Trigger Config**: doc/orchestration/agent-triggers.yaml (604 lines, 15 rules)
- **Trigger Script**: scripts/agent_trigger.py (536 lines, execution engine)
- **Trigger Guide**: doc/orchestration/triggers-guide.md (usage and customization)

