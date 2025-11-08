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

---

## AI辅助测试策略

> **适用场景**: AI深度参与的项目开发  
> **核心理念**: AI生成代码 + 自动化验证 + 最小化人工测试

### AI驱动测试流程

```
传统流程:
  手工编写代码 → 手工编写测试 → 手工执行测试 → 手工回归测试

AI辅助流程:
  AI生成代码 → AI生成测试 → 自动化执行 → 自动化回归
       ↓             ↓            ↓           ↓
    人工审核     人工审核     CI自动运行    契约保证兼容
```

---

### 1. AI生成测试用例

**使用场景**：
- 为新功能快速生成测试框架
- 补充边界情况测试
- 生成性能测试场景

**AI提示词示例**：
```
为以下函数生成完整测试用例，包括：
1. 正常场景（至少3个）
2. 边界情况（空值、极大值、极小值）
3. 异常场景（无效输入、权限不足）
4. 使用AAA模式（Arrange-Act-Assert）

函数签名：
def create_order(user_id: str, items: List[Item], discount: Optional[float]) -> Order:
    """创建订单"""
    pass
```

**人工审核要点**：
- ✅ 验证测试覆盖度是否完整
- ✅ 检查边界情况是否遗漏
- ✅ 确认业务规则理解正确
- ✅ 验证测试数据是否合理

---

### 2. 契约驱动开发（Contract-First）

**推荐流程**：
```
1. 先定义CONTRACT.md（人工或AI辅助）
   - 明确输入输出格式
   - 定义错误码
   - 说明业务规则

2. AI根据CONTRACT生成代码
   - 接口实现
   - 数据验证
   - 错误处理

3. 自动化契约测试验证
   - make contract_compat_check
   - 保证实现符合契约
   - 防止破坏性变更
```

**优势**：
- 清晰的接口定义
- 自动化兼容性验证
- 减少沟通成本
- AI理解更准确

---

### 3. 自动化检查取代手工QA

**核心检查（15个）**：
```bash
make dev_check
  ├─ docgen                    # 文档索引生成
  ├─ doc_style_check           # 文档风格检查
  ├─ agent_lint               # Agent配置校验
  ├─ registry_check           # 模块注册表校验
  ├─ doc_route_check          # 文档路由验证
  ├─ type_contract_check      # 类型契约校验
  ├─ doc_script_sync_check    # 文档脚本同步
  ├─ db_lint                  # 数据库文件校验
  ├─ dag_check                # DAG检查
  ├─ contract_compat_check    # 契约兼容性
  ├─ deps_check               # 依赖检查
  ├─ runtime_config_check     # 配置验证
  ├─ migrate_check            # 迁移脚本检查
  ├─ consistency_check        # 一致性验证
  └─ frontend_types_check     # 前端类型检查
```

**CI集成**：
```yaml
# .github/workflows/ci.yml
on: [push, pull_request]
jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run dev_check
        run: make dev_check
      - name: Run tests
        run: make test
      - name: Check coverage
        run: |
          pytest tests/ --cov --cov-report=xml
          # 覆盖率 < 80% 失败
```

---

### 4. AI代码的特殊测试关注点

#### 关注点1：幻觉问题
```python
# AI可能生成看似正确但有bug的代码
def calculate_discount(price, discount_percent):
    # ❌ AI可能忘记边界验证
    return price * (1 - discount_percent / 100)

# ✅ 测试应该覆盖边界
def test_discount_boundary():
    """测试边界情况"""
    # 负数
    with pytest.raises(ValueError):
        calculate_discount(100, -10)
    
    # 超过100%
    with pytest.raises(ValueError):
        calculate_discount(100, 150)
    
    # 0折扣
    assert calculate_discount(100, 0) == 100
```

#### 关注点2：业务逻辑理解偏差
```python
# 业务规则可能有隐含条件
# 测试需要明确所有条件

def test_vip_discount_complete():
    """
    VIP折扣规则（完整版）：
    1. 必须是VIP用户
    2. 订单金额 > 1000
    3. 非促销期
    4. 账户状态正常
    """
    # 所有条件满足
    assert calculate_vip_discount(
        user=vip_user,
        amount=1500,
        is_promotion=False,
        account_status="active"
    ) == 0.95
    
    # 任一条件不满足都应该无折扣
    assert calculate_vip_discount(
        user=vip_user,
        amount=500,  # < 1000
        is_promotion=False,
        account_status="active"
    ) == 1.0
```

#### 关注点3：边缘情况遗漏
```python
# AI倾向于考虑正常情况，测试需要补充边缘情况

def test_edge_cases():
    """测试边缘情况"""
    # 空输入
    assert process_data(None) == default_value
    assert process_data([]) == default_value
    assert process_data("") == default_value
    
    # 极大值
    assert process_data("x" * 10000) raises ValidationError
    
    # 特殊字符
    assert process_data("!@#$%^&*()") is handled
    
    # Unicode
    assert process_data("你好🌍") is handled
```

---

### 5. 测试即文档

**理念**：测试用例是最准确的业务规则文档

```python
def test_order_creation_rules():
    """
    订单创建规则：
    1. 用户必须已登录
    2. 购物车不能为空
    3. 商品库存充足
    4. 用户地址信息完整
    5. 支付金额 = 商品总价 - 折扣 + 运费
    """
    # 每个规则都有明确的测试
    
    # 规则1: 未登录用户
    with pytest.raises(AuthenticationError):
        create_order(user=anonymous_user, items=items)
    
    # 规则2: 空购物车
    with pytest.raises(ValidationError, match="购物车为空"):
        create_order(user=logged_in_user, items=[])
    
    # 规则3: 库存不足
    with pytest.raises(StockError):
        create_order(user=logged_in_user, items=[out_of_stock_item])
    
    # ... 更多测试
```

**优势**：
- 新成员通过阅读测试理解业务
- 测试失败时立即知道哪个业务规则被破坏
- 重构时测试保证行为不变

---

### 6. Mock数据管理

**生成Mock数据**：
```bash
# 使用AI-TEMPLATE提供的工具
make generate_mock MODULE=user TABLE=users COUNT=1000

# 生成后自动注册到生命周期管理
# 测试完成后自动清理
make cleanup_mocks
```

**Mock数据配置**（TEST_DATA.md）：
```yaml
mock_rules:
  users:
    count: 1000
    fields:
      - name: username
        type: faker.user_name
      - name: email
        type: faker.email
      - name: age
        type: random.randint
        min: 18
        max: 80
      - name: created_at
        type: faker.date_time_between
        start_date: "-1y"
        end_date: "now"
```

---

### 7. 最佳实践总结

#### ✅ 推荐做法

1. **契约先行**：先写CONTRACT.md，再让AI生成代码
2. **AI生成 + 人工审核**：AI生成测试后必须人工审核
3. **自动化优先**：优先使用自动化检查，最小化手工测试
4. **测试即文档**：测试用例就是业务规则的最准确描述
5. **CI强制执行**：所有检查在CI中自动运行，失败阻断合并

#### ❌ 避免做法

1. **盲目信任AI**：AI生成的代码和测试都需要审核
2. **忽略边界情况**：手工补充AI遗漏的边界测试
3. **跳过自动化检查**：不要因为"只是小改动"就跳过检查
4. **过度依赖手工测试**：手工测试应该是最小化的
5. **忽略测试覆盖率**：严格执行80%覆盖率要求

---

### 8. AI测试工具链

```bash
# 完整的测试工作流
make dev_check              # 开发时运行（警告模式）
make test                   # 执行所有测试
make contract_compat_check  # 检查兼容性
make rollback_check         # 验证回滚

# CI自动运行（严格模式）
make validate              # 聚合验证（7个检查）
# 任何失败都阻断合并
```

---

## 相关文档

- **测试计划模板**: doc/modules/TEMPLATES/TEST_PLAN.md.template
- **质量门槛**: doc/policies/safety.md
- **质量标准**: doc/policies/quality_standards.md
- **检查命令**: doc/reference/commands.md
- **发布流程**: doc/project/RELEASE_TRAIN.md

---

**维护**: 测试策略变更时更新

