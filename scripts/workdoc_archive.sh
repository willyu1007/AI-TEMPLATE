#!/usr/bin/env bash
#
# workdoc_archive.sh - workdoc
#
# : ./workdoc_archive.sh <task-name>
# :   make workdoc_archive TASK=<task-name>

set -e

# 
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# 
WORKDOCS_DIR="$PROJECT_ROOT/ai/workdocs"
ACTIVE_DIR="$WORKDOCS_DIR/active"
ARCHIVE_DIR="$WORKDOCS_DIR/archive"

# 
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ : ${NC}"
    echo ": $0 <task-name>"
    echo
    echo -e "${BLUE}:${NC}"
    if [ -d "$ACTIVE_DIR" ]; then
        ls -1 "$ACTIVE_DIR" 2>/dev/null || echo "  ()"
    else
        echo "  ()"
    fi
    exit 1
fi

TASK_NAME=$1

# 
TASK_DIR="$ACTIVE_DIR/$TASK_NAME"
if [ ! -d "$TASK_DIR" ]; then
    echo -e "${RED}❌ :  '$TASK_NAME' ${NC}"
    echo
    echo -e "${BLUE}:${NC}"
    if [ -d "$ACTIVE_DIR" ]; then
        ls -1 "$ACTIVE_DIR" 2>/dev/null || echo "  ()"
    else
        echo "  ()"
    fi
    exit 1
fi

# 
ARCHIVE_TARGET="$ARCHIVE_DIR/$TASK_NAME"
if [ -d "$ARCHIVE_TARGET" ]; then
    echo -e "${YELLOW}⚠️  : : $ARCHIVE_TARGET${NC}"
    echo -n "? (yes/no): "
    read -r CONFIRM
    if [ "$CONFIRM" != "yes" ]; then
        echo ""
        exit 0
    fi
    rm -rf "$ARCHIVE_TARGET"
fi

# 
echo -e "${BLUE}📦 workdoc: $TASK_NAME${NC}"
echo
echo -e "${YELLOW}:${NC} $TASK_DIR"
echo -e "${YELLOW}:${NC} $ARCHIVE_TARGET"
echo
echo -n "? (yes/no): "
read -r CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo ""
    exit 0
fi

# 
mkdir -p "$ARCHIVE_DIR"

# 
echo
echo -e "${YELLOW}📁 ...${NC}"
mv "$TASK_DIR" "$ARCHIVE_TARGET"

# 
ARCHIVE_DATE=$(date +"%Y-%m-%d %H:%M")
echo >> "$ARCHIVE_TARGET/context.md"
echo "---" >> "$ARCHIVE_TARGET/context.md"
echo >> "$ARCHIVE_TARGET/context.md"
echo "## 📦 " >> "$ARCHIVE_TARGET/context.md"
echo >> "$ARCHIVE_TARGET/context.md"
echo "- ****: $ARCHIVE_DATE" >> "$ARCHIVE_TARGET/context.md"
echo "- ****: ai/workdocs/active/$TASK_NAME" >> "$ARCHIVE_TARGET/context.md"

# 
echo
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Workdoc${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
echo -e "${BLUE}📂 :${NC} $ARCHIVE_TARGET"
echo -e "${BLUE}📅 :${NC} $ARCHIVE_DATE"
echo
echo -e "${YELLOW}💡 :${NC}"
echo "  - workdoc"
echo "  - , active/ "
echo

