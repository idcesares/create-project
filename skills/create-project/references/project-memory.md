# Project memory

Repository files carry intent, decisions, evidence, and the next action across
sessions. Follow the repository's established document locations and link
rather than copy. The filenames below are defaults, not a required scaffold.

## Choose records by purpose

| Record | Owns | Create when |
| --- | --- | --- |
| `PROJECT.md` | Outcome, scope, constraints, acceptance, state, navigation | The project spans sessions or people |
| `CONTEXT.md` | Domain vocabulary, sourced facts, open questions | Accumulated understanding outgrows `PROJECT.md` |
| `docs/SPEC.md` | Behavior, interfaces, failure behavior, acceptance | Several slices need one shared contract |
| `docs/adr/NNNN-topic.md` | One consequential decision, alternatives, consequences | The reason for a decision must outlive the session |
| `docs/work.md` or an existing tracker | Slices, dependencies, progress | Work needs explicit sequencing or handoff |
| `README.md` | What exists and how a human installs, runs, tests, and uses it | There is a deliverable to use |
| `AGENTS.md` | Repository-specific operating instructions | Local instructions are missing and adding them is in scope |

Give each fact a single owner and link to it elsewhere. Templates for the
first three kinds live in this skill's `assets/` folder: `PROJECT.md`,
`SPEC.md`, and `adr.md`. Copy one only when the record is needed, and keep only
the sections that hold real information. An existing `AGENTS.md` belongs to
the user: extend it when that is in scope, and keep project notes free of
permission grants.

## Small project note

A one-session project can keep these lines in the reply or a short existing
document; a stateless or advisory task needs no file at all.

```markdown
Outcome: Who receives what useful result.
Scope: Capabilities to deliver; explicit exclusions.
Constraints: Existing choices and practical limits.
Acceptance: Observable checks of success.
Assumptions: Unconfirmed statements that affect the approach.
State: Current phase, blocker if any, and next action.
```

## Specifications and work items

Describe requirements as observable behavior: inputs and outputs, important
data relationships, trust boundaries, failure behavior, and any performance or
reliability target with its reason. Give acceptance criteria stable IDs when
tests or work items refer to them. Keep "desired", "implemented", and
"verified" as distinct states.

A work item is a **vertical slice**: a useful behavior a user or caller can
observe, such as "a user can save and reopen a draft", rather than separate
database, backend, and frontend tickets. It names its acceptance criteria,
prerequisites, owned files or interfaces, verification, and exclusions. Local
work records suffice when no tracker is configured; writing to an external
tracker requires authorization.

## Resuming and changing direction

1. Read `PROJECT.md` (or its equivalent): outcome, acceptance, state, next
   action.
2. Observe the tree: run the recorded test or run command, and check that the
   recorded status still matches the implementation.
3. Reconcile. The user's current instruction outranks older notes; a conflict
   that changes scope gets surfaced before dependent work starts. Preserve
   unrelated user edits.
4. Continue from the next action, and update the record when it changes.

Update records after a material decision, a verified slice, a scope
correction, or a handoff. Supersede an old decision with a new record that
links to it, so the historical reasoning survives. Keep credentials, private
transcripts, and unneeded personal data out of project memory.
