---
spec_version: "1.0"
agent_id: "modules.example.v1"
role: "示例模块，演示模块结构与文档协同，作为其他模块的参考模板"
level: 1
module_type: "1_example"

ownership:
  code_paths:
    include:
      - modules/example/
    exclude:
      - modules/example/doc/CHANGELOG.md

io:
  inputs:
    - name: task
      schema_ref: modules/example/doc/CONTRACT.md#输入参数
      description: "任务描述，长度1-10000字符"
    - name: language
      schema_ref: modules/example/doc/CONTRACT.md#输入参数
      description: "目标语言（python/javascript/go），可选，默认python"
    - name: dry_run
      schema_ref: modules/example/doc/CONTRACT.md#输入参数
      description: "演练模式，可选，默认false"
  outputs:
    - name: result
      schema_ref: modules/example/doc/CONTRACT.md#输出格式
      description: "处理结果或错误信息"
    - name: status
      schema_ref: modules/example/doc/CONTRACT.md#输出格式
      description: "执行状态（success/error）"
    - name: metadata
      schema_ref: modules/example/doc/CONTRACT.md#输出格式
      description: "元数据（处理时长、版本号等）"

contracts:
  apis:
    - modules/example/doc/CONTRACT.md

dependencies:
  upstream: []
  downstream: []

constraints:
  - "必须保持测试覆盖率 >= 80%"
  - "不直接访问数据库，如需持久化通过配置开启"
  - "所有接口必须向后兼容"
  - "响应时间 < 500ms（P95）"

tools_allowed:
  calls:
    - http
    - fs.read
    - fs.write

quality_gates:
  required_tests:
    - unit
    - integration
  coverage_min: 0.80

orchestration_hints:
  triggers:
    - "用户需要创建新模块时"
    - "学习模块文档最佳实践时"
    - "理解模块化开发流程时"
  routing_tags:
    - example
    - template
    - level:1

test_data:
  enabled: true
  spec: "doc/TEST_DATA.md"

context_routes:
  always_read:
    - modules/example/README.md
    - modules/example/doc/CONTRACT.md
  on_demand:
    - topic: "开发计划"
      paths:
        - modules/example/plan.md
    - topic: "测试"
      paths:
        - modules/example/doc/TEST_PLAN.md
    - topic: "运维"
      paths:
        - modules/example/doc/RUNBOOK.md
    - topic: "缺陷"
      paths:
        - modules/example/doc/BUGS.md
    - topic: "进度"
      paths:
        - modules/example/doc/PROGRESS.md
    - topic: "变更历史"
      paths:
        - modules/example/doc/CHANGELOG.md
---

# example 模块 - Agent配置

> **模块类型**: 1级基础示例模块
> **维护团队**: AI-TEMPLATE维护团队
> **版本**: 1.0.0

---

## 0. 模块概述

### 核心职责
本模块是**AI-TEMPLATE的示例和参考模板**，用于：
1. 展示如何组织模块代码和文档
2. 提供8个必备文档的完整示例
3. 演示单元测试、集成测试和冒烟测试

### 适用场景
- 创建新模块时的参考模板
- 学习模块文档最佳实践
- 理解模块化开发流程

---

## 1. 模块定位

### 1.1 边界定义

**输入**:
- 用户请求（HTTP/WebSocket）
- 其他模块数据流（通过契约定义）
- 配置参数（从config/加载）

**输出**:
- 处理结果（JSON格式）
- 状态信息（success/error/progress）
- 日志和审计记录

**不负责**:
- 直接的数据库操作（如需持久化需配置）
- 用户认证和授权（由上层处理）
- 跨模块事务管理

### 1.2 依赖关系

**上游依赖**: 无（独立模块）

**下游输出**: 无（示例模块）

**公共依赖**:
- `common/utils/` - 通用工具函数
- `config/` - 配置管理

---

## 2. 工作规范

### 2.1 代码修改权限

**允许修改**:
- `modules/example/` 下的所有代码文件
- `modules/example/doc/` 下的文档（除CHANGELOG.md）
- `modules/example/README.md`
- `modules/example/plan.md`

**禁止修改**:
- `modules/example/doc/CHANGELOG.md` - 仅在发布时更新
- 其他模块的代码
- 根目录的配置文件（除非经过审批）

### 2.2 质量标准

**测试要求**:
- 单元测试覆盖率 ≥ 80%
- 必须有集成测试
- 关键路径需要冒烟测试

**性能要求**:
- 响应时间 < 500ms（P95）
- 内存占用 < 100MB（稳态）

**兼容性**:
- 所有接口必须向后兼容
- 破坏性变更需要在CONTRACT.md中说明并提前通知

---

## 3. 开发流程

### 3.1 开始开发

1. **阅读文档**:
   - 先读 `README.md` 了解模块定位
   - 再读 `doc/CONTRACT.md` 了解接口
   - 查看 `plan.md` 了解当前任务

2. **环境准备**:
   ```bash
   # 安装依赖
   pip install -r requirements.txt
   
   # 配置环境
   export APP_ENV=dev
   export LOG_LEVEL=DEBUG
   ```

3. **开始编码**:
   - 遵循 `/doc/process/CONVENTIONS.md` 的编码规范
   - 测试驱动开发（TDD）
   - 提交前运行 `make test`

### 3.2 测试

```bash
# 单元测试
make test

# 集成测试
make test_integration

# 覆盖率报告
make coverage
```

### 3.3 提交代码

1. 运行质量检查：`make dev_check`
2. 更新 `doc/CHANGELOG.md`（如有变更）
3. 提交并创建PR
4. 等待CI通过和代码审查

详见 `/doc/process/pr_workflow.md`

---

## 4. 运维指南

### 4.1 部署

参见 `doc/RUNBOOK.md` 的部署章节

### 4.2 监控

关键指标：
- 请求成功率
- 响应时间（P50/P95/P99）
- 错误率

### 4.3 故障排查

常见问题和解决方案见 `doc/RUNBOOK.md` 的故障排查章节

---

## 5. 文档索引

| 文档 | 用途 | 何时阅读 |
|------|------|---------|
| README.md | 模块概述和架构 | 第一次接触模块时 |
| plan.md | 开发计划 | 开始新任务前 |
| doc/CONTRACT.md | 接口契约 | 调用模块或修改接口时 |
| doc/TEST_PLAN.md | 测试计划 | 编写测试用例时 |
| doc/RUNBOOK.md | 运维手册 | 部署或故障排查时 |
| doc/BUGS.md | 缺陷管理 | 遇到问题或复盘时 |
| doc/PROGRESS.md | 进度跟踪 | 了解里程碑时 |
| doc/CHANGELOG.md | 变更历史 | 查看版本历史时 |

---

## 6. 注意事项

### ⚠️ 重要约束

1. **测试覆盖率**: 不低于80%，否则CI会失败
2. **接口兼容性**: 所有变更必须向后兼容
3. **性能基线**: 响应时间不超过500ms（P95）
4. **文档同步**: 代码变更必须同步更新CONTRACT.md

### 💡 最佳实践

1. **增量开发**: 每次改动尽量小，便于review
2. **测试先行**: 先写测试，再写实现
3. **及时更新文档**: 代码和文档同步更新
4. **使用配置**: 避免硬编码，使用config/

---

## 7. 联系方式

**维护团队**: AI-TEMPLATE维护团队

**问题反馈**:
- 提交Issue到项目仓库
- 或在 `doc/BUGS.md` 中记录

**参考资源**:
- 项目文档: `/doc/`
- 模块指南: `/doc/modules/MODULE_INIT_GUIDE.md`
- 模块类型: `/doc/modules/MODULE_TYPES.md`

---

**最后更新**: 2025-11-07
**版本**: 1.0.0

