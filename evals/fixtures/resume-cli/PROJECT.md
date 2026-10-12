# wordtally

## Outcome

A local CLI that summarizes word usage in plain-text files for a writer.

## Acceptance

Requirements and their states live in [docs/requirements.md](docs/requirements.md).

## State

- Phase: slices
- Last verified: 2026-09-20, `python -m unittest discover -s tests`, passed
- Blocker: none
- Next action: implement R2 (`--top N`)

## Map

- Run: `python wordtally.py FILE`
- Test: `python -m unittest discover -s tests`
