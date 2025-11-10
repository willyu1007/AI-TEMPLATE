# 上下文索引规则

> **用途**: 定义.aicontext/的生成和使用规则
> **版本**: 1.0
> **创建时间**: 2025-11-07

---

## .aicontext/ 目录作用

### 目标
为智能体提供快速索引，避免遍历整个代码库：
- 收录文件路径和摘要
- 标注主题标签
- 提供依赖关系图

### 非目标
❌ 不替代原文档（只是索引）
❌ 不收录代码实现（只收录接口）
❌ 不收录二进制和生成物

---

## 收录规则

### 必须收录
✅ **文档索引**
- README.md、agent.md的摘要
- CONTRACT.md、CHANGELOG.md的路径
- doc/下的所有规范文档

✅ **API接口**
- OpenAPI规范（tools/openapi.json）
- 公共函数签名
- 模型定义（common/models/）

✅ **依赖关系**
- 模块注册表（doc/orchestration/registry.yaml）
- DAG拓扑（flows/dag.yaml）
- 模块间依赖（从agent.md提取）

### 禁止收录
❌ **二进制文件**
- 图片、视频、音频
- 编译产物（.pyc, .so, .dll）
- 压缩包

❌ **生成物**
- node_modules/, venv/, __pycache__/
- dist/, build/, target/
- .aicontext/ 自身

❌ **敏感信息**
- 密钥、Token
- 配置文件中的密码
- 生产环境的连接串

---

## 大文件处理

### 切片策略
对于大文件（>500KB），按主题切片：

```yaml
# .aicontext/large_files.yaml
- file: modules/user/core/service.py
  size: 1.2MB
  slices:
    - lines: 1-200
      topic: "用户认证"
      summary: "实现基于JWT的用户认证逻辑"
    - lines: 201-500
      topic: "用户授权"
      summary: "实现基于RBAC的权限检查"
    - lines: 501-800
      topic: "用户CRUD"
      summary: "实现用户的增删改查"
```

### 标签系统
为每个切片添加标签：

```yaml
tags:
  - module:user
  - domain:auth
  - level:core
  - lang:python
```

---

## 索引生成

### 自动生成
使用docgen脚本：

```bash
make docgen
```

生成内容：
- .aicontext/summary.yaml - 文件摘要
- .aicontext/keywords.yaml - 关键词索引
- .aicontext/deps.yaml - 依赖关系
- .aicontext/hash.yaml - 文件哈希（检测变更）

### 增量更新
只更新有变更的文件：

```bash
make docgen  # 自动检测变更
```

检测方法：
1. 对比文件哈希
2. 只处理变更的文件
3. 更新对应索引条目

---

## 使用场景

### 场景1: 智能体启动
读取索引快速了解项目：

```
1. 读取 .aicontext/summary.yaml
2. 获取模块列表和摘要
3. 读取 doc/orchestration/registry.yaml
4. 构建项目全景图
```

### 场景2: 搜索相关文档
根据任务类型查找：

```python
# 伪代码
task = "修改用户认证逻辑"
keywords = ["用户", "认证", "auth"]

# 从keywords.yaml搜索
results = search_by_keywords(keywords)
# → modules/user/core/service.py (lines 1-200)
# → modules/user/doc/CONTRACT.md
# → common/middleware/auth.py
```

### 场景3: 依赖分析
查找模块依赖：

```yaml
# 从 .aicontext/deps.yaml
module: user.v1
depends_on:
  - common.models.base
  - common.middleware.auth
  - db.engines.postgres
depended_by:
  - app.frontend.pages.login
  - modules.admin.v1
```

---

## 索引格式

### summary.yaml
```yaml
files:
  - path: modules/user/README.md
    summary: "用户模块，提供用户认证、授权、CRUD功能"
    last_modified: "2025-11-07"
    hash: "a1b2c3d4"
  - path: modules/user/agent.md
    summary: "用户模块的Agent配置"
    agent_id: "modules.user.v1"
    level: 1
    hash: "e5f6g7h8"
```

### keywords.yaml
```yaml
keywords:
  "认证":
    - modules/user/core/service.py:1-200
    - common/middleware/auth.py
  "数据库":
    - db/engines/postgres/doc/README.md
    - doc/db/DB_SPEC.yaml
```

### deps.yaml
```yaml
dependencies:
  "modules.user.v1":
    upstream:
      - common.models.base
      - db.engines.postgres
    downstream:
      - app.frontend.login
```

---

## 维护

### 定期更新
建议在以下时机运行`make docgen`：
- 提交代码前
- CI构建时
- 每天定时任务

### 手动检查
检查索引是否准确：

```bash
# 检查是否有遗漏的文档
find . -name "*.md" -not -path "./.aicontext/*" | while read file; do
  grep -q "$file" .aicontext/summary.yaml || echo "Missing: $file"
done
```

### 清理陈旧条目
删除已不存在的文件索引：

```bash
# docgen脚本会自动清理
make docgen
```

---

## 最佳实践

### 1. 保持索引最新
- 在pre-commit hook中运行docgen
- CI中检查索引是否最新

### 2. 合理使用标签
- 标签要有意义（module:user, domain:auth）
- 不要过度细分（避免tag爆炸）
- 统一标签命名规范

### 3. 文件摘要撰写
- 简洁明了（1-2句话）
- 突出核心功能
- 包含关键词

### 4. 大文件切片
- 按逻辑功能切片（不按固定行数）
- 每个切片100-500行
- 提供清晰的topic

---

## 相关工具

### docgen.py
生成.aicontext/索引：

```bash
make docgen
# 或
python scripts/docgen.py
```

### codebase_search（AI工具）
使用索引搜索代码库：

```
Query: "用户认证逻辑在哪里"
↓ 使用 .aicontext/keywords.yaml
Result: modules/user/core/service.py (lines 1-200)
```

---

## 未来扩展

### 计划支持
- [ ] 代码调用关系图（call graph）
- [ ] 函数签名索引
- [ ] 测试覆盖率索引
- [ ] 性能热点标注

### 不计划支持
- ❌ 全文搜索（使用grep/ripgrep更快）
- ❌ 代码执行（非索引职责）
- ❌ 实时更新（按需生成即可）

---

**维护**: 索引规则变更时，更新本文档并更新docgen.py
**相关**: scripts/docgen.py, doc/policies/goals.md

