---
audience: human
language: zh
version: complete
purpose: Documentation for GUARDRAIL_GUIDE
---
# Guardrail使用指南

> **用途**: 详细说明Guardrail防护机制  
> **目标受众**: AI Agent和开发者  
> **版本**: 1.0  
> **创建时间**: 2025-11-08

---

## 概述

### 什么是Guardrail

Guardrail（防护栏）是一套自动化的安全防护机制，在AI执行敏感操作前：
- **Block**: 严格阻止，必须满足条件才能继续
- **Warn**: 警告提示，需要用户确认
- **Suggest**: 建议提示，不阻止操作

### 核心价值

**为项目提供**:
- ✅ 自动阻止危险操作（如：修改生产配置、删除数据）
- ✅ 强制执行质量标准（如：运行测试、校验）
- ✅ 减少人为错误（如：忘记更新CHANGELOG）
- ✅ 统一规范执行（所有AI都遵守）

---

## Guardrail级别

### Block - 严格阻止🛑

**场景**: 高风险操作，必须满足条件

**行为**:
1. 检测到操作→立即阻止
2. 显示要求清单
3. 检查skip_conditions
4. 满足条件→允许继续
5. 不满足→操作终止

**示例规则**:
- 安全相关代码修改
- API契约变更
- 生产配置修改
- 数据库迁移脚本

---

### Warn - 警告确认⚠️

**场景**: 需要谨慎的操作，需要确认

**行为**:
1. 检测到操作→显示警告
2. 列出建议操作
3. 询问用户确认
4. 用户yes→继续
5. 用户no→终止

**示例规则**:
- 根agent.md修改
- 模块注册表修改
- 部署操作

---

### Suggest - 建议提示💡

**场景**: 一般操作，仅提示

**行为**:
1. 检测到操作→显示建议
2. 推荐相关文档
3. 不阻止操作

**示例规则**:
- 模块开发
- 测试编写
- 文档更新

---

## Guardrail规则

### 当前覆盖的关键领域

运行统计查看：
```bash
make guardrail_coverage
```

**关键领域覆盖** ✅:
- ✅ 安全相关（security）
- ✅ 契约变更（contract-changes）
- ✅ 生产配置（prod-config-changes）
- ✅ 数据库迁移（database-migrations）
- ✅ 根配置变更（root-agent-changes）

**总体覆盖率**: 100%

---

## Block规则详解

### 规则1: 安全相关（security）

**触发条件**:
- 文件路径：`**/auth/**/*`, `**/security/**/*`
- 内容关键词：password, secret, token, jwt, encrypt
- Prompt关键词：安全、认证、加密、密码

**Block要求**:
```
📋 安全检查清单:
1. 禁止硬编码密钥、密码、token
2. 敏感信息必须通过环境变量或密钥服务
3. 必须先阅读 doc/policies/security_details.md
4. Code Review必须包含安全审查
```

**跳过条件**: 无（严格Block）

**配置**:
```yaml
security:
  enforcement: block
  priority: critical
  block_config:
    require_confirmation: true
    confirmation_prompt: "已确认遵守安全规范? (yes/no)"
```

---

### 规则2: 契约变更（contract-changes）

**触发条件**:
- 文件路径：`modules/*/doc/CONTRACT.md`, `schemas/**/*.yaml`
- Prompt关键词：契约、接口变更、API变更、breaking change

**Block要求**:
```
📋 必须执行:
1. 运行: make contract_compat_check
2. 确认无破坏性变更或已规划兼容方案
3. 更新CHANGELOG.md记录变更
4. 更新版本号（如需要）
```

**跳过条件**:
- `make contract_compat_check`通过
- 或设置环境变量：`SKIP_CONTRACT_CHECK`

**配置**:
```yaml
contract-changes:
  enforcement: block
  priority: critical
  block_config:
    skip_conditions:
      make_commands_passed:
        - "make contract_compat_check"
      or_env_var: "SKIP_CONTRACT_CHECK"
```

---

### 规则3: 生产配置变更（prod-config-changes）

**触发条件**:
- 文件路径：`config/prod.yaml`, `config/staging.yaml`, `.env.production`
- Prompt关键词：生产配置、prod config、production

**Block要求**:
```
📋 必须执行:
1. 运行: make runtime_config_check
2. Code Review（至少2人审批）
3. 在staging环境完整测试
4. 准备回滚方案
5. 通知运维团队
```

**跳过条件**:
- 设置环境变量：`ALLOW_PROD_CONFIG`
- 或用户角色为：admin

**配置**:
```yaml
prod-config-changes:
  enforcement: block
  priority: critical
  block_config:
    skip_conditions:
      env_var: "ALLOW_PROD_CONFIG"
      or_user_role: "admin"
```

---

### 规则4: 数据库迁移脚本（database-migrations）

**触发条件**:
- 文件路径：`db/engines/**/migrations/*_up.sql`, `*_down.sql`
- Prompt关键词：迁移脚本、migration script

**Block要求**:
```
📋 必须执行:
1. 确认up和down脚本成对存在
2. 确认脚本具有幂等性（可重复执行）
3. 运行: make db_lint
4. 在dev环境测试up脚本
5. 在dev环境测试down脚本（回滚）
6. 添加适当的事务控制
```

**跳过条件**:
- `make db_lint`通过
- 且用户确认

**配置**:
```yaml
database-migrations:
  enforcement: block
  priority: critical
  block_config:
    skip_conditions:
      make_commands_passed:
        - "make db_lint"
      and_confirmation: true
```

---

## Warn规则详解

### 规则1: 根agent.md变更（root-agent-changes）

**触发条件**:
- 文件路径：`agent.md`（仅根目录）
- Prompt关键词：修改agent.md、更新agent

**Warn提示**:
```
⚠️ WARNING - 根agent.md变更

这是核心配置文件！建议:
1. 运行: make agent_lint
2. 运行: make doc_route_check
3. 确认所有路由有效
4. 通知团队成员

继续?
```

**配置**:
```yaml
root-agent-changes:
  enforcement: warn
  priority: high
  warn_config:
    require_confirmation: true
```

---

### 规则2: Registry变更（registry-changes）

**触发条件**:
- 文件路径：`doc/orchestration/registry.yaml`
- Prompt关键词：registry、注册表、模块注册

**Warn提示**:
```
⚠️ WARNING - Registry变更

建议:
1. 运行: make registry_check
2. 确认模块路径存在
3. 确认依赖关系无循环

继续?
```

---

### 规则3: 部署操作（deployment）

**触发条件**:
- 文件路径：`.github/workflows/**`, `docker-compose.yml`
- Prompt关键词：部署、deploy、发布、release

**Warn提示** + **Guardrail检查**:
```
建议运行:
- make dev_check (必须通过所有检查)
- make rollback_check (高风险变更需要验证回滚)
```

---

## 跳过条件（Skip Conditions）

### 类型1: Make命令检查

**配置**:
```yaml
skip_conditions:
  make_commands_passed:
    - "make db_lint"
    - "make contract_compat_check"
```

**行为**:
- 自动运行指定的make命令
- 所有命令都通过→跳过Block
- 任一命令失败→继续Block

---

### 类型2: 环境变量

**配置**:
```yaml
skip_conditions:
  env_var: "ALLOW_PROD_CONFIG"
```

**行为**:
- 检查环境变量是否设置
- 已设置→跳过Block
- 未设置→继续Block

**使用场景**: 
- 紧急情况绕过检查
- 特定环境（如CI）

---

### 类型3: 组合条件

**AND条件**:
```yaml
skip_conditions:
  make_commands_passed:
    - "make db_lint"
  and_confirmation: true
```
必须：命令通过 **且** 用户确认

**OR条件**:
```yaml
skip_conditions:
  env_var: "ALLOW_CONFIG"
  or_user_role: "admin"
```
满足：环境变量 **或** 用户角色

---

## 使用方法

### 自动触发

Guardrail会自动触发，无需手动调用：

```bash
# AI编辑文件时，自动检查Guardrail
# 如果触发Block规则，AI会自动停止并显示要求
```

---

### 手动测试

可以手动测试Guardrail触发：

```bash
# 测试文件触发
make agent_trigger FILE=config/prod.yaml

# 测试prompt触发
make agent_trigger_prompt PROMPT="修改生产配置"

# Dry-run模式（不执行Guardrail）
python scripts/agent_trigger.py --file db/migrations/002_up.sql --dry-run
```

---

### 查看统计

```bash
# 摘要统计
make guardrail_stats

# 详细统计
make guardrail_stats_detailed

# 覆盖检查
make guardrail_coverage
```

---

## AI执行规范

### 遇到Block时

✅ **必须做**:
1. 阅读Block message，了解要求
2. 执行所有必需操作（如运行make命令）
3. 如果有skip_conditions，尝试满足条件
4. 如果需要confirmation，向用户确认

❌ **不要做**:
- ❌ 不要试图绕过Guardrail
- ❌ 不要跳过必需的检查
- ❌ 不要假设用户会说yes

---

### 遇到Warn时

✅ **必须做**:
1. 阅读Warn message，了解风险
2. 执行建议的检查（如有）
3. 向用户确认是否继续
4. 根据用户回答决定行动

❌ **不要做**:
- ❌ 不要自动assume用户会继续
- ❌ 不要跳过警告直接操作

---

### 遇到Suggest时

✅ **应该做**:
1. 阅读推荐的文档
2. 按照最佳实践操作

但不强制，可以根据情况判断。

---

## 最佳实践

### 为项目配置Guardrail

**Step 1: 识别关键操作**
- 哪些操作是高风险的？
- 哪些操作容易出错？
- 哪些操作影响范围大？

**Step 2: 选择Enforcement级别**
- 数据安全、生产环境→Block
- 配置变更、架构修改→Warn
- 一般开发操作→Suggest

**Step 3: 定义检查清单**
- Block: 列出必须执行的操作
- 添加skip_conditions（如make命令）
- 设置require_confirmation

**Step 4: 测试Guardrail**
```bash
# 测试各个规则
make agent_trigger FILE=<sensitive-file>

# 检查覆盖率
make guardrail_coverage
```

---

### 绕过Guardrail（紧急情况）

**方式1: 满足skip_conditions**
```bash
# 运行所需的make命令
make db_lint
make contract_compat_check

# 然后可以继续操作
```

**方式2: 设置环境变量**
```bash
# 设置跳过环境变量（谨慎！）
export SKIP_CONTRACT_CHECK=1
export ALLOW_PROD_CONFIG=1

# 执行操作

# 完成后立即清除
unset SKIP_CONTRACT_CHECK
unset ALLOW_PROD_CONFIG
```

**⚠️ 警告**: 仅在紧急情况下绕过Guardrail！

---

## Guardrail配置

### 配置文件

`doc/orchestration/agent-triggers.yaml`

### Block配置示例

```yaml
triggers:
  example-block-rule:
    enforcement: block
    priority: critical
    
    file_triggers:
      path_patterns:
        - "sensitive/**/*"
    
    block_config:
      message: |
        ⚠️ BLOCKED - 敏感操作
        
        📋 必须执行:
        1. 操作1
        2. 操作2
        3. 运行: make check_command
      
      skip_conditions:
        make_commands_passed:
          - "make check_command"
        or_env_var: "ALLOW_SENSITIVE_OP"
      
      require_confirmation: true
      confirmation_prompt: "已确认? (yes/no)"
```

---

### Warn配置示例

```yaml
triggers:
  example-warn-rule:
    enforcement: warn
    priority: high
    
    file_triggers:
      path_patterns:
        - "important/**/*"
    
    warn_config:
      message: |
        ⚠️ WARNING - 重要操作
        
        建议:
        1. 建议1
        2. 建议2
        
        继续?
      
      require_confirmation: true
      confirmation_prompt: "(yes/no)"
```

---

## 常见场景

### 场景1: AI修改生产配置

```
AI检测到: 修改 config/prod.yaml

Guardrail触发: prod-config-changes (Block)

显示:
⚠️ BLOCKED - 生产配置变更

📋 必须执行:
1. 运行: make runtime_config_check
2. Code Review（至少2人审批）
3. 在staging环境完整测试
4. 准备回滚方案
5. 通知运维团队

AI行为:
- 停止修改操作
- 提示用户上述要求
- 等待用户满足条件后再继续
```

---

### 场景2: AI修改API契约

```
AI检测到: 修改 modules/user/doc/CONTRACT.md

Guardrail触发: contract-changes (Block)

显示:
⚠️ BLOCKED - 契约变更检查

📋 必须执行:
1. 运行: make contract_compat_check
2. 确认无破坏性变更

AI行为:
- 停止修改操作
- 尝试运行 make contract_compat_check
- 如果通过→继续操作
- 如果失败→提示用户并终止
```

---

### 场景3: AI修改根agent.md

```
AI检测到: 修改 agent.md

Guardrail触发: root-agent-changes (Warn)

显示:
⚠️ WARNING - 根agent.md变更

这是核心配置文件！建议:
1. 运行: make agent_lint
2. 运行: make doc_route_check
3. 通知团队成员

继续? (yes/no)

AI行为:
- 暂停操作
- 显示警告和建议
- 询问用户确认
- 用户yes→继续，no→终止
```

---

## 统计和监控

### 查看Guardrail统计

```bash
# 摘要统计
make guardrail_stats

# 输出示例：
📊 总体统计:
  总规则数: 13
  文件模式数: 44
  Prompt关键词数: 60

🔐 Enforcement分布:
  🛑 block   :  4 ( 30.8%)
  ⚠️ warn    :  3 ( 23.1%)
  💡 suggest :  6 ( 46.2%)
```

---

### 查看详细统计

```bash
make guardrail_stats_detailed

# 显示每个规则的详细信息
```

---

### 检查覆盖率

```bash
make guardrail_coverage

# 输出示例：
关键领域覆盖:
  ✅ 安全相关
  ✅ 契约变更
  ✅ 生产配置
  ✅ 数据库迁移
  ✅ 根配置变更

总体覆盖率: 100%
✅ 所有关键领域都有Guardrail保护
```

---

## 常见问题

### Q1: Guardrail会影响开发效率吗？
**A**: 不会。Guardrail只针对高风险操作：
- 一般开发操作（编写代码、测试）→不影响
- 敏感操作（修改配置、契约）→阻止或警告
- 大部分情况下，AI会自动满足skip_conditions

### Q2: 如何知道有哪些Guardrail规则？
**A**: 
```bash
# 查看配置文件
cat doc/orchestration/agent-triggers.yaml

# 查看统计
make guardrail_stats_detailed
```

### Q3: 紧急情况下如何快速绕过？
**A**: 设置环境变量（谨慎使用）：
```bash
export SKIP_CONTRACT_CHECK=1
# 执行操作
unset SKIP_CONTRACT_CHECK
```

### Q4: 如何添加新的Guardrail规则？
**A**: 编辑`agent-triggers.yaml`，添加新规则：
1. 定义触发条件（file_triggers/prompt_triggers）
2. 设置enforcement（block/warn/suggest）
3. 配置block_config或warn_config
4. 运行`make guardrail_stats`验证

### Q5: Block和Warn的区别？
**A**:
- **Block**: 严格阻止，必须满足条件（如运行测试）
- **Warn**: 警告提示，用户确认即可继续

选择原则：
- 可能导致数据丢失、安全问题→Block
- 需要谨慎但可控→Warn

### Q6: skip_conditions什么时候用？
**A**: 当操作可以通过自动化检查来验证安全性时。例如：
- 契约变更→运行`make contract_compat_check`
- 数据库迁移→运行`make db_lint`

不要对所有Block都添加skip_conditions，某些操作必须人工审查。

---

## Guardrail覆盖的操作

### 文件操作

| 操作 | Guardrail | 级别 |
|------|-----------|------|
| 修改生产配置 | prod-config-changes | 🛑 Block |
| 修改API契约 | contract-changes | 🛑 Block |
| 修改安全代码 | security | 🛑 Block |
| 创建迁移脚本 | database-migrations | 🛑 Block |
| 修改根agent.md | root-agent-changes | ⚠️ Warn |
| 修改Registry | registry-changes | ⚠️ Warn |
| 部署操作 | deployment | ⚠️ Warn |
| 模块开发 | module-development | 💡 Suggest |
| 测试编写 | testing | 💡 Suggest |
| 文档更新 | documentation-writing | 💡 Suggest |

---

## 相关资源

- **配置文件**: `doc/orchestration/agent-triggers.yaml`
- **触发引擎**: `scripts/agent_trigger.py`
- **统计工具**: `scripts/guardrail_stats.py`
- **触发指南**: `doc/orchestration/triggers-guide.md`

---

## 版本历史

- **1.0** (2025-11-08): 创建Guardrail指南（Phase 10.4）

