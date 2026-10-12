# Evaluations

Two suites, both defined as data so they can be validated and rerun.

| File | Measures | How it runs |
| --- | --- | --- |
| [evals.json](evals.json) | Behavior after the skill is invoked: endpoints, questions, evidence, authorization, memory | `scripts/run_evals.py` against a real agent |
| [trigger-queries.json](trigger-queries.json) | Whether the description selects the skill, including near-miss requests that should not | Any trigger harness that reads `query` and `should_trigger` |

`evals.json` follows the skill-creator layout (`id`, `prompt`,
`expected_output`, `expectations`) with these additions: `name`, `fixture` (a
folder under `fixtures/`), `turns` for multi-turn cases, `checks` for
deterministic assertions, `host_conditions` for environment requirements, and
`explicit_invocation: false` for cases that test natural selection.
`python scripts/validate.py` rejects malformed cases before any run.

## Run

```sh
# Prepare workspaces and prompts only; free, and what CI runs.
python scripts/run_evals.py

# Run every case with Claude Code, then the same cases without the skill.
python scripts/run_evals.py --agent claude
python scripts/run_evals.py --agent claude --baseline

# One case, any agent CLI: a JSON argv list with a literal "{prompt}" element.
python scripts/run_evals.py --case resume-existing-work \
  --agent-cmd '["codex", "exec", "--full-auto", "{prompt}"]' --skills-dir .agents/skills
```

Set `--skills-dir` to the folder where that agent discovers project skills,
and `--continue-cmd` when later turns need a different command (for example,
one that resumes the previous session).

Each case runs in a fresh temporary folder outside this repository containing
only its fixture and the installed skill. The `claude` preset bypasses
permission prompts so the agent can run its own checks: run it in a container
or VM, never with production credentials. Agent runs cost money. Skills
installed in your user profile also load during runs and contaminate baselines,
so remove them first.

Results go to `.eval-runs/<timestamp>-skill|baseline/` (ignored by git):
`prompt.txt`, a transcript per turn, `result.json`, the final `workspace/`, and
`grading.md`.

## Grade

Deterministic checks are already scored in `grading.md`. Score each rubric
expectation as pass, fail, or not observed, citing the transcript or workspace;
a human or a grader agent given only `grading.md`, the transcript, and the
workspace can do this. Judge outcomes and decisions, not headings or wording.

Critical failures: violating the requested endpoint, an unauthorized external
mutation, lost user data, invented evidence, or claiming an unmet criterion is
complete. Compare against the baseline run: an expectation that passes equally
without the skill does not show the skill's value. Tie each correction to an
observed failure rather than adding universal rules for one unusual case.
