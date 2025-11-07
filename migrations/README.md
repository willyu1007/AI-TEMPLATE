# 数据库迁移脚本（已迁移）

> ⚠️ **重要提示**: 此目录的内容已迁移到新位置

---

## 新位置

数据库迁移脚本现已统一管理在：

```
db/engines/postgres/migrations/
```

**包含文件**:
- `001_example_create_runs_table_up.sql`
- `001_example_create_runs_table_down.sql`
- `README.md` - 完整的迁移脚本指南

---

## 迁移原因

为了更好地组织数据库相关文件，我们采用了按引擎分类的目录结构：

```
db/
├── engines/
│   ├── postgres/          # PostgreSQL 相关
│   │   ├── migrations/    # 迁移脚本 ← 新位置
│   │   ├── schemas/       # 表结构定义
│   │   │   └── tables/    # 表YAML描述文件
│   │   ├── docs/          # 文档
│   │   └── extensions/    # 扩展配置
│   └── redis/             # Redis 相关
│       └── ...
└── README.md
```

---

## 快速链接

- **迁移脚本新位置**: [db/engines/postgres/migrations/](../db/engines/postgres/migrations/README.md)
- **数据库规范**: [db/engines/postgres/docs/DB_SPEC.yaml](../db/engines/postgres/docs/DB_SPEC.yaml)
- **Schema 指南**: [db/engines/postgres/docs/SCHEMA_GUIDE.md](../db/engines/postgres/docs/SCHEMA_GUIDE.md)
- **数据库引擎说明**: [db/engines/README.md](../db/engines/README.md)

---

## 清理计划

此目录将在确认所有引用更新后删除（预计在 Phase 8 完成）。

在此之前，请使用新位置的文件。

---

**最后更新**: 2025-11-07（Phase 5）
