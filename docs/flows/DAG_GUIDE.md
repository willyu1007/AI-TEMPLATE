# DAG 管理指引

## 目标
维护系统/模块级的有向无环图（DAG），明确依赖关系和数据流。

## 适用场景
- 定义系统架构拓扑
- 规划模块依赖关系
- 设计数据流和处理流程

## 前置条件
- 了解系统整体架构
- 明确模块边界和职责
- 已定义接口契约

## DAG 节点声明

每个节点必须包含以下字段：

### 必填字段
1. **id**：节点唯一标识（格式：`<domain>.<name>`）
2. **kind**：节点类型（`app`, `service`, `data`, `external`）
3. **inputs**：输入数据列表
4. **outputs**：输出数据列表

### 可选字段
- **sla**：服务等级协议（如 `p95_latency_ms: 2000`）
- **version**：节点版本
- **contracts**：契约文件引用

**示例**：
```yaml
nodes:
  - id: web.frontend
    kind: app
    inputs: [route, user_session]
    outputs: [payload, events]
    version: "1.0.0"
    
  - id: api.user_service
    kind: service
    inputs: [http_request]
    outputs: [http_response]
    contracts: { file: "tools/user-api/contract.json" }
    sla: { p95_latency_ms: 200 }
```

## DAG 边声明

**格式**：
```yaml
edges:
  - from: web.frontend
    to: api.user_service
    when: route == "/api/users"  # 可选条件
```

## 核心约束

### 1. 禁止有环
**要求**：DAG 必须无环，否则 `make dag_check` 会失败

**检测方式**：拓扑排序

### 2. 引用文件必须存在
**要求**：
- `contracts.file` 指向的文件必须存在
- 被引用的节点必须在 `nodes` 中声明

## 验证步骤

```bash
# 1. 语法检查
yamllint flows/dag.yaml

# 2. DAG 校验
make dag_check

# 预期输出：
# ✅ 无重复节点
# ✅ 无环路
# ✅ 所有边引用有效
# ✅ 契约文件存在
```

## 维护流程

### 1. 添加新节点
1. 在 `flows/dag.yaml` 的 `nodes` 中添加节点定义
2. 添加必要的边
3. 运行 `make dag_check` 验证
4. 运行 `make docgen` 更新索引

### 2. 修改节点
1. 更新节点定义
2. 检查是否影响下游节点
3. 运行 `make dag_check` 验证
4. 更新相关文档

### 3. 删除节点
1. 检查是否有其他节点依赖
2. 删除相关的边
3. 删除节点定义
4. 运行 `make dag_check` 验证

## 回滚逻辑

如果 DAG 变更导致问题：

1. **识别问题**
   ```bash
   make dag_check
   # 查看错误信息
   ```

2. **回滚变更**
   ```bash
   git checkout HEAD~1 -- flows/dag.yaml
   make dag_check
   ```

3. **验证修复**
   ```bash
   make dev_check
   ```

## 相关文档
- DAG 定义：`flows/dag.yaml`
- 契约文件：`tools/*/contract.json`
- 系统边界：`docs/project/SYSTEM_BOUNDARY.md`

