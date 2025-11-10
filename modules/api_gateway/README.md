# API Gateway Module

## Overview
High-performance API gateway with middleware pipeline for request routing, authentication, rate limiting, and observability.

## Features
- 🚀 Fast request routing (<10ms overhead)
- 🔐 Built-in authentication middleware
- ⚡ Rate limiting and throttling
- 📊 Request/response logging
- 💾 Response caching
- 🔄 Circuit breaker pattern
- ⚖️ Load balancing

## Quick Start
```python
from modules.api_gateway import Gateway

gateway = Gateway(config_file="gateway.yaml")
await gateway.start()
```

## Architecture
```
Request → [Auth] → [RateLimit] → [Logging] → [Route] → Service
           ↓         ↓             ↓           ↓
         [Cache] ← [Response] ← [Transform] ← [Result]
```

## Dependencies
- `modules.common`: Base utilities
- `aiohttp`: Async HTTP server
- `redis`: Caching and rate limiting

## Testing
```bash
# Run all tests
make gateway_test

# Coverage report
make gateway_coverage
```

## Documentation
- [Contract](./doc/CONTRACT.md)
- [Routing Guide](./doc/ROUTING.md)
- [Middleware](./doc/MIDDLEWARE.md)
- [Examples](./examples/)

## Performance
- Throughput: 10,000 req/s
- Latency: p50=5ms, p99=15ms
- Memory: ~100MB base

## License
See repository LICENSE
