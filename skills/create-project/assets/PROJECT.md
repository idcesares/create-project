# Project name

<!-- Intent and navigation for a multi-session project. Keep each fact in one
place: link to the spec, decisions, and evidence instead of copying them.
Delete any section that has no real content yet. -->

## Outcome

Who receives what useful result, and why it matters now.

## Scope

- In: capabilities this project delivers.
- Out: explicit non-goals.

## Constraints

Existing choices, platforms, budgets, data rules, and deadlines that bind the
design.

## Acceptance

| ID | Criterion | Check that proves it | State |
| --- | --- | --- | --- |
| A1 | A user can save a draft and see it after reopening | `pytest tests/test_drafts.py::test_reopen` | Not run |

State is one of: Not run, Passed, Failed, Not verified (with the reason).

## Assumptions

Unconfirmed statements the approach depends on, and how each could be checked.

## Decisions

- [0001: Storage engine](docs/adr/0001-storage-engine.md): one-line gist.

## State

- Phase: contract | tracer bullet | slices | delivery | blocked
- Last verified: date, command, result
- Blocker: the exact prerequisite, or none
- Next action: one concrete step a new session can start on

## Map

- Run: the command that starts or exercises the project
- Test: the command that verifies it
- Spec, research, and work records: links, if they exist
