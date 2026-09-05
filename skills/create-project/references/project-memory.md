# Project memory

Use repository files to preserve intent, decisions, evidence, and the next
action across sessions. Follow established document locations and link rather
than duplicate content. These filenames are defaults, not a required scaffold.

## Choose records by purpose

| Record | Owns | Create when |
| --- | --- | --- |
| `PROJECT.md` | Purpose, users, outcome, non-goals, constraints, phase, navigation | The project benefits from durable intent |
| `CONTEXT.md` | Domain vocabulary, sourced facts, working assumptions, unresolved questions | Accumulated understanding no longer fits the project note |
| `docs/SPEC.md` | Behavioral requirements, interfaces, failure behavior, acceptance criteria | Multiple slices need one shared contract |
| `docs/adr/NNNN-topic.md` | A consequential decision, alternatives, evidence, consequences, status | The reason for a decision must survive the session |
| `docs/work.md` or an existing tracker | Slices, dependencies, acceptance, progress | Work needs explicit sequencing or handoff |
| `README.md` | What exists and how a human installs, runs, tests, and uses it | There is a deliverable to use |
| `AGENTS.md` | Repository-specific operating instructions | Useful local instructions are missing and adding them is in scope |

Do not duplicate assumptions between files. Keep a single owner for each fact
and use links elsewhere. Add architecture and research documents only when they
carry substantial information that does not belong in an existing record.

## Small project note

For a one-session project, these fields can fit in a short existing document or
the conversation if the user does not want files:

```markdown
# Project name

Outcome: Who receives what useful result.
Scope: Capabilities to deliver; explicit exclusions.
Constraints: Existing choices and practical limits.
Acceptance: Observable checks of success.
Assumptions: Unconfirmed statements that affect the approach.
State: Current phase, blocker if any, and next action.
```

Expand only fields that contain real information. If the task is explicitly
stateless or advisory, do not create project files just to satisfy this guide.

## Specifications and work items

Describe requirements as observable behavior. Include inputs and outputs,
important data relationships, relevant trust boundaries, failure behavior, and
performance or reliability constraints with a justified target when needed.
Give acceptance criteria stable identifiers when tickets or tests reference
them. Keep "desired," "implemented," and "verified" distinguishable.

A work item should state the useful behavior, linked acceptance criteria,
prerequisites, affected interfaces or owned files, how to verify it, and what is
excluded. Prefer "a user can save and reopen a draft" to separate database,
backend, and frontend tickets. External tracker writes require authorization;
local work records are sufficient when no tracker is configured.

## Resuming and changing direction

Read intent, current work state, relevant decisions, and the actual working tree.
Check whether recorded commands and status still match the implementation.
Treat notes as evidence that may be stale, not a substitute for observation.
If sources conflict in a way that changes scope, surface that conflict before
dependent work; preserve unrelated user edits.

Update records after a material decision, verified slice, scope correction, or
handoff. Record the next concrete action and blockers. Supersede old decisions
with links instead of rewriting their historical reasons. Keep credentials,
private transcripts, and unnecessary personal data out of project memory.
