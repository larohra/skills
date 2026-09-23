"""Validate public Copilot skill metadata and obvious privacy tripwires."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

PRIVATE_PLAYBOOK_TERM = "agent" + "-" + "playbook"

FORBIDDEN_PATTERNS = {
    "private playbook repository": re.compile(PRIVATE_PLAYBOOK_TERM, re.IGNORECASE),
    "Copilot session state path": re.compile(r"\.copilot[\\/](session-state|repos)", re.IGNORECASE),
    "Windows user profile path": re.compile(r"C:\\Users\\[^\\\s]+", re.IGNORECASE),
    "environment assignment": re.compile(r"(?m)^\s*[A-Z][A-Z0-9_]*(TOKEN|SECRET|PASSWORD|KEY)\s*="),
    "GitHub token literal": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
}


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, [f"{path}: missing opening frontmatter delimiter"]
    try:
        _, raw_frontmatter, _ = text.split("---\n", 2)
    except ValueError:
        return {}, [f"{path}: missing closing frontmatter delimiter"]

    metadata: dict[str, str] = {}
    for line in raw_frontmatter.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"{path}: invalid frontmatter line {line!r}")
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata, errors


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    metadata, metadata_errors = parse_frontmatter(path)
    errors.extend(metadata_errors)

    expected_name = path.parent.name
    actual_name = metadata.get("name", "")
    description = metadata.get("description", "")
    if actual_name != expected_name:
        errors.append(f"{path}: name must be {expected_name!r}, got {actual_name!r}")
    if len(description) < 20:
        errors.append(f"{path}: description is missing or too short")

    text = path.read_text(encoding="utf-8")
    if f"# {expected_name.replace('-', ' ').title()}" not in text:
        errors.append(f"{path}: missing title heading for {expected_name!r}")

    return errors


def validate_privacy(root: Path) -> list[str]:
    errors: list[str] = []
    checked_extensions = {".md", ".py", ".ps1", ".json", ".yml", ".yaml", ".txt"}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in checked_extensions:
            continue
        if path == Path(__file__).resolve():
            continue
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path.relative_to(root)}: possible private content ({label})")
    return errors


def main() -> int:
    errors: list[str] = []
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        errors.append("No skills/*/SKILL.md files found")
    for skill_file in skill_files:
        errors.extend(validate_skill(skill_file))
    errors.extend(validate_privacy(ROOT))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Validated {len(skill_files)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
