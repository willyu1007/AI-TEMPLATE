---
audience: human
language: en
version: reference
purpose: Explain the intelligent trigger system
---
# Trigger System Guide

## Overview
`doc_agent/orchestration/agent-triggers.yaml` defines file- and prompt-based guardrail triggers. This guide helps humans extend or debug the system.

## Components
- **file_triggers** - match changed paths or glob patterns.
- **prompt_triggers** - match natural-language intents.
- **actions** - load documents, block execution, or emit suggestions.
- **skip_conditions** - allow emergency overrides with explicit reasons.

## Adding A Rule
1. Pick a unique `rule_id` and description.
2. Define `execution_mode` (`block`, `warn`, `suggest`).
3. Add path/keyword regex patterns.
4. Reference docs or scripts to load when triggered.
5. Update guardrail quickstart + workdocs with the new rule.

## Testing
```bash
make agent_trigger FILE=config/prod.yaml
make agent_trigger_prompt PROMPT="plan a database migration"
make agent_trigger_test
```
Inspect logs in `scripts/agent_trigger.py` for debugging.

## Best Practices
- Keep rules objective (match artifacts, not opinions).
- Provide remediation steps in `documents_to_load`.
- Align severity with real risk; over-blocking slows teams.
- Audit logs regularly and tune keywords to reduce noise.

## References
- `doc_agent/quickstart/guardrail-quickstart.md`
- `scripts/agent_trigger.py`
- Workdoc templates (include guardrail outcomes).

