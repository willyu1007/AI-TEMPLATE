# 安全规范与质量门槛

> **用途**: 定义安全约束和质量要求
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## 安全约束

### 1. 路径访问控制

#### 读权限
智能体只能读取以下路径：
- `context_routes`中声明的路径
- 当前模块的目录（如modules/user/）
- 公共文档（doc/, docs/, README.md）

#### 写权限
智能体只能写入`ownership.code_paths`中声明的路径：

```yaml
ownership:
  code_paths:
    include:
      - modules/user/          # 允许写入user模块
      - tests/user/            # 允许写入user测试
    exclude:
      - modules/*/doc/CHANGELOG.md  # 禁止直接改CHANGELOG
      - "**/*.sql"                   # 禁止直接改SQL
```

**校验**: 智能体尝试写入未声明路径时应报错

---

### 2. 工具与API调用限制

#### 白名单机制
只允许调用`tools_allowed.calls`中声明的工具：

```yaml
tools_allowed:
  calls:
    - http.get              # 允许HTTP GET
    - http.post             # 允许HTTP POST
    - fs.read               # 允许读文件
    - fs.write              # 允许写文件
    - db.query              # 允许查询数据库
    # db.execute 未声明，禁止执行DDL
  models:
    - gpt-4                 # 允许使用GPT-4
    - claude-3-sonnet       # 允许使用Claude
```

**校验**: 调用未声明的工具时应拦截

---

### 3. 数据库安全

#### 半自动化原则
数据库操作必须经过人工审核：

1. **生成DDL**（自动）
   ```bash
   make db_gen_ddl TABLE=users
   # 生成: db/engines/postgres/migrations/XXX_create_users.sql
   ```

2. **人工审核**
   - 检查生成的SQL是否正确
   - 确认对现有表的影响
   - 评估性能影响

3. **执行迁移**（需确认）
   ```bash
   make db_migrate  # 需要用户确认
   ```

4. **回滚测试**
   ```bash
   make rollback_check PREV_REF=v1.0.0
   ```

#### 禁止操作
❌ 直接执行`DROP TABLE`
❌ 直接执行`TRUNCATE`
❌ 跳过迁移脚本直接改表
❌ 删除迁移脚本

---

### 4. 网络访问控制

#### 默认禁止
模块默认**不能**访问网络，除非显式声明：

```yaml
tools_allowed:
  calls:
    - http.get
    - http.post
constraints:
  - "只能访问内部API（*.internal.example.com）"
  - "禁止访问外部第三方API"
```

#### 外部依赖审核
如需访问外部API：
1. 在agent.md中声明
2. 说明用途和频率
3. 经安全审核批准

---

## 质量门槛

### 1. 测试要求

#### 必需的测试类型
每个模块至少包含：

```yaml
quality_gates:
  required_tests:
    - unit           # 单元测试
    - integration    # 集成测试
    - contract       # 契约测试
```

可选测试类型：
- e2e: 端到端测试
- smoke: 冒烟测试
- performance: 性能测试

#### 覆盖率要求
默认最低覆盖率：80%

```yaml
quality_gates:
  coverage_min: 0.80
```

模块可设置更高要求（如90%）

**校验**: 
```bash
make test_status_check
```

---

### 2. 文档要求

#### 必需的文档
每个模块实例必须有：

```
modules/<entity>/
├── agent.md        ✅ 带YAML Front Matter
├── README.md       ✅ 含"目录结构"章节
├── doc/
│   ├── CONTRACT.md     ✅ API契约
│   ├── CHANGELOG.md    ✅ 变更记录
│   ├── RUNBOOK.md      ✅ 运维手册
│   ├── BUGS.md         ✅ 已知问题
│   ├── PROGRESS.md     ✅ 进度追踪
│   └── TEST_PLAN.md    ✅ 测试计划
```

**校验**: 
```bash
make consistency_check
```

---

### 3. 兼容性要求

#### 契约兼容性
API变更必须保持向后兼容，或：
1. 更新CONTRACT.md
2. 更新CHANGELOG.md
3. 通过兼容性检查

```bash
make contract_compat_check
```

#### 数据库兼容性
表结构变更必须：
1. 提供up和down迁移脚本（成对）
2. 通过回滚测试
3. 记录在CHANGELOG.md

```bash
make migrate_check
make rollback_check PREV_REF=v1.0.0
```

---

### 4. 代码规范

#### 命名约束
- 模块名：小写字母+下划线（user_auth）
- 类名：大驼峰（UserService）
- 函数名：小驼峰或蛇形（getUserById, get_user_by_id）
- 常量：大写+下划线（MAX_RETRY_COUNT）

#### 文档风格
- 语言一致（中文或英文，不混用）
- 无颜文字（emoji）
- 结构化（使用标题、列表、表格）

```bash
make doc_style_check
```

---

## 违规处理

### 开发阶段（警告模式）
- 不符合规范时发出警告
- 允许继续开发
- 提示需要修复

### 提交阶段（严格模式）
- CI门禁检查所有规范
- 不通过则拒绝合并
- 必须修复后重新提交

### 生产阶段（强制模式）
- 部署前最终检查
- 任何违规都阻断部署
- 人工审核关键变更

---

## 豁免机制

特殊情况下可申请豁免：

### 申请流程
1. 在agent.md中添加`exemptions`字段
2. 说明豁免原因和范围
3. 设置豁免到期时间
4. 经审核批准

### 示例
```yaml
exemptions:
  - rule: "coverage_min"
    reason: "原型验证阶段，暂时放宽覆盖率要求"
    expiry: "2025-12-31"
    approved_by: "tech_lead"
```

---

## 审计与监控

### 定期审计
- 每月检查所有模块的安全配置
- 审查工具调用日志
- 检查是否有越权访问

### 监控指标
- 文档覆盖率
- 测试覆盖率
- 校验通过率
- 违规次数

### 报告
```bash
make ai_maintenance  # 生成维护报告
```

报告包含：
- 未通过的校验项
- 需要补充的文档
- 待修复的问题

---

## 相关资源

- **全局目标**: doc/policies/goals.md
- **路由规则**: doc/orchestration/routing.md
- **初始化指南**: doc/init/PROJECT_INIT_GUIDE.md
- **模块初始化**: doc/modules/MODULE_INIT_GUIDE.md

---

**维护**: 发现新的安全风险时，及时更新本文档
**审核**: 每季度由安全团队审核一次

