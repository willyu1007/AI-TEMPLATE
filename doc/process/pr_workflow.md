# 提交与PR工作流

> **用途**: 定义代码提交和Pull Request流程
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## 提交流程

### 1. 开发完成

```bash
# 确保代码质量
make dev_check

# 如果是高风险变更
make rollback_check PREV_REF=<previous-version>
```

---

### 2. 文档更新

必须同步更新的文档：
- [ ] `modules/<entity>/doc/CONTRACT.md` - 如有接口变更
- [ ] `modules/<entity>/doc/CHANGELOG.md` - 记录变更
- [ ] `modules/<entity>/doc/TEST_PLAN.md` - 如有测试变更
- [ ] `modules/<entity>/doc/RUNBOOK.md` - 如有部署变更
- [ ] `doc/flows/dag.yaml` - 如有依赖变更
- [ ] `doc/orchestration/registry.yaml` - 如有模块变更

运行`make docgen`刷新索引。

---

### 3. 生成AI自审（AI-SR）

#### AI-SR-plan.md（方案阶段）
```markdown
# AI自审 - 方案

## 意图
<描述要做什么，为什么做>

## 影响面
- 代码变更：<文件列表>
- 接口变更：<API列表>
- 数据变更：<表/字段>
- 依赖变更：<模块依赖>

## 变更点
### DAG变更
<如有DAG变更>

### 契约变更
<如有接口契约变更>

### DB变更
<如有数据库变更>

## 测试点
- [ ] 单元测试
- [ ] 集成测试
- [ ] 回归测试

## 回滚方案
<如何回滚>
```

#### AI-SR-impl.md（实施阶段）
```markdown
# AI自审 - 实施

## 实施总结
<完成了什么>

## 变更文件
- `file1.py`: <说明>
- `file2.py`: <说明>

## 测试结果
\`\`\`
make dev_check: PASS
测试覆盖率: 85%
\`\`\`

## 遗留问题
<如有>

## 验证步骤
1. ...
2. ...
```

---

### 4. 提交代码

```bash
# 暂存变更
git add .

# 提交（遵循Conventional Commits）
git commit -m "feat(user): add user authentication"
git commit -m "fix(order): resolve payment timeout issue"
git commit -m "docs: update API documentation"
```

#### Commit消息规范
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type类型**:
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具
- `perf`: 性能优化

---

### 5. 创建Pull Request

#### PR标题
```
feat(user): add user authentication module
fix(order): resolve payment timeout issue
```

#### PR描述模板
```markdown
## 变更类型
- [ ] 新功能（feat）
- [ ] Bug修复（fix）
- [ ] 文档更新（docs）
- [ ] 重构（refactor）
- [ ] 性能优化（perf）

## 变更说明
<简要说明变更内容>

## 影响范围
- 影响模块：modules/user
- 接口变更：有/无
- 数据库变更：有/无
- 配置变更：有/无

## 测试
- [ ] 单元测试已添加/更新
- [ ] 集成测试已添加/更新
- [ ] 手动测试已完成
- [ ] 覆盖率达标（≥80%）

## 检查清单
- [ ] `make dev_check`通过
- [ ] 文档已更新
- [ ] AI-SR已生成
- [ ] CHANGELOG已更新

## AI自审
附件：`ai/sessions/<date>_<name>/AI-SR-impl.md`

## 相关Issue
Closes #123
```

---

## CI/CD门禁

### 自动检查项

PR提交后，CI自动运行：

```bash
# 1. 代码检查
make dev_check
  ├─ docgen              # 文档索引
  ├─ doc_style_check     # 文档风格
  ├─ dag_check           # DAG拓扑
  ├─ contract_compat_check  # 契约兼容
  ├─ runtime_config_check   # 配置校验
  ├─ migrate_check       # 迁移检查
  ├─ consistency_check   # 一致性
  ├─ frontend_types_check   # 前端类型
  ├─ agent_lint          # Agent校验
  ├─ registry_check      # 注册表校验
  └─ doc_route_check     # 文档路由

# 2. 测试运行
pytest tests/ --cov --cov-report=xml

# 3. 高风险检查（如标记为high-risk）
make rollback_check PREV_REF=main
```

### 门禁规则

| 风险级别 | 检查项 | 失败处理 |
|---------|--------|---------|
| Low | dev_check | 失败阻断合并 |
| Medium | dev_check + 人工审核 | 失败阻断合并 |
| High | dev_check + rollback_check + 架构师审核 | 失败阻断合并 |

---

## 审核流程

### 快速通道（Low Risk）

**适用**:
- 文档更新
- 测试补充
- Bug修复（无接口变更）

**流程**:
```
开发 → AI自审 → CI检查 → 自动合并（或快速人工审核）
```

---

### 常规通道（Medium Risk）

**适用**:
- 新增功能
- 接口扩展（向后兼容）
- 代码重构

**流程**:
```
开发 → AI自审 → CI检查 → Code Review → 合并
```

**Code Review要点**:
- [ ] 代码质量
- [ ] 测试覆盖
- [ ] 文档完整性
- [ ] 安全性

---

### 严格通道（High Risk）

**适用**:
- 接口变更（不兼容）
- 数据库迁移
- 架构调整
- 安全相关

**流程**:
```
开发 → AI自审 → CI检查 → Code Review → 架构师审核 → 回滚测试 → 合并
```

**额外检查**:
- [ ] 回滚方案验证
- [ ] 性能影响评估
- [ ] 安全风险评估
- [ ] 兼容性确认

---

## 合并策略

### 合并方式
- **Squash Merge**: 功能开发（推荐）
- **Merge Commit**: 保留完整历史
- **Rebase**: 保持线性历史

### 合并后
```bash
# 1. 删除功能分支
git branch -d feature/xxx

# 2. 更新主分支
git checkout main
git pull

# 3. 运行维护
make ai_maintenance
```

---

## 回滚机制

### 发现问题时

#### 1. 代码回滚
```bash
# 回滚到上一个稳定版本
git revert <commit-hash>

# 或强制回滚（需谨慎）
git reset --hard <commit-hash>
git push --force  # 需要权限
```

#### 2. 数据库回滚
```bash
# 运行down迁移
make db_rollback VERSION=<previous-version>
```

#### 3. 验证回滚
```bash
make rollback_check PREV_REF=<stable-version>
```

---

## 分支策略

### 分支命名
```
feature/<module>-<description>   # 新功能
fix/<module>-<description>       # Bug修复
refactor/<module>-<description>  # 重构
docs/<description>               # 文档更新
```

### 主要分支
- **main**: 生产分支，保护分支
- **develop**: 开发分支（可选）
- **feature/***: 功能分支
- **hotfix/***: 紧急修复分支

---

## 发布流程

### 版本标签
```bash
# 打标签
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### 版本号规范（SemVer）
- **主版本**: 不兼容的API变更
- **次版本**: 向后兼容的功能新增
- **修订号**: 向后兼容的Bug修复

### 发布检查清单
- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] CHANGELOG已更新
- [ ] 回滚测试通过
- [ ] 性能测试通过（如需要）
- [ ] 安全扫描通过

---

## 相关文档

- **角色与门禁**: doc/policies/roles.md
- **测试准则**: doc/process/testing.md
- **安全规范**: doc/policies/safety.md
- **命令参考**: doc/reference/commands.md

---

**维护**: PR流程变更时更新

