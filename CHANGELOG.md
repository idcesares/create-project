# Changelog

## 0.2.0 - 2026-10-12

- Description states trigger conditions only, covers loose requests that never
  say "project", and keeps the near-miss exclusions.
- `SKILL.md` is a six-step workflow with a copyable checklist, a completion
  condition per step, a batched question protocol, an evidence gate, and a
  table of common traps. Guidance favors positive targets over prohibitions.
- Added `PROJECT.md`, `SPEC.md`, and ADR templates under `assets/`.
- Added a numbered resume procedure to the project memory reference.
- Replaced the prose scenario table with `evals/evals.json` (14 cases with
  fixtures and deterministic checks), `evals/trigger-queries.json` (20 queries),
  and `scripts/run_evals.py`, which runs cases against an agent CLI in isolated
  workspaces with an optional no-skill baseline.
- Validation now rejects unknown frontmatter keys, angle brackets in the
  description, bundled files not linked from `SKILL.md`, long references
  without contents, oversized bodies, and malformed eval definitions.

## 0.1.0 - 2026-09-05

- Initial portable skill with conditional references, package validation, and
  manual scenarios.
