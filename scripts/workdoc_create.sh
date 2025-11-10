#!/usr/bin/env bash
#
# workdoc_create.sh - workdoc
#
# : ./workdoc_create.sh <task-name>
# :   make workdoc_create TASK=<task-name>

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
TEMPLATES_DIR="$PROJECT_ROOT/doc/templates"

# 
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ : ${NC}"
    echo ": $0 <task-name>"
    echo ": $0 implement-user-auth"
    exit 1
fi

TASK_NAME=$1

# 
if ! [[ "$TASK_NAME" =~ ^[a-z0-9-]+$ ]]; then
    echo -e "${RED}❌ : ${NC}"
    echo ": implement-user-auth, fix-bug-123, refactor-db-layer"
    exit 1
fi

# 
TASK_DIR="$ACTIVE_DIR/$TASK_NAME"
if [ -d "$TASK_DIR" ]; then
    echo -e "${RED}❌ :  '$TASK_NAME' ${NC}"
    echo ": $TASK_DIR"
    exit 1
fi

# 
PLAN_TEMPLATE="$TEMPLATES_DIR/workdoc-plan.md"
CONTEXT_TEMPLATE="$TEMPLATES_DIR/workdoc-context.md"
TASKS_TEMPLATE="$TEMPLATES_DIR/workdoc-tasks.md"

if [ ! -f "$PLAN_TEMPLATE" ] || [ ! -f "$CONTEXT_TEMPLATE" ] || [ ! -f "$TASKS_TEMPLATE" ]; then
    echo -e "${RED}❌ : ${NC}"
    echo ":"
    echo "  - $PLAN_TEMPLATE"
    echo "  - $CONTEXT_TEMPLATE"
    echo "  - $TASKS_TEMPLATE"
    exit 1
fi

# 
echo -e "${BLUE}🚀 workdoc: $TASK_NAME${NC}"
echo

# 
echo -e "${YELLOW}📁 ...${NC}"
mkdir -p "$TASK_DIR"
echo -e "${GREEN}✓${NC} : $TASK_DIR"

# 
echo
echo -e "${YELLOW}📄 ...${NC}"

# plan.md
cp "$PLAN_TEMPLATE" "$TASK_DIR/plan.md"
# 
TASK_TITLE=$(echo "$TASK_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1')
CURRENT_DATE=$(date +%Y-%m-%d)
sed -i.bak "s/\[Task Name\]/$TASK_TITLE/g" "$TASK_DIR/plan.md"
sed -i.bak "s/YYYY-MM-DD/$CURRENT_DATE/g" "$TASK_DIR/plan.md"
rm "$TASK_DIR/plan.md.bak"
echo -e "${GREEN}✓${NC} : plan.md"

# context.md
cp "$CONTEXT_TEMPLATE" "$TASK_DIR/context.md"
sed -i.bak "s/\[Task Name\]/$TASK_TITLE/g" "$TASK_DIR/context.md"
CURRENT_DATETIME=$(date +"%Y-%m-%d %H:%M")
sed -i.bak "s/YYYY-MM-DD HH:MM/$CURRENT_DATETIME/g" "$TASK_DIR/context.md"
rm "$TASK_DIR/context.md.bak"
echo -e "${GREEN}✓${NC} : context.md"

# tasks.md
cp "$TASKS_TEMPLATE" "$TASK_DIR/tasks.md"
sed -i.bak "s/\[Task Name\]/$TASK_TITLE/g" "$TASK_DIR/tasks.md"
sed -i.bak "s/YYYY-MM-DD HH:MM/$CURRENT_DATETIME/g" "$TASK_DIR/tasks.md"
sed -i.bak "s/YYYY-MM-DD/$CURRENT_DATE/g" "$TASK_DIR/tasks.md"
rm "$TASK_DIR/tasks.md.bak"
echo -e "${GREEN}✓${NC} : tasks.md"

# 
echo
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Workdoc${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
echo -e "${BLUE}📂 :${NC} $TASK_DIR"
echo
echo -e "${BLUE}📝 :${NC}"
echo "  - plan.md:    "
echo "  - context.md: "
echo "  - tasks.md:   "
echo
echo -e "${YELLOW}💡 :${NC}"
echo "  1.  plan.md "
echo "  2.  context.md"
echo "  3.  tasks.md "
echo
echo -e "${YELLOW}📖 :${NC}"
echo "  doc/process/WORKDOCS_GUIDE.md"
echo

