# 数据库变更 - 创建新表

> **所属**: DB_CHANGE_GUIDE.md  
> **用途**: 创建新表的详细流程  
> **目标**: 安全地创建新的数据库表

---

## 目标

创建一个新的数据库表，包括表YAML、迁移脚本和测试数据

---

## Step 1: 明确需求

### AI引导对话

```
AI: 需要新建表。让我了解表的基本信息：

1. 表名是什么？（小写+下划线，如：user_profiles）
   用户: [回答]
   
2. 表的用途是什么？（一句话描述）
   用户: [回答]
   
3. 这个表属于哪个模块？
   用户: [回答模块名]
   
4. 表的主要字段有哪些？（列举关键字段）
   格式：字段名:类型
   例如：id:uuid, username:varchar(100), created_at:timestamp
   用户: [列举]
   
5. 是否需要外键关联？
   - 是（请说明关联哪个表的哪个字段）
   - 否
   用户: [回答]
   
6. 是否需要特殊索引？
   - 唯一索引（字段名）
   - 普通索引（字段名）
   - 组合索引（字段名列表）
   - 不需要特殊索引
   用户: [回答]
```

---

## Step 2: 创建表YAML

### 文件位置

```bash
db/engines/postgres/schemas/tables/<table_name>.yaml
```

### 表YAML模板

**参考示例**: `db/engines/postgres/schemas/tables/runs.yaml`

```yaml
table: <table_name>
description: "<表的用途说明>"

ownership:
  module: modules.<entity>
  maintainer: "<维护者>"

columns:
  # 主键（推荐使用UUID）
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
  
  # 外键示例（如有）
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
  
  # 时间索引（推荐）
  - columns: [created_at]
    unique: false

foreign_keys:
  - column: user_id
    references:
      table: users
      column: id
    on_delete: CASCADE
    on_update: CASCADE

constraints:
  # CHECK约束示例
  - type: check
    name: "chk_<table>_<field>_positive"
    expression: "<field> > 0"

metadata:
  partition_key: null
  estimated_rows: 10000
  retention_days: null
  comment: "<表级注释>"
```

### 常见字段类型

| 类型 | PostgreSQL | 用途 | 示例 |
|------|-----------|------|------|
| ID | uuid | 主键 | id |
| 字符串 | varchar(N) | 短文本 | username, email |
| 长文本 | text | 长文本 | description, content |
| 整数 | integer | 数值 | count, age |
| 大整数 | bigint | 大数值 | total_amount |
| 小数 | numeric(p,s) | 精确数值 | price, amount |
| 布尔 | boolean | 是/否 | is_active, is_deleted |
| 时间戳 | timestamp | 时间 | created_at, updated_at |
| 日期 | date | 日期 | birth_date |
| JSON | jsonb | JSON数据 | settings, metadata |

---

## Step 3: 创建迁移脚本

### 生成迁移编号

```bash
# 自动计算下一个编号
NEXT_NUM=$(ls db/engines/postgres/migrations/ | grep -E "^[0-9]+" | sort -n | tail -1 | sed 's/^0*//' | awk '{print $1+1}')
NEXT_NUM=$(printf "%03d" $NEXT_NUM)
```

### 创建up脚本

```bash
cat > db/engines/postgres/migrations/${NEXT_NUM}_create_<table>_up.sql <<'EOF'
-- Migration: Create <table> table
-- Generated: $(date +%Y-%m-%d)

CREATE TABLE <table> (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  <field1> VARCHAR(255) NOT NULL,
  <field2> INTEGER,
  user_id UUID NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  
  CONSTRAINT fk_<table>_user FOREIGN KEY (user_id) 
    REFERENCES users(id) ON DELETE CASCADE,
  
  CONSTRAINT chk_<table>_<field> CHECK (<field> > 0)
);

CREATE INDEX idx_<table>_<field> ON <table>(<field>);
CREATE INDEX idx_<table>_created_at ON <table>(created_at);

COMMENT ON TABLE <table> IS '<表说明>';
COMMENT ON COLUMN <table>.<field> IS '<字段说明>';
EOF
```

### 创建down脚本

```bash
cat > db/engines/postgres/migrations/${NEXT_NUM}_create_<table>_down.sql <<'EOF'
-- Migration Rollback: Drop <table> table
-- Generated: $(date +%Y-%m-%d)

DROP TABLE IF EXISTS <table> CASCADE;
EOF
```

---

## Step 4: 校验

```bash
make db_lint
```

期望输出：
```
✓ 迁移脚本成对性检查: 通过
✓ Table YAML格式检查: 通过
✓ 文件命名规范检查: 通过
```

---

## 常见问题

### Q: 主键用UUID还是自增ID？
**A**: 推荐UUID：
- 优点：分布式友好，不会冲突
- 缺点：占用空间稍大

自增ID适用于：单实例数据库，需要顺序ID

### Q: 是否必须有created_at和updated_at？
**A**: 强烈推荐。这两个字段对审计和调试非常有用。

### Q: 外键约束on_delete应该用什么？
**A**: 
- CASCADE: 删除父记录时，自动删除子记录
- SET NULL: 删除父记录时，设置子记录的外键为NULL
- RESTRICT: 不允许删除有子记录的父记录

### Q: 索引如何选择？
**A**: 
- 查询频繁的字段：创建索引
- WHERE条件常用字段：创建索引
- 外键字段：通常需要索引
- 时间戳字段：推荐创建索引

---

## 下一步

- 如需修改表结构 → [db-alter-table.md](db-alter-table.md)
- 如需创建迁移脚本 → [db-migration-script.md](db-migration-script.md)
- 如需更新测试数据 → [db-test-data.md](db-test-data.md)

