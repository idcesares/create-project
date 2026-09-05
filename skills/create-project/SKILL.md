---
name: create-project
description: >-
  Turn an idea for a new software, AI, data, automation, or research project
  into a scoped and validated outcome, or resume that project from its saved
  context. Use when the user wants to create, build, or start a project and
  needs coordination from intent through delivery. Do not activate for an
  isolated bug fix, routine edit, or question about an existing codebase.
license: MIT
metadata:
  version: "0.1.0"
---

# Create Project

Own the route from the user's intent to evidence that the requested outcome
works. Choose the smallest process that resolves the actual uncertainty.
Optimize for a useful, defensible outcome rather than code or document volume.

## Start from intent and evidence

Read the current request, relevant conversation, repository instructions,
existing project notes, and working tree before proposing a new structure.
Use existing discovery tools and conventions; do not assume a particular MCP,
shell, framework, tracker, or companion skill exists.

Distinguish the requested endpoint: exploration, plan, prototype, implementation,
or delivery. A planning request ends with a plan; an implementation request
continues through implementation and validation. Resume unfinished work from
the evidence on disk instead of restarting discovery. A later correction changes
the affected decisions and work, not necessarily the whole objective.

Discover facts yourself. Infer reversible technical choices from the repository
and current evidence, state material assumptions, and proceed. Ask only when a
missing answer changes the product purpose, meaningful scope, privacy, cost, or
an expensive-to-reverse choice. Give a recommendation and the tradeoff in plain
language. Continue independent work while a necessary answer is pending; silence
does not resolve that question. Do not make the user choose a stack merely to
fill in a questionnaire.

## Choose the route

Assess scope, uncertainty, and consequences independently. A tiny tool can have
important data-loss risks; a large familiar application may need little research.
Explain the chosen route briefly without requiring approval of routine phases.

| Situation | Useful route | Durable record |
| --- | --- | --- |
| Small and clear | Brief acceptance criteria, implement, run, review | Compact project note if persistence is useful |
| Multi-session build | Scope, key decisions, acceptance criteria, end-to-end slices, validate | Project intent plus the supporting records actually needed |
| Uncertain feasibility or design | Resolve the blocking questions through research or a bounded prototype, then reclassify | Evidence, decision, and next step |
| Research or experiment | Question, method, baseline, experiment, reproducible result | Method, inputs, limitations, findings |

Use these references only when their condition applies. Paths are relative to
this installed skill directory, not the user's project directory.

- [Discovery and uncertainty](references/discovery.md): ambiguous outcomes,
  current technical facts, competing designs, or a research-heavy effort.
- [Project memory](references/project-memory.md): work spanning sessions,
  consequential decisions, specifications, or resuming existing work.
- [Build and verification](references/build-and-verify.md): multi-step
  implementation, AI behavior, data workflows, or material operational risks.
- [Delivery](references/delivery.md): a completed requested endpoint or a handoff
  blocked by a real external prerequisite.

For a simple task, work directly from this entrypoint. These references are
guidance, not a required sequence of separate roles or installed skills.

## Establish what success means

Capture the problem, intended user or consumer, requested outcome, constraints,
explicit non-goals, and observable acceptance criteria. Reuse existing records.
Use a short note for a small task and a specification for a complex contract;
do not create empty architecture, research, or ticket folders.

For multi-session projects, keep `PROJECT.md` as intent and a navigation point
unless the repository already has an equivalent. Link to evidence and keep the
current phase, unresolved blockers, and next step recoverable. Split context,
specification, and decision records only when they have distinct information to
preserve. Do not overwrite `AGENTS.md` or turn project notes into permissions.

Settle the decisions that block the first useful result. Prefer the simplest
architecture satisfying the acceptance criteria. Record consequential choices
with their reasons and evidence; leave deferred choices explicitly open.

## Produce the smallest useful result

Scaffold for the selected project and existing environment. Add dependencies,
infrastructure, configuration, and tooling only for a demonstrated requirement.
Use a relevant installed specialist skill when it helps, but remain able to
perform the workflow without one. Preserve explicit user choices.

For a build, make one small end-to-end behavior run before expanding it. Include
the relevant input, processing, output, and persistence or integration boundary.
For research, execute one reproducible experiment or analysis before scaling the
method. If that first result contradicts the design, revisit the affected choice
before multiplying the implementation.

Implement remaining work as observable capabilities with clear dependencies.
Use test-first development when it clarifies a behavioral contract; use the
appropriate run, visual check, experiment, or integration check for other work.
Verify meaningful failure paths in proportion to risk. A build passing alone
does not establish acceptance. Keep simulated and real integrations distinct.

Delegation is optional and follows the host's permissions. If available and
authorized, delegate only bounded independent work with clear file ownership,
inputs, and acceptance evidence. Keep overall decisions and integration with the
primary agent. Proceed sequentially when delegation adds no value.

## Close against evidence

Compare the result to the user's requested endpoint and each acceptance
criterion. Check both behavior and the maintainability of the actual changes.
Run relevant checks, investigate failures, and update run instructions and
project memory to match what exists. Distinguish passed, failed, and not-run
checks, with their evidence. Do not invent compliance percentages or label a
stub, untested integration, or unresolved requirement complete.

Finish authorized work before handing back. Building a project does not itself
authorize public publication, deployment, paid provisioning, external messages,
or destructive operations. Reuse authorization already given for such actions;
ask for a missing decision only after preparing the concrete result for review.
If blocked, describe the precise prerequisite and preserve a runnable next step.

Report the delivered outcome, how to use it, validation performed, material
limitations, and any action still required. Keep the explanation proportional
to the work.
