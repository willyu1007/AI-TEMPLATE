# 变更日志（Changelog）

## 目标
记录模块的所有版本变更，便于追踪历史和理解演进。

## 适用场景
- 了解版本差异
- 追踪功能演进
- 生成 Release Notes

## 使用说明
1. 遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/) 规范。
2. 版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)（Semver）
3. 按时间倒序排列（最新在前）
4. 每次发布前更新

---

## [Unreleased]

### 计划中
- 添加更多示例代码
- 完善测试用例
- 增加性能基准测试

---

## [1.0.0] - 2025-11-04

### Added（新增）
**文档系统**：
- 初始化模块结构
- 创建 8 个必备文档：
  - `README.md`：模块概述和架构说明
  - `plan.md`：任务计划模板
  - `CONTRACT.md`：接口契约定义
  - `TEST_PLAN.md`：测试计划和用例
  - `RUNBOOK.md`：运维手册和故障排查
  - `PROGRESS.md`：进度跟踪和里程碑
  - `BUGS.md`：缺陷管理和复盘
  - `CHANGELOG.md`：变更日志（本文件）

**测试框架**：
- 集成测试脚手架
- 添加冒烟测试示例
- 配置 pytest fixtures

**文档增强**：
- 所有文档添加目标和适用场景
- 补充详细的验证步骤
- 完善回滚逻辑说明

**自动化**：
- 集成到 `make ai_begin` 命令
- 添加文档一致性检查
- 添加文档风格预检

### Changed（变更）
- 无

### Deprecated（弃用）
- 无

### Removed（移除）
- 无

### Fixed（修复）
- 无

### Security（安全）
- 无

---

## 变更类型说明

| 类型 | 说明 | 版本影响 |
|------|------|---------|
| **Added** | 新增功能 | MINOR 或 MAJOR |
| **Changed** | 现有功能变更 | MINOR 或 MAJOR |
| **Deprecated** | 标记即将移除的功能 | MINOR |
| **Removed** | 已移除的功能 | MAJOR |
| **Fixed** | Bug 修复 | PATCH |
| **Security** | 安全相关修复 | PATCH 或 MINOR |

---

## 版本号规范

### Semver 格式
```
MAJOR.MINOR.PATCH

示例：
1.0.0 → 1.0.1  (Bug 修复)
1.0.1 → 1.1.0  (新功能，向后兼容)
1.1.0 → 2.0.0  (破坏性变更)
```

### 版本升级规则
1. **PATCH**: Bug 修复，完全向后兼容
2. **MINOR**: 新增功能，向后兼容
3. **MAJOR**: API 变更，不向后兼容

---

## 维护指南

### 更新时机
1. **发布前**：整理本版本所有变更
2. **重要变更后**：立即更新 Unreleased 章节。
3. **定期**：每周回顾并整理

### 更新步骤
```
# 1. 编辑 CHANGELOG
vim modules/example/CHANGELOG.md

# 2. 添加变更内容到对应类型
# - Added: 新增功能
# - Fixed: Bug 修复
# - Changed: 功能变更
# - ...

# 3. 提交变更
git add modules/example/CHANGELOG.md
git commit -m "docs(example): 更新 CHANGELOG for v1.1.0"

# 4. 发布时创建标签
git tag -a v1.1.0 -m "Release version 1.1.0"
git push --tags
```

---

## 相关文档
- **进度跟踪**: `PROGRESS.md`
- **缺陷管理**: `BUGS.md`
- **测试计划**: `TEST_PLAN.md`
- **版本管理**: `docs/project/RELEASE_TRAIN.md`

