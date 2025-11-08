# 脚本目录说明

本目录包含项目的自动化脚本，用于检查、生成和维护。

---

## 脚本分类

### 文档与索引
| 脚本 | 功能 | 命令 |
|------|------|------|
| docgen.py | 生成文档索引（.aicontext/） | `make docgen` |
| doc_style_check.py | 文档风格检查（调用scripts/encoding_check.py） | `make doc_style_check` |

### DAG与契约
| 脚本 | 功能 | 命令 |
|------|------|------|
| dag_check.py | DAG拓扑校验 | `make dag_check` |
| contract_compat_check.py | 契约兼容性检查 | `make contract_compat_check` |

### 数据库
| 脚本 | 功能 | 命令 |
|------|------|------|
| migrate_check.py | 迁移脚本成对检查 | `make migrate_check` |
| rollback_check.sh | 回滚验证 | `make rollback_check PREV_REF=<tag>` |

### 配置与一致性
| 脚本 | 功能 | 命令 |
|------|------|------|
| runtime_config_check.py | 运行时配置校验 | `make runtime_config_check` |
| consistency_check.py | 文档一致性检查 | `make consistency_check` |
| app_structure_check.py | 应用层结构检查 | `make app_structure_check` |

### 依赖管理
| 脚本 | 功能 | 命令 |
|------|------|------|
| deps_manager.py | 依赖检测与补全 | `make deps_check` |

### 测试
| 脚本 | 功能 | 命令 |
|------|------|------|
| test_scaffold.py | 生成测试脚手架 | `make tests_scaffold MODULE=<name>` |
| test_status_check.py | 人工测试状态检查 | `make test_status_check` |

### 前端类型
| 脚本 | 功能 | 命令 |
|------|------|------|
| generate_openapi.py | 生成OpenAPI规范 | `make generate_openapi` |
| generate_frontend_types.py | 生成前端TypeScript类型 | `make generate_frontend_types` |
| frontend_types_check.py | 前端类型一致性检查 | `make frontend_types_check` |

### UX与数据流
| 脚本 | 功能 | 命令 |
|------|------|------|
| dataflow_trace.py | UX数据流转检查 | `make dataflow_check` |

### AI维护
| 脚本 | 功能 | 命令 |
|------|------|------|
| ai_maintenance.py | AI自动维护 | `make ai_maintenance` |
| ai_begin.sh | 模块初始化 | `make ai_begin MODULE=<name>` |

### 编排与模块管理（Phase 1-4）
| 脚本 | 功能 | 命令 | 状态 |
|------|------|------|------|
| agent_lint.py | 校验agent.md YAML前言 | `make agent_lint` | ✅ Phase 1 |
| registry_check.py | 校验模块注册表 | `make registry_check` | ✅ Phase 1 |
| doc_route_check.py | 校验文档路由路径 | `make doc_route_check` | ✅ Phase 1 |
| type_contract_check.py | 校验模块类型契约 | `make type_contract_check` | ✅ Phase 4 |
| doc_script_sync_check.py | 文档与脚本同步检查 | `make doc_script_sync_check` | ✅ Phase 4 |
| registry_gen.py | 生成registry.yaml草案（半自动） | `make registry_gen` | ✅ Phase 1 |
| module_doc_gen.py | 生成模块实例文档 | `make module_doc_gen` | ✅ Phase 1 |

### 数据库治理（Phase 5）
| 脚本 | 功能 | 命令 | 状态 |
|------|------|------|------|
| db_lint.py | 数据库文件校验（迁移脚本、表YAML） | `make db_lint` | ✅ Phase 5 |

### 测试数据管理（Phase 7）
| 脚本 | 功能 | 命令 | 状态 |
|------|------|------|------|
| fixture_loader.py | Fixtures加载工具（模块感知） | `make load_fixture MODULE=<name> FIXTURE=<scenario>` | ✅ Phase 7 |
| fixture_loader.py | 清理模块测试数据 | `make cleanup_fixture MODULE=<name>` | ✅ Phase 7 |
| fixture_loader.py | 列举所有模块 | `make list_modules` | ✅ Phase 7 |
| fixture_loader.py | 列举模块的Fixtures | `make list_fixtures MODULE=<name>` | ✅ Phase 7 |

### 聚合验证
| 脚本 | 功能 | 命令 | 状态 |
|------|------|------|------|
| validate.sh | 完整验证流程（7个检查） | `make validate` | ✅ 已有 |

### 内部工具（不直接调用）
| 脚本 | 功能 | 被谁调用 |
|------|------|---------|
| encoding_check.py | 文件编码检查 | doc_style_check.py内部调用 |

---

## 命令说明

### 已实现的命令
上述表格中列出的所有脚本都已实现，可以直接使用。

### 文档中提及但未实现的命令

以下命令在文档中提及，但尚未实现或不需要实现：

#### 示例命令（不需要实现）
这些命令出现在`doc/modules/example/`示例模块中，仅作为示例说明：
- `make test` - 示例：运行测试
- `make test_integration` - 示例：集成测试
- `make coverage` - 示例：覆盖率报告
- `make dev MODULE=<name>` - 示例：运行服务
- `make backup` - 示例：备份数据
- `make setup_test_data` - 示例：准备测试数据
- `make cleanup_test_data` - 示例：清理测试数据

**说明**: 这些是文档示例，实际项目可根据需要实现。

#### Phase 5+将实现的命令（数据库相关）
- `make db_migrate` - 数据库迁移（待Phase 8+实现）
- `make db_rollback` - 数据库回滚（待Phase 8+实现）
- `make db_shell` - 数据库Shell（待Phase 8+实现）
- `make db_gen_ddl` - 生成DDL（待Phase 8+实现）
- `make db_env ENV=<env>` - 数据库环境切换（Phase 7部分实现）

**说明**: 
- Phase 5已实现：db_lint（数据库文件校验）
- Phase 7已实现：fixture_loader（Fixtures加载）
- 其他数据库命令待Phase 8+实现。

#### 其他
- `make style_check` - 可能是`doc_style_check`的别名，待确认

---

## 使用说明

### 开发流程中的脚本调用

#### 1. 初始化新模块
```bash
make ai_begin MODULE=my_feature
# 调用：ai_begin.sh
```

#### 2. 开发过程中
```bash
make dev_check
# 聚合调用（Phase 7更新）：
#   - docgen.py
#   - doc_style_check.py
#   - agent_lint.py (Phase 1)
#   - registry_check.py (Phase 1)
#   - doc_route_check.py (Phase 1)
#   - type_contract_check.py (Phase 4)
#   - doc_script_sync_check.py (Phase 4)
#   - db_lint.py (Phase 5)
#   - dag_check.py
#   - contract_compat_check.py
#   - deps_manager.py
#   - runtime_config_check.py
#   - migrate_check.py
#   - consistency_check.py
#   - frontend_types_check.py
```

#### 3. 提交前
```bash
make rollback_check PREV_REF=v1.0.0
# 调用：rollback_check.sh
```

#### 4. 模块注册（Phase 1）
```bash
# 生成草案
make registry_gen

# 人工审核doc/orchestration/registry.yaml.draft
# 补充TODO标记的内容

# 重命名为registry.yaml
mv doc/orchestration/registry.yaml.draft doc/orchestration/registry.yaml

# 校验
make registry_check

# 生成模块文档
make module_doc_gen
```

#### 5. 测试数据管理（Phase 7新增）
```bash
# 列举所有模块
make list_modules

# 列举模块的Fixtures
make list_fixtures MODULE=example

# 加载Fixtures（dry-run模式，仅检查）
make load_fixture MODULE=example FIXTURE=minimal DRY_RUN=1

# 加载Fixtures（实际执行，需要数据库连接）
make load_fixture MODULE=example FIXTURE=minimal

# 清理测试数据
make cleanup_fixture MODULE=example
```

### 8. Mock数据生成与管理（Phase 8.5+）

**Mock数据生成器** (`mock_generator.py`):
- 从TEST_DATA.md读取Mock生成规则
- 使用Faker生成随机测试数据
- 支持数据分布、约束、关系
- 批量插入数据库
- 注册到生命周期管理

**Mock生命周期管理** (`mock_lifecycle.py`):
- 列出活跃的Mock记录
- 清理过期的Mock数据
- 查看Mock统计信息
- 手动删除Mock记录

**用法**:
```bash
# 生成Mock数据（dry-run模式）
make generate_mock MODULE=example TABLE=runs COUNT=1000 DRY_RUN=1

# 生成Mock数据（实际插入，需要数据库连接和Faker库）
make generate_mock MODULE=example TABLE=runs COUNT=1000

# 生成短期Mock数据（1小时后过期）
make generate_mock MODULE=example TABLE=runs COUNT=100 LIFECYCLE=ephemeral

# 生成持久Mock数据（需手动清理）
make generate_mock MODULE=example TABLE=runs COUNT=50 LIFECYCLE=persistent

# 使用随机种子（可重复生成）
make generate_mock MODULE=example TABLE=runs COUNT=100 SEED=42

# 列出活跃的Mock记录
make list_mocks

# 按模块过滤
make list_mocks MODULE=example

# 清理过期的Mock数据
make cleanup_mocks

# Dry-run模式
make cleanup_mocks DRY_RUN=1

# 查看Mock统计信息
make mock_stats

# 按模块查看统计
make mock_stats MODULE=example

# 删除指定Mock记录
make delete_mock ID=<mock_id>
```

**生命周期类型**:
- `ephemeral`: 1小时后自动过期
- `temporary`: 7天后自动过期（默认）
- `persistent`: 持久保留，需手动清理
- `fixture`: 可转为Fixture保存

**依赖**:
- `Faker>=20.0.0` - Mock数据生成（必需）
- `psycopg2-binary>=2.9.0` - 数据库连接（可选，无则dry-run）

---

## 依赖

### Python依赖
大部分脚本需要：
- Python ≥ 3.7
- pyyaml

可选依赖：
- jsonschema（用于agent_lint.py的Schema校验）
- pytest（用于测试）

安装：
```bash
pip install -r requirements.txt
```

### Bash脚本
以下脚本需要Bash环境：
- ai_begin.sh
- rollback_check.sh
- validate.sh

Windows用户可以使用Git Bash或WSL。

---

## 开发指南

### 添加新脚本

1. 在scripts/目录创建脚本文件
2. 添加文件头注释（功能说明、用法）
3. 设置Windows UTF-8输出支持（如需）：
   ```python
   if sys.platform == "win32":
       import io
       sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
       sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
   ```
4. 在Makefile中添加对应命令
5. 更新本README.md
6. 如集成到dev_check，更新Makefile的dev_check目标

### 脚本规范

1. **文件头**：包含功能说明和用法
2. **编码**：支持UTF-8，处理Windows编码问题
3. **路径**：使用pathlib.Path，兼容Windows和Linux
4. **错误处理**：友好的错误信息，明确的退出码
5. **输出格式**：使用[ok]/[error]/[warn]前缀
6. **兼容性**：考虑Phase过渡期的路径兼容（doc/ vs doc/）

---

## 维护

脚本维护责任人：项目维护者

如发现脚本问题或需要新功能，请：
1. 提交Issue说明问题
2. 或直接提交PR修复

---

**最后更新**: 2025-11-08 (Phase 8.5+)

## 变更历史

- **2025-11-08 Phase 8.5+**: 新增Mock数据生成与管理工具（mock_generator.py、mock_lifecycle.py）
- **2025-11-07 Phase 7**: 新增测试数据管理工具（fixture_loader.py）、更新dev_check集成所有校验
- **2025-11-07 Phase 5**: 新增数据库治理工具（db_lint.py）
- **2025-11-07 Phase 4**: 新增类型契约校验和文档同步检查
- **2025-11-07 Phase 1**: 新增编排与模块管理工具（agent_lint等7个脚本）
- **2025-11-07**: 初始版本


