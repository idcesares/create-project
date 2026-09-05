# Design notes

## Intent

Make one project-level skill easy to install, understand, modify, and share.
The initial brief called for automatic routing from an idea through a useful
result, minimal unnecessary questions, durable context, and evidence of
completion. It also suggested a large collection of cooperating skills.

This version implements one skill with conditional references. Splitting every
phase into its own skill would add installation dependencies and overlapping
triggers before there is evidence that those capabilities need independent
entry points. The installable folder contains all runtime guidance.

## Decisions

- **Adaptive depth.** Size, uncertainty, and consequences select the process.
  Research, decision maps, detailed specs, and work records are conditional.
- **Durable intent.** Use `PROJECT.md` for multi-session work, or the repository's
  existing equivalent. Separate records by purpose when they contain enough
  distinct information to justify maintenance.
- **Evidence before expansion.** Run a small end-to-end behavior or experiment
  early. Use observable acceptance criteria and relevant failure checks.
- **Proportional validation.** Test-first work is useful for behavior contracts;
  it is not imposed on every document, visual edit, or exploratory activity.
  Report actual evidence instead of invented completion scores.
- **Optional integrations.** No required MCP, issue tracker, framework, external
  skills, delegation, hooks, or setup wizard. The host retains its permissions.
- **Portable distribution.** Standard Markdown and YAML; Codex UI metadata is
  isolated in `agents/openai.yaml`. A copy of the MIT license travels with the
  installed skill. Repository tooling is kept outside that folder.
- **Incremental growth.** Add references for demonstrated needs. Split a new
  skill only when independent invocation is useful; do not add a plugin manifest,
  package manager, installer script, or runtime just to distribute instructions.

## Sources and attribution

Reviewed on 2026-09-05:

- [Agent Skills specification](https://agentskills.io/specification): portable
  directory, metadata, and progressive disclosure conventions.
- [Matt Pocock's ask-matt](https://github.com/mattpocock/skills/blob/main/skills/engineering/ask-matt/SKILL.md):
  inspiration for routing an idea through discovery, optional prototypes,
  specifications, behavioral work items, and review.
- [Matt Pocock's wayfinder guide](https://github.com/mattpocock/skills/blob/main/docs/engineering/wayfinder.md):
  inspiration for resolving interdependent uncertainty in large fuzzy efforts.
- [Skills CLI](https://github.com/vercel-labs/skills): installation and client
  selection conventions used in the README.

This is an original implementation of the brief, not a vendored copy or an
official extension of Matt Pocock's package. No upstream skill installation is
required. Source links describe inspiration and packaging, not a dependency.

## Release procedure

1. Run package validation and tests; review changed behavior using the relevant
   evaluation scenarios. Record what was actually executed and remaining limits.
2. Check that the README matches the installable folder, both license copies
   match, and the skill metadata identifies the intended version.
3. Commit the reviewed files and wait for CI to pass on that commit.
4. Tag that commit as `v<version>` and publish the tag to the intended repository.
   Tag publication follows the user's or maintainer's existing authorization.
5. Verify that the public repository and the selected skill can be discovered.

Use a patch version for narrow corrections, a minor version for compatible
workflow additions, and a major version for changes that require users to adjust
their established workflow. Review compatibility rather than relying on the
version number alone. Git tags identify intended releases; users needing an
exact immutable source should record the commit SHA.
