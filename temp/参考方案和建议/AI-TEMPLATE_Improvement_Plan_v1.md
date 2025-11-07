# AI‑TEMPLATE 改善方案（完整一一对应版）
版本：v1.0 · 生成时间：2025-11-06 10:44

> 目标：将“AI 友好 + 模块化 + 自动化 + 可编排”落到仓库结构与文档中。本文按**现状问题 → 设计原则 → 方案 → 落地动作 → 验收标准**的顺序逐项给出，便于直接执行与验收。

---

## 0. 快速结论（TL;DR）
- **核心设计**：README（人读）与 agent.md（模型/编排读）职责彻底分离；agent.md 采用 **YAML Front Matter + Markdown**，并由统一 Schema 校验；根级 agent.md 轻量，仅保留全局策略与**文档路由**；模块实例具备标准化骨架（`agent.md / README.md / plan.md / doc/`）；编排注册表 `doc/orchestration/registry.yaml` 统一描述**模块类型/实例/依赖/上下游**。  
- **自动化门禁**：三类校验脚本（Agent Schema / Registry DAG / 文档路由）+ GitHub Actions CI；本地 `make dev_check` 一键跑全套。  
- **并发治理**：以 `plan.md` 为准入门；未获批不得写码；冲突解决与合并顺序在 plan 中刚性声明。  
- **初始化**：项目与模块两套规范（`doc/init/*` 与 `doc/modules/*`），让大模型和人都能**按标准化流程**完成初始化。

---

## 1. 设计原则
1. **AI 友好**：文档可解析；上下文按需加载；路径路由清晰；避免冗长根文档。  
2. **模块化**：同类型可替换；实例独立；I/O 稳定。  
3. **自动化**：一切可校验、可脚本化、可 CI 化。  
4. **可编排**：Orchestrator 能自动读取/合并 agent.md，基于标签与约束做调度。  
5. **安全与质量**：默认最小权限；测试矩阵与覆盖率门槛前置。

---

## 2. 一一对应改进映射（Issue → Solution → Deliverable → Check）
> 下表列出**现状问题/诉求**与**改进方案**的逐项映射，以及在增强包中的**落地交付物**与**验收检查点**。

| # | 现状问题/诉求 | 解决方案（摘要） | 对应交付物/改动位置 | 验收检查 |
|---:|---|---|---|---|
| 1 | 根 `agent.md` 过重，污染上下文 | 根级**轻量化**：仅保留合并策略、全局目标/安全引用、文档路由 | `agent.md`（根，轻量版） | 体量显著下降；`agent_lint.py` 通过；上下文加载减少 |
| 2 | README 与 agent.md 职责交叉 | **职责切分**：README=语义地图（人读）；agent.md=角色与约束（模型读） | 各级 `README.md` 模板 + 声明“编排请读 agent.md” | 抽查模块：README 不含编排细节；agent.md 可被解析 |
| 3 | 缺少统一可解析规范 | **YAML Front Matter + Schema**，强校验 | `schemas/agent.schema.yaml` + `scripts/agent_lint.py` | CI 通过；必填字段齐全；类型/范围合法 |
| 4 | 模块实例无标准化骨架 | **标准骨架**：`agent.md / README.md / plan.md / doc/` | `modules/example/*` 样例与模板 | 新建模块按模板复制即可运行校验 |
| 5 | 模块关系与依赖分散 | **编排注册表**集中描述类型/实例/依赖/上下游 | `doc/orchestration/registry.yaml` + `registry_check.py` | DAG 无环；引用存在且唯一 |
| 6 | 文档路由缺失 | 在 agent.md 的 `context_routes` 中声明**必读/按需/按范围** | 根与模块 `agent.md` 的 YAML | `doc_route_check.py` 全绿；路径存在 |
| 7 | 初始化不可操作 | **两套规范**：项目初始化与模块初始化 | `doc/init/PROJECT_INIT_GUIDE.md`、`doc/modules/MODULE_INIT_GUIDE.md` | 按指南执行能产出可校验结构 |
| 8 | 并发开发易冲突 | **plan.md 准入制**：执行人、锁定路径、合并顺序、破坏性变更标记 | 各模块 `plan.md` 模板 | 无 plan 禁止合并；冲突处理有据可依 |
| 9 | 自动化门禁不足 | **三脚本 + CI**：Schema / Registry / 路由 校验，并纳入 Actions | `.github/workflows/ci.yml` | PR 必过三关；失败阻塞合并 |
|10 | 上下文索引不一致 | `.aicontext/` 收敛规则与路由策略 | `doc/indexes/context-rules.md` | 索引只收录必要文本；避免二进制污染 |
|11 | 安全与质量无统一阈值 | **统一门槛**：权限白名单、测试矩阵、覆盖率阈值 | `doc/policies/goals.md`、`doc/policies/safety.md` | 质量门槛对齐；变更触发合同/兼容检查 |

> 注：表内交付物均已在增强包结构中给出对应文件与样例，便于复制套用。

---

## 3. 目录与文档规范（落地形态）
### 3.1 根目录
- `agent.md`（轻量）：合并策略=子级覆盖父级；全局目标/安全文档引用；`context_routes` 给出**按范围**的文档读取建议。  
- `README.md`：地图、入口、安装、示例；第二段明确**编排/大模型请读 agent.md**。

### 3.2 模块实例目录
```
modules/<entity>/
├─ agent.md      # 可解析（YAML+MD），声明角色/I-O/依赖/权限/路由
├─ README.md     # 人读，使用与结构说明
├─ plan.md       # 执行与并发治理清单
└─ doc/
   ├─ CONTRACT.md
   ├─ TEST_PLAN.md
   ├─ RUNBOOK.md
   ├─ CHANGELOG.md
   ├─ PROGRESS.md
   └─ BUGS.md
```

### 3.3 编排注册与策略
- `doc/orchestration/registry.yaml`：记录**模块类型、实例名、路径、上下游、版本、状态**。  
- `doc/orchestration/routing.md`：合并与路由规则（子覆盖父；按需加载）。

---

## 4. agent.md v2 规范（要点）
- **结构**：`YAML Front Matter`（必含 `spec_version / agent_id / role` 等） + 正文（Summary、Responsibilities、Limitations、I/O 示例、SLO、Runbook 链接）。  
- **关键字段**：  
  - `ownership.code_paths`：可改动范围（最小权限）。  
  - `tools_allowed`：调用白名单（API/模型/IO）。  
  - `quality_gates`：测试类型与覆盖率阈值。  
  - `orchestration_hints`：触发、路由标签、优先级。  
  - `context_routes`：**always_read / on_demand / by_scope** 三层路由。  
- **合并策略**：Orchestrator 自下而上合并，**子级覆盖父级**。  
- **校验**：由 `agent_lint.py` 读取 YAML 前言并按 `schemas/agent.schema.yaml` 做 jsonschema 校验。

---

## 5. 初始化流程（项目 / 模块）
### 5.1 项目初始化（标准流程）
1. **信息收集**：目标、范围、非目标、质量与合规门槛。  
2. **生成骨架**：落地根 `agent.md`（轻量）与 `/doc/*`。  
3. **编排登记**：初始化 `registry.yaml`。  
4. **第一次校验**：`make dev_check`。  
5. **清理**：初始化完成后删除 `init/` 与 `TEMPLATE_USAGE.md`。  
> 详见 `doc/init/PROJECT_INIT_GUIDE.md`。

### 5.2 模块初始化（标准流程）
1. **生成目录**：`modules/<entity>/` 下创建标准四件套。  
2. **需求冻结**：需求文档（若有）入 `doc/`；无则新建后迭代至可执行。  
3. **补齐 agent.md**：填写 YAML 必填项与路由。  
4. **注册编排**：在 `registry.yaml` 登记类型/实例/上下游。  
5. **准入**：提交 `plan.md` 并获批后再写码。  
6. **校验**：`make dev_check` 全绿。  
> 详见 `doc/modules/MODULE_INIT_GUIDE.md`。

---

## 6. 并行开发与冲突治理（plan.md 要求）
- **必填**：`assignee / reviewers / code_paths.lock / breaking_change / merge_order / conflict_resolution`。  
- **规则**：  
  - 未提交或未通过的 `plan.md` → **禁止合并**；  
  - 破坏性变更需声明兼容策略（双栈/灰度/回滚路径）。  
- **CI 钩子**：可按需将 plan 校验加入 `make dev_check`（建议）。

---

## 7. 自动化校验与 CI
- `scripts/agent_lint.py`：YAML 前言解析 + Schema 校验。  
- `scripts/registry_check.py`：实例唯一、引用完整、**DAG 无环**。  
- `scripts/doc_route_check.py`：`context_routes` 指向路径有效。  
- `.github/workflows/ci.yml`：三脚本 + 自定义 `make dev_check`。  
- **通过标准**：  
  - 新增/修改任意模块，三脚本均需绿；  
  - 失败即阻塞 PR 合并。

---

## 8. 验收矩阵（Checklist）
**仓库级（Root）**
- [ ] 根 `agent.md` 为轻量版，含合并策略与路由；无大段流程性内容  
- [ ] `schemas/agent.schema.yaml` 存在且字段与类型满足校验  
- [ ] `doc/orchestration/registry.yaml` 列举当前所有模块与关系  
- [ ] CI 成功跑通三校验

**模块级（每个模块实例）**
- [ ] 存在 `agent.md / README.md / plan.md / doc/*`  
- [ ] `agent.md` 的 `ownership.code_paths` 与 `tools_allowed` 合理  
- [ ] `doc/CONTRACT.md` 与 `doc/TEST_PLAN.md` 形成最小执行闭环  
- [ ] `plan.md` 已获批后才进入开发

---

## 9. 风险与回滚
- **风险**：首次拆分根文档带来引用缺失；注册表不完整导致编排断链；未声明权限导致工具调用受限。  
- **回滚**：保留原根文档副本；注册表增量维护；`tools_allowed` 采用白名单滚动收敛。  
- **缓解**：在 PR 首轮只做“结构与校验”改造，不动业务逻辑；CI 可允许短周期“警告模式”。

---

## 10. FAQ（执行过程中的常见问题）
- **Q**：为什么强调 YAML 前言？  
  **A**：便于 Orchestrator 与脚本稳定解析，减少提示词依赖。  
- **Q**：根 `agent.md` 放什么就够了？  
  **A**：合并策略、全局目标/安全引用、文档路由、最小限度的全局约束。  
- **Q**：如何判断是否需要新建模块实例？  
  **A**：当同类型出现“实现策略差异 + 可替换”时，落为新实例，并在注册表登记。  

---

## 11. 变更日志（本方案）
- v1.0：首版，一一对应映射 + 目录规范 + 初始化流程 + 校验与 CI + 并发治理。

> 备注：涉及模板与脚本的具体实现，均已在增强包内提供；本文不重复贴出大段样例，仅给出**定位与验收点**以便执行。
