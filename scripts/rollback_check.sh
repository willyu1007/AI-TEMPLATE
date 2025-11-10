#!/usr/bin/env bash
set -euo pipefail

#  downFeature Flag

PREV_REF=${1:-}

if [ -z "$PREV_REF" ]; then
    echo ": bash scripts/rollback_check.sh <PREV_REF>"
    echo ": bash scripts/rollback_check.sh v0.1.0"
    exit 1
fi

echo "🔄  (: $PREV_REF)"
echo ""

# 1. 
echo "[1/3] ..."
if [ -d "migrations" ]; then
    UP_COUNT=$(find migrations -name "*_up.sql" | wc -l)
    DOWN_COUNT=$(find migrations -name "*_down.sql" | wc -l)
    
    if [ "$UP_COUNT" -eq "$DOWN_COUNT" ]; then
        echo "  ✓  (up: $UP_COUNT, down: $DOWN_COUNT)"
    else
        echo "  ❌  (up: $UP_COUNT, down: $DOWN_COUNT)"
        exit 1
    fi
else
    echo "  ⚠️  migrations/ "
fi

# 2.  Feature Flag 
echo "[2/3]  Feature Flag..."
#  feature_flags 
if grep -q "feature_flags" config/defaults.yaml 2>/dev/null; then
    echo "  ✓ Feature Flag "
else
    echo "  ⚠️   Feature Flag "
fi

# 3. 
echo "[3/3] ..."
if git rev-parse "$PREV_REF" >/dev/null 2>&1; then
    echo "  ✓ : $PREV_REF"
    
    # 
    if [ -n "$(git status --porcelain)" ]; then
        echo "  ⚠️  "
    else
        echo "  ✓ "
    fi
else
    echo "  ❌ : $PREV_REF"
    exit 1
fi

echo ""
echo "="$(printf '=%.0s' {1..48})
echo "✅ "
echo ""
echo "💡 :"
echo "   1.  down "
echo "   2.  $PREV_REF"
echo "   3. "
echo "   4. "

