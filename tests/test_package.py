"""Regression tests for broken portable packages, using isolated copies."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate import validate_evals, validate_skill


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "create-project"


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / "create-project"
        shutil.copytree(SOURCE, self.skill)

    def replace(self, old, new):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")

    def errors_containing(self, text):
        return [e for e in validate_skill(self.skill) if text in e]

    def test_package_survives_copy_without_repository(self):
        self.assertEqual(validate_skill(self.skill), [])

    def test_missing_reference_is_rejected(self):
        (self.skill / "references" / "discovery.md").unlink()
        self.assertTrue(self.errors_containing("Missing local file"))

    def test_outside_file_cannot_satisfy_reference(self):
        (self.skill.parent / "outside.md").write_text("outside", encoding="utf-8")
        self.replace("references/discovery.md", "../outside.md")
        self.assertTrue(self.errors_containing("escapes package"))

    def test_encoded_traversal_is_rejected(self):
        self.replace("references/discovery.md", "%2e%2e/outside.md")
        self.assertTrue(self.errors_containing("escapes package"))

    def test_windows_absolute_link_is_rejected(self):
        self.replace("references/discovery.md", "C:/private/discovery.md")
        self.assertTrue(self.errors_containing("Nonportable"))

    def test_wrong_folder_identity_is_rejected(self):
        self.replace("name: create-project", "name: another-project")
        self.assertTrue(self.errors_containing("matching its folder"))

    def test_empty_description_is_rejected(self):
        path = self.skill / "SKILL.md"
        path.write_text('---\nname: create-project\ndescription: ""\nlicense: MIT\n---\nBody\n', encoding="utf-8")
        self.assertTrue(self.errors_containing("Description"))

    def test_angle_brackets_in_description_are_rejected(self):
        self.replace("Use when someone", "Use when <someone>")
        self.assertTrue(self.errors_containing("angle brackets"))

    def test_unknown_frontmatter_key_is_rejected(self):
        self.replace("license: MIT", "license: MIT\ntriggers: always")
        self.assertTrue(self.errors_containing("Unexpected frontmatter keys: triggers"))

    def test_malformed_yaml_is_rejected(self):
        self.replace("name: create-project", "name: [")
        self.assertTrue(self.errors_containing("Invalid YAML"))

    def test_license_is_included_in_standalone_copy(self):
        (self.skill / "LICENSE").unlink()
        self.assertTrue(self.errors_containing("bundled LICENSE"))

    def test_wrong_codex_prompt_is_rejected(self):
        ui = self.skill / "agents" / "openai.yaml"
        ui.write_text(ui.read_text(encoding="utf-8").replace("$create-project", "$other"), encoding="utf-8")
        self.assertTrue(self.errors_containing("default_prompt"))

    def test_unlinked_reference_is_rejected(self):
        (self.skill / "references" / "orphan.md").write_text("# Orphan\n", encoding="utf-8")
        self.assertTrue(self.errors_containing("not linked from SKILL.md: references/orphan.md"))

    def test_long_reference_needs_contents(self):
        path = self.skill / "references" / "discovery.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nline\n" * 120, encoding="utf-8")
        self.assertTrue(self.errors_containing("contents section"))

    def test_oversized_body_is_rejected(self):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8") + "word " * 4000, encoding="utf-8")
        self.assertTrue(self.errors_containing("tokens"))

    def test_template_links_are_not_resolved(self):
        template = self.skill / "assets" / "PROJECT.md"
        self.assertIn("docs/adr/", template.read_text(encoding="utf-8"))
        self.assertEqual(validate_skill(self.skill), [])


class EvalDefinitionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.evals = Path(self.temp.name) / "evals"
        shutil.copytree(ROOT / "evals", self.evals)
        self.suite = json.loads((self.evals / "evals.json").read_text(encoding="utf-8"))

    def save(self):
        (self.evals / "evals.json").write_text(json.dumps(self.suite), encoding="utf-8")

    def test_repository_evals_are_valid(self):
        self.assertEqual(validate_evals(self.evals, "create-project"), [])

    def test_duplicate_id_is_rejected(self):
        self.suite["evals"][1]["id"] = self.suite["evals"][0]["id"]
        self.save()
        self.assertTrue(any("unique integer" in e for e in validate_evals(self.evals, "create-project")))

    def test_unknown_check_type_is_rejected(self):
        self.suite["evals"][0]["checks"].append({"type": "vibes"})
        self.save()
        self.assertTrue(any("unknown check type" in e for e in validate_evals(self.evals, "create-project")))

    def test_unchanged_path_must_exist_in_fixture(self):
        self.suite["evals"][0]["checks"][0]["paths"].append("missing.csv")
        self.save()
        self.assertTrue(any("missing from fixture" in e for e in validate_evals(self.evals, "create-project")))

    def test_fixture_must_stay_inside_fixtures(self):
        self.suite["evals"][0]["fixture"] = "../scripts"
        self.save()
        self.assertTrue(any("under evals/fixtures" in e for e in validate_evals(self.evals, "create-project")))

    def test_one_sided_trigger_queries_are_rejected(self):
        path = self.evals / "trigger-queries.json"
        path.write_text(json.dumps([{"query": "build an app", "should_trigger": True}]), encoding="utf-8")
        self.assertTrue(any("both" in e for e in validate_evals(self.evals, "create-project")))


if __name__ == "__main__":
    unittest.main()
