# 模块文档模板

> **用途**: 提供标准化的模块文档模板
> **使用时机**: 创建新模块时

---

## 模板列表

| 模板文件 | 用途 | 必需 |
|---------|------|------|
| CONTRACT.md.template | API契约定义 | ✅ 必需 |
| CHANGELOG.md.template | 变更记录 | ✅ 必需 |
| RUNBOOK.md.template | 运维手册 | ✅ 必需 |
| BUGS.md.template | 已知问题 | ✅ 必需 |
| PROGRESS.md.template | 进度追踪 | ✅ 必需 |
| TEST_PLAN.md.template | 测试计划 | ✅ 必需 |

---

## 使用方法

### 方式1: 通过脚本（推荐）

```bash
make ai_begin MODULE=<module-name>
```

脚本会自动：
1. 复制所有模板到 `modules/<module-name>/doc/`
2. 替换模板变量（`<Entity>`, `<entity>`, `<date>`）
3. 生成初始内容

### 方式2: 手动复制

```bash
# 创建模块doc目录
mkdir -p modules/<module-name>/doc

# 复制模板
cp doc/modules/TEMPLATES/*.template modules/<module-name>/doc/

# 重命名（去掉.template后缀）
cd modules/<module-name>/doc/
for f in *.template; do mv "$f" "${f%.template}"; done

# 手动替换变量
# 将所有文件中的 <Entity> 替换为实际模块名（如User）
# 将所有文件中的 <entity> 替换为实际模块名（如user）
# 将所有文件中的 <date> 替换为当前日期
```

---

## 模板变量

在使用模板时，需要替换以下变量：

| 变量 | 说明 | 示例 |
|------|------|------|
| `<Entity>` | 模块名（首字母大写） | User, Order, Product |
| `<entity>` | 模块名（小写） | user, order, product |
| `<date>` | 日期 | 2025-11-07 |
| `<name>` | 负责人姓名 | Zhang San |
| `<email>` | 邮箱 | zhangsan@example.com |

---

## 模板说明

### CONTRACT.md.template
定义模块的对外接口：
- API接口（HTTP）
- 内部函数接口（Python/Go/TS）
- 前端组件接口（如有）
- 数据模型
- 事件（如有）

### CHANGELOG.md.template
记录模块的所有变更：
- 遵循 [Keep a Changelog](https://keepachangelog.com/) 规范
- 按版本组织
- 分类：新增、变更、废弃、移除、修复、安全

### RUNBOOK.md.template
运维手册：
- 部署步骤
- 配置说明
- 监控指标
- 告警规则
- 故障处理
- 扩容/升级/回滚

### BUGS.md.template
已知问题追踪：
- 活跃问题
- 已解决问题
- 已知限制
- 技术债务
- 性能问题
- 安全问题

### PROGRESS.md.template
进度追踪：
- 里程碑
- 任务清单
- 时间线
- 风险与问题
- 团队信息

### TEST_PLAN.md.template
测试计划：
- 测试策略
- 单元测试
- 集成测试
- 契约测试
- E2E测试
- 性能测试
- 安全测试

---

## 自定义模板

如需添加新模板：

1. 在本目录创建 `<NAME>.md.template`
2. 使用模板变量（`<Entity>`, `<entity>` 等）
3. 更新本 README.md
4. 更新 `scripts/ai_begin.sh` 或 `MODULE_INIT_GUIDE.md`

---

## 模板维护

### 更新模板
当模板需要更新时：
1. 修改相应的 `.template` 文件
2. 在本README中记录变更
3. 通知团队更新现有模块

### 模板版本
- 当前版本：v1.0
- 最后更新：2025-11-07

---

## 相关文档

- **模块初始化指南**: doc/modules/MODULE_INIT_GUIDE.md
- **模块类型说明**: doc/modules/MODULE_TYPES.md
- **项目初始化指南**: doc/init/PROJECT_INIT_GUIDE.md

---

**维护**: 模板变更时更新
**审核**: 模板重大变更需团队评审

