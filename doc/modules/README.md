# 模块文档目录

> **用途**: 模块开发相关的指南、类型定义、示例和模板
> **维护者**: 项目维护团队
> **最后更新**: 2025-11-07

---

## 目录结构

```
doc/modules/
├── README.md               # 本文档：目录说明
├── MODULE_INIT_GUIDE.md    # 模块初始化指南
├── MODULE_TYPES.md         # 模块类型说明
├── MODULE_INSTANCES.md     # 模块实例索引（自动生成）
├── example/                # 完整的模块参考示例 ⭐
│   ├── agent.md
│   ├── README.md
│   ├── plan.md
│   └── doc/
│       ├── BUGS.md
│       ├── CHANGELOG.md
│       ├── CONTRACT.md
│       ├── PROGRESS.md
│       ├── RUNBOOK.md
│       └── TEST_PLAN.md
└── TEMPLATES/              # 空白文档模板
    ├── BUGS.md.template
    ├── CHANGELOG.md.template
    ├── CONTRACT.md.template
    ├── PROGRESS.md.template
    ├── RUNBOOK.md.template
    └── TEST_PLAN.md.template
```

---

## 📚 文档说明

### MODULE_INIT_GUIDE.md
**用途**: 模块初始化完整指南

**何时阅读**:
- 创建新模块时
- 不确定模块结构时
- 需要了解api/和frontend/是否需要创建时

**主要内容**:
- 7个Phase的详细步骤
- 决策树（是否需要api/frontend/）
- 校验清单
- 常见问题

---

### MODULE_TYPES.md
**用途**: 模块类型定义和分类标准

**何时阅读**:
- 确定新模块的类型和层级
- 理解模块分类体系
- 设计模块间关系

**主要内容**:
- 4个层级定义（Level 1-4）
- 4种模块类型（Assign, Select, SelectMethod, Aggregator）
- 类型选择决策树

---

### MODULE_INSTANCES.md（自动生成）
**用途**: 所有模块实例的索引

**何时阅读**:
- 查看现有模块列表
- 了解模块依赖关系
- 查找特定模块的路径

**生成方式**:
```bash
make module_doc_gen
```

---

### example/ ⭐ 参考示例
**用途**: 完整的模块实现示例，用于模块初始化时参考

**重要**: `example/` **不是业务模块**，仅用于参考！

**为什么放在doc/modules/下**:
- ✅ 明确是**文档/参考**性质，不是业务模块
- ✅ 避免被模块扫描工具误认为业务模块
- ✅ 与MODULE_INIT_GUIDE.md等文档放在一起
- ✅ 初始化完成后，业务模块用不到example，减少上下文混乱

**何时参考**:
1. **创建agent.md时**
   - 查看 `example/agent.md`
   - 学习YAML Front Matter怎么写
   - 了解完整的字段定义

2. **创建README.md时**
   - 查看 `example/README.md`
   - 参考"目录结构"章节
   - 参考"文档索引"格式

3. **填写CONTRACT.md时**
   - 查看 `example/doc/CONTRACT.md`
   - 学习输入/输出定义格式
   - 参考错误码定义

4. **其他文档**
   - BUGS.md: 缺陷管理格式
   - CHANGELOG.md: 变更记录规范
   - RUNBOOK.md: 运维手册结构
   - PROGRESS.md: 进度跟踪方式
   - TEST_PLAN.md: 测试计划内容

**不应该做的**:
- ❌ 把example当作业务模块运行
- ❌ 在modules/下寻找example（已移至doc/modules/）
- ❌ 在registry.yaml的module_instances中注册example
- ❌ 直接复制example的内容（应该根据实际模块调整）

---

### TEMPLATES/ 空白模板
**用途**: 空白的文档骨架（.template文件）

**与example/的区别**:
- `TEMPLATES/` - **空白骨架**，只有结构没有内容
- `example/` - **完整示例**，包含实际内容和说明

**何时使用**:
- 使用脚本初始化模块时（自动从TEMPLATES/复制）
- 手动创建模块文档时（复制模板后填写）

---

## 快速开始

### 场景1: 创建新模块

1. **阅读指南**
   ```bash
   # 阅读模块初始化指南
   cat doc/modules/MODULE_INIT_GUIDE.md
   ```

2. **参考示例**
   ```bash
   # 查看完整的模块示例
   ls -la doc/modules/example/
   cat doc/modules/example/agent.md
   ```

3. **使用脚本（推荐）**
   ```bash
   make ai_begin MODULE=<module-name>
   ```

4. **或手动创建**
   - 按照MODULE_INIT_GUIDE.md的步骤
   - 参考example/的实际实现
   - 从TEMPLATES/复制空白模板

### 场景2: 理解模块体系

1. **模块类型**
   ```bash
   # 了解模块分类
   cat doc/modules/MODULE_TYPES.md
   ```

2. **现有模块**
   ```bash
   # 查看已有模块
   cat doc/modules/MODULE_INSTANCES.md
   ```

### 场景3: 学习模块结构

```bash
# 查看example模块的完整结构
tree doc/modules/example/

# 学习agent.md的YAML Front Matter
head -90 doc/modules/example/agent.md

# 学习README.md的结构
cat doc/modules/example/README.md
```

---

## 📋 模块初始化检查清单

创建新模块时，确保：

### 必需文件
- [ ] modules/<entity>/agent.md - 含完整YAML Front Matter
- [ ] modules/<entity>/README.md - 含"目录结构"章节
- [ ] modules/<entity>/plan.md - 实施计划
- [ ] modules/<entity>/core/ - 核心业务逻辑目录
- [ ] modules/<entity>/doc/ - 6个标准文档目录
  - [ ] CONTRACT.md
  - [ ] CHANGELOG.md
  - [ ] RUNBOOK.md
  - [ ] BUGS.md
  - [ ] PROGRESS.md
  - [ ] TEST_PLAN.md

### 可选文件（根据需要）
- [ ] modules/<entity>/api/ - 如提供HTTP接口
- [ ] modules/<entity>/frontend/ - 如有特定UI组件
- [ ] modules/<entity>/models/ - 如有专属数据模型

### 注册与校验
- [ ] 在doc/orchestration/registry.yaml中注册
- [ ] `make agent_lint` 通过
- [ ] `make registry_check` 通过
- [ ] `make doc_route_check` 通过

---

## ❓ 常见问题

### Q1: example模块为什么在doc/modules/下？
**A**: example不是业务模块，仅用于参考。放在doc/modules/下：
- 明确是文档性质
- 避免被模块扫描工具误认为业务模块
- 初始化完成后不会增加上下文混乱

### Q2: TEMPLATES和example有什么区别？
**A**: 
- TEMPLATES/: 空白骨架（.template文件），没有实际内容
- example/: 完整示例，包含实际内容和说明

创建模块时两者都要参考：从TEMPLATES/复制骨架，参考example/填写内容。

### Q3: 如何更新example示例？
**A**: 
1. 修改 `doc/modules/example/` 中的文件
2. 确保修改后仍符合规范
3. 不需要在registry.yaml的module_instances中注册（它在reference_modules中）

### Q4: 真实的业务模块应该放在哪里？
**A**: `modules/<entity>/`，不是doc/modules/！
- doc/modules/ - 文档和参考
- modules/ - 真实的业务模块

---

## 相关文档

- **项目初始化**: doc/init/PROJECT_INIT_GUIDE.md
- **编排注册表**: doc/orchestration/registry.yaml
- **文档路由**: doc/orchestration/routing.md
- **全局目标**: doc/policies/goals.md
- **安全规范**: doc/policies/safety.md

---

## 🔄 维护说明

### 更新MODULE_INSTANCES.md
```bash
# 当有新模块注册或模块信息变更时
make module_doc_gen
```

### 更新example示例
当有模块规范变更时，同步更新 `doc/modules/example/`，确保：
- agent.md符合最新的schema
- 文档结构符合最新规范
- 内容完整且有意义

### 更新TEMPLATES
当文档模板格式变更时，同步更新 `doc/modules/TEMPLATES/`。

---

**最后更新**: 2025-11-07  
**维护者**: AI-TEMPLATE维护团队

