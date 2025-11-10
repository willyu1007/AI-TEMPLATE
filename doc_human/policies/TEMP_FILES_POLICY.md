# Temporary Files Management Policy

> **Purpose**: Define standards for temporary files, reports, and short-lived artifacts  
> **Version**: 1.0  
> **Last Updated**: 2025-11-09  
> **Language**: English (AI-optimized)

---

## 1. File Classification

### 1.1 Temporary Files (`_tmp` suffix)

**Definition**: Files used only during a specific task and should be deleted after task completion.

**Naming Convention**: `<descriptive_name>_tmp.<extension>`

**Examples**:
- `fix_headings_tmp.py` - One-time fix script
- `debug_api_tmp.sh` - Debug script
- `test_data_tmp.json` - Test data file
- `task_summary_tmp.md` - Task summary document

**Location**:
- Recommended: `tmp/` directory
- Alternative: `modules/<name>/tmp/`
- Must be in `.gitignore` (auto-ignored via `*_tmp.*` pattern)

**Cleanup**: 
- Immediate: After task completion
- Command: `make cleanup_tmp`
- Automated: CI blocks commits with `*_tmp.*` files

### 1.2 Report Files (time-based retention)

**Definition**: Auto-generated reports from maintenance, health checks, and analysis tools.

**Categories**:

| Type | Pattern | Retention | Location |
|------|---------|-----------|----------|
| **Health Reports** | `health-report-*.json` | 30 days or last 10 | `ai/maintenance_reports/` |
| **Health Summaries** | `health-summary-*.md` | Keep latest only | `ai/maintenance_reports/` |
| **Dataflow Reports** | `report_*.html` | 30 days or last 5 | `ai/dataflow_reports/` |
| **Trend Analysis** | `*-trend-*.json` | 90 days | `ai/maintenance_reports/` |
| **Failed Reports** | `*failed*.json` | Permanent (for tracking) | `ai/maintenance_reports/` |

**Naming Convention**: `<type>-<YYYYMMDD>[-HHMMSS].<ext>`

**Examples**:
- `health-report-20251109.json`
- `dataflow-report-20251109_143022.html`
- `health-trend-20251109.json`

**Cleanup**:
- Semi-automatic: `make cleanup_reports AGE=30`
- Smart cleanup: `make cleanup_reports_smart` (keeps failed reports)
- Manual review: Check `ai/maintenance_reports/README.md`

### 1.3 Archive Files (permanent retention)

**Definition**: Important documents for long-term reference or project history.

**Examples**:
- `optimization-plan.md` - Planning documents
- `project-audit-report.md` - Milestone reports
- `optimization-complete-report.md` - Completion summaries
- `README.md` - Directory documentation

**Location**: Same as report files but explicitly documented

**Cleanup**: Manual only (never auto-delete)

---

## 2. Identification Rules

### 2.1 How to Identify Temporary Files

A file is considered **temporary** if it meets ANY of the following criteria:

1. **Not in `Makefile`**: Not used as a command target
2. **Not in `agent.md`**: Not explicitly mentioned in workflow docs
3. **Not in `README.md`**: Not part of core project features
4. **Task-specific tool**: One-time fix, debug, or check script
5. **Auto-generated report**: Maintenance, check, or analysis output
6. **Task summary doc**: Patterns like `*_SUMMARY.md`, `*_FIX.md`, `*_REPORT.md`

### 2.2 Decision Tree

```
Is this file needed after task completion?
├─ NO → Use _tmp suffix → Delete after task
├─ YES, but only for N days → Use timestamp naming → Auto-cleanup
└─ YES, permanently → Use descriptive name → Manual management
```

---

## 3. AI Generation Guidelines

### 3.1 Pre-Creation Checklist

Before generating ANY file, AI must:

- [ ] Determine if file is temporary (check criteria in 2.1)
- [ ] Apply correct naming convention (`_tmp` suffix if temporary)
- [ ] Choose appropriate location (`tmp/` or module-specific)
- [ ] Add header comment (for temporary files only)

### 3.2 Header Template (Temporary Files)

**Python**:
```python
#!/usr/bin/env python3
"""
TEMPORARY FILE - <Purpose description>
Should be deleted after task completion

Usage: python <script_name>
Created: <date>
Task: <task_name>
"""
```

**Shell**:
```bash
#!/bin/bash
# TEMPORARY FILE - <Purpose description>
# Should be deleted after task completion
# Created: <date>
# Task: <task_name>
```

**Markdown**:
```markdown
# TEMPORARY FILE - <Purpose>

**Status**: Should be deleted after task completion  
**Created**: <date>  
**Task**: <task_name>

---
```

---

## 4. Cleanup Strategies

### 4.1 Immediate Cleanup (Temporary Files)

**When**: After task completion, before PR

**Command**:
```bash
make cleanup_tmp
```

**What it does**:
- Deletes all `*_tmp.*` files
- Removes all `*_tmp/` directories
- Cleans `tmp/` directory
- Excludes: `.git/`, `node_modules/`, virtual envs

### 4.2 Scheduled Cleanup (Report Files)

**When**: Weekly or monthly maintenance

**Commands**:
```bash
# Delete reports older than 30 days
make cleanup_reports AGE=30

# Smart cleanup (keeps failed reports + last 10)
make cleanup_reports_smart

# Delete specific report type
make cleanup_reports TYPE=health AGE=30
```

**What it does**:
- Removes old report files based on timestamp
- Preserves reports with "failed" status
- Keeps minimum number of recent reports (configurable)

### 4.3 Manual Review (Archive Files)

**When**: Quarterly or when disk space is needed

**Process**:
1. Review `ai/maintenance_reports/` and `ai/dataflow_reports/`
2. Identify obsolete archive files (check LEDGER.md)
3. Move to `archive/` subdirectory or delete
4. Update `README.md` if structure changes

---

## 5. Automated Enforcement

### 5.1 CI/CD Checks

**Gate 1: Pre-commit** (via `make dev_check`)
```bash
make temp_files_check  # Blocks commits with *_tmp.* files
```

**Gate 2: PR Review**
- CI warns if `ai/maintenance_reports/` has >20 files
- CI fails if `*_tmp.*` files detected

### 5.2 Maintenance Integration

**Auto-check** (via `make ai_maintenance`)
- Detects uncleaned temporary files
- Reports aged report files (>30 days)
- Suggests cleanup commands

---

## 6. Directory Structure

### 6.1 Temporary Files Directory

```
tmp/
├── README.md           # This directory's purpose
├── reports/            # Temporary report files
├── scripts/            # Temporary scripts
└── data/               # Temporary data files
```

**Rules**:
- All files in `tmp/` should use `_tmp` suffix
- Auto-cleaned by `make cleanup_tmp`
- Entire directory is in `.gitignore`

### 6.2 Reports Directories

```
ai/
├── maintenance_reports/
│   ├── README.md       # Retention policies
│   ├── health-report-*.json      # 30 days retention
│   ├── health-summary-*.md       # Keep latest
│   └── archive/                   # Manual archive
└── dataflow_reports/
    ├── README.md
    └── report_*.html              # 30 days retention
```

---

## 7. Best Practices

### 7.1 For AI Agents

✅ **DO**:
- Always check if file is temporary before creation
- Use `_tmp` suffix for all temporary files
- Add clear header comments
- Run `make cleanup_tmp` after task completion
- Document cleanup plan in PR description

❌ **DON'T**:
- Create temporary files without `_tmp` suffix
- Leave temporary files after task completion
- Commit `*_tmp.*` files to git
- Delete archive files without review

### 7.2 For Developers

✅ **DO**:
- Review temporary files before PR
- Run `make cleanup_tmp` before commit
- Keep report directories organized
- Archive important reports with clear names

❌ **DON'T**:
- Ignore CI warnings about temporary files
- Let report directories grow unbounded
- Delete reports without checking dependencies

---

## 8. Examples

### Example 1: Debug Script (Temporary)

**Correct**:
```bash
# File: tmp/scripts/test_api_connection_tmp.sh
#!/bin/bash
# TEMPORARY FILE - Test API connection for debugging
# Should be deleted after task completion

curl -v http://localhost:8000/health
```

**Incorrect**:
```bash
# File: scripts/test_api_connection.sh  ❌ Wrong location, no _tmp suffix
curl -v http://localhost:8000/health
```

### Example 2: Health Report (Time-based)

**Correct**:
```bash
# Generated by make health_check
# File: ai/maintenance_reports/health-report-20251109.json
# Auto-cleanup after 30 days
```

**Incorrect**:
```bash
# File: health-report_tmp.json  ❌ Should not use _tmp suffix
```

### Example 3: Optimization Plan (Archive)

**Correct**:
```markdown
# File: ai/maintenance_reports/optimization-plan.md
# Permanent archive file
# No _tmp suffix, manual management
```

---

## 9. Related Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `make cleanup_tmp` | Delete all `*_tmp.*` files | After every task |
| `make cleanup_reports` | Delete old reports | Weekly/monthly |
| `make cleanup_reports_smart` | Smart cleanup (keeps important) | Monthly maintenance |
| `make temp_files_check` | Check for uncleaned files | Pre-commit (auto) |
| `make ai_maintenance` | Full maintenance (includes check) | After every task |

---

## 10. Related Documents

- **Workflow**: `agent.md` §0 (S6 - Auto Maintenance)
- **Quality Standards**: `doc/policies/quality.md`
- **Safety Rules**: `doc/policies/safety.md`
- **Maintenance Reports**: `ai/maintenance_reports/README.md`

---

**Maintained by**: Project Team  
**Review Cycle**: Quarterly or when adding new file types

