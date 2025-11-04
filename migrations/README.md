# 数据库迁移脚本

## 命名规范
```
<version>_<description>_up.sql
<version>_<description>_down.sql
```

示例：
- `001_create_users_table_up.sql`
- `001_create_users_table_down.sql`

## 规则
1. **必须成对**：每个 up 脚本必须有对应的 down 脚本
2. **版本递增**：版本号递增（001, 002, 003...）
3. **幂等性**：脚本应可重复执行
4. **向下兼容**：尽量保持向下兼容，避免破坏性变更

## 执行
```bash
# 检查迁移脚本
make migrate_check

# 手动执行（示例）
psql -d database_name -f migrations/001_create_users_table_up.sql

# 回滚（示例）
psql -d database_name -f migrations/001_create_users_table_down.sql
```

## 注意事项
- 在 down 脚本中要谨慎处理数据删除
- 对于生产环境，建议先备份数据
- 大表变更要评估锁表时间

