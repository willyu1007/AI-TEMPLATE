# 数据库迁移脚本（Database Migrations）

## 目标
管理数据库 Schema 的版本演进，确保变更可追溯、可回滚。

## 适用场景
- 数据库表结构变更
- 添加/删除字段或索引
- 数据迁移和转换

## 前置条件
- 数据库已安装并可访问
- 已了解当前 Schema（见 `../docs/DB_SPEC.yaml`）
- 已准备测试数据

---

## 命名规范

### 格式
```
<version>_<description>_up.sql    # 向前迁移
<version>_<description>_down.sql  # 回滚迁移
```

### 示例
```
001_create_users_table_up.sql
001_create_users_table_down.sql

002_add_user_roles_up.sql
002_add_user_roles_down.sql
```

### 规则
- 版本号必须递增（001, 002, 003...）
- 描述使用小写和下划线
- 文件名不超过 100 字符

---

## 核心规则

### 1. 必须成对
每个 `up.sql` 必须有对应的 `down.sql`

**验证**：
```
make migrate_check
```

### 2. 幂等性
脚本必须可以安全地重复执行

**示例**：
```
-- up.sql（幂等）
CREATE TABLE IF NOT EXISTS users (...);

-- 而不是
CREATE TABLE users (...);  -- 第二次执行会失败
```

### 3. 向后兼容
尽量避免破坏性变更：
- 新增字段使用默认值或允许NULL
- 不直接删除字段（先标记废弃）
- 不修改现有字段类型

### 4. 事务包装
```
BEGIN;

-- 迁移操作
CREATE TABLE ...;
CREATE INDEX ...;

COMMIT;
```

---

## 执行流程

### 1. 创建迁移脚本
```
# 步骤 1：创建文件
touch migrations/003_add_email_index_up.sql
touch migrations/003_add_email_index_down.sql

# 步骤 2：编写 SQL
vim migrations/003_add_email_index_up.sql
# 内容：CREATE INDEX ...

vim migrations/003_add_email_index_down.sql
# 内容：DROP INDEX ...

# 步骤 3：检查成对性
make migrate_check
```

## 2. 测试迁移（开发环境）
```
# 步骤 1：备份数据
pg_dump dev_db > backup_before_migration.sql

# 步骤 2：执行 up
psql -d dev_db -f migrations/003_add_email_index_up.sql

# 步骤 3：验证变更
psql -d dev_db -c "\d+ users"

# 步骤 4：测试 down
psql -d dev_db -f migrations/003_add_email_index_down.sql

# 步骤 5：验证回滚
psql -d dev_db -c "\d+ users"

# 步骤 6：重新执行 up
psql -d dev_db -f migrations/003_add_email_index_up.sql
```

## 3. 生产环境执行
```
# 步骤 1：备份（必须）
pg_dump prod_db > backup_$(date +%Y%m%d_%H%M%S).sql

# 步骤 2：在维护窗口执行
psql -d prod_db -f migrations/003_add_email_index_up.sql

# 步骤 3：验证
psql -d prod_db -c "\d+ users"

# 步骤 4：监控应用
# 查看 Grafana 确认无异常

# 步骤 5：保留 down 脚本备用
# 如有问题立即执行回滚
```

---

## 验证步骤

### 开发环境验证
```
# 1. 语法检查
psql -d dev_db -f migrations/XXX_up.sql --dry-run

# 2. 成对性检查
make migrate_check

# 3. 实际执行测试
psql -d dev_db -f migrations/XXX_up.sql
psql -d dev_db -f migrations/XXX_down.sql

# 4. 应用兼容性测试
pytest tests/ -v
```

---

## 回滚操作

### 触发条件
- 迁移执行失败
- 应用功能异常
- 性能严重下降
- 数据一致性问题

### 回滚步骤
```
# 步骤 1：立即执行 down 脚本
psql -d prod_db -f migrations/XXX_down.sql

# 步骤 2：验证表结构
psql -d prod_db -c "\d+ table_name"

# 步骤 3：重启应用
systemctl restart app

# 步骤 4：验证功能
pytest tests/smoke/ -v

# 步骤 5：监控指标
# 查看 Grafana 确认恢复正常
```

## 回滚时间目标
- **执行时间**: < 10 分钟
- **验证时间**: < 5 分钟
- **总计**: < 15 分钟

---

## 注意事项

### 数据安全
1. ⚠️ 生产环境执行前必须备份
2. ⚠️ down 脚本中谨慎处理数据删除
3. ⚠️ 大表变更需要评估锁表时间

### 性能考虑
```
-- 大表添加索引使用 CONCURRENTLY（不锁表）
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- 大表变更分批执行
UPDATE users SET status = 'active' 
WHERE id IN (SELECT id FROM users LIMIT 1000);
```

### 兼容性
- 先添加字段（允许NULL）
- 然后填充数据
- 最后添加 NOT NULL 约束

---

## 相关文档
- Schema 指南：`../docs/SCHEMA_GUIDE.md`
- 数据库规范：`../docs/DB_SPEC.yaml`
- 回滚验证：`../../../../scripts/rollback_check.sh`
- 数据库引擎规范：`../../README.md`


