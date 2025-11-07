# 测试准则

> **用途**: 定义项目的测试策略和规范
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## 测试策略

### 测试金字塔

```
        /\
       /E2\      10% - 端到端测试
      /----\
     /Integ\     20% - 集成测试
    /------\
   / Unit  \     70% - 单元测试
  /----------\
```

### 覆盖率要求

- **默认要求**: ≥80%
- **核心模块**: ≥90%
- **工具函数**: ≥95%

模块可在`agent.md`中设置更高要求：
```yaml
quality_gates:
  coverage_min: 0.90  # 90%
```

---

## 测试类型

### 1. 单元测试（Unit Tests）

**目标**: 测试单个函数/类的行为

**适用**: 
- 所有业务逻辑（core/）
- 所有工具函数（utils/）
- 所有数据模型（models/）

**示例**（Python）:
```python
def test_create_user_success():
    """测试成功创建用户"""
    service = UserService()
    data = {"username": "test", "email": "test@example.com"}
    result = await service.create_user(data)
    assert result["id"] is not None
    assert result["username"] == "test"
```

**示例**（Go）:
```go
func TestCreateUserSuccess(t *testing.T) {
    service := NewUserService()
    data := &UserData{Username: "test", Email: "test@example.com"}
    result, err := service.CreateUser(context.Background(), data)
    assert.NoError(t, err)
    assert.NotNil(t, result.ID)
}
```

---

### 2. 集成测试（Integration Tests）

**目标**: 测试模块间交互

**适用**:
- API接口（api/）
- 数据库操作
- 第三方服务集成

**示例**（Python）:
```python
def test_api_create_user(client):
    """测试创建用户API"""
    response = client.post("/api/users/", json={
        "username": "test",
        "email": "test@example.com"
    })
    assert response.status_code == 201
    assert "id" in response.json()
```

---

### 3. 契约测试（Contract Tests）

**目标**: 验证API符合CONTRACT.md

**适用**:
- 所有对外API
- 模块间接口

**示例**:
```python
def test_contract_compatibility():
    """测试API契约兼容性"""
    contract = load_contract("modules/user/doc/CONTRACT.md")
    response = client.post("/api/users/", json=contract["create_request"])
    validate_schema(response.json(), contract["create_response"])
```

---

### 4. 端到端测试（E2E Tests）

**目标**: 测试完整业务流程

**适用**:
- 关键业务流程
- 跨模块交互

**示例**:
```python
@pytest.mark.e2e
def test_user_registration_flow(browser):
    """测试用户注册完整流程"""
    # 1. 访问注册页
    browser.visit("/register")
    # 2. 填写表单
    browser.fill("username", "testuser")
    browser.fill("email", "test@example.com")
    browser.click("submit")
    # 3. 验证成功
    assert browser.is_text_present("注册成功")
```

---

## 多语言测试规范

### Python (pytest)

#### 配置
```python
# conftest.py
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def cleanup():
    """每个测试后清理数据"""
    yield
    db.session.rollback()
```

#### 运行
```bash
# 所有测试
pytest tests/

# 单元测试
pytest tests/ -m unit

# 生成覆盖率
pytest tests/ --cov=modules --cov-report=html
```

---

### Go (testing)

#### 配置
```go
// setup_test.go
func TestMain(m *testing.M) {
    setup()
    code := m.Run()
    teardown()
    os.Exit(code)
}
```

#### 运行
```bash
# 所有测试
go test ./...

# 生成覆盖率
go test -cover ./...

# 详细覆盖率报告
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

---

### TypeScript (Jest/Vitest)

#### 配置
```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      lines: 80,
    },
  },
});
```

#### 运行
```bash
# 所有测试
npm test

# 生成覆盖率
npm test -- --coverage
```

---

## 测试最佳实践

### 1. 测试命名
- Python: `test_<function>_<scenario>`
- Go: `Test<Function><Scenario>`
- TypeScript: `describe('<Function>', () => { it('should <scenario>', ...) })`

### 2. AAA模式
```python
def test_example():
    # Arrange - 准备测试数据
    service = MyService()
    data = {"key": "value"}
    
    # Act - 执行操作
    result = service.do_something(data)
    
    # Assert - 验证结果
    assert result == expected
```

### 3. 独立性
- 测试间不互相依赖
- 每个测试可单独运行
- 使用fixtures/setup管理测试数据

### 4. 可读性
- 测试名称清晰说明测试内容
- 一个测试只验证一个场景
- 添加必要的注释

---

## 质量门槛

### 必需的测试类型
```yaml
quality_gates:
  required_tests:
    - unit           # 单元测试（必需）
    - integration    # 集成测试（必需）
    - contract       # 契约测试（建议）
```

### 阻断发布条件
- ❌ 测试覆盖率 < 80%
- ❌ 有失败的测试用例
- ❌ 有未修复的Critical Bug

---

## 测试数据管理

### Fixtures
- 使用fixtures管理测试数据
- 测试后自动清理
- 避免硬编码

### 测试数据库
- 使用独立的测试数据库
- 每个测试使用事务回滚
- 或使用in-memory数据库

---

## CI集成

### 自动运行
```yaml
# .github/workflows/test.yml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest tests/ --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

### 门禁检查
```bash
make dev_check  # 包含测试检查
```

---

## 相关文档

- **测试计划模板**: doc/modules/TEMPLATES/TEST_PLAN.md.template
- **质量门槛**: doc/policies/safety.md
- **检查命令**: doc/reference/commands.md

---

**维护**: 测试策略变更时更新

