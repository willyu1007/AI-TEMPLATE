# 模块初始化 - Phase 6: 数据库变更

> **所属**: MODULE_INIT_GUIDE.md Phase 6  
> **用途**: Phase 6的详细执行指南  
> **目标**: 处理模块相关的数据库变更（可选）

---

## 目标

如果模块需要数据库支持，定义表结构、创建迁移脚本

---

## ⚠️ 重要说明

**Phase 6是可选的**。仅在以下情况执行：
- 模块需要专属的数据库表
- 需要修改现有表结构
- 需要添加索引或约束

**如果模块不涉及数据库，请直接跳过到Phase 7**

---

## 6.1 判断是否需要数据库变更

询问用户：
```
该模块是否需要专属的数据库表？
├─ 是 → 继续执行Phase 6
└─ 否 → 跳过到Phase 7
```

---

## 6.2 完整流程

**推荐使用独立流程**: 参考 `doc/process/DB_CHANGE_GUIDE.md`

该文档提供完整的数据库变更流程：
1. 创建表YAML（db/engines/postgres/schemas/tables/）
2. 生成迁移脚本（db/engines/postgres/migrations/）
3. 更新TEST_DATA.md
4. 运行db_lint校验

---

## 6.3 快速参考

### 步骤1: 创建表YAML

```bash
# 创建表结构定义
cat > db/engines/postgres/schemas/tables/<entity>_<table>.yaml <<EOF
table_name: <entity>_<table>
description: "<表功能描述>"

columns:
  - name: id
    type: bigserial
    constraints:
      - PRIMARY KEY
    description: "主键"
  
  - name: name
    type: varchar(255)
    constraints:
      - NOT NULL
    description: "名称"
  
  - name: created_at
    type: timestamp
    constraints:
      - NOT NULL
      - "DEFAULT CURRENT_TIMESTAMP"
    description: "创建时间"

indexes:
  - name: idx_<entity>_<table>_name
    columns: [name]
    unique: false

foreign_keys: []

constraints:
  - type: check
    expression: "length(name) > 0"
EOF
```

### 步骤2: 创建迁移脚本

```bash
# 生成迁移脚本编号
NEXT_NUM=$(ls db/engines/postgres/migrations/ | grep -E "^[0-9]+" | sort -n | tail -1 | sed 's/^0*//' | awk '{print $1+1}')
NEXT_NUM=$(printf "%03d" $NEXT_NUM)

# 创建up脚本
cat > db/engines/postgres/migrations/${NEXT_NUM}_create_<entity>_<table>_up.sql <<EOF
-- Migration: Create <entity>_<table> table
-- Generated: $(date +%Y-%m-%d)

CREATE TABLE <entity>_<table> (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT check_name_not_empty CHECK (length(name) > 0)
);

CREATE INDEX idx_<entity>_<table>_name ON <entity>_<table>(name);

COMMENT ON TABLE <entity>_<table> IS '<表功能描述>';
EOF

# 创建down脚本
cat > db/engines/postgres/migrations/${NEXT_NUM}_create_<entity>_<table>_down.sql <<EOF
-- Migration Rollback: Drop <entity>_<table> table
-- Generated: $(date +%Y-%m-%d)

DROP TABLE IF EXISTS <entity>_<table> CASCADE;
EOF
```

### 步骤3: 校验

```bash
make db_lint
```

---

## 常见问题

### Q: 一定要创建表YAML吗？
**A**: 是的。表YAML是数据库的"文档"，便于AI理解表结构。

### Q: 迁移脚本如何编号？
**A**: 使用三位数字（001, 002, 003...），自动递增。脚本会自动计算下一个编号。

### Q: 如果表已存在怎么办？
**A**: 创建ALTER TABLE迁移脚本，不要DROP重建。参考`DB_CHANGE_GUIDE.md` § 修改表。

### Q: 需要立即执行迁移脚本吗？
**A**: 不需要。迁移脚本在部署时由DBA或CI执行。初始化阶段只需创建脚本文件。

---

## AI执行规范

**必须做**:
- ✅ 询问用户是否需要数据库变更
- ✅ 如果需要，参考DB_CHANGE_GUIDE.md执行
- ✅ 运行`make db_lint`验证
- ✅ 如果不需要，直接跳过

**不要做**:
- ❌ 不要自动假设需要数据库
- ❌ 不要跳过表YAML的创建
- ❌ 不要手动执行迁移脚本（由部署流程执行）

---

## 下一步

完成数据库变更（或跳过）后，进入 → [Phase 7: 定义测试数据](init-testdata.md)

