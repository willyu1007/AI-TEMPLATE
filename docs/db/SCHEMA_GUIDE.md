# 数据库 Schema 指南

## 目标
规范数据库表结构设计，确保数据一致性、性能和可维护性。

## 适用场景
- 新建数据库表
- 修改现有表结构
- 添加索引和约束

## 核心规范

### 1. 主键设计
**要求**：所有表必须使用 UUID v7 作为主键

**理由**：
- 全局唯一
- 包含时间信息，可排序
- 分布式友好

**示例**：
```
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ...
);
```

### 2. 时间字段
**要求**：使用 `TIMESTAMPTZ` 类型

**必备字段**：
- `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`
- `updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`

**触发器**：
```
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 3. 索引命名规范
**格式**：`idx_<表名>_<字段1>_<字段2>`

**示例**：
```
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_orders_user_id_status ON orders(user_id, status);
```

### 4. 外键约束
**要求**：明确设置级联规则

**示例**：
```
ALTER TABLE orders
    ADD CONSTRAINT fk_orders_user_id
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
```

### 5. 字段命名
- 使用 `snake_case`
- 布尔字段使用 `is_` 或 `has_` 前缀
- 时间字段使用 `_at` 后缀
- 外键使用 `<表名>_id` 格式

## Schema 变更流程

### 步骤
1. **更新 DB_SPEC.yaml**
   ```
   vim docs/db/DB_SPEC.yaml
   ```

2. **创建迁移脚本**
   ```
   # 创建成对的 up/down 脚本
   touch migrations/002_add_user_roles_up.sql
   touch migrations/002_add_user_roles_down.sql
   ```

3. **编写迁移 SQL**
   - up.sql：添加字段/表/索引
   - down.sql：回滚变更

4. **验证迁移**
   ```
   # 检查成对性
   make migrate_check
   
   # 测试执行
   psql -d test_db -f migrations/002_add_user_roles_up.sql
   psql -d test_db -f migrations/002_add_user_roles_down.sql
   ```

5. **更新文档**
   - 更新 `SCHEMA_GUIDE.md`
   - 更新相关模块的 `README.md`
   - 运行 `make docgen`

## 验证步骤

```bash
# 1. 检查迁移脚本
make migrate_check

# 2. 检查 DB_SPEC.yaml
cat docs/db/DB_SPEC.yaml

# 3. 在测试环境验证
psql -d test_db -f migrations/<version>_up.sql
# 验证数据结构
\d+ table_name
# 回滚测试
psql -d test_db -f migrations/<version>_down.sql
```

## 回滚逻辑

如果 Schema 变更导致问题：

1. **评估影响**
   - 检查是否有数据写入
   - 确认应用层是否已使用新字段

2. **执行回滚**
   ```
   # 数据库回滚
   psql -d prod_db -f migrations/<version>_down.sql
   
   # 应用回滚
   git revert <commit-hash>
   ```

3. **验证回滚**
   ```
   # 检查表结构
   \d+ table_name
   
   # 检查应用功能
   make dev_check
   ```

## 性能考虑

### 1. 索引策略
- 高频查询字段必须建索引
- 组合索引遵循最左前缀原则
- 避免过多索引（写入性能）

### 2. 大表变更
- 评估锁表时间
- 考虑在线 DDL（如 `CONCURRENTLY`）
- 分批迁移数据

**示例**：
```
-- 在线创建索引（不锁表）
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

## 相关文档
- 数据库规范：`docs/db/DB_SPEC.yaml`
- 迁移脚本：`migrations/README.md`
- 环境配置：`docs/process/ENV_SPEC.yaml`

