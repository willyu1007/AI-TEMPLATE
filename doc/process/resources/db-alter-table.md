# 数据库变更 - 修改表结构

> **所属**: DB_CHANGE_GUIDE.md  
> **用途**: 修改现有表的详细流程  
> **目标**: 安全地修改表结构

---

## 目标

修改现有表的结构，包括添加/删除字段、修改约束等

---

## ⚠️ 重要提醒

修改表结构是高风险操作，需要考虑：
- 数据兼容性（现有数据是否需要迁移）
- 代码兼容性（是否需要同步修改代码）
- 性能影响（是否会锁表）
- 回滚方案（如何撤销变更）

---

## Step 1: 明确修改需求

### AI引导对话

```
AI: 需要修改现有表结构。具体是什么操作？

1. 要修改哪个表？
   用户: [表名]
   
2. 修改操作是？
   A. 增加字段
   B. 删除字段（慎重！需考虑数据迁移）
   C. 修改字段类型（慎重！需考虑数据兼容性）
   D. 修改字段约束（如：增加NOT NULL）
   
   用户: [选择]
   
3. 具体改动是？（详细描述）
   用户: [描述]
   
4. 是否会影响现有数据？
   - 是（需要数据迁移脚本）
   - 否
   用户: [回答]
   
5. 是否向后兼容？
   - 是（旧代码仍可正常运行）
   - 否（需要同步修改代码）
   用户: [回答]
```

---

## Step 2: 更新表YAML

### 场景A: 添加字段

```yaml
columns:
  # ... 现有字段 ...
  
  # 新增字段
  - name: new_field
    type: varchar(100)
    not_null: false  # 新字段通常允许NULL，避免影响现有数据
    default: null
    description: "新增字段说明"
```

### 场景B: 修改字段类型

```yaml
columns:
  - name: existing_field
    type: text  # 原来是 varchar(255)
    not_null: true
    description: "字段说明（已扩展类型）"
```

### 场景C: 添加/修改约束

```yaml
constraints:
  - type: check
    name: "chk_<table>_new_constraint"
    expression: "new_field IS NOT NULL OR old_field IS NOT NULL"
```

---

## Step 3: 创建迁移脚本

### 场景A: 添加字段

**up脚本**:
```sql
-- Migration: Add new_field to <table>
-- Generated: $(date +%Y-%m-%d)

ALTER TABLE <table> ADD COLUMN new_field VARCHAR(100);

COMMENT ON COLUMN <table>.new_field IS '新增字段说明';
```

**down脚本**:
```sql
-- Migration Rollback: Remove new_field from <table>

ALTER TABLE <table> DROP COLUMN IF EXISTS new_field;
```

### 场景B: 修改字段类型

**up脚本**:
```sql
-- Migration: Change existing_field type in <table>
-- ⚠️ 注意：此操作可能影响现有数据

ALTER TABLE <table> ALTER COLUMN existing_field TYPE TEXT;
```

**down脚本**:
```sql
-- Migration Rollback: Revert existing_field type
-- ⚠️ 注意：回滚可能导致数据截断

ALTER TABLE <table> ALTER COLUMN existing_field TYPE VARCHAR(255);
```

### 场景C: 添加NOT NULL约束

**up脚本**:
```sql
-- Migration: Add NOT NULL constraint to existing_field
-- Step 1: 填充NULL值（如果有）
UPDATE <table> SET existing_field = 'default_value' WHERE existing_field IS NULL;

-- Step 2: 添加约束
ALTER TABLE <table> ALTER COLUMN existing_field SET NOT NULL;
```

**down脚本**:
```sql
-- Migration Rollback: Remove NOT NULL constraint

ALTER TABLE <table> ALTER COLUMN existing_field DROP NOT NULL;
```

### 场景D: 删除字段（慎重！）

**up脚本**:
```sql
-- Migration: Remove old_field from <table>
-- ⚠️ 警告：此操作不可逆，数据将永久丢失

-- Step 1: 备份数据（推荐）
-- CREATE TABLE <table>_backup AS SELECT * FROM <table>;

-- Step 2: 删除字段
ALTER TABLE <table> DROP COLUMN old_field;
```

**down脚本**:
```sql
-- Migration Rollback: Re-add old_field
-- ⚠️ 注意：无法恢复原数据

ALTER TABLE <table> ADD COLUMN old_field VARCHAR(255);
```

---

## Step 4: 数据迁移（如需要）

如果修改影响现有数据，需要在迁移脚本中添加数据转换逻辑：

```sql
-- Migration: Migrate data for field type change
-- Step 1: 添加临时字段
ALTER TABLE <table> ADD COLUMN new_field_temp TEXT;

-- Step 2: 迁移数据
UPDATE <table> SET new_field_temp = old_field::TEXT;

-- Step 3: 删除旧字段
ALTER TABLE <table> DROP COLUMN old_field;

-- Step 4: 重命名新字段
ALTER TABLE <table> RENAME COLUMN new_field_temp TO old_field;
```

---

## Step 5: 校验

```bash
make db_lint
```

---

## 常见问题

### Q: 添加NOT NULL字段如何处理现有数据？
**A**: 两种方式：
1. 字段允许NULL（推荐）
2. 设置默认值，然后在迁移脚本中填充现有行

### Q: 修改字段类型会影响性能吗？
**A**: 会。PostgreSQL可能需要重写整个表。建议：
- 在维护窗口执行
- 使用`SET statement_timeout`设置超时
- 考虑先创建新字段，迁移数据，再删除旧字段

### Q: 如何安全地删除字段？
**A**: 
1. 先在代码中停止使用该字段
2. 等待一段时间（如1周）
3. 确认无影响后再删除

### Q: 回滚脚本需要测试吗？
**A**: 必须！特别是涉及数据迁移的脚本。建议在测试环境先执行回滚。

---

## 下一步

- 如需创建迁移脚本 → [db-migration-script.md](db-migration-script.md)
- 如需更新测试数据 → [db-test-data.md](db-test-data.md)

