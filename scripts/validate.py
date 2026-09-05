"""Check this repository's portable skill packages, not agent behavior.

Run from any directory with Python 3.11+ and requirements-dev.txt installed.
The link check supports the simple inline Markdown links used in this repo;
it checks local file targets, not external URLs or heading anchors.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


def validate_skill(skill: Path) -> list[str]:
    skill = skill.resolve()
    errors: list[str] = []
    entrypoint = skill / "SKILL.md"
    if not entrypoint.is_file():
        return ["Missing SKILL.md"]
    content = entrypoint.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    if not match:
        return ["Missing or malformed YAML frontmatter"]
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return [f"Invalid YAML: {exc}"]
    if not isinstance(metadata, dict):
        return ["Frontmatter must be a mapping"]
    name = metadata.get("name")
    if (
        not isinstance(name, str)
        or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
        or len(name) > 64
        or name != skill.name
    ):
        errors.append("Name must be lowercase hyphenated text matching its folder (1-64 characters)")
    description = metadata.get("description")
    if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
        errors.append("Description must contain 1-1024 characters")
    extra = metadata.get("metadata", {})
    if not isinstance(extra, dict) or any(
        not isinstance(k, str) or not isinstance(v, str) for k, v in extra.items()
    ):
        errors.append("Metadata keys and values must be strings")
    if not content[match.end():].strip():
        errors.append("Skill body is empty")
    if len(content.splitlines()) >= 500:
        errors.append("Repository convention: keep SKILL.md below 500 lines")
    if metadata.get("license") != "MIT" or not (skill / "LICENSE").is_file():
        errors.append("Repository convention: include MIT metadata and a bundled LICENSE")

    for document in sorted(skill.rglob("*.md")):
        if not document.resolve().is_relative_to(skill):
            errors.append(f"Document escapes package: {document.name}")
            continue
        text = document.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]\n]+\]\(([^\s)]+)\)", text):
            if target.startswith("#"):
                continue
            parsed = urlsplit(target)
            if parsed.scheme in {"https", "http", "mailto"}:
                continue
            if parsed.scheme or parsed.netloc or "\\" in target:
                errors.append(f"Nonportable link in {document.name}: {target}")
                continue
            path = (document.parent / unquote(parsed.path)).resolve()
            if not path.is_relative_to(skill):
                errors.append(f"Link escapes package in {document.name}: {target}")
            elif not path.is_file():
                errors.append(f"Missing local file in {document.name}: {target}")

    ui_file = skill / "agents" / "openai.yaml"
    if ui_file.is_file():
        try:
            ui = yaml.safe_load(ui_file.read_text(encoding="utf-8"))
            interface = ui["interface"]
            short = interface["short_description"]
            prompt = interface["default_prompt"]
            if not isinstance(short, str) or not 25 <= len(short) <= 64:
                errors.append("Codex short_description must contain 25-64 characters")
            if not isinstance(prompt, str) or f"${name}" not in prompt:
                errors.append("Codex default_prompt must invoke the skill by name")
        except (yaml.YAMLError, KeyError, TypeError):
            errors.append("Malformed Codex UI metadata")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="*", type=Path)
    args = parser.parse_args()
    skills = args.skills or sorted(
        path.parent for path in (Path(__file__).resolve().parents[1] / "skills").glob("*/SKILL.md")
    )
    if not skills:
        print("FAIL: no skills found")
        return 1
    failed = False
    for skill in skills:
        errors = validate_skill(skill)
        failed |= bool(errors)
        print(f"{'FAIL' if errors else 'PASS'}: {skill.name}")
        for error in errors:
            print(f"  {error}")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
