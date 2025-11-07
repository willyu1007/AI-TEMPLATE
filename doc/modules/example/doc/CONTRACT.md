# 接口契约（Contract）

## 目标
定义模块的输入输出规范，确保接口稳定性和向后兼容性。

## 适用场景
- 模块间调用
- 第三方集成
- API 版本管理

## 前置条件
- 模块职责已明确（见 `README.md`）
- 数据流已规划（见 `flows/dag.yaml`）

---

## 接口规范

### 1. 输入参数

#### 请求格式
```
{
  "task": "string - 任务描述",
  "language": "string - 目标语言（可选）",
  "dry_run": "boolean - 是否为演练模式（默认: false）"
}
```

#### 字段说明
| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `task` | string | 是 | - | 任务描述，长度 1-10000 字符 |
| `language` | string | 否 | "python" | 目标语言（python/javascript/go）|
| `dry_run` | boolean | 否 | false | 演练模式，不执行实际操作 |

#### 验证规则
- `task` 不能为空
- `task` 长度必须在 1-10000 字符之间
- `language` 必须是支持的语言之一
- `dry_run` 必须是布尔值

---

### 2. 输出格式

#### 成功响应
```
{
  "result": "string - 处理结果",
  "status": "success",
  "metadata": {
    "duration_ms": "number - 处理时长",
    "version": "string - 版本号"
  }
}
```

#### 失败响应
```
{
  "result": "string - 错误信息",
  "status": "error",
  "error_code": "string - 错误代码",
  "metadata": {
    "duration_ms": "number - 处理时长",
    "version": "string - 版本号"
  }
}
```

---

### 3. 错误码定义

| 错误码 | 含义 | HTTP 状态码 | 处理建议 |
|--------|------|------------|---------|
| `E001` | 参数验证失败 | 400 | 检查请求参数 |
| `E002` | 处理超时 | 504 | 减少任务复杂度或重试 |
| `E003` | 内部错误 | 500 | 联系技术支持 |
| `E004` | 资源不足 | 503 | 稍后重试 |

---

## 兼容性策略

### 向后兼容原则
1. **不删除现有字段**：废弃字段标记为 `@deprecated`
2. **不改变字段类型**：如需改变，创建新字段
3. **不改变字段语义**：如需改变，升级 major 版本。
4. **新增可选字段**：必须提供默认值

### 版本管理
- 遵循语义化版本（Semver）：`MAJOR.MINOR.PATCH`
- **PATCH**：Bug 修复，完全向后兼容
- **MINOR**：新增功能，向后兼容
- **MAJOR**：破坏性变更，不向后兼容

### 破坏性变更处理
如需引入破坏性变更：
1. 创建新的 major 版本（如 `v2`）
2. 保留旧版本至少一个发布周期
3. 提供迁移指南
4. 在文档中明确标注废弃时间

---

## 调用示例

### 示例 1：基础调用
```
curl -X POST http://localhost:8000/api/example \
  -H "Content-Type: application/json" \
  -d '{
    "task": "实现用户登录功能",
    "language": "python"
  }'
```

**预期响应**：
```
{
  "result": "登录功能实现完成",
  "status": "success",
  "metadata": {
    "duration_ms": 1250,
    "version": "1.0.0"
  }
}
```

### 示例 2：演练模式
```
curl -X POST http://localhost:8000/api/example \
  -H "Content-Type: application/json" \
  -d '{
    "task": "生成数据模型",
    "language": "go",
    "dry_run": true
  }'
```

**预期响应**：
```
{
  "result": "预览：将生成 User 模型（未执行）",
  "status": "success",
  "metadata": {
    "duration_ms": 150,
    "version": "1.0.0"
  }
}
```

### 示例 3：错误处理
```
curl -X POST http://localhost:8000/api/example \
  -H "Content-Type: application/json" \
  -d '{}'
```

**预期响应**：
```
{
  "result": "参数 task 不能为空",
  "status": "error",
  "error_code": "E001",
  "metadata": {
    "duration_ms": 5,
    "version": "1.0.0"
  }
}
```

---

## 验证步骤

### 1. 契约测试
```
# 运行契约测试
pytest tests/example/test_contract.py -v

# 验证所有字段类型
pytest tests/example/test_contract.py::test_response_schema
```

## 2. 兼容性检查
```
# 检查与基线的兼容性
make contract_compat_check

# 预期输出：无破坏性变更
```

## 3. 集成测试
```
# 测试真实调用
pytest tests/example/test_integration.py -v
```

---

## 回滚逻辑

如果接口变更导致问题：

### 1. 识别影响范围
```
# 查看哪些模块依赖此接口
grep -r "example" flows/dag.yaml

# 检查调用方
grep -r "api/example" modules/
```

## 2. 回滚契约
```
# 恢复到上一版本
git checkout <previous-tag> -- modules/example/CONTRACT.md
git checkout <previous-tag> -- tools/example/contract.json

# 更新基线
make update_baselines
```

## 3. 通知下游
如果有其他模块依赖：
1. 通知相关团队
2. 提供迁移指导
3. 协助集成测试

### 4. 验证回滚
```
# 检查兼容性
make contract_compat_check

# 运行集成测试
pytest tests/integration/ -k example
```

---

## 变更历史

### v1.0.0 (2025-11-04)
- 初始版本
- 定义基础输入输出
- 添加 3 个核心错误码

---

## 相关文档
- **模块架构**：`README.md`
- **测试计划**：`TEST_PLAN.md`
- **项目 DAG**：`flows/dag.yaml`
- **契约规范**：`agent.md` §4

