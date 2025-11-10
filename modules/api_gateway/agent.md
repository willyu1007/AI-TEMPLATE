---
spec_version: "1.0"
agent_id: "modules.api_gateway.v1"
role: "API Gateway module - Request routing and middleware management"
level: 2
module_type: "2_Service/Gateway"

# Token optimization
token_budget:
  max_context: 1500
  always_load: 150
  on_demand: 1350

ownership:
  code_paths:
    include:
      - modules/api_gateway/src/*
      - modules/api_gateway/middleware/*
    exclude: []

io:
  inputs:
    - name: "http_request"
      type: "HttpRequest"
      required: true
      description: "Incoming HTTP request"
      
  outputs:
    - name: "http_response"
      type: "HttpResponse"
      required: true
      description: "Processed HTTP response"

contracts:
  apis:
    - modules/api_gateway/doc/CONTRACT.md

dependencies:
  upstream: ["modules.common"]
  downstream: ["modules.*"]

quality_gates:
  required_tests: [unit, integration, load]
  coverage_min: 0.85

context_routes:
  always_read:
    - /modules/api_gateway/README.md
  
  on_demand:
    - topic: "Routing Rules"
      paths:
        - /modules/api_gateway/doc/ROUTING.md
    - topic: "Middleware Chain"
      paths:
        - /modules/api_gateway/doc/MIDDLEWARE.md

merge_strategy: "child_overrides_parent"
---

# API Gateway Module

> High-performance request routing with middleware pipeline

## Quick Context (50 tokens)
- **Purpose**: Route HTTP requests to appropriate services
- **Features**: Rate limiting, auth, logging, caching
- **Performance**: <10ms overhead per request
- **Scaling**: Horizontal with load balancing

## Implementation Pattern (80 tokens)
```python
from modules.api_gateway import Gateway, Route

# Configure gateway
gateway = Gateway()
gateway.add_middleware('auth', AuthMiddleware())
gateway.add_middleware('rate_limit', RateLimitMiddleware())

# Define routes
@gateway.route('/api/v1/users')
async def handle_users(request):
    return await user_service.process(request)

# Start gateway
await gateway.start(port=8080)
```

## Key Patterns (50 tokens)
1. **Middleware Chain**: Sequential processing pipeline
2. **Circuit Breaker**: Fault tolerance for downstream services
3. **Request Caching**: Response caching with TTL
4. **Load Balancing**: Round-robin, least-connections

## Testing (40 tokens)
```bash
# Unit tests
pytest tests/api_gateway/unit/

# Integration tests
pytest tests/api_gateway/integration/

# Load tests
locust -f tests/api_gateway/load/
```

## Configuration (30 tokens)
```yaml
gateway:
  port: 8080
  workers: 4
  timeout: 30
  middleware:
    - auth
    - rate_limit
    - logging
```

## Commands
```bash
# Development
make gateway_dev

# Production
make gateway_prod
```

## References
- Contract: `/modules/api_gateway/doc/CONTRACT.md`
- Examples: `/modules/api_gateway/examples/`
- Config: `/modules/api_gateway/config/`

---
*Total: ~150 lines (optimized for AI context)*
