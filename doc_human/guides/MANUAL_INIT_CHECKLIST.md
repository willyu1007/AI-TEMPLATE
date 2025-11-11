---
audience: human
language: en
version: checklist
purpose: Manual tasks to complete after requesting initialization support
---

# Manual Initialization Checklist

Use this checklist when you prefer to edit files yourself or need to verify AI-assisted initialization.

## Before Editing

- [ ] Confirm repository language in `config/language.yaml` and share it with the team.  
- [ ] Decide which initialization mode you are following (document-driven, create-doc-first, manual, or migration).  
- [ ] Gather requirement docs, architecture notes, and module lists.

## During Initialization

- [ ] Keep a running workdoc capturing decisions and outstanding questions.  
- [ ] Review AI summaries and approve plans before files are modified.  
- [ ] Run `pip install -r requirements.txt` (or equivalent) to validate dependency setup.  
- [ ] Execute agreed Make targets (`make ai_begin`, `make docgen`, etc.) or record that the AI executed them.

## After Editing

- [ ] Rewrite `README.md` with project name, purpose, quick start, and workflows.  
- [ ] Update root `AGENTS.md` context routes and metadata.  
- [ ] Update or create required docs under `doc_agent/` and `doc_human/`.  
- [ ] Scaffold initial modules (docs, tests, registry entries) if applicable.  
- [ ] Run guardrail checks (`make agent_trigger_test`, `make dev_check`).  
- [ ] Remove temporary scaffolding (`TEMPLATE_USAGE.md`, the old `doc_human/init/` folder).  
- [ ] Record open items in workdocs or issue tracker.  
- [ ] Notify the AI that manual initialization is complete.


