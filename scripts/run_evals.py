"""Run the behavioral evaluation cases in evals/evals.json against an agent.

Each case gets a fresh temporary workspace outside this repository containing
only its fixture and, unless --baseline is set, an installed copy of the skill.
The agent command runs once per turn inside that workspace. Afterwards the
script applies the case's deterministic checks, copies the final workspace
into the results folder, and writes a grading sheet for the rubric
expectations, which need a human or grader-agent judgment.

Without --agent or --agent-cmd, the script only prepares the workspaces and
prompts, so it costs nothing and runs in CI. Running an agent may cost money
and executes the agent's actions on this machine: prefer a container or VM.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
SKILL = ROOT / "skills" / "create-project"
IGNORED_PARTS = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache"}
PRESETS = {
    # Runs with permissions bypassed so the agent can execute its own checks.
    "claude": (
        ["claude", "-p", "{prompt}", "--output-format", "stream-json", "--verbose",
         "--dangerously-skip-permissions"],
        ["claude", "-p", "{prompt}", "--continue", "--output-format", "stream-json", "--verbose",
         "--dangerously-skip-permissions"],
    ),
}
INVOKE = "Use the create-project skill for this request.\n\n"


def load_cases(path: Path = EVALS / "evals.json") -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["evals"]


def turns_of(case: dict) -> list[str]:
    return case.get("turns") or [case["prompt"]]


def glob_regex(pattern: str) -> re.Pattern[str]:
    """Translate a workspace glob with ** support into a regex over POSIX paths."""
    out, i = "", 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif pattern.startswith("**", i):
            out, i = out + ".*", i + 2
        elif pattern[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif pattern[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(pattern[i]), i + 1
    return re.compile(out + r"\Z")


def snapshot(workspace: Path, skip: Path | None = None) -> dict[str, str]:
    files = {}
    for path in workspace.rglob("*"):
        if not path.is_file() or IGNORED_PARTS & set(path.relative_to(workspace).parts):
            continue
        if skip and path.is_relative_to(skip):
            continue
        files[path.relative_to(workspace).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def run_checks(case: dict, workspace: Path, before: dict, after: dict) -> list[dict]:
    results = []
    new = sorted(set(after) - set(before))
    for check in case.get("checks", []):
        kind, passed, detail = check["type"], True, ""
        if kind == "unchanged":
            changed = [p for p in check["paths"] if before.get(p) is None or after.get(p) != before[p]]
            passed, detail = not changed, f"changed or missing: {changed}" if changed else "identical"
        elif kind == "absent":
            hits = [p for p in new if any(glob_regex(g).match(p) for g in check["globs"])]
            passed, detail = not hits, f"created: {hits}" if hits else "none created"
        elif kind == "present":
            hits = [p for p in after if any(glob_regex(g).match(p) for g in check["globs"])]
            passed, detail = bool(hits), f"found: {hits}" if hits else "none found"
        elif kind == "no_new_files":
            passed, detail = not new, f"created: {new}" if new else "none created"
        elif kind == "contains":
            target = workspace / check["path"]
            text = target.read_text(encoding="utf-8", errors="replace") if target.is_file() else ""
            passed = bool(re.search(check["pattern"], text))
            detail = "matched" if passed else ("no match" if target.is_file() else "file missing")
        elif kind == "command":
            argv = [sys.executable if a == "{python}" else a for a in check["argv"]]
            try:
                proc = subprocess.run(argv, cwd=workspace, capture_output=True, text=True, timeout=300)
                passed, detail = proc.returncode == 0, f"exit {proc.returncode}: {(proc.stdout + proc.stderr)[-400:]}"
            except (OSError, subprocess.TimeoutExpired) as exc:
                passed, detail = False, f"could not run: {exc}"
        else:
            passed, detail = False, f"unknown check type {kind}"
        results.append({"check": check, "passed": passed, "detail": detail})
    return results


def prepare(case: dict, baseline: bool, skills_dir: str) -> tuple[Path, Path | None]:
    workspace = Path(tempfile.mkdtemp(prefix=f"create-project-eval-{case['id']}-"))
    if case.get("fixture"):
        shutil.copytree(EVALS / case["fixture"], workspace, dirs_exist_ok=True)
    installed = None
    if not baseline:
        installed = workspace / skills_dir / SKILL.name
        shutil.copytree(SKILL, installed)
    return workspace, installed


def prompts_for(case: dict, baseline: bool) -> list[str]:
    turns = turns_of(case)
    if not baseline and case.get("explicit_invocation", True):
        turns = [INVOKE + turns[0], *turns[1:]]
    return turns


def grading_sheet(case: dict, checks: list[dict]) -> str:
    lines = [f"# {case['id']}: {case['name']}", "", f"Expected: {case['expected_output']}", ""]
    if case.get("host_conditions"):
        lines += [f"Host conditions: {case['host_conditions']}", ""]
    lines += ["## Deterministic checks", ""]
    lines += [f"- {'PASS' if r['passed'] else 'FAIL'} `{r['check']['type']}`: {r['detail']}" for r in checks] or ["- none"]
    lines += ["", "## Rubric", "", "Mark each pass, fail, or not observed, with evidence from the transcript or workspace.", ""]
    lines += [f"- [ ] {e}\n  - Result:\n  - Evidence:" for e in case["expectations"]]
    return "\n".join(lines) + "\n"


def run_case(case: dict, out: Path, first_cmd: list[str] | None, next_cmd: list[str] | None,
             baseline: bool = False, skills_dir: str = ".claude/skills", timeout: int = 1800) -> dict:
    case_dir = out / f"{case['id']:02d}-{case['name']}"
    case_dir.mkdir(parents=True)
    workspace, installed = prepare(case, baseline, skills_dir)
    prompts = prompts_for(case, baseline)
    (case_dir / "prompt.txt").write_text("\n\n--- next turn ---\n\n".join(prompts), encoding="utf-8")
    before = snapshot(workspace, installed)
    result = {"id": case["id"], "name": case["name"], "baseline": baseline, "turns": []}
    try:
        if first_cmd is None:
            result["status"] = "prepared"
            return result
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        for index, prompt in enumerate(prompts):
            template = first_cmd if index == 0 else (next_cmd or first_cmd)
            argv = [prompt if a == "{prompt}" else a for a in template]
            started = time.monotonic()
            try:
                proc = subprocess.run(argv, cwd=workspace, env=env, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace", timeout=timeout)
                code, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
            except subprocess.TimeoutExpired as exc:
                code, stdout, stderr = "timeout", str(exc.stdout or ""), str(exc.stderr or "")
            (case_dir / f"transcript-{index + 1}.txt").write_text(stdout, encoding="utf-8")
            (case_dir / f"stderr-{index + 1}.txt").write_text(stderr, encoding="utf-8")
            result["turns"].append({"exit": code, "seconds": round(time.monotonic() - started, 1)})
        checks = run_checks(case, workspace, before, snapshot(workspace, installed))
        result["checks"] = checks
        result["status"] = "ran"
        (case_dir / "grading.md").write_text(grading_sheet(case, checks), encoding="utf-8")
        return result
    finally:
        def ignore(directory: str, names: list[str]) -> set[str]:
            skipped = {n for n in names if n in IGNORED_PARTS}
            return skipped | {n for n in names if installed and Path(directory, n) == installed}

        shutil.copytree(workspace, case_dir / "workspace", ignore=ignore)
        shutil.rmtree(workspace, ignore_errors=True)
        (case_dir / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--case", action="append", default=[], help="case id or name; repeatable")
    agent = parser.add_mutually_exclusive_group()
    agent.add_argument("--agent", choices=sorted(PRESETS), help="run a preset agent command")
    agent.add_argument("--agent-cmd", help="JSON argv list with a literal \"{prompt}\" element")
    parser.add_argument("--continue-cmd", help="JSON argv list for later turns (default: --agent-cmd)")
    parser.add_argument("--baseline", action="store_true", help="run without installing the skill")
    parser.add_argument("--skills-dir", default=".claude/skills", help="install path inside the workspace")
    parser.add_argument("--timeout", type=int, default=1800, help="seconds per turn")
    parser.add_argument("--out", type=Path, default=ROOT / ".eval-runs")
    args = parser.parse_args()

    cases = load_cases()
    if args.case:
        cases = [c for c in cases if str(c["id"]) in args.case or c["name"] in args.case]
        if not cases:
            parser.error(f"no case matches {args.case}")
    first_cmd = next_cmd = None
    if args.agent:
        first_cmd, next_cmd = PRESETS[args.agent]
    elif args.agent_cmd:
        first_cmd = json.loads(args.agent_cmd)
        next_cmd = json.loads(args.continue_cmd) if args.continue_cmd else first_cmd
    for template in filter(None, (first_cmd, next_cmd)):
        if "{prompt}" not in template:
            parser.error("agent command must contain a literal \"{prompt}\" element")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = args.out / f"{stamp}-{'baseline' if args.baseline else 'skill'}"
    results = [run_case(c, out, first_cmd, next_cmd, args.baseline, args.skills_dir, args.timeout) for c in cases]

    lines = ["| Case | Status | Deterministic checks |", "| --- | --- | --- |"]
    for r in results:
        checks = r.get("checks", [])
        summary = f"{sum(c['passed'] for c in checks)}/{len(checks)} passed" if r["status"] == "ran" else "not run"
        lines.append(f"| {r['id']}: {r['name']} | {r['status']} | {summary} |")
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nResults: {out}")
    if first_cmd is None:
        print("Prepared only. Add --agent claude or --agent-cmd to run an agent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
