#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Documentation Tools Wrapper

Subcommands:
  - style       -> scripts/doc_style_check.py
  - freshness   -> scripts/doc_freshness_check.py --json
  - sync        -> scripts/doc_script_sync_check.py
  - all         -> run all the above sequentially
Exit code is non-zero when any invoked task fails (for 'all', aggregates).
"""
from __future__ import annotations

import sys
import subprocess
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def run_cmd(args: list[str]) -> int:
    proc = subprocess.run([sys.executable, *args], cwd=REPO_ROOT)
    return proc.returncode


def cmd_style() -> int:
    return run_cmd([str(SCRIPTS / "doc_style_check.py")])


def cmd_freshness() -> int:
    return run_cmd([str(SCRIPTS / "doc_freshness_check.py"), "--json"])


def cmd_sync() -> int:
    return run_cmd([str(SCRIPTS / "doc_script_sync_check.py")])


def cmd_all() -> int:
    rc1 = cmd_style()
    rc2 = cmd_freshness()
    rc3 = cmd_sync()
    # non-zero if any fails
    return 0 if (rc1 == 0 and rc2 == 0 and rc3 == 0) else 1


def main() -> int:
    p = argparse.ArgumentParser(description="Unified wrapper for documentation checks")
    p.add_argument(
        "action",
        choices=["style", "freshness", "sync", "all"],
        help="which doc task(s) to run",
    )
    args = p.parse_args()
    if args.action == "style":
        return cmd_style()
    if args.action == "freshness":
        return cmd_freshness()
    if args.action == "sync":
        return cmd_sync()
    if args.action == "all":
        return cmd_all()
    return 0


if __name__ == "__main__":
    sys.exit(main())
