# Redis Engine

> Template-ready structure for cache/session/queue workloads powered by Redis.

---

## Use Cases

- **Caching**: Short-lived key/value pairs to reduce database load.
- **Sessions**: User/session state with configurable TTL.
- **Queues / Streams**: Lightweight background job coordination.

---

## Directory Layout

```text
db/engines/redis/
├── README.md              # This overview
├── docs/                  # Engine-specific guides and contracts
│   └── CACHE_GUIDE.md
├── schemas/               # Key design specifications
│   └── keys/
│       └── README.md
└── scripts/               # Operational utilities
    └── health_check.py
```

---

## Operating Principles

1. Keep keys namespaced: `<service>:<entity>:<id>[:<attribute>]`.
2. Define TTL per use case; document defaults inside `schemas/keys/`.
3. Avoid storing authoritative data—Redis complements, not replaces, primary databases.
4. Every background script must handle connection failures gracefully.
5. Track command usage (e.g., `INCR`, `SCAN`) to avoid latency spikes.

---

## Quick Start

1. Document the data model in `schemas/keys/` (structure, TTL, eviction policy).
2. If new Lua scripts or custom commands are needed, reference them inside `docs/`.
3. Run `python db/engines/redis/scripts/health_check.py --url redis://localhost:6379` before and after changes.
4. Update `/db/engines/AGENTS.md` routing if you add new guides.

---

## References

- `/db/engines/redis/docs/CACHE_GUIDE.md`
- `/db/engines/redis/schemas/keys/README.md`
- `/db/engines/AGENTS.md`


