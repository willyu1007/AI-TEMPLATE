# 数据库表结构定义（Tables YAML）

## 目标
以结构化的 YAML 格式描述数据库表结构，用于文档生成、校验和版本管理。

## 适用场景
- 新建表时创建对应的 YAML 描述
- 修改表结构时同步更新 YAML
- 自动生成数据库文档
- 校验表结构与迁移脚本的一致性

---

## 文件命名规范

### 格式
```
<table_name>.yaml
```

### 示例
```
runs.yaml          # runs 表
users.yaml         # users 表
orders.yaml        # orders 表
```

### 规则
- 文件名必须与表名完全一致
- 使用小写字母和下划线
- 一个文件对应一个表

---

## YAML 结构规范

### 最小必需字段

```yaml
meta:
  table_name: <表名>
  description: "表用途说明"
  migration_version: "001"

table:
  name: <表名>
  schema: public
  
  columns:
    - name: <字段名>
      type: <数据类型>
      nullable: true/false
      description: "字段说明"
  
  indexes:
    - name: <索引名>
      columns: [<字段列表>]

migrations:
  up: "<迁移脚本路径>"
  down: "<回滚脚本路径>"
```

### 完整字段说明

参见示例文件：`runs.yaml`

---

## 创建流程

### 步骤1: 创建 YAML 文件
```bash
cd db/engines/postgres/schemas/tables/
vim my_table.yaml
```

### 步骤2: 编写表结构描述
```yaml
meta:
  table_name: my_table
  description: "我的表说明"
  owner: "module_name"
  migration_version: "002"

table:
  name: my_table
  columns:
    - name: id
      type: UUID
      constraints: [PRIMARY KEY]
      nullable: false
      description: "主键"
    # ... 更多字段

  indexes:
    - name: idx_my_table_created_at
      columns: [created_at DESC]
```

### 步骤3: 创建对应的迁移脚本
```bash
# 创建迁移脚本
touch ../../migrations/002_create_my_table_up.sql
touch ../../migrations/002_create_my_table_down.sql

# 编写 SQL
vim ../../migrations/002_create_my_table_up.sql
```

### 步骤4: 在 YAML 中引用迁移脚本
```yaml
migrations:
  up: "../migrations/002_create_my_table_up.sql"
  down: "../migrations/002_create_my_table_down.sql"
```

### 步骤5: 运行校验
```bash
# 校验 YAML 格式
make db_lint

# 校验与迁移脚本一致性（如已实现）
make db_spec_align_check
```

---

## 维护规范

### 规则
1. **同步更新**: 修改表结构时，必须同步更新 YAML
2. **版本追踪**: `migration_version` 字段记录最后一次修改的迁移版本
3. **完整描述**: 所有字段和索引必须有 description
4. **关系维护**: 外键关系必须在 `relationships` 中声明

### 检查清单
- [ ] YAML 文件名与表名一致
- [ ] 所有字段有 description
- [ ] 索引名称符合规范（`idx_<表名>_<字段>`）
- [ ] 引用的迁移脚本路径正确
- [ ] `migration_version` 已更新
- [ ] 数据治理信息（sensitivity, retention）已填写

---

## 数据治理字段说明

### sensitivity（敏感级别）
- `public`: 公开数据
- `low`: 低敏感度
- `medium`: 中等敏感度（如用户行为数据）
- `high`: 高敏感度（如个人身份信息）
- `critical`: 极度敏感（如密码、支付信息）

### retention_days（保留天数）
- 数据保留的天数
- `-1` 表示永久保留
- 根据业务需求和合规要求设置

### access_control（访问控制）
定义哪些角色可以访问此表，及其权限：
```yaml
access_control:
  - role: app_service
    permissions: [SELECT, INSERT, UPDATE, DELETE]
  - role: analytics
    permissions: [SELECT]
  - role: backup
    permissions: [SELECT]
```

---

## 自动化工具（计划中）

### 生成文档
```bash
# 从 YAML 生成 Markdown 文档
make db_docgen

# 输出：db/engines/postgres/docs/TABLES.md
```

### 校验一致性
```bash
# 校验 YAML 与实际表结构的一致性
make db_spec_align_check
```

### 可视化
```bash
# 生成 ER 图（未来）
make db_diagram
```

---

## 示例文件

### runs.yaml
完整的表结构描述示例，包含：
- 元数据
- 字段定义
- 索引定义
- 数据治理信息
- 性能考虑
- 示例查询

---

## 相关文档
- Schema 指南：`../../docs/SCHEMA_GUIDE.md`
- 数据库规范：`../../docs/DB_SPEC.yaml`
- 迁移脚本：`../../migrations/README.md`
- 数据库引擎说明：`../../../README.md`

---

## 注意事项

### ⚠️ 重要
1. YAML 是文档，不是执行脚本
2. 表结构变更仍需通过迁移脚本执行
3. YAML 用于版本管理和文档生成
4. 保持 YAML 与实际表结构同步

### 最佳实践
- 创建表后立即创建 YAML
- 每次迁移后更新 `migration_version`
- 定期运行 `db_lint` 检查一致性
- 使用 `example_queries` 记录常用查询

---

**最后更新**: 2025-11-07（Phase 5）

