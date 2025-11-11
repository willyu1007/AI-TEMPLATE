#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telemetry utilities shared by context usage and optimization scripts.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

# Windows UTF-8 support
import sys
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Repo paths and log targets
REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = REPO_ROOT / "temp" / "context_cache"
LOG_FILE = LOG_DIR / "route_usage.jsonl"


def ensure_log_dir() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def is_truthy(value: Optional[str]) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def append_usage_record(topic: str, path: str, ts: Optional[str] = None) -> None:
    ensure_log_dir()
    record = {
        "ts": ts or datetime.utcnow().isoformat(),
        "topic": topic.strip(),
        "path": path.strip(),
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_usage_records(log_file: Path = LOG_FILE) -> List[Dict[str, Any]]:
    if not log_file.exists():
        return []
    out: List[Dict[str, Any]] = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out


def read_agent_front_matter(agent_path: Path) -> Tuple[Dict[str, Any], str]:
    text = agent_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    _, yml, rest = parts
    if yaml is None:
        return {}, text
    data = yaml.safe_load(yml) or {}
    return data, rest.lstrip("\n")


def write_agent_front_matter(agent_path: Path, data: Dict[str, Any], body: str) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML not available")
    yml = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    content = f"---\n{yml}---\n{body}"
    agent_path.write_text(content, encoding="utf-8")


