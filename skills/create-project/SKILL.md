---
name: create-project
description: >-
  Use when someone wants to start, build, plan, or prototype something new from
  an idea: an app, CLI, service, library, agent, data pipeline, automation, or
  research effort, including loose asks such as "I want to make a tool that..."
  or "help me build an MVP" that never say "project". Also use when resuming a
  project tracked in PROJECT.md or similar notes, or when the request names an
  endpoint such as "plan only" or "just a prototype". Not for a single bug fix,
  a routine change to an existing codebase, or a question about code.
license: MIT
metadata:
  version: "0.2.0"
---

# Create Project

You own the route from an idea to **evidence** that the requested **endpoint**
is reached. Size the process to the real uncertainty. The deliverable is a
working, verified result, or the plan or findings that were asked for; files,
folders, and documents count only when they serve that result.

Facts are yours to find. Decisions about purpose, scope, and risk are the
user's. Work with the tools, conventions, and permissions the host provides;
every companion skill, tracker, MCP server, or subagent is optional.

## Workflow

Copy this checklist into your task list or notes and keep it current. Stop at
the requested endpoint: a plan request ends at step 3 with the plan delivered;
a research request ends with reproducible findings.

```text
- [ ] 1. Orient: endpoint, existing state, constraints
- [ ] 2. Route: size, uncertainty, consequences
- [ ] 3. Contract: outcome, non-goals, observable acceptance checks
- [ ] 4. Tracer bullet: one end-to-end behavior observed running
- [ ] 5. Slices: remaining capabilities, each verified
- [ ] 6. Close: evidence per criterion, usable handoff, resumable state
```

### 1. Orient

Read the request, the conversation, repository instructions (`AGENTS.md`,
`CLAUDE.md`, `README.md`), any project record such as `PROJECT.md`, and the
working tree. Name the endpoint: **explore**, **plan**, **prototype**,
**build**, or **deliver**. A later correction changes the affected decisions
and work; the rest of the objective stands.

When resuming, treat notes as claims. Run the recorded check, compare the
recorded state with the tree, and let the user's current instruction override
stale notes. See [project memory](references/project-memory.md).

Done when you can state the endpoint, what already exists, and the binding
constraints in one sentence each.

### 2. Route

Judge scope, uncertainty, and consequences separately: a tiny tool can still
destroy data, and a large familiar app may need no research.

| Situation | Route | Durable record |
| --- | --- | --- |
| Small and clear | Brief acceptance checks, tracer bullet, verify | None, or a short note in the reply |
| Multi-session build | Contract, key decisions, tracer bullet, slices | `PROJECT.md` plus only the records that carry distinct information |
| Uncertain feasibility or design | Bounded research or prototype, then reroute | Evidence, decision, next step |
| Research or experiment | Question, method, baseline, reproducible run | Method, inputs, limitations, findings |

State the route in one line and continue; routine phases need no approval.
Read [discovery](references/discovery.md) when an open question could change
the design or invalidate the build.

### 3. Contract

Discover facts yourself. Infer reversible technical choices from the
repository and request, and state them as assumptions. Ask only about choices
that change product purpose, meaningful scope, privacy, ongoing cost, or are
expensive to reverse. Put every blocking question in one message, at most
three, each with your recommendation and its tradeoff in plain language. Keep
working on everything that does not depend on the answer; silence leaves the
question open.

Record the outcome, intended user, non-goals, constraints, assumptions, and
acceptance checks. A small task keeps this in the reply. A multi-session
project starts `PROJECT.md` from [the template](assets/PROJECT.md) unless the
repository already has an equivalent. Settle only the decisions that block the
first useful result and record consequential ones with their reasons.

Done when every acceptance criterion names the observation that will prove it.

### 4. Tracer bullet

Build the thinnest behavior that crosses every real boundary: input,
processing, output, and the persistence or integration point. For research,
run one reproducible analysis on real inputs. Use the existing stack; add a
dependency, service, or configuration only for a demonstrated requirement.

If the result contradicts the design, revisit that decision now, while it is
cheap. Done when you have run it and seen the output.

### 5. Slices

Grow the result one observable capability at a time. For each slice, choose
the check first (a failing test when it clarifies a behavioral contract; a
run, visual check, or experiment otherwise), implement, run the check, and
review the diff. Cover failure paths in proportion to risk. Label simulated
integrations as simulated. Read [build and verification](references/build-and-verify.md)
for multi-step builds, AI behavior, data workflows, or operational risk.

Delegate only bounded, independent work with clear file ownership and an
acceptance check, when the host allows it. Integration and final decisions
stay with you. After each verified slice of multi-session work, update the
project record's state and next action so the work stays **resumable**.

Done when each slice's check has run and passed, or its failure is recorded.

### 6. Close

Hold every claim to the evidence gate:

| Claim | Evidence | Not enough |
| --- | --- | --- |
| It works | Observed run of the user flow, or test output from this session | Code written; build passed |
| Criterion met | That criterion's named check passed | Related tests pass |
| Integration works | A call against the real service | Mock, fixture, or stub |
| Delegated work is done | Inspected diff and re-run checks | The worker's report |
| Published or deployed | The live destination, checked | The push or deploy command started |

Report each check as passed, failed, or not run, with its evidence. Read
[delivery](references/delivery.md) for substantial work or a blocked handoff.

Building is authorization to build. Publishing, deploying, paid provisioning,
external messages, and destructive operations need authorization of their
own; reuse any already given, and otherwise prepare the concrete result first,
then ask. When blocked, leave the working result, the exact prerequisite, and
a runnable next step.

Finish with the outcome, how to use it, the evidence, material limitations,
and any action still required, in proportion to the work.

## Traps

| Thought | Instead |
| --- | --- |
| "Scaffold the full structure first." | Make one behavior run end to end; structure follows need. |
| "Ask which stack they prefer." | Infer it from the repository and request, state it, proceed. |
| "The mock passes, so the integration is done." | Mark it simulated; real verification stays open. |
| "The build is green, so we're done." | Check each acceptance criterion against its own evidence. |
| "They asked me to build it, so I'll ship it." | Prepare it locally; publishing needs its own authorization. |
| "The notes say X, so X is true." | Verify X against the working tree and the user's latest word. |
| "One more retry might work." | Diagnose; if the prerequisite cannot change, record the blocker and move on. |

## Bundled files

Paths are relative to this skill's directory, not the user's project. Load
each only when its condition applies.

- [references/discovery.md](references/discovery.md): ambiguous outcomes,
  current technical facts, competing designs, research-heavy efforts.
- [references/project-memory.md](references/project-memory.md): multi-session
  work, consequential decisions, specifications, resuming.
- [references/build-and-verify.md](references/build-and-verify.md): multi-step
  builds, AI behavior, data workflows, operational risk.
- [references/delivery.md](references/delivery.md): substantial completion or
  a handoff blocked by an external prerequisite.
- [assets/PROJECT.md](assets/PROJECT.md), [assets/SPEC.md](assets/SPEC.md),
  [assets/adr.md](assets/adr.md): starting points to copy when that record is
  needed; delete any section without real content.
