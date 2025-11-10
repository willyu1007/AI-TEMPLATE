#!/usr/bin/env bash
set -euo pipefail

echo "🔍 ..."
echo ""

FAILED=0

# [1/7]  JSON 
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[1/7]  JSON "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if test -f tools/codegen/contract.json; then
    echo "✓ "
    if python - <<'PY'
import json, sys
try:
    json.load(open('tools/codegen/contract.json'))
    print("✓ contract.json ")
except Exception as e:
    print(f"❌ contract.json : {e}")
    sys.exit(1)
PY
    then
        echo "✓  JSON "
    else
        FAILED=1
    fi
else
    echo "❌ "
    FAILED=1
fi
echo ""

# [2/7] DAG 
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[2/7] DAG "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python scripts/dag_check.py; then
    echo ""
else
    FAILED=1
    echo ""
fi

# [3/7] 
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[3/7] "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python scripts/contract_compat_check.py; then
    echo ""
else
    FAILED=1
    echo ""
fi

# [4/7] 
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[4/7] "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python scripts/runtime_config_check.py; then
    echo ""
else
    FAILED=1
    echo ""
fi

# [5/7] 
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[5/7] "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python scripts/migrate_check.py; then
    echo ""
else
    FAILED=1
    echo ""
fi

# [6/7] 
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[6/7] "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python scripts/consistency_check.py; then
    echo ""
else
    FAILED=1
    echo ""
fi

# [7/7] DB 
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[7/7] DB "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
# Phase 3
if test -f doc/db/DB_SPEC.yaml; then
    echo "✓ DB_SPEC.yaml "
elif test -f docs/db/DB_SPEC.yaml; then
    echo "✓ DB_SPEC.yaml "
else
    echo "❌ DB_SPEC.yaml "
    FAILED=1
fi
echo ""

# 
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $FAILED -eq 0 ]; then
    echo "✅ "
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 0
else
    echo "❌ "
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 1
fi
