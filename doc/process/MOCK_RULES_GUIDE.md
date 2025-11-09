---
audience: human
language: zh
version: complete
purpose: Documentation for MOCK_RULES_GUIDE
---
# Mock规则编写指南

> **用途**: 指导开发者编写Mock数据生成规则  
> **维护者**: AI-TEMPLATE团队  
> **创建时间**: 2025-11-09  
> **适用范围**: 所有使用mock_generator.py的模块

---

## 概述

### 什么是Mock规则

Mock规则是在TEST_DATA.md中定义的YAML格式配置，用于指导`mock_generator.py`自动生成符合要求的测试数据。

### 适用场景

- **大量数据需求**: 需要生成数百或数千条测试数据
- **随机性测试**: 需要测试系统对随机输入的处理能力
- **性能测试**: 需要大规模数据验证系统性能
- **边界测试**: 需要生成各种边界情况的数据

### Mock vs Fixtures

| 维度 | Mock数据 | Fixtures |
|------|---------|---------|
| 数量 | 大量（100+条） | 少量（≤50条） |
| 精确性 | 随机生成，不精确 | 手工维护，精确 |
| 维护成本 | 低（规则驱动） | 高（逐条维护） |
| 适用场景 | 性能测试、压力测试 | 单元测试、集成测试 |
| 可重复性 | 可通过seed控制 | 完全可重复 |

详见：[TEST_DATA_STRATEGY.md](./TEST_DATA_STRATEGY.md)

---

## Mock规则语法

### 基本结构

```yaml
mock_rules:
  <table_name>:
    count: <number>           # 生成记录数
    seed: <number>            # 随机种子（可选，用于可重复生成）
    lifecycle: <type>         # 生命周期类型
    fields:
      <field_name>:
        type: <generator_type>
        <generator_params>
```

### 生命周期类型

```yaml
lifecycle: ephemeral    # 临时（测试结束立即删除）
lifecycle: temporary    # 短期（24小时内删除）
lifecycle: persistent   # 持久（手动删除）
lifecycle: fixture      # Fixture级别（长期保留）
```

**推荐**:
- 单元测试: `ephemeral`
- 集成测试: `temporary`  
- 演示环境: `persistent`

---

## 字段生成器类型

### 1. 基础类型生成器

#### 1.1 uuid（UUID生成）

```yaml
id:
  type: uuid
  version: 4              # UUID版本，默认4
```

**生成示例**: `550e8400-e29b-41d4-a716-446655440000`

---

#### 1.2 string（字符串生成）

```yaml
name:
  type: string
  faker: name             # Faker方法名
  locale: zh_CN           # 地区（可选）
```

**常用faker方法**:
- `name`: 人名
- `company`: 公司名
- `address`: 地址
- `email`: 邮箱
- `phone_number`: 电话
- `url`: URL
- `sentence`: 句子
- `paragraph`: 段落
- `word`: 单词

**示例**:
```yaml
title:
  type: string
  faker: sentence
  max_length: 100

description:
  type: string
  faker: paragraph
  max_length: 500
```

---

#### 1.3 int（整数生成）

```yaml
age:
  type: int
  min: 18
  max: 65
```

**参数**:
- `min`: 最小值（包含）
- `max`: 最大值（包含）

**生成示例**: `42`

---

#### 1.4 float（浮点数生成）

```yaml
price:
  type: float
  min: 10.0
  max: 1000.0
  decimals: 2         # 小数位数
```

**生成示例**: `156.78`

---

#### 1.5 bool（布尔值生成）

```yaml
is_active:
  type: bool
  true_probability: 0.7   # true的概率（0-1）
```

**生成示例**: `true` 或 `false`

---

#### 1.6 enum（枚举值生成）

```yaml
status:
  type: enum
  values: [pending, active, completed, failed]
  weights: [0.1, 0.6, 0.2, 0.1]    # 各值的权重（可选）
```

**说明**:
- `values`: 可选值列表
- `weights`: 对应权重，总和应为1（可选，默认均匀分布）

**生成示例**: `active`（60%概率）

---

### 2. 日期时间生成器

#### 2.1 timestamp（时间戳生成）

```yaml
created_at:
  type: timestamp
  start: "-30d"          # 30天前
  end: "now"             # 当前时间
  format: "iso8601"      # 输出格式
```

**时间表达式**:
- `now`: 当前时间
- `-Nd`: N天前（如`-7d`）
- `-Nh`: N小时前（如`-2h`）
- `-Nm`: N分钟前（如`-30m`）
- `+Nd`: N天后（如`+7d`）
- 绝对时间: `2024-01-01T00:00:00Z`

**格式选项**:
- `iso8601`: ISO 8601格式（默认）
- `unix`: Unix时间戳（秒）
- `unix_ms`: Unix时间戳（毫秒）
- 自定义: `%Y-%m-%d %H:%M:%S`

**示例**:
```yaml
created_at:
  type: timestamp
  start: "-7d"
  end: "now"
  format: "iso8601"

updated_at:
  type: timestamp
  start: "-1d"
  end: "now"
  format: "iso8601"
```

---

#### 2.2 date（日期生成）

```yaml
birthday:
  type: date
  start: "1960-01-01"
  end: "2005-12-31"
  format: "%Y-%m-%d"
```

**生成示例**: `1985-03-15`

---

### 3. 关联数据生成器

#### 3.1 foreign_key（外键关联）

```yaml
user_id:
  type: foreign_key
  table: users
  field: id
  strategy: random      # random | sequential | weighted
```

**策略说明**:
- `random`: 随机选择现有记录
- `sequential`: 顺序选择
- `weighted`: 按权重选择（需配合weights字段）

**示例**:
```yaml
# 70%关联活跃用户，30%关联不活跃用户
creator_id:
  type: foreign_key
  table: users
  field: id
  strategy: weighted
  conditions:
    - filter: {is_active: true}
      weight: 0.7
    - filter: {is_active: false}
      weight: 0.3
```

---

#### 3.2 reference（引用其他字段）

```yaml
# 确保updated_at >= created_at
created_at:
  type: timestamp
  start: "-30d"
  end: "now"

updated_at:
  type: reference
  source: created_at
  offset: "+0h"         # 偏移量
  max_offset: "+24h"    # 最大偏移
```

**生成逻辑**: `updated_at = created_at + random(offset, max_offset)`

---

### 4. 高级生成器

#### 4.1 json（JSON对象生成）

```yaml
metadata:
  type: json
  template:
    version: "1.0"
    source:
      type: string
      faker: word
    count:
      type: int
      min: 1
      max: 100
```

**说明**: template中可嵌套任意字段生成器

---

#### 4.2 array（数组生成）

```yaml
tags:
  type: array
  item_type: string
  item_config:
    faker: word
  min_length: 1
  max_length: 5
```

**参数**:
- `item_type`: 数组元素类型
- `item_config`: 元素生成配置
- `min_length`: 最小长度
- `max_length`: 最大长度

**生成示例**: `["technology", "python", "web"]`

---

#### 4.3 computed（计算字段）

```yaml
full_name:
  type: computed
  expression: "${first_name} ${last_name}"
  depends_on: [first_name, last_name]
```

**说明**:
- 必须先生成依赖字段
- 使用`${field_name}`引用其他字段
- 支持简单的字符串拼接

---

## 分布控制

### 1. 数值分布

```yaml
price:
  type: float
  min: 10.0
  max: 1000.0
  distribution: normal    # normal | uniform | exponential
  mean: 100.0             # 正态分布的均值
  std_dev: 30.0           # 正态分布的标准差
```

**分布类型**:
- `uniform`: 均匀分布（默认）
- `normal`: 正态分布（需指定mean和std_dev）
- `exponential`: 指数分布（需指定lambda参数）

---

### 2. 时间分布

```yaml
created_at:
  type: timestamp
  start: "-30d"
  end: "now"
  distribution: weighted_recent
  recent_weight: 0.7      # 最近7天的权重
```

**时间分布类型**:
- `uniform`: 均匀分布
- `weighted_recent`: 最近时间权重更高
- `business_hours`: 仅工作时间（9:00-18:00）
- `weekend_only`: 仅周末

---

### 3. 类别分布

```yaml
status:
  type: enum
  values: [draft, active, archived]
  distribution: real_world
  weights: [0.15, 0.70, 0.15]    # 反映真实世界的分布
```

---

## 完整示例

### 示例1: 用户表（简单）

```yaml
mock_rules:
  users:
    count: 100
    seed: 42
    lifecycle: temporary
    fields:
      id:
        type: uuid
      
      username:
        type: string
        faker: user_name
      
      email:
        type: string
        faker: email
      
      age:
        type: int
        min: 18
        max: 65
        distribution: normal
        mean: 35
        std_dev: 12
      
      is_active:
        type: bool
        true_probability: 0.8
      
      created_at:
        type: timestamp
        start: "-180d"
        end: "now"
        distribution: uniform
```

---

### 示例2: 订单表（带关联）

```yaml
mock_rules:
  orders:
    count: 500
    seed: 123
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
            weight: 0.9
          - filter: {is_active: false}
            weight: 0.1
      
      status:
        type: enum
        values: [pending, paid, shipped, delivered, cancelled]
        weights: [0.1, 0.2, 0.3, 0.35, 0.05]
      
      amount:
        type: float
        min: 10.0
        max: 5000.0
        decimals: 2
        distribution: exponential
        lambda: 0.002
      
      items_count:
        type: int
        min: 1
        max: 10
        distribution: normal
        mean: 3
        std_dev: 2
      
      created_at:
        type: timestamp
        start: "-90d"
        end: "now"
        distribution: weighted_recent
        recent_weight: 0.6
      
      updated_at:
        type: reference
        source: created_at
        offset: "+0h"
        max_offset: "+72h"
```

---

### 示例3: 文章表（JSON和数组）

```yaml
mock_rules:
  articles:
    count: 200
    lifecycle: temporary
    fields:
      id:
        type: uuid
      
      title:
        type: string
        faker: sentence
        max_length: 100
      
      author_id:
        type: foreign_key
        table: users
        field: id
        strategy: random
      
      tags:
        type: array
        item_type: string
        item_config:
          faker: word
        min_length: 1
        max_length: 5
      
      metadata:
        type: json
        template:
          views:
            type: int
            min: 0
            max: 10000
          likes:
            type: int
            min: 0
            max: 500
          category:
            type: enum
            values: [tech, business, lifestyle, education]
      
      published_at:
        type: timestamp
        start: "-365d"
        end: "now"
        distribution: business_hours
```

---

### 示例4: 时间序列数据

```yaml
mock_rules:
  metrics:
    count: 1440          # 24小时 * 60分钟
    seed: 999
    lifecycle: ephemeral
    fields:
      id:
        type: uuid
      
      metric_name:
        type: enum
        values: [cpu_usage, memory_usage, disk_io, network_io]
        weights: [0.25, 0.25, 0.25, 0.25]
      
      value:
        type: float
        min: 0.0
        max: 100.0
        decimals: 2
        distribution: normal
        mean: 45.0
        std_dev: 15.0
      
      timestamp:
        type: timestamp
        start: "-24h"
        end: "now"
        interval: "1m"       # 每条记录间隔1分钟
        format: "iso8601"
```

---

### 示例5: 电商商品（完整）

```yaml
mock_rules:
  products:
    count: 300
    seed: 456
    lifecycle: persistent
    fields:
      id:
        type: uuid
      
      sku:
        type: computed
        expression: "PRD-${year}-${sequence}"
        depends_on: [year, sequence]
      
      year:
        type: int
        min: 2023
        max: 2024
      
      sequence:
        type: int
        min: 10000
        max: 99999
      
      name:
        type: string
        faker: catch_phrase
        max_length: 100
      
      category:
        type: enum
        values: [electronics, clothing, books, home, sports]
        weights: [0.3, 0.25, 0.15, 0.2, 0.1]
      
      price:
        type: float
        min: 9.99
        max: 999.99
        decimals: 2
        distribution: exponential
        lambda: 0.01
      
      stock:
        type: int
        min: 0
        max: 1000
        distribution: normal
        mean: 100
        std_dev: 50
      
      is_featured:
        type: bool
        true_probability: 0.15
      
      tags:
        type: array
        item_type: string
        item_config:
          type: enum
          values: [new, sale, popular, trending, limited]
        min_length: 0
        max_length: 3
      
      specs:
        type: json
        template:
          weight:
            type: float
            min: 0.1
            max: 50.0
            decimals: 2
          dimensions:
            type: string
            faker: sentence
          color:
            type: enum
            values: [black, white, red, blue, green, yellow]
      
      created_at:
        type: timestamp
        start: "-365d"
        end: "-30d"
        format: "iso8601"
      
      updated_at:
        type: reference
        source: created_at
        offset: "+1d"
        max_offset: "+60d"
```

---

## 最佳实践

### 1. 使用合适的种子值

```yaml
# 生产环境：使用固定种子确保可重复
mock_rules:
  users:
    count: 1000
    seed: 42              # 固定种子

# 开发环境：不指定种子以获得随机数据
mock_rules:
  users:
    count: 100
    # seed: 无
```

---

### 2. 合理设置生命周期

```yaml
# 单元测试：立即清理
lifecycle: ephemeral

# 集成测试：24小时后清理
lifecycle: temporary

# Demo环境：长期保留
lifecycle: persistent
```

---

### 3. 控制数据量

```yaml
# 小规模验证
count: 10

# 中等规模测试
count: 100

# 大规模性能测试
count: 10000
```

**注意**: 大规模生成时注意数据库性能

---

### 4. 使用真实的分布

```yaml
# ❌ 不好：均匀分布（不真实）
status:
  type: enum
  values: [active, inactive]
  # 默认50/50分布

# ✅ 好：反映真实世界
status:
  type: enum
  values: [active, inactive]
  weights: [0.85, 0.15]    # 85%活跃用户
```

---

### 5. 保持关联一致性

```yaml
# 确保订单的updated_at在created_at之后
created_at:
  type: timestamp
  start: "-90d"
  end: "now"

updated_at:
  type: reference
  source: created_at
  offset: "+0h"
  max_offset: "+72h"
```

---

## 常见问题

### Q1: 如何生成中文数据？

```yaml
name:
  type: string
  faker: name
  locale: zh_CN        # 指定中文地区
```

---

### Q2: 如何避免重复的email？

```yaml
email:
  type: string
  faker: email
  unique: true         # 确保唯一性（注意：大量数据时可能失败）
```

---

### Q3: 如何生成递增的ID？

```yaml
sequence_id:
  type: int
  min: 1
  max: 999999
  strategy: sequential  # 顺序生成
```

---

### Q4: Mock生成速度慢怎么办？

1. 减少`count`数量
2. 简化复杂的`json`和`array`字段
3. 避免大量`foreign_key`查询
4. 使用批量插入（execute_batch）

---

## 参考资料

- [TEST_DATA_STRATEGY.md](./TEST_DATA_STRATEGY.md) - 测试数据策略
- [FIELD_GENERATORS.md](../reference/FIELD_GENERATORS.md) - 字段生成器详细参考
- [Faker文档](https://faker.readthedocs.io/) - Faker库官方文档

---

## 维护历史

- 2025-11-09: 创建文档（Phase 11）

