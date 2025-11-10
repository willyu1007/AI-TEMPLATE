# doc_human/

This directory holds long-form documentation for humans: deep guides, templates, and historical decisions. Keep everything factual, actionable, and in the repository language (English unless `config/language.yaml` says otherwise).

## Layout
```text
doc_human/
|-- guides/        # Detailed how-to guides
|-- policies/      # Goals, safety, quality, security deep dives
|-- project/       # PRD, release train, summaries
|-- architecture/  # Structural references
|-- adr/           # Architecture decision records
|-- reference/     # Command/pr workflow references
|-- templates/     # Workdoc + module templates
`-- examples/      # Example module and docs
```

## Usage
- Load `doc_agent/*` first for quick tasks, then come here if you need narrative context or examples.
- Update both AI and human docs when workflows change (AI doc stays lean; human doc captures rationale).
- Mention the language requirement in every template so contributors remember to keep comments/reports consistent.

## Key Files
- Guides: `PROJECT_INIT_GUIDE.md`, `PROJECT_MIGRATION_GUIDE.md`, `MODULE_INIT_GUIDE.md`, `GUARDRAIL_GUIDE.md`, `WORKDOCS_GUIDE.md`.
- Policies: `goals.md`, `safety.md`, `quality_standards.md`, `security_details.md`.
- Templates: `templates/module-templates/*.md`, `templates/workdoc-*.md`.
- Examples: `examples/module-example/` contains a fully documented sample module.

Keep documents concise but thorough: focus on steps, decisions, and ownership instead of storytelling.

