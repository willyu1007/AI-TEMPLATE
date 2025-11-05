# example 模块

## 目标
演示模块结构与文档协同，作为其他模块的参考模板，提供完整的文档范例。

## 适用场景
- 创建新模块时的参考模板
- 学习模块文档最佳实践
- 理解模块化开发流程

## 前置条件
- 已阅读 `agent.md` §5 模块化开发流程
- 已执行 `make docgen` 生成索引
- 了解项目整体架构

---

## 模块职责

### 核心功能
1. **功能演示**：展示如何组织模块代码和文档
2. **文档模板**：提供 8 个必备文档的完整示例
3. **测试示例**：展示单元测试、集成测试和冒烟测试

### 边界定义

#### 输入
- 来自前端的用户请求（HTTP/WebSocket）
- 其他模块的数据流（通过契约定义）
- 配置参数（从 `config/` 加载）

#### 输出
- 处理结果（JSON 格式）
- 状态信息（成功/失败/进行中）
- 日志和审计记录

#### 依赖
- **工具**：codegen（`tools/codegen/contract.json`）
- **服务**：无
- **模块**：无（独立模块）
- **数据库**：可选（如需持久化）

---

## 目录结构

```
modules/example/
├── README.md        # 本文档：模块概述和架构
├── plan.md          # 开发计划：当前迭代任务
├── CONTRACT.md      # 接口契约：输入输出定义
├── TEST_PLAN.md     # 测试计划：测试用例清单
├── RUNBOOK.md       # 运维手册：部署和故障排查
├── PROGRESS.md      # 进度跟踪：里程碑和状态
├── BUGS.md          # 缺陷管理：已知问题和复盘
├── CHANGELOG.md     # 变更日志：版本历史
├── core/            # 核心业务逻辑
├── api/             # API 接口层
├── models/          # 数据模型定义
└── utils/           # 工具函数
```

---

## 技术栈

### 运行时要求
- **Python**: ≥ 3.11
- **依赖包**：见 `requirements.txt`

### 环境变量
| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `APP_ENV` | 是 | dev | 运行环境（dev/staging/prod）|
| `LOG_LEVEL` | 否 | INFO | 日志级别 |
| `DATABASE_URL` | 否 | - | 数据库连接（如需持久化）|

### 配置项
参见 `config/defaults.yaml` 中的 `example` 章节

---

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境
```bash
export APP_ENV=dev
export LOG_LEVEL=DEBUG
```

### 3. 运行模块
```bash
# 方法 1：直接运行
python -m example.main

# 方法 2：使用 docker-compose
docker-compose up example
```

### 4. 验证功能
```bash
# 运行冒烟测试
pytest tests/example/test_smoke.py

# 调用接口测试
curl http://localhost:8000/api/example/health
```

---

## 验证步骤

### 功能验证
```bash
# 1. 模块可导入
python -c "import example; print('OK')"

# 2. 核心功能可用
pytest tests/example/ -v

# 3. 接口可访问（如有）
curl http://localhost:8000/api/example/status
```

### 集成验证
```bash
# 1. 与其他模块集成测试
pytest tests/integration/ -k example

# 2. DAG 校验
make dag_check

# 3. 契约兼容性
make contract_compat_check
```

---

## 回滚逻辑

如果模块变更导致问题：

### 1. 快速回滚
```bash
# 代码回滚
git checkout <previous-tag>

# 重启服务
docker-compose restart example

# 验证
pytest tests/example/test_smoke.py
```

### 2. 数据库回滚（如有迁移）
```bash
# 执行 down 脚本
psql -d app -f migrations/<version>_down.sql

# 验证表结构
\d+ example_table
```

### 3. 配置回滚
```bash
# 恢复配置文件
git checkout <previous-tag> -- config/

# 重启服务
docker-compose restart
```

---

## 性能指标

### SLA 要求
- **响应时间**: P95 < 2000ms（见 `flows/dag.yaml`）
- **可用性**: ≥ 99.9%
- **并发**：支持 10+ 并发请求

### 监控指标
- 请求成功率
- 平均响应时间
- 错误率

---

## 相关文档
- **开发计划**：`plan.md`
- **接口契约**：`CONTRACT.md`
- **测试计划**：`TEST_PLAN.md`
- **运维手册**：`RUNBOOK.md`
- **项目 DAG**：`flows/dag.yaml`
