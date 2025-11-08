# AI-TEMPLATE 互补方案：集成claude-code-infrastructure-showcase优势

> **创建时间**: 2025-11-08  
> **目的**: 将claude-showcase的自动激活、渐进式披露、dev docs、guardrail机制整合到AI-TEMPLATE  
> **状态**: 设计方案  
> **预期收益**: 提升AI工作效率30%+，降低token成本25%+

---

## 执行摘要

### 核心互补点

| 序号 | 互补项 | 来源 | 预期效果 |
|------|--------|------|----------|
| 1 | **技能自动激活** | claude-showcase | 减少手动指定文档，提升响应速度 |
| 2 | **渐进式披露** | claude-showcase | 大文档分块加载，降低token成本25% |
| 3 | **Dev docs模式** | claude-showcase | 增强上下文恢复能力，节省重新理解时间 |
| 4 | **Guardrail机制** | claude-showcase | 强制质量检查，避免常见错误 |

### 整体架构

```
AI-TEMPLATE现有架构
├── agent.md (编排配置)
├── context_routes (路由规则)
├── Makefile (自动化工具)
└── doc/ (文档体系)

+

claude-showcase优势
├── skill-rules.json (触发规则) → 整合为 agent-triggers.yaml
├── 渐进式披露 (主文件+resources) → 改造大文档
├── dev docs (plan/context/tasks) → 新增 ai/workdocs/
└── guardrail (block模式) → 扩展 agent.md

=

增强版AI-TEMPLATE
├── agent.md (扩展：增加triggers字段)
├── agent-triggers.yaml (新增：自动激活规则)
├── doc/ (改造：渐进式披露)
├── ai/workdocs/ (新增：dev docs支持)
└── Makefile (扩展：guardrail命令)
```

---

## 互补方案1: 技能自动激活机制

### 1.1 现状分析

#### AI-TEMPLATE现有机制
```yaml
# 当前：手动路由
context_routes:
  on_demand:
    - topic: "数据库操作"  # ← 需要AI判断主题
      paths: [/doc/db/DB_SPEC.yaml]
```

**问题**:
- ❌ 依赖AI主动判断"这是数据库操作"
- ❌ 可能遗漏相关文档
- ❌ 无法基于文件路径自动触发

#### claude-showcase机制
```json
{
  "backend-dev-guidelines": {
    "fileTriggers": {
      "pathPatterns": ["api/**/*.ts"],
      "contentPatterns": ["router\\."]
    },
    "promptTriggers": {
      "keywords": ["controller", "service", "API"],
      "intentPatterns": ["(create|add).*?(route|endpoint)"]
    }
  }
}
```

**优势**:
- ✅ 基于文件路径自动触发
- ✅ 基于prompt关键词自动触发
- ✅ 无需AI判断，系统自动匹配

---

### 1.2 集成方案

#### 方案设计：agent-triggers.yaml

在AI-TEMPLATE中新增 `doc/orchestration/agent-triggers.yaml`:

```yaml
version: "1.0"
description: "AI智能体自动触发规则"

# 全局配置
config:
  enabled: true
  priority_order: ["critical", "high", "medium", "low"]
  enforcement_default: "suggest"  # suggest|warn|block

# 触发规则
triggers:
  # 规则1: 数据库操作自动触发
  database-operations:
    priority: high
    enforcement: suggest
    description: "数据库操作相关文档"
    
    # 文件触发
    file_triggers:
      path_patterns:
        - "db/engines/**/*.sql"
        - "db/engines/**/*.yaml"
        - "migrations/**/*.sql"
        - "modules/*/models/**/*.py"
      content_patterns:
        - "CREATE TABLE"
        - "ALTER TABLE"
        - "prisma\\."
        - "async def.*query"
    
    # Prompt触发
    prompt_triggers:
      keywords:
        - "数据库"
        - "database"
        - "迁移"
        - "migration"
        - "表结构"
        - "schema"
      intent_patterns:
        - "(创建|修改|删除).{0,5}(表|字段|索引)"
        - "(add|create|modify|delete).{0,10}(table|column|index)"
    
    # 触发时加载的文档
    load_documents:
      - path: /doc/db/DB_SPEC.yaml
        priority: critical
      - path: /doc/db/SCHEMA_GUIDE.md
        priority: high
      - path: /doc/process/DB_CHANGE_GUIDE.md
        priority: high
      - path: /db/engines/README.md
        priority: medium

  # 规则2: 模块开发自动触发
  module-development:
    priority: high
    enforcement: suggest
    description: "模块开发相关文档"
    
    file_triggers:
      path_patterns:
        - "modules/*/agent.md"
        - "modules/*/README.md"
        - "modules/*/plan.md"
        - "modules/*/core/**/*.py"
        - "modules/*/api/**/*.py"
    
    prompt_triggers:
      keywords:
        - "模块"
        - "module"
        - "初始化模块"
        - "create module"
        - "新建模块"
      intent_patterns:
        - "(创建|初始化|添加).{0,5}模块"
        - "(create|initialize|add).{0,10}module"
    
    load_documents:
      - path: /doc/modules/MODULE_INIT_GUIDE.md
        priority: critical
      - path: /doc/modules/MODULE_TYPES.md
        priority: high
      - path: /doc/modules/example/README.md
        priority: medium

  # 规则3: 契约变更（Guardrail模式）
  contract-changes:
    priority: critical
    enforcement: block  # ← 强制检查
    description: "契约变更必须遵守兼容性规则"
    
    file_triggers:
      path_patterns:
        - "tools/*/contract.json"
        - "modules/*/doc/CONTRACT.md"
    
    prompt_triggers:
      keywords:
        - "契约"
        - "contract"
        - "API变更"
        - "breaking change"
      intent_patterns:
        - "(修改|删除|变更).{0,5}(契约|接口|API)"
        - "(modify|delete|change).{0,10}(contract|API|interface)"
    
    load_documents:
      - path: /doc/policies/safety.md
        priority: critical
      - path: /doc/process/CONVENTIONS.md
        priority: high
    
    # Block模式配置
    block_config:
      message: |
        ⚠️ BLOCKED - 契约变更检查
        
        📋 必须执行:
        1. 运行: make contract_compat_check
        2. 确认无破坏性变更
        3. 如有破坏性变更，更新VERSION
        4. 在CHANGELOG.md中记录
        
        原因: 保护契约兼容性
        文件: {file_path}
      
      skip_conditions:
        # 跳过条件
        file_markers:
          - "# SKIP_CONTRACT_CHECK"
        env_override: "SKIP_CONTRACT_GUARD"
        make_commands_passed:
          - "make contract_compat_check"

  # 规则4: agent.md编辑（Guardrail模式）
  agent-config-changes:
    priority: critical
    enforcement: warn
    description: "agent.md变更需要验证"
    
    file_triggers:
      path_patterns:
        - "agent.md"
        - "modules/*/agent.md"
    
    load_documents:
      - path: /schemas/agent.schema.yaml
        priority: critical
      - path: /doc/orchestration/routing.md
        priority: high
    
    block_config:
      message: |
        ⚠️ WARNING - agent.md变更
        
        📋 建议执行:
        1. 运行: make agent_lint
        2. 运行: make doc_route_check
        3. 确认YAML Front Matter格式正确
        
        继续? (yes/no)
      
      skip_conditions:
        make_commands_passed:
          - "make agent_lint"

  # 规则5: 文档编写（自动加载规范）
  documentation-writing:
    priority: medium
    enforcement: suggest
    description: "文档编写规范"
    
    file_triggers:
      path_patterns:
        - "doc/**/*.md"
        - "modules/*/doc/**/*.md"
        - "README.md"
    
    prompt_triggers:
      keywords:
        - "文档"
        - "documentation"
        - "写文档"
        - "更新文档"
    
    load_documents:
      - path: /doc/process/CONVENTIONS.md
        priority: high

# 触发器元数据
metadata:
  total_rules: 5
  enforcement_modes:
    suggest: "建议加载文档，AI可以选择忽略"
    warn: "警告并建议，需要用户确认继续"
    block: "阻止操作，必须满足条件才能继续"
  
  priority_levels:
    critical: "最高优先级，必须立即加载"
    high: "高优先级，强烈建议加载"
    medium: "中优先级，可选加载"
    low: "低优先级，按需加载"
```

---

### 1.3 实现机制

#### 触发器执行流程

```
用户输入 Prompt
      ↓
┌─────────────────────────────────────┐
│ 1. 分析Prompt和当前编辑的文件      │
│    - 提取关键词                     │
│    - 识别文件路径                   │
│    - 分析用户意图                   │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│ 2. 匹配agent-triggers.yaml规则     │
│    - file_triggers匹配              │
│    - prompt_triggers匹配            │
│    - 优先级排序                     │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│ 3. 根据enforcement模式处理         │
│                                      │
│  suggest模式:                       │
│    → 在响应中建议文档               │
│    → AI可选择性加载                 │
│                                      │
│  warn模式:                          │
│    → 显示警告信息                   │
│    → 需要用户确认继续               │
│                                      │
│  block模式:                         │
│    → 阻止操作                       │
│    → 显示必须执行的步骤             │
│    → 检查skip_conditions            │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│ 4. 加载文档到上下文                │
│    - 按优先级加载                   │
│    - 合并到当前上下文               │
└─────────────────────────────────────┘
      ↓
    执行任务
```

#### 实现方式

**方式A: Python脚本实现（推荐）**

创建 `scripts/agent_trigger.py`:

```python
#!/usr/bin/env python3
"""
AI Agent自动触发器
实现类似claude-showcase的skill-rules.json机制
"""
import re
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

class AgentTrigger:
    def __init__(self, config_path: str = "doc/orchestration/agent-triggers.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.rules = self.config.get("triggers", {})
    
    def match_file(self, file_path: str) -> List[Dict[str, Any]]:
        """匹配文件路径触发器"""
        matched = []
        
        for rule_id, rule in self.rules.items():
            file_triggers = rule.get("file_triggers", {})
            path_patterns = file_triggers.get("path_patterns", [])
            
            for pattern in path_patterns:
                # 转换glob pattern为正则表达式
                regex_pattern = pattern.replace("**", ".*").replace("*", "[^/]*")
                if re.match(regex_pattern, file_path):
                    matched.append({
                        "rule_id": rule_id,
                        "rule": rule,
                        "trigger_type": "file_path",
                        "matched_pattern": pattern
                    })
                    break
        
        return matched
    
    def match_prompt(self, prompt: str) -> List[Dict[str, Any]]:
        """匹配Prompt触发器"""
        matched = []
        
        for rule_id, rule in self.rules.items():
            prompt_triggers = rule.get("prompt_triggers", {})
            
            # 检查关键词
            keywords = prompt_triggers.get("keywords", [])
            for keyword in keywords:
                if keyword.lower() in prompt.lower():
                    matched.append({
                        "rule_id": rule_id,
                        "rule": rule,
                        "trigger_type": "keyword",
                        "matched_keyword": keyword
                    })
                    break
            
            # 检查意图模式
            intent_patterns = prompt_triggers.get("intent_patterns", [])
            for pattern in intent_patterns:
                if re.search(pattern, prompt, re.IGNORECASE):
                    matched.append({
                        "rule_id": rule_id,
                        "rule": rule,
                        "trigger_type": "intent_pattern",
                        "matched_pattern": pattern
                    })
                    break
        
        return matched
    
    def get_documents_to_load(self, matched_rules: List[Dict[str, Any]]) -> List[str]:
        """获取需要加载的文档列表"""
        documents = []
        
        # 按优先级排序
        priority_order = self.config.get("config", {}).get("priority_order", 
                                                             ["critical", "high", "medium", "low"])
        
        # 收集所有文档
        all_docs = []
        for match in matched_rules:
            rule = match["rule"]
            load_docs = rule.get("load_documents", [])
            for doc in load_docs:
                all_docs.append(doc)
        
        # 去重并按优先级排序
        seen = set()
        for priority_level in priority_order:
            for doc in all_docs:
                if doc["path"] not in seen and doc.get("priority") == priority_level:
                    documents.append(doc["path"])
                    seen.add(doc["path"])
        
        return documents
    
    def check_enforcement(self, matched_rules: List[Dict[str, Any]], 
                         file_path: Optional[str] = None) -> Dict[str, Any]:
        """检查enforcement模式"""
        for match in matched_rules:
            rule = match["rule"]
            enforcement = rule.get("enforcement", "suggest")
            
            if enforcement == "block":
                block_config = rule.get("block_config", {})
                
                # 检查跳过条件
                skip_conditions = block_config.get("skip_conditions", {})
                
                # 检查文件标记
                if file_path:
                    file_markers = skip_conditions.get("file_markers", [])
                    with open(file_path) as f:
                        content = f.read()
                        if any(marker in content for marker in file_markers):
                            continue
                
                # 检查make命令是否通过
                make_commands = skip_conditions.get("make_commands_passed", [])
                # TODO: 实际检查make命令结果
                
                # 如果没有满足跳过条件，返回block
                return {
                    "action": "block",
                    "message": block_config.get("message", "").format(file_path=file_path or ""),
                    "rule_id": match["rule_id"]
                }
            
            elif enforcement == "warn":
                block_config = rule.get("block_config", {})
                return {
                    "action": "warn",
                    "message": block_config.get("message", ""),
                    "rule_id": match["rule_id"]
                }
        
        return {"action": "suggest"}

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python agent_trigger.py <file_path> [prompt]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else ""
    
    trigger = AgentTrigger()
    
    # 匹配规则
    file_matches = trigger.match_file(file_path)
    prompt_matches = trigger.match_prompt(prompt)
    all_matches = file_matches + prompt_matches
    
    if not all_matches:
        print("✓ 无触发规则匹配")
        sys.exit(0)
    
    # 检查enforcement
    enforcement_result = trigger.check_enforcement(all_matches, file_path)
    
    if enforcement_result["action"] == "block":
        print(f"❌ BLOCKED\n\n{enforcement_result['message']}")
        sys.exit(1)
    
    elif enforcement_result["action"] == "warn":
        print(f"⚠️  WARNING\n\n{enforcement_result['message']}")
        # 等待用户确认
        response = input("\n继续? (yes/no): ")
        if response.lower() != "yes":
            sys.exit(1)
    
    # 获取要加载的文档
    documents = trigger.get_documents_to_load(all_matches)
    
    if documents:
        print(f"\n📚 建议加载以下文档:")
        for doc in documents:
            print(f"  - {doc}")
    
    print("\n✓ 触发器检查完成")

if __name__ == "__main__":
    main()
```

**集成到Makefile**:

```makefile
# agent触发器检查
agent_trigger_check:
	@if [ -z "$(FILE)" ]; then \
		echo "❌ 错误：需要指定 FILE 参数"; \
		exit 1; \
	fi
	@python scripts/agent_trigger.py $(FILE) "$(PROMPT)"

# 在dev_check中添加（可选）
dev_check: ... agent_trigger_check ...
```

---

### 1.4 与现有context_routes的协同

```yaml
# agent.md 扩展

context_routes:
  # 原有的静态路由
  always_read: [...]
  on_demand: [...]
  by_scope: [...]
  
  # 新增：动态触发器
  triggers:
    enabled: true
    config_ref: /doc/orchestration/agent-triggers.yaml
    execution_mode: "pre_task"  # pre_task|on_demand
    
    # 触发器覆盖
    overrides:
      - rule: "contract-changes"
        enforcement: "block"  # 强制block模式
      - rule: "documentation-writing"
        enabled: false  # 禁用某规则
```

---

### 1.5 预期效果

| 指标 | 优化前 | 优化后 | 改进 |
|------|--------|--------|------|
| **文档加载准确率** | 70% (依赖AI判断) | 95% (自动匹配) | ⬆️ 36% |
| **响应延迟** | 需要AI思考主题 | 直接匹配触发 | ⬇️ 50% |
| **遗漏关键文档** | 30%可能遗漏 | <5%遗漏 | ⬆️ 83% |
| **Guardrail覆盖** | 手动提醒 | 自动阻止 | ⬆️ 100% |

---

## 互补方案2: 渐进式披露（Progressive Disclosure）

### 2.1 现状分析

#### AI-TEMPLATE大文档问题

| 文档 | 行数 | Token估算 | 问题 |
|------|------|-----------|------|
| safety.md | 299 | ~450 | always_read，每次必加载 |
| MODULE_INIT_GUIDE.md | 1200 | ~1800 | 一次性加载，实际只需部分 |
| CLAUDE_INTEGRATION_GUIDE.md | 880 | ~1320 | 大而全，但场景特定 |
| DB_CHANGE_GUIDE.md | 688 | ~1000 | 多场景，但每次只用一种 |

**问题**:
- ❌ 大文档一次性加载，浪费token
- ❌ AI需要从大文档中找相关部分
- ❌ 无法精确加载所需章节

#### claude-showcase渐进式披露

```
backend-dev-guidelines/
├── SKILL.md (304行，主文件)
│   ├── § Overview
│   ├── § Navigation (指向resources)
│   └── § Quick Reference
└── resources/
    ├── routing.md (200行)
    ├── controllers.md (180行)
    ├── services.md (220行)
    ├── repositories.md (150行)
    ├── testing.md (240行)
    ├── error-handling.md (160行)
    └── ... (12个resource文件)
```

**优势**:
- ✅ 主文件<500行，快速概览
- ✅ Resources按需加载
- ✅ 每个resource聚焦单一主题

---

### 2.2 集成方案：改造大文档

#### 改造策略

**原则**:
- 主文件 ≤ 300行（概览+导航+快速参考）
- Resources ≤ 200行/文件（单一主题深入）
- 保持原文档路径（向后兼容）

---

#### 示例1: 拆分MODULE_INIT_GUIDE.md

**当前**: `doc/modules/MODULE_INIT_GUIDE.md` (1200行)

**改造后**:

```
doc/modules/MODULE_INIT_GUIDE.md (300行，主文件)
doc/modules/resources/
├── init-planning.md (Phase 1详细，200行)
├── init-directory.md (Phase 2详细，150行)
├── init-documents.md (Phase 3详细，250行)
├── init-registration.md (Phase 4详细，120行)
├── init-validation.md (Phase 5详细，100行)
├── init-database.md (Phase 6详细，180行)
├── init-testdata.md (Phase 7详细，200行)
└── init-code.md (Phase 9详细，150行)
```

**主文件结构**:

```markdown
# 模块初始化指南

> **用途**: 指导在现有项目中添加新模块
> **完整文档**: 本文件+8个resource文件

---

## 快速开始

### 使用脚本（推荐）
\`\`\`bash
make ai_begin MODULE=<name>
\`\`\`

### 手动创建
按照完整流程执行 → 见§完整流程

---

## 完整流程概览

### Phase 1: 规划（5-10分钟）
**目标**: 确定模块信息（名称、类型、层级、接口）

**快速指引**:
- 询问模块名称和描述
- 确定模块类型（参考MODULE_TYPES.md）
- 决定是否需要api/和frontend/

**详细指南**: → `resources/init-planning.md`

---

### Phase 2: 创建目录（2-3分钟）
**目标**: 创建基础目录结构

**快速指引**:
\`\`\`bash
mkdir -p modules/$MODULE/{core,doc}
\`\`\`

**详细指南**: → `resources/init-directory.md`

---

### Phase 3: 生成文档（10-15分钟）
**目标**: 创建8个必备文档

**快速指引**:
- agent.md（从TEMPLATES复制）
- README.md（从TEMPLATES复制）
- doc/下6个文档

**详细指南**: → `resources/init-documents.md`

---

### Phase 4-9: [类似结构]

---

## AI执行规范

### 必须做的事
✅ 询问是否需要api/和frontend/
✅ 创建完整的doc/子目录
✅ 更新registry.yaml
✅ 运行全部校验

**详细规范**: → `resources/init-documents.md` § AI执行规范

---

## 常见问题

### Q1: 如何判断是否需要api/子目录？
**A**: 询问用户是否对外提供HTTP接口

**详细解答**: → `resources/init-planning.md` § 决策树

### Q2-5: [列出问题，指向详细resource]

---

## Resources索引

| Resource | 内容 | 何时阅读 |
|----------|------|----------|
| init-planning.md | Phase 1详细流程 | 规划阶段 |
| init-directory.md | Phase 2详细流程 | 创建目录 |
| init-documents.md | Phase 3详细流程 | 生成文档 |
| init-registration.md | Phase 4详细流程 | 注册模块 |
| init-validation.md | Phase 5详细流程 | 校验 |
| init-database.md | Phase 6详细流程 | 数据库变更 |
| init-testdata.md | Phase 7详细流程 | 测试数据 |
| init-code.md | Phase 9详细流程 | 初始代码 |

---

## 版本历史
- 2025-11-08: v2.0 渐进式披露改造
- 2025-11-07: v1.0 创建
```

**Resource文件示例** (`init-planning.md`):

```markdown
# 模块初始化 - Phase 1: 规划

> **所属**: MODULE_INIT_GUIDE.md Phase 1  
> **用途**: Phase 1的详细执行指南  
> **时间**: 5-10分钟

---

## 目标
确定模块的基本信息、类型、层级和接口定义

---

## 1.1 确定模块信息

### AI对话脚本

\`\`\`
AI: 让我们创建一个新模块。首先需要了解基本信息：

Q1: 模块名称？（小写+下划线，如user_auth）
用户: [输入]

Q2: 模块功能？（一句话描述）
用户: [输入]

Q3: 模块类型？
  - 1_Assign: 基础业务模块（用户、订单）
  - 2_Select: 选择/查询模块
  - 3_SelectMethod: 算法选择
  - 4_Aggregator: 聚合模块
  
详见: MODULE_TYPES.md

用户: [选择]

Q4: 模块层级？（1-4）
用户: [输入]
\`\`\`

### 信息记录表

| 字段 | 值 | 备注 |
|------|---|------|
| entity | _______ | 模块名 |
| description | _______ | 功能描述 |
| type | _______ | 模块类型 |
| level | _______ | 层级 |

---

## 1.2 决策树：api/和frontend/

### 决策流程图

\`\`\`
模块是否对外提供HTTP接口？
├─ 是 → 创建 api/ 子目录
│   └─ 询问接口类型：RESTful / GraphQL / WebSocket
└─ 否 → 不创建（仅提供Python函数）

模块是否有特定UI组件？
├─ 是 → 创建 frontend/ 子目录
│   └─ 询问组件类型：React / Vue / Angular
└─ 否 → 不创建（使用通用UI）
\`\`\`

### AI对话脚本

\`\`\`
AI: 接下来确定模块的接口需求：

Q5: 该模块是否对外提供HTTP接口？
  - 是：创建 api/ 子目录
  - 否：仅内部调用，不创建

用户: [是/否]

[如果是]
AI: 接口类型？
  - RESTful API（推荐）
  - GraphQL
  - WebSocket
  
用户: [选择]

Q6: 该模块是否有特定的UI组件？
  - 是：创建 frontend/ 子目录
  - 否：使用通用UI组件

用户: [是/否]

[如果是]
AI: 前端框架？
  - React（推荐）
  - Vue
  - Angular
  
用户: [选择]
\`\`\`

### 决策记录

| 决策 | 结果 | 说明 |
|------|------|------|
| has_api | true/false | 是否创建api/ |
| api_type | RESTful/GraphQL/... | 接口类型 |
| has_frontend | true/false | 是否创建frontend/ |
| frontend_framework | React/Vue/... | 前端框架 |

---

## 1.3 确认模块结构

### 结构展示模板

\`\`\`
AI: 根据您的选择，将创建以下结构：

modules/<entity>/
├── agent.md             ✅ 必须
├── README.md            ✅ 必须
├── plan.md              ✅ 必须
├── doc/                 ✅ 必须 (6个文档)
├── core/                ✅ 必须 (业务逻辑)
[如has_api=true]
├── api/                 ⚡ 可选 (HTTP接口)
[如has_frontend=true]
├── frontend/            ⚡ 可选 (UI组件)
└── models/              ⚡ 可选 (数据模型)

请确认？
\`\`\`

---

## 1.4 依赖关系确认

### AI对话脚本

\`\`\`
AI: 最后，确认模块的依赖关系：

Q7: 该模块依赖哪些上游模块？
  - common.models（基础模型，默认）
  - 其他业务模块（如有）

用户: [列举]

Q8: 该模块输出到哪些下游？
  - orchestrator.main（编排器，默认）
  - 其他模块（如有）

用户: [列举]
\`\`\`

---

## 输出物

Phase 1完成后，应有清晰的模块规划：

- ✅ 模块基本信息（entity, type, level）
- ✅ 接口决策（has_api, has_frontend）
- ✅ 目录结构确认
- ✅ 依赖关系明确

---

## 下一步

→ Phase 2: 创建目录 (`resources/init-directory.md`)

---

**关联文档**:
- 主文档: MODULE_INIT_GUIDE.md
- 模块类型: MODULE_TYPES.md
- 职责划分: temp/app_frontend_职责划分说明.md
```

---

#### 示例2: 拆分DB_CHANGE_GUIDE.md

**当前**: `doc/process/DB_CHANGE_GUIDE.md` (688行)

**改造后**:

```
doc/process/DB_CHANGE_GUIDE.md (250行，主文件)
doc/process/resources/
├── db-create-table.md (创建表完整指南，180行)
├── db-alter-table.md (修改表完整指南，200行)
├── db-drop-table.md (删除表完整指南，150行)
├── db-migration-script.md (迁移脚本编写，160行)
└── db-test-data.md (测试数据更新，120行)
```

**主文件结构**:

```markdown
# 数据库变更指南

> **用途**: 指导安全的数据库变更操作
> **完整文档**: 本文件+5个resource文件

---

## 快速决策树

\`\`\`
你的变更类型？
├─ 创建新表 → db-create-table.md
├─ 修改现有表 → db-alter-table.md
├─ 删除表 → db-drop-table.md
├─ 优化索引 → db-alter-table.md § 索引优化
└─ 数据迁移 → db-migration-script.md
\`\`\`

---

## 标准流程（概览）

### Step 1: 规划变更
- 确定变更类型
- 评估影响范围
- 制定回滚方案

**详见**: 各resource文件的"规划"章节

### Step 2: 创建Table YAML
- 编写表结构定义
- 定义索引和外键

**详见**: `db-create-table.md` 或 `db-alter-table.md`

### Step 3: 编写迁移脚本
- 创建up.sql（升级）
- 创建down.sql（回滚）

**详见**: `db-migration-script.md`

### Step 4-6: [类似结构]

---

## Resource索引

| Resource | 适用场景 | 何时阅读 |
|----------|---------|----------|
| db-create-table.md | 创建新表 | 新增业务实体 |
| db-alter-table.md | 修改表结构 | 增删改字段、索引 |
| db-drop-table.md | 删除表 | 废弃功能 |
| db-migration-script.md | 编写迁移脚本 | 所有变更 |
| db-test-data.md | 更新测试数据 | 变更后 |

---

## 常见场景快速入口

### 场景1: 新模块需要新表
→ `db-create-table.md`

### 场景2: 给现有表增加字段
→ `db-alter-table.md` § 增加字段

### 场景3: 删除废弃的表
→ `db-drop-table.md`

### 场景4: 优化查询性能
→ `db-alter-table.md` § 索引优化

---

## 安全检查清单

- [ ] 已创建Table YAML
- [ ] 已编写up和down迁移脚本
- [ ] 已运行 make db_lint
- [ ] 已更新测试数据
- [ ] 已在dev环境测试
- [ ] 已准备回滚方案

**详细清单**: → 各resource文件的"检查清单"章节
```

---

### 2.3 触发器集成

更新 `agent-triggers.yaml`，支持渐进式加载：

```yaml
triggers:
  database-operations:
    load_documents:
      # 先加载主文件
      - path: /doc/process/DB_CHANGE_GUIDE.md
        priority: critical
        type: main
      
      # 根据场景加载resource
      - path: /doc/process/resources/db-create-table.md
        priority: high
        type: resource
        conditions:
          prompt_contains: ["创建表", "create table", "新表"]
      
      - path: /doc/process/resources/db-alter-table.md
        priority: high
        type: resource
        conditions:
          prompt_contains: ["修改表", "alter table", "增加字段", "删除字段"]
      
      - path: /doc/process/resources/db-drop-table.md
        priority: high
        type: resource
        conditions:
          prompt_contains: ["删除表", "drop table", "废弃表"]
```

---

### 2.4 实施优先级

| 文档 | 行数 | 拆分收益 | 优先级 |
|------|------|----------|--------|
| MODULE_INIT_GUIDE.md | 1200 | 节省~900 tokens | 🔴 高 |
| DB_CHANGE_GUIDE.md | 688 | 节省~500 tokens | 🔴 高 |
| safety.md | 299 | 节省~150 tokens | 🟡 中 |
| agent.md | 263 | 已达标，不拆分 | ⚪ 无 |

---

### 2.5 预期效果

| 指标 | 优化前 | 优化后 | 改进 |
|------|--------|--------|------|
| **平均文档大小** | 600行 | 250行(主)+150行(resource) | ⬇️ 33% |
| **Token消耗** | 1次加载全部 | 主文件+按需resource | ⬇️ 25% |
| **加载精度** | 加载整个大文档 | 精确到相关章节 | ⬆️ 80% |
| **AI查找时间** | 需要扫描全文 | 直接定位resource | ⬇️ 60% |

---

## 互补方案3: Dev Docs模式

### 3.1 现状分析

#### AI-TEMPLATE现有机制

```
ai/
├── LEDGER.md (任务清册)
└── sessions/
    └── <date>_<name>/
        ├── AI-SR-plan.md (方案预审)
        └── AI-SR-impl.md (实施自审)
```

**优势**:
- ✅ 有会话历史记录
- ✅ 有AI-SR文档

**缺少**:
- ❌ 无专门的上下文恢复文件
- ❌ 无任务进度追踪
- ❌ 无关键决策记录

#### claude-showcase dev docs

```
dev/active/[task]/
├── [task]-plan.md (战略计划)
├── [task]-context.md (关键上下文)
└── [task]-tasks.md (任务清单)
```

**优势**:
- ✅ 专门的上下文恢复
- ✅ SESSION PROGRESS实时更新
- ✅ 任务清单追踪

---

### 3.2 集成方案

#### 目录结构

```
ai/
├── LEDGER.md (保留，总清册)
├── sessions/ (保留，会话历史)
│   └── <date>_<name>/
│       ├── AI-SR-plan.md
│       └── AI-SR-impl.md
└── workdocs/ (新增，dev docs)
    ├── active/ (进行中)
    │   └── <task-name>/
    │       ├── plan.md
    │       ├── context.md
    │       └── tasks.md
    └── archive/ (已完成)
        └── <task-name>/
            └── ...
```

---

#### 文件模板

**plan.md** (战略计划):

```markdown
# [Task Name] - 实施计划

> **创建时间**: 2025-11-08  
> **预计时间**: X天  
> **状态**: 进行中

---

## 执行摘要

### 目标
[简要说明要实现什么]

### 范围
- ✅ 包含: [列举]
- ❌ 不包含: [列举]

---

## 当前状态分析

### 现状
[当前系统状态]

### 问题
1. [问题1]
2. [问题2]

---

## 实施阶段

### Phase 1: [名称] (X小时)

**目标**: [简述]

**任务**:
- Task 1.1: [名称]
  - 验收标准: [具体可验证的标准]
  - 文件: [涉及哪些文件]
  - 风险: [风险评估]

- Task 1.2: [名称]
  - ...

### Phase 2-N: [类似结构]

---

## 风险管理

### 高风险项
1. **[风险名称]**
   - 影响: [描述]
   - 缓解措施: [方案]
   - 应急预案: [备选方案]

---

## 成功指标

- [ ] 功能指标: [可测量的指标]
- [ ] 质量指标: 测试覆盖率≥80%
- [ ] 性能指标: [响应时间等]
- [ ] 文档指标: 所有文档更新

---

## 时间线

| Phase | 预计时间 | 实际时间 | 状态 |
|-------|---------|---------|------|
| Phase 1 | 2h | - | ⏳ |
| Phase 2 | 3h | - | ⏳ |
| ... | ... | ... | ... |

---

## 依赖关系

### 上游依赖
- [依赖项1]: [说明]

### 下游影响
- [影响项1]: [说明]

---

## 相关资源

- 契约: [文件路径]
- 设计文档: [文件路径]
- 相关Issue: [链接]
```

---

**context.md** (关键上下文，**最重要**):

```markdown
# [Task Name] - 上下文

> **更新频率**: 每完成一个milestone就更新  
> **上次更新**: 2025-11-08 15:30

---

## ⚡ SESSION PROGRESS (重要！)

### ✅ COMPLETED (已完成)
- ✅ [2025-11-08 14:00] Task 1.1: [名称]
  - 文件: modules/user/core/service.py
  - 提交: commit abc123
  
- ✅ [2025-11-08 15:00] Task 1.2: [名称]
  - 文件: modules/user/api/routes.py
  - 提交: commit def456

### 🟡 IN PROGRESS (进行中)
- 🟡 Task 2.1: [名称]
  - 文件: modules/user/models/schemas.py
  - 进度: 70% (已完成字段定义，待添加验证)
  - 下一步: 添加Pydantic验证器

### ⏳ PENDING (待处理)
- ⏳ Task 2.2: [名称]
- ⏳ Task 3.1: [名称]

### ⚠️ BLOCKERS (阻塞)
- ⚠️ [问题描述]
  - 原因: [说明]
  - 解决方案: [计划]

---

## 关键文件

### modules/user/core/service.py
- **职责**: 用户业务逻辑
- **状态**: ✅ 完成
- **关键函数**:
  - `create_user()`: 创建用户，已实现验证逻辑
  - `get_user()`: 获取用户，TODO: 添加缓存

### modules/user/api/routes.py
- **职责**: 用户API路由
- **状态**: ✅ 完成
- **关键路由**:
  - POST /users/: 创建用户
  - GET /users/{id}: 获取用户

### modules/user/models/schemas.py
- **职责**: 用户数据模型
- **状态**: 🟡 进行中 (70%)
- **已完成**: 基础字段定义
- **待完成**: Pydantic验证器

---

## 关键决策

### Decision 1: [决策标题]
- **日期**: 2025-11-08
- **决策**: [具体决策]
- **原因**: [为什么这样决策]
- **影响**: [影响范围]
- **备选方案**: [被放弃的方案及原因]

### Decision 2: [决策标题]
- ...

---

## 错误记录（重要！）

### ERROR-001: [错误标题]
- **日期**: 2025-11-08
- **错误**: [做了什么错事]
- **后果**: [导致了什么问题]
- **教训**: [应该怎么做]
- **⚠️ AI注意**: [警告AI不要重复这个错误]

---

## 技术约束

### 已知约束
1. [约束1]: [说明]
2. [约束2]: [说明]

### 依赖版本
- Python: 3.9+
- FastAPI: 0.104+
- Pydantic: 2.0+

---

## Quick Resume（快速恢复）

**如果上下文丢失，按以下步骤恢复**:

1. **读取本文件** (context.md)
2. **检查SESSION PROGRESS** - 了解当前状态
3. **阅读"进行中"任务** - 知道要做什么
4. **检查关键文件** - 了解代码状态
5. **继续下一步**: [具体指示]

**当前下一步**:
- 在 `modules/user/models/schemas.py` 添加Pydantic验证器
- 参考 `doc/process/CONVENTIONS.md` § Pydantic规范

---

## 测试策略

- 单元测试: tests/user/test_service.py ✅
- 集成测试: tests/user/test_api.py ⏳
- E2E测试: 待定

---

## 性能考虑

- [性能点1]: [说明]
- [性能点2]: [说明]

---

## 相关资源

- Plan: `ai/workdocs/active/<task>/plan.md`
- Tasks: `ai/workdocs/active/<task>/tasks.md`
- Contract: `modules/user/doc/CONTRACT.md`
```

---

**tasks.md** (任务清单):

```markdown
# [Task Name] - 任务清单

> **更新频率**: 每完成一个task就勾选  
> **上次更新**: 2025-11-08 15:30

---

## Phase 1: [名称] ✅ COMPLETE

- [x] Task 1.1: [名称]
  - 验收: [标准]
  - 完成时间: 2025-11-08 14:00
  
- [x] Task 1.2: [名称]
  - 验收: [标准]
  - 完成时间: 2025-11-08 15:00

---

## Phase 2: [名称] 🟡 IN PROGRESS

- [x] Task 2.1: 创建数据模型基础结构
  - 验收: schemas.py存在，基础字段定义完成
  - 完成时间: 2025-11-08 15:30
  
- [ ] Task 2.2: 添加Pydantic验证器 (IN PROGRESS)
  - 验收: 所有字段有验证器，测试通过
  - 预计完成: 2025-11-08 16:30
  - **当前状态**: 已完成email验证器，待添加password验证器
  
- [ ] Task 2.3: 编写单元测试
  - 验收: test_schemas.py覆盖率≥80%
  - 预计完成: 2025-11-08 17:00

---

## Phase 3: [名称] ⏳ NOT STARTED

- [ ] Task 3.1: [名称]
- [ ] Task 3.2: [名称]
- [ ] Task 3.3: [名称]

---

## 总体进度

- Phase 1: ✅ 100% (2/2)
- Phase 2: 🟡 33% (1/3)
- Phase 3: ⏳ 0% (0/3)
- **总进度**: 42% (3/7)

---

## Quick Status（快速状态）

**下一个要做的任务**:
- Task 2.2: 添加Pydantic验证器
  - 文件: modules/user/models/schemas.py
  - 位置: class UserCreate
  - 任务: 添加password_validator

**最近完成**:
- Task 2.1: 创建数据模型基础结构 (2025-11-08 15:30)

---

## 阻塞任务

- [ ] ⚠️ [被阻塞的任务]
  - 阻塞原因: [说明]
  - 解决方案: [计划]
  - 负责人: [谁来解决]

---

## 里程碑

- [ ] M1: Phase 1-2完成 (预计: 2025-11-08 17:00)
- [ ] M2: Phase 3完成 (预计: 2025-11-09 12:00)
- [ ] M3: 全部测试通过 (预计: 2025-11-09 15:00)
- [ ] M4: 文档更新完成 (预计: 2025-11-09 17:00)
```

---

### 3.3 集成到agent.md

```yaml
# agent.md 扩展

context_routes:
  workdocs:
    enabled: true
    location: /ai/workdocs/
    
    # 自动检测active任务
    auto_detect: true
    auto_load_on_start: true
    
    # 任务恢复
    resume_priority:
      - context.md  # 最高优先级
      - tasks.md
      - plan.md
```

---

### 3.4 Makefile命令

```makefile
# 创建work doc
workdoc_create:
	@if [ -z "$(TASK)" ]; then \
		echo "❌ 错误：需要指定 TASK 参数"; \
		exit 1; \
	fi
	@bash scripts/workdoc_create.sh $(TASK)

# 更新work doc
workdoc_update:
	@python scripts/workdoc_update.py

# 归档work doc
workdoc_archive:
	@if [ -z "$(TASK)" ]; then \
		echo "❌ 错误：需要指定 TASK 参数"; \
		exit 1; \
	fi
	@bash scripts/workdoc_archive.sh $(TASK)

# 列出active任务
workdoc_list:
	@ls -1 ai/workdocs/active/
```

---

### 3.5 自动化脚本

`scripts/workdoc_create.sh`:

```bash
#!/bin/bash
# 创建新的work doc

TASK=$1
TASK_DIR="ai/workdocs/active/$TASK"

if [ -d "$TASK_DIR" ]; then
    echo "❌ 任务已存在: $TASK"
    exit 1
fi

# 创建目录
mkdir -p "$TASK_DIR"

# 复制模板
cp doc/templates/workdoc-plan.md "$TASK_DIR/plan.md"
cp doc/templates/workdoc-context.md "$TASK_DIR/context.md"
cp doc/templates/workdoc-tasks.md "$TASK_DIR/tasks.md"

# 替换占位符
sed -i "" "s/\[Task Name\]/$TASK/g" "$TASK_DIR"/*.md
sed -i "" "s/\[YYYY-MM-DD\]/$(date +%Y-%m-%d)/g" "$TASK_DIR"/*.md

echo "✅ Work doc创建成功: $TASK_DIR"
echo ""
echo "下一步:"
echo "  1. 编辑 plan.md 定义实施计划"
echo "  2. AI会自动维护 context.md 和 tasks.md"
```

---

### 3.6 预期效果

| 指标 | 优化前 | 优化后 | 改进 |
|------|--------|--------|------|
| **上下文恢复时间** | 15-30分钟 | 2-5分钟 | ⬇️ 83% |
| **任务进度可见性** | 需要查代码 | 实时tasks.md | ⬆️ 100% |
| **关键决策记录** | 分散在commit | 集中在context.md | ⬆️ 100% |
| **错误重复率** | 20% | <5% | ⬇️ 75% |

---

## 互补方案4: Guardrail机制

### 4.1 现状分析

#### AI-TEMPLATE现有机制

**质量门禁**:
```bash
make dev_check  # 15个检查
```

**问题**:
- ❌ 事后检查（代码已写完）
- ❌ 依赖开发者记得运行
- ❌ 无法阻止错误操作

#### claude-showcase Guardrail

```json
{
  "frontend-dev-guidelines": {
    "enforcement": "block",  // ← 阻止模式
    "blockMessage": "⚠️ BLOCKED - 必须先使用技能..."
  }
}
```

**优势**:
- ✅ 事前阻止（写代码前）
- ✅ 自动触发，无需记忆
- ✅ 强制执行规范

---

### 4.2 集成方案

#### Guardrail规则（已在agent-triggers.yaml中）

```yaml
triggers:
  # Guardrail 1: 契约变更（Block）
  contract-changes:
    enforcement: block
    block_config:
      message: |
        ⚠️ BLOCKED - 契约变更检查
        
        📋 必须执行:
        1. 运行: make contract_compat_check
        2. 确认无破坏性变更
        3. 更新VERSION和CHANGELOG.md
      
      skip_conditions:
        make_commands_passed:
          - "make contract_compat_check"

  # Guardrail 2: 数据库变更（Block）
  database-schema-changes:
    enforcement: block
    file_triggers:
      path_patterns:
        - "db/engines/**/*.yaml"
        - "migrations/**/*.sql"
    block_config:
      message: |
        ⚠️ BLOCKED - 数据库变更检查
        
        📋 必须执行:
        1. 确认已创建Table YAML
        2. 确认已编写up和down迁移脚本
        3. 运行: make db_lint
        4. 在dev环境测试
      
      skip_conditions:
        make_commands_passed:
          - "make db_lint"

  # Guardrail 3: 根agent.md变更（Warn）
  root-agent-changes:
    enforcement: warn
    file_triggers:
      path_patterns:
        - "agent.md"  # 仅根agent.md
    block_config:
      message: |
        ⚠️ WARNING - 根agent.md变更
        
        这是核心配置文件！建议:
        1. 运行: make agent_lint
        2. 运行: make doc_route_check
        3. 通知团队成员
        
        继续? (yes/no)

  # Guardrail 4: 生产配置变更（Block）
  prod-config-changes:
    enforcement: block
    file_triggers:
      path_patterns:
        - "config/prod.yaml"
        - "config/staging.yaml"
    block_config:
      message: |
        ⚠️ BLOCKED - 生产配置变更
        
        📋 必须执行:
        1. 运行: make runtime_config_check
        2. Code Review审批
        3. 在staging环境测试
        4. 准备回滚方案
      
      skip_conditions:
        env_override: "ALLOW_PROD_CONFIG_CHANGE"
```

---

#### 实现增强

`scripts/agent_trigger.py` 增强（支持make命令检查）:

```python
def check_make_command_passed(self, command: str) -> bool:
    """检查make命令是否通过"""
    import subprocess
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            timeout=30
        )
        return result.returncode == 0
    except:
        return False

def check_enforcement(self, matched_rules: List[Dict[str, Any]], 
                     file_path: Optional[str] = None) -> Dict[str, Any]:
    """检查enforcement模式（增强版）"""
    for match in matched_rules:
        rule = match["rule"]
        enforcement = rule.get("enforcement", "suggest")
        
        if enforcement == "block":
            block_config = rule.get("block_config", {})
            skip_conditions = block_config.get("skip_conditions", {})
            
            # 检查make命令
            make_commands = skip_conditions.get("make_commands_passed", [])
            for cmd in make_commands:
                if not self.check_make_command_passed(cmd):
                    return {
                        "action": "block",
                        "message": block_config.get("message", ""),
                        "rule_id": match["rule_id"],
                        "failed_command": cmd
                    }
            
            # 如果所有命令都通过，允许继续
            return {"action": "allow"}
        
        # ... warn模式处理 ...
    
    return {"action": "suggest"}
```

---

### 4.3 Git Hooks集成（可选）

创建 `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook: 运行guardrail检查

echo "🔍 运行Guardrail检查..."

# 获取staged文件
STAGED_FILES=$(git diff --cached --name-only)

for FILE in $STAGED_FILES; do
    # 运行触发器检查
    python scripts/agent_trigger.py "$FILE" "" 2>&1
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Guardrail检查失败: $FILE"
        echo "请解决上述问题后再提交"
        exit 1
    fi
done

echo "✅ Guardrail检查通过"
```

---

### 4.4 预期效果

| 场景 | 优化前 | 优化后 | 改进 |
|------|--------|--------|------|
| **契约破坏性变更** | 可能直接提交 | Block阻止 | 避免100% |
| **数据库变更未测试** | 可能直接上线 | 强制测试 | 避免100% |
| **生产配置误改** | 可能影响线上 | 需要审批 | 风险⬇️ 90% |
| **文档规范遵守** | 70%遵守 | 95%遵守 | ⬆️ 36% |

---

## 总结：整合后的架构

### 增强架构图

```
AI-TEMPLATE v2.0 (整合claude-showcase优势)

┌─────────────────────────────────────────────────────────────┐
│                      入口层                                   │
│  - agent.md (扩展triggers字段)                               │
│  - README.md (人类入口)                                       │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    智能触发层 (新增)                          │
│  - agent-triggers.yaml (触发规则)                            │
│  - scripts/agent_trigger.py (触发器引擎)                     │
│  功能:                                                        │
│    ✅ 自动匹配文件路径和prompt                               │
│    ✅ 按优先级加载文档                                        │
│    ✅ Block/Warn/Suggest模式                                 │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    文档层 (改造)                              │
│  原有:                                                        │
│   - doc/policies/ (核心策略)                                 │
│   - doc/modules/ (模块文档)                                  │
│   - doc/process/ (流程规范)                                  │
│                                                               │
│  改造:                                                        │
│   - doc/*/resources/ (渐进式披露)                            │
│   - 主文件<300行                                             │
│   - Resource文件<200行                                       │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    上下文层 (扩展)                            │
│  原有:                                                        │
│   - ai/LEDGER.md (任务清册)                                  │
│   - ai/sessions/ (会话历史)                                  │
│   - .aicontext/ (索引)                                       │
│                                                               │
│  新增:                                                        │
│   - ai/workdocs/active/ (Dev docs)                          │
│     ├── plan.md (战略计划)                                   │
│     ├── context.md (关键上下文+错误记录)                     │
│     └── tasks.md (任务清单)                                  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    质量门禁层 (增强)                          │
│  原有:                                                        │
│   - make dev_check (15个检查)                               │
│   - 事后检查                                                  │
│                                                               │
│  新增:                                                        │
│   - Guardrail机制 (事前阻止)                                │
│   - Git hooks (pre-commit)                                  │
│   - 自动触发检查                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 主要增强点总结

| # | 增强点 | 机制 | 预期收益 |
|---|--------|------|----------|
| 1 | **自动触发** | agent-triggers.yaml | 文档加载准确率⬆️ 36% |
| 2 | **渐进式披露** | 主文件+resources | Token成本⬇️ 25% |
| 3 | **Dev docs** | workdocs/plan/context/tasks | 上下文恢复时间⬇️ 83% |
| 4 | **Guardrail** | Block/Warn模式 | 错误避免率⬆️ 90% |

---

### 实施路线图

#### Phase 1: 基础设施（1-2天）
- [ ] 创建agent-triggers.yaml
- [ ] 实现scripts/agent_trigger.py
- [ ] 添加Makefile命令
- [ ] 测试基本触发功能

#### Phase 2: 渐进式披露（3-4天）
- [ ] 拆分MODULE_INIT_GUIDE.md
- [ ] 拆分DB_CHANGE_GUIDE.md
- [ ] 拆分safety.md
- [ ] 更新触发器规则

#### Phase 3: Dev Docs（2-3天）
- [ ] 创建workdoc模板
- [ ] 实现workdoc_create.sh
- [ ] 实现workdoc_update.py
- [ ] 集成到agent.md

#### Phase 4: Guardrail（1-2天）
- [ ] 定义Guardrail规则
- [ ] 实现Block/Warn机制
- [ ] 添加Git hooks（可选）
- [ ] 测试阻止场景

#### Phase 5: 验证与优化（2-3天）
- [ ] 端到端测试
- [ ] 性能优化
- [ ] 文档更新
- [ ] 团队培训

**总计**: 9-14天

---

### 预期综合效果

| 维度 | 优化前 | 优化后 | 改进 |
|------|--------|--------|------|
| **AI工作效率** | 基准 | +30% | ⬆️ 30% |
| **Token成本** | 基准 | -25% | ⬇️ 25% |
| **错误率** | 基准 | -60% | ⬇️ 60% |
| **上下文恢复** | 15-30分钟 | 2-5分钟 | ⬇️ 83% |
| **文档精度** | 70% | 95% | ⬆️ 36% |
| **开发体验** | 良好 | 优秀 | ⬆️ 显著 |

---

## 风险评估与缓解

### 风险1: 触发器误触发

**风险**: 规则配置不当导致频繁触发或漏触发

**缓解**:
- 从高优先级场景开始
- 设置测试期（suggest模式）
- 收集反馈后调整
- 提供disable开关

---

### 风险2: 渐进式披露增加维护成本

**风险**: 文档拆分后，维护多个文件更复杂

**缓解**:
- 主文件作为"目录"
- Resources聚焦单一主题
- 自动化检查文档同步
- 提供合并视图工具

---

### 风险3: Dev docs维护负担

**风险**: 开发者忘记更新context.md

**缓解**:
- 设置自动提醒
- 在Guardrail中检查
- 提供快速更新命令
- SESSION PROGRESS自动生成

---

### 风险4: Guardrail过于严格

**风险**: Block模式影响开发效率

**缓解**:
- 仅在高风险场景使用Block
- 提供skip_conditions
- 支持紧急override
- 定期review规则合理性

---

## 附录

### A. 完整文件清单

**新增文件**:
```
doc/orchestration/agent-triggers.yaml (核心配置)
scripts/agent_trigger.py (触发器引擎)
scripts/workdoc_create.sh (创建work doc)
scripts/workdoc_update.py (更新work doc)
scripts/workdoc_archive.sh (归档work doc)

doc/modules/resources/ (8个resource文件)
doc/process/resources/ (5个resource文件)
doc/policies/security_details.md (安全详情)
doc/policies/quality_standards.md (质量标准)

doc/templates/workdoc-plan.md (模板)
doc/templates/workdoc-context.md (模板)
doc/templates/workdoc-tasks.md (模板)

ai/workdocs/active/ (目录)
ai/workdocs/archive/ (目录)
```

**修改文件**:
```
agent.md (扩展triggers字段)
Makefile (新增命令)
doc/modules/MODULE_INIT_GUIDE.md (拆分)
doc/process/DB_CHANGE_GUIDE.md (拆分)
doc/policies/safety.md (精简)
```

---

### B. 兼容性说明

**向后兼容**:
- ✅ 现有文档路径不变
- ✅ 原有命令继续工作
- ✅ 渐进式启用新功能
- ✅ 可选功能开关

**迁移策略**:
1. 新功能默认disabled
2. 通过配置逐步启用
3. 提供迁移指南
4. 保留旧文档直到稳定

---

### C. 成功指标

**技术指标**:
- [ ] 触发器准确率≥95%
- [ ] Token成本降低≥25%
- [ ] 上下文恢复时间<5分钟
- [ ] Guardrail误报率<5%

**体验指标**:
- [ ] 开发者满意度≥90%
- [ ] AI响应速度提升≥30%
- [ ] 文档查找时间减少≥60%
- [ ] 错误重复率降低≥75%

**业务指标**:
- [ ] 开发效率提升≥20%
- [ ] Bug率降低≥40%
- [ ] 代码质量提升（测试覆盖率≥85%）
- [ ] 文档完整度≥95%

---

**文档版本**: v1.0  
**创建时间**: 2025-11-08  
**下一步**: 开始Phase 1实施

