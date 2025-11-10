#!/usr/bin/env python3
"""
Lightweight Redis health probe for TemplateAI.

Usage:
    python db/engines/redis/scripts/health_check.py --url redis://localhost:6379 --key ping:test

Requires the `redis` Python package. Install with:
    pip install redis
"""
from __future__ import annotations

import argparse
import sys
import time

try:
    import redis
except ImportError as exc:  # pragma: no cover - runtime guard
    print("ERROR: redis package not installed. Run `pip install redis`.", file=sys.stderr)
    raise SystemExit(2) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Redis health check")
    parser.add_argument("--url", default="redis://localhost:6379", help="Redis connection URL")
    parser.add_argument("--key", default="health:ping", help="Temporary key used for round-trip test")
    parser.add_argument("--ttl", type=int, default=5, help="TTL (seconds) for temporary key")
    parser.add_argument("--timeout", type=float, default=1.5, help="Socket timeout in seconds")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    client = redis.from_url(args.url, socket_timeout=args.timeout)

    start = time.perf_counter()
    try:
        pong = client.ping()
        if not pong:
            print("ERROR: PING failed")
            return 3

        client.set(args.key, "ok", ex=args.ttl)
        value = client.get(args.key)
        latency_ms = (time.perf_counter() - start) * 1000
        status = {
            "url": args.url,
            "key": args.key,
            "reachable": True,
            "latency_ms": round(latency_ms, 2),
            "roundtrip_ok": value == b"ok",
        }
        print(status)
        return 0 if status["roundtrip_ok"] else 4
    except redis.RedisError as exc:
        print(f"ERROR: Redis operation failed: {exc}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())


