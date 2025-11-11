#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal lint framework used by agent linters.
Provides BaseLinter, LintIssue, Severity, and run_linter().
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

# Windows UTF-8 support
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


class Severity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class LintIssue:
    file: str
    severity: Severity
    message: str
    rule: Optional[str] = None
    fix: Optional[str] = None


class BaseLinter:
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root: Path = repo_root or Path(__file__).resolve().parent.parent
        self.issues: List[LintIssue] = []
        self.stats: Dict[str, int] = {
            "files_checked": 0,
            "errors": 0,
            "warnings": 0,
            "infos": 0,
        }

    @property
    def name(self) -> str:
        return "Base"

    def print_separator(self) -> None:
        print("-" * 60)

    def add_issue(self, issue: LintIssue) -> None:
        self.issues.append(issue)
        if issue.severity == Severity.ERROR:
            self.stats["errors"] += 1
        elif issue.severity == Severity.WARNING:
            self.stats["warnings"] += 1
        else:
            self.stats["infos"] += 1

    def check(self) -> bool:
        raise NotImplementedError("Subclasses must implement check()")


def _to_json(issues: List[LintIssue], stats: Dict[str, int], name: str) -> str:
    payload: Dict[str, Any] = {
        "linter": name,
        "stats": stats,
        "issues": [
            {
                "file": i.file,
                "severity": i.severity.value,
                "message": i.message,
                **({"rule": i.rule} if i.rule else {}),
                **({"fix": i.fix} if i.fix else {}),
            }
            for i in issues
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _to_markdown(issues: List[LintIssue], stats: Dict[str, int], name: str) -> str:
    lines: List[str] = []
    lines.append(f"# {name} Lint Report")
    lines.append("")
    lines.append(f"- Files checked: {stats.get('files_checked', 0)}")
    lines.append(f"- Errors: {stats.get('errors', 0)}")
    lines.append(f"- Warnings: {stats.get('warnings', 0)}")
    lines.append(f"- Infos: {stats.get('infos', 0)}")
    lines.append("")
    lines.append("| File | Severity | Message | Rule | Fix |")
    lines.append("| --- | --- | --- | --- | --- |")
    for i in issues:
        lines.append(
            f"| {i.file} | {i.severity.value} | {i.message} | "
            f"{i.rule or ''} | {i.fix or ''} |"
        )
    return "\n".join(lines)


def run_linter(linter_cls: Type[BaseLinter]) -> int:
    # very small arg parser
    args = sys.argv[1:]
    as_json = "--json" in args
    as_md = "--markdown" in args

    linter = linter_cls(repo_root=Path(__file__).resolve().parent.parent)
    ok = linter.check()

    # default console output if neither json nor markdown requested
    if as_json:
        print(_to_json(linter.issues, linter.stats, linter.name))
    elif as_md:
        print(_to_markdown(linter.issues, linter.stats, linter.name))
    else:
        print("")
        linter.print_separator()
        print(f"{linter.name} Lint Summary")
        linter.print_separator()
        print(f"Files checked: {linter.stats['files_checked']}")
        print(f"Errors:        {linter.stats['errors']}")
        print(f"Warnings:      {linter.stats['warnings']}")
        if linter.issues:
            linter.print_separator()
            for i in linter.issues:
                print(f"[{i.severity.value}] {i.file}: {i.message}")
                if i.fix:
                    print(f"  fix: {i.fix}")

    return 0 if ok else 1


