# 测试目录（Tests）

## 目标
组织和管理所有测试代码，确保代码质量和功能正确性。

## 适用场景
- 单元测试：测试单个函数/类
- 集成测试：测试模块间交互
- 端到端测试：测试完整用户流程

## 前置条件
- 已安装测试依赖（`pip install -r requirements.txt`）
- 了解测试金字塔理念
- 熟悉所用测试框架（pytest/Vitest/Go testing）

---

## 目录结构

```
tests/
├── README.md           # 本文件
├── conftest.py         # Pytest 全局配置（Python 项目）
├── <module>/           # 模块测试
│   ├── __init__.py
│   ├── test_unit.py        # 单元测试
│   ├── test_integration.py # 集成测试
│   ├── test_smoke.py       # 冒烟测试
│   └── conftest.py         # 模块级 fixtures
└── e2e/                # 端到端测试（可选）
```

## 测试类型

### 单元测试（Unit Tests）
- **目的**：测试单个函数/类/组件
- **特点**：快速、独立、无外部依赖
- **文件**：`test_unit.py` 或 `*_test.go`
- **运行**：应该在 1 秒内完成

### 集成测试（Integration Tests）
- **目的**：测试模块间交互
- **特点**：可能依赖数据库/缓存/外部服务（需 Mock）
- **文件**：`test_integration.py`
- **运行**：可能需要几秒到几分钟

### 冒烟测试（Smoke Tests）
- **目的**：快速验证核心功能
- **特点**：覆盖主要路径，快速反馈
- **文件**：`test_smoke.py`
- **运行**：每次提交必跑

### 端到端测试（E2E Tests）
- **目的**：测试完整用户流程
- **特点**：真实环境、完整流程
- **文件**：`e2e/`
- **运行**：发布前运行

## 测试命令

### Python (pytest)
```bash
# 运行所有测试
pytest tests/

# 运行特定模块
pytest tests/example/

# 运行特定文件
pytest tests/example/test_smoke.py

# 运行特定测试
pytest tests/example/test_smoke.py::test_module_imports

# 覆盖率报告
pytest --cov=modules --cov-report=html tests/

# 详细输出
pytest -v tests/

# 失败时详细信息
pytest -vv tests/

# 只运行失败的测试
pytest --lf tests/
```

### TypeScript/Vue (Vitest)
```bash
# 运行所有测试
npm run test

# 运行单元测试
npm run test:unit

# 运行特定文件
npm run test -- Button.spec.ts

# 覆盖率
npm run test:coverage

# 监听模式
npm run test -- --watch
```

### Go (testing)
```bash
# 运行所有测试
go test ./...

# 运行特定包
go test ./tests/example/

# 详细输出
go test -v ./tests/example/

# 覆盖率
go test -cover ./tests/example/

# 生成覆盖率报告
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# 竞态检测
go test -race ./...

# 基准测试
go test -bench=. ./tests/example/
```

## 测试覆盖率要求

根据 `agent.md` §6 测试准则：

### Python
- 核心模块：≥80%
- 工具函数：≥90%
- 边界情况：必须覆盖

### Vue/TypeScript
- 组件：≥75%
- 工具函数：≥90%
- 关键业务逻辑：100%

### Go
- 核心包：≥80%
- 公共 API：≥90%
- 并发代码：必须有竞态检测

## 测试最佳实践

### 1. 测试独立性
```python
# ❌ 错误：测试依赖顺序
def test_step1():
    global user
    user = create_user()

def test_step2():
    # 依赖 test_step1 的结果
    update_user(user)

# ✅ 正确：每个测试独立
def test_create_user():
    user = create_user()
    assert user is not None

def test_update_user():
    user = create_user()  # 自己准备数据
    updated = update_user(user)
    assert updated
```

### 2. 使用 Fixtures
```python
# ✅ 推荐：使用 fixtures 管理测试数据
@pytest.fixture
def user():
    return create_test_user()

def test_update_user(user):
    updated = update_user(user)
    assert updated.version == user.version + 1
```

### 3. Mock 外部依赖
```python
# ✅ 推荐：Mock 外部 API
from unittest.mock import patch

def test_fetch_data():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"data": "test"}
        result = fetch_external_data()
        assert result["data"] == "test"
```

### 4. 参数化测试
```python
# ✅ 推荐：使用参数化避免重复
@pytest.mark.parametrize("input,expected", [
    ("test@example.com", True),
    ("invalid", False),
    ("", False),
])
def test_validate_email(input, expected):
    assert validate_email(input) == expected
```

### 5. 测试命名清晰
```python
# ❌ 不清晰
def test_1():
    pass

# ✅ 清晰：描述测试场景和期望
def test_create_user_with_valid_email_should_succeed():
    pass

def test_create_user_with_duplicate_email_should_raise_error():
    pass
```

## 示例参考

- **Python 示例**：`tests/example/test_smoke.py`
- **TypeScript 示例**：`tests/example/Button.spec.ts`
- **Go 示例**：`tests/example/user_test.go`

详细测试指南参见 `agent.md` §6 测试准则。

## CI 集成

测试会在以下时机自动运行：
- 每次 git push
- 创建/更新 PR 时
- 合并到 main 前
- 定时任务（每日）

配置文件：`.github/workflows/ci.yml`

## 性能测试与数学指标

### 响应时间要求

使用数学符号明确表示性能要求：

**延迟要求**（以毫秒为单位）:
- 百分位延迟 P50: $t_{50} < 1000$ ms
- 百分位延迟 P95: $t_{95} < 2000$ ms  
- 百分位延迟 P99: $t_{99} < 3000$ ms

**计算公式**：
$$
P_{95} = \inf\{x \in \mathbb{R} : F(x) \geq 0.95\}
$$

其中 $F(x)$ 是累积分布函数（CDF）。

### 吞吐量要求

**QPS（每秒查询数）**:
$$
QPS = \frac{N_{total}}{T_{duration}}
$$

其中：
- $N_{total}$ = 总请求数
- $T_{duration}$ = 测试持续时间（秒）

**目标**: $QPS \geq 100$

### 并发测试

**并发用户数与错误率关系**：

| 并发数 $C$ | 错误率 $E$ | 要求 |
|-----------|-----------|------|
| $C = 10$ | $E < 0.1\%$ | 几乎无错误 |
| $C = 50$ | $E < 1\%$ | 可接受 |
| $C = 100$ | $E < 5\%$ | 最大容忍 |

---

## 故障排查

### 测试失败怎么办？

按照以下顺序排查：

1. **首先**，查看错误信息和堆栈跟踪
   ```bash
   pytest -vv --tb=long
   ```

2. **然后**，使用详细输出模式
   ```bash
   pytest -vv tests/example/test_specific.py
   ```

3. **接着**，单独运行失败的测试
   ```bash
   pytest --lf  # Last Failed
   ```

4. **随后**，检查测试数据和Mock配置
   - 验证 fixtures 是否正确
   - 检查 Mock 返回值

5. **最后**，使用调试器定位问题
   ```bash
   # Python
   pytest --pdb
   
   # 或
   python -m pdb -m pytest tests/example/test_specific.py
   ```

### 覆盖率不达标？

系统化提升覆盖率：

1. **生成覆盖率报告**
   ```bash
   pytest --cov=modules --cov-report=html tests/
   # 打开 htmlcov/index.html
   ```

2. **识别未覆盖代码**
   - 查看红色标记的代码行
   - 分析为何未覆盖

3. **补充测试**
   - 边界条件测试
   - 错误场景测试
   - 异常路径测试

4. **清理无用代码**
   - 删除不可达代码
   - 移除废弃功能

---

## 相关文档
- 测试规范：`agent.md` §6
- 测试计划：`modules/*/TEST_PLAN.md`
- CI 配置：`.github/workflows/ci.yml`

---

**最后更新**: 2025-11-05  
**维护者**: [填写维护者]


