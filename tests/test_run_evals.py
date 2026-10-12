"""Tests for the eval runner using a scripted stand-in for an agent."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.run_evals import glob_regex, load_cases, run_case

FAKE_AGENT = """
import pathlib, sys
prompt = sys.argv[1]
pathlib.Path("prompts.log").open("a", encoding="utf-8").write(prompt + "\\n---\\n")
pathlib.Path("report.txt").write_text("duplicates: files/a.txt files/nested/b.txt", encoding="utf-8")
pathlib.Path("files/c.txt").write_text("tampered", encoding="utf-8")
skill = pathlib.Path(".claude/skills/create-project/SKILL.md")
pathlib.Path("saw-skill.txt").write_text(str(skill.is_file()), encoding="utf-8")
"""


def case(**overrides):
    base = {
        "id": 99,
        "name": "fake",
        "turns": ["first request", "second request"],
        "fixture": "fixtures/duplicate-finder",
        "expected_output": "anything",
        "expectations": ["Reports duplicates"],
        "checks": [
            {"type": "unchanged", "paths": ["files/a.txt"]},
            {"type": "unchanged", "paths": ["files/c.txt"]},
            {"type": "present", "globs": ["report.txt"]},
            {"type": "absent", "globs": ["**/*.log"]},
            {"type": "contains", "path": "report.txt", "pattern": "nested/b\\.txt"},
            {"type": "command", "argv": ["{python}", "-c", "import pathlib; assert pathlib.Path('report.txt').exists()"]},
            {"type": "no_new_files"},
        ],
    }
    base.update(overrides)
    return base


class GlobTests(unittest.TestCase):
    def test_double_star_matches_any_depth_including_root(self):
        self.assertTrue(glob_regex("**/*.py").match("app.py"))
        self.assertTrue(glob_regex("**/*.py").match("src/pkg/app.py"))
        self.assertTrue(glob_regex("docs/**").match("docs/adr/0001.md"))

    def test_single_star_stays_within_a_folder(self):
        self.assertFalse(glob_regex("*.md").match("docs/SPEC.md"))
        self.assertTrue(glob_regex("PROJECT.md").match("PROJECT.md"))


class RunCaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name)
        self.cmd = [sys.executable, "-c", FAKE_AGENT, "{prompt}"]

    def test_checks_report_agent_effects(self):
        result = run_case(case(), self.out, self.cmd, self.cmd)
        outcome = {(c["check"]["type"], json.dumps(c["check"].get("paths"))): c["passed"] for c in result["checks"]}
        self.assertTrue(outcome[("unchanged", '["files/a.txt"]')])
        self.assertFalse(outcome[("unchanged", '["files/c.txt"]')])
        passed = {c["check"]["type"]: c["passed"] for c in result["checks"] if c["check"]["type"] != "unchanged"}
        self.assertEqual(passed, {"present": True, "absent": False, "contains": True, "command": True, "no_new_files": False})

    def test_turns_run_in_order_with_explicit_invocation_first(self):
        run_case(case(), self.out, self.cmd, self.cmd)
        workspace = self.out / "99-fake" / "workspace"
        prompts = (workspace / "prompts.log").read_text(encoding="utf-8").split("\n---\n")
        self.assertTrue(prompts[0].startswith("Use the create-project skill"))
        self.assertTrue(prompts[0].endswith("first request"))
        self.assertEqual(prompts[1], "second request")
        self.assertTrue((self.out / "99-fake" / "grading.md").is_file())

    def test_skill_is_installed_for_agent_but_not_kept_in_results(self):
        run_case(case(), self.out, self.cmd, self.cmd)
        workspace = self.out / "99-fake" / "workspace"
        self.assertEqual((workspace / "saw-skill.txt").read_text(encoding="utf-8"), "True")
        self.assertFalse((workspace / ".claude" / "skills" / "create-project").exists())

    def test_baseline_has_no_skill_and_no_invocation(self):
        run_case(case(), self.out, self.cmd, self.cmd, baseline=True)
        workspace = self.out / "99-fake" / "workspace"
        self.assertEqual((workspace / "saw-skill.txt").read_text(encoding="utf-8"), "False")
        self.assertTrue((workspace / "prompts.log").read_text(encoding="utf-8").startswith("first request"))

    def test_prepare_only_runs_nothing(self):
        result = run_case(case(), self.out, None, None)
        self.assertEqual(result["status"], "prepared")
        self.assertFalse((self.out / "99-fake" / "workspace" / "report.txt").exists())

    def test_repository_cases_prepare(self):
        for item in load_cases():
            self.assertEqual(run_case(item, self.out, None, None)["status"], "prepared")


if __name__ == "__main__":
    unittest.main()
