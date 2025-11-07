# Schemas目录

## 目标
存放项目中使用的Schema定义文件，用于数据结构验证和规范化。

## 适用场景
- 定义数据结构的Schema（JSON Schema、YAML Schema）
- 用于自动化校验脚本
- 确保数据格式的一致性和正确性

---

## Schema文件列表

### agent.schema.yaml
**用途**: 定义agent.md文件的YAML Front Matter规范

**被使用**:
- `scripts/agent_lint.py` - 校验agent.md的YAML前言

**主要字段**:
- 必填: spec_version, agent_id, role
- 可选: level, module_type, ownership, io, dependencies等

**相关命令**:
```bash
make agent_lint    # 使用此Schema校验agent.md
```

**参考文档**:
- agent.md v2规范: temp/修改方案(正式版).md §4

---

### db/table.schema.yaml（规划中，Phase 5）
**用途**: 定义数据库表结构YAML的Schema

**将被使用**:
- `scripts/db_spec_align_check.py` - 校验表结构定义

---

## 目录说明

### 不需要agent.md
本目录**不需要**agent.md文档，因为：
- schemas/不是业务模块，而是配置/规范存放目录
- 不需要被Orchestrator调度
- 不需要定义I/O接口和依赖关系

### 仅需README.md
- 本README.md说明schemas/的用途
- 列出所有Schema文件及其使用场景
- 提供相关命令和参考文档

---

## 使用说明

### 添加新的Schema

1. **创建Schema文件**
   ```bash
   # 在schemas/目录创建新的Schema文件
   touch schemas/my_schema.yaml
   ```

2. **定义Schema**
   ```yaml
   # schemas/my_schema.yaml
   type: object
   required: [field1, field2]
   properties:
     field1: {type: string}
     field2: {type: integer}
   ```

3. **在脚本中使用**
   ```python
   # scripts/my_check.py
   import yaml
   from pathlib import Path
   
   SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "my_schema.yaml"
   
   with open(SCHEMA_PATH) as f:
       schema = yaml.safe_load(f)
   
   # 使用jsonschema进行校验
   import jsonschema
   jsonschema.validate(data, schema)
   ```

4. **更新本README**
   - 添加新Schema的说明
   - 列出使用该Schema的脚本

---

## 依赖

### Python库
Schema校验通常需要：
- `pyyaml` - 解析YAML文件
- `jsonschema` - Schema校验（可选，推荐安装）

安装：
```bash
pip install pyyaml jsonschema
```

---

## 相关目录

| 目录 | 关系 | 说明 |
|------|------|------|
| schemas/ | 定义 | 本目录，存放Schema规范 |
| scripts/ | 使用 | 使用Schema进行校验的脚本 |
| doc/ | 规范 | 存放文档规范（文字描述） |

**关系图**:
```
schemas/agent.schema.yaml
    ↓ (被使用)
scripts/agent_lint.py → 校验 → agent.md
```

---

## 维护

### 更新Schema
当需要新增或修改字段时：
1. 更新schemas/中的Schema文件
2. 更新使用该Schema的脚本
3. 更新本README.md
4. 运行相关校验命令测试

### Schema版本管理
- Schema文件内建议包含version字段
- 重大变更时更新版本号
- 向后兼容性考虑

---

**创建时间**: 2025-11-07 (Phase 1)
**最后更新**: 2025-11-07


