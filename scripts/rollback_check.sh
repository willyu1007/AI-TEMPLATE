#!/usr/bin/env bash
set -euo pipefail

# 回滚验证脚本：检查迁移 down、Feature Flag、可切回前版本

PREV_REF=${1:-}

if [ -z "$PREV_REF" ]; then
    echo "用法: bash scripts/rollback_check.sh <PREV_REF>"
    echo "示例: bash scripts/rollback_check.sh v0.1.0"
    exit 1
fi

echo "🔄 开始回滚验证 (目标: $PREV_REF)"
echo ""

# 1. 检查迁移脚本成对存在
echo "[1/3] 检查迁移脚本..."
if [ -d "migrations" ]; then
    UP_COUNT=$(find migrations -name "*_up.sql" | wc -l)
    DOWN_COUNT=$(find migrations -name "*_down.sql" | wc -l)
    
    if [ "$UP_COUNT" -eq "$DOWN_COUNT" ]; then
        echo "  ✓ 迁移脚本成对 (up: $UP_COUNT, down: $DOWN_COUNT)"
    else
        echo "  ❌ 迁移脚本不成对 (up: $UP_COUNT, down: $DOWN_COUNT)"
        exit 1
    fi
else
    echo "  ⚠️  migrations/ 目录不存在"
fi

# 2. 检查 Feature Flag 配置（占位）
echo "[2/3] 检查 Feature Flag..."
# 这里可以检查配置文件中是否有 feature_flags 字段
if grep -q "feature_flags" config/defaults.yaml 2>/dev/null; then
    echo "  ✓ Feature Flag 配置存在"
else
    echo "  ⚠️  未找到 Feature Flag 配置（建议添加）"
fi

# 3. 验证可切回前版本（占位检查）
echo "[3/3] 验证回滚目标..."
if git rev-parse "$PREV_REF" >/dev/null 2>&1; then
    echo "  ✓ 目标引用存在: $PREV_REF"
    
    # 检查是否有未提交的变更
    if [ -n "$(git status --porcelain)" ]; then
        echo "  ⚠️  工作区有未提交变更，回滚前需清理"
    else
        echo "  ✓ 工作区干净"
    fi
else
    echo "  ❌ 目标引用不存在: $PREV_REF"
    exit 1
fi

echo ""
echo "="$(printf '=%.0s' {1..48})
echo "✅ 回滚验证通过"
echo ""
echo "💡 回滚步骤（需人工执行）:"
echo "   1. 执行数据库 down 迁移"
echo "   2. 切换代码到 $PREV_REF"
echo "   3. 重启服务"
echo "   4. 验证功能"

