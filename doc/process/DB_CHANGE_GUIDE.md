# 数据库变更指南

> **用途**: 指导开发过程中的数据库变更流程（创建表、修改表结构、删除表）
> **适用场景**: 模块初始化、功能开发、需求变更、重构
> **执行方式**: AI辅助或手动执行
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## 概述

### 何时需要数据库变更

数据库变更可能发生在以下场景：

**模块初始化阶段**:
- 新模块需要持久化数据
- 明确知道需要哪些表

**功能开发阶段**:
- 实现新功能时发现需要新表
- 现有表字段不足，需要扩展
- 性能优化需要增加索引

**需求变更阶段**:
- 业务需求调整导致数据结构变化
- 增加新的业务实体

**重构阶段**:
- 表结构优化
- 数据模型调整

### 与模块初始化的区别

| 维度 | 模块初始化时 | 开发过程中 |
|------|------------|-----------|
| 触发点 | MODULE_INIT_GUIDE.md Phase 6 | plan.md标记或开发时发现 |
| 确定性 | 可能不确定，可跳过 | 明确需要 |
| 流程 | 可选步骤 | 本文档流程 |

---

## 触发机制

### 方式1: 通过plan.md标记（推荐）

在开始任何迭代前，在`modules/<entity>/plan.md`中评估：

```markdown
## 数据库影响评估（必填）

### 本次迭代是否涉及数据库变更？
- [ ] 是，涉及数据库变更
  - 变更类型：
    - [ ] 新建表
    - [ ] 修改表结构（增加字段）
    - [ ] 修改表结构（删除字段）
    - [ ] 修改表结构（修改字段类型）
    - [ ] 增加索引
    - [ ] 删除索引
    - [ ] 增加外键约束
    - [ ] 删除表（慎重！）
  - 影响表：<表名列表>
  - 影响范围：<描述影响的模块和功能>
  - 数据迁移需求：<是否需要迁移现有数据>
  
- [ ] 否，不涉及数据库变更

### 测试数据影响（如涉及数据库变更必填）
- [ ] 需要更新Fixtures
  - 影响场景：
    - [ ] minimal（最小集）
    - [ ] standard（标准集）
    - [ ] full（完整集）
- [ ] 需要更新Mock规则
  - 影响表：<表名列表>
- [ ] 不需要更新测试数据（请说明原因）
```

**标记后**：继续阅读本文档，执行数据库变更流程

---

### 方式2: 开发过程中发现

在编码过程中发现需要数据库变更：

1. **暂停编码**
2. **回到plan.md**，补充数据库影响评估
3. **继续本文档流程**
4. **完成后再继续编码**

---

### 方式3: Code Review时识别

Review代码时发现有数据库操作但没有对应的表结构定义：

1. **标记问题**："缺少数据库表定义和迁移脚本"
2. **要求补充**：按本文档流程补充
3. **重新Review**

---

## 数据库变更流程

### Step 1: 明确变更需求（5-10分钟）

#### AI引导对话

```
AI: 我注意到plan.md中标记了数据库变更需求。
    让我了解一下具体情况：

1. 变更类型是什么？
   A. 新建表
   B. 修改现有表结构
   C. 删除表（慎重！）
   D. 仅调整索引/约束
   
   用户: [选择]

[如选A - 新建表]

AI: 好的，需要新建表。让我了解表的基本信息：

2. 表名是什么？（小写+下划线，如：user_profiles）
   用户: [回答]
   
3. 表的用途是什么？（一句话描述）
   用户: [回答]
   
4. 这个表属于哪个模块？
   用户: [回答模块名]
   
5. 表的主要字段有哪些？（列举关键字段，格式：字段名:类型）
   例如：id:uuid, username:varchar(100), created_at:timestamp
   用户: [列举]
   
6. 是否需要外键关联？
   - 是（请说明关联哪个表的哪个字段）
   - 否
   用户: [回答]
   
7. 是否需要特殊索引？
   - 唯一索引（字段名）
   - 普通索引（字段名）
   - 组合索引（字段名列表）
   - 不需要特殊索引
   用户: [回答]

[如选B - 修改表结构]

AI: 需要修改现有表结构。具体是什么操作？

2. 要修改哪个表？
   用户: [表名]
   
3. 修改操作是？
   A. 增加字段
   B. 删除字段（慎重！需考虑数据迁移）
   C. 修改字段类型（慎重！需考虑数据兼容性）
   D. 修改字段约束（如：增加NOT NULL）
   
   用户: [选择]
   
4. 具体改动是？（详细描述）
   用户: [描述]
   
5. 是否会影响现有数据？
   - 是（需要数据迁移脚本）
   - 否
   用户: [回答]
   
6. 是否向后兼容？
   - 是（旧代码仍可正常运行）
   - 否（需要同步修改代码）
   用户: [回答]

[如选C - 删除表]

AI: ⚠️ 警告：删除表是高风险操作！

2. 确认要删除哪个表？
   用户: [表名]
   
3. 删除原因？
   用户: [说明]
   
4. 表中是否有数据？
   - 是（需要数据备份和迁移方案）
   - 否（测试环境的临时表）
   用户: [回答]
   
5. 是否有其他表依赖这个表（外键）？
   - 是（需要先解除依赖）
   - 否
   用户: [回答]
   
6. 确认删除？（请输入表名再次确认）
   用户: [输入表名确认]
```

---

### Step 2: 创建表结构YAML（10-20分钟）

#### 2.1 文件位置

```bash
db/engines/postgres/schemas/tables/<table_name>.yaml
```

#### 2.2 表YAML模板

**参考示例**: `db/engines/postgres/schemas/tables/runs.yaml`

```yaml
table: <table_name>
description: "<表的用途说明>"

ownership:
  module: modules.<entity>
  maintainer: "<维护者>"

columns:
  # 主键（通常是UUID或自增ID）
  - name: id
    type: uuid
    primary_key: true
    not_null: true
    default: "gen_random_uuid()"
    description: "主键"
  
  # 业务字段示例
  - name: <field_name>
    type: varchar(255)
    not_null: true
    unique: false
    default: null
    description: "<字段说明>"
  
  # 外键示例
  - name: user_id
    type: uuid
    not_null: true
    description: "关联用户表"
  
  # 时间戳字段（推荐）
  - name: created_at
    type: timestamp
    not_null: true
    default: "now()"
    description: "创建时间"
  
  - name: updated_at
    type: timestamp
    not_null: true
    default: "now()"
    description: "更新时间"

indexes:
  # 单字段索引
  - columns: [<field_name>]
    unique: false
    name: "idx_<table>_<field>"
  
  # 组合索引
  - columns: [field1, field2]
    unique: false
    name: "idx_<table>_field1_field2"
  
  # 唯一索引
  - columns: [email]
    unique: true
    name: "idx_<table>_email_unique"
  
  # 时间索引（推荐）
  - columns: [created_at]
    unique: false

foreign_keys:
  - column: user_id
    references:
      table: users
      column: id
    on_delete: CASCADE    # 或 SET NULL, RESTRICT, NO ACTION
    on_update: CASCADE

constraints:
  # CHECK约束示例
  - type: check
    name: "chk_<table>_<field>_positive"
    expression: "<field> > 0"

metadata:
  partition_key: null     # 如需分区，指定分区键
  estimated_rows: 10000   # 预估行数
  retention_days: null    # 如需自动清理，指定保留天数
  comment: "<表级注释>"
```

#### 2.3 字段类型参考

| 类型 | 说明 | 示例 |
|------|------|------|
| uuid | UUID | `id uuid` |
| varchar(n) | 可变长字符串 | `username varchar(100)` |
| text | 长文本 | `description text` |
| integer / int | 整数 | `age integer` |
| bigint | 大整数 | `count bigint` |
| decimal(p,s) | 精确小数 | `price decimal(10,2)` |
| boolean / bool | 布尔值 | `is_active boolean` |
| timestamp | 时间戳 | `created_at timestamp` |
| timestamptz | 带时区时间戳 | `updated_at timestamptz` |
| date | 日期 | `birth_date date` |
| json / jsonb | JSON | `metadata jsonb` |
| array | 数组 | `tags text[]` |

#### 2.4 AI辅助生成

```
AI: 根据您提供的信息，我生成了表YAML定义：

[显示生成的YAML内容]

请确认：
1. 字段类型是否正确？
2. 约束（NOT NULL、UNIQUE）是否合理？
3. 索引是否完整？
4. 外键关系是否正确？

如需修改，请告诉我。

用户: [确认/修改]

AI: 好的，我已创建文件：
    db/engines/postgres/schemas/tables/<table>.yaml
```

---

### Step 3: 创建迁移脚本（15-30分钟）

#### 3.1 生成迁移脚本编号

```bash
# 查看当前最大编号
LAST_NUM=$(ls db/engines/postgres/migrations/*_up.sql 2>/dev/null | sort | tail -1 | grep -oP '^\d+' || echo "000")

# 生成新编号
NEXT_NUM=$(printf "%03d" $((10#$LAST_NUM + 1)))

echo "新迁移脚本编号：$NEXT_NUM"
```

#### 3.2 创建UP迁移（应用变更）

**文件名格式**: `<num>_<module>_<action>_<table>_up.sql`

**示例**:
- `002_user_create_user_profiles_up.sql`
- `003_user_add_email_to_users_up.sql`
- `004_order_modify_status_in_orders_up.sql`

**UP脚本模板（新建表）**:

```sql
-- 迁移: 创建<table_name>表
-- 模块: <module_name>
-- 作者: <maintainer>
-- 日期: <YYYY-MM-DD>
-- 说明: <简要说明变更原因>

BEGIN;

-- 创建表
CREATE TABLE IF NOT EXISTS <table_name> (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    <field_name> VARCHAR(255) NOT NULL,
    user_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_<table>_<field> 
    ON <table_name>(<field_name>);

CREATE INDEX IF NOT EXISTS idx_<table>_created 
    ON <table_name>(created_at);

-- 创建外键
ALTER TABLE <table_name>
    ADD CONSTRAINT fk_<table>_user
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE;

-- 添加注释
COMMENT ON TABLE <table_name> IS '<表说明>';
COMMENT ON COLUMN <table_name>.<field_name> IS '<字段说明>';

COMMIT;
```

**UP脚本模板（修改表）**:

```sql
-- 迁移: 为<table_name>表增加<field_name>字段
-- 模块: <module_name>
-- 作者: <maintainer>
-- 日期: <YYYY-MM-DD>
-- 说明: <变更原因>

BEGIN;

-- 增加字段
ALTER TABLE <table_name>
    ADD COLUMN IF NOT EXISTS <field_name> VARCHAR(255);

-- 如需默认值（对现有数据）
UPDATE <table_name>
    SET <field_name> = '<default_value>'
    WHERE <field_name> IS NULL;

-- 如需添加约束
ALTER TABLE <table_name>
    ALTER COLUMN <field_name> SET NOT NULL;

-- 创建索引（如需要）
CREATE INDEX IF NOT EXISTS idx_<table>_<field>
    ON <table_name>(<field_name>);

-- 添加注释
COMMENT ON COLUMN <table_name>.<field_name> IS '<字段说明>';

COMMIT;
```

#### 3.3 创建DOWN迁移（回滚变更）

**文件名格式**: `<num>_<module>_<action>_<table>_down.sql`

**DOWN脚本模板（新建表的回滚）**:

```sql
-- 回滚: 删除<table_name>表
-- 模块: <module_name>
-- 作者: <maintainer>
-- 日期: <YYYY-MM-DD>

BEGIN;

-- 删除表（CASCADE会自动删除相关的外键、索引、触发器等）
DROP TABLE IF EXISTS <table_name> CASCADE;

COMMIT;
```

**DOWN脚本模板（修改表的回滚）**:

```sql
-- 回滚: 删除<table_name>表的<field_name>字段
-- 模块: <module_name>
-- 作者: <maintainer>
-- 日期: <YYYY-MM-DD>

BEGIN;

-- 删除字段
ALTER TABLE <table_name>
    DROP COLUMN IF EXISTS <field_name>;

-- 注意：索引会随字段自动删除

COMMIT;
```

#### 3.4 AI辅助生成迁移脚本

```
AI: 我已生成迁移脚本：

UP脚本（应用变更）：
db/engines/postgres/migrations/<num>_<module>_<action>_<table>_up.sql

[显示UP脚本内容]

DOWN脚本（回滚变更）：
db/engines/postgres/migrations/<num>_<module>_<action>_<table>_down.sql

[显示DOWN脚本内容]

请确认：
1. SQL语法是否正确？
2. 事务使用是否合理（BEGIN/COMMIT）？
3. 回滚逻辑是否完整？
4. 是否需要数据迁移脚本？

用户: [确认/修改/需要数据迁移]

[如需要数据迁移]

AI: 好的，我会在UP脚本中添加数据迁移逻辑：

[显示带数据迁移的UP脚本]
```

---

### Step 4: 更新测试数据（20-40分钟）

#### 4.1 评估影响

```
AI: 数据库变更会影响测试数据。让我确认：

1. 是否需要更新Fixtures？
   - 是（新表或修改表结构）
   - 否（只是索引调整）
   
   用户: [回答]

[如需要更新Fixtures]

2. 影响哪些测试场景？
   - [ ] minimal（最小集，<10条）- 单元测试
   - [ ] standard（标准集，10-100条）- 集成测试
   - [ ] full（完整集，>1000条）- 性能测试
   
   用户: [选择]

3. 是否需要更新Mock规则？
   - 是（新表需要Mock生成规则）
   - 否
   
   用户: [回答]
```

#### 4.2 更新Fixtures

**位置**: `modules/<entity>/fixtures/<scenario>.sql`

**示例：为新表添加minimal fixtures**:

```sql
-- Fixtures: minimal (最小集)
-- 新增表: <table_name>
-- 用途: 单元测试

-- 插入<table_name>测试数据
INSERT INTO <table_name> (id, <field_name>, user_id, created_at, updated_at) VALUES
('test-<table>-001', 'Test Value 1', 'test-user-001', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
('test-<table>-002', 'Test Value 2', 'test-user-002', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
('test-<table>-003', 'Test Value 3', 'test-user-001', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days');
```

**修改表结构时的Fixtures更新**:

```sql
-- 更新：为现有记录设置新字段的值
UPDATE <table_name> SET <new_field> = '<default_value>' WHERE id IN (
    'test-<table>-001',
    'test-<table>-002',
    'test-<table>-003'
);

-- 或者：重新插入完整数据
TRUNCATE TABLE <table_name> CASCADE;
INSERT INTO <table_name> (...) VALUES (...);
```

#### 4.3 更新TEST_DATA.md

**位置**: `modules/<entity>/doc/TEST_DATA.md`

**需要更新的章节**:

1. **Fixtures定义**:
   - 添加新表的Fixtures概览
   - 更新记录数统计
   - 补充数据特征说明

2. **Mock规则定义**（如需要）:
   - 添加新表的字段生成规则
   - 定义数据分布
   - 配置生成数量

**示例更新**:

```markdown
## Fixtures定义

### 1. Fixtures概览

| 场景名称 | 文件路径 | 数据表 | 记录数 | 用途 |
|---------|---------|--------|--------|------|
| minimal | fixtures/minimal.sql | users | 3 | 单元测试 |
|         |                      | <new_table> | 3 | 单元测试 | ← 新增
| standard | fixtures/standard.sql | users | 20 | 集成测试 |
|          |                       | <new_table> | 15 | 集成测试 | ← 新增

### 场景1: minimal（最小集）

**数据表**: `<new_table>`（新增）
\`\`\`yaml
records:
  - id: "test-<table>-001"
    <field_name>: "Test Value 1"
    user_id: "test-user-001"
    created_at: "2024-01-01T10:00:00Z"
\`\`\`
```

---

### Step 5: 校验（5-10分钟）

#### 5.1 运行数据库校验

```bash
make db_lint
```

**检查项**:
- ✅ 迁移脚本成对（up + down）
- ✅ 表YAML格式正确
- ✅ 文件命名规范
- ✅ SQL语法正确

#### 5.2 验证迁移脚本

```bash
# 本地测试环境
# 1. 应用迁移
psql -U postgres -d test_db -f db/engines/postgres/migrations/<num>_*_up.sql

# 2. 验证表是否创建成功
psql -U postgres -d test_db -c "\d <table_name>"

# 3. 测试回滚
psql -U postgres -d test_db -f db/engines/postgres/migrations/<num>_*_down.sql

# 4. 验证表是否删除
psql -U postgres -d test_db -c "\d <table_name>"
```

#### 5.3 验证测试数据

```bash
# 加载Fixtures
make load_fixture MODULE=<entity> FIXTURE=minimal

# 验证数据是否正确
psql -U postgres -d test_db -c "SELECT COUNT(*) FROM <table_name>;"

# 运行相关测试
pytest tests/<entity>/
```

#### 5.4 AI引导确认

```
AI: 校验完成！结果如下：

✅ db_lint: 通过
  - 迁移脚本成对: ✅
  - 表YAML格式: ✅
  - 文件命名: ✅

✅ 迁移脚本验证: 通过
  - UP脚本执行成功
  - 表创建成功
  - DOWN脚本执行成功
  - 回滚成功

✅ 测试数据验证: 通过
  - Fixtures加载成功
  - 记录数正确: <count>条

所有检查通过！数据库变更已准备就绪。

下一步：
1. 提交变更（git add + commit）
2. 更新plan.md（标记数据库变更已完成）
3. 继续功能开发

用户: [确认]
```

---

## 常见场景示例

### 场景1: 新建用户档案表

**需求**: 用户模块需要存储用户的扩展信息（头像、签名、地区等）

**表YAML**: `db/engines/postgres/schemas/tables/user_profiles.yaml`

```yaml
table: user_profiles
description: "用户扩展档案信息"
ownership:
  module: modules.user
  maintainer: "张三"

columns:
  - name: id
    type: uuid
    primary_key: true
    not_null: true
    default: "gen_random_uuid()"
  - name: user_id
    type: uuid
    not_null: true
    unique: true
    description: "关联用户ID"
  - name: avatar_url
    type: varchar(500)
    description: "头像URL"
  - name: signature
    type: varchar(200)
    description: "个性签名"
  - name: region
    type: varchar(100)
    description: "地区"
  - name: created_at
    type: timestamp
    not_null: true
    default: "now()"
  - name: updated_at
    type: timestamp
    not_null: true
    default: "now()"

indexes:
  - columns: [user_id]
    unique: true
  - columns: [region]
  - columns: [created_at]

foreign_keys:
  - column: user_id
    references:
      table: users
      column: id
    on_delete: CASCADE
```

**迁移脚本**: `002_user_create_user_profiles_up.sql` / `_down.sql`

**Fixtures**: 在`modules/user/fixtures/minimal.sql`中添加3条测试数据

---

### 场景2: 为orders表增加status字段

**需求**: 订单需要增加状态跟踪

**迁移脚本**: `003_order_add_status_to_orders_up.sql`

```sql
BEGIN;

-- 增加status字段
ALTER TABLE orders
    ADD COLUMN IF NOT EXISTS status VARCHAR(50) NOT NULL DEFAULT 'pending';

-- 为现有数据设置状态（根据实际业务逻辑）
UPDATE orders
    SET status = CASE
        WHEN completed_at IS NOT NULL THEN 'completed'
        WHEN cancelled_at IS NOT NULL THEN 'cancelled'
        ELSE 'pending'
    END;

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_orders_status
    ON orders(status);

-- 添加CHECK约束
ALTER TABLE orders
    ADD CONSTRAINT chk_orders_status
    CHECK (status IN ('pending', 'processing', 'completed', 'cancelled'));

COMMENT ON COLUMN orders.status IS '订单状态：pending/processing/completed/cancelled';

COMMIT;
```

**DOWN脚本**: `003_order_add_status_to_orders_down.sql`

```sql
BEGIN;

ALTER TABLE orders
    DROP CONSTRAINT IF EXISTS chk_orders_status;

ALTER TABLE orders
    DROP COLUMN IF EXISTS status;

COMMIT;
```

**更新Fixtures**: 修改所有orders记录，添加status字段

---

### 场景3: 优化查询 - 增加组合索引

**需求**: 经常按user_id + created_at查询，需要组合索引

**迁移脚本**: `004_user_add_composite_index_up.sql`

```sql
BEGIN;

-- 创建组合索引
CREATE INDEX IF NOT EXISTS idx_user_activities_user_created
    ON user_activities(user_id, created_at DESC);

-- 分析表统计信息（可选，帮助查询优化器）
ANALYZE user_activities;

COMMIT;
```

**DOWN脚本**:

```sql
BEGIN;

DROP INDEX IF EXISTS idx_user_activities_user_created;

COMMIT;
```

**说明**: 仅索引变更，不影响测试数据

---

## 常见问题

### Q1: 什么时候应该创建新表，什么时候应该增加字段？

**A**: 
- **新表**: 新的业务实体，与现有表是1对多或多对多关系
- **增加字段**: 现有实体的属性扩展，与现有表是1对1关系

**示例**:
- 用户的订单 → 新表`orders`（1个用户多个订单）
- 用户的头像URL → 增加字段`users.avatar_url`（1个用户1个头像）

### Q2: 迁移脚本中的BEGIN/COMMIT是必需的吗？

**A**: 
- **强烈推荐**，事务可以保证：
  - 要么全部成功，要么全部回滚
  - 避免部分执行导致数据不一致
- **例外情况**: 某些DDL操作（如CREATE INDEX CONCURRENTLY）不能在事务中

### Q3: 删除字段会丢失数据吗？

**A**: 
- **是的**，删除字段会永久丢失该列的所有数据
- **操作前必须**:
  1. 确认该字段确实不再需要
  2. 备份重要数据
  3. 考虑用"标记废弃"代替直接删除

### Q4: 如何处理大表的迁移（百万级数据）？

**A**:
- **分批处理**: `UPDATE ... WHERE id IN (SELECT id FROM ... LIMIT 10000)`
- **避免锁表**: 考虑使用`pg_repack`或在线迁移工具
- **创建索引**: 使用`CREATE INDEX CONCURRENTLY`避免锁表
- **时间窗口**: 在低峰期执行

### Q5: DOWN脚本一定要能完全回滚吗？

**A**:
- **理想情况**: 完全回滚到变更前状态
- **实际情况**: 某些操作不可逆（如删除字段、删除表）
- **建议**: 
  - 不可逆操作在DOWN脚本中注释说明
  - 提供数据恢复的备用方案
  - 在生产环境应用前充分测试

### Q6: 如何确保不同环境（dev/test/prod）的一致性？

**A**:
- **使用迁移脚本**: 所有环境都通过相同的迁移脚本
- **版本控制**: 迁移脚本纳入Git管理
- **顺序执行**: 按编号顺序执行，不跳过
- **记录追踪**: 使用`schema_migrations`表记录已执行的迁移

---

## 相关文档

- **表YAML示例**: /db/engines/postgres/schemas/tables/runs.yaml
- **数据库规范**: /db/engines/postgres/docs/DB_SPEC.yaml
- **模块初始化**: /doc/modules/MODULE_INIT_GUIDE.md（Phase 6）
- **测试数据规格**: /doc/modules/TEMPLATES/TEST_DATA.md.template
- **测试数据示例**: /doc/modules/example/doc/TEST_DATA.md

---

## 版本历史

- 2025-11-07: v1.0 创建数据库变更指南（Phase 6.5）

---

**维护责任**: 项目维护者
**更新频率**: 流程变更时更新

