# 数据库变更 - 测试数据更新

> **所属**: DB_CHANGE_GUIDE.md  
> **用途**: 更新测试数据以匹配数据库变更  
> **目标**: 确保测试数据与表结构同步

---

## 目标

在数据库变更后，更新相关的测试数据和Fixtures

---

## Step 1: 更新TEST_DATA.md

### 文件位置

```
modules/<entity>/doc/TEST_DATA.md
```

### 更新内容

#### 新建表时

添加新章节：

```markdown
## X. <Table>表测试数据

### X.1 数据需求

| 场景 | 数据量 | 说明 |
|------|--------|------|
| 单元测试 | 3-5条 | 基本CRUD |
| 集成测试 | 20-30条 | 完整流程 |
| 性能测试 | 1000+条 | 压力测试 |

### X.2 Fixture文件

- minimal.sql: 最小测试集（3条）
- standard.sql: 标准测试集（20条）
- performance.sql: 性能测试集（1000条）

### X.3 Mock规则

\`\`\`yaml
mock_rules:
  - table: <table>
    count: 20
    generators:
      - field: name
        type: faker
        provider: name
      - field: email
        type: faker
        provider: email
\`\`\`
```

#### 修改表结构时

更新相应章节，说明字段变更：

```markdown
### 变更记录

- 2025-XX-XX: 新增 `new_field` 字段（允许NULL）
- 2025-XX-XX: `old_field` 类型从 VARCHAR(255) 改为 TEXT
```

---

## Step 2: 更新Fixtures

### 文件位置

```
modules/<entity>/fixtures/
```

### 新建表时

创建3个Fixture文件：

**minimal.sql**:
```sql
-- Minimal fixture for <table>
-- Generated: $(date +%Y-%m-%d)

DELETE FROM <table> WHERE id < 1000;

INSERT INTO <table> (id, field1, field2, created_at) VALUES
  ('00000000-0000-0000-0000-000000000001', 'Test 1', 'Value 1', CURRENT_TIMESTAMP),
  ('00000000-0000-0000-0000-000000000002', 'Test 2', 'Value 2', CURRENT_TIMESTAMP),
  ('00000000-0000-0000-0000-000000000003', 'Test 3', 'Value 3', CURRENT_TIMESTAMP);
```

**standard.sql**:
```sql
-- Standard fixture for <table>
-- Generated: $(date +%Y-%m-%d)

DELETE FROM <table> WHERE id < 10000;

INSERT INTO <table> (id, field1, field2, created_at) VALUES
  ('00000000-0000-0000-0000-000000000101', 'Standard 1', 'Value 1', CURRENT_TIMESTAMP),
  -- ... 共20条
  ('00000000-0000-0000-0000-000000000120', 'Standard 20', 'Value 20', CURRENT_TIMESTAMP);
```

### 修改表结构时

#### 添加字段（允许NULL）

Fixtures无需修改（新字段为NULL）

#### 添加字段（NOT NULL或有默认值）

更新所有Fixture文件，添加新字段：

```sql
-- 更新Fixture，添加新字段
DELETE FROM <table> WHERE id < 1000;

INSERT INTO <table> (id, field1, field2, new_field, created_at) VALUES
  ('...', 'Test 1', 'Value 1', 'New Value 1', CURRENT_TIMESTAMP),
  ('...', 'Test 2', 'Value 2', 'New Value 2', CURRENT_TIMESTAMP),
  ('...', 'Test 3', 'Value 3', 'New Value 3', CURRENT_TIMESTAMP);
```

#### 删除字段

从Fixture中移除该字段。

---

## Step 3: 更新Mock规则（如使用Mock）

### 新建表时

在TEST_DATA.md中添加Mock规则：

```yaml
mock_rules:
  - table: <table>
    count: 20
    generators:
      - field: <field1>
        type: faker
        provider: name
      - field: <field2>
        type: faker
        provider: email
      - field: <field3>
        type: integer
        min: 1
        max: 100
```

### 修改字段时

更新对应字段的Mock规则。

---

## Step 4: 验证

### 加载Fixture测试

```bash
# 加载最小集
make load_fixture MODULE=<entity> FIXTURE=minimal DRY_RUN=1

# 检查输出是否有错误
```

### 生成Mock测试（如适用）

```bash
# 生成Mock数据
make generate_mock MODULE=<entity> TABLE=<table> COUNT=10 DRY_RUN=1

# 检查输出是否有错误
```

---

## 常见问题

### Q: 是否需要立即更新所有Fixtures？
**A**: 
- 如果添加字段允许NULL：可以延后更新
- 如果添加字段NOT NULL：必须立即更新
- 如果删除字段：必须立即更新

### Q: Fixture文件太多了怎么办？
**A**: 
- 只更新minimal.sql（必需）
- standard.sql和performance.sql可以延后更新

### Q: Mock规则什么时候用？
**A**: 
- 需要大量随机测试数据时
- 性能测试时
- 不需要固定数据的场景

### Q: 如何确保测试数据不冲突？
**A**: 
- 使用固定的UUID范围（如：00000000-0000-0000-0000-0000000000XX）
- 使用固定的ID范围（如：1-999为minimal，100-9999为standard）
- 在Fixture开头清理旧数据

---

## 完成

测试数据更新完成后：

1. 运行 `make validate` 确保一切正常
2. 提交所有变更（表YAML、迁移脚本、TEST_DATA.md、Fixtures）
3. 在测试环境验证

