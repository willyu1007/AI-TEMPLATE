#!/usr/bin/env bash
set -euo pipefail

MOD=${1:-}

if [ -z "$MOD" ]; then
    echo ": bash scripts/ai_begin.sh <module>"
    echo ": bash scripts/ai_begin.sh user_auth"
    echo ""
    echo "💡  doc/modules/MODULE_INIT_GUIDE.md"
    echo "   AI"
    exit 1
fi

echo "🚀 : $MOD"
echo ""
echo "📚 doc/modules/example/ "
echo ""

# Phase 6
mkdir -p "modules/$MOD/core"
mkdir -p "modules/$MOD/doc"

# .context/Phase 8.5
mkdir -p "modules/$MOD/.context"

# Phase 6
echo "[1/5] ..."

# README.md
cat > "modules/$MOD/README.md" <<'EOF'
# <> 

## 


## 
### 
- /
- 

### 
- 
- 

### 
- /
- 

## 


## 
- 
- 
- 
EOF

# plan.mdPhase 6.5
cat > "modules/$MOD/plan.md" <<EOF
#  ($(date +%Y-%m-%d))

## 


## 
- 
- 

## /DB 
- /
- DAG 

---

## ⭐

### 
- [ ] 
  - 
    - [ ] 
    - [ ] 
    - [ ] 
    - [ ] 
    - [ ] 
    - [ ] 
  - <>
  - <>
  - doc/process/DB_CHANGE_GUIDE.md
  
- [ ] 

### ⭐
- [ ] Fixtures
  - 
    - [ ] minimal
    - [ ] standard
    - [ ] full
- [ ] Mock
  - <>
- [ ] 

---

## 
- [ ] 
- [ ] 
- [ ] 

## 
\`\`\`bash
make dev_check
make db_lint       # 
# 
\`\`\`

## 

- <down>
- <git commit hash>
- Feature Flag<>
EOF

# CONTRACT.mdPhase 6doc/
cat > "modules/$MOD/doc/CONTRACT.md" <<'EOF'
# CONTRACT - 

## 
```json
{
  "field1": "",
  "field2": ""
}
```

## 
```json
{
  "result": "",
  "status": "success|error"
}
```

## 
- `E001`: 
- `E002`: 

## 
- 
- semver

## 
### 
```json
{
  "field1": "example"
}
```

### 
```json
{
  "result": "example",
  "status": "success"
}
```
EOF

# TEST_PLAN.mdPhase 6doc/
cat > "modules/$MOD/doc/TEST_PLAN.md" <<'EOF'
# TEST_PLAN - 

## 
1. **1**
   - 
   - 
   - 

2. **2**
   - 
   - 
   - 

## 
- 
- 
- 

## 
- 
- 
- 

## 

EOF

# RUNBOOK.mdPhase 6doc/
cat > "modules/$MOD/doc/RUNBOOK.md" <<'EOF'
# RUNBOOK - 

## 
```bash
# 
```

## 
- 
- 
- 

## 
|  |  |  |
|---------|---------|---------|
| Alert1  |     |     |

## 
```bash
# 
```

## 
- 1
- 2
EOF

# PROGRESS.mdPhase 6doc/
cat > "modules/$MOD/doc/PROGRESS.md" <<EOF
# PROGRESS - 

## 
-  /  /  / 
- $(date +%Y-%m-%d)

## 
- [ ] M1:  ()
- [ ] M2:  ()
- [ ] M3:  ()

## 


## 
- $(date +%Y-%m-%d): 
EOF

# BUGS.mdPhase 6doc/
cat > "modules/$MOD/doc/BUGS.md" <<'EOF'
# BUGS - 

## 
- [ ] **BUG-001**: 
  - 
  - 
  - 

## 
- [x] **BUG-000**: 
  - YYYY-MM-DD
  - 

## 

EOF

# CHANGELOG.mdPhase 6doc/
cat > "modules/$MOD/doc/CHANGELOG.md" <<EOF
# CHANGELOG - 

## [Unreleased]

## [0.1.0] - $(date +%Y-%m-%d)
### Added
- 
- 

### Changed
-

### Fixed
-

### Removed
-
EOF

echo "  ✓ 6doc/"

# AGENTS.mdPhase 6Phase 14.0
echo "[2/5] AGENTS.md..."
cat > "modules/$MOD/AGENTS.md" <<EOF
---
spec_version: "1.0"
agent_id: "modules.$MOD.v1"
role: "Business logic agent for $MOD module"
level: 1
module_type: "1_$MOD"

ownership:
  code_paths:
    include:
      - modules/$MOD/
      - tests/$MOD/
    exclude:
      - modules/$MOD/doc/CHANGELOG.md

io:
  inputs:
    - name: "input_placeholder"
      type: "object"
      required: true
      description: "TODO: Define input parameters"
      schema_ref: "modules/$MOD/doc/CONTRACT.md#inputs"
  
  outputs:
    - name: "result"
      type: "object"
      required: true
      description: "TODO: Define output format"
      schema_ref: "modules/$MOD/doc/CONTRACT.md#outputs"

contracts:
  apis:
    - modules/$MOD/doc/CONTRACT.md

dependencies:
  upstream: []
  downstream: []

constraints:
  - "Maintain test coverage ≥80%"
  - "Backward compatibility required"
  - "Response time <500ms (P95)"

tools_allowed:
  calls:
    - http
    - fs.read

quality_gates:
  required_tests:
    - unit
    - integration
  coverage_min: 0.80

context_routes:
  always_read:
    - modules/$MOD/README.md
    - modules/$MOD/doc/CONTRACT.md
  on_demand:
    - topic: "Development Plan"
      paths:
        - modules/$MOD/plan.md
    - topic: "Test Plan"
      paths:
        - modules/$MOD/doc/TEST_PLAN.md
    - topic: "Operations Guide"
      paths:
        - modules/$MOD/doc/RUNBOOK.md
---

# $MOD Module - Agent Guide

> **For AI Agents** - Module-specific guidance  
> **Language**: English (AI-optimized)

## 1. Module Overview

TODO: Describe the purpose and scope of this module

## 2. Core Features

TODO: List the main functionalities provided by this module

## 3. Dependencies

TODO: Document upstream and downstream module dependencies

---

**Maintainer**: TBD  
**Created**: $(date +%Y-%m-%d)  
**Last Updated**: $(date +%Y-%m-%d)
EOF

echo "  ✓ AGENTS.md"

# 
echo "[3/6] ..."
python scripts/test_scaffold.py "$MOD"

# 
echo "[4/6] ..."
python scripts/docgen.py

# .context/Phase 8.5
echo "[5/6] ..."

cat > "modules/$MOD/.context/README.md" <<EOF
# .context/ - 

> ****: AI/

## 

**5**: \`overview.md\` + \`../plan.md\`  
**15**:  + \`decisions.md\`

## 3

- **overview.md**: <200
- **decisions.md**:  + ****
- **prd.md**: 

****: ❌ 

****: doc/process/CONTEXT_GUIDE.md
EOF

cat > "modules/$MOD/.context/overview.md" <<EOF
# ${MOD}

> ****: AI/  
> ****: <200  
> ****: $(date +%Y-%m-%d)

## 

[2-3]

## 

1. [1]
2. [2]
3. [3]

## 

1. [1]
2. [2]

## 

- \`../doc/CONTRACT.md\`
- \`decisions.md\` - 
EOF

cat > "modules/$MOD/.context/decisions.md" <<'EOF'
# 

> ****: AI/  
> ****:  + ****

## 

### ADR-001: []

****: []  
****: []  
****: []

---

## ⭐ 

### ERROR-001: []

****: []  
****: []  
****: []  
****: []  
****: []

**AI**: [AI]

---

## 

### REJECTED-001: []

****: []  
****: []
EOF

# Phase 6
echo ""
echo "[6/6] "
echo ""
echo "✅  '$MOD' "
echo ""
echo "📂 "
echo "   - modules/$MOD/AGENTS.mdAgent"
echo "   - modules/$MOD/README.md"
echo "   - modules/$MOD/plan.md"
echo "   - modules/$MOD/doc/ (6)"
echo "   - modules/$MOD/.context/ (3)"
echo "   - modules/$MOD/core/ ()"
echo "   - tests/$MOD/ ()"
echo ""
echo "💡 "
echo ""
echo "   0. 📝 5"
echo "      -  modules/$MOD/.context/overview.md++"
echo "      - PRD modules/$MOD/.context/prd.md"
echo "      doc/process/CONTEXT_GUIDE.md"
echo ""
echo "   1. 📋 "
echo "       modules/$MOD/plan.md"
echo ""
echo "   2. 🗄️ "
echo "      - : db/engines/postgres/schemas/tables/<table>.yaml"
echo "      - : db/engines/postgres/migrations/<num>_${MOD}_<action>_[up|down].sql"
echo "      - : make db_lint"
echo "      doc/modules/MODULE_INIT_GUIDE.md Phase 6"
echo ""
echo "   3. 🧪 "
echo "      - : cp doc/modules/TEMPLATES/TEST_DATA.md.template modules/$MOD/doc/TEST_DATA.md"
echo "      - fixtures: mkdir modules/$MOD/fixtures"
echo "      - AGENTS.md: test_data"
echo "      doc/modules/example/doc/TEST_DATA.md"
echo ""
echo "   4. 💻 "
echo "      - modules/$MOD/core/service.py"
echo "      - modules/$MOD/api/routes.pyHTTP"
echo ""
echo "   5. ✅ "
echo "      - tests/$MOD/"
echo ""
echo "   6. 🔍 "
echo "      make agent_lint    # AGENTS.md"
echo "      make db_lint       # "
echo "      make dev_check     # "
echo ""
echo "📖 "
echo "   - : doc/modules/MODULE_INIT_GUIDE.md"
echo "   - : doc/modules/example/"
echo "   - : doc/modules/MODULE_TYPES.md"
echo ""
