# Context Index Rules

> Defines how `.aicontext/` is generated and consumed.

## Purpose
- Fast lookup for agents without loading the entire repo.
- Track file summaries, keywords, and dependencies.
- Never replace the original documents; this is metadata only.

## Collected Data
- **Documents** - README, agent files, contracts, changelogs, guides.
- **APIs** - OpenAPI specs, public function signatures, models.
- **Dependencies** - registry entries, DAGs, module dependencies.

## Exclusions
- Binary assets, generated folders (`node_modules`, `dist`, etc.), and `.aicontext` itself.
- Secrets or credential files.

## Large File Strategy
Split files >500 KB by topic and store slices with tags:
```yaml
- file: modules/user/core/service.py
  slices:
    - lines: 1-200
      topic: auth
      tags: [module:user, domain:auth, lang:python]
```

## Generation
```bash
make docgen
```
Outputs include:
- `.aicontext/summary.yaml` - file summaries + hashes.
- `.aicontext/keywords.yaml` - search index.
- `.aicontext/deps.yaml` - dependency graph.
- `.aicontext/hash.yaml` - change detection.

`docgen` updates entries incrementally by comparing hashes.

## Usage
- Agents read `.aicontext/summary.yaml` at startup for a mental map.
- Scripts use `keywords.yaml` to find relevant files quickly.
- Guardrails read `deps.yaml` to determine upstream/downstream impact.

## Maintenance
- Run `make docgen` after meaningful changes or as part of CI (`make dev_check`).
- Periodically verify coverage (simple `find` + `grep` to spot missing files).
- Keep summaries to 1-2 sentences, objective and action-oriented.

## Roadmap
- Potential call graph and coverage overlays.
- No plan for full-text indexing (use `rg` instead).

Keep this document synced when docgen behavior or inclusion rules change.

