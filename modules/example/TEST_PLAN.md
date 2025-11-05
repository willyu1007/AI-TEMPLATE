# 测试计划（Test Plan）

## 目标
定义完整的测试策略，确保模块功能正确、性能达标、边界安全。

## 适用场景
- 功能开发完成后
- 代码变更前的回归测试
- 发布前的质量验证

## 前置条件
- 代码已实现（或有可测试的原型）
- 测试环境已准备
- 测试数据已准备

---

## 测试策略

### 测试金字塔
```
     /\
    /E2E\        10% - 端到端测试
   /------\
  /集成测试\     20% - 模块间交互
 /----------\
/  单元测试  \   70% - 函数/类级别
```

### 覆盖率要求
- **单元测试**：≥ 80%
- **集成测试**：覆盖所有关键交互
- **E2E 测试**：覆盖核心用户流程

---

## 测试用例清单

### 1. 单元测试

#### 1.1 正常流程测试
**用例ID**: TC001  
**描述**: 基础任务处理 - 成功场景  
**前置条件**: 服务正常运行  
**输入**:
```
{
  "task": "示例任务",
  "language": "python"
}
```
**预期输出**:
```
{
  "status": "success",
  "result": "...",
  "metadata": {"duration_ms": <number>, "version": "1.0.0"}
}
```
**验证点**:
- [ ] 响应格式正确
- [ ] `status` 为 `success`
- [ ] `result` 非空
- [ ] `metadata.version` 正确

---

#### 1.2 参数验证测试
**用例ID**: TC002  
**描述**: 缺少必填字段  
**输入**:
```
{}
```
**预期输出**:
```
{
  "status": "error",
  "error_code": "E001",
  "result": "参数 task 不能为空"
}
```
**验证点**:
- [ ] 错误码为 `E001`
- [ ] 错误信息清晰
- [ ] HTTP 状态码为 400

---

#### 1.3 可选参数测试
**用例ID**: TC003  
**描述**: dry_run 模式验证  
**输入**:
```
{
  "task": "示例任务",
  "dry_run": true
}
```
**预期输出**:
```
{
  "status": "success",
  "result": "预览：...(未执行)",
  "metadata": {...}
}
```
**验证点**:
- [ ] 返回预览结果
- [ ] 未执行实际操作
- [ ] 响应时间 < 500ms

---

### 2. 边界测试

#### 2.1 空值测试
- [ ] `task` 为空字符串 → 返回 E001
- [ ] `task` 为 null → 返回 E001  
- [ ] `language` 为空 → 使用默认值 "python"

#### 2.2 极端值测试
- [ ] `task` 长度 = 1 字符 → 成功处理
- [ ] `task` 长度 = 10000 字符 → 成功处理
- [ ] `task` 长度 > 10000 字符 → 返回 E001

#### 2.3 非法值测试
- [ ] `language` 为不支持的值 → 返回 E001
- [ ] `dry_run` 为非布尔值 → 返回 E001

---

### 3. 性能测试

#### 3.1 响应时间测试
**目标**: P95 < 2000ms（见 `flows/dag.yaml`）

**测试方法**:
```
# 使用 Apache Bench
ab -n 1000 -c 10 -T 'application/json' \
   -p request.json \
   http://localhost:8000/api/example
```

**验证点**:
- [ ] P50 < 1000ms
- [ ] P95 < 2000ms
- [ ] P99 < 3000ms

## 3.2 并发测试
**目标**: 支持 10+ 并发请求

**测试方法**:
```
# 并发测试
pytest tests/example/test_performance.py::test_concurrent_requests
```

**验证点**:
- [ ] 10 并发无错误
- [ ] 50 并发错误率 < 1%
- [ ] 100 并发错误率 < 5%

---

## 4. 集成测试

#### 4.1 契约测试
- [ ] 输入验证：必填字段检查
- [ ] 输入验证：类型检查
- [ ] 输出格式验证：字段完整性
- [ ] 输出格式验证：类型正确性
- [ ] 错误码测试：所有错误码可触发

#### 4.2 依赖测试
- [ ] 与 codegen 工具集成
- [ ] 配置加载正确
- [ ] 日志记录正常

---

### 5. 回归测试

每次代码变更必须运行：

**快速回归**（< 5 分钟）:
```
pytest tests/example/test_smoke.py -v
```

**完整回归**（< 30 分钟）:
```
pytest tests/example/ -v --cov=example
```

**验证点**:
- [ ] 所有契约测试通过
- [ ] 关键路径用例通过
- [ ] 边界测试通过
- [ ] 测试覆盖率 ≥ 80%

---

## 测试执行

### 本地执行
```
# 1. 运行所有测试
pytest tests/example/ -v

# 2. 运行特定类型
pytest tests/example/test_unit.py       # 单元测试
pytest tests/example/test_integration.py # 集成测试
pytest tests/example/test_smoke.py      # 冒烟测试

# 3. 生成覆盖率报告
pytest --cov=example --cov-report=html tests/example/
# 查看报告：htmlcov/index.html

# 4. 性能测试
pytest tests/example/test_performance.py -v
```

## CI 执行
```
# .github/workflows/ci.yml
- name: Test example module
  run: |
    pytest tests/example/ \
      --cov=example \
      --cov-fail-under=80 \
      --junit-xml=test-results.xml
```

---

## 验证步骤

### 测试前验证
```
# 1. 环境准备
export APP_ENV=test
pip install -r requirements.txt

# 2. 数据准备（如需要）
python scripts/setup_test_data.py

# 3. 服务启动
docker-compose up -d
```

## 测试中验证
```
# 1. 运行测试并监控
pytest tests/example/ -v --tb=short

# 2. 检查覆盖率
pytest --cov=example tests/example/
# 确保 ≥ 80%

# 3. 检查性能
pytest tests/example/test_performance.py -v
# 确保 P95 < 2000ms
```

## 测试后验证
```
# 1. 清理测试数据
python scripts/cleanup_test_data.py

# 2. 检查测试报告
cat test-results.xml

# 3. 验证无副作用
docker-compose down
```

---

## 回滚逻辑

如果测试发现严重问题：

### 1. 停止发布
```
# 标记为阻塞
git tag -a v1.0.0-blocked -m "Tests failed, blocking release"

# 通知团队
# 发送通知邮件或消息
```

## 2. 分析问题
```
# 查看失败的测试
pytest tests/example/ -v --lf  # 只运行失败的测试

# 查看详细日志
pytest tests/example/ -vv --tb=long
```

## 3. 决策
- **问题可快速修复**：修复后重新测试
- **问题复杂**：回滚代码到上一版本

### 4. 回滚测试
```
# 回滚到上一版本
git checkout <previous-tag>

# 重新运行测试
pytest tests/example/ -v

# 确认问题解决
```

---

## 测试数据管理

### 测试数据原则
1. **独立性**：每个测试使用独立的数据
2. **可重复性**：测试结果可复现
3. **清理**：测试后清理数据

### 测试夹具（Fixtures）
```
# tests/example/conftest.py
import pytest

@pytest.fixture
def sample_request():
    """示例请求数据"""
    return {
        "task": "测试任务",
        "language": "python"
    }

@pytest.fixture
def mock_database(monkeypatch):
    """Mock 数据库连接"""
    # Mock 实现
    pass
```

---

---

## 人工测试跟踪

### 目标
跟踪需要人工验证的功能状态，确保部分完成的功能得到及时测试和验证。

### 待测试功能清单

| 功能 | 状态 | 测试人员 | 测试日期 | 测试结果 | 备注 |
|------|------|---------|---------|---------|------|
| 用户登录 | 待测试 | - | - | - | 需要验证 OAuth 流程 |
| 数据导出 | 待测试 | - | - | - | 需要验证 CSV 和 Excel 格式 |
| API 性能 | 待测试 | - | - | - | 需要验证 P95 延迟是否达标 |

### 测试状态说明

- **待测试**: 功能已完成，等待人工测试
- **测试中**: 正在进行人工测试
- **已通过**: 测试通过，可以发布
- **已失败**: 测试失败，需要修复
- **已跳过**: 暂不测试（需说明原因）

### 测试结果记录

#### 测试记录模板
```
#### YYYY-MM-DD - [功能名称]测试
- **测试人员**: [姓名]
- **测试环境**: [开发/测试/生产]
- **测试结果**: ✅ 通过 / ❌ 失败 / ⚠️ 部分通过
- **发现问题**: [问题描述，无则填写"无"]
- **备注**: [其他说明]
```

### 维护要求

1. **AI 开发完成后**: 必须更新此表格，标记需要人工测试的功能。
2. **测试完成后**: 更新测试状态、测试人员和测试日期。
3. **定期审查**: 每周审查一次，确保待测试功能得到及时处理。
4. **状态更新**: 使用 `make test_status_check` 检查跟踪状态。

### 验证步骤

```bash
# 检查人工测试跟踪状态
make test_status_check

# 预期输出：
# ✓ 所有模块都包含人工测试跟踪章节
# ⚠️  共有 X 个功能等待人工测试
```

---

## 相关文档
- **接口契约**：`CONTRACT.md`
- **模块架构**：`README.md`
- **运维手册**：`RUNBOOK.md`
- **测试规范**：`agent.md` §6
- **AI 自动化审计**：`docs/project/AI_AUTOMATION_AUDIT.md`

