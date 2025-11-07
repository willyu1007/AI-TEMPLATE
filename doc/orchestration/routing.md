# 文档路由与合并规则

> **用途**: 定义智能体如何读取和合并agent.md配置
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## 核心原则

### 1. 分层读取
智能体读取agent.md的顺序：
```
模块实例agent.md → 根agent.md → doc/policies/
```

### 2. 合并策略
- **默认**: `child_overrides_parent`（子级覆盖父级）
- **可在根agent.md中配置**: `merge_strategy: "child_overrides_parent"`

示例：
```yaml
# 根agent.md
constraints:
  - "不得直接操作数据库"
  - "保持测试覆盖率≥80%"

# 模块agent.md
constraints:
  - "必须使用ORM访问数据库"
  - "保持测试覆盖率≥90%"  # 覆盖父级

# 最终合并结果（子级覆盖）
constraints:
  - "必须使用ORM访问数据库"
  - "保持测试覆盖率≥90%"
```

### 3. 按需加载
- **always_read**: 每次必读的文档（如policies/goals.md）
- **on_demand**: 按主题读取（如"数据库"→DB_SPEC.yaml）
- **by_scope**: 按范围读取（如"模块user"→modules/user/doc/）

---

## Context Routes配置

### always_read（必读文档）
每个智能体启动时自动读取：

```yaml
context_routes:
  always_read:
    - /doc/policies/goals.md
    - /doc/policies/safety.md
    - /README.md
```

### on_demand（按需文档）
根据任务主题按需读取：

```yaml
context_routes:
  on_demand:
    - topic: "数据库操作"
      paths:
        - /docs/db/DB_SPEC.yaml
        - /docs/db/SCHEMA_GUIDE.md
    - topic: "API开发"
      paths:
        - /docs/process/CONVENTIONS.md
        - /tools/openapi.json
    - topic: "模块开发"
      paths:
        - /doc/modules/MODULE_INIT_GUIDE.md
        - /doc/modules/MODULE_TYPES.md
```

### by_scope（按范围文档）
根据工作范围读取：

```yaml
context_routes:
  by_scope:
    - scope: "modules/user"
      read:
        - /modules/user/agent.md
        - /modules/user/README.md
        - /modules/user/doc/CONTRACT.md
        - /modules/user/doc/CHANGELOG.md
    - scope: "common"
      read:
        - /common/README.md
        - /common/models/base.py
```

---

## 路由实践

### 场景1: 初始化新模块
智能体应读取：
```
always_read: policies/goals.md, policies/safety.md
on_demand: 
  - topic: "模块开发"
by_scope: 
  - scope: "modules/<entity>"
```

### 场景2: 修改数据库
智能体应读取：
```
always_read: policies/goals.md, policies/safety.md
on_demand: 
  - topic: "数据库操作"
by_scope: 
  - scope: "db/"
```

### 场景3: 修复模块Bug
智能体应读取：
```
always_read: policies/goals.md, policies/safety.md
on_demand: 
  - topic: "模块开发"
by_scope: 
  - scope: "modules/<entity>"
  - scope: "tests/<entity>"
```

---

## 路径校验

使用`doc_route_check.py`脚本自动校验所有路由路径：

```bash
make doc_route_check
```

校验内容：
- 路径是否存在
- 路径是否指向有效文件
- 是否有循环依赖

---

## 注意事项

### 避免过度加载
- 不要在`always_read`中包含大文件（>500KB）
- 大文件应放在`on_demand`或`by_scope`中

### 路径规范
- 使用绝对路径（从根目录开始）
- 使用正斜杠`/`（跨平台兼容）
- 路径兼容：当前支持`docs/`和`doc/`（Phase 3后统一为`doc/`）

### 安全限制
- 智能体只能读取`context_routes`中声明的路径
- 写入受`ownership.code_paths`限制

---

**维护**: 根agent.md变更时，同步更新本文档
**相关**: doc/policies/goals.md, doc/policies/safety.md

