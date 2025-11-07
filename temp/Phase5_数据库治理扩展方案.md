# Phase 5 数据库治理扩展方案

> **文档目的**: 记录Phase 5完成后的数据库治理扩展讨论和方案
> **创建日期**: 2025-11-07
> **状态**: 方案确认，待Phase 6+实施

---

## 0. 背景

Phase 5已完成数据库基础治理：
- ✅ 统一的db/engines/目录结构
- ✅ 迁移脚本管理
- ✅ 表结构YAML描述（runs.yaml示例）
- ✅ 数据库校验工具（db_lint.py）

在此基础上，讨论了4个关键工程问题，形成扩展方案。

---

## 1. 数据库CRUD操作流程

### 1.1 操作层级分类

```yaml
L1_Schema变更（高风险）:
  触发条件: 需要修改表结构
  操作流程:
    1. AI生成迁移脚本草案（up/down）
    2. 人工审核SQL
    3. 更新对应的tables/*.yaml
    4. 运行make db_lint校验
    5. 在dev环境测试
    6. 人工确认后执行
  工具支持:
    - db_plan.py: 生成预览
    - db_apply.py: 执行迁移
  
L2_数据迁移（中风险）:
  触发条件: 需要数据转换/清理
  操作流程:
    1. AI生成数据迁移脚本
    2. 在副本数据库测试
    3. 人工审核结果
    4. 生成回滚脚本
    5. 执行+验证
  保护机制: 必须先备份
  
L3_查询操作（低风险）:
  触发条件: 数据分析/调试
  操作流程:
    1. AI生成SELECT查询
    2. 自动添加LIMIT保护
    3. 只读权限执行
    4. 结果返回给AI
  限制: 默认只读，无写权限
```

### 1.2 环境配置方案

```yaml
# 目录结构（建议Phase 6+实施）
db/engines/postgres/config/
├── dev.yaml          # 本地开发环境
├── test.yaml         # 测试环境
├── staging.yaml      # 预发布环境
└── prod.yaml         # 生产环境（严格限制）

# 配置示例
# dev.yaml
meta:
  environment: dev
  ai_access: full_control

connection:
  type: local
  host: localhost
  port: 5432
  
credentials:
  source: env_vars
  prefix: DEV_DB_

ai_permissions:
  schema_changes: prompt_required
  data_writes: prompt_required
  data_reads: auto_allowed
  migrations: manual_only

# prod.yaml（严格限制）
meta:
  environment: prod
  ai_access: read_only_reporting

ai_permissions:
  schema_changes: disabled
  data_writes: disabled
  data_reads: require_approval
  migrations: manual_only

safety:
  require_vpn: true
  require_mfa: true
  audit_all_queries: true
```

### 1.3 环境管理工具

```python
# scripts/db_env.py（建议Phase 6实施）
"""
数据库环境管理工具

用法:
    python scripts/db_env.py --env dev
    python scripts/db_env.py --show
"""

流程:
1. 读取db/engines/postgres/config/{env}.yaml
2. 验证权限和凭证
3. 设置环境变量
4. 显示当前配置和AI权限
```

---

## 2. 数据库访问权限配置

### 2.1 多环境支持

```yaml
环境类型:
  local: 本地开发数据库
  docker: Docker容器数据库
  ci: CI测试数据库
  rds: AWS RDS
  cloud_sql: Google Cloud SQL
  azure: Azure Database

识别机制:
  - 明确选择，不推断
  - 用户确认目标环境
  - AI记录当前环境
```

### 2.2 凭证管理

```yaml
凭证来源:
  env_vars: 环境变量（开发环境）
  vault: HashiCorp Vault（推荐）
  aws_secrets: AWS Secrets Manager
  azure_keyvault: Azure Key Vault
  
安全原则:
  - 凭证不写入代码
  - 不同环境使用不同凭证
  - 生产凭证需要MFA
```

---

## 3. 数据库实例识别（registry.yaml）

### 3.1 实例注册表

```yaml
# db/engines/registry.yaml（建议Phase 6+创建）

instances:
  postgres_dev_local:
    engine: postgres
    environment: dev
    location: local
    identifier: "postgres://localhost:5432/app_dev"
    ai_accessible: true
    
  postgres_prod_rds:
    engine: postgres
    environment: prod
    location: aws_rds
    identifier: "postgres://prod.xxxxx.rds.amazonaws.com:5432/app"
    ai_accessible: false  # 禁止AI访问
    
  redis_dev_local:
    engine: redis
    environment: dev
    location: local
    identifier: "redis://localhost:6379"
    ai_accessible: true

identification_rules:
  method: explicit_selection
  safety_checks:
    - 禁止推断
    - 环境标识
    - 颜色标识
    - 二次确认
```

### 3.2 AI操作流程

```python
# AI识别数据库的标准流程
1. 检查是否已设置环境
   - 如未设置，提示用户选择

2. 解析用户意图中的引擎类型
   - postgres | redis | mongo

3. 从registry查找可访问实例
   - 过滤ai_accessible=true

4. 如果只有一个，自动选择；多个则询问

5. 验证操作安全性
   - 检查实例权限
   - 检查操作类型
   - 生产环境特殊保护
```

---

## 4. Mock数据与Fixtures管理

### 4.1 概念定义

```yaml
Fixtures:
  定义: 预定义的固定测试数据文件
  特征:
    - 固定内容
    - 可重复
    - 版本化（提交到git）
    - 场景化
  用途: 单元测试、精确测试
  数据量: 小（10-500条）

Mock数据:
  定义: 动态生成的随机数据
  特征:
    - 动态生成
    - 每次不同
    - 不提交到git
    - 规则化
  用途: 压力测试、性能测试
  数据量: 大（100-10万条）
```

### 4.2 Fixtures管理

```yaml
# 目录结构
db/engines/postgres/fixtures/
├── README.md
├── test/
│   ├── minimal.sql         # 最小测试集
│   └── integration.sql     # 集成测试集
├── dev/
│   └── seed.sql           # 开发种子数据
├── demo/
│   └── showcase.sql       # 演示数据
└── scripts/
    ├── load_fixtures.py
    └── export_fixtures.py

场景分类:
  minimal_test: 最小可测试集（10-50条）
  integration_test: 集成测试集（100-500条）
  dev_seed: 开发环境初始数据
  demo: 演示/展示数据
```

### 4.3 Mock数据生成

```yaml
# 按需生成原则
生成方式:
  声明式: 用YAML描述需求
  动态性: 每次生成不同
  智能性: 理解表关系和约束
  可控性: 控制分布和范围

# Mock规则文件
db/engines/postgres/fixtures/mock/rules/
└── default.yaml

规则内容:
  - 字段生成类型（faker, choice, random, foreign_key）
  - 数据分布（weights, probability）
  - 业务特征（status分布、渠道分布）
  - 关联关系（外键依赖）
```

### 4.4 Mock数据生命周期

```yaml
生命周期策略:
  ephemeral:    # 短暂
    ttl: 0
    auto_cleanup: true
    用途: 测试结束立即删除
    
  temporary:    # 临时
    ttl: 7天
    auto_cleanup: true
    用途: 保留7天后自动清理
    
  persistent:   # 持久
    ttl: null
    auto_cleanup: false
    用途: 需手动删除
    
  fixture:      # 转为fixture
    ttl: null
    export_as_fixture: true
    用途: 永久保留，转为fixture

管理机制:
  - 注册表（_mock_lifecycle表）
  - 自动清理（定期任务）
  - 导出功能（转为fixture）
  - 查询列表（活跃Mock）
```

---

## 5. 模块级测试数据管理（重要）⭐

### 5.1 设计原则

**核心原则**: 保持agent.md轻量化

```yaml
方案: 路由式管理
  agent.md: 只保留路由（5-10行）
  TEST_DATA.md: 详细规格（200-500行）
  rules.yaml: 工具可读规则（自动生成）

优势:
  - agent.md保持轻量
  - 详细内容分离
  - AI按需读取
  - 易于维护和diff
```

### 5.2 agent.md中的定义

```yaml
# modules/<module>/agent.md

# 测试数据路由（轻量化，5-10行）
test_data:
  enabled: true
  spec: "doc/TEST_DATA.md"

context_routes:
  on_demand:
    - topic: test_data
      description: "测试数据需求、Fixtures和Mock规则"
      paths:
        - "doc/TEST_DATA.md"
        - "fixtures/README.md"
```

### 5.3 TEST_DATA.md详细规格

```markdown
# modules/<module>/doc/TEST_DATA.md

# 测试数据规格说明

## 1. 数据实体概览
- 核心实体列表
- 实体关系图

## 2. Fixtures规格
- minimal_test: 最小测试集
- integration_test: 集成测试集
- dev_seed: 开发种子数据

## 3. Mock数据生成规格
- 表级生成范围
- 字段生成规则
- 数据分布特征
- 业务常态说明

## 4. 数据质量要求
- 约束检查
- 验证查询

## 5. 使用指南
- 加载Fixtures命令
- 生成Mock命令
- 清理命令

## 6. 维护指南
- 何时更新
- 更新流程
```

### 5.4 目录结构

```
modules/<module>/
├── agent.md                  # 只有test_data路由（5-10行）
├── doc/
│   ├── TEST_DATA.md         # 详细规格（200-500行）⭐
│   └── ...
└── fixtures/
    ├── README.md            # 索引
    ├── test/
    │   ├── minimal.sql      # 固定测试数据
    │   └── integration.sql
    ├── dev/
    │   └── seed.sql         # 开发种子数据
    └── mock/
        └── rules.yaml       # Mock生成规则（自动生成）
```

### 5.5 模块初始化引导

```yaml
# MODULE_INIT_GUIDE.md 新增步骤

第7步: 定义测试数据需求（可选）

AI引导问题:
  Q1: 需要哪些固定的测试场景？
  Q2: 最小测试集需要几条数据？
  Q3: 是否需要Mock数据生成？
  Q4: 数据字段的分布应该是怎样的？

AI自动创建:
  - agent.md中的test_data路由
  - doc/TEST_DATA.md详细规格
  - fixtures/test/minimal.sql
  - fixtures/dev/seed.sql
  - fixtures/mock/rules.yaml（自动生成）
```

---

## 6. Schema扩展（agent.schema.yaml）

### 6.1 test_data字段定义

```yaml
# schemas/agent.schema.yaml 扩展

test_data:
  type: object
  description: "模块的测试数据（轻量化，详细内容在doc/TEST_DATA.md）"
  properties:
    enabled:
      type: boolean
      description: "是否启用测试数据管理"
      
    spec:
      type: string
      description: "测试数据规格文档路径"
      default: "doc/TEST_DATA.md"
```

---

## 7. 实施计划

### 对执行计划的影响（已更新到执行计划.md）

**Phase 6扩展**（原4个子任务 → 10个子任务）:
- 原有任务（2个）：PROJECT_INIT_GUIDE.md、ai_begin.sh
- **新增任务（4个）**：
  - 子任务3: MODULE_INIT_GUIDE.md添加"第7步：定义测试数据需求"
  - 子任务4: Schema扩展（test_data字段）
  - 子任务5: 创建TEST_DATA.md.template模板
  - 子任务6: example模块添加测试数据示例
- 扩展任务（4个）：agent_lint.py、module_doc_gen.py支持、测试

**Phase 7扩展**（原4个子任务 → 6个子任务）:
- 原有任务（3个）：dev_check集成、CI配置、测试
- **新增任务（3个）**：
  - 子任务3: Fixtures管理工具实施（fixture_loader.py）
  - 子任务4: 环境管理工具实施（db_env.py，可选）
  - Makefile添加load_fixture等命令

**Phase 8扩展**（原5个子任务 → 8个子任务）:
- 原有任务（4个）：文档更新、路径引用、映射表
- **新增任务（2个）**：
  - 子任务5: Mock数据生成器实施（可选）
  - 子任务6: 数据库实例注册表实施（可选）
- 旧文件清理、完整检验

### Phase 6（初始化规范完善）详细任务

#### 基础任务（必须）

1. ✅ **Schema扩展**
   - 在agent.schema.yaml添加test_data字段定义
   - 更新agent_lint.py支持新字段校验

2. ✅ **模块初始化引导**
   - 在MODULE_INIT_GUIDE.md添加"第7步：定义测试数据需求"
   - 包含AI引导对话示例
   - Fixtures和Mock的选择逻辑
   - 数据分布定义方法

3. ✅ **文档模板**
   - 创建doc/modules/TEMPLATES/TEST_DATA.md.template
   - 包含完整的章节结构和示例
   - 说明Fixtures和Mock的使用场景

4. ✅ **example模块示例**
   - 在doc/modules/example/doc/TEST_DATA.md创建示例
   - 创建doc/modules/example/fixtures/目录结构
   - 创建示例fixtures（minimal.sql）
   - 在example的agent.md添加test_data路由

5. ✅ **脚本更新**
   - 更新scripts/agent_lint.py支持test_data字段
   - 更新scripts/module_doc_gen.py支持生成Mock规则

### Phase 7（CI集成与测试数据工具）详细任务

#### Fixtures管理（建议实施）

1. ✅ **Fixtures加载器**
   - 实现scripts/fixture_loader.py（模块感知）
   - 读取模块agent.md的test_data定义
   - 支持场景选择和加载
   - Makefile添加load_fixture命令

2. ✅ **目录结构**
   - 创建db/engines/postgres/fixtures/
   - 创建test/、dev/、demo/子目录
   - 为example模块创建示例fixtures

#### 环境管理（可选实施）

3. ⏳ **环境管理工具**
   - 实现scripts/db_env.py
   - 创建db/engines/postgres/config/
   - 创建dev.yaml、test.yaml配置示例
   - Makefile添加db_env命令

### Phase 8（高级功能）详细任务

#### Mock生成器（可选实施）

1. ⏳ **Mock生成器**
   - 实现scripts/mock_generator.py
   - 从模块agent.md读取test_data路由
   - 读取TEST_DATA.md规格
   - 生成符合规格的随机数据
   - Makefile添加generate_mock命令

2. ⏳ **Mock生命周期管理**
   - 实现scripts/mock_lifecycle.py
   - 支持4种生命周期策略（ephemeral、temporary、persistent、fixture）
   - 自动清理过期数据
   - 导出为fixture功能
   - Makefile添加cleanup_mock命令

3. ⏳ **实例注册表**
   - 创建db/engines/registry.yaml
   - 注册所有数据库实例（dev、test、prod）
   - 实现识别和验证机制

### 未来优化（按需）

1. ⏳ **高级Mock功能**
   - Faker库智能使用
   - 数据关系推断
   - 从生产数据自动脱敏

2. ⏳ **可视化工具**
   - Mock数据预览
   - 数据分布图表
   - ER图生成

3. ⏳ **数据质量工具**
   - 自动验证Mock数据质量
   - 数据分布分析
   - 异常数据检测

---

## 8. 关键设计决策

### 决策1: 轻量化agent.md ✅

**决策**: 测试数据详细规格不放在agent.md中，而是通过路由引用

**理由**:
- 保持agent.md≤500行的目标
- 测试数据规格可以很长（200-500行）
- AI按需读取，不影响性能

**实现**:
```yaml
# agent.md只有路由
test_data:
  enabled: true
  spec: "doc/TEST_DATA.md"
```

### 决策2: 模块级管理 ✅

**决策**: 测试数据管理在模块级，而非全局

**理由**:
- 业务相关性：每个模块有独特的数据特征
- 责任明确：模块维护者最了解数据需求
- 版本同步：规则随模块代码一起演进

**实现**: 每个模块有自己的fixtures/和TEST_DATA.md

### 决策3: 半自动化生成 ✅

**决策**: Mock规则文件由module_doc_gen从TEST_DATA.md自动生成

**理由**:
- 减少重复：避免同时维护TEST_DATA.md和rules.yaml
- 单一数据源：TEST_DATA.md是唯一权威
- 自动同步：保证一致性

**实现**: module_doc_gen.py解析TEST_DATA.md生成rules.yaml

### 决策4: 明确识别原则 ✅

**决策**: AI不推断目标数据库，必须明确选择

**理由**:
- 安全性：避免误操作生产数据库
- 可审计：所有操作有明确记录
- 用户信任：用户清楚知道操作哪个数据库

**实现**: 
- 必须先设置环境（db_env.py --env dev）
- AI显示当前环境
- 写操作需要确认

---

## 9. 对比总结

### 方案演进

| 版本 | agent.md | 详细规格 | 优点 | 缺点 |
|------|----------|----------|------|------|
| V1: 全在agent.md | 很重（+200行） | 在agent.md中 | 集中 | agent.md过重 |
| V2: 路由式（最终）⭐ | 轻量（+10行） | 在TEST_DATA.md | 轻量+完整 | 需多个文件 |

### Fixtures vs Mock对比

| 维度 | Fixtures | Mock数据 |
|------|----------|----------|
| 定义 | 预定义固定数据 | 动态生成随机数据 |
| 可重复性 | ✅ 完全可重复 | ❌ 每次不同 |
| 版本控制 | ✅ 提交到git | ❌ 不提交 |
| 数据量 | 小（10-500） | 大（100-10万） |
| 使用场景 | 单元测试 | 压力测试 |
| 生命周期 | 永久 | 临时 |

---

## 10. 参考文档

### 相关文档
- Phase5_完成报告.md - Phase 5成果
- Phase5_最终总结.md - Phase 5总结
- 执行计划.md - 总体规划

### 讨论记录
- 数据库CRUD操作流程讨论（2025-11-07）
- 数据库访问权限配置讨论（2025-11-07）
- Mock数据与测试数据处理讨论（2025-11-07）
- 数据库操作对象识别讨论（2025-11-07）
- 模块级测试数据管理方案讨论（2025-11-07）

---

**文档状态**: ✅ 方案确认  
**下一步**: 在Phase 6中实施测试数据管理基础（Schema扩展、引导文档、模板）  
**创建时间**: 2025-11-07

