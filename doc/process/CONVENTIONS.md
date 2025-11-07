# 开发约定

## 目标
规范团队开发流程，确保代码质量和可追溯性。

## 适用场景
- 团队协作开发
- AI Agent 辅助开发
- 需要严格代码审查的项目

## 前置条件
- 团队成员已阅读 `agent.md`
- Git 工作流已配置
- CI/CD 已就绪

## 核心约定

### 1. 分支策略
- **主分支模型**：Trunk-based Development
- **功能分支**：短生命周期（< 2天）
- **命名规范**：`feature/<name>`, `fix/<name>`, `hotfix/<name>`

### 2. Pull Request 要求
必须包含以下内容：
1. **AI-SR 文档**：自审文档（`ai/sessions/<date>_<name>/AI-SR-impl.md`）
2. **测试证明**：所有测试通过的截图或日志
3. **文档更新**：相关模块文档已同步更新

### 3. 代码审查
参考 `agent.md` §11 三粒度审查流程

