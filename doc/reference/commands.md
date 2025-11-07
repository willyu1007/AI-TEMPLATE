# 命令速查手册

> **用途**: 提供所有可用命令的快速参考
> **版本**: 1.0
> **创建时间**: 2025-11-07
> **更新**: 新增命令时同步更新

---

## 日常开发

### 初始化
```bash
# 初始化新模块
make ai_begin MODULE=<name>

# 生成测试脚手架
make tests_scaffold MODULE=<name>
```

### 开发检查
```bash
# 完整检查（CI门禁）
make dev_check

# 快速检查
make quick_check

# 生成文档索引
make docgen
```

---

## 编排与模块管理（Phase 1新增）

```bash
# 校验agent.md YAML前言
make agent_lint

# 校验模块注册表
make registry_check

# 校验文档路由路径
make doc_route_check

# 生成registry.yaml草案（半自动）
make registry_gen

# 生成模块实例文档
make module_doc_gen
```

---

## 文档与索引

```bash
# 生成文档索引
make docgen

# 文档风格检查
make doc_style_check

# 依赖检测与补全
make deps_check
```

---

## DAG与契约

```bash
# DAG拓扑校验
make dag_check

# 契约兼容性检查
make contract_compat_check

# 更新契约基线
make update_baselines
```

---

## 数据库相关

```bash
# 生成DDL（半自动，Phase 5）
make db_gen_ddl TABLE=<table>

# 执行迁移（需确认）
make db_migrate

# 回滚迁移
make db_rollback VERSION=<version>

# 检查迁移脚本成对
make migrate_check

# 连接数据库
make db_shell
```

---

## 配置与一致性

```bash
# 运行时配置校验
make runtime_config_check

# 文档一致性检查
make consistency_check

# 应用层结构检查
make app_structure_check
```

---

## 测试相关

```bash
# 测试状态检查
make test_status_check

# 生成测试脚手架
make tests_scaffold MODULE=<name>

# 运行测试（项目自定义）
make test
```

---

## 前端类型相关

```bash
# 生成OpenAPI规范
make generate_openapi

# 生成前端TypeScript类型
make generate_frontend_types

# 前端类型一致性检查
make frontend_types_check
```

---

## 回滚与验证

```bash
# 回滚验证（高风险变更必做）
make rollback_check PREV_REF=<tag|branch>

# 示例
make rollback_check PREV_REF=v1.0.0
make rollback_check PREV_REF=main
```

---

## AI维护

```bash
# AI自动维护（生成维护报告）
make ai_maintenance

# 清理临时文件
make cleanup_tmp
```

---

## 聚合命令

```bash
# 开发检查（聚合）
make dev_check
# 包含：docgen, doc_style_check, dag_check, contract_compat_check,
#      deps_check, runtime_config_check, migrate_check, 
#      consistency_check, frontend_types_check,
#      agent_lint, registry_check, doc_route_check

# 快速检查（跳过慢速检查）
make quick_check

# 查看所有命令
make help
```

---

## 命令分类

### 校验类（验证规范）
- `agent_lint` - Agent校验
- `registry_check` - 注册表校验
- `doc_route_check` - 文档路由校验
- `dag_check` - DAG校验
- `contract_compat_check` - 契约兼容性
- `migrate_check` - 迁移检查
- `consistency_check` - 一致性检查

### 生成类（自动生成）
- `docgen` - 文档索引
- `registry_gen` - 注册表草案
- `module_doc_gen` - 模块文档
- `tests_scaffold` - 测试脚手架
- `generate_openapi` - OpenAPI规范
- `generate_frontend_types` - 前端类型

### 初始化类（创建资源）
- `ai_begin` - 初始化模块
- `db_migrate` - 数据库迁移

### 维护类（维护清理）
- `ai_maintenance` - AI维护
- `cleanup_tmp` - 清理临时文件
- `update_baselines` - 更新基线

---

## 常用组合

### 开始新任务
```bash
make docgen                    # 刷新索引
make ai_begin MODULE=<name>    # 创建模块（如需要）
# 编辑代码...
make dev_check                 # 验证
```

### 提交前
```bash
make dev_check                 # 完整检查
make rollback_check PREV_REF=main  # 高风险变更
git add .
git commit -m "..."
```

### 发布前
```bash
make dev_check                 # 完整检查
make rollback_check PREV_REF=v1.0.0  # 回滚测试
make ai_maintenance            # 生成维护报告
```

---

## 环境变量

某些命令需要环境变量：

```bash
# 数据库连接
export DATABASE_URL=postgresql://user:pass@host:5432/db

# 模块指定
export MODULE=user

# 回滚目标
export PREV_REF=v1.0.0
```

---

## 故障排查

### make dev_check失败

**检查步骤**:
1. 运行单个检查定位问题：`make agent_lint`
2. 查看具体错误信息
3. 修复后重新运行

### make命令找不到

**解决**:
```bash
# 检查Makefile
cat Makefile | grep "^[a-z_]*:"

# 查看帮助
make help
```

### Python脚本报错

**解决**:
```bash
# 安装依赖
pip install -r requirements.txt

# 检查Python版本
python --version  # 需要≥3.7
```

---

## 相关文档

- **Makefile**: 项目根目录Makefile（实现）
- **脚本说明**: scripts/README.md
- **快速开始**: QUICK_START.md
- **角色与门禁**: doc/policies/roles.md

---

**维护**: 新增命令时同步更新本文档
**审核**: 每个Phase完成后审核命令列表

