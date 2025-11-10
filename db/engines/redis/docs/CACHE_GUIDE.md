---
audience: ai
language: en
version: reference
purpose: Redis usage guide for cache/session/queue scenarios
---

# Redis Cache Guide

## Goals

- Document standard Redis patterns used by TemplateAI modules.
- Provide TTL defaults and eviction expectations.
- Highlight safety rules before automation touches production.

---

## Key Patterns

| Pattern | Data Type | TTL | Notes |
| --- | --- | --- | --- |
| `cache:<module>:<hash>` | Hash | 3600s | Store rendered responses or computed attributes |
| `session:<user_id>` | String | 86400s | JSON blob with session metadata |
| `queue:<module>` | List | None | Push job payloads; workers pop with `BRPOP` |
| `rate:<module>:<id>` | ZSet | 60s | Sliding window rate limiting; score = timestamp |

---

## Safety & Guardrails

1. **Namespace collisions**: Prefix keys with module identifiers to avoid overlap.
2. **Serialization**: Use JSON; avoid pickled/binary formats for portability.
3. **Eviction**: Stick with `volatile-lru` or `allkeys-lru`; document overrides.
4. **Backups**: For critical data, enable AOF + snapshot backups; record the location.
5. **Monitoring**: Collect metrics (`used_memory`, `connected_clients`, `evicted_keys`) and alert when thresholds exceed targets.

---

## Operational Checklist

- [ ] Update `schemas/keys/README.md` with new key structures.
- [ ] Document TTL + eviction policy changes in workdocs.
- [ ] Run `health_check.py` before/after deployment.
- [ ] For queues/streams, include retry & dead-letter logic in module docs.

---

## Related Assets

- `/db/engines/redis/README.md`
- `/db/engines/redis/scripts/health_check.py`
- `/doc_human/guides/DB_CHANGE_GUIDE.md` (for approval process)


