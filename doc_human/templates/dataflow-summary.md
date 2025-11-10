# 数据流分析摘要

> **AI优化文档** - 轻量化设计，≤100行  
> **人类完整参考**: [DATAFLOW_ANALYSIS_GUIDE.md](../process/DATAFLOW_ANALYSIS_GUIDE.md)

---

## 📊 分析结果

**生成时间**: {timestamp}

### 问题统计

- 🔴 **Critical**: {critical_count} 个 - 需立即处理
- 🟠 **High**: {high_count} 个 - 高优先级
- 🟡 **Medium**: {medium_count} 个 - 中优先级
- 🟢 **Low**: {low_count} 个 - 优化建议

**总计**: {total_issues} 个问题/建议

---

## 🔴 Critical问题（需立即处理）

{critical_issues_list}

---

## 🎯 Top 5优化建议

{top_recommendations}

---

## 📈 性能瓶颈（ASCII雷达图）

```
        性能
        100 |     *
            |    / \
         80 |   /   \
扩展性  60 | *       * 可维护性
         40 |   \   /
         20 |    \ /
          0 |     *
            数据库
```

**评分说明**:
- 性能: {performance_score}/100
- 扩展性: {scalability_score}/100
- 可维护性: {maintainability_score}/100
- 数据库: {database_score}/100

---

## 🚀 快速修复建议

### 1. {recommendation_1_title}
**影响**: {recommendation_1_impact}  
**修复时间**: {recommendation_1_time}  
**操作**: {recommendation_1_action}

### 2. {recommendation_2_title}
**影响**: {recommendation_2_impact}  
**修复时间**: {recommendation_2_time}  
**操作**: {recommendation_2_action}

### 3. {recommendation_3_title}
**影响**: {recommendation_3_impact}  
**修复时间**: {recommendation_3_time}  
**操作**: {recommendation_3_action}

---

## 📋 相关资源

- **完整分析报告**: `dataflow-report.html` (交互式)
- **JSON数据**: `dataflow-analysis.json`
- **瓶颈检测规则**: [bottleneck_rules.yaml](../../scripts/bottleneck_rules.yaml)
- **详细指南**: [DATAFLOW_ANALYSIS_GUIDE.md](../process/DATAFLOW_ANALYSIS_GUIDE.md)

---

## 🛠️ 快速命令

```bash
# 重新生成报告
make dataflow_analyze

# 生成可视化
make dataflow_visualize FORMAT=html

# 瓶颈检测
make bottleneck_detect

# 查看完整报告
open doc/templates/dataflow-report.html
```

---

**💡 提示**: 这是AI优化文档，完整详细说明请查看[DATAFLOW_ANALYSIS_GUIDE.md](../process/DATAFLOW_ANALYSIS_GUIDE.md)

