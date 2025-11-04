# 贡献指南

感谢你对 Agent Repo 模板的关注！本文档说明如何贡献代码和反馈问题。

---

## 🐛 报告问题

### 提交 Issue 前
1. 搜索现有 Issues，避免重复
2. 使用最新版本重现问题
3. 准备详细的复现步骤

### Issue 模板
```markdown
## 问题描述
[清晰描述遇到的问题]

## 复现步骤
1. 执行命令：`make xxx`
2. 看到错误：...
3. 期望结果：...

## 环境信息
- OS: Windows 10 / macOS 14 / Ubuntu 22.04
- Python: 3.11
- 相关工具版本: ...

## 错误日志
```
[粘贴错误信息]
```

## 截图
[如适用]
```

---

## 💡 功能建议

### 建议模板
```markdown
## 功能描述
[描述建议的新功能]

## 使用场景
[说明哪些场景需要这个功能]

## 预期效果
[说明实现后的效果]

## 可选实现方案
[如有想法，可以提供]
```

---

## 🔧 提交代码

### 准备工作
```bash
# 1. Fork 仓库
# 2. 克隆你的 fork
git clone https://github.com/your-username/agent-repo-template.git
cd agent-repo-template

# 3. 添加上游仓库
git remote add upstream https://github.com/original-org/agent-repo-template.git

# 4. 创建开发分支
git checkout -b feature/your-feature-name
```

### 开发流程

#### 1. 遵循 agent.md 流程
```bash
# 如果是新模块
make ai_begin MODULE=your_module

# 更新计划
vim modules/your_module/plan.md

# 实现功能
# ... 编写代码 ...

# 添加测试
# ... 编写测试 ...

# 运行检查
make dev_check
```

#### 2. 代码规范
- **Python**: 遵循 PEP 8，使用 pylint
- **TypeScript**: 遵循 ESLint 规则
- **Go**: 遵循 Go 官方风格，使用 gofmt

**风格指南**: `.aicontext/style_guide.md`

#### 3. 提交信息
```bash
# 格式：<type>(<scope>): <subject>

# 示例
git commit -m "feat(scripts): 添加依赖自动检测功能"
git commit -m "fix(dag_check): 修复环路检测算法"
git commit -m "docs(readme): 更新快速开始说明"
```

**类型**：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

#### 4. 测试要求
```bash
# 必须满足
- [ ] 新功能有单元测试
- [ ] 测试覆盖率 ≥80%（核心代码）
- [ ] 所有测试通过
- [ ] make dev_check 通过
```

### 提交 PR

#### 1. 推送分支
```bash
git push origin feature/your-feature-name
```

#### 2. 创建 PR
- 使用 PR 模板填写完整信息
- 链接相关 Issue
- 添加截图（如适用）

#### 3. PR 标题
```
<type>(<scope>): <subject>

示例：
feat(scripts): 添加依赖自动检测功能
fix(dag_check): 修复环路检测算法
```

#### 4. PR 描述
使用 `.github/PULL_REQUEST_TEMPLATE.md` 模板：
- 变更说明
- 影响范围
- 测试结果
- 自审
- 文档更新

### Code Review

#### 作为提交者
- 响应 review 评论
- 及时修复问题
- 更新 PR 说明（如需要）

#### 作为审查者
参考 `agent.md` §11 代码审查流程：
- 🏗️ Repo 级：架构变更
- 📦 模块级：功能开发
- ⚙️ 代码级：代码质量

---

## 📋 贡献类型

### 代码贡献
- 新增脚本/工具
- Bug 修复
- 性能优化
- 测试补充

### 文档贡献
- 修正错误
- 补充说明
- 翻译（如需要）
- 示例代码

### 其他贡献
- 问题反馈
- 功能建议
- 使用反馈
- 传播推广

---

## 🎯 贡献重点方向

### 高价值贡献
1. **完善测试示例**
   - 更多语言的测试示例
   - 更多测试场景

2. **增强自动化工具**
   - 更智能的依赖检测
   - 更多的代码质量检查
   - 更好的错误提示

3. **丰富模板文档**
   - 更多行业的 PRD 示例
   - 更多场景的 RUNBOOK 模板

4. **CI/CD 集成**
   - 更多 CI 平台支持
   - 部署脚本示例

### 待改进领域
- 多语言支持（Rust, Java等）
- 性能测试框架
- 安全扫描增强
- 文档生成工具

---

## ✅ PR 合并标准

### 必须满足
1. ✅ CI 全部通过
2. ✅ 至少 1 人审查通过
3. ✅ 所有讨论已解决
4. ✅ 文档已更新
5. ✅ 测试覆盖充分

### 审查周期
- 小型 PR（<100 行）：1-2 天
- 中型 PR（100-500 行）：2-3 天
- 大型 PR（>500 行）：3-5 天（建议拆分）

---

## 🏆 贡献者

感谢所有贡献者！

[贡献者列表将在此处展示]

---

## 📞 联系方式

- **Issues**: [GitHub Issues](https://github.com/your-org/agent-repo-template/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/agent-repo-template/discussions)
- **Email**: [联系邮箱]

---

## 📜 行为准则

### 基本原则
- 尊重他人
- 建设性沟通
- 包容多样性
- 专注技术讨论

### 不可接受的行为
- 人身攻击
- 骚扰
- 发布他人隐私
- 不专业行为

---

## 📚 相关资源

- **开发指南**: `agent.md`
- **快速开始**: `QUICK_START.md`
- **模板使用**: `TEMPLATE_USAGE.md`
- **PR 规则**: `agent.md` §10.5
- **代码审查**: `agent.md` §11

---

**感谢你的贡献！** 🎉

