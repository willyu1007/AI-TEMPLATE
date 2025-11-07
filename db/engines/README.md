# 数据库引擎

> **用途**: 数据库层的组织和规范
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## 目录结构

```
db/engines/
├── postgres/                # PostgreSQL
│   ├── migrations/          # 迁移脚本
│   ├── schemas/             # 表结构定义
│   │   └── tables/          # 表定义YAML
│   ├── extensions/          # 扩展配置
│   └── docs/                # 数据库文档
└── redis/                   # Redis
    ├── schemas/             # Key结构定义
    │   └── keys/            # Key定义YAML
    └── docs/                # Redis文档
```

---

## 数据库规范

### 操作原则
1. **禁止直接操作生产数据库**
2. **所有变更必须通过迁移脚本**
3. **迁移脚本必须成对（up + down）**
4. **重大变更需回滚测试**

### 迁移流程（半自动化）

#### 1. 定义表结构
```yaml
# db/engines/postgres/schemas/tables/users.yaml
table: users
columns:
  - name: id
    type: uuid
    primary_key: true
  - name: username
    type: varchar(100)
    unique: true
  ...
```

#### 2. 生成迁移脚本
```bash
make db_gen_ddl TABLE=users
# 自动生成: db/engines/postgres/migrations/XXX_create_users_up.sql
# 自动生成: db/engines/postgres/migrations/XXX_create_users_down.sql
```

#### 3. 人工审核
- 检查生成的SQL是否正确
- 确认对现有表的影响
- 评估性能影响

#### 4. 执行迁移
```bash
make db_migrate  # 需要用户确认
```

#### 5. 回滚测试
```bash
make rollback_check PREV_REF=v1.0.0
```

---

## PostgreSQL规范

### 命名规范
- 表名：小写+下划线，复数形式（users, orders）
- 列名：小写+下划线（user_id, created_at）
- 索引：`idx_<table>_<column>`
- 外键：`fk_<table>_<ref_table>`

### 必需字段
所有表必须包含：
- `id` (uuid, primary key)
- `created_at` (timestamp)
- `updated_at` (timestamp)

### 索引策略
- 外键必须有索引
- 常用查询字段添加索引
- 复合索引注意字段顺序

---

## Redis规范

### Key命名规范
```
<namespace>:<entity>:<id>:<attribute>

示例:
cache:user:12345:profile
session:web:abc123:data
queue:task:pending
```

### TTL策略
- 缓存数据：设置合理TTL（如3600s）
- 会话数据：设置过期时间（如86400s）
- 队列数据：根据业务设置

### 数据类型选择
- String: 简单值、JSON
- Hash: 对象属性
- List: 队列、时间线
- Set: 去重集合
- ZSet: 排行榜、延时队列

---

## 迁移脚本规范

### 成对原则
每个变更必须有up和down脚本：
```
001_create_users_up.sql
001_create_users_down.sql
```

### 幂等性
脚本必须可重复执行：
```sql
-- 创建表
CREATE TABLE IF NOT EXISTS users (...);

-- 添加列
DO $$ BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name='users' AND column_name='email'
  ) THEN
    ALTER TABLE users ADD COLUMN email VARCHAR(255);
  END IF;
END $$;
```

### 回滚脚本
down脚本必须能完全回滚up的变更：
```sql
-- down脚本
DROP TABLE IF EXISTS users;
```

---

## 工具命令

### 迁移相关
```bash
# 生成DDL（半自动）
make db_gen_ddl TABLE=<table-name>

# 执行迁移（需确认）
make db_migrate

# 回滚迁移
make db_rollback VERSION=<version>

# 检查迁移
make migrate_check
```

### 数据库工具
```bash
# 连接数据库
make db_shell

# 备份数据库
make db_backup

# 恢复数据库
make db_restore FILE=<backup-file>
```

---

## 相关文档

- **数据库规范**: docs/db/DB_SPEC.yaml
- **Schema指南**: docs/db/SCHEMA_GUIDE.md
- **安全规范**: doc/policies/safety.md

---

**维护**: 数据库规范变更时更新

