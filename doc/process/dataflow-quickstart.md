---
audience: ai
language: en
version: summary
purpose: Documentation for dataflow-quickstart
---
# Dataflow Analysis - AI Quick Start

> **For AI Agents** - Quick reference (~100 lines)  
> **Full Guide**: DATAFLOW_ANALYSIS_GUIDE.md  
> **Language**: English (AI-optimized)

---

## Purpose

Trace and visualize data flow across modules, detect performance bottlenecks automatically.

---

## Quick Commands

```bash
# Basic analysis
make dataflow_trace            # Trace data flow
make dataflow_visualize        # Generate Mermaid diagram
make dataflow_analyze          # Full analysis (trace + visualize + bottlenecks)

# Advanced
make dataflow_visualize FORMAT=html  # Interactive D3.js visualization
make dataflow_visualize FORMAT=dot   # Graphviz DOT format
make bottleneck_detect               # Detect 7 types of performance issues
make dataflow_report                 # Generate complete report (JSON + MD + HTML)
```

---

## 7 Bottleneck Types

| Priority | Type | Detection | Fix Suggestion |
|----------|------|-----------|----------------|
| 🔴 Critical | Circular Dependency | Cycle in call graph | Refactor, introduce abstraction |
| 🟠 High | Call Chain Depth | Depth > 5 | Flatten hierarchy, cache results |
| 🟠 High | N+1 Query | Loop with DB calls | Use batch query, eager loading |
| 🟡 Medium | Missing Index | Table scan detected | Add database index |
| 🟡 Medium | Parallelization | Independent calls in sequence | Use async/parallel execution |
| 🟢 Low | Cache Opportunity | Repeated computation | Add caching layer |
| 🟢 Low | Duplicate Computation | Same input → same output | Memoization, cache |

---

## 3 Visualization Formats

1. **Mermaid** (default): Lightweight, embeddable in Markdown
2. **Graphviz DOT**: Professional graph rendering
3. **D3.js HTML**: Interactive, drag-and-drop, zoomable

---

## Workflow

### Step 1: Trace Data Flow
```bash
make dataflow_trace
# Output: temp/dataflow_trace.json
```

Analyzes:
- Module dependencies
- API call chains
- Data transformation paths
- External service calls

### Step 2: Visualize
```bash
make dataflow_visualize
# Output: temp/dataflow_diagram.mermaid

# Or interactive HTML
make dataflow_visualize FORMAT=html
# Output: temp/dataflow_diagram.html (open in browser)
```

### Step 3: Detect Bottlenecks
```bash
make bottleneck_detect
# Output: temp/bottleneck_report.json
```

Reports:
- Critical issues (immediate action)
- High/Medium issues (plan to fix)
- Low issues (optimization opportunities)

### Step 4: Generate Report
```bash
make dataflow_report
# Outputs:
#   - temp/dataflow_report.json (machine-readable)
#   - temp/dataflow_report.md (human-readable)
#   - temp/dataflow_report.html (visual dashboard)
```

---

## Configuration

Edit `scripts/bottleneck_rules.yaml` to customize:
- Detection thresholds
- Severity levels
- Custom rules

---

## Common Use Cases

### 1. New Module Review
```bash
# After creating a new module
make dataflow_analyze
# Check: circular dependencies, call depth
```

### 2. Performance Investigation
```bash
# When API is slow
make bottleneck_detect
# Look for: N+1 queries, missing indexes, parallelization opportunities
```

### 3. Refactoring Planning
```bash
# Before major refactor
make dataflow_visualize FORMAT=html
# Understand: module coupling, data flow patterns
```

---

## Output Files

All outputs in `temp/` directory:
- `dataflow_trace.json` - Raw trace data
- `dataflow_diagram.mermaid` - Mermaid diagram
- `dataflow_diagram.html` - Interactive visualization
- `dataflow_diagram.dot` - Graphviz format
- `bottleneck_report.json` - Bottleneck detection results
- `dataflow_report.*` - Complete reports (JSON/MD/HTML)

---

## Integration

### In CI/CD
```yaml
# .github/workflows/dataflow-check.yml
- name: Dataflow Analysis
  run: make bottleneck_detect
  continue-on-error: true  # Don't fail build, but report
```

### In Development
```bash
# Add to pre-commit hook
make bottleneck_detect | grep "🔴 Critical"
# Block commit if critical issues found
```

---

## See Also

- **Full Guide**: doc/process/DATAFLOW_ANALYSIS_GUIDE.md (519 lines, detailed examples)
- **Bottleneck Rules**: scripts/bottleneck_rules.yaml (166 lines, rule configuration)
- **Scripts**: scripts/dataflow_trace.py (723 lines), scripts/dataflow_visualizer.py (438 lines)
- **Template**: doc/templates/dataflow-summary.md (AI-optimized summary template)

