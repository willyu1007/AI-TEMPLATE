---
audience: human
language: en
version: reference
purpose: Command quick reference
---
# Command Reference

| Area | Command | Description |
|------|---------|-------------|
| Setup | `pip install -r requirements.txt` | Install Python deps |
| Docs | `make docgen` | Regenerate headers + index |
| Docs | `make doc_style_check` | Validate language + headers |
| Guardrails | `make agent_trigger FILE=<path>` | Run guardrail on file |
| Guardrails | `make agent_trigger_prompt PROMPT="..."` | Prompt-based guardrail |
| Quality | `make dev_check` | Aggregated lint/test/doc suite |
| DB | `make migrate_check` | Ensure migration pairs |
| DB | `make rollback_check PREV_REF=<tag>` | Dry-run rollback |
| Modules | `make ai_begin MODULE=<name>` | Scaffold module |
| Workdocs | `make workdoc_create TASK=<name>` | Create workdoc |
| Workflow | `make workflow_suggest PROMPT="..."` | Suggest workflow pattern |

Add more commands as automation grows; keep descriptions concise and English-only.
