# Safety & Quality Standards

> **Purpose**: Define safety constraints and quality requirements (core principles)  
> **Version**: 2.1  
> **Created**: 2025-11-07  
> **Last Updated**: 2025-11-09 (Phase 14.0.3)

---

## Quick Reference

### Safety Constraints Quick Lookup

| Category | Principle | Details |
|----------|-----------|---------|
| **Path Access** | Read: context_routes, Write: ownership scope | security_details.md § 1 |
| **Tool Calls** | Whitelist mechanism, default deny | security_details.md § 2 |
| **Database Ops** | Semi-automated, human review | security_details.md § 3 |
| **Network Access** | Default deny, explicit declaration | security_details.md § 4 |

### Quality Standards Quick Lookup

| Category | Requirement | Details |
|----------|-------------|---------|
| **Test Coverage** | ≥80% | quality_standards.md § 1 |
| **Doc Completeness** | 6 standard docs | quality_standards.md § 2 |
| **Compatibility** | Backward compatible | quality_standards.md § 3 |
| **Code Standards** | Naming + style + complexity | quality_standards.md § 4 |

---

## 1. Safety Constraints

### 1.1 Path Access Control
- ✅ Read Permission: context_routes + current module + public docs
- ✅ Write Permission: Only paths declared in ownership.code_paths
- ❌ No Unauthorized Access: Undeclared paths are denied by default

**Details**: `doc/policies/security_details.md` § 1

### 1.2 Tool & API Call Restrictions
- ✅ Whitelist Mechanism: Only tools declared in tools_allowed are permitted
- ❌ Default Deny: Undeclared tool calls are intercepted
- ⚠️ External API Requires Approval: External network access needs security team approval

**Details**: `doc/policies/security_details.md` § 2

### 1.3 Database Safety
- ✅ Semi-Automated: AI generates + human reviews + human executes
- ❌ No Direct DDL: AI cannot directly execute CREATE/ALTER/DROP
- ⚠️ 迁移脚本成对: 每个up必须有对应的down

**详见**: `doc/policies/security_details.md` § 3

### 1.4 网络访问控制
- ❌ 默认禁止: 模块不能访问网络
- ✅ 显式声明: 需要时在tools_allowed中声明
- ⚠️ 域名白名单: 仅允许访问声明的域名

**详见**: `doc/policies/security_details.md` § 4

---

## 2. 质量门槛

### 2.1 测试要求
- ✅ 必需测试: 单元测试、集成测试、契约测试
- ✅ 覆盖率要求: ≥80%（可配置更高）
- 校验: `make test_status_check`

**详见**: `doc/policies/quality_standards.md` § 1

### 2.2 文档要求
- ✅ 必需文档: 6个标准文档（CONTRACT/CHANGELOG/RUNBOOK/BUGS/PROGRESS/TEST_PLAN）
- ✅ 同步要求: 代码变更必须更新相关文档
- 校验: `make consistency_check`

**详见**: `doc/policies/quality_standards.md` § 2

### 2.3 兼容性要求
- ✅ API兼容: 不删除字段、不改类型、不改语义
- ✅ 数据库兼容: 迁移脚本成对、通过回滚测试
- 校验: `make contract_compat_check`, `make rollback_check`

**详见**: `doc/policies/quality_standards.md` § 3

### 2.4 代码规范
- ✅ 命名: 模块（蛇形）、类（大驼峰）、函数（蛇形/小驼峰）、常量（大写）
- ✅ 文档: 语言一致、无颜文字、结构化
- 校验: `make doc_style_check`

**详见**: `doc/policies/quality_standards.md` § 4

---

## 3. 违规处理

### 3.1 分阶段门槛

**开发阶段**（警告模式）:
- 不符合规范 → 显示警告
- 允许继续开发
- 提示需要修复

**提交阶段**（严格模式）:
- CI门禁检查
- 不通过 → 拒绝合并
- 必须修复后重新提交

**生产阶段**（强制模式）:
- 部署前最终检查
- 任何违规 → 阻断部署
- 人工审核关键变更

---

### 3.2 CI门禁

**必须通过的检查**:
```bash
make validate  # 聚合7个检查
make test      # 所有测试通过
coverage ≥80%  # 测试覆盖率达标
```

**高风险变更额外检查**:
```bash
make rollback_check  # 数据库变更需通过回滚测试
```

---

## 4. 豁免机制

### 4.1 何时申请

**适用场景**:
- 原型验证阶段（临时放宽测试覆盖率）
- 紧急修复（跳过部分流程）
- 技术限制（暂时无法满足）
- 迁移过渡期（新规范未全部适配）

**不适用**:
- ❌ 长期绕过规范
- ❌ 核心安全规范
- ❌ 数据安全相关

---

### 4.2 申请流程

**在agent.md中配置**:
```yaml
exemptions:
  - rule: "coverage_min"
    reason: "原型验证阶段"
    current_value: 0.60
    standard_value: 0.80
    expiry: "2025-12-31"
    approved_by: "tech_lead"
```

**审核要点**:
- ✅ 豁免理由充分？
- ✅ 豁免范围最小化？
- ✅ 到期时间合理？
- ✅ 有修复计划？

**到期处理**:
- 到期后自动失效
- CI会报错
- 需续期需重新申请

**详见**: `doc/policies/security_details.md` § 5

---

## 5. 审计与监控

### 5.1 审计范围

**记录内容**:
- 文件操作（read/write/delete）
- 工具调用（http/db/shell）
- 数据库操作（DDL/DML/DQL）
- 越权尝试（拦截记录）

**详见**: `doc/policies/security_details.md` § 6

---

### 5.2 监控指标

**关键指标**:
- 文档覆盖率（agent.md、CONTRACT.md存在率）
- 测试覆盖率（≥80%达标率）
- 校验通过率（dev_check通过率）
- 违规次数（越权尝试、工具滥用）

**报告生成**:
```bash
make ai_maintenance
# 输出: 未通过的校验项、缺失的文档、待修复的问题
```

**详见**: `doc/policies/security_details.md` § 6

---

## 6. 相关资源

### 核心策略
- **全局目标**: doc/policies/goals.md
- **角色与门禁**: doc/policies/roles.md

### 详细规范
- **安全详情**: doc/policies/security_details.md（路径控制、工具限制、审计监控）
- **质量标准**: doc/policies/quality_standards.md（测试、文档、兼容性、代码规范）

### 流程指南
- **数据库变更**: doc/process/DB_CHANGE_GUIDE.md
- **PR工作流**: doc/process/pr_workflow.md
- **测试准则**: doc/process/testing.md

### 工具参考
- **路由规则**: doc/orchestration/routing.md
- **初始化指南**: doc/init/PROJECT_INIT_GUIDE.md
- **模块初始化**: doc/modules/MODULE_INIT_GUIDE.md

---

**维护**: 发现新的安全风险时，及时更新本文档和详细说明文档  
**审核**: 每季度由安全团队审核一次
