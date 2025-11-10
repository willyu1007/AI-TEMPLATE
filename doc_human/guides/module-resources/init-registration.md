# 模块初始化 - Phase 4: 注册模块

> **所属**: MODULE_INIT_GUIDE.md Phase 4  
> **用途**: Phase 4的详细执行指南  
> **目标**: 将模块注册到registry.yaml

---

## 目标

将新模块注册到`doc/orchestration/registry.yaml`，建立模块关系

---

## 4.1 编辑registry.yaml

打开`doc/orchestration/registry.yaml`，在`module_instances`下添加：

```yaml
module_instances:
  - entity: <entity>
    version: "v1"
    description: "<模块功能描述>"
    type: "<模块类型，如1_Assign/user>"
    level: 1
    agent_path: /modules/<entity>/agent.md
    readme_path: /modules/<entity>/README.md
    plan_path: /modules/<entity>/plan.md
    
    # 依赖关系
    upstream:
      - common.models.base
      # - modules.<other>.v1  # 如有依赖
    downstream:
      - orchestrator.main    # 或其他下游
    
    # 输入输出
    inputs:
      - name: <input_name>
        description: "<描述>"
    outputs:
      - name: <output_name>
        description: "<描述>"
    
    # 状态
    status: "planning"  # planning|development|testing|deployed
    maturity: "alpha"   # alpha|beta|stable
```

---

## 4.2 填写说明

**entity** (必需):
- 模块名称，与目录名一致
- 小写+下划线，如`user_auth`

**type** (必需):
- 格式：`<类型ID>/<entity>`
- 示例：`1_Assign/user`, `2_Select/search`
- 参考：`MODULE_TYPE_CONTRACTS.yaml`

**level** (必需):
- 1-4的整数
- Level 1: 基础服务
- Level 2: 核心业务
- Level 3: 组合业务
- Level 4: 聚合服务

**upstream/downstream** (必需):
- 列出所有上下游依赖
- 格式：`modules.<entity>.v1` 或 `common.<module>`

**status** (必需):
- planning: 规划中
- development: 开发中
- testing: 测试中
- deployed: 已部署

---

## 4.3 验证注册

运行registry检查：

```bash
make registry_check
```

期望输出：
```
✓ Registry YAML格式正确
✓ 所有模块路径有效
✓ 依赖关系无循环
✓ 类型定义存在
```

---

## 常见问题

### Q: 如何确定upstream和downstream？
**A**: 
- upstream: 该模块调用的其他模块
- downstream: 调用该模块的其他模块

参考：`MODULE_TYPE_CONTRACTS.yaml`中的关系图

### Q: status应该填什么？
**A**: 新建模块填`planning`。随着开发推进逐步更新为`development`、`testing`、`deployed`。

### Q: inputs和outputs必须填吗？
**A**: 建议填写。如果暂时不清楚，可以先填占位符，后续在Phase 6补充完善。

---

## AI执行规范

**必须做**:
- ✅ 添加到registry.yaml的module_instances下
- ✅ 填写所有必需字段
- ✅ 运行`make registry_check`验证
- ✅ 如果检查失败，修复后再继续

**不要做**:
- ❌ 不要直接修改reference_modules
- ❌ 不要跳过registry_check
- ❌ 不要留空必需字段

---

## 下一步

完成注册后，进入 → [Phase 5: 校验](init-validation.md)

