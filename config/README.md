# 配置管理（Configuration）

## 目标
提供统一的配置加载机制，支持多环境部署和安全的密钥管理。

## 配置层次

配置按以下优先级层叠加载：

### 加载顺序（优先级从低到高）
1. **defaults.yaml** - 默认配置（所有环境通用）
2. **<env>.yaml** - 环境特定配置（dev/staging/prod）
3. **环境变量** - 运行时覆盖
4. **Secrets** - 密钥（最高优先级，不提交到 git）

## 文件说明

| 文件 | 用途 | 提交到git |
|------|------|----------|
| `schema.yaml` | 配置结构定义（类型、必填、默认值）| ✅ |
| `defaults.yaml` | 默认配置 | ✅ |
| `dev.yaml` | 开发环境配置 | ✅ |
| `staging.yaml` | 预发布环境配置 | ✅ |
| `prod.yaml` | 生产环境配置（无密钥）| ✅ |
| `.secrets.yaml` | 本地密钥（**禁止提交**）| ❌ |

## 加载示例

参考 `loader/` 目录下的示例代码：
- `python_loader.py` - Python 配置加载
- `go_loader.go` - Go 配置加载
- `ts_loader.ts` - TypeScript 配置加载

## 相关文档
- 详细指南：`docs/process/CONFIG_GUIDE.md`
- 环境规范：`docs/process/ENV_SPEC.yaml`


