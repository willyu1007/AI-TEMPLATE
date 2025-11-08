#!/usr/bin/env bash
#
# workdoc_create.sh - 创建新的workdoc
#
# 用法: ./workdoc_create.sh <task-name>
# 或:   make workdoc_create TASK=<task-name>

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
TEMPLATES_DIR="$PROJECT_ROOT/doc/templates"

# 检查参数
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ 错误: 需要提供任务名称${NC}"
    echo "用法: $0 <task-name>"
    echo "示例: $0 implement-user-auth"
    exit 1
fi

TASK_NAME=$1

# 验证任务名称格式（小写字母、数字、连字符）
if ! [[ "$TASK_NAME" =~ ^[a-z0-9-]+$ ]]; then
    echo -e "${RED}❌ 错误: 任务名称只能包含小写字母、数字和连字符${NC}"
    echo "示例: implement-user-auth, fix-bug-123, refactor-db-layer"
    exit 1
fi

# 检查任务是否已存在
TASK_DIR="$ACTIVE_DIR/$TASK_NAME"
if [ -d "$TASK_DIR" ]; then
    echo -e "${RED}❌ 错误: 任务 '$TASK_NAME' 已存在${NC}"
    echo "路径: $TASK_DIR"
    exit 1
fi

# 检查模板是否存在
PLAN_TEMPLATE="$TEMPLATES_DIR/workdoc-plan.md"
CONTEXT_TEMPLATE="$TEMPLATES_DIR/workdoc-context.md"
TASKS_TEMPLATE="$TEMPLATES_DIR/workdoc-tasks.md"

if [ ! -f "$PLAN_TEMPLATE" ] || [ ! -f "$CONTEXT_TEMPLATE" ] || [ ! -f "$TASKS_TEMPLATE" ]; then
    echo -e "${RED}❌ 错误: 模板文件不存在${NC}"
    echo "请确保以下文件存在:"
    echo "  - $PLAN_TEMPLATE"
    echo "  - $CONTEXT_TEMPLATE"
    echo "  - $TASKS_TEMPLATE"
    exit 1
fi

# 开始创建
echo -e "${BLUE}🚀 创建workdoc: $TASK_NAME${NC}"
echo

# 创建任务目录
echo -e "${YELLOW}📁 创建目录...${NC}"
mkdir -p "$TASK_DIR"
echo -e "${GREEN}✓${NC} 已创建: $TASK_DIR"

# 复制模板文件
echo
echo -e "${YELLOW}📄 复制模板文件...${NC}"

# 复制plan.md
cp "$PLAN_TEMPLATE" "$TASK_DIR/plan.md"
# 替换占位符
TASK_TITLE=$(echo "$TASK_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1')
CURRENT_DATE=$(date +%Y-%m-%d)
sed -i.bak "s/\[Task Name\]/$TASK_TITLE/g" "$TASK_DIR/plan.md"
sed -i.bak "s/YYYY-MM-DD/$CURRENT_DATE/g" "$TASK_DIR/plan.md"
rm "$TASK_DIR/plan.md.bak"
echo -e "${GREEN}✓${NC} 已创建: plan.md"

# 复制context.md
cp "$CONTEXT_TEMPLATE" "$TASK_DIR/context.md"
sed -i.bak "s/\[Task Name\]/$TASK_TITLE/g" "$TASK_DIR/context.md"
CURRENT_DATETIME=$(date +"%Y-%m-%d %H:%M")
sed -i.bak "s/YYYY-MM-DD HH:MM/$CURRENT_DATETIME/g" "$TASK_DIR/context.md"
rm "$TASK_DIR/context.md.bak"
echo -e "${GREEN}✓${NC} 已创建: context.md"

# 复制tasks.md
cp "$TASKS_TEMPLATE" "$TASK_DIR/tasks.md"
sed -i.bak "s/\[Task Name\]/$TASK_TITLE/g" "$TASK_DIR/tasks.md"
sed -i.bak "s/YYYY-MM-DD HH:MM/$CURRENT_DATETIME/g" "$TASK_DIR/tasks.md"
sed -i.bak "s/YYYY-MM-DD/$CURRENT_DATE/g" "$TASK_DIR/tasks.md"
rm "$TASK_DIR/tasks.md.bak"
echo -e "${GREEN}✓${NC} 已创建: tasks.md"

# 显示结果
echo
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Workdoc创建成功${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
echo -e "${BLUE}📂 任务目录:${NC} $TASK_DIR"
echo
echo -e "${BLUE}📝 文件:${NC}"
echo "  - plan.md:    实施计划"
echo "  - context.md: 上下文（最重要）"
echo "  - tasks.md:   任务清单"
echo
echo -e "${YELLOW}💡 下一步:${NC}"
echo "  1. 编辑 plan.md 制定实施计划"
echo "  2. 在开发过程中持续更新 context.md"
echo "  3. 使用 tasks.md 追踪任务进度"
echo
echo -e "${YELLOW}📖 详细指南:${NC}"
echo "  doc/process/WORKDOCS_GUIDE.md"
echo

