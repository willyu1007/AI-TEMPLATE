# Script Consolidation Analysis

## Current State: 39 checking/validation scripts

### Category 1: Documentation Checks (7 scripts)
```
doc_style_check.py       - Check doc headers and formatting
doc_freshness_check.py   - Check if docs are up-to-date
doc_route_check.py       - Validate context routes
doc_script_sync_check.py - Ensure docs match scripts
agent_lint.py            - Validate AGENTS.md files
registry_check.py        - Validate registry entries
module_health_check.py   - Check module documentation
```
**Consolidation potential**: HIGH - Could merge into `doc_validator.py`

### Category 2: Code Quality Checks (6 scripts)
```
python_scripts_lint.py   - Python linting
complexity_check.py      - Cyclomatic complexity
coupling_check.py        - Module coupling analysis
consistency_check.py     - Cross-repo consistency
app_structure_check.py   - Application structure
refactor_suggest.py      - Refactoring suggestions
```
**Consolidation potential**: MEDIUM - Could merge into `code_quality.py`

### Category 3: Health & Metrics (5 scripts)
```
health_check.py          - Overall repo health
module_health_check.py   - Module-specific health
ai_friendliness_check.py - AI compatibility
observability_check.py   - Monitoring coverage
health_trend_analyzer.py - Health trends over time
```
**Consolidation potential**: HIGH - Could merge into `health_suite.py`

### Category 4: Configuration & Contract (8 scripts)
```
config_lint.py           - Config validation
runtime_config_check.py  - Runtime config check
contract_compat_check.py - Contract compatibility
type_contract_check.py   - Type contracts
frontend_types_check.py  - Frontend type checking
makefile_check.py        - Makefile validation
dag_check.py            - DAG validation
migrate_check.py        - Migration validation
```
**Consolidation potential**: LOW - Different domains, keep separate

### Category 5: Database & Resources (3 scripts)
```
db_lint.py              - Database schema validation
resources_check.py      - Resource availability
secret_scan.py         - Security scanning
```
**Consolidation potential**: LOW - Different concerns

### Category 6: Testing (2 scripts)
```
test_status_check.py    - Test completion tracking
test_coverage_check.py  - Coverage reporting
```
**Consolidation potential**: HIGH - Could merge into `test_tools.py`

## Recommendation

### Phase 1: High-Value Consolidations (Now)
1. **Documentation tools** (7→1): Create `doc_tools.py` with subcommands
2. **Health checks** (5→1): Create `health_suite.py` with modules
3. **Test tools** (2→1): Create `test_tools.py`

**Total reduction**: 14 scripts → 3 scripts (78% reduction)

### Phase 2: Medium-Value Consolidations (Later)
4. **Code quality** (6→1): Create `code_quality.py` when patterns stabilize

### Keep Separate (Domain-specific)
- Config/contract validators (each has unique logic)
- Database tools (specialized)
- Security scanning (isolated concern)

## Implementation Strategy

### Example: Consolidating Documentation Tools

```python
# doc_tools.py
import argparse

def style_check():
    """Check documentation style and headers"""
    # Logic from doc_style_check.py
    
def freshness_check():
    """Check documentation freshness"""
    # Logic from doc_freshness_check.py
    
def route_check():
    """Validate context routes"""
    # Logic from doc_route_check.py

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    
    # Add subcommands
    subparsers.add_parser('style', help='Check style')
    subparsers.add_parser('freshness', help='Check freshness')
    subparsers.add_parser('routes', help='Check routes')
    subparsers.add_parser('all', help='Run all checks')
    
    args = parser.parse_args()
    
    if args.command == 'style':
        return style_check()
    elif args.command == 'freshness':
        return freshness_check()
    elif args.command == 'routes':
        return route_check()
    elif args.command == 'all':
        # Run all checks
        results = []
        results.append(style_check())
        results.append(freshness_check())
        results.append(route_check())
        return 0 if all(r == 0 for r in results) else 1
```

### Makefile Updates Required

```makefile
# Old targets (keep for compatibility)
doc_style_check:
	@python scripts/doc_tools.py style

doc_freshness_check:
	@python scripts/doc_tools.py freshness
	
# New unified target
doc_check_all:
	@python scripts/doc_tools.py all
```

## Benefits of Consolidation

1. **Reduced maintenance**: Fewer files to update
2. **Better code reuse**: Share common functions
3. **Clearer organization**: Related tools in one place
4. **Easier discovery**: Fewer scripts to understand
5. **Consistent interfaces**: Unified command structure

## Risks to Consider

1. **Breaking changes**: Existing Makefile targets must continue working
2. **Complexity**: Consolidated files might become too large
3. **Testing**: Need comprehensive tests for consolidated tools
4. **Documentation**: Must update all references
