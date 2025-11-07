# AI-TEMPLATE 仓库改进执行计划（草案）

> 说明：本计划处于“草案”阶段，未获确认前将不会修改 temp 目录以外的任何文件或目录。

## 目标
- 完善仓库结构与自动化流程
- 提升文档体系的完整性、一致性与可读性
- 明确模块边界与贡献规范，降低维护成本

## 步骤与交付
1. 在根目录创建临时目录并建立计划与笔记（本步骤）
   - 交付：`temp/EXECUTION_PLAN.md`、`temp/READING_NOTES.md`
2. 系统梳理当前仓库结构与关键文档
   - 交付：结构图、自动化流程梳理、模块说明（记录于笔记）
3. 阅读与对齐外部需求文档：`/Volumes/DataDisk/Project/tmp/ai-template/完善模板和文档(需求文档).md`
   - 交付：需求要点对齐（记录于笔记）
4. 阅读改进建议：`/Volumes/DataDisk/Project/tmp/ai-template/修改和完善建议.md`
   - 交付：可落地建议列表（记录于笔记/计划）
5. 阅读与提炼：`/Volumes/DataDisk/Project/tmp/ai-template/AI-TEMPLATE_Improvement_Plan_v1.md` 及目录 `AI-TEMPLATE-Enhancement-Pack`
   - 交付：增强包可复用项与集成路径（记录于笔记/计划）
6. 汇总并与仓库现状对比，形成执行清单与改动方案，与您讨论确认
   - 交付：本计划文档中的“执行清单（建议）”章节
7. 获确认后，分阶段实施并回报进度
   - 交付：PR/变更列表、更新后的文档与脚本

## 里程碑与状态
- M1：现状与需求对齐（步骤2-5完成）
- M2：方案确认（步骤6完成）
- M3：实施与交付（步骤7）

当前状态：M1 进行中

## 执行清单（建议，待讨论）
- 结构
  - 模块骨架标准化：`modules/<name>/{agent.md, README.md, plan.md, doc/*}`，现有 `CONTRACT/TEST_PLAN/RUNBOOK/PROGRESS/BUGS/CHANGELOG` 下沉至 `doc/`。
  - 根 `agent.md` 轻量化：采用 YAML Front Matter + Markdown，保留全局目标/安全/路由与合并策略，详细内容迁移到 `doc/policies/*`。
  - 新增 `doc/orchestration/registry.yaml`：维护模块类型/实例/依赖/上下游关系。
  - 新增 `schemas/agent.schema.yaml`：用于校验各层级 `agent.md` YAML 头部。
- 自动化
  - Makefile 增加三校验命令：`agent_lint`、`registry_check`、`doc_route_check`，并纳入 `dev_check`。
  - CI（.github/workflows）新增步骤：运行三校验，首轮可“警告模式”（不阻断），二轮转阻断。
  - 保持现有 `dag_check/contract_compat/runtime_config/migrate/consistency` 等门禁。
- 文档
  - README 职责收敛为“人读语义地图/安装/示例”，在顶部声明“编排/模型请读同级 agent.md”。
  - 新增 `/doc/init/PROJECT_INIT_GUIDE.md` 与 `/doc/modules/MODULE_INIT_GUIDE.md`，指导项目与模块标准化初始化。
  - 新增 `/doc/indexes/context-rules.md` 描述 `.aicontext/` 收敛与屏蔽规则（可选）。
- 质量与治理
  - `plan.md` 作为执行准入：声明执行人/锁定路径/合并顺序/破坏性变更标记；未获批禁止进入实现。
  - 明确 `ownership.code_paths` 与 `tools_allowed`（写入各模块 `agent.md`）。

## 实施阶段（建议分步推进）
- Phase 0：安全落地（不破坏现状）
  - 引入 `schemas/agent.schema.yaml` 与三校验脚本于 `scripts/`（或保留在 tools 下），新增 Make/CI 步骤但先“警告模式”。
  - 补充 `doc/orchestration/registry.yaml`（最小版本）。
- Phase 1：根级文档调整
  - 根 `agent.md` 轻量化（保留路由/全局目标/安全/合并策略 + YAML 头部）。
  - `README.md` 顶部补充“编排系统请读 agent.md”的声明。
- Phase 2：模块骨架统一
  - 为现有模块（示例模块优先）补齐 `agent.md（YAML+MD）/ doc/*` 结构，平移原有文档。
  - 在 `agent.md` 中声明 `ownership.code_paths`、`io.contracts`、`dependencies` 与 `context_routes`。
- Phase 3：CI 阶段转阻断
  - 将三校验由“警告模式”切换为“阻断合并”。
  - 在 `dev_check` 中严格执行全部门禁。

## 脚本接入（混合式方案）
- 采用 Enhancement Pack 的 `schemas/agent.schema.yaml`、`scripts/agent_lint.py`、`scripts/registry_check.py`、`scripts/doc_route_check.py`，并做最小改造：
  - 修正 `doc_route_check.py` 的路径基准为“仓库根目录”，补充忽略目录（`.git/`、`node_modules/`、`temp/`）。
  - `agent_lint.py`：在未安装 `jsonschema` 时降级为提示（warning mode）。
- Makefile 接入（计划新增目标名）：
  - `agent_lint`：遍历所有 `agent.md`，校验 YAML 前言与 schema（可选）。
  - `registry_check`：校验 `doc/orchestration/registry.yaml` 唯一性/引用存在/无环。
  - `doc_route_check`：校验 `context_routes` 指向的文档路径存在。
- CI 接入策略：
  - 第一阶段（警告模式）：三校验失败不阻断，仅标黄并汇总输出。
  - 第二阶段（阻断模式）：三校验失败直接 fail job。

## 根 agent.md 轻量化 —— 迁出规范与流程
- 设计目标
  - 保持“agent.md 作为路由，doc/ 作为知识库”的风格；根级仅承载全局策略与路由。
  - 降低上下文体积，提升模型检索效率；细节迁入 `doc/` 下分册。

- 保留在根 agent.md 的内容（精简）
  - YAML 前言最小集：`spec_version`、`agent_id: repo`、`role: policy_router`、`context_routes`、`quality_gates`（枚举名称即可）、`orchestration_hints`（简要）。
  - 合并/继承策略：子级覆盖父级；冲突解决顺序。
  - 路由：
    - `always_read`: `doc/policies/goals.md`、`doc/policies/safety.md`
    - `by_scope`：`repo`/`module`/`orchestration` 分别路由到 `docs/flows/DAG_GUIDE.md`、`doc/orchestration/registry.yaml`、`docs/process/CONFIG_GUIDE.md` 等。

- 迁出映射表（从根 agent.md → 目标文档）
  - 工作流程（S0–S6）→ `doc/init/PROJECT_INIT_GUIDE.md`
  - 临时文件规范/安全/合规 → `doc/policies/safety.md`、`docs/process/CONVENTIONS.md`
  - 文档与风格规范 → `doc/policies/goals.md`、`docs/process/CONVENTIONS.md`
  - 应用/前端结构指引 → `doc/init/PROJECT_INIT_GUIDE.md`
  - 详细示例与 checklist → `doc/modules/MODULE_INIT_GUIDE.md`

- YAML 前言模板（根级示例）
  ```yaml
  ---
  spec_version: "1.0"
  agent_id: "repo"
  role: "policy_router"
  quality_gates: { gates: [dag_check, contract_compat, tests, docs] }
  orchestration_hints: { routing_tags: ["repo"], priority: 10 }
  context_routes:
    always_read:
      - "/doc/policies/goals.md"
      - "/doc/policies/safety.md"
    by_scope:
      - scope: repo
        read: ["/docs/flows/DAG_GUIDE.md", "/docs/process/CONFIG_GUIDE.md"]
      - scope: orchestration
        read: ["/doc/orchestration/registry.yaml"]
  ---
  ```

- 迁出流程（只读改造期，不动业务）
  1) 盘点：为根 agent.md 建立“章节 → 目标文档”映射表（见上）。
  2) 新建：创建 `doc/policies/*`、`doc/init/*`、`doc/modules/*`、`doc/orchestration/registry.yaml` 草案文件。
  3) 迁文：将根 agent.md 的长段落原文迁移到对应文档（保持语义不改，必要时加引导小节）。
  4) 精简：在根 agent.md 中以一句话 + 链接替代长段落；补齐 YAML 前言与 `context_routes`。
  5) 校验：本地运行三校验（warning）；确保 `doc_route_check` 全绿。
  6) 审阅：提交 PR，附变更映射清单与 diff 预览；获得确认后进入 Phase 1 合并。

- 验收标准
  - 根 agent.md 字数显著降低（仅保留路由与策略）；YAML 前言可被 `agent_lint` 正确解析。
  - 路由指向的文档均存在且可读；`doc_route_check` 通过。
  - 现有 Make/CI 无破坏；`dev_check` 仍通过。

- 回滚策略
  - 保留根 agent.md 迁出前副本（同 PR 中以 `agent.md.bak` 方式暂存或在描述中附完整快照）。
  - 若校验不通过或出现路径断链，可一键恢复为迁出前版本。

## 模块文档骨架与初始化规范（摘录）
- 目录：`modules/<name>/{agent.md, README.md, plan.md, doc/CONTRACT.md, doc/TEST_PLAN.md, doc/RUNBOOK.md, doc/PROGRESS.md, doc/BUGS.md, doc/CHANGELOG.md}`。
- 模块 `agent.md` YAML 前言最小集：
  - `spec_version`、`agent_id`、`role`、`level`、`module_type`、`ownership.code_paths`、`io.inputs/outputs`（schema ref 可选）、`contracts.apis`、`dependencies.upstream/downstream`、`context_routes`。
- 初始化流程：详见 `doc/modules/MODULE_INIT_GUIDE.md`（将给出可复制模板与验收 checklist）。

## 数据库治理与目录重构（提案）

### 目标
- 收敛数据相关内容，统一目录与规范，提升可读性与可校验性。
- 为大模型提供友好的表结构文档与上下文路由，支撑 CRUD 与迁移自动化辅助。
- 兼容多数据库（PostgreSQL、Redis），支持扩展（pgvector、TimescaleDB）。

### 目录方案（不立即改动，获批后迁移）
```text
db/
├─ registry.yaml                 # 数据引擎/实例/扩展注册表
└─ engines/
   ├─ postgres/
   │  ├─ migrations/            # 原 migrations/ 下沉至此
   │  ├─ schemas/
   │  │  └─ tables/             # 每张表 1 个 YAML（可按 schema 分目录）
   │  ├─ extensions/            # pgvector、timescaledb 等配置/说明
   │  └─ docs/                  # 原 docs/db/* 下沉至此
   └─ redis/
      ├─ schemas/keys/          # key 模式与 TTL 约定（YAML）
      └─ docs/
```
- 迁移映射（规划）：
  - `migrations/*` → `db/engines/postgres/migrations/*`
  - `docs/db/*` → `db/engines/postgres/docs/*`
  - 新增：`db/engines/postgres/schemas/tables/*.yaml`（详见“文档标准”）

### 文档标准（表结构 YAML，最小必需）
```yaml
table: public.runs
version: 1
description: 运行记录表
columns:
  - name: run_id
    type: uuid
    primary_key: true
    nullable: false
    default: gen_random_uuid()
    comment: 运行唯一标识
  - name: agent
    type: text
    nullable: false
indexes:
  - name: idx_runs_created_at
    columns: [created_at]
    order: desc
constraints:
  - type: check
    expr: latency_ms >= 0
relations:
  - type: fk
    column: user_id
    ref: public.users(id)
security:
  pii: none
  rls: false
lifecycle:
  retention: 365d
extensions:
  uses: []  # [pgvector, timescaledb]
```
- 生成汇编文档：由 `schemas/tables/*.yaml` 自动汇总生成 `SCHEMA_CATALOG.md`（供人/模型快速浏览）。

### 校验与自动化（首轮警告模式）
- 扩展 `migrate_check`：
  - 事务包装提示：非 CONCURRENTLY 操作缺少 BEGIN/COMMIT → warning
  - 幂等性提示：CREATE/ALTER/INDEX 缺少 IF NOT EXISTS → warning
  - 版本连续性提示：检测编号空洞 → warning
- 新增 `db_spec_align_check.py`：
  - 当有迁移变更时，要求 `schemas/tables/*.yaml` 或 `DB_SPEC.yaml` 同步更新，否则告警。
- 新增 `docgen_db.py`：
  - 汇总 YAML 表定义为 `db/engines/postgres/docs/SCHEMA_CATALOG.md`。
- Make/CI（规划目标）
  - `make db_lint`：聚合 migrate_check + db_spec_align_check
  - `make db_docgen`：生成 SCHEMA_CATALOG.md
  - `make db_plan`/`make db_apply`：预览/执行迁移（本地，需 DB_URL；CI 仅 dry-run）

### 自动化执行策略（安全边界 + 目标库选择）
- 准入：仅当 `modules/<name>/plan.md` 声明 DB 变更且获批后，才允许 `db_apply`。
- 顺序：preview（dry-run）→ 人工确认 → 执行 → 验证（结构/回滚脚本可用）。
- 保护：禁止自动执行破坏性 DROP（默认拦截，需显式开关与二次确认短语）。
- CI：永远不连生产库；仅做语法/幂等/事务/对齐校验与 dry-run（模拟）。
- 目标库选择优先级（高 → 低）：
  1) 命令行：`TARGET=dev|staging|prod` 或显式 `URL=postgres://...`
  2) 环境变量：`DATABASE_URL`/`POSTGRES_URL`（Redis：`REDIS_URL`）
  3) 配置文件：`config/<env>.yaml` 的 `db.url`
  4) 默认：本地 docker-compose（Postgres:16 / Redis:7）
- Make 目标与参数（规划）：
  - `make db_plan [TARGET=dev|staging|prod] [URL=...] [DRY_RUN=1]`
  - `make db_apply [TARGET=...] [URL=...] [DRY_RUN=0|1] [MODE=auto|manual|sync-only] [PROTECT_DROP=1] [CONFIRM="I-UNDERSTAND"]`
  - 样例：
    - 仅预览：`make db_apply DRY_RUN=1`
    - 本地执行：`make db_apply TARGET=dev`
    - 指定云端：`make db_apply URL=postgres://user:***@host:5432/app`
    - 仅生成 SQL 与报告：`make db_apply MODE=manual`
    - 已人工执行，仅同步文档：`make db_apply MODE=sync-only`

### 多数据库扩展
- 新增数据库时在 `db/engines/<engine>/` 建立子目录与 schemas/docs；在 `db/registry.yaml` 登记。
- PostgreSQL 扩展：`db/engines/postgres/extensions/{pgvector,timescaledb}.md|yaml` 记录启用/配置与使用约定。

### 分阶段（DB）
- DB‑0（规划）：本计划内定稿目录与规范；不移动现有文件。
- DB‑1（落盘骨架）：新增 `db/` 空目录与占位 README（获批后实施）；补充脚本草案（warning）。
- DB‑2（迁移与适配）：迁移 `migrations/` 与 `docs/db/`；脚本与 Make/CI 路径适配；补充表 YAML（最小核心表）。
- DB‑3（自动化）：落地 `db_plan/db_apply`（本地仅用）；完善校验项并切换部分为阻断。

### 验收标准（DB）
- 目录统一，现有迁移/文档均可在新路径下定位；脚本适配完成。
- 表 YAML 至少覆盖核心表；SCHEMA_CATALOG.md 可生成且被路由。
- 三类 DB 校验在 CI 报告中可见；告警可读、无误报。

### 目录变更影响面清单（静态扫描，待迁移/需更新引用）
- 需要迁移的目录/文件：
  - `migrations/*` → `db/engines/postgres/migrations/*`
  - `docs/db/*`（`DB_SPEC.yaml`, `SCHEMA_GUIDE.md`）→ `db/engines/postgres/docs/*`
- 需要更新路径引用的文件（示例，非穷尽）：
  - `README.md`, `QUICK_START.md`, `TEMPLATE_USAGE.md`
  - `migrations/README.md`（内部大量 `migrations/` 与 `docs/db/` 路径）
  - `docs/project/*`（RELEASE_TRAIN.md, IMPLEMENTATION_SUMMARY.md, SYSTEM_BOUNDARY.md 等）
  - `modules/example/*`（README.md/RUNBOOK.md/plan.md 中的迁移命令示例）
  - `agent.md`（多处引用 `docs/db/DB_SPEC.yaml` 与 `migrations/`）
  - 脚本：`scripts/migrate_check.py`, `scripts/rollback_check.sh`, `scripts/validate.sh`, `scripts/consistency_check.py`
- 调整策略：
  - 首轮保留兼容别名（如在 `migrations/` 放置 README 提示并引导至新路径），同时更新脚本默认路径至新目录。
  - 文档统一替换到新路径；为避免破坏链接，在变更说明中列出路径映射表。

### 表结构文档自动化（方案）
- 目标：把“迁移→结构更新→文档更新→校验”串为闭环，减少人工同步成本。
- 表 YAML（单表一文件）作为“解析友好的人读/机读”载体；来源以“迁移 + 实例化库内省”为准。
- 执行链：
  1) `make db_plan`：读取“意图”（命令行/配置/交互），生成迁移草案（up/down），打印差异概要（DDL 级）。
  2) `make db_apply`：
     - 先 dry-run（CI 永远只 dry-run）。
     - 本地经二次确认后，连接 dev DB（docker-compose 默认 postgres:16）应用迁移。
     - 迁移后内省库结构（information_schema/pg_catalog），更新对应表的 YAML（增删列/索引/约束）。
     - 运行 `make db_docgen` 生成/刷新 `SCHEMA_CATALOG.md`。
     - 运行 `make db_lint` 与 `make migrate_check` 确认一致性。
  3) 失败回滚：若任一步失败，自动执行 down 并恢复 YAML 的上一版本（预写快照）。
- 准入门槛：必须有 `modules/<name>/plan.md` 中的 DB 变更条目且获批。

### PII/RLS 字段说明（用于表 YAML）
- PII（Personally Identifiable Information，个人可识别信息）：
  - 分级建议：`none`（无）/`internal`（内部业务数据）/`personal`（个人信息，如邮箱/手机号）/`sensitive`（敏感，如身份证/精确定位）。
  - 用途：指导脱敏、导出限制与最小化原则；在生成数据样例与接口时做遮蔽。
- RLS（Row Level Security，行级安全，PostgreSQL 特性）：
  - `rls: true|false` 标记是否启用；
  - `rls_policies`：列出策略名/表达式/适用角色；
  - 生成提示：自动生成 `ALTER TABLE ... ENABLE ROW LEVEL SECURITY; CREATE POLICY ...` 草案，供审阅。

### 自动化执行流程（dry-run + 半自动模式，首轮警告）
- 输入：声明要添加/修改的表/列/索引（CLI/交互），或提供 YAML 意图文件。
- 生成：产出 up/down SQL 草案（自动补全 IF NOT EXISTS/事务包裹）。
- 预览（dry-run）：打印 DDL 差异、影响面与需更新的代码/契约提示；CI 仅到此步。
- 确认：交互式二次确认（y/N），破坏性操作需额外确认短语（`CONFIRM=I-UNDERSTAND`）。
- 执行（半自动）：连接目标库应用迁移（dev/staging 推荐）；生产建议 `MODE=manual` 走变更单。
- 同步：内省 DB → 更新表 YAML → 生成 `SCHEMA_CATALOG.md` → 运行 `db_lint/migrate_check`。
- 验证：最小 CRUD 冒烟、`rollback_check` 通过。
- 输出：变更报告（附路由），用于 PR 审阅与归档。

### 多人协作（团队开发建议）
- 共享开发库：提供 `dev-shared` 云端实例，按人/分支使用独立 schema 或库，最小权限与审计开启。
- 本地验证：保留本地 docker-compose 数据库用于离线与快速验证；与云端解耦。
- 迁移治理：
  - 以 `plan.md` 为准入，声明执行人/范围/合并顺序；避免并发写同一对象。
  - 迁移文件命名附作者/分支信息（可选），并提供 `migrations/LOCK` 机制（可选脚本实现）。
  - 提供数据脱敏样例与只读快照策略，便于复现实验。

### 环境与配置（.env 与 schema 草案）
- `.env.example`（规划新增）
  - `APP_ENV=dev`
  - `DATABASE_URL=postgresql://dev:dev@localhost:5432/app`
  - `POSTGRES_URL=postgresql://dev:dev@localhost:5432/app`
  - `REDIS_URL=redis://localhost:6379`
  - `DB_SCHEMA=dev_yourname`  # 可选，按人隔离 schema
- `config/schema.yaml`（规划新增字段）
  ```yaml
  app: { name: str, env: [dev, staging, prod] }
  db:
    url: str              # 连接串（优先被 CLI/ENV 覆盖）
    engine: [postgres, redis]
    schema: str           # 可选，Postgres search_path
  ```
  - `config/dev.yaml|staging.yaml|prod.yaml` 可按需提供 `db.url` 与 `db.schema`。
## 验证与验收（总表）
- 本地（开发者）：`make agent_lint || true`、`make registry_check || true`、`make doc_route_check || true`、`make dev_check`。
- CI（警告模式）：
  - 输出报告中包含：缺失字段、无效引用、路由断链、DAG/契约/迁移/配置等门禁结果。
- 切换为阻断模式前置条件：
  - 根与至少一个模块完成新骨架，三校验在主干分支稳定 1 周无误。

（以上为占位建议，后续将结合实际仓库现状细化与取舍）

## 决策记录
- 仅在 `temp/` 目录内记录与修改，直至计划获批

## 风险与假设
- 风险：现有自动化脚本依赖未显式记录；模块边界存在隐式耦合
- 缓解：先审阅与记录，再进行小步重构，配合 CI 保障

## 沟通与确认
- 请您确认本执行计划的流程与边界，确认后我将基于调查结果补充“执行清单（建议）”并进入实施阶段。
