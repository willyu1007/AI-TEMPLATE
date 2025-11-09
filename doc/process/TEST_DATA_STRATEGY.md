# 测试数据策略指南

> **用途**: 指导开发者选择合适的测试数据管理策略  
> **维护者**: AI-TEMPLATE团队  
> **创建时间**: 2025-11-09  
> **适用范围**: 所有模块的测试数据规划

---

## 概述

测试数据管理是软件质量保证的关键环节。本指南帮助团队在Fixtures和Mock数据之间做出正确选择，并提供最佳实践。

---

## Fixtures vs Mock 对比

### 核心区别

| 维度 | Fixtures（固定装置） | Mock数据（模拟数据） |
|------|-------------------|-------------------|
| **定义方式** | SQL文件手工编写 | YAML规则自动生成 |
| **数据量** | 小规模（≤50条） | 大规模（100-10000条） |
| **精确性** | 完全精确，可预测 | 随机生成，半随机 |
| **维护成本** | 高（逐条维护） | 低（维护规则） |
| **可重复性** | 100%可重复 | 可通过seed控制 |
| **创建时间** | 慢（手工编写） | 快（自动生成） |
| **适用测试** | 单元、集成测试 | 性能、压力测试 |
| **数据质量** | 高（人工设计） | 中（规则生成） |
| **边界覆盖** | 好（可精确设计） | 一般（需规则支持） |

---

## 决策树

### 何时使用Fixtures？

```
是否需要精确的数据？
├─ 是
│  └─ 数据量 ≤ 50条？
│      ├─ 是 → ✅ 使用Fixtures
│      └─ 否 → ⚠️  考虑拆分测试场景或使用混合策略
└─ 否
   └─ 继续评估Mock数据
```

**适用场景**:

1. **单元测试**
   - 测试特定边界条件
   - 验证精确的业务逻辑
   - 需要可预测的测试结果
   
   ```yaml
   # example: 测试用户状态转换
   - id: "user-001"
     status: "active"      # 精确控制状态
     balance: 100.00       # 精确金额
   ```

2. **集成测试**
   - API响应验证
   - 数据流转测试
   - 跨模块交互测试
   
   ```yaml
   # example: 测试订单创建流程
   - user_id: "user-001"   # 引用已知用户
     product_id: "prod-001" # 引用已知商品
     expected_total: 299.99 # 已知结果
   ```

3. **回归测试**
   - 复现已知bug
   - 验证修复效果
   
   ```yaml
   # example: Bug #123 - 特殊字符导致解析失败
   - description: "Test <script>alert('xss')</script>"
     expected: "escaped"
   ```

4. **演示数据**
   - Demo环境
   - 产品展示
   - 培训材料
   
   ```yaml
   # example: 精心设计的示例数据
   - name: "示例公司"
     industry: "科技"
     description: "这是一个完整的示例..."
   ```

---

### 何时使用Mock数据？

```
是否需要大量数据（>50条）？
├─ 是
│  └─ 数据精确性要求？
│      ├─ 低（随机即可） → ✅ 使用Mock
│      ├─ 中（需符合规则） → ✅ 使用Mock + 详细规则
│      └─ 高（需精确控制） → ⚠️  使用Fixtures或混合策略
└─ 否
   └─ 使用Fixtures
```

**适用场景**:

1. **性能测试**
   - 需要大量数据验证系统性能
   - 测试数据库查询效率
   - 验证分页和索引
   
   ```yaml
   mock_rules:
     users:
       count: 10000        # 10K用户测试查询性能
       seed: 42
   ```

2. **压力测试**
   - 模拟高并发场景
   - 测试系统极限
   
   ```yaml
   mock_rules:
     orders:
       count: 100000       # 100K订单压测
       distribution: weighted_recent  # 最近订单更多
   ```

3. **分布测试**
   - 验证系统对不同数据分布的处理
   - 测试统计和聚合功能
   
   ```yaml
   mock_rules:
     products:
       fields:
         price:
           distribution: exponential  # 符合真实分布
           lambda: 0.01
   ```

4. **随机性测试**
   - 验证系统对随机输入的鲁棒性
   - Fuzz testing
   
   ```yaml
   mock_rules:
     inputs:
       count: 1000
       fields:
         content:
           type: string
           faker: text      # 随机文本
           max_length: 500
   ```

5. **时间序列测试**
   - 测试趋势分析
   - 验证时间范围查询
   
   ```yaml
   mock_rules:
     metrics:
       count: 8640        # 60天 * 24小时 * 6次/小时
       fields:
         timestamp:
           type: timestamp
           start: "-60d"
           interval: "10m"  # 每10分钟一条
   ```

---

## 数据量级决策

### 分级标准

| 级别 | 记录数 | 建议策略 | 生成时间 | 数据库大小 |
|------|--------|---------|---------|-----------|
| **微型** | 1-10 | Fixtures | < 1分钟 | < 10KB |
| **小型** | 11-50 | Fixtures | < 5分钟 | < 100KB |
| **中型** | 51-500 | Mock | < 10分钟 | < 1MB |
| **大型** | 501-5000 | Mock | < 30分钟 | < 10MB |
| **超大** | 5001+ | Mock（分批） | 按需 | > 10MB |

### 决策矩阵

```
                精确性需求
                ↓
        低          中          高
    ┌─────────┬─────────┬─────────┐
少  │ Fixtures│ Fixtures│ Fixtures│
量  │         │         │         │
级  └─────────┴─────────┴─────────┘
    ┌─────────┬─────────┬─────────┐
中  │  Mock   │  Mock   │ Fixtures│
量  │         │ + Rules │  或混合 │
级  └─────────┴─────────┴─────────┘
    ┌─────────┬─────────┬─────────┐
大  │  Mock   │  Mock   │  不推荐 │
量  │         │ + Rules │  拆分   │
级  └─────────┴─────────┴─────────┘
        ↑
    数据量需求
```

---

## 混合策略

### 何时使用混合策略？

在以下场景下，Fixtures和Mock数据可以组合使用：

#### 场景1: 基础数据 + 批量数据

```yaml
# 1. Fixtures: 精确的基础数据
# fixtures/base.sql
INSERT INTO users (id, name, role) VALUES
  ('admin-001', 'Admin User', 'admin'),
  ('test-001', 'Test User', 'user');

# 2. Mock: 批量普通用户
mock_rules:
  users:
    count: 1000
    fields:
      role:
        type: enum
        values: [user]
        weights: [1.0]    # 100%普通用户
```

**优势**:
- 关键数据精确可控（admin用户）
- 大量普通数据快速生成

---

#### 场景2: 主数据 + 关联数据

```yaml
# 1. Fixtures: 精确的商品数据
# fixtures/products.sql
INSERT INTO products (id, name, price) VALUES
  ('prod-001', 'iPhone 15', 999.99),
  ('prod-002', 'MacBook Pro', 2499.99);

# 2. Mock: 大量订单数据（关联到精确商品）
mock_rules:
  orders:
    count: 5000
    fields:
      product_id:
        type: foreign_key
        table: products
        field: id
        strategy: weighted
        conditions:
          - filter: {id: 'prod-001'}
            weight: 0.7    # 70%订单是iPhone
          - filter: {id: 'prod-002'}
            weight: 0.3    # 30%订单是MacBook
```

**优势**:
- 商品信息精确（价格、名称）
- 订单数据大量且真实

---

#### 场景3: 分层测试数据

```
┌─────────────────────────────────────┐
│ Layer 1: 基础 Fixtures (10条)      │ ← 精确、可预测
│  - 关键账户                         │
│  - 系统配置                         │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ Layer 2: 中等 Mock (100条)         │ ← 半随机、规则化
│  - 普通用户                         │
│  - 常规订单                         │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ Layer 3: 大量 Mock (10000条)       │ ← 随机、批量
│  - 历史数据                         │
│  - 性能测试数据                     │
└─────────────────────────────────────┘
```

---

## 场景适用性

### 1. 单元测试

**推荐**: Fixtures（100%）

**原因**:
- 需要精确控制输入和预期输出
- 数据量小（通常<10条）
- 需要高度可重复性

**示例**:
```sql
-- fixtures/unit_test.sql
INSERT INTO orders (id, user_id, status, total) VALUES
  ('order-001', 'user-001', 'pending', 100.00),   -- 测试pending状态
  ('order-002', 'user-001', 'paid', 200.00),      -- 测试paid状态
  ('order-003', 'user-001', 'cancelled', 50.00);  -- 测试cancelled状态
```

---

### 2. 集成测试

**推荐**: Fixtures（80%） + Mock（20%）

**原因**:
- 主要测试数据需要精确（Fixtures）
- 辅助数据可以随机（Mock）

**示例**:
```yaml
# Fixtures: 关键用户和商品
fixtures/integration.sql: 5个用户, 10个商品

# Mock: 大量订单测试分页
mock_rules:
  orders:
    count: 200
    fields:
      user_id:
        type: foreign_key
        table: users
        field: id
```

---

### 3. API测试

**推荐**: Fixtures（90%） + Mock（10%）

**原因**:
- API响应需要精确验证
- 极少需要大量数据

**示例**:
```yaml
# Fixtures: 每个API端点的测试数据
GET /users/:id → user-001 (已知数据)
POST /orders   → user-001, prod-001 (已知关联)
GET /orders?page=2 → Mock生成200条订单测试分页
```

---

### 4. 性能测试

**推荐**: Mock（95%） + Fixtures（5%）

**原因**:
- 需要大量数据
- 精确性要求低

**示例**:
```yaml
# Fixtures: 少量测试账户
fixtures/perf_base.sql: 5个账户

# Mock: 大量数据
mock_rules:
  users:
    count: 100000
  orders:
    count: 500000
  products:
    count: 10000
```

---

### 5. 压力测试

**推荐**: Mock（100%）

**原因**:
- 需要极大量数据
- 不关心数据精确性
- 快速生成和清理

**示例**:
```yaml
mock_rules:
  concurrent_requests:
    count: 10000
    lifecycle: ephemeral  # 测试完立即删除
```

---

### 6. Demo/演示环境

**推荐**: Fixtures（100%）

**原因**:
- 需要精心设计的示例数据
- 数据需要"看起来真实"
- 需要可重复展示

**示例**:
```sql
-- fixtures/demo.sql
-- 精心设计的公司、用户、订单数据
INSERT INTO companies (id, name, industry) VALUES
  ('comp-001', '创新科技有限公司', '互联网'),
  ('comp-002', '蓝海贸易集团', '电商');
```

---

## 最佳实践

### 1. 命名约定

```
Fixtures文件命名:
✅ fixtures/minimal.sql        # 最小集
✅ fixtures/standard.sql       # 标准集
✅ fixtures/edge_cases.sql     # 边界情况
✅ fixtures/demo.sql           # 演示数据

❌ fixtures/data.sql           # 太模糊
❌ fixtures/test.sql           # 不说明用途
```

---

### 2. 文档化测试数据

在TEST_DATA.md中清晰记录：

```yaml
## Fixtures定义

### minimal场景
- 用途: 单元测试
- 数据量: 3条
- 特征: 覆盖success/error/running三种状态

## Mock规则

### 性能测试
- 数据量: 10000条
- 分布: 85%活跃用户
- 生命周期: ephemeral
```

---

### 3. 生命周期管理

```yaml
# 单元测试：立即清理
lifecycle: ephemeral

# 集成测试：24小时后清理
lifecycle: temporary

# 性能测试：手动清理（可保留分析）
lifecycle: persistent
```

---

### 4. 数据隔离

```yaml
# ✅ 好：每个测试套件独立数据
fixtures/unit_tests/user_service/...
fixtures/integration_tests/order_flow/...

# ❌ 不好：所有测试共享数据
fixtures/all_tests.sql  # 可能产生干扰
```

---

### 5. 版本控制

```bash
# ✅ Fixtures纳入Git
git add doc/modules/*/fixtures/*.sql

# ✅ Mock规则纳入Git
git add doc/modules/*/doc/TEST_DATA.md

# ❌ Mock生成的数据不要提交
.gitignore:
  **/mock_generated_*.sql
```

---

## 迁移策略

### 从Fixtures迁移到Mock

**何时迁移**:
- Fixtures文件超过50条记录
- 维护成本过高
- 需要更多数据变化

**迁移步骤**:

1. **分析现有Fixtures**
   ```bash
   # 统计每个场景的记录数
   wc -l fixtures/*.sql
   ```

2. **提取关键Fixtures**
   ```sql
   -- 保留：关键的、精确的数据（≤10条）
   minimal.sql: 3条核心数据
   ```

3. **编写Mock规则**
   ```yaml
   # 将大量数据转为Mock规则
   mock_rules:
     users:
       count: 100  # 原Fixtures有100条
       fields: ...
   ```

4. **验证等效性**
   ```bash
   # 确保测试仍然通过
   make test
   ```

---

### 从Mock迁移到Fixtures

**何时迁移**:
- 发现需要精确控制数据
- Mock生成的数据不符合测试需求
- 需要更高的可重复性

**迁移步骤**:

1. **运行Mock生成数据**
   ```bash
   python scripts/mock_generator.py --module=users --count=10 --dry-run
   ```

2. **导出满意的数据**
   ```bash
   # 将生成的数据保存为SQL
   pg_dump --data-only --table=users > fixtures/users.sql
   ```

3. **手工调整**
   ```sql
   -- 调整为精确的测试数据
   UPDATE users SET email = 'test1@example.com' WHERE id = 'user-001';
   ```

---

## 常见问题

### Q1: 多个测试共享Fixtures会互相干扰吗？

**A**: 是的，可能会。建议：
- 使用事务回滚：每个测试后rollback
- 独立数据库：每个测试套件独立schema
- 唯一标识：使用UUID避免ID冲突

---

### Q2: Mock数据可以用于生产环境吗？

**A**: 不建议。Mock数据：
- 随机性高，不符合真实场景
- 缺少业务逻辑约束
- 仅用于测试和开发

生产初始数据应该：
- 手工创建或从真实系统导入
- 经过严格验证
- 符合业务规则

---

### Q3: 如何确保Fixtures和Mock生成的数据兼容？

**A**: 
1. 在TEST_DATA.md中明确记录数据关系
2. 使用foreign_key确保引用正确
3. 统一使用相同的schema定义

---

### Q4: 测试数据会占用多少存储空间？

**A**: 估算公式：
```
数据库大小 ≈ 记录数 × 平均行大小

示例:
- 用户表（10字段，平均200字节）
- 10000条记录 ≈ 2MB
- 100000条记录 ≈ 20MB
```

建议：
- 定期清理测试数据
- 使用lifecycle自动管理
- 监控数据库大小

---

## 工具支持

### Fixtures工具

```bash
# 加载Fixtures
make load_fixture MODULE=users FIXTURE=minimal

# 清理Fixtures
make cleanup_fixture MODULE=users
```

### Mock工具

```bash
# 生成Mock数据
make generate_mock MODULE=users COUNT=100

# 查看Mock统计
make mock_stats MODULE=users

# 清理Mock数据
make cleanup_mocks MODULE=users
```

---

## 参考资料

- [MOCK_RULES_GUIDE.md](./MOCK_RULES_GUIDE.md) - Mock规则编写指南
- [FIELD_GENERATORS.md](../reference/FIELD_GENERATORS.md) - 字段生成器参考
- [MODULE_INIT_GUIDE.md](../modules/MODULE_INIT_GUIDE.md) - 模块初始化指南（Phase 6-7: 测试数据）

---

## 维护历史

- 2025-11-09: 创建文档（Phase 11）

