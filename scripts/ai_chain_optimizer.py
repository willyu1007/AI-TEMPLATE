#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Chain Optimizer

Provides lightweight suggestions to improve AI route efficiency based on
context usage telemetry recorded by context_usage_tracker.py.
"""
from __future__ import annotations

import sys
import json
import argparse
from pathlib import Path
from typing import Any, Dict, List, Tuple
from collections import Counter

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = REPO_ROOT / "tmp" / "context_cache" / "route_usage.jsonl"


def load_usage() -> List[Dict[str, Any]]:
    if not LOG_FILE.exists():
        return []
    records: List[Dict[str, Any]] = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except Exception:
                continue
    return records


def suggest(records: List[Dict[str, Any]], limit: int = 10) -> Dict[str, Any]:
    topic_ctr: Counter[str] = Counter(r["topic"] for r in records if r.get("topic"))
    path_ctr: Counter[str] = Counter(r["path"] for r in records if r.get("path"))
    top_topics = [t for t, _ in topic_ctr.most_common(limit)]
    top_paths = [p for p, _ in path_ctr.most_common(limit)]

    suggestions: List[str] = []
    if not records:
        suggestions.append(
            "No usage data detected. Run with ROUTE_USAGE_LOGGING=1 and collect a day of events."
        )
        return {
            "top_topics": [],
            "top_paths": [],
            "suggestions": suggestions,
        }

    if len(top_topics) >= 3:
        suggestions.append(
            "Consider reordering on_demand routes so the top 3 topics appear first."
        )
    if len(top_topics) >= 5:
        suggestions.append(
            "If top 1-2 topics are loaded on almost every task, consider moving them to always_read (keep under ~200 tokens)."
        )
    suggestions.append(
        "Drop rarely used topics (tail 20%) or hide behind task_specific to save tokens."
    )
    suggestions.append("Avoid recursive includes; keep one-hop depth.")

    return {
        "top_topics": top_topics,
        "top_paths": top_paths,
        "suggestions": suggestions,
    }


def main() -> int:
    p = argparse.ArgumentParser(
        description="Analyze telemetry and propose AI context route optimizations"
    )
    p.add_argument(
        "--optimize", action="store_true", help="Print optimization suggestions"
    )
    p.add_argument("--limit", default="10", help="How many top items to consider")
    args = p.parse_args()

    if not args.optimize:
        p.print_help()
        return 0

    limit = max(1, int(args.limit or "10"))
    records = load_usage()
    result = suggest(records, limit=limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
