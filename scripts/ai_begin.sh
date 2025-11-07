#!/usr/bin/env bash
set -euo pipefail

MOD=${1:-}

if [ -z "$MOD" ]; then
    echo "用法: bash scripts/ai_begin.sh <module>"
    echo "示例: bash scripts/ai_begin.sh user_auth"
    echo ""
    echo "💡 提示：建议查看 doc/modules/MODULE_INIT_GUIDE.md"
    echo "   了解完整的模块初始化流程（包含AI对话式引导）"
    exit 1
fi

echo "🚀 初始化模块: $MOD"
echo ""
echo "📚 参考：doc/modules/example/ 是完整的模块示例"
echo ""

# 创建模块目录结构（Phase 6更新）
mkdir -p "modules/$MOD/core"
mkdir -p "modules/$MOD/doc"

# 生成模块文档（Phase 6更新）
echo "[1/5] 生成模块文档..."

# README.md
cat > "modules/$MOD/README.md" <<'EOF'
# <模块名> 模块

## 职责
描述此模块的核心职责和功能范围。

## 边界
### 输入
- 来自哪些模块/服务的数据
- 期望的输入格式

### 输出
- 产出什么数据
- 输出到哪里

### 依赖
- 工具：列出使用的工具/服务
- 模块：列出依赖的其他模块

## 架构
简要描述模块内部结构和关键组件。

## 运行要求
- 环境变量
- 配置项
- 外部依赖
EOF

# plan.md（Phase 6.5更新：添加数据库和测试数据影响评估）
cat > "modules/$MOD/plan.md" <<EOF
# 计划 ($(date +%Y-%m-%d))

## 目标
明确本次迭代要实现的功能或解决的问题。

## 范围
- 包含：列出要做的事情
- 不包含：明确不做什么（避免范围蔓延）

## 接口/DB 影响
- 新增/修改的接口：
- DAG 节点变更：

---

## 数据库影响评估（必填）⭐

### 本次迭代是否涉及数据库变更？
- [ ] 是，涉及数据库变更
  - 变更类型：
    - [ ] 新建表
    - [ ] 修改表结构（增加字段）
    - [ ] 修改表结构（删除字段）
    - [ ] 修改表结构（修改字段类型）
    - [ ] 增加索引
    - [ ] 删除表（慎重！）
  - 影响表：<表名列表>
  - 影响范围：<描述>
  - 参考流程：doc/process/DB_CHANGE_GUIDE.md
  
- [ ] 否，不涉及数据库变更

### 测试数据影响（如涉及数据库变更必填）⭐
- [ ] 需要更新Fixtures
  - 影响场景：
    - [ ] minimal（最小集）
    - [ ] standard（标准集）
    - [ ] full（完整集）
- [ ] 需要更新Mock规则
  - 影响表：<表名列表>
- [ ] 不需要更新测试数据（请说明原因）

---

## 测试清单
- [ ] 单元测试
- [ ] 集成测试
- [ ] 边界情况测试

## 验证命令
\`\`\`bash
make dev_check
make db_lint       # 如涉及数据库变更
# 其他验证命令
\`\`\`

## 回滚计划
如果出现问题，如何回滚？
- 数据库迁移回滚：<down脚本路径>
- 代码回滚：<git commit hash>
- Feature Flag：<标记名称>
EOF

# CONTRACT.md（Phase 6更新：移到doc/）
cat > "modules/$MOD/doc/CONTRACT.md" <<'EOF'
# CONTRACT - 接口契约

## 输入
```json
{
  "field1": "类型和说明",
  "field2": "类型和说明"
}
```

## 输出
```json
{
  "result": "类型和说明",
  "status": "success|error"
}
```

## 错误码
- `E001`: 错误说明
- `E002`: 错误说明

## 兼容策略
- 向后兼容：不删除字段，不改变类型
- 版本管理：semver

## 示例
### 请求示例
```json
{
  "field1": "example"
}
```

### 响应示例
```json
{
  "result": "example",
  "status": "success"
}
```
EOF

# TEST_PLAN.md（Phase 6更新：移到doc/）
cat > "modules/$MOD/doc/TEST_PLAN.md" <<'EOF'
# TEST_PLAN - 测试计划

## 关键路径用例
1. **用例1**：正常流程
   - 输入：
   - 期望输出：
   - 验证点：

2. **用例2**：异常处理
   - 输入：
   - 期望输出：
   - 验证点：

## 契约测试
- 输入验证
- 输出格式验证
- 错误码测试

## 边界测试
- 空值
- 极端值
- 并发场景

## 回归测试
列出每次必须运行的回归用例。
EOF

# RUNBOOK.md（Phase 6更新：移到doc/）
cat > "modules/$MOD/doc/RUNBOOK.md" <<'EOF'
# RUNBOOK - 运维手册

## 启动
```bash
# 启动命令
```

## 调试
- 日志位置：
- 常见问题排查：
- 调试工具：

## 告警
| 告警名称 | 触发条件 | 处理步骤 |
|---------|---------|---------|
| Alert1  | 条件    | 步骤    |

## 回滚
```bash
# 回滚步骤
```

## 监控指标
- 关键指标1：
- 关键指标2：
EOF

# PROGRESS.md（Phase 6更新：移到doc/）
cat > "modules/$MOD/doc/PROGRESS.md" <<EOF
# PROGRESS - 进度与里程碑

## 当前状态
- 状态：规划中 / 开发中 / 测试中 / 已完成
- 最后更新：$(date +%Y-%m-%d)

## 里程碑
- [ ] M1: 基础功能 (目标日期)
- [ ] M2: 完整功能 (目标日期)
- [ ] M3: 优化与发布 (目标日期)

## 阻塞项
列出阻塞进度的问题。

## 已完成
- $(date +%Y-%m-%d): 初始化模块
EOF

# BUGS.md（Phase 6更新：移到doc/）
cat > "modules/$MOD/doc/BUGS.md" <<'EOF'
# BUGS - 缺陷跟踪

## 已知缺陷
- [ ] **BUG-001**: 缺陷描述
  - 影响：严重程度
  - 复现步骤：
  - 临时方案：

## 已修复
- [x] **BUG-000**: 示例缺陷（已修复）
  - 修复时间：YYYY-MM-DD
  - 修复方案：

## 复盘
对重要缺陷的根因分析和改进措施。
EOF

# CHANGELOG.md（Phase 6更新：移到doc/）
cat > "modules/$MOD/doc/CHANGELOG.md" <<EOF
# CHANGELOG - 变更日志

## [Unreleased]

## [0.1.0] - $(date +%Y-%m-%d)
### Added
- 初始化模块结构
- 创建基础文档

### Changed
-

### Fixed
-

### Removed
-
EOF

echo "  ✓ 模块文档已生成（6个文档在doc/下）"

# 生成agent.md（Phase 6新增）
echo "[2/5] 生成agent.md..."
cat > "modules/$MOD/agent.md" <<EOF
---
spec_version: "1.0"
agent_id: "modules.$MOD.v1"
role: "$MOD模块的业务逻辑Agent"
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
  inputs: []
  outputs: []

contracts:
  apis:
    - modules/$MOD/doc/CONTRACT.md

dependencies:
  upstream: []
  downstream: []

constraints:
  - "保持测试覆盖率≥80%"

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
    - topic: "开发计划"
      paths:
        - modules/$MOD/plan.md
    - topic: "测试计划"
      paths:
        - modules/$MOD/doc/TEST_PLAN.md
---

# $MOD模块Agent

## 1. 模块概述

（待补充）

## 2. 核心功能

（待补充）

## 3. 依赖关系

（待补充）

---

**维护者**: 待指定
**创建时间**: $(date +%Y-%m-%d)
EOF

echo "  ✓ agent.md已生成"

# 生成测试脚手架
echo "[3/5] 生成测试脚手架..."
python scripts/test_scaffold.py "$MOD"

# 更新索引
echo "[4/5] 更新索引..."
python scripts/docgen.py

# 提示数据库和测试数据（Phase 6新增）
echo ""
echo "[5/5] 完成！"
echo ""
echo "✅ 模块 '$MOD' 初始化完成"
echo ""
echo "📂 生成的文件："
echo "   - modules/$MOD/agent.md（Agent配置）"
echo "   - modules/$MOD/README.md（模块文档）"
echo "   - modules/$MOD/plan.md（实施计划）"
echo "   - modules/$MOD/doc/ (6个标准文档)"
echo "   - modules/$MOD/core/ (核心代码目录)"
echo "   - tests/$MOD/ (测试目录)"
echo ""
echo "💡 下一步（建议按顺序）："
echo ""
echo "   1. 📋 定义计划"
echo "      编辑 modules/$MOD/plan.md"
echo ""
echo "   2. 🗄️ 数据库变更（如需要）"
echo "      - 创建表结构: db/engines/postgres/schemas/tables/<table>.yaml"
echo "      - 创建迁移: db/engines/postgres/migrations/<num>_${MOD}_<action>_[up|down].sql"
echo "      - 运行校验: make db_lint"
echo "      参考：doc/modules/MODULE_INIT_GUIDE.md Phase 6"
echo ""
echo "   3. 🧪 测试数据定义（推荐）"
echo "      - 从模板复制: cp doc/modules/TEMPLATES/TEST_DATA.md.template modules/$MOD/doc/TEST_DATA.md"
echo "      - 创建fixtures: mkdir modules/$MOD/fixtures"
echo "      - 更新agent.md: 添加test_data字段"
echo "      参考：doc/modules/example/doc/TEST_DATA.md"
echo ""
echo "   4. 💻 实现功能"
echo "      - modules/$MOD/core/service.py（核心逻辑）"
echo "      - modules/$MOD/api/routes.py（如需HTTP接口）"
echo ""
echo "   5. ✅ 补充测试"
echo "      - tests/$MOD/（单元测试和集成测试）"
echo ""
echo "   6. 🔍 运行校验"
echo "      make agent_lint    # 校验agent.md"
echo "      make db_lint       # 校验数据库文件（如有）"
echo "      make dev_check     # 完整校验"
echo ""
echo "📖 完整指南："
echo "   - 模块初始化: doc/modules/MODULE_INIT_GUIDE.md"
echo "   - 参考示例: doc/modules/example/"
echo "   - 模块类型: doc/modules/MODULE_TYPES.md"
echo ""
