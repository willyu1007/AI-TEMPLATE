# Contributing Guide

This repository is designed for AI-assisted teams, so contributions must stay lightweight, traceable, and testable. Follow the rules below and reference `AGENTS.md` whenever something is unclear.

## Scope
- Report reproducible bugs.
- Suggest improvements to documentation, guardrails, or automation.
- Submit code for modules, scripts, or docs.

## Before You Start
1. Fork the repository and sync it with upstream.
2. Read `AGENTS.md` (especially routing, guardrails, and code review sections).
3. Configure your environment: Python 3.11+, Docker, Make, and the tools listed in `requirements.txt`.
4. Respect the configured language (`config/language.yaml`); comments and docs must follow that language.

## Reporting Issues
Use GitHub Issues and include:
- Clear description and motivation.
- Steps to reproduce (commands, expected vs actual behavior).
- Environment info (OS, Python version, tool versions).
- Logs or screenshots if available.

## Suggesting Features
1. Describe the user value and workflows affected.
2. Provide constraints or guardrails that must remain.
3. Propose an implementation outline or point to related scripts/docs.
4. Tag whether it requires updates to `AGENTS.md`, guardrails, or doc roles.

## Submitting Code
```bash
git clone git@github.com:<you>/templateai.git
cd templateai
git remote add upstream git@github.com:TemplateAI/AI-TEMPLATE.git
git checkout -b feature/<topic>
```

### Development Workflow
```bash
make ai_begin MODULE=my_feature   # if starting a module
<implement feature>
make dev_check                    # run before every commit
```

### Coding Standards
- Python: PEP 8 + repository lint rules.
- TypeScript: ESLint + Prettier (see `package.json` if available).
- Go: `gofmt` + go test.
- Always run `make dev_check` before pushing.

### Commit Format
```
<type>(<scope>): <summary>
```
Types: `feat`, `fix`, `docs`, `refactor`, `build`, `test`, `chore`. Scope is optional but recommended (`scripts`, `guardrail`, `module/<name>`).

## Pull Request Checklist
- [ ] Linked Issue or motivation.
- [ ] Tests updated/added.
- [ ] Documentation updated (AI doc + human doc if relevant).
- [ ] `make dev_check` output attached or summarized.
- [ ] Guardrail/trigger changes explained clearly.

## Code Review Expectations
**As an author**
- Respond to every comment.
- Keep commits focused; rebase or fixup when requested.
- Update documentation roles if you add/remove docs.

**As a reviewer**
- Validate guardrail coverage and test depth.
- Confirm documentation follows `audience/language/purpose` front matter.
- Request clarifications when automation or routing changes are under-explained.

## High-Value Contributions
1. Stronger automation checks (doc freshness, route validation, graph health).
2. Additional workflow patterns for AI coding agents.
3. Better module templates and test data scaffolds.
4. Observability and maintenance tooling that shortens incident resolution.

## Merge Requirements
1. CI passes.
2. At least one maintainer approval.
3. Docs updated and language compliant.
4. Guardrails/tests in place for risky areas.
5. No unresolved review threads.

## Conduct
- Be respectful and concise.
- Attack problems, not people.
- Escalate sensitive topics privately.

## Contact
- Issues: GitHub Issues tab.
- Discussions: GitHub Discussions.
- Email: project maintainers (see `README.md`).

Thank you for keeping the repository AI-friendly and deterministic!
