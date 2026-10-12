"""Check this repository's portable skill packages and eval definitions.

This checks structure, not agent behavior. Run from any directory with Python
3.11+ and requirements-dev.txt installed. The link check supports the simple
inline Markdown links used in this repo; it checks local file targets, not
external URLs or heading anchors. Files under assets/ are templates whose links
point into the user's future project, so they are not link-checked.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
CHECK_TYPES = {"unchanged", "absent", "present", "no_new_files", "contains", "command"}
BODY_TOKEN_BUDGET = 5000  # rough estimate: words * 4 / 3
LINK = re.compile(r"\[[^\]\n]+\]\(([^\s)]+)\)")


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
    unexpected = sorted(set(metadata) - ALLOWED_KEYS)
    if unexpected:
        errors.append(f"Unexpected frontmatter keys: {', '.join(unexpected)}")
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
    elif "<" in description or ">" in description:
        errors.append("Description must not contain angle brackets")
    compatibility = metadata.get("compatibility")
    if compatibility is not None and (not isinstance(compatibility, str) or not 1 <= len(compatibility) <= 500):
        errors.append("Compatibility must contain 1-500 characters")
    extra = metadata.get("metadata", {})
    if not isinstance(extra, dict) or any(
        not isinstance(k, str) or not isinstance(v, str) for k, v in extra.items()
    ):
        errors.append("Metadata keys and values must be strings")
    body = content[match.end():]
    if not body.strip():
        errors.append("Skill body is empty")
    if len(body.split()) * 4 // 3 > BODY_TOKEN_BUDGET:
        errors.append(f"Skill body exceeds about {BODY_TOKEN_BUDGET} tokens; move detail into references")
    if len(content.splitlines()) >= 500:
        errors.append("Repository convention: keep SKILL.md below 500 lines")
    if metadata.get("license") != "MIT" or not (skill / "LICENSE").is_file():
        errors.append("Repository convention: include MIT metadata and a bundled LICENSE")

    linked_from_entrypoint = set()
    for document in sorted(skill.rglob("*.md")):
        if not document.resolve().is_relative_to(skill):
            errors.append(f"Document escapes package: {document.name}")
            continue
        if document.resolve().is_relative_to(skill / "assets"):
            continue
        text = document.read_text(encoding="utf-8")
        if len(text.splitlines()) > 100 and document != entrypoint and not re.search(r"(?im)^#+ contents", text):
            errors.append(f"Reference over 100 lines needs a contents section: {document.name}")
        for target in LINK.findall(text):
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
            elif document == entrypoint:
                linked_from_entrypoint.add(path)

    for bundled in sorted([*skill.glob("references/**/*"), *skill.glob("assets/**/*")]):
        if bundled.is_file() and bundled.resolve() not in linked_from_entrypoint:
            errors.append(f"Bundled file is not linked from SKILL.md: {bundled.relative_to(skill).as_posix()}")

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


def validate_evals(evals_dir: Path, skill_name: str) -> list[str]:
    """Check eval definitions so a broken case fails here, not mid-run."""
    errors: list[str] = []
    try:
        suite = json.loads((evals_dir / "evals.json").read_text(encoding="utf-8"))
        queries = json.loads((evals_dir / "trigger-queries.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Unreadable eval file: {exc}"]
    if suite.get("skill_name") != skill_name:
        errors.append("evals.json skill_name must match the skill")
    seen_ids, seen_names = set(), set()
    for case in suite.get("evals", []):
        label = f"eval {case.get('id')}"
        if not isinstance(case.get("id"), int) or case["id"] in seen_ids:
            errors.append(f"{label}: id must be a unique integer")
        if not isinstance(case.get("name"), str) or case["name"] in seen_names:
            errors.append(f"{label}: name must be a unique string")
        seen_ids.add(case.get("id"))
        seen_names.add(case.get("name"))
        turns = case.get("turns") or [case.get("prompt")]
        if not all(isinstance(t, str) and t.strip() for t in turns):
            errors.append(f"{label}: needs a prompt or non-empty turns")
        if not case.get("expectations") or not isinstance(case.get("expected_output"), str):
            errors.append(f"{label}: needs expected_output and expectations")
        fixture = case.get("fixture")
        if fixture is not None:
            path = (evals_dir / fixture).resolve()
            if not path.is_relative_to(evals_dir.resolve() / "fixtures") or not path.is_dir():
                errors.append(f"{label}: fixture must be a folder under evals/fixtures")
        for check in case.get("checks", []):
            if check.get("type") not in CHECK_TYPES:
                errors.append(f"{label}: unknown check type {check.get('type')!r}")
            elif check["type"] == "unchanged" and fixture:
                missing = [p for p in check["paths"] if not (evals_dir / fixture / p).is_file()]
                if missing:
                    errors.append(f"{label}: unchanged paths missing from fixture: {missing}")
    if not suite.get("evals"):
        errors.append("evals.json has no cases")
    triggers = [q.get("should_trigger") for q in queries if isinstance(q, dict) and isinstance(q.get("query"), str)]
    if len(triggers) != len(queries) or not all(isinstance(t, bool) for t in triggers):
        errors.append("trigger-queries.json entries need a query string and a should_trigger boolean")
    elif not (any(triggers) and not all(triggers)):
        errors.append("trigger-queries.json needs both should-trigger and should-not-trigger queries")
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
    evals_dir = Path(__file__).resolve().parents[1] / "evals"
    if not args.skills and evals_dir.is_dir():
        errors = validate_evals(evals_dir, "create-project")
        failed |= bool(errors)
        print(f"{'FAIL' if errors else 'PASS'}: evals")
        for error in errors:
            print(f"  {error}")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
