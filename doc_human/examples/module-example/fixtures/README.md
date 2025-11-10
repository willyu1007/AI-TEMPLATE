# Example模块 Fixtures

## 概述

本目录包含example模块的测试数据Fixtures。

## 文件说明

| 文件 | 记录数 | 用途 |
|------|--------|------|
| minimal.sql | 3条 | 单元测试 |
| standard.sql | 20条 | 集成测试 |

## 使用方法

### 加载Fixtures

```bash
# 加载最小集（单元测试）
make load_fixture MODULE=example FIXTURE=minimal

# 加载标准集（集成测试）
make load_fixture MODULE=example FIXTURE=standard
```

### 在测试中使用

```python
# tests/example/conftest.py
import pytest

@pytest.fixture
def minimal_data(db_session):
    """加载minimal fixtures"""
    load_fixture("example", "minimal")
    yield
    cleanup_fixture()

@pytest.fixture(scope="class")
def standard_data(db_session):
    """加载standard fixtures"""
    load_fixture("example", "standard")
    yield
    cleanup_fixture()
```

## 维护说明

### 更新Fixtures

1. 修改 `doc/TEST_DATA.md` 中的定义
2. 更新对应的.sql文件
3. 测试加载：`make load_fixture MODULE=example FIXTURE=minimal`
4. 运行测试验证：`pytest tests/example/`
5. 提交变更

### 注意事项

- **数据一致性**：Fixtures数据必须与TEST_DATA.md定义一致
- **数据独立性**：测试间数据互不影响，每次测试前重新加载
- **相对时间**：使用相对时间（如`NOW() - INTERVAL '7 days'`）而非硬编码
- **数据量**：minimal保持<10条，standard保持10-100条

## 数据特征

### minimal（最小集）

- 3条记录，覆盖3种状态（success、error、running）
- 3种语言（python、javascript、go）
- 适合快速单元测试

### standard（标准集）

- 20条记录
- 状态分布：70% success、20% error、10% running
- 语言分布：50% python、30% javascript、20% go
- 时间分布：过去7天均匀分布
- 适合集成测试和API测试

## 相关文档

- [TEST_DATA.md](../doc/TEST_DATA.md) - 测试数据规格定义
- [TEST_PLAN.md](../doc/TEST_PLAN.md) - 测试计划
- [db/engines/postgres/schemas/tables/runs.yaml](/db/engines/postgres/schemas/tables/runs.yaml) - 表结构定义

---

**维护者**: AI-TEMPLATE维护者
**最后更新**: 2025-11-07

