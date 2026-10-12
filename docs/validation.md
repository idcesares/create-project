# Validation record

Each section records what was executed for a version and what was not.
GitHub Actions runs package checks, tests, and a prepare-only evaluation pass
on Windows and Linux with Python 3.11 and 3.14; the Actions run for a commit is
the source of truth for its CI status.

## 0.2.0 (2026-10-12)

Environment: Linux, Python 3.13.16, PyYAML 6.0.1, Node.js 22.

- `python scripts/validate.py`: `PASS: create-project` and `PASS: evals`.
- `python -m unittest discover -s tests -v`: 30 tests passed, covering the new
  frontmatter, unlinked-file, reference-length, and body-size rules, eval
  definition errors, glob matching, and the runner's checks, turn order,
  skill installation, baseline mode, and prepare-only mode with a scripted
  stand-in agent.
- `python scripts/run_evals.py`: prepared all 14 cases in isolated workspaces.
- Anthropic skill-creator `quick_validate.py`: `Skill is valid!`.
- `npx skills add . --list`: discovered exactly one skill, `create-project`,
  with the new description; fixture folders were not mistaken for skills.
- Fixture sanity: `resume-cli` tests pass before the next slice exists, and
  `off-by-one` tests fail on the bug as intended.

Not executed: the 14 behavioral cases and 20 trigger queries against a real
agent, with or without the skill. Behavioral improvement over 0.1.0 is
therefore designed and reviewed, not measured.

## 0.1.0 (2026-09-05)

### Executed locally

Environment: Windows, Python 3.14.6, PyYAML 6.0.3.

- `python scripts/validate.py`: passed package metadata, local file links,
  standalone license presence, and Codex interface checks.
- `python -m unittest discover -s tests -v`: 10 tests passed. Includes copying
  the skill into an isolated directory without repository files, missing
  references, escaping links, invalid metadata, and absent license coverage.
- Bundled Codex skill-creator `quick_validate.py`: reported `Skill is valid!`.
- Root and installable license copies: byte-for-byte match.
- `npx --yes skills add . --list`: discovered exactly one skill named
  `create-project` without installing a dependency catalog.
- Manual installation into the local Codex user skill directory: package
  validation passed after copying the complete skill folder.

### Scope of evidence

These checks validate packaging, not agent decision quality. The behavioral
cases (then `evals/scenarios.md`) were authored and reviewed but were not executed
as independent agent runs. Automatic triggering and end-to-end behavior in
Claude Code and Cursor have not been tested. The optional Codex metadata and
shared skill format support portability without proving identical behavior.
