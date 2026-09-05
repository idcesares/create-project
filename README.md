# Create Project

A portable agent skill that turns "I want to build a project" into a scoped,
validated outcome. It scales from a one-session tool to an uncertain,
multi-session build without imposing the same ceremony on both.

The agent discovers technical facts, asks for meaningful product decisions,
keeps useful project knowledge on disk, and verifies an end-to-end result before
expanding. It can also stop at research, a plan, or a prototype when that is the
requested outcome.

## Install

Using Node.js and the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add idcesares/create-project --skill create-project
```

The installer lets you choose an agent. To install for Codex across projects:

```sh
npx skills add idcesares/create-project --skill create-project --agent codex --global
```

The same CLI supports `claude-code` and `cursor`. Installation commands follow
the CLI's documented interface; model behavior and automatic selection can vary
by host. This project does not claim behavioral certification across clients.

For a reviewed version, check out a specific tag or commit and install locally:

```sh
git clone https://github.com/idcesares/create-project.git
cd create-project
git checkout v0.1.0
npx skills add . --skill create-project
```

No Node.js is required to use the skill itself. You can instead copy the entire
`skills/create-project/` folder into your agent's supported skill directory.
Keep the references and bundled license with it. For Codex, the user skill
directory in this setup is `~/.codex/skills/`. Consult your client's settings
if it uses a custom location. Reload skill discovery or start a new session
according to your client.

For CLI-managed installations, use `npx skills update create-project` to update
and `npx skills remove create-project` to uninstall; include `--global` when
removing a global installation. For manual copies, compare local customizations
before replacing the folder. Never overwrite a customized installation blindly.

## Use

In Codex:

```text
Use $create-project to build a local tool that turns CSV exports into a weekly report.
```

Or describe the project naturally:

```text
I want to create a project that tracks research papers and maps related concepts.
```

Automatic selection is enabled by default where supported; the host decides
whether a request matches. For other clients, use their skill invocation syntax.

You can state constraints and endpoints directly:

- "Plan this project only; don't implement yet."
- "Use the existing Python stack and keep everything local."
- "Resume from PROJECT.md and finish the next acceptance criterion."
- "Build a prototype to test whether the interaction works."

## What it does

| Project situation | Expected approach |
| --- | --- |
| Small, clear task | Brief criteria, implementation, relevant checks |
| Multi-session build | Durable intent, necessary decisions and specification, behavioral slices |
| Uncertain feasibility | Bounded research or experiment before committing to a design |
| Research project | Method, baseline, reproducible result, limitations |

Project records can include `PROJECT.md`, `CONTEXT.md`, `docs/SPEC.md`, and
decision records. Existing equivalents take precedence. Small tasks do not need
all these files. The skill does not select a universal stack, require another
skill, create a team of agents, or grant permission to publish or spend money.

## Repository layout

```text
skills/create-project/
  SKILL.md                 Entry point and routing
  agents/openai.yaml       Optional Codex interface metadata
  references/              Conditional workflow guidance
  LICENSE                  License travels with the installed folder
scripts/validate.py        Maintainer package checks
tests/test_package.py      Portability regression tests
evals/scenarios.md         Behavioral evaluation requests and rubric
docs/design.md            Design choices and source attribution
```

The installable folder is self-contained and follows the
[Agent Skills format](https://agentskills.io/specification). Repository-level
development tools are not runtime dependencies. To extend the workflow, add a
focused reference and link it from the entrypoint. Introduce another skill only
when it has a useful independent trigger and capability.

## Contribute and validate

Use Python 3.11 or later in a virtual environment:

```sh
python -m venv .venv
# Activate .venv using your shell, then:
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

CI runs package checks and regression tests on Windows and Linux. Checks cover
frontmatter, portable local links, a bundled license, and Codex metadata. They
do not prove an agent will follow the workflow. Use the
[behavioral scenarios](evals/scenarios.md) for changes to routing or decisions.
The [initial validation record](docs/validation.md) states what was tested.
Include the scenario, observed failure, proposed correction, and validation
evidence in contributions. Avoid adding universal rules for one unusual case.

Maintainers publish version tags after checks pass and review the behavioral
impact. The initial version is `0.1.0`; update the skill metadata and tag together.
For release preparation, follow the concise procedure in
[the design notes](docs/design.md).

## License and inspiration

[MIT](LICENSE). Inspired by the workflow concepts in
[Matt Pocock's skills](https://github.com/mattpocock/skills), with original
instructions tailored to portable, proportional project work. See
[design notes](docs/design.md) for what was retained and changed.
