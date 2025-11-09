# 测试计划（Test Plan）

## 目标
定义 common 模块的完整测试策略，确保基础库功能正确、性能达标、跨平台兼容。

## 适用场景
- 功能开发完成后
- 代码变更前的回归测试
- 发布前的质量验证

## 前置条件
- 代码已实现
- 测试环境已准备
- 测试数据已准备

---

## 测试策略

### 测试金字塔
```
     /\
    /E2E\        10% - 端到端测试（与其他模块集成）
   /------\
  /集成测试\     20% - 工具类交互
 /----------\
/  单元测试  \   70% - 函数/类级别
```

### 覆盖率要求
- **单元测试**：≥ 80%
- **集成测试**：覆盖所有关键交互
- **跨平台测试**：Windows、macOS、Linux

---

## 测试用例清单

### 1. 单元测试

#### 1.1 常量模块测试（constants）

**TC001 - 错误码常量**
- [ ] 验证所有错误码唯一
- [ ] 验证错误码格式正确（E001-E999）
- [ ] 验证错误消息非空

**TC002 - 状态常量**
- [ ] 验证状态值唯一
- [ ] 验证状态转换逻辑
- [ ] 验证状态枚举完整性

---

#### 1.2 工具类测试（utils）

**TC003 - 日期工具类（date_utils.py）**
```python
# 测试用例
def test_format_datetime():
    """测试日期格式化"""
    assert format_datetime(datetime(2025, 1, 1)) == "2025-01-01 00:00:00"

def test_parse_datetime():
    """测试日期解析"""
    dt = parse_datetime("2025-01-01 12:00:00")
    assert dt.year == 2025
    assert dt.month == 1

def test_timezone_conversion():
    """测试时区转换"""
    # UTC to Asia/Shanghai
    pass
```

**验证点**:
- [ ] 日期格式化正确
- [ ] 日期解析正确
- [ ] 时区转换准确
- [ ] 边界值处理（None、空字符串）

---

**TC004 - 加密工具类（encryption.py）**
```python
def test_encrypt_decrypt():
    """测试加密解密"""
    plaintext = "test data"
    encrypted = encrypt(plaintext)
    decrypted = decrypt(encrypted)
    assert decrypted == plaintext

def test_encrypt_unicode():
    """测试 Unicode 加密"""
    plaintext = "测试数据"
    encrypted = encrypt(plaintext)
    decrypted = decrypt(encrypted)
    assert decrypted == plaintext

def test_encrypt_empty():
    """测试空值加密"""
    with pytest.raises(ValueError):
        encrypt("")
```

**验证点**:
- [ ] 加密解密往返成功
- [ ] Unicode 字符正确处理
- [ ] 空值和 None 正确处理
- [ ] 加密结果不可读（非明文）

---

**TC005 - 字符串工具类（string_utils.py）**
- [ ] 字符串清理（去空格、特殊字符）
- [ ] 字符串验证（邮箱、手机号）
- [ ] 字符串转换（驼峰、下划线）
- [ ] Unicode 处理

---

**TC006 - 验证工具类（validation.py）**
- [ ] 数据类型验证
- [ ] 数值范围验证
- [ ] 字符串长度验证
- [ ] 自定义规则验证

---

#### 1.3 模型类测试（models）

**TC007 - 基础模型（base.py）**
- [ ] 模型创建和初始化
- [ ] 字段验证
- [ ] 序列化/反序列化
- [ ] __str__ 和 __repr__ 方法

---

#### 1.4 中间件测试（middleware）

**TC008 - 认证中间件（auth.py）**
```python
def test_auth_success():
    """测试认证成功"""
    token = "valid_token"
    result = authenticate(token)
    assert result.success is True

def test_auth_failure():
    """测试认证失败"""
    token = "invalid_token"
    result = authenticate(token)
    assert result.success is False
    assert result.error_code == "E401"
```

**验证点**:
- [ ] 有效 token 认证成功
- [ ] 无效 token 认证失败
- [ ] 过期 token 处理
- [ ] 空 token 处理

---

**TC009 - 日志中间件（logging.py）**
- [ ] 日志记录功能
- [ ] 日志级别控制
- [ ] 日志格式正确
- [ ] 性能影响 < 10ms

---

**TC010 - 限流中间件（rate_limit.py）**
- [ ] 限流阈值生效
- [ ] 超限返回 429
- [ ] 时间窗口正确
- [ ] 并发场景处理

---

### 2. 边界测试

#### 2.1 空值测试
- [ ] None 输入处理
- [ ] 空字符串处理
- [ ] 空列表/字典处理
- [ ] 0 值处理

#### 2.2 极端值测试
- [ ] 超长字符串（10000+ 字符）
- [ ] 超大数值（Int64 边界）
- [ ] 最小值测试

#### 2.3 非法值测试
- [ ] 错误类型输入
- [ ] 格式不正确的数据
- [ ] SQL 注入尝试
- [ ] XSS 攻击尝试

---

### 3. 性能测试

#### 3.1 响应时间测试
**目标**: 所有工具函数 P95 < 10ms

**测试方法**:
```python
def test_performance_encryption():
    """测试加密性能"""
    import time
    iterations = 1000
    start = time.time()
    for _ in range(iterations):
        encrypt("test data")
    elapsed = time.time() - start
    avg = elapsed / iterations
    assert avg < 0.01  # < 10ms
```

**验证点**:
- [ ] encrypt/decrypt < 10ms
- [ ] validation < 1ms
- [ ] date_utils < 1ms

---

#### 3.2 并发测试
**目标**: 支持 100+ 并发调用

**测试方法**:
```python
def test_concurrent_calls():
    """测试并发调用"""
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(encrypt, f"data{i}") for i in range(100)]
        results = [f.result() for f in futures]
    assert len(results) == 100
```

---

### 4. 跨平台测试

#### 4.1 编码测试
- [ ] Windows UTF-8 支持
- [ ] macOS UTF-8 支持
- [ ] Linux UTF-8 支持
- [ ] 中文字符处理

#### 4.2 路径测试
- [ ] Windows 路径分隔符（\）
- [ ] Unix 路径分隔符（/）
- [ ] 相对路径处理
- [ ] 绝对路径处理

---

### 5. 集成测试

#### 5.1 模块间交互
- [ ] 与其他模块的集成
- [ ] 中间件链调用
- [ ] 错误传播机制

#### 5.2 配置加载
- [ ] 开发环境配置
- [ ] 生产环境配置
- [ ] 环境变量覆盖

---

### 6. 回归测试

每次代码变更必须运行：

**快速回归**（< 2 分钟）:
```bash
pytest tests/common/test_smoke.py -v
```

**完整回归**（< 10 分钟）:
```bash
pytest tests/common/ -v --cov=modules/common
```

**验证点**:
- [ ] 所有单元测试通过
- [ ] 边界测试通过
- [ ] 测试覆盖率 ≥ 80%
- [ ] 性能测试通过

---

## 测试执行

### 本地执行
```bash
# 1. 运行所有测试
pytest tests/common/ -v

# 2. 运行特定类型
pytest tests/common/test_utils.py       # 工具类测试
pytest tests/common/test_middleware.py  # 中间件测试
pytest tests/common/test_models.py      # 模型测试

# 3. 生成覆盖率报告
pytest --cov=modules/common --cov-report=html tests/common/
# 查看报告：htmlcov/index.html

# 4. 性能测试
pytest tests/common/test_performance.py -v

# 5. 跨平台测试（Windows）
pytest tests/common/test_cross_platform.py -v -m windows
```

### CI 执行
```yaml
# .github/workflows/ci.yml
- name: Test common module
  run: |
    pytest tests/common/ \
      --cov=modules/common \
      --cov-fail-under=80 \
      --junit-xml=test-results-common.xml
```

---

## 验证步骤

### 测试前验证
```bash
# 1. 环境准备
export APP_ENV=test
pip install -r requirements.txt

# 2. 安装测试依赖
pip install pytest pytest-cov pytest-mock

# 3. 验证环境
python -c "import modules.common; print('OK')"
```

### 测试中验证
```bash
# 1. 运行测试并监控
pytest tests/common/ -v --tb=short

# 2. 检查覆盖率
pytest --cov=modules/common tests/common/
# 确保 ≥ 80%

# 3. 检查性能
pytest tests/common/test_performance.py -v
# 确保所有指标达标
```

### 测试后验证
```bash
# 1. 检查测试报告
cat test-results-common.xml

# 2. 查看覆盖率详情
open htmlcov/index.html
```

---

## 回滚逻辑

如果测试发现严重问题：

### 1. 停止发布
```bash
# 标记为阻塞
git tag -a v1.1.0-blocked -m "Common module tests failed"

# 通知团队
echo "⚠️ Common module 测试失败，阻止发布" | tee /dev/stderr
```

### 2. 分析问题
```bash
# 查看失败的测试
pytest tests/common/ -v --lf  # 只运行失败的测试

# 查看详细日志
pytest tests/common/ -vv --tb=long
```

### 3. 决策
- **问题可快速修复**：修复后重新测试
- **问题影响广泛**：回滚到上一版本

### 4. 回滚测试
```bash
# 回滚到上一版本
git checkout <previous-tag> -- modules/common/

# 重新运行测试
pytest tests/common/ -v

# 确认问题解决
```

---

## 测试数据管理

### 测试数据原则
1. **独立性**：每个测试使用独立的数据
2. **可重复性**：测试结果可复现
3. **清理**：测试后清理数据

### 测试夹具（Fixtures）
```python
# tests/common/conftest.py
import pytest

@pytest.fixture
def sample_data():
    """示例数据"""
    return {
        "text": "test data",
        "number": 42,
        "list": [1, 2, 3]
    }

@pytest.fixture
def mock_config(monkeypatch):
    """Mock 配置"""
    monkeypatch.setenv("SECRET_KEY", "test_key_123")
    yield
    monkeypatch.undo()
```

---

## 人工测试跟踪

### 目标
跟踪需要人工验证的功能状态。

### 待测试功能清单

| 功能 | 状态 | 测试人员 | 测试日期 | 测试结果 | 备注 |
|------|------|---------|---------|---------|------|
| 跨平台编码 | 已通过 | AI | 2025-11-09 | ✅ | Windows/macOS/Linux 验证 |
| 加密性能 | 待测试 | - | - | - | 需要验证 P95 < 10ms |
| 并发安全性 | 待测试 | - | - | - | 需要验证 100+ 并发 |

### 测试状态说明

- **待测试**: 功能已完成，等待人工测试
- **测试中**: 正在进行人工测试
- **已通过**: 测试通过，可以发布
- **已失败**: 测试失败，需要修复
- **已跳过**: 暂不测试（需说明原因）

### 维护要求

1. **AI 开发完成后**: 必须更新此表格，标记需要人工测试的功能。
2. **测试完成后**: 更新测试状态、测试人员和测试日期。
3. **定期审查**: 每周审查一次，确保待测试功能得到及时处理。
4. **状态更新**: 使用 `make test_status_check` 检查跟踪状态。

---

## 相关文档
- **接口契约**：`CONTRACT.md`
- **模块架构**：`README.md`
- **运维手册**：`RUNBOOK.md`
- **缺陷管理**：`BUGS.md`

