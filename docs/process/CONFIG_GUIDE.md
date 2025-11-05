# 配置管理指南（Configuration Guide）

## 目标
提供统一的配置管理机制，支持多环境部署和安全的密钥管理。

## 适用场景
- 多环境部署（dev/staging/prod）
- 配置变更管理
- 密钥和敏感信息管理

## 配置层次结构

配置通过以下优先级层叠加载：

```
1. config/defaults.yaml     （默认配置，最低优先级）
2. config/<env>.yaml         （环境特定配置）
3. 环境变量                  （运行时覆盖）
4. Secrets                   （密钥，最高优先级）
```

## 配置文件说明

### config/schema.yaml
**目的**：定义所有配置项的类型和约束

**示例**：
```yaml
database:
  type: object
  required: true
  properties:
    host:
      type: string
      required: true
    port:
      type: integer
      default: 5432
```

### config/defaults.yaml
**目的**：提供所有配置的默认值

### config/dev.yaml
**目的**：开发环境配置

### config/staging.yaml
**目的**：预发布环境配置

### config/prod.yaml
**目的**：生产环境配置（不包含敏感信息）

## 使用方法

### 1. 加载配置
参考 `config/loader/` 下的示例代码：
- `python_loader.py` - Python 加载示例
- `go_loader.go` - Go 加载示例
- `ts_loader.ts` - TypeScript 加载示例

### 2. 环境变量覆盖
```bash
# 示例：覆盖数据库配置
export DATABASE_HOST=custom-host
export DATABASE_PORT=5433
```

### 3. 密钥管理
**禁止**：将密钥直接写入配置文件

**推荐**：
- 使用环境变量
- 使用密钥管理服务（如 AWS Secrets Manager）
- 本地开发使用 `.env` 文件（不提交到 git）

## 验证步骤

```bash
# 检查配置文件格式和必填项
make runtime_config_check

# 验证配置加载
python -c "from config.loader.python_loader import load_config; print(load_config('dev'))"
```

## 相关文档
- 配置 Schema：`config/schema.yaml`
- 环境规范：`docs/process/ENV_SPEC.yaml`
- 配置加载器：`config/loader/`

