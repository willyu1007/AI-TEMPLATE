#!/usr/bin/env bash
#
# workdoc_archive.sh - 归档已完成的workdoc
#
# 用法: ./workdoc_archive.sh <task-name>
# 或:   make workdoc_archive TASK=<task-name>

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录的父目录（项目根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# 目录定义
WORKDOCS_DIR="$PROJECT_ROOT/ai/workdocs"
ACTIVE_DIR="$WORKDOCS_DIR/active"
ARCHIVE_DIR="$WORKDOCS_DIR/archive"

# 检查参数
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ 错误: 需要提供任务名称${NC}"
    echo "用法: $0 <task-name>"
    echo
    echo -e "${BLUE}可归档的任务:${NC}"
    if [ -d "$ACTIVE_DIR" ]; then
        ls -1 "$ACTIVE_DIR" 2>/dev/null || echo "  (无)"
    else
        echo "  (无)"
    fi
    exit 1
fi

TASK_NAME=$1

# 检查任务是否存在
TASK_DIR="$ACTIVE_DIR/$TASK_NAME"
if [ ! -d "$TASK_DIR" ]; then
    echo -e "${RED}❌ 错误: 任务 '$TASK_NAME' 不存在或已归档${NC}"
    echo
    echo -e "${BLUE}可归档的任务:${NC}"
    if [ -d "$ACTIVE_DIR" ]; then
        ls -1 "$ACTIVE_DIR" 2>/dev/null || echo "  (无)"
    else
        echo "  (无)"
    fi
    exit 1
fi

# 检查归档目标是否已存在
ARCHIVE_TARGET="$ARCHIVE_DIR/$TASK_NAME"
if [ -d "$ARCHIVE_TARGET" ]; then
    echo -e "${YELLOW}⚠️  警告: 归档目录已存在: $ARCHIVE_TARGET${NC}"
    echo -n "是否覆盖? (yes/no): "
    read -r CONFIRM
    if [ "$CONFIRM" != "yes" ]; then
        echo "已取消"
        exit 0
    fi
    rm -rf "$ARCHIVE_TARGET"
fi

# 确认归档
echo -e "${BLUE}📦 准备归档workdoc: $TASK_NAME${NC}"
echo
echo -e "${YELLOW}源目录:${NC} $TASK_DIR"
echo -e "${YELLOW}目标目录:${NC} $ARCHIVE_TARGET"
echo
echo -n "确认归档? (yes/no): "
read -r CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "已取消"
    exit 0
fi

# 创建归档目录
mkdir -p "$ARCHIVE_DIR"

# 移动任务
echo
echo -e "${YELLOW}📁 归档中...${NC}"
mv "$TASK_DIR" "$ARCHIVE_TARGET"

# 添加归档时间戳
ARCHIVE_DATE=$(date +"%Y-%m-%d %H:%M")
echo >> "$ARCHIVE_TARGET/context.md"
echo "---" >> "$ARCHIVE_TARGET/context.md"
echo >> "$ARCHIVE_TARGET/context.md"
echo "## 📦 归档信息" >> "$ARCHIVE_TARGET/context.md"
echo >> "$ARCHIVE_TARGET/context.md"
echo "- **归档时间**: $ARCHIVE_DATE" >> "$ARCHIVE_TARGET/context.md"
echo "- **原路径**: ai/workdocs/active/$TASK_NAME" >> "$ARCHIVE_TARGET/context.md"

# 显示结果
echo
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Workdoc已归档${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
echo -e "${BLUE}📂 归档路径:${NC} $ARCHIVE_TARGET"
echo -e "${BLUE}📅 归档时间:${NC} $ARCHIVE_DATE"
echo
echo -e "${YELLOW}💡 提示:${NC}"
echo "  - 归档的workdoc仍可查看"
echo "  - 如需恢复,可手动移回 active/ 目录"
echo

