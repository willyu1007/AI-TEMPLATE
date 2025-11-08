# 模块初始化 - Phase 7: 定义测试数据需求

> **所属**: MODULE_INIT_GUIDE.md Phase 7  
> **用途**: Phase 7的详细执行指南  
> **目标**: 定义测试数据需求和Fixtures（推荐）

---

## 目标

定义模块的测试数据需求，创建TEST_DATA.md和Fixtures

---

## 7.1 创建TEST_DATA.md

从模板复制：

```bash
MODULE=<entity>

cp doc/modules/TEMPLATES/TEST_DATA.md.template modules/$MODULE/doc/TEST_DATA.md
```

填写内容（参考`doc/modules/example/doc/TEST_DATA.md`）：

```markdown
# <Entity>模块测试数据规格

## 1. 测试数据概述

### 1.1 数据类型
- User账号数据
- 业务数据
- 关联数据

### 1.2 数据量级
- 最小集：3-5条核心数据
- 标准集：20-30条典型数据
- 压力集：1000+条数据

## 2. Fixtures定义

### 2.1 minimal.sql（最小集）
**用途**: 单元测试、快速验证
**数据量**: 3条

### 2.2 standard.sql（标准集）
**用途**: 集成测试、开发调试
**数据量**: 20条

### 2.3 performance.sql（压力集）
**用途**: 性能测试
**数据量**: 1000条

## 3. Mock数据规则

### 3.1 用户数据
\`\`\`yaml
mock_rules:
  - table: users
    count: 20
    generators:
      - field: username
        type: faker
        provider: user_name
      - field: email
        type: faker
        provider: email
\`\`\`

## 4. 数据生命周期

| Fixture | 生命周期 | 清理方式 |
|---------|---------|---------|
| minimal | ephemeral | 测试后立即清理 |
| standard | temporary | 每日清理 |
| performance | persistent | 手动清理 |
```

---

## 7.2 创建fixtures/目录

```bash
MODULE=<entity>

mkdir -p modules/$MODULE/fixtures
```

---

## 7.3 创建Fixtures文件

### minimal.sql（最小集）

```sql
-- Minimal fixture for <entity>
-- Generated: $(date +%Y-%m-%d)

-- 清理旧数据
DELETE FROM <entity>_<table> WHERE id < 1000;

-- 插入测试数据
INSERT INTO <entity>_<table> (id, name, created_at) VALUES
  (1, 'Test Entity 1', CURRENT_TIMESTAMP),
  (2, 'Test Entity 2', CURRENT_TIMESTAMP),
  (3, 'Test Entity 3', CURRENT_TIMESTAMP);
```

### standard.sql（标准集）

```sql
-- Standard fixture for <entity>
-- Generated: $(date +%Y-%m-%d)

-- 清理旧数据
DELETE FROM <entity>_<table> WHERE id < 10000;

-- 插入20条测试数据
INSERT INTO <entity>_<table> (id, name, created_at) VALUES
  (101, 'Standard Entity 1', CURRENT_TIMESTAMP),
  (102, 'Standard Entity 2', CURRENT_TIMESTAMP),
  -- ... 共20条
  (120, 'Standard Entity 20', CURRENT_TIMESTAMP);
```

### fixtures/README.md

```markdown
# <Entity>模块Fixtures

## 文件说明

| 文件 | 用途 | 数据量 | 生命周期 |
|------|------|--------|---------|
| minimal.sql | 单元测试 | 3条 | ephemeral |
| standard.sql | 集成测试 | 20条 | temporary |
| performance.sql | 性能测试 | 1000条 | persistent |

## 使用方法

### 加载Fixture
\`\`\`bash
make load_fixture MODULE=<entity> FIXTURE=minimal
\`\`\`

### 清理数据
\`\`\`bash
make cleanup_fixture MODULE=<entity>
\`\`\`

### 生成Mock数据
\`\`\`bash
make generate_mock MODULE=<entity> TABLE=<table> COUNT=100
\`\`\`
```

---

## 7.4 更新agent.md

在agent.md中添加test_data配置：

```yaml
test_data:
  fixtures_dir: /modules/<entity>/fixtures
  test_data_spec: /modules/<entity>/doc/TEST_DATA.md
  lifecycle:
    minimal: ephemeral
    standard: temporary
```

---

## 常见问题

### Q: 测试数据一定要创建吗？
**A**: 强烈推荐。测试数据是模块质量的保障，便于快速测试和调试。

### Q: Fixtures和Mock数据有什么区别？
**A**:
- Fixtures: 预定义的SQL文件，数据固定
- Mock数据: 使用Faker等工具动态生成，数据随机

### Q: 数据量级如何确定？
**A**:
- 最小集：能覆盖核心功能即可（3-5条）
- 标准集：能覆盖常见场景（20-30条）
- 压力集：能测试性能瓶颈（1000+条）

### Q: 生命周期如何选择？
**A**:
- ephemeral（临时）: 测试后立即清理，用于单元测试
- temporary（暂时）: 定期清理（如每日），用于集成测试
- persistent（持久）: 手动清理，用于性能测试

---

## AI执行规范

**必须做**:
- ✅ 创建TEST_DATA.md（从模板复制）
- ✅ 创建fixtures/目录
- ✅ 至少创建minimal.sql
- ✅ 更新agent.md的test_data配置

**可选做**:
- 创建standard.sql和performance.sql
- 定义Mock数据规则

**不要做**:
- ❌ 不要跳过TEST_DATA.md
- ❌ 不要在Fixtures中使用生产数据

---

## 下一步

完成测试数据定义后，进入 → [Phase 8: 建立上下文恢复机制](init-context.md)

