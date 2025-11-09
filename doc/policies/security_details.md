---
audience: human
language: zh
version: complete
purpose: Documentation for security_details
---
# 安全规范详细说明

> **用途**: 安全约束和工具限制的详细说明  
> **版本**: 1.0  
> **创建时间**: 2025-11-08

---

## 1. 路径访问控制详解

### 1.1 读权限规则

**允许读取**:
1. `context_routes`中声明的所有路径
2. 当前模块的完整目录（如 modules/user/）
3. 公共文档目录（doc/、README.md、schemas/）
4. 配置文件（config/*.yaml）

**禁止读取**:
1. 其他模块的内部实现（除非在dependencies中声明）
2. 敏感配置文件（如含密钥的配置）
3. .git/目录
4. node_modules/、venv/等依赖目录

---

### 1.2 写权限规则

**ownership.code_paths配置**:
```yaml
ownership:
  code_paths:
    include:
      - modules/user/          # 允许写入user模块
      - tests/user/            # 允许写入user测试
      - doc/modules/user/      # 允许写入user文档（如有）
    exclude:
      - modules/*/doc/CHANGELOG.md  # 禁止直接改CHANGELOG
      - "**/*.sql"                   # 禁止直接改SQL
      - "db/engines/*/migrations/*"  # 禁止直接改迁移脚本
```

**规则说明**:
- ✅ include: 白名单，明确允许写入的路径
- ❌ exclude: 黑名单，即使在include中也禁止
- ⚠️ 未声明路径: 默认禁止写入

**校验机制**:
- AI尝试写入未声明路径时，应拦截并提示
- 人工确认后可临时授权
- 记录所有写操作到审计日志

---

### 1.3 路径访问示例

**示例1: 用户模块开发**
```yaml
# modules/user/agent.md
ownership:
  code_paths:
    include:
      - modules/user/**
      - tests/user/**
    exclude:
      - modules/user/doc/CHANGELOG.md
```

**允许操作**:
- ✅ 读取: modules/user/下所有文件
- ✅ 读取: doc/modules/MODULE_INIT_GUIDE.md（公共文档）
- ✅ 写入: modules/user/core/user_service.py
- ✅ 写入: tests/user/test_user.py

**禁止操作**:
- ❌ 写入: modules/order/（其他模块）
- ❌ 写入: modules/user/doc/CHANGELOG.md（exclude中）
- ❌ 写入: config/prod.yaml（敏感配置）

---

## 2. 工具与API调用限制详解

### 2.1 工具白名单机制

**tools_allowed配置**:
```yaml
tools_allowed:
  calls:
    # 文件系统
    - fs.read               # 读取文件
    - fs.write              # 写入文件（受ownership限制）
    - fs.list               # 列出目录
    
    # HTTP请求
    - http.get              # HTTP GET
    - http.post             # HTTP POST
    # - http.delete         # 默认禁止DELETE
    
    # 数据库
    - db.query              # 只读查询
    # - db.execute          # 默认禁止DDL/DML
    
    # 工具
    - shell.safe            # 安全shell命令（白名单）
    # - shell.raw           # 禁止任意shell命令
  
  models:
    - gpt-4
    - claude-3-sonnet
    # - gpt-3.5-turbo      # 如需使用需明确声明
```

**规则**:
- 注释掉的工具默认禁止
- 需要时在agent.md中声明
- 需人工审核批准

---

### 2.2 HTTP调用限制

**默认策略**: 禁止访问外部网络

**允许的HTTP调用**:
```yaml
tools_allowed:
  calls:
    - http.get
    - http.post
  
constraints:
  http:
    allowed_domains:
      - "*.internal.example.com"  # 内部API
      - "api.example.com"          # 公司API
    denied_domains:
      - "*"  # 默认拒绝所有外部域名
    
    rate_limit:
      max_requests_per_minute: 60
      max_requests_per_day: 1000
```

**审核流程**:
1. 模块需要访问外部API时，在agent.md中声明
2. 说明用途、频率、数据类型
3. 经安全团队审核
4. 批准后添加到allowed_domains

---

### 2.3 数据库操作限制

**查询操作**（db.query）:
```sql
-- ✅ 允许: SELECT查询（自动添加LIMIT）
SELECT * FROM users WHERE id = 123 LIMIT 100;

-- ❌ 禁止: 无LIMIT的大查询
SELECT * FROM users;  -- 可能返回数百万行

-- ❌ 禁止: 写操作
UPDATE users SET password = 'xxx';
DELETE FROM users;
```

**DDL/DML操作**（db.execute，默认禁止）:
```sql
-- ❌ 禁止: 直接执行DDL
CREATE TABLE new_table (...);
ALTER TABLE users ADD COLUMN xxx;

-- ✅ 替代方案: 通过半自动化流程
1. AI生成迁移脚本草案
2. 人工审核SQL
3. 人工执行 make db_migrate
```

---

## 3. 数据库安全详解

### 3.1 半自动化流程

**完整流程**:
```bash
# 1. AI生成DDL草案
AI: 分析需求 → 生成表YAML → 生成迁移脚本

# 2. 人工审核（必需）
Human: 检查SQL正确性 → 评估影响 → 确认执行

# 3. 执行迁移
make db_migrate  # 需要人工确认

# 4. 验证结果
make db_lint  # 校验表结构

# 5. 回滚测试（高风险变更）
make rollback_check PREV_REF=v1.0.0
```

---

### 3.2 危险操作保护

**Level 1: 警告级**（开发环境）
```sql
-- 以下操作会警告，但允许继续
ALTER TABLE users DROP COLUMN email;
UPDATE users SET status = 'inactive';
```

**Level 2: 确认级**（测试/预发环境）
```sql
-- 以下操作需要确认
DROP TABLE temp_users;
TRUNCATE TABLE logs;
```

**Level 3: 禁止级**（生产环境）
```sql
-- 以下操作绝对禁止AI执行
DROP TABLE users;
TRUNCATE TABLE orders;
DELETE FROM users;  -- 无WHERE条件
```

**保护机制**:
1. 环境识别（通过APP_ENV）
2. 操作分级（DDL、DML、DQL）
3. 二次确认（高危操作）
4. 审计日志（所有数据库操作）

---

### 3.3 迁移脚本规范

**成对原则**: 每个迁移必须有up和down
```bash
001_create_users_up.sql    # 创建表
001_create_users_down.sql  # 删除表（回滚）
```

**命名规范**:
```
<序号>_<描述>_<方向>.sql

序号: 001, 002, 003...（3位数字）
描述: 简短的英文描述（下划线分隔）
方向: up（执行）或 down（回滚）
```

**校验**:
```bash
make migrate_check  # 检查成对性
make rollback_check # 测试回滚
```

---

## 4. 网络访问控制详解

### 4.1 默认策略

**默认禁止**: 模块不能访问网络，除非显式声明

**声明方式**:
```yaml
# modules/<module>/agent.md
tools_allowed:
  calls:
    - http.get
    - http.post

constraints:
  - "只能访问内部API（*.internal.example.com）"
  - "禁止访问外部第三方API"
  - "最大请求频率: 60次/分钟"
```

---

### 4.2 外部API审核流程

**申请**:
1. 在agent.md中添加外部API声明
2. 说明用途、频率、数据类型
3. 提供API文档链接

**审核检查**:
- ✅ 用途是否合理？
- ✅ 是否有替代方案？
- ✅ 数据安全如何保证？
- ✅ 失败如何处理？
- ✅ 是否有速率限制？

**批准后**:
- 添加到allowed_domains
- 记录到doc/CHANGELOG.md
- 定期审查使用情况

---

### 4.3 网络调用示例

**示例1: 调用内部API**
```yaml
# modules/order/agent.md
tools_allowed:
  calls:
    - http.post

constraints:
  http:
    allowed_domains:
      - "payment.internal.example.com"
    endpoints:
      - "POST /api/v1/charge"
    max_requests_per_minute: 100
```

**示例2: 调用外部API**（需审核）
```yaml
# modules/weather/agent.md
tools_allowed:
  calls:
    - http.get

constraints:
  http:
    allowed_domains:
      - "api.openweathermap.org"
    endpoints:
      - "GET /data/2.5/weather"
    api_key_required: true
    max_requests_per_day: 1000
    
external_dependency:
  name: OpenWeatherMap API
  purpose: 获取天气信息
  review_status: approved
  approved_by: "security_team"
  approved_at: "2025-11-08"
```

---

## 5. 豁免机制详解

### 5.1 何时申请豁免

**适用场景**:
1. 原型验证阶段（临时放宽测试覆盖率）
2. 紧急修复（跳过部分流程）
3. 技术限制（某些规范暂时无法满足）
4. 迁移过渡期（新规范未全部适配）

**不适用**:
- ❌ 长期绕过规范
- ❌ 核心安全规范
- ❌ 数据安全相关

---

### 5.2 豁免配置

**在agent.md中配置**:
```yaml
exemptions:
  - rule: "coverage_min"
    reason: "原型验证阶段，暂时放宽覆盖率要求"
    current_value: 0.60
    standard_value: 0.80
    expiry: "2025-12-31"
    approved_by: "tech_lead"
    review_required: true
    
  - rule: "required_tests"
    reason: "e2e测试框架尚未搭建"
    exempted_tests: ["e2e"]
    expiry: "2025-12-15"
    approved_by: "qa_lead"
```

---

### 5.3 豁免审核

**申请流程**:
1. 在agent.md添加exemptions配置
2. 提交PR附上豁免说明
3. 相关负责人审核
4. 批准后合并

**审核要点**:
- ✅ 豁免理由是否充分？
- ✅ 豁免范围是否最小化？
- ✅ 到期时间是否合理？
- ✅ 是否有修复计划？

**定期审查**:
- 每月检查即将到期的豁免
- 到期后自动失效（CI会报错）
- 需续期需重新申请

---

## 6. 审计与监控详解

### 6.1 审计内容

**文件操作审计**:
```
记录内容:
- 时间戳
- 操作类型（read/write/delete）
- 文件路径
- 模块ID
- AI会话ID
- 是否越权（是否在ownership范围内）
```

**工具调用审计**:
```
记录内容:
- 时间戳
- 工具名称（http.get、db.query等）
- 调用参数
- 返回结果
- 是否在tools_allowed中
```

**数据库操作审计**:
```
记录内容:
- 时间戳
- SQL语句
- 影响行数
- 执行时长
- 是否需要人工确认
```

---

### 6.2 监控指标

**文档覆盖率**:
```bash
# 检查哪些模块缺少文档
make consistency_check

监控:
- agent.md存在率
- CONTRACT.md存在率
- 6个标准文档完整率
- 测试覆盖率
```

**校验通过率**:
```bash
# 运行所有校验
make dev_check

监控:
- 各项校验通过率
- 失败次数和类型
- 修复时长
```

**违规次数**:
```
监控:
- 越权访问尝试次数
- 未声明工具调用次数
- 数据库危险操作次数
```

---

### 6.3 监控报告

**ai_maintenance生成的报告**:
```markdown
# AI维护报告

## 1. 文档覆盖率
- agent.md: 5/5 (100%)
- CONTRACT.md: 5/5 (100%)
- 标准文档: 28/30 (93%)

## 2. 校验通过率
- agent_lint: 5/5 (100%)
- registry_check: 通过
- doc_route_check: 26/26 (100%)
...

## 3. 需要修复的问题
- [ ] module_A缺少TEST_PLAN.md
- [ ] module_B的测试覆盖率仅62%（< 80%）

## 4. 豁免到期提醒
- ⚠️ module_C的coverage_min豁免将于2025-11-15到期
```

---

## 7. 安全检查清单

### 新增模块时

- [ ] agent.md包含ownership.code_paths
- [ ] ownership范围最小化
- [ ] tools_allowed明确声明
- [ ] 无敏感信息硬编码
- [ ] 数据库操作符合规范

### 修改模块时

- [ ] 仅修改ownership范围内的文件
- [ ] 数据库变更通过半自动化流程
- [ ] 外部API调用已声明
- [ ] 测试覆盖率未降低

### 部署前

- [ ] 所有校验通过（make validate）
- [ ] 无活跃的豁免（或豁免已审核）
- [ ] 审计日志无异常
- [ ] 回滚方案已测试

---

**维护**: 发现新的安全风险时，及时更新本文档  
**审核**: 每季度由安全团队审核一次

