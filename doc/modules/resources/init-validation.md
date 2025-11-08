# 模块初始化 - Phase 5: 校验

> **所属**: MODULE_INIT_GUIDE.md Phase 5  
> **用途**: Phase 5的详细执行指南  
> **目标**: 运行所有校验工具，确保模块符合规范

---

## 目标

运行所有校验工具，确保模块符合规范

---

## 5.1 运行完整校验

```bash
make validate
```

该命令会运行7个检查：
1. agent_lint - agent.md格式校验
2. registry_check - registry.yaml校验
3. doc_route_check - 文档路由校验
4. type_contract_check - 类型契约校验
5. doc_script_sync_check - 脚本同步检查
6. db_lint - 数据库文件校验（如有）
7. encoding_check - 编码检查

---

## 5.2 逐项校验

如果`make validate`失败，可以逐项排查：

### 5.2.1 agent.md校验

```bash
make agent_lint
```

常见问题：
- ❌ YAML Front Matter格式错误
- ❌ 必需字段缺失
- ❌ agent_id格式不正确

### 5.2.2 registry.yaml校验

```bash
make registry_check
```

常见问题：
- ❌ 模块未注册
- ❌ 路径不存在
- ❌ 依赖关系循环

### 5.2.3 文档路由校验

```bash
make doc_route_check
```

常见问题：
- ❌ context_routes中的路径不存在
- ❌ 文档引用错误

### 5.2.4 类型契约校验

```bash
make type_contract_check
```

常见问题：
- ❌ 模块类型未在CONTRACTS.yaml中定义
- ❌ IO定义与类型契约不匹配

---

## 5.3 修复问题

根据校验输出修复问题，常见修复：

**YAML格式问题**:
```bash
# 使用yamllint检查
yamllint modules/<entity>/agent.md
```

**路径问题**:
```bash
# 检查文件是否存在
ls -la modules/<entity>/README.md
ls -la modules/<entity>/doc/CONTRACT.md
```

**依赖问题**:
```bash
# 检查registry.yaml中的依赖模块是否存在
grep -A 5 "upstream" doc/orchestration/registry.yaml
```

---

## 5.4 全部通过

当所有检查都通过时：

```bash
$ make validate
✓ agent_lint: 1/1 通过
✓ registry_check: 通过
✓ doc_route_check: 23/23 路由有效
✓ type_contract_check: 通过
✓ doc_script_sync_check: 无孤儿脚本
✓ db_lint: 所有检查通过
✓ encoding_check: 通过

所有检查通过 ✓
```

---

## 常见问题

### Q: agent_lint失败，提示YAML解析错误？
**A**: 检查：
1. YAML缩进是否正确（使用空格，不用Tab）
2. 字符串是否需要引号
3. 列表格式是否正确

### Q: registry_check失败，提示路径不存在？
**A**: 检查：
1. agent_path, readme_path, plan_path是否正确
2. 文件是否已创建
3. 路径是否以`/`开头（绝对路径）

### Q: 可以跳过某些检查吗？
**A**: 不建议跳过。所有检查都是为了确保模块质量。如果确实需要跳过，可以单独运行通过的检查。

---

## AI执行规范

**必须做**:
- ✅ 运行`make validate`完整校验
- ✅ 修复所有失败的检查
- ✅ 确保所有检查都通过后再继续

**不要做**:
- ❌ 不要跳过任何失败的检查
- ❌ 不要继续到下一Phase如果校验未通过
- ❌ 不要修改校验脚本以绕过检查

---

## 下一步

所有校验通过后，可以选择：
- → [Phase 6: 数据库变更](init-database.md)（如需要）
- → [Phase 7: 定义测试数据](init-testdata.md)（推荐）
- → 跳过到Phase 9完成初始化

