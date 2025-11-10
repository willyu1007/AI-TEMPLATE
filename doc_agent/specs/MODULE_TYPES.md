---
audience: ai
language: en
version: summary
---
# Module Type Specification

> **Purpose**: Define module classification standards and naming conventions
> **Version**: 2.0
> **Last Updated**: 2025-11-09

---

## Quick Reference

### 4 Core Types

| Type | Naming | Level | Responsibility | Typical Instances |
|------|--------|-------|----------------|-------------------|
| **Assign** | `1_<entity>` | 1-2 | CRUD operations | user, order, product |
| **Select** | `2_<domain>` | 1-2 | Query/filter data | user_query, data_filter |
| **SelectMethod** | `3_<strategy>` | 2-3 | Strategy selection | payment_method, shipping_method |
| **Aggregator** | `4_<domain>_aggregator` | 3-4 | Data aggregation | dashboard, report |

### Quick Decision Tree

```
Need CRUD operations? → 1_Assign
Need query/filter? → 2_Select  
Need strategy selection? → 3_SelectMethod
Need data aggregation? → 4_Aggregator
```

**Detailed IO Contracts**: See `MODULE_TYPE_CONTRACTS.yaml`

---

## Core Concepts

### Module Type Definition

Module Type is an abstract classification of module functionality:
- **Same-type modules follow identical IO contracts** - Ensures replaceability
- **Same-type modules are interchangeable** - No system impact
- **Type determines orchestration role** - Defines responsibility boundaries

### Type vs Instance

```
Type (Abstract)          Instance (Concrete)
1_Assign                1_user, 1_order, 1_product
2_Select                2_user_query, 2_data_filter
3_SelectMethod          3_payment_method, 3_cache_strategy
4_Aggregator            4_dashboard_aggregator
```

### Module Instance Definition
The authoritative checklist lives in `doc_human/guides/MODULE_INSTANCES.md`. Use it after `make ai_begin MODULE=<name>` to ensure the instance:
- Conforms to one module type contract (this file + `MODULE_TYPE_CONTRACTS.yaml`).
- Ships all required docs/tests/registry entries so orchestration can enforce guardrails.
- Records ownership, guardrails, and escalation paths in the shared guide.

---

## Type Specifications

### 1_Assign (Entity Management)

**Purpose**: Basic CRUD operations for single entity
**Level**: 1-2
**Naming**: `1_<entity>` (e.g., 1_user, 1_product)

**Responsibilities**:
- Create, Read, Update, Delete operations
- Data validation
- Business rules enforcement
- Transaction management

**IO Contract**:
```yaml
input:
  operation: create|read|update|delete
  entity: object
  id?: string
output:
  success: boolean
  data?: object
  error?: string
```

### 2_Select (Query Processing)

**Purpose**: Data query and filtering
**Level**: 1-2
**Naming**: `2_<domain>` (e.g., 2_user_query, 2_log_filter)

**Responsibilities**:
- Complex query execution
- Data filtering and sorting
- Pagination support
- Result transformation

**IO Contract**:
```yaml
input:
  query: object
  filters?: array
  sort?: object
  pagination?: object
output:
  success: boolean
  data: array
  total?: number
  error?: string
```

### 3_SelectMethod (Strategy Execution)

**Purpose**: Select and execute strategies
**Level**: 2-3
**Naming**: `3_<strategy>` (e.g., 3_payment_method, 3_auth_strategy)

**Responsibilities**:
- Strategy selection logic
- Method execution
- Result validation
- Fallback handling

**IO Contract**:
```yaml
input:
  method: string
  params: object
  context?: object
output:
  success: boolean
  result: any
  method_used: string
  error?: string
```

### 4_Aggregator (Data Aggregation)

**Purpose**: Aggregate data from multiple sources
**Level**: 3-4
**Naming**: `4_<domain>_aggregator` (e.g., 4_dashboard_aggregator)

**Responsibilities**:
- Multi-source data collection
- Data transformation
- Computation and statistics
- Result caching

**IO Contract**:
```yaml
input:
  sources: array
  aggregation: object
  timeframe?: object
output:
  success: boolean
  aggregated_data: object
  metadata?: object
  error?: string
```

---

## Usage Guidelines

### Type Selection

1. **Start with responsibility analysis**
   - What is the module's primary function?
   - What data does it process?
   - What operations does it support?

2. **Match to type pattern**
   - CRUD → 1_Assign
   - Query → 2_Select
   - Strategy → 3_SelectMethod
   - Aggregation → 4_Aggregator

3. **Verify IO contract compatibility**
   - Input/output matches type specification
   - Can replace existing same-type modules

### Naming Conventions

```
Format: <type_prefix>_<domain>_<specific>

Examples:
1_user           - User entity CRUD
2_user_query     - User query processor
3_payment_method - Payment strategy selector
4_sales_aggregator - Sales data aggregator
```

---

## See Also

- `MODULE_TYPE_CONTRACTS.yaml` - Detailed IO contracts
- `MODULE_INSTANCES.md` - Registered module instances
- `doc_agent/orchestration/registry.yaml` - Module registry

---

**Maintained by**: Architecture Team
**Questions**: Check module type before implementation
