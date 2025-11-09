# 根目录结构优化分析

> **分析日期**: 2025-11-09  
> **当前版本**: v2.4 (Phase 14.0)

---

## 当前根目录结构

```
AI-TEMPLATE/
├── .aicontext/           # ✅ AI上下文索引 (隐藏，合理)
├── .contracts_baseline/  # ⚠️ 缺少README (Phase 14.0.1已识别)
├── .github/              # ✅ GitHub配置 (标准)
├── .vscode/              # ✅ VS Code配置 (标准)
├── ai/                   # ✅ AI会话记录
├── config/               # ✅ 配置文件
├── db/                   # ✅ 数据库治理
├── doc/                  # ✅ 文档 (已优化)
├── evals/                # ✅ 评估基线
├── migrations/           # ⚠️ 冗余？已有db/engines/*/migrations/
├── modules/              # ✅ 业务模块 (Phase 14.0.1新增)
├── observability/        # ⚠️ 缺少AI文档 (Phase 14.0.1已识别)
├── schemas/              # ✅ Schema定义
├── scripts/              # ✅ 自动化脚本
├── temp/                 # ✅ 临时文件
├── tests/                # ✅ 测试目录
├── tools/                # ✅ 工具契约
├── agent.md              # ✅ 根编排配置
├── README.md             # ✅ 项目说明
├── QUICK_START.md        # ✅ 快速开始
├── TEMPLATE_USAGE.md     # ✅ 模板使用
├── CONTRIBUTING.md       # ✅ 贡献指南
├── Makefile              # ✅ 命令入口
└── requirements.txt      # ✅ Python依赖
```

---

## 优化建议

### 问题1: migrations/ 目录冗余

**当前状态**:
- `/migrations/` (顶层，2个示例文件)
- `/db/engines/postgres/migrations/` (实际使用)

**分析**:
- 顶层migrations/只有示例文件 (001_example_*.sql)
- 实际迁移在db/engines/*/migrations/
- 可能导致混淆：迁移应该放哪里？

**建议**:
- **选项A**: 删除顶层migrations/，所有迁移放db/engines/*/
- **选项B**: 保留顶层migrations/，作为跨引擎共享迁移
- **推荐**: 选项A（简化结构）

**影响**: 低（仅2个示例文件）

### 问题2: .contracts_baseline/ 缺少README

**当前状态**: 仅有JSON文件，无说明文档

**建议**: 创建 `.contracts_baseline/README.md`
- 说明契约基线机制
- 如何更新基线 (make update_baselines)
- 破坏性变更检测原理
- 豁免机制

**优先级**: 中 (Phase 14.0.1已识别，待实施)

### 问题3: observability/ 缺少文档

**当前状态**: 
- 有alerts/, logging/, metrics/, tracing/目录
- 仅有README.md (简单)
- 无AI快速参考

**建议**: 创建 `observability/QUICK_START.md` (AI文档)
- Quick configuration guide
- Local dev startup
- Production deployment checklist
- 50行左右，英文

**优先级**: 低 (模板项目标记，实际项目按需)

### 问题4: 顶层文件组织

**当前状态**: 顶层有多个README/指南文件

**分析**:
```
✅ 保持现状（清晰的入口点）:
├── README.md           # 项目总览 (必须)
├── QUICK_START.md      # 快速开始 (推荐)
├── TEMPLATE_USAGE.md   # 模板使用 (推荐)
├── CONTRIBUTING.md     # 贡献指南 (标准)
├── LICENSE             # 许可证 (必须)
└── agent.md            # AI编排 (核心)
```

**建议**: 保持现状，清晰明确

### 问题5: temp/ 目录管理

**当前状态**: 156个文件（大量Phase报告）

**建议**: 定期归档
- 创建 `temp/archive/phaseX/` 子目录
- 保留最近的报告在顶层
- 归档历史Phase报告

**优先级**: 低（不影响功能）

---

## 优化优先级

| 优先级 | 优化项 | 预估时间 | 建议执行时机 |
|--------|--------|----------|--------------|
| P0 | .contracts_baseline/README.md | 15min | Phase 14.0或14.1 |
| P1 | 删除顶层migrations/ | 5min | Phase 14完成后 |
| P2 | observability/QUICK_START.md | 20min | 实际项目使用时 |
| P3 | temp/归档整理 | 10min | Phase 14完成后 |

---

## 总体评估

**当前结构评分**: 9/10

**优点**:
- ✅ 清晰的分层（ai/, doc/, modules/, scripts/）
- ✅ 隐藏目录合理（.aicontext, .contracts_baseline）
- ✅ 标准文件齐全（README, LICENSE, CONTRIBUTING）
- ✅ 配置集中（config/, schemas/）

**小瑕疵**:
- ⚠️ migrations/顶层冗余（建议删除）
- ⚠️ .contracts_baseline/缺文档（建议补充）

**建议**: 根目录结构整体优秀，仅需微调

