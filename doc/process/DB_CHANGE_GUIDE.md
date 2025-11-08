# 数据库变更指南

> **用途**: 指导数据库变更的完整流程  
> **适用场景**: 新建表、修改表结构、删除表  
> **版本**: 2.0 (渐进式披露)  
> **创建时间**: 2025-11-07  
> **最后更新**: 2025-11-08

---

## 概述

### 什么是数据库变更

数据库变更包括：
- 新建表（CREATE TABLE）
- 修改表结构（ALTER TABLE）
- 删除表（DROP TABLE）
- 创建/修改索引
- 调整约束

### 半自动化流程

1. **人工定义**: 创建表YAML（人类可读的表结构定义）
2. **半自动生成**: 根据YAML生成迁移脚本（未来可自动化）
3. **人工审核**: 审核迁移脚本
4. **自动校验**: 运行db_lint检查
5. **DBA执行**: 由部署流程或DBA执行迁移

---

## 触发机制

数据库变更可以在以下时机触发：

### 1. 通过plan.md触发（推荐）

在模块的`plan.md`中声明：

```yaml
database_impact:
  has_changes: true
  changes:
    - type: create_table
      table: <table_name>
      description: "<说明>"
```

AI会自动检测并引导完成数据库变更流程。

### 2. 模块初始化时（Phase 6）

在执行MODULE_INIT_GUIDE.md的Phase 6时，如果模块需要专属表。

### 3. 开发过程中

在Code Review或开发过程中，如果发现需要数据库变更。

---

## 数据库影响评估（必填）

在plan.md中声明数据库影响（**必填**）：

```yaml
database_impact:
  has_changes: true  # 或 false
  changes:          # 如has_changes=true，必须填写
    - type: create_table | alter_table | drop_table
      table: <table_name>
      description: "<变更说明>"
      risk_level: low | medium | high
      backward_compatible: true | false
```

---

## 快速开始

### 场景选择

根据你的需求选择：

| 场景 | 说明 | 详细指南 |
|------|------|----------|
| 新建表 | 创建一个新表 | [`resources/db-create-table.md`](resources/db-create-table.md) |
| 修改表 | 添加/删除字段、修改约束 | [`resources/db-alter-table.md`](resources/db-alter-table.md) |
| 迁移脚本 | 编写规范的up/down脚本 | [`resources/db-migration-script.md`](resources/db-migration-script.md) |
| 测试数据 | 更新Fixtures和TEST_DATA.md | [`resources/db-test-data.md`](resources/db-test-data.md) |

---

## 完整流程概览

### Step 1: 明确变更需求

**目标**: 确定变更类型、表名、字段等信息

**快速指引**:
- 询问用户变更类型（新建/修改/删除）
- 收集表名和字段信息
- 确认风险级别

**详细指南**: 
- 新建表 → [`resources/db-create-table.md § Step 1`](resources/db-create-table.md)
- 修改表 → [`resources/db-alter-table.md § Step 1`](resources/db-alter-table.md)

---

### Step 2: 创建/更新表YAML

**目标**: 在`db/engines/postgres/schemas/tables/`创建表结构YAML

**快速指引**:
```bash
# 文件位置
db/engines/postgres/schemas/tables/<table_name>.yaml

# 从模板复制
cp db/engines/postgres/schemas/tables/runs.yaml \
   db/engines/postgres/schemas/tables/<table_name>.yaml
```

**详细指南**: 
- 新建表 → [`resources/db-create-table.md § Step 2`](resources/db-create-table.md)
- 修改表 → [`resources/db-alter-table.md § Step 2`](resources/db-alter-table.md)

---

### Step 3: 创建迁移脚本

**目标**: 创建up和down迁移脚本

**快速指引**:
```bash
# 生成编号
NEXT_NUM=$(ls db/engines/postgres/migrations/ | grep -E "^[0-9]+" | sort -n | tail -1 | sed 's/^0*//' | awk '{print $1+1}')
NEXT_NUM=$(printf "%03d" $NEXT_NUM)

# 创建脚本
vi db/engines/postgres/migrations/${NEXT_NUM}_<operation>_<table>_up.sql
vi db/engines/postgres/migrations/${NEXT_NUM}_<operation>_<table>_down.sql
```

**详细指南**: 
- 迁移脚本规范 → [`resources/db-migration-script.md`](resources/db-migration-script.md)

---

### Step 4: 更新测试数据

**目标**: 更新TEST_DATA.md和Fixtures

**快速指引**:
- 更新`modules/<entity>/doc/TEST_DATA.md`
- 更新`modules/<entity>/fixtures/minimal.sql`
- 可选：更新standard.sql和performance.sql

**详细指南**: 
- 测试数据更新 → [`resources/db-test-data.md`](resources/db-test-data.md)

---

### Step 5: 校验

**目标**: 运行db_lint检查所有文件

**快速指引**:
```bash
make db_lint
```

**期望输出**:
```
✓ 迁移脚本成对性检查: 通过
✓ Table YAML格式检查: 通过
✓ 文件命名规范检查: 通过
```

---

## AI执行规范

### 必须做的事

✅ **询问变更类型和详细信息**  
   不要假设，需要明确用户意图

✅ **创建表YAML**  
   表YAML是数据库的"文档"，必须创建

✅ **创建成对的迁移脚本**  
   up和down必须成对，且down能够完全回滚up

✅ **更新TEST_DATA.md**  
   新表或表结构变更需要更新测试数据定义

✅ **运行db_lint校验**  
   确保所有文件符合规范

### 不要做的事

❌ **不要直接执行迁移脚本**  
   迁移脚本由部署流程或DBA执行

❌ **不要跳过表YAML**  
   即使可以直接写SQL，也要创建YAML

❌ **不要忘记down脚本**  
   每个up脚本必须有对应的down

❌ **不要在生产环境测试**  
   始终在测试环境验证

---

## 常见问题

### Q1: 什么时候需要数据库变更？
**A**: 
- 模块需要专属的表
- 需要添加/修改字段
- 需要调整索引或约束

不需要：仅查询现有表，或使用ORM的自动表创建（不推荐生产环境使用）。

### Q2: 表YAML和迁移脚本的关系？
**A**: 
- 表YAML：人类可读的表结构定义（文档）
- 迁移脚本：实际的SQL语句（执行）

两者应该保持同步，但表YAML是"源头"。

### Q3: 迁移脚本什么时候执行？
**A**: 由部署流程在部署时执行，不是在开发阶段手动执行。

### Q4: 如何回滚数据库变更？
**A**: 执行对应的down脚本。确保down脚本经过测试。

### Q5: 大表修改如何避免锁表？
**A**: 
- 使用`CONCURRENTLY`创建索引
- 分批更新数据
- 在维护窗口执行
- 参考：[db-alter-table.md § 常见问题](resources/db-alter-table.md)

---

## Resources索引

完整的数据库变更指南，请参考resources/目录：

| Resource | 内容 | 何时阅读 |
|----------|------|----------|
| [db-create-table.md](resources/db-create-table.md) | 创建新表流程 | 需要新建表时 |
| [db-alter-table.md](resources/db-alter-table.md) | 修改表结构流程 | 需要修改表时 |
| [db-migration-script.md](resources/db-migration-script.md) | 迁移脚本规范 | 编写迁移脚本时 |
| [db-test-data.md](resources/db-test-data.md) | 测试数据更新 | 变更后更新测试数据 |

---

## 相关文档

- [MODULE_INIT_GUIDE.md Phase 6](../modules/MODULE_INIT_GUIDE.md#phase-6) - 模块初始化时的数据库变更
- [db_lint.py](../../scripts/db_lint.py) - 数据库文件校验工具
- [runs.yaml](../../db/engines/postgres/schemas/tables/runs.yaml) - 表YAML示例

---

## 版本历史

- **2.0** (2025-11-08): 渐进式披露改造，拆分resources/
- **1.0** (2025-11-07): 创建初始版本
