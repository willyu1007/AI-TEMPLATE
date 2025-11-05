# AI 维护报告目录

## 目标
存储 AI 自动维护脚本生成的维护报告，用于追踪仓库维护历史和问题趋势。

## 适用场景
- 查看最近维护结果
- 分析维护问题趋势
- 追踪修复进度

## 文件命名
```
maintenance_YYYYMMDD_HHMMSS.json
```

示例：`maintenance_20251105_103000.json`

---

## 报告格式

每个报告包含：
- `timestamp`: 维护执行时间
- `summary`: 摘要统计（总数/通过/失败/警告）
- `tasks`: 详细任务结果列表

---

## 查看报告

### 查看最新报告
```bash
# 按时间排序
ls -lt ai/maintenance_reports/*.json | head -1

# 查看内容
cat ai/maintenance_reports/maintenance_*.json | jq '.' | tail -50
```

### 统计维护历史
```bash
# 统计通过率
python -c "
import json
from pathlib import Path

reports = list(Path('ai/maintenance_reports').glob('*.json'))
for r in sorted(reports)[-10:]:
    data = json.loads(r.read_text())
    print(f\"{r.name}: {data['summary']['passed']}/{data['summary']['total']}\")
"
```

---

## 清理策略

建议保留：
- 最近 30 天的报告
- 包含失败项的报告（用于问题追踪）

清理命令：
```bash
# 删除 30 天前的报告（保留失败报告）
find ai/maintenance_reports/ -name "*.json" -mtime +30 -exec sh -c '
  if ! grep -q "\"status\": \"failed\"" "$1"; then
    rm "$1"
  fi
' _ {} \;
```

---

## 相关文档
- AI 维护机制：`agent.md` §14
- 维护脚本：`scripts/ai_maintenance.py`

