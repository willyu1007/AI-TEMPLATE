#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Context Usage Tracker

Subcommands:
  - log:        record a single (topic, path) usage event
  - maybe-log:  record only when ROUTE_USAGE_LOGGING env is truthy
  - report:     aggregate top topics/paths
  - optimize:   propose reordering agent.md on_demand routes by usage; optional --write to apply
"""
from __future__ import annotations

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import Counter
from typing import Any, Dict, List, Tuple

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = REPO_ROOT / "tmp" / "context_cache"
LOG_FILE = LOG_DIR / "route_usage.jsonl"


def _ensure_log_dir() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def _truthy(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def cmd_log(args: argparse.Namespace, conditional: bool = False) -> int:
    if conditional:
        if not _truthy(os.getenv("ROUTE_USAGE_LOGGING")):
            return 0
    topic = (args.topic or "").strip()
    path = (args.path or "").strip()
    if not topic or not path:
        print("topic and path are required", file=sys.stderr)
        return 1
    _ensure_log_dir()
    record = {
        "ts": args.ts or datetime.utcnow().isoformat(),
        "topic": topic,
        "path": path,
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return 0


def _load_records() -> List[Dict[str, Any]]:
    if not LOG_FILE.exists():
        return []
    out: List[Dict[str, Any]] = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out


def cmd_report(args: argparse.Namespace) -> int:
    records = _load_records()
    limit = max(1, int(args.limit or 10))
    topic_ctr: Counter[str] = Counter(r["topic"] for r in records if r.get("topic"))
    path_ctr: Counter[str] = Counter(r["path"] for r in records if r.get("path"))

    top_topics = topic_ctr.most_common(limit)
    top_paths = path_ctr.most_common(limit)

    if args.json:
        payload = {
            "total_records": len(records),
            "top_topics": [{"topic": k, "count": v} for k, v in top_topics],
            "top_paths": [{"path": k, "count": v} for k, v in top_paths],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"Total records: {len(records)}")
    print("\nTop topics:")
    for topic, count in top_topics:
        print(f"  - {topic}: {count}")
    print("\nTop paths:")
    for p, count in top_paths:
        print(f"  - {p}: {count}")
    return 0


def _read_agent_front_matter(agent_path: Path) -> Tuple[Dict[str, Any], str]:
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


def _write_agent_front_matter(
    agent_path: Path, data: Dict[str, Any], body: str
) -> None:
    if yaml is None:
        raise RuntimeError("yaml not available")
    yml = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    content = f"---\n{yml}---\n{body}"
    agent_path.write_text(content, encoding="utf-8")


def cmd_optimize(args: argparse.Namespace) -> int:
    if yaml is None:
        print("PyYAML not installed; cannot optimize", file=sys.stderr)
        return 1
    records = _load_records()
    if not records:
        print("No usage records; nothing to optimize")
        return 0
    limit = max(1, int(args.limit or 10))
    topic_ctr: Counter[str] = Counter(r["topic"] for r in records if r.get("topic"))
    top_topics = [t for t, _ in topic_ctr.most_common(limit)]

    agent_path = (
        (REPO_ROOT / args.agent).resolve() if args.agent else (REPO_ROOT / "agent.md")
    )
    if not agent_path.exists():
        print(f"Agent not found: {agent_path}", file=sys.stderr)
        return 1

    fm, body = _read_agent_front_matter(agent_path)
    routes = fm.get("context_routes") or {}
    on_demand: List[Dict[str, Any]] = routes.get("on_demand") or []
    if not isinstance(on_demand, list) or not on_demand:
        print("No on_demand routes found; nothing to reorder")
        return 0

    def key_of(entry: Dict[str, Any]) -> Tuple[int, str]:
        topic = (entry or {}).get("topic", "")
        # earlier in top_topics => smaller index
        idx = top_topics.index(topic) if topic in top_topics else len(top_topics) + 1
        return (idx, topic.lower())

    new_on_demand = sorted(on_demand, key=key_of)
    changed = json.dumps(on_demand, sort_keys=True) != json.dumps(
        new_on_demand, sort_keys=True
    )

    print("Proposed on_demand order by observed usage:")
    for e in new_on_demand:
        t = e.get("topic", "")
        c = topic_ctr.get(t, 0)
        print(f"  - {t} (count={c})")

    if args.write and changed:
        routes["on_demand"] = new_on_demand
        fm["context_routes"] = routes
        _write_agent_front_matter(agent_path, fm, body)
        print(f"\nApplied reordering to: {agent_path.relative_to(REPO_ROOT)}")
    elif not changed:
        print("\nNo change in order needed.")
    else:
        print("\nUse --write to apply changes.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Track and analyze context route usage")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_log = sub.add_parser("log", help="record a usage event")
    p_log.add_argument("--topic", required=True)
    p_log.add_argument("--path", required=True)
    p_log.add_argument("--ts", required=False)

    p_maybe = sub.add_parser(
        "maybe-log",
        help="conditionally record a usage event based on ROUTE_USAGE_LOGGING env",
    )
    p_maybe.add_argument("--topic", required=True)
    p_maybe.add_argument("--path", required=True)
    p_maybe.add_argument("--ts", required=False)

    p_report = sub.add_parser("report", help="aggregate frequent topics/paths")
    p_report.add_argument("--limit", required=False, default="10")
    p_report.add_argument("--json", action="store_true")

    p_opt = sub.add_parser(
        "optimize", help="propose route ordering and optionally write back to agent"
    )
    p_opt.add_argument("--agent", required=False, default="agent.md")
    p_opt.add_argument("--limit", required=False, default="10")
    p_opt.add_argument("--write", action="store_true")

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.cmd == "log":
        return cmd_log(args, conditional=False)
    if args.cmd == "maybe-log":
        return cmd_log(args, conditional=True)
    if args.cmd == "report":
        return cmd_report(args)
    if args.cmd == "optimize":
        return cmd_optimize(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
