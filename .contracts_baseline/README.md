# 契约基线目录

## 目标
存储契约文件的基线版本，用于自动检测破坏性变更，确保 API 向后兼容。

## 用途
- 对比当前契约与基线，检测破坏性变更
- 确保 API 向后兼容
- 作为契约演进的历史记录

## 使用方法

### 首次初始化
```bash
# 将当前契约复制为基线
make update_baselines
```

## 日常开发
```bash
# 1. 修改契约文件（如 tools/codegen/contract.json）
vim tools/codegen/contract.json

# 2. 检查兼容性
make contract_compat_check

# 3. 如果有破坏性变更，选择：
#    A. 修复契约保持兼容
#    B. 创建新版本契约（major 版本升级）
#    C. 评审后更新基线（谨慎）
make update_baselines
```

## 目录结构
基线目录与 `tools/` 目录结构对应：
```text
.contracts_baseline/
└── tools/
    └── <tool>/
        └── contract.json  # 基线版本
```

## 注意事项
1. **不要手动编辑此目录** - 使用 `make update_baselines` 自动更新
2. **基线文件应纳入版本控制** - 跟踪契约演进历史
3. **破坏性变更需团队审查** - 不要轻易更新基线
4. **新项目首次运行**：
   ```bash
   make docgen              # 生成索引
   make update_baselines    # 创建初始基线
   make dev_check          # 验证所有检查通过
   ```

## 破坏性变更检测
以下变更会被检测为破坏性：
- ❌ 类型变更（string → number）
- ❌ 新增必填字段（required）
- ❌ 删除已有字段
- ❌ 字段类型变更（object → array）

## 兼容性变更
以下变更是兼容的：
- ✅ 新增可选字段
- ✅ 放宽验证规则
- ✅ 增加枚举值（谨慎）
- ✅ 扩展文档说明

## 版本管理策略
遵循语义化版本（Semver）：
- **Major**: 破坏性变更（需创建新版本契约）
- **Minor**: 新增功能（向后兼容）
- **Patch**: Bug 修复（向后兼容）

---

**最后更新**: 2025-11-04  
**相关文档**: 
- `agent.md` §4 DAG 与接口契约
- `docs/project/IMPLEMENTATION_SUMMARY.md`
