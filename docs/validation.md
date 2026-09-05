# Initial validation

Validation of the initial `0.1.0` package on 2026-09-05.

## Executed locally

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

## Scope of evidence

These checks validate packaging, not agent decision quality. The behavioral
cases in `evals/scenarios.md` were authored and reviewed but were not executed
as independent agent runs. Automatic triggering and end-to-end behavior in
Claude Code and Cursor have not been tested. The optional Codex metadata and
shared skill format support portability without proving identical behavior.

GitHub Actions runs the package checks and tests on Windows and Linux with
Python 3.11 and 3.14; the Actions run for a commit is the source of truth for
its CI status. This note records the initial local evidence, not future runs.
