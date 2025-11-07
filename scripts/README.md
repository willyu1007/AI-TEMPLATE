# 脚本目录说明

本目录包含项目的自动化脚本，用于检查、生成和维护。

---

## 脚本分类

### 文档与索引
| 脚本 | 功能 | 命令 |
|------|------|------|
| docgen.py | 生成文档索引（.aicontext/） | `make docgen` |
| doc_style_check.py | 文档风格检查 | `make doc_style_check` |
| encoding_check.py | 编码检查 | 内部调用 |

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

### 编排与模块管理（Phase 1新增）
| 脚本 | 功能 | 命令 | 状态 |
|------|------|------|------|
| agent_lint.py | 校验agent.md YAML前言 | `make agent_lint` | ✅ Phase 1 |
| registry_check.py | 校验模块注册表 | `make registry_check` | ✅ Phase 1 |
| doc_route_check.py | 校验文档路由路径 | `make doc_route_check` | ✅ Phase 1 |
| registry_gen.py | 生成registry.yaml草案（半自动） | `make registry_gen` | ✅ Phase 1 |
| module_doc_gen.py | 生成模块实例文档 | `make module_doc_gen` | ✅ Phase 1 |

### 聚合脚本
| 脚本 | 功能 | 命令 |
|------|------|------|
| validate.sh | 聚合验证 | 内部调用 |

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
# 聚合调用：
#   - docgen.py
#   - doc_style_check.py
#   - dag_check.py
#   - contract_compat_check.py
#   - deps_manager.py
#   - runtime_config_check.py
#   - migrate_check.py
#   - consistency_check.py
#   - frontend_types_check.py
#   - agent_lint.py (Phase 1新增)
#   - registry_check.py (Phase 1新增)
#   - doc_route_check.py (Phase 1新增)
```

#### 3. 提交前
```bash
make rollback_check PREV_REF=v1.0.0
# 调用：rollback_check.sh
```

#### 4. 模块注册（Phase 1新增）
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
6. **兼容性**：考虑Phase过渡期的路径兼容（docs/ vs doc/）

---

## 维护

脚本维护责任人：项目维护者

如发现脚本问题或需要新功能，请：
1. 提交Issue说明问题
2. 或直接提交PR修复

---

**最后更新**: 2025-11-07 (Phase 1)


