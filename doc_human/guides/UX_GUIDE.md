# UX 与使用流程规范

## 目标
规范用户界面设计和交互流程，确保一致的用户体验和清晰的系统行为。

## 适用场景
- 前端页面设计
- 用户流程规划
- API 调用序列设计

## 前置条件
- 产品需求已明确（见 `docs/project/PRD_ONEPAGER.md`）
- 系统架构已定义（见 `flows/dag.yaml`）
- API 契约已制定（见 `tools/*/contract.json`）

## 核心规范

### 1. 页面命名与路由

**命名规则**：
- 使用小写字母和连字符
- 反映页面功能和层次
- 保持简洁清晰

**路由结构**：
```
/                       # 首页
/login                  # 登录页
/dashboard              # 控制面板
/users                  # 用户列表
/users/:id              # 用户详情
/users/:id/edit         # 编辑用户
```

### 2. 状态管理约定

#### 加载状态
- **初始状态**：`idle`
- **加载中**：`loading`
- **成功**：`success`
- **失败**：`error`

**实现示例**：
```
interface PageState {
  status: 'idle' | 'loading' | 'success' | 'error'
  data: any | null
  error: Error | null
}
```

#### 错误处理
**必须展示的信息**：
1. 错误类型（网络/权限/数据）
2. 用户友好的错误提示
3. 建议的操作（重试/联系支持）

**示例**：
```
if (error.code === 'NETWORK_ERROR') {
  showMessage('网络连接失败，请检查网络后重试')
} else if (error.code === 'UNAUTHORIZED') {
  showMessage('登录已过期，请重新登录')
  redirectTo('/login')
}
```

### 3. API 调用序列

#### 重试策略
```
// 指数退避重试
const retryConfig = {
  maxRetries: 3,
  initialDelay: 1000,  // 1秒
  multiplier: 2,       // 每次翻倍
  // 重试间隔：1s, 2s, 4s
}
```

#### 降级策略
```
// 示例：API 不可用时使用缓存数据
async function fetchUserData(userId: string) {
  try {
    return await api.getUser(userId)
  } catch (error) {
    if (cache.has(userId)) {
      console.warn('API 不可用，使用缓存数据')
      return cache.get(userId)
    }
    throw error
  }
}
```

### 4. 用户流程图

使用 Mermaid 绘制关键流程：

**登录流程示例**：
```
flowchart TD
    A[用户访问登录页] --> B{是否已登录}
    B -->|是| C[重定向到首页]
    B -->|否| D[展示登录表单]
    D --> E[用户输入账号密码]
    E --> F{验证}
    F -->|成功| G[保存 Token]
    F -->|失败| H[展示错误提示]
    G --> I[重定向到首页]
    H --> D
```

### 5. 交互规范

#### 响应时间要求
- **即时反馈**：< 100ms（按钮点击、输入）
- **快速操作**：< 1s（表单提交、页面切换）
- **常规操作**：< 3s（数据加载、搜索）
- **复杂操作**：提供进度提示

#### 加载指示
```
操作时长 < 1s：无需加载指示
操作时长 1-3s：显示 Loading 动画
操作时长 > 3s：显示进度百分比
```

## 验证步骤

### 1. 流程验证
```
# 手动测试关键用户流程
1. 登录流程
2. 核心业务流程
3. 错误处理流程
```

## 2. 性能验证
```
# 使用开发者工具测试
1. 页面加载时间（Lighthouse）
2. API 响应时间
3. 交互响应性
```

## 3. 兼容性验证
```
测试浏览器：
- [ ] Chrome 最新版
- [ ] Firefox 最新版
- [ ] Safari 最新版

测试分辨率：
- [ ] 1920x1080（桌面）
- [ ] 1366x768（笔记本）
- [ ] 768x1024（平板）
```

---

## 数据流追踪与验证

### 数据流追踪要求

在 AI 自动化开发过程中，确保 UX 文档与实际代码实现保持一致：

1. **API 端点一致性**
   - UX 文档中提到的 API 端点必须在代码中存在
   - API 端点变更时，必须同步更新 UX 文档

2. **流程图一致性**
   - 用户流程图应反映实际的数据流转
   - 接口调用序列应与代码实现匹配

3. **DAG 关联性**
   - UX 文档中的流程应与 `flows/dag.yaml` 中的节点和边对应
   - 数据流向应保持一致

### 验证步骤

```bash
# 检查 UX 数据流转文档一致性
make dataflow_check

# 预期输出：
# ✓ 文档结构完整
# ✓ 未发现明显的不一致
```

## 维护流程

1. **开发阶段**
   - 修改用户流程时，同步更新 `docs/ux/*.md`
   - 新增 API 端点时，在 UX 文档中记录

2. **验证阶段**
   - 运行 `make dataflow_check` 检查一致性
   - 修复发现的不一致问题

3. **审查阶段**
   - 在 PR 审查时，检查 UX 文档是否更新
   - 验证流程图是否反映实际实现

### 数据流追踪最佳实践

1. **使用 Mermaid 绘制流程图**
   - 使用 `flowchart` 绘制用户流程
   - 使用 `sequenceDiagram` 绘制 API 调用序列

2. **保持文档更新**
   - 每次流程变更后立即更新文档
   - 定期审查文档与代码的一致性

3. **关联 DAG**
   - 在 UX 文档中引用 DAG 节点
   - 确保数据流向与 DAG 一致

---

## 相关文档
- 产品需求：`docs/project/PRD_ONEPAGER.md`
- 系统边界：`docs/project/SYSTEM_BOUNDARY.md`
- API 契约：`tools/*/contract.json`
- DAG 定义：`flows/dag.yaml`
- AI 自动化审计：`docs/project/AI_AUTOMATION_AUDIT.md`

