# example 模块

## 职责
演示模块结构与文档协同，作为其他模块的参考模板。

## 边界
### 输入
- 来自前端的用户请求
- 其他模块的数据流

### 输出
- 处理结果
- 状态信息

### 依赖
- 工具：codegen（`tools/codegen/contract.json`）
- 服务：无
- 模块：无

## 架构
```
example/
├── core/          # 核心逻辑
├── api/           # API 接口
├── models/        # 数据模型
└── utils/         # 工具函数
```

## 运行要求
- Python 3.11+
- 环境变量：
  - `APP_ENV`: 运行环境（dev/staging/prod）
- 配置项：见 `config/defaults.yaml`
