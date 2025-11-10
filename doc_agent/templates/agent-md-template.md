---
spec_version: "1.0"
agent_id: "{module_name}"
role: "{module_description}"
level: {level_number}
module_type: "{module_type}"

# Token optimization settings
token_budget:
  max_context: 2000
  always_load: 200
  on_demand: 1800
  
ownership:
  code_paths:
    include:
      - modules/{module_name}/src/*
      - modules/{module_name}/tests/*
    exclude: []

io:
  inputs:
    - name: "{input_name}"
      type: "{input_type}"
      required: true
      description: "{input_description}"
      
  outputs:
    - name: "{output_name}"
      type: "{output_type}"
      required: true
      description: "{output_description}"

contracts:
  apis:
    - modules/{module_name}/doc/CONTRACT.md

dependencies:
  upstream: []
  downstream: []

constraints:
  - "{constraint_1}"
  - "{constraint_2}"

quality_gates:
  required_tests: [unit, integration]
  coverage_min: 0.80

context_routes:
  always_read:
    - /modules/{module_name}/README.md
  
  on_demand:
    - topic: "Implementation Details"
      paths:
        - /modules/{module_name}/doc/CONTRACT.md
        - /modules/{module_name}/doc/PATTERNS.md

merge_strategy: "child_overrides_parent"
---

# {Module Name} Agent

> {One-line description for AI context}

## Quick Context (50 tokens)
- **Purpose**: {core_purpose}
- **Input**: {main_input}
- **Output**: {main_output}
- **Dependencies**: {key_deps}

## Implementation Guide (100 tokens)
```python
# Minimal example
from modules.{module_name} import {MainClass}

instance = {MainClass}()
result = instance.process(input_data)
```

## Key Patterns (50 tokens)
1. {pattern_1}
2. {pattern_2}
3. {pattern_3}

## Testing Strategy (50 tokens)
- Unit: Test {what_to_unit_test}
- Integration: Verify {what_to_integration_test}
- Coverage: Minimum {coverage}%

## Commands
```bash
# Development
pytest tests/{module_name}/

# Validation  
make {module_name}_check
```

## References (50 tokens)
- Contract: `/modules/{module_name}/doc/CONTRACT.md`
- Examples: `/modules/{module_name}/examples/`
- Tests: `/tests/{module_name}/`

---
*Total estimated tokens: ~300*
