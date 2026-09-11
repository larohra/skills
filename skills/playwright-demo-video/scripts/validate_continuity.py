"""Validate declared lifecycle identity continuity in a demo-video manifest."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from editorial_common import (
    EditorialInputError,
    emit_json,
    iter_manifest_scenes,
    load_json,
    require_mapping,
)


def _identifier(
    value: Any, field: str, errors: list[dict[str, str]]
) -> tuple[str, str] | None:
    if not isinstance(value, dict):
        errors.append({"path": field, "message": "must be an identity object"})
        return None
    name = value.get("name")
    identifier_value = value.get("value")
    if not isinstance(name, str) or not name.strip():
        errors.append({"path": f"{field}.name", "message": "must be a non-empty string"})
        return None
    if not isinstance(identifier_value, str) or not identifier_value.strip():
        errors.append({"path": f"{field}.value", "message": "must be a non-empty string"})
        return None
    return name, identifier_value


def _aliases(
    value: Any, field: str, errors: list[dict[str, str]]
) -> dict[str, str]:
    if not isinstance(value, list):
        errors.append({"path": field, "message": "must be an array of aliases"})
        return {}
    aliases: dict[str, str] = {}
    for index, raw_alias in enumerate(value):
        alias = _identifier(raw_alias, f"{field}[{index}]", errors)
        if alias is None:
            continue
        name, identifier_value = alias
        if name in aliases:
            errors.append(
                {
                    "path": f"{field}[{index}].name",
                    "message": f"duplicate alias name '{name}'",
                }
            )
        aliases[name] = identifier_value
    return aliases


def _record(
    value: Any, field: str, evidence_ids: set[str], errors: list[dict[str, str]]
) -> tuple[tuple[str, str] | None, dict[str, str]]:
    if not isinstance(value, dict):
        errors.append({"path": field, "message": "must be a before/after evidence record"})
        return None, {}
    evidence_shot_id = value.get("evidence_shot_id")
    if not isinstance(evidence_shot_id, str) or not evidence_shot_id:
        errors.append(
            {"path": f"{field}.evidence_shot_id", "message": "must name an evidence shot"}
        )
    elif evidence_shot_id not in evidence_ids:
        errors.append(
            {
                "path": f"{field}.evidence_shot_id",
                "message": f"does not match a declared evidence_shots id: {evidence_shot_id}",
            }
        )
    return (
        _identifier(value.get("identity"), f"{field}.identity", errors),
        _aliases(value.get("aliases"), f"{field}.aliases", errors),
    )


def validate_continuity(document: dict[str, Any]) -> dict[str, Any]:
    """Validate identity equality separately from expected aliases."""
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    checked = 0

    try:
        scenes = list(iter_manifest_scenes(document))
    except EditorialInputError as error:
        return {
            "tool": "validate_continuity",
            "valid": False,
            "lifecycle_claims_checked": 0,
            "errors": [{"path": "chapters", "message": str(error)}],
            "warnings": [],
        }

    for chapter_index, _chapter, scene_index, scene in scenes:
        if scene.get("lifecycle_claim") is not True:
            continue
        checked += 1
        scene_path = f"chapters[{chapter_index}].scenes[{scene_index}]"
        continuity = scene.get("continuity")
        if not isinstance(continuity, dict):
            errors.append(
                {
                    "path": f"{scene_path}.continuity",
                    "message": "lifecycle claims require a continuity object",
                }
            )
            continue
        evidence_ids = {
            shot.get("id")
            for shot in scene.get("evidence_shots", [])
            if isinstance(shot, dict) and isinstance(shot.get("id"), str)
        }
        expected_identity = _identifier(
            continuity.get("expected_identity"),
            f"{scene_path}.continuity.expected_identity",
            errors,
        )
        before_identity, before_aliases = _record(
            continuity.get("before"),
            f"{scene_path}.continuity.before",
            evidence_ids,
            errors,
        )
        after_identity, after_aliases = _record(
            continuity.get("after"),
            f"{scene_path}.continuity.after",
            evidence_ids,
            errors,
        )

        if before_identity is not None and after_identity is not None:
            if before_identity != after_identity:
                errors.append(
                    {
                        "path": f"{scene_path}.continuity",
                        "message": (
                            "identity continuity failed: before "
                            f"{before_identity[0]}={before_identity[1]!r}, after "
                            f"{after_identity[0]}={after_identity[1]!r}. "
                            "Aliases cannot substitute for the lifecycle identity."
                        ),
                    }
                )
        if expected_identity is not None:
            for label, actual in (("before", before_identity), ("after", after_identity)):
                if actual is not None and actual != expected_identity:
                    errors.append(
                        {
                            "path": f"{scene_path}.continuity.{label}.identity",
                            "message": (
                                f"expected identity {expected_identity[0]}="
                                f"{expected_identity[1]!r}, found {actual[0]}="
                                f"{actual[1]!r}"
                            ),
                        }
                    )

        expected_aliases = continuity.get("expected_aliases")
        if not isinstance(expected_aliases, list):
            errors.append(
                {
                    "path": f"{scene_path}.continuity.expected_aliases",
                    "message": "must be an array; use [] when no aliases matter",
                }
            )
            continue
        for alias_index, raw_expected in enumerate(expected_aliases):
            alias_path = f"{scene_path}.continuity.expected_aliases[{alias_index}]"
            if not isinstance(raw_expected, dict):
                errors.append({"path": alias_path, "message": "must be an object"})
                continue
            name = raw_expected.get("name")
            if not isinstance(name, str) or not name:
                errors.append(
                    {"path": f"{alias_path}.name", "message": "must be a non-empty string"}
                )
                continue
            same_value = raw_expected.get("value")
            expected_before = raw_expected.get("before", same_value)
            expected_after = raw_expected.get("after", same_value)
            if not isinstance(expected_before, str) or not isinstance(expected_after, str):
                errors.append(
                    {
                        "path": alias_path,
                        "message": "must supply value or both before and after strings",
                    }
                )
                continue
            for label, aliases, expected_value in (
                ("before", before_aliases, expected_before),
                ("after", after_aliases, expected_after),
            ):
                actual_value = aliases.get(name)
                if actual_value != expected_value:
                    errors.append(
                        {
                            "path": f"{scene_path}.continuity.{label}.aliases",
                            "message": (
                                f"alias {name!r} expected {expected_value!r} in {label} "
                                f"evidence, found {actual_value!r}. This is an alias "
                                "check, not proof of lifecycle identity."
                            ),
                        }
                    )
            if expected_before != expected_after:
                warnings.append(
                    {
                        "path": alias_path,
                        "message": (
                            f"alias {name!r} is expected to change from "
                            f"{expected_before!r} to {expected_after!r}; verify the "
                            "narration does not describe it as a stable identity."
                        ),
                    }
                )

    return {
        "tool": "validate_continuity",
        "valid": not errors,
        "lifecycle_claims_checked": checked,
        "errors": errors,
        "warnings": warnings,
        "strategy": (
            "Checks declared evidence records only. Reviewers must confirm that the "
            "identifiers are visibly readable in the linked before/after frames."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate before/after identity and alias expectations for lifecycle claims."
    )
    parser.add_argument("manifest", type=Path, help="Claim-evidence manifest JSON")
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()

    document = require_mapping(load_json(args.manifest), "manifest")
    report = validate_continuity(document)
    report["manifest"] = str(args.manifest)
    emit_json(report, args.output)
    if not report["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except EditorialInputError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2) from error
