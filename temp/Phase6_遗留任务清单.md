# Phase 6 + 6.5 遗留任务清单

> **用途**: 记录Phase 6和6.5未完成的任务，需要在后续Phase中解决
> **创建时间**: 2025-11-07
> **状态**: 待处理

---

## 概述

Phase 6和Phase 6.5主要完成了**文档和流程**的建设，但部分**工具实施**和**自动化功能**需要在后续Phase中完成。

---

## 必须实施的任务（Phase 7）

### 1. Fixtures管理工具 ⭐⭐⭐

**任务**: 实现`scripts/fixture_loader.py`

**原因**: 
- Phase 6已创建TEST_DATA.md和fixtures文件
- Phase 6.5已在plan.md中建立触发机制
- 但缺少实际的加载工具

**需要实现**:
- 读取模块的TEST_DATA.md
- 加载指定场景的Fixtures（minimal/standard/full）
- 支持模块感知（从agent.md读取test_data配置）
- 支持环境选择（dev/test/demo）
- 清理功能

**验收标准**:
```bash
make load_fixture MODULE=example FIXTURE=minimal
# 应该：
# - 读取doc/modules/example/doc/TEST_DATA.md
# - 加载doc/modules/example/fixtures/minimal.sql
# - 输出加载结果统计
```

**优先级**: 🔴 高（Phase 7必须完成）

**预计时间**: 4-6小时

**依赖**: Phase 6的TEST_DATA.md和fixtures文件（已完成）

---

### 2. dev_check命令集成 ⭐⭐⭐

**任务**: 在Makefile的dev_check中整合所有校验

**原因**:
- 目前有9个校验命令分散
- 缺少统一的开发质量检查入口

**需要实现**:
```makefile
dev_check:
	@echo "🔍 运行开发质量检查..."
	@make agent_lint
	@make registry_check
	@make doc_route_check
	@make type_contract_check
	@make doc_script_sync_check
	@make db_lint
	@make doc_style_check
	@make consistency_check
	@echo "✅ 所有检查通过！"
```

**验收标准**:
- `make dev_check`一次性运行所有校验
- 清晰的输出格式
- 失败时明确指出哪个检查失败

**优先级**: 🔴 高（Phase 7必须完成）

**预计时间**: 1-2小时

---

## 建议实施的任务（Phase 7-8）

### 3. 环境管理工具 ⭐⭐

**任务**: 实现`scripts/db_env.py`（可选）

**原因**:
- TEST_DATA.md中定义了dev/test/demo环境
- 缺少环境识别和切换工具

**需要实现**:
- 识别当前数据库环境
- 切换数据库环境
- 读取环境配置（db/engines/postgres/config/*.yaml）
- 验证环境配置正确性

**验收标准**:
```bash
make db_env ENV=test
# 应该：
# - 切换到测试数据库
# - 验证连接
# - 显示当前环境信息
```

**优先级**: 🟡 中（Phase 7建议实施，Phase 8也可以）

**预计时间**: 3-4小时

---

### 4. CI配置更新 ⭐⭐

**任务**: 更新`.github/workflows/ci.yml`（如有）

**原因**:
- 新增了多个校验工具
- 需要集成到CI流程

**需要实现**:
```yaml
- name: Run validation
  run: |
    make agent_lint
    make registry_check
    make doc_route_check
    make type_contract_check
    make db_lint
    make validate
```

**验收标准**:
- CI可以运行所有校验
- 失败时明确报错
- 每个校验结果单独显示

**优先级**: 🟡 中（Phase 7建议实施）

**预计时间**: 1-2小时

---

## 可选实施的任务（Phase 8+）

### 5. Mock数据生成器 ⭐

**任务**: 实现`scripts/mock_generator.py`（可选）

**原因**:
- TEST_DATA.md中已定义Mock规则
- 用于大规模测试数据生成

**需要实现**:
- 读取TEST_DATA.md中的Mock规则
- 使用Faker生成随机数据
- 支持数据分布配置
- 批量插入数据库

**验收标准**:
```bash
make generate_mock MODULE=example TABLE=runs COUNT=1000
# 应该：
# - 读取Mock规则
# - 生成1000条随机数据
# - 插入测试数据库
```

**优先级**: 🟢 低（Phase 8可选实施）

**预计时间**: 6-8小时

---

### 6. Mock生命周期管理 ⭐

**任务**: 实现`scripts/mock_lifecycle.py`（可选）

**原因**:
- Mock数据需要清理
- 需要生命周期管理

**需要实现**:
- 清理Mock数据
- 查看Mock统计
- 验证Mock数据完整性

**验收标准**:
```bash
make cleanup_mock MODULE=example
make mock_stats MODULE=example
```

**优先级**: 🟢 低（Phase 8可选，与任务5配套）

**预计时间**: 2-3小时

---

### 7. 项目迁移自动化工具 ⭐

**任务**: 实现项目迁移辅助工具（可选）

**原因**:
- PROJECT_MIGRATION_GUIDE.md是流程文档
- 缺少自动化工具辅助

**需要实现**:
- `scripts/project_migrate.py`
  - 扫描旧项目结构
  - 生成架构映射方案
  - 自动调整import路径
  - 生成迁移报告

**验收标准**:
```bash
python scripts/project_migrate.py --source <old-project> --strategy A
# 应该：
# - 分析旧项目
# - 生成映射方案
# - 执行复制和路径调整
# - 输出迁移报告
```

**优先级**: 🟢 低（Phase 8+可选，当前手动流程已足够）

**预计时间**: 8-12小时

---

### 8. 文档解析器（方式1自动化） ⭐

**任务**: 实现文档解析和自动生成工具（可选）

**原因**:
- PROJECT_INIT_GUIDE.md方式1（有开发文档）是流程说明
- 缺少实际的文档解析工具

**需要实现**:
- `scripts/doc_parser.py`
  - 解析PRD/需求文档
  - 提取模块、功能、表结构
  - 生成项目骨架

**验收标准**:
```bash
python scripts/doc_parser.py --doc requirements.md --output project-config.yaml
# 应该：
# - 解析文档内容
# - 提取结构化信息
# - 生成配置文件
```

**优先级**: 🟢 低（Phase 8+可选，AI理解能力已足够）

**预计时间**: 10-15小时（需要NLP能力）

---

## 已知限制（非遗留任务）

### 1. ai_begin.sh生成的agent.md需要手动完善

**现状**: 
- ai_begin.sh生成基础YAML字段
- io.inputs/outputs、dependencies需要手动补充

**是否需要解决**: ❌ 否

**原因**: 
- 这些内容需要理解具体业务逻辑
- 手动补充是合理的
- MODULE_INIT_GUIDE.md中已明确说明

**处理方式**: 保持现状，文档中已说明

---

### 2. 方式1和方式4的自动化程度有限

**现状**:
- 方式1（有文档）：需要AI理解能力
- 方式4（项目迁移）：架构映射需要人工判断

**是否需要解决**: ❌ 否（短期）

**原因**:
- 当前流程文档已足够AI执行
- 完全自动化需要复杂的NLP和代码分析
- 投入产出比不高

**处理方式**: 
- 保持流程指南
- AI在执行时按流程引导用户
- 后期可选实施自动化工具（任务7、8）

---

## 任务优先级总览

### 🔴 高优先级（Phase 7必须完成）

| 任务 | 说明 | 预计时间 |
|------|------|---------|
| 1. fixture_loader.py | Fixtures加载工具 | 4-6小时 |
| 2. dev_check集成 | 统一质量检查命令 | 1-2小时 |

**小计**: 5-8小时（0.5-1天）

---

### 🟡 中优先级（Phase 7建议实施）

| 任务 | 说明 | 预计时间 |
|------|------|---------|
| 3. db_env.py | 环境管理工具 | 3-4小时 |
| 4. CI配置更新 | GitHub Actions集成 | 1-2小时 |

**小计**: 4-6小时（0.5天）

---

### 🟢 低优先级（Phase 8+可选）

| 任务 | 说明 | 预计时间 |
|------|------|---------|
| 5. mock_generator.py | Mock数据生成器 | 6-8小时 |
| 6. mock_lifecycle.py | Mock生命周期管理 | 2-3小时 |
| 7. project_migrate.py | 项目迁移工具 | 8-12小时 |
| 8. doc_parser.py | 文档解析器 | 10-15小时 |

**小计**: 26-38小时（3-5天，全部可选）

---

## Phase 7任务建议

### 必须做（高优先级）

1. ✅ **实现fixture_loader.py**
   - 读取TEST_DATA.md
   - 加载Fixtures到数据库
   - 支持场景选择
   - 清理功能

2. ✅ **dev_check集成**
   - 整合所有校验命令
   - 统一输出格式
   - 错误汇总

### 建议做（中优先级）

3. ✅ **db_env.py环境管理**
   - 环境识别
   - 环境切换
   - 配置验证

4. ✅ **CI配置更新**
   - GitHub Actions集成
   - 自动运行校验

### 可以暂缓（低优先级）

5-8. Mock生成器、项目迁移工具、文档解析器等
   - 这些是锦上添花
   - Phase 8+再考虑
   - 当前手动流程已足够

---

## Phase 8任务建议

### 可选实施

1. **Mock数据生成器**（如需要大规模测试）
2. **项目迁移工具**（如经常有项目迁移需求）
3. **文档解析器**（如经常使用方式1初始化）

### 优先级判断

- 如果团队经常需要大量测试数据 → 优先实施任务5、6
- 如果经常有项目迁移需求 → 优先实施任务7
- 如果经常基于文档创建项目 → 优先实施任务8
- 如果以上都不频繁 → 可以都不实施

---

## 非遗留任务（已知限制）

以下**不是**遗留任务，而是设计上的合理限制：

### 1. ai_begin.sh生成的agent.md需要手动完善

**状态**: ✅ 符合预期

**原因**: 
- io.inputs/outputs依赖具体业务逻辑
- 手动补充是合理的
- 文档中已明确说明

**处理**: 无需处理，保持现状

---

### 2. 初始化方式1和4需要AI能力

**状态**: ✅ 符合预期

**原因**:
- 文档解析需要AI理解
- 架构映射需要业务理解
- 当前流程指南已足够AI执行

**处理**: 
- 当前：AI按流程引导用户（手动辅助）
- 未来：可选实施自动化工具（任务7、8）

---

## 总结

### 遗留任务统计

- **必须实施**（Phase 7）: 2个任务，5-8小时
- **建议实施**（Phase 7）: 2个任务，4-6小时
- **可选实施**（Phase 8+）: 4个任务，26-38小时

### Phase 7重点

**必须做**:
1. ✅ fixture_loader.py（核心）
2. ✅ dev_check集成（核心）

**建议做**:
3. ✅ db_env.py（增强）
4. ✅ CI配置（增强）

**Phase 7预计时间**: 2-3天（含必须+建议任务）

### 后续Phase可选

- Mock生成器（Phase 8，如需要）
- 项目迁移工具（Phase 8+，如需要）
- 文档解析器（Phase 8+，如需要）

---

## 建议

### 对Phase 7的建议

**核心任务**（必须）:
1. fixture_loader.py
2. dev_check集成

**增强任务**（建议）:
3. db_env.py
4. CI配置

**总计**: 9-14小时（1-2天）

### 对Phase 8的建议

**评估后再决定是否实施**:
- Mock生成器：是否经常需要大规模测试数据？
- 项目迁移工具：是否经常有迁移需求？
- 文档解析器：是否经常基于文档创建项目？

**建议**: 根据实际使用情况决定，不必全部实施

---

## 相关文档

- **Phase 6完成报告**: temp/Phase6_完成报告.md（遗留问题章节）
- **Phase 6.5完成报告**: temp/Phase6.5_完成报告.md（遗留问题章节）
- **Phase 5扩展方案**: temp/Phase5_数据库治理扩展方案.md（工具设计）
- **执行计划**: temp/执行计划.md（Phase 7任务）

---

**创建时间**: 2025-11-07
**维护者**: AI Assistant

