# Example模块测试数据规格

> **用途**: 演示模块的测试数据管理（作为参考模板）
> **维护者**: AI-TEMPLATE维护者
> **创建时间**: 2025-11-07
> **最后更新**: 2025-11-07

---

## 概述

### 测试数据需求

**数据量级**:
- 最小集（minimal）: 用于单元测试，3条记录
- 标准集（standard）: 用于集成测试，20条记录

**数据来源**:
- Fixtures（手工维护的精确数据）

**注意**: example模块是参考模板，不涉及真实数据库操作，因此测试数据为示例性质。

---

## Fixtures定义

### 1. Fixtures概览

| 场景名称 | 文件路径 | 数据表 | 记录数 | 用途 |
|---------|---------|--------|--------|------|
| minimal | fixtures/minimal.sql | runs | 3 | 单元测试 |
| standard | fixtures/standard.sql | runs | 20 | 集成测试 |

### 2. Fixtures详细定义

#### 场景1: minimal（最小集）

**用途**: 单元测试、快速验证

**数据表**: `runs`（示例表）
```yaml
records:
  - id: "run-test-001"
    task_description: "示例任务1：简单测试"
    language: "python"
    status: "success"
    result: '{"output": "Hello World"}'
    created_at: "2024-01-01T10:00:00Z"
    updated_at: "2024-01-01T10:00:05Z"
  
  - id: "run-test-002"
    task_description: "示例任务2：错误处理测试"
    language: "javascript"
    status: "error"
    result: '{"error": "Syntax Error"}'
    created_at: "2024-01-02T11:00:00Z"
    updated_at: "2024-01-02T11:00:03Z"
  
  - id: "run-test-003"
    task_description: "示例任务3：长任务测试"
    language: "go"
    status: "running"
    result: null
    created_at: "2024-01-03T12:00:00Z"
    updated_at: "2024-01-03T12:00:00Z"
```

**数据特征**:
- 覆盖3种状态：success、error、running
- 覆盖3种语言：python、javascript、go
- 包含不同的时间戳

---

#### 场景2: standard（标准集）

**用途**: 集成测试、API测试

**数据分布**:
- `runs`: 20条记录
  - 14条 status="success" (70%)
  - 4条 status="error" (20%)
  - 2条 status="running" (10%)
  - language: python(10条)、javascript(6条)、go(4条)
  - created_at: 过去7天内均匀分布

**数据特征**:
- 包含边界值测试数据（空描述、超长描述）
- 包含特殊字符测试
- 时间分布接近真实场景

---

### 3. Fixtures文件结构

```
doc/modules/example/fixtures/
├── minimal.sql           # 最小集（3条记录）
├── standard.sql          # 标准集（20条记录）
└── README.md             # Fixtures使用说明
```

### 4. Fixtures维护规范

**何时更新**:
- [ ] 添加新表时
- [ ] 修改表结构时
- [ ] 发现测试数据不足时

**更新流程**:
1. 修改Fixtures定义（本文档）
2. 更新对应的.sql文件
3. 运行`make load_fixture MODULE=example FIXTURE=minimal`测试加载
4. 运行相关测试验证数据正确性
5. 提交变更

**注意事项**:
- Fixtures数据应该是确定的、可重复的
- 使用相对时间（如"7天前"）而非硬编码时间戳
- 保持数据量适中（单元测试<10条）

---

## Mock数据生成规则

### 1. Mock概览

**注意**: example模块作为参考模板，暂不需要Mock数据生成。

如需要大规模测试数据，可参考以下规则示例：

#### 表: `runs`（示例）

```yaml
table: runs
count: 1000  # 生成1000条记录

columns:
  id:
    type: uuid
    generator: uuid4
  
  task_description:
    type: string
    generator: faker.sentence
    min_words: 5
    max_words: 20
  
  language:
    type: enum
    values: ["python", "javascript", "go"]
    distribution:
      python: 0.5
      javascript: 0.3
      go: 0.2
  
  status:
    type: enum
    values: ["success", "error", "running"]
    distribution:
      success: 0.7
      error: 0.2
      running: 0.1
  
  result:
    type: json
    generator: conditional
    conditions:
      - if: "status == 'success'"
        value: '{"output": "<faker.text>"}'
      - if: "status == 'error'"
        value: '{"error": "<faker.sentence>"}'
      - if: "status == 'running'"
        value: null
  
  created_at:
    type: timestamp
    generator: faker.date_time_between
    start_date: "-7d"
    end_date: "now"
  
  updated_at:
    type: timestamp
    generator: relative
    base: created_at
    offset: "+0s to +300s"
```

---

## 测试场景映射

### 单元测试（Unit Tests）

**数据需求**: Fixtures - minimal
**加载方式**: 测试前加载，测试后清理
**数据量**: 3条记录
**目的**: 验证业务逻辑正确性

```python
# tests/example/test_service.py
import pytest

@pytest.fixture
def minimal_data(db):
    """加载最小Fixtures"""
    # 注意：example模块不涉及真实DB，此为示例
    load_fixture("minimal")
    yield
    cleanup_fixture()

def test_process_task(minimal_data):
    """测试任务处理"""
    service = ExampleService()
    result = service.process_task("run-test-001")
    assert result["status"] == "success"
```

---

### 集成测试（Integration Tests）

**数据需求**: Fixtures - standard
**加载方式**: 测试类级别加载一次
**数据量**: 20条记录
**目的**: 验证模块间交互

```python
# tests/example/test_integration.py
import pytest

@pytest.fixture(scope="class")
def standard_data(db):
    """加载标准Fixtures"""
    load_fixture("standard")
    yield
    cleanup_fixture()

class TestExampleIntegration:
    """集成测试套件"""
    
    def test_batch_processing(self, standard_data):
        """测试批量处理"""
        service = ExampleService()
        results = service.batch_process(language="python")
        assert len(results) == 10  # 20条中的10条python
```

---

## 数据生命周期管理

### Fixtures生命周期

```
创建 → 版本控制 → 加载到测试DB → 测试运行 → 清理 → （保留Fixtures文件）
```

**特点**:
- Fixtures文件持久存储在repo中
- 测试数据临时存在于测试数据库
- 每次测试前重新加载

### 测试隔离

- 每个测试用例独立
- 测试前加载Fixtures
- 测试后清理数据
- 避免测试间干扰

---

## 环境配置

### 开发环境（dev）

**数据策略**: Fixtures - standard
**目的**: 本地开发、手工测试
**加载**: 一次性加载，手动刷新

```bash
make load_fixture MODULE=example FIXTURE=standard ENV=dev
```

### 测试环境（test）

**数据策略**: 
- 单元测试: Fixtures - minimal
- 集成测试: Fixtures - standard

**目的**: 自动化测试
**加载**: 每次测试前自动加载/清理

### 演示环境（demo）

**数据策略**: Fixtures - standard
**目的**: 产品演示、培训
**加载**: 按需加载，定期刷新

---

## 依赖关系

### 上游依赖

本模块的测试数据无上游依赖（独立模块）。

### 下游影响

作为参考模板，其他模块的测试数据定义应参考本文档结构。

---

## 常见问题

### Q1: example模块的测试数据是真实的吗？

不是。example模块作为参考模板，测试数据仅为示例性质。

### Q2: 如何使用这些测试数据？

参考MODULE_INIT_GUIDE.md中Phase 7的说明，了解如何定义和使用测试数据。

### Q3: 为什么不使用Mock生成器？

example模块数据量小，使用Fixtures更简单清晰。Mock生成器适用于大规模测试数据。

### Q4: 如何为我的模块创建类似的测试数据？

1. 从TEMPLATES/TEST_DATA.md.template复制
2. 参考本文档的结构
3. 根据模块实际情况调整
4. 创建对应的fixtures文件

---

## 相关文档

- **数据库规范**: /db/engines/postgres/docs/DB_SPEC.yaml
- **表结构定义**: /db/engines/postgres/schemas/tables/runs.yaml
- **模块契约**: doc/CONTRACT.md
- **测试计划**: doc/TEST_PLAN.md
- **测试数据模板**: /doc/modules/TEMPLATES/TEST_DATA.md.template

---

## Mock规则定义

### 概述

Mock规则用于自动生成大量测试数据，适用于性能测试和压力测试。

**注意**: example模块是参考模板，以下Mock规则仅作示例。

### Mock规则示例

#### 场景1: 大量运行记录（性能测试）

```yaml
mock_rules:
  runs:
    count: 1000                # 生成1000条记录
    seed: 42                   # 固定种子确保可重复
    lifecycle: temporary       # 24小时后自动清理
    fields:
      id:
        type: uuid
        version: 4
      
      task_description:
        type: string
        faker: sentence
        max_length: 200
      
      language:
        type: enum
        values: [python, javascript, go, typescript, rust]
        weights: [0.4, 0.25, 0.15, 0.15, 0.05]  # Python占40%
      
      status:
        type: enum
        values: [success, error, running, timeout]
        weights: [0.70, 0.15, 0.10, 0.05]       # 70%成功率
      
      result:
        type: json
        template:
          output:
            type: string
            faker: text
            max_length: 500
          execution_time:
            type: float
            min: 0.1
            max: 30.0
            decimals: 2
          memory_used:
            type: int
            min: 1024
            max: 524288  # 1KB - 512KB
      
      created_at:
        type: timestamp
        start: "-90d"          # 90天前
        end: "now"
        distribution: weighted_recent
        recent_weight: 0.6     # 最近数据权重更高
        format: "iso8601"
      
      updated_at:
        type: reference
        source: created_at
        offset: "+0s"
        max_offset: "+300s"    # 最多5分钟后更新
```

**使用方法**:
```bash
# 生成数据
make generate_mock MODULE=example COUNT=1000

# 查看统计
make mock_stats MODULE=example

# 清理数据
make cleanup_mocks MODULE=example
```

---

#### 场景2: 关联数据示例（外键关系）

假设有users表和runs表的关联关系：

```yaml
# Step 1: 先生成用户数据
mock_rules:
  users:
    count: 50
    seed: 100
    lifecycle: temporary
    fields:
      id:
        type: uuid
      
      username:
        type: string
        faker: user_name
      
      is_active:
        type: bool
        true_probability: 0.85  # 85%活跃用户

# Step 2: 生成关联的运行记录
mock_rules:
  runs:
    count: 500               # 每个用户平均10条记录
    seed: 101
    lifecycle: temporary
    fields:
      id:
        type: uuid
      
      user_id:
        type: foreign_key
        table: users
        field: id
        strategy: weighted
        conditions:
          - filter: {is_active: true}
            weight: 0.9      # 90%关联到活跃用户
          - filter: {is_active: false}
            weight: 0.1      # 10%关联到不活跃用户
      
      task_description:
        type: string
        faker: sentence
      
      language:
        type: enum
        values: [python, javascript, go]
        weights: [0.5, 0.3, 0.2]
      
      status:
        type: enum
        values: [success, error]
        weights: [0.8, 0.2]
      
      created_at:
        type: timestamp
        start: "-30d"
        end: "now"
        format: "iso8601"
```

---

#### 场景3: 分布控制示例

```yaml
mock_rules:
  runs:
    count: 2000
    seed: 200
    lifecycle: temporary
    fields:
      id:
        type: uuid
      
      task_description:
        type: string
        faker: sentence
      
      language:
        type: enum
        values: [python, javascript, go]
        weights: [0.60, 0.30, 0.10]  # 真实世界分布
      
      status:
        type: enum
        values: [success, error, running, timeout]
        weights: [0.75, 0.15, 0.05, 0.05]  # 生产环境分布
      
      execution_time:
        type: float
        min: 0.1
        max: 60.0
        decimals: 2
        distribution: exponential  # 指数分布
        lambda: 0.1
      
      created_at:
        type: timestamp
        start: "-60d"
        end: "now"
        distribution: weighted_recent
        recent_weight: 0.7
        format: "iso8601"
```

---

### Mock规则参考

完整的Mock规则语法和字段生成器说明，请参考：
- [MOCK_RULES_GUIDE.md](../../../process/MOCK_RULES_GUIDE.md) - Mock规则编写指南
- [TEST_DATA_STRATEGY.md](../../../process/TEST_DATA_STRATEGY.md) - 测试数据策略

---

## 版本历史

- 2025-11-07: v1.0 初始创建，作为参考示例
- 2025-11-09: v1.1 补充Mock规则章节（Phase 11）

---

**维护责任**: AI-TEMPLATE维护者
**审核责任**: 项目维护者
**更新频率**: 模板结构变更时更新

