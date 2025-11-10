# 数据库变更 - 迁移脚本

> **所属**: DB_CHANGE_GUIDE.md  
> **用途**: 迁移脚本编写规范  
> **目标**: 编写安全、可回滚的迁移脚本

---

## 目标

编写符合规范的迁移脚本（up和down）

---

## 迁移脚本规范

### 文件命名

```
{编号}_{操作描述}_up.sql
{编号}_{操作描述}_down.sql
```

**编号**: 三位数字（001, 002, 003...），按时间顺序递增  
**操作描述**: 小写+下划线，简明扼要

**示例**:
```
001_create_users_table_up.sql
001_create_users_table_down.sql
002_add_email_to_users_up.sql
002_add_email_to_users_down.sql
```

---

## 编写规范

### 1. 头部注释（必需）

```sql
-- Migration: {简要描述}
-- Generated: {日期}
-- Author: {作者}
-- Related: {相关Issue/PR}
```

### 2. 事务控制（推荐）

```sql
BEGIN;

-- 迁移操作
...

COMMIT;
```

**何时不使用事务**:
- 创建/删除数据库
- 创建/删除索引（CONCURRENTLY）
- VACUUM等维护操作

### 3. 幂等性（重要）

迁移脚本应该可以重复执行而不出错：

**好的示例**:
```sql
-- 创建表（如果不存在）
CREATE TABLE IF NOT EXISTS users (...);

-- 添加列（如果不存在）
ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(255);

-- 删除表（如果存在）
DROP TABLE IF EXISTS old_table CASCADE;
```

**不好的示例**:
```sql
-- 会在第二次执行时失败
CREATE TABLE users (...);
ALTER TABLE users ADD COLUMN email VARCHAR(255);
```

### 4. 回滚脚本（必需）

每个up脚本必须有对应的down脚本，能够完全撤销变更：

**up.sql**:
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  name VARCHAR(255)
);
```

**down.sql**:
```sql
DROP TABLE IF EXISTS users CASCADE;
```

---

## 常见模式

### 创建表

```sql
CREATE TABLE IF NOT EXISTS <table> (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ...
);
```

### 添加字段

```sql
ALTER TABLE <table> ADD COLUMN IF NOT EXISTS <column> <type>;
```

### 删除字段

```sql
ALTER TABLE <table> DROP COLUMN IF EXISTS <column>;
```

### 创建索引

```sql
-- 普通索引
CREATE INDEX IF NOT EXISTS idx_<table>_<column> ON <table>(<column>);

-- 并发创建（不锁表）
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_<table>_<column> ON <table>(<column>);
```

### 添加外键

```sql
ALTER TABLE <table> 
  ADD CONSTRAINT fk_<table>_<ref_table> 
  FOREIGN KEY (<column>) REFERENCES <ref_table>(<ref_column>);
```

### 数据迁移

```sql
-- 批量更新（避免锁表过久）
UPDATE <table> SET <column> = <value> WHERE <condition>
  AND id IN (SELECT id FROM <table> WHERE <condition> LIMIT 1000);
```

---

## 安全检查清单

执行迁移前检查：

- [ ] up和down脚本成对存在
- [ ] 脚本可以重复执行（幂等性）
- [ ] down脚本能够完全回滚up的变更
- [ ] 在测试环境验证过
- [ ] 考虑了性能影响（大表操作）
- [ ] 考虑了数据兼容性
- [ ] 添加了适当的注释
- [ ] 设置了合理的超时（如需要）

---

## 常见问题

### Q: 迁移脚本何时执行？
**A**: 由部署流程执行，不是在开发阶段手动执行。开发阶段只需创建脚本文件。

### Q: 如何测试迁移脚本？
**A**: 
1. 在测试环境执行up脚本
2. 验证表结构和数据
3. 执行down脚本
4. 验证回滚成功

### Q: 迁移脚本失败怎么办？
**A**: 
1. 如果在事务中，会自动回滚
2. 如果不在事务中，需要手动执行down脚本
3. 修复问题后重新执行

### Q: 大表修改如何避免锁表？
**A**:
1. 使用`CONCURRENTLY`创建索引
2. 分批更新数据（LIMIT）
3. 在维护窗口执行
4. 考虑使用逻辑复制

---

## 下一步

- 如需更新测试数据 → [db-test-data.md](db-test-data.md)

