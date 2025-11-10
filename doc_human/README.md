# doc_human/ - 人类开发者文档

> **用途**: 为人类开发者提供详细、完整的文档
> **特点**: 支持中文、包含完整示例、深度解释

---

## 目录结构

```
doc_human/
├── guides/           # 完整指南
├── policies/         # 详细策略文档
├── project/          # 项目文档
├── init/             # 初始化指南
├── adr/              # 架构决策记录
├── architecture/     # 架构文档
├── reference/        # 参考手册
├── templates/        # 模板文件
└── examples/         # 示例代码
```

## 使用说明

### 主要文档分类

#### 1. guides/ - 操作指南
完整的操作手册，包含：
- `CONVENTIONS.md` - 编码规范大全
- `MODULE_INIT_GUIDE.md` - 模块初始化详细指南
- `GUARDRAIL_GUIDE.md` - 护栏机制完整说明
- `WORKDOCS_GUIDE.md` - 工作文档管理指南

#### 2. policies/ - 策略文档
中文版策略和详细说明：
- `goals-zh.md` - 项目目标（中文）
- `safety-zh.md` - 安全策略（中文）
- `quality_standards.md` - 质量标准详解
- `security_details.md` - 安全实施细节

#### 3. project/ - 项目文档
项目管理和规划文档：
- `PRD_ONEPAGER.md` - 产品需求文档
- `IMPLEMENTATION_SUMMARY.md` - 实施总结
- `RELEASE_TRAIN.md` - 发布计划

#### 4. init/ - 初始化资源
项目和模块初始化：
- `PROJECT_INIT_GUIDE.md` - 项目初始化指南
- `PROJECT_MIGRATION_GUIDE.md` - 项目迁移指南
- `resources/` - 初始化脚本和模板

#### 5. templates/ - 模板库
各种文档和代码模板：
- `module-templates/` - 模块文档模板
- `workdoc-*.md` - 工作文档模板
- `health-dashboard.html` - 健康度仪表板

## 文档特点

### 与doc_agent的区别

| 特性 | doc_human | doc_agent |
|------|-----------|-----------|
| 语言 | 中英文混合 | 纯英文 |
| 长度 | 不限制 | <200行 |
| 内容 | 详细完整 | 精简高效 |
| 示例 | 丰富示例 | 最小示例 |
| 受众 | 人类开发者 | AI代理 |

### 最佳实践

1. **学习路径**
   - 新手：先读 `guides/` 下的指南
   - 进阶：研究 `templates/` 和 `examples/`
   - 专家：参考 `adr/` 理解决策过程

2. **查找文档**
   - 操作方法 → `guides/`
   - 项目信息 → `project/`
   - 代码模板 → `templates/`
   - 最佳实践 → `examples/`

3. **贡献文档**
   - 保持中文文档的准确性
   - 提供实际案例和示例
   - 更新时同步修改相关文档

---

## 重要文档索引

### 必读文档
- [编码规范](guides/CONVENTIONS.md)
- [模块开发指南](guides/MODULE_INIT_GUIDE.md)
- [项目初始化](init/PROJECT_INIT_GUIDE.md)

### 参考文档
- [命令大全](reference/commands.md)
- [PR工作流](reference/pr_workflow.md)
- [架构决策](adr/README.md)

### 模板示例
- [模块示例](examples/module-example/)
- [文档模板](templates/module-templates/)
- [工作文档模板](templates/workdoc-plan.md)

---

**说明**: 
- AI代理请使用 `/doc_agent/` 目录
- 本目录专门为人类开发者优化
- 支持母语阅读，包含完整细节
