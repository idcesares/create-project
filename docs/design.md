# Design notes

## Intent

Make one project-level skill easy to install, understand, modify, and share.
The initial brief called for automatic routing from an idea through a useful
result, minimal unnecessary questions, durable context, and evidence of
completion. It also suggested a large collection of cooperating skills.

This version implements one skill with conditional references and templates.
Splitting every phase into its own skill would add installation dependencies
and overlapping triggers before there is evidence that those capabilities need
independent entry points. The installable folder contains all runtime guidance.

## Decisions

- **Adaptive depth.** Size, uncertainty, and consequences select the process.
  Research, decision maps, detailed specs, and work records are conditional.
- **Endpoint first.** The agent names the requested endpoint (explore, plan,
  prototype, build, deliver) before anything else, and stops there.
- **Facts versus decisions.** The agent discovers facts and infers reversible
  choices; the user decides purpose, scope, privacy, cost, and hard-to-reverse
  choices. Blocking questions go out together, at most three, each with a
  recommendation, while independent work continues.
- **Tracer bullet before breadth.** One end-to-end behavior through the real
  boundaries runs before the build expands, so a wrong design is found cheaply.
- **Evidence gate.** Each kind of claim names the evidence it needs and the
  evidence that does not suffice. Checks are reported as passed, failed, or not
  run. There are no completion percentages.
- **Durable, resumable intent.** `PROJECT.md` (or the repository's equivalent)
  holds outcome, acceptance, state, and the next action, so any session can
  resume by verifying the recorded state against the tree.
- **Positive targets.** Guidance states the behavior to perform; prohibitions
  remain only where a boundary must be explicit, such as authorization, and the
  traps table pairs each tempting thought with what to do instead.
- **Optional integrations.** No required MCP, issue tracker, framework, external
  skills, delegation, hooks, or setup wizard. The host retains its permissions.
- **Portable distribution.** Standard Markdown and YAML; Codex UI metadata is
  isolated in `agents/openai.yaml`. A copy of the MIT license travels with the
  installed skill. Repository tooling is kept outside that folder.
- **Executable evaluation.** Behavioral cases are data with fixtures and
  deterministic checks, runnable against any agent CLI with a no-skill
  baseline. Trigger accuracy is measured separately from behavior.
- **Incremental growth.** Add references for demonstrated needs. Split a new
  skill only when independent invocation is useful; do not add a plugin manifest,
  package manager, installer script, or runtime just to distribute instructions.

## Comparison with related projects

Reviewed on 2026-10-12 from each project's default branch.

| Project | Strength adopted here | Choice not adopted, and why |
| --- | --- | --- |
| [Matt Pocock's skills](https://github.com/mattpocock/skills) | Tracer-bullet vertical slices; facts are the agent's, decisions the user's; leading words; positive phrasing over negation; completion criteria per step | Around 30 cooperating skills with a router and a tracker setup step. One skill keeps a single trigger and no install dependencies. |
| [Superpowers](https://github.com/obra/superpowers) | Descriptions that state triggers without summarizing the workflow; an evidence gate before completion claims; tables that answer common rationalizations; testing a skill against a baseline | Hard approval gates before any building and mandatory skill chains. This skill proceeds on reversible choices and asks only about consequential ones. |
| [Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | `evals.json` layout, trigger queries with near misses, with-skill versus baseline comparison, frontmatter rules | A browser viewer and benchmark aggregation. A Markdown grading sheet per case keeps the harness small; the trigger file can feed skill-creator's tooling. |
| [Spec Kit](https://github.com/github/spec-kit) | Given/When/Then acceptance with stable IDs; a cap on clarification questions | A fixed specify, plan, tasks, implement pipeline with per-feature folders and hooks. Records here are created only when they carry information. |

## Sources and attribution

- [Agent Skills specification](https://agentskills.io/specification): portable
  directory, metadata, and progressive disclosure conventions (reviewed
  2026-09-05).
- [Matt Pocock's ask-matt](https://github.com/mattpocock/skills/blob/main/skills/engineering/ask-matt/SKILL.md),
  [wayfinder](https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md),
  and [writing-for-agents](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md):
  routing an idea through discovery, prototypes, specifications, and slices;
  resolving interdependent uncertainty; writing guidance agents follow.
- [Superpowers writing-skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md)
  and [verification-before-completion](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md):
  trigger-only descriptions and evidence before claims.
- [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md):
  evaluation layout, trigger evaluation, and frontmatter validation rules.
- [Spec Kit spec template](https://github.com/github/spec-kit/blob/main/templates/spec-template.md):
  prioritized, independently testable acceptance scenarios.
- [Skills CLI](https://github.com/vercel-labs/skills): installation and client
  selection conventions used in the README.

This is an original implementation of the brief, not a vendored copy or an
official extension of any of these projects. No upstream skill installation is
required. Source links describe inspiration and packaging, not a dependency.

## Release procedure

1. Run package validation and tests; run the relevant evaluation cases with and
   without the skill. Record what was actually executed and remaining limits in
   `docs/validation.md`.
2. Check that the README matches the installable folder, both license copies
   match, the skill metadata identifies the intended version, and
   `CHANGELOG.md` describes the change.
3. Commit the reviewed files and wait for CI to pass on that commit.
4. Tag that commit as `v<version>` and publish the tag to the intended repository.
   Tag publication follows the user's or maintainer's existing authorization.
5. Verify that the public repository and the selected skill can be discovered.

Use a patch version for narrow corrections, a minor version for compatible
workflow additions, and a major version for changes that require users to adjust
their established workflow. Review compatibility rather than relying on the
version number alone. Git tags identify intended releases; users needing an
exact immutable source should record the commit SHA.
