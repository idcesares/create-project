"""Regression tests for broken portable packages, using isolated copies."""

import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate import validate_skill


SOURCE = Path(__file__).resolve().parents[1] / "skills" / "create-project"


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / "create-project"
        shutil.copytree(SOURCE, self.skill)

    def replace(self, old, new):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")

    def test_package_survives_copy_without_repository(self):
        self.assertEqual(validate_skill(self.skill), [])

    def test_missing_reference_is_rejected(self):
        (self.skill / "references" / "discovery.md").unlink()
        self.assertTrue(any("Missing local file" in e for e in validate_skill(self.skill)))

    def test_outside_file_cannot_satisfy_reference(self):
        (self.skill.parent / "outside.md").write_text("outside", encoding="utf-8")
        self.replace("references/discovery.md", "../outside.md")
        self.assertTrue(any("escapes package" in e for e in validate_skill(self.skill)))

    def test_encoded_traversal_is_rejected(self):
        self.replace("references/discovery.md", "%2e%2e/outside.md")
        self.assertTrue(any("escapes package" in e for e in validate_skill(self.skill)))

    def test_windows_absolute_link_is_rejected(self):
        self.replace("references/discovery.md", "C:/private/discovery.md")
        self.assertTrue(any("Nonportable" in e for e in validate_skill(self.skill)))

    def test_wrong_folder_identity_is_rejected(self):
        self.replace("name: create-project", "name: another-project")
        self.assertTrue(any("matching its folder" in e for e in validate_skill(self.skill)))

    def test_empty_description_is_rejected(self):
        path = self.skill / "SKILL.md"
        path.write_text('---\nname: create-project\ndescription: ""\nlicense: MIT\n---\nBody\n', encoding="utf-8")
        self.assertTrue(any("Description" in e for e in validate_skill(self.skill)))

    def test_malformed_yaml_is_rejected(self):
        self.replace("name: create-project", "name: [")
        self.assertTrue(any("Invalid YAML" in e for e in validate_skill(self.skill)))

    def test_license_is_included_in_standalone_copy(self):
        (self.skill / "LICENSE").unlink()
        self.assertTrue(any("bundled LICENSE" in e for e in validate_skill(self.skill)))

    def test_wrong_codex_prompt_is_rejected(self):
        ui = self.skill / "agents" / "openai.yaml"
        ui.write_text(ui.read_text(encoding="utf-8").replace("$create-project", "$other"), encoding="utf-8")
        self.assertTrue(any("default_prompt" in e for e in validate_skill(self.skill)))


if __name__ == "__main__":
    unittest.main()
