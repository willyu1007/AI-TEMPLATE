# Runbook - Common Module

Shared library; no runtime service. Checklist:
- Run `pytest tests/common/ -v`.
- Update docs/templates and ensure English language compliance.
- Regenerate docs via `make docgen`.
- If guardrails fail, fix before other modules consume the helpers.

