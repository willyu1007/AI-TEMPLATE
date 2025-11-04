# TEST_PLAN - 测试计划

## 关键路径用例
1. **正常流程 - 基础任务处理**
   - 输入：`{"task": "示例任务", "language": "python"}`
   - 期望输出：`{"status": "success", "result": "..."}`
   - 验证点：响应格式正确、状态为 success

2. **参数验证 - 缺少必填字段**
   - 输入：`{}`（缺少 task）
   - 期望输出：`{"status": "error", "error_code": "E001"}`
   - 验证点：错误码正确、错误信息清晰

3. **可选参数 - dry_run 模式**
   - 输入：`{"task": "示例任务", "dry_run": true}`
   - 期望输出：预览结果，不执行实际操作
   - 验证点：dry_run 模式正确生效

## 契约测试
- 输入验证：必填字段检查、类型检查
- 输出格式验证：字段完整性、类型正确性
- 错误码测试：所有错误码可触发并返回正确

## 边界测试
- 空值：`task` 为空字符串
- 极端值：超长 `task` 字符串（>10000字符）
- 非法值：`language` 为不支持的语言
- 并发：多个请求同时处理

## 性能测试
- 响应时间：P95 < 2000ms（见 `flows/dag.yaml` SLA）
- 并发处理：支持 10+ 并发请求

## 回归测试
每次变更必须运行：
1. 所有契约测试
2. 关键路径用例
3. 边界测试的子集

## 测试执行
```bash
# 运行所有测试
pytest tests/example/

# 运行特定测试
pytest tests/example/test_smoke.py

# 覆盖率报告
pytest --cov=example tests/example/
```
