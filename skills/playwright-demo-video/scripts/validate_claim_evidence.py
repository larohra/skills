"""Validate the deterministic parts of a claim-evidence editorial manifest.

This script confirms that declared evidence files and marker attestations are
present. It deliberately does not claim to OCR or semantically understand a
frame; a reviewer must still inspect the generated claim frames.
"""

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
    normalize_marker,
    require_list,
    require_mapping,
    require_number,
    require_string,
    resolve_from,
)

COMPLETION_EVIDENCE_ROLES = {"outcome", "response", "status"}


def add_issue(
    issues: list[dict[str, str]], path: str, message: str, severity: str = "error"
) -> None:
    issues.append({"path": path, "message": message, "severity": severity})


def marker_values(value: Any, field: str, issues: list[dict[str, str]]) -> set[str]:
    if not isinstance(value, list) or not value:
        add_issue(issues, field, "must be a non-empty array of visible text/markers")
        return set()
    values: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            add_issue(issues, f"{field}[{index}]", "must be a non-empty string")
            continue
        values.add(normalize_marker(item))
    return values


def has_required_string(
    value: Any, field: str, issues: list[dict[str, str]]
) -> str | None:
    if not isinstance(value, str) or not value.strip():
        add_issue(issues, field, "must be a non-empty string")
        return None
    return value


def has_nonnegative_number(
    value: Any, field: str, issues: list[dict[str, str]]
) -> float | None:
    try:
        return require_number(value, field)
    except EditorialInputError as error:
        add_issue(issues, field, str(error))
        return None


def validate_manifest(
    document: dict[str, Any],
    base: Path,
    *,
    allow_missing_files: bool,
    min_completion_hold: float,
    max_completion_hold: float,
    frame_index: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a JSON-ready report for a claim-evidence manifest."""
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    chapters_checked = 0
    scenes_checked = 0
    seen_chapter_ids: set[str] = set()
    seen_scene_ids: set[str] = set()
    indexed_claim_scenes: set[str] = set()

    has_required_string(document.get("schema_version"), "schema_version", errors)
    video = document.get("video")
    if not isinstance(video, dict):
        add_issue(errors, "video", "must be an object with a source")
    else:
        has_required_string(video.get("source"), "video.source", errors)

    if frame_index is not None:
        raw_frames = frame_index.get("frames")
        if not isinstance(raw_frames, list):
            add_issue(errors, "frame_index.frames", "must be an array")
        else:
            for item in raw_frames:
                if isinstance(item, dict) and item.get("kind") == "claim":
                    scene_id = item.get("scene_id")
                    if isinstance(scene_id, str):
                        indexed_claim_scenes.add(scene_id)

    try:
        scenes = list(iter_manifest_scenes(document))
    except EditorialInputError as error:
        add_issue(errors, "chapters", str(error))
        scenes = []

    for chapter_index, chapter, scene_index, scene in scenes:
        chapter_path = f"chapters[{chapter_index}]"
        scene_path = f"{chapter_path}.scenes[{scene_index}]"
        if scene_index == 0:
            chapters_checked += 1
            chapter_id = has_required_string(
                chapter.get("id"), f"{chapter_path}.id", errors
            )
            if chapter_id is not None:
                if chapter_id in seen_chapter_ids:
                    add_issue(errors, f"{chapter_path}.id", "must be unique")
                seen_chapter_ids.add(chapter_id)
            has_required_string(chapter.get("capability"), f"{chapter_path}.capability", errors)
            has_required_string(chapter.get("user_value"), f"{chapter_path}.user_value", errors)
            has_required_string(
                chapter.get("distinct_value_from_prior"),
                f"{chapter_path}.distinct_value_from_prior",
                errors,
            )

        scenes_checked += 1
        scene_id = has_required_string(scene.get("id"), f"{scene_path}.id", errors)
        if scene_id is not None:
            if scene_id in seen_scene_ids:
                add_issue(errors, f"{scene_path}.id", "must be unique across chapters")
            seen_scene_ids.add(scene_id)
        has_required_string(scene.get("claim"), f"{scene_path}.claim", errors)
        timeline = scene.get("timeline")
        if not isinstance(timeline, dict):
            add_issue(errors, f"{scene_path}.timeline", "must be an object")
            timeline_start = None
            timeline_end = None
        else:
            timeline_start = has_nonnegative_number(
                timeline.get("start_seconds"),
                f"{scene_path}.timeline.start_seconds",
                errors,
            )
            timeline_end = has_nonnegative_number(
                timeline.get("end_seconds"),
                f"{scene_path}.timeline.end_seconds",
                errors,
            )
            if (
                timeline_start is not None
                and timeline_end is not None
                and timeline_end <= timeline_start
            ):
                add_issue(
                    errors,
                    f"{scene_path}.timeline.end_seconds",
                    "must be after timeline.start_seconds",
                )
        required_markers = marker_values(
            scene.get("required_visible_markers"),
            f"{scene_path}.required_visible_markers",
            errors,
        )
        has_required_string(
            scene.get("expected_result"), f"{scene_path}.expected_result", errors
        )
        correlation_ids = scene.get("correlation_ids")
        if not isinstance(correlation_ids, list):
            add_issue(errors, f"{scene_path}.correlation_ids", "must be an array")
        elif not correlation_ids and not isinstance(scene.get("correlation_rationale"), str):
            add_issue(
                errors,
                f"{scene_path}.correlation_rationale",
                "is required when correlation_ids is intentionally empty",
            )
        else:
            for correlation_index, correlation in enumerate(correlation_ids):
                correlation_path = (
                    f"{scene_path}.correlation_ids[{correlation_index}]"
                )
                if not isinstance(correlation, dict):
                    add_issue(errors, correlation_path, "must be an object")
                    continue
                has_required_string(correlation.get("name"), f"{correlation_path}.name", errors)
                has_required_string(correlation.get("value"), f"{correlation_path}.value", errors)

        has_required_string(scene.get("fallback"), f"{scene_path}.fallback", errors)

        raw_shots = scene.get("evidence_shots")
        if not isinstance(raw_shots, list) or not raw_shots:
            add_issue(errors, f"{scene_path}.evidence_shots", "must be a non-empty array")
            raw_shots = []
        declared_markers: set[str] = set()
        completion_shots: list[tuple[str, float | None, float | None, set[str]]] = []
        seen_shot_ids: set[str] = set()
        for shot_index, raw_shot in enumerate(raw_shots):
            shot_path = f"{scene_path}.evidence_shots[{shot_index}]"
            if not isinstance(raw_shot, dict):
                add_issue(errors, shot_path, "must be an object")
                continue
            shot_id = has_required_string(raw_shot.get("id"), f"{shot_path}.id", errors)
            if shot_id is not None:
                if shot_id in seen_shot_ids:
                    add_issue(errors, f"{shot_path}.id", "must be unique within this scene")
                seen_shot_ids.add(shot_id)
            filename = has_required_string(raw_shot.get("file"), f"{shot_path}.file", errors)
            if filename is not None and not allow_missing_files:
                evidence_file = resolve_from(base, filename)
                if not evidence_file.is_file():
                    add_issue(
                        errors,
                        f"{shot_path}.file",
                        f"evidence file does not exist: {evidence_file}",
                    )
            evidence_timestamp = has_nonnegative_number(
                raw_shot.get("timestamp_seconds"), f"{shot_path}.timestamp_seconds", errors
            )
            if (
                evidence_timestamp is not None
                and timeline_start is not None
                and timeline_end is not None
                and not timeline_start <= evidence_timestamp <= timeline_end
            ):
                add_issue(
                    errors,
                    f"{shot_path}.timestamp_seconds",
                    "must fall within the scene timeline",
                )
            shot_markers = marker_values(
                raw_shot.get("visible_markers"), f"{shot_path}.visible_markers", errors
            )
            declared_markers.update(shot_markers)
            role = raw_shot.get("role")
            if role not in {"action", "context", "outcome", "response", "status", "telemetry"}:
                add_issue(
                    errors,
                    f"{shot_path}.role",
                    "must be one of action, context, outcome, response, status, telemetry",
                )
            hold_start = has_nonnegative_number(
                raw_shot.get("hold_start_seconds"),
                f"{shot_path}.hold_start_seconds",
                errors,
            )
            hold_end = has_nonnegative_number(
                raw_shot.get("hold_end_seconds"), f"{shot_path}.hold_end_seconds", errors
            )
            if (
                hold_start is not None
                and hold_end is not None
                and hold_end < hold_start
            ):
                add_issue(
                    errors,
                    f"{shot_path}.hold_end_seconds",
                    "must be greater than or equal to hold_start_seconds",
                )
            if (
                hold_start is not None
                and hold_end is not None
                and timeline_start is not None
                and timeline_end is not None
                and (hold_start < timeline_start or hold_end > timeline_end)
            ):
                add_issue(
                    errors,
                    shot_path,
                    "hold_start_seconds and hold_end_seconds must fall within the scene timeline",
                )
            if role in COMPLETION_EVIDENCE_ROLES:
                completion_shots.append((shot_path, hold_start, hold_end, shot_markers))

        missing_markers = required_markers - declared_markers
        if missing_markers:
            add_issue(
                errors,
                f"{scene_path}.required_visible_markers",
                "are not declared by any evidence shot: "
                + ", ".join(sorted(missing_markers)),
            )

        narration = scene.get("narration")
        if not isinstance(narration, dict):
            add_issue(errors, f"{scene_path}.narration", "must be an object")
            narration = {}
        has_required_string(narration.get("claim"), f"{scene_path}.narration.claim", errors)
        narration_start = has_nonnegative_number(
            narration.get("start_seconds"),
            f"{scene_path}.narration.start_seconds",
            errors,
        )
        narration_end = has_nonnegative_number(
            narration.get("end_seconds"),
            f"{scene_path}.narration.end_seconds",
            errors,
        )
        if (
            narration_start is not None
            and narration_end is not None
            and narration_end <= narration_start
        ):
            add_issue(
                errors,
                f"{scene_path}.narration.end_seconds",
                "must be after narration.start_seconds",
            )
        claim_timestamp = has_nonnegative_number(
            narration.get("claim_timestamp_seconds"),
            f"{scene_path}.narration.claim_timestamp_seconds",
            errors,
        )
        declared_hold = has_nonnegative_number(
            narration.get("visible_hold_seconds"),
            f"{scene_path}.narration.visible_hold_seconds",
            errors,
        )
        if (
            claim_timestamp is not None
            and timeline_start is not None
            and timeline_end is not None
            and not timeline_start <= claim_timestamp <= timeline_end
        ):
            add_issue(
                errors,
                f"{scene_path}.narration.claim_timestamp_seconds",
                "must fall within the scene timeline",
            )
        if not isinstance(narration.get("asserts_completion"), bool):
            add_issue(
                errors,
                f"{scene_path}.narration.asserts_completion",
                "must be true or false",
            )
        if narration.get("asserts_completion") is True:
            valid_completion_shot = False
            for shot_path, hold_start, hold_end, shot_markers in completion_shots:
                if hold_start is None or hold_end is None or claim_timestamp is None:
                    continue
                hold_duration = hold_end - hold_start
                if (
                    required_markers <= shot_markers
                    and hold_end <= claim_timestamp
                    and hold_duration >= min_completion_hold
                ):
                    valid_completion_shot = True
                    if hold_duration > max_completion_hold:
                        add_issue(
                            warnings,
                            shot_path,
                            f"completion evidence is held {hold_duration:.2f}s; "
                            f"review whether it can be shortened toward {max_completion_hold:.1f}s",
                            "warning",
                        )
                    break
            if not valid_completion_shot:
                add_issue(
                    errors,
                    f"{scene_path}.narration",
                    "a completion claim needs an outcome, response, or status shot that "
                    f"shows all required markers for at least {min_completion_hold:.1f}s "
                    "before the narration claim timestamp",
                )
            if declared_hold is not None and declared_hold < min_completion_hold:
                add_issue(
                    errors,
                    f"{scene_path}.narration.visible_hold_seconds",
                    f"must be at least {min_completion_hold:.1f}s for a completion claim",
                )
            elif declared_hold is not None and declared_hold > max_completion_hold:
                add_issue(
                    warnings,
                    f"{scene_path}.narration.visible_hold_seconds",
                    f"is {declared_hold:.2f}s; review whether it can be shortened toward "
                    f"{max_completion_hold:.1f}s",
                    "warning",
                )

        if scene.get("lifecycle_claim") is True:
            continuity = scene.get("continuity")
            if not isinstance(continuity, dict):
                add_issue(
                    errors,
                    f"{scene_path}.continuity",
                    "is required for a lifecycle_claim and must declare before/after identifiers",
                )
            elif "before" not in continuity or "after" not in continuity:
                add_issue(
                    errors,
                    f"{scene_path}.continuity",
                    "must contain both before and after evidence records",
                )

        if frame_index is not None and scene_id is not None and scene_id not in indexed_claim_scenes:
            add_issue(
                warnings,
                scene_path,
                "no claim timestamp frame appears in the supplied frame index",
                "warning",
            )

    return {
        "tool": "validate_claim_evidence",
        "valid": not errors,
        "checked": {"chapters": chapters_checked, "scenes": scenes_checked},
        "errors": errors,
        "warnings": warnings,
        "strategy": (
            "Validated manifest fields, declared marker coverage, timing, and referenced "
            "files. Marker declarations are reviewer attestations; this tool does not "
            "perform OCR or claim that pixels alone prove a product behavior."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a claim-evidence manifest and declared evidence files."
    )
    parser.add_argument("manifest", type=Path, help="Claim-evidence manifest JSON")
    parser.add_argument(
        "--frame-index",
        type=Path,
        help="Optional index.json generated by extract_scene_qc.py",
    )
    parser.add_argument(
        "--allow-missing-files",
        action="store_true",
        help="Use for pre-capture storyboard review; still validates all manifest fields.",
    )
    parser.add_argument(
        "--min-completion-hold",
        type=float,
        default=3.0,
        help="Minimum visible completion evidence before narration (default: 3.0).",
    )
    parser.add_argument(
        "--max-completion-hold",
        type=float,
        default=5.0,
        help="Review warning threshold for completion evidence duration (default: 5.0).",
    )
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()

    if args.min_completion_hold <= 0 or args.max_completion_hold < args.min_completion_hold:
        raise EditorialInputError(
            "completion hold thresholds must be positive and max must be at least min"
        )
    document = require_mapping(load_json(args.manifest), "manifest")
    frame_index = (
        require_mapping(load_json(args.frame_index), "frame index")
        if args.frame_index is not None
        else None
    )
    report = validate_manifest(
        document,
        args.manifest.parent,
        allow_missing_files=args.allow_missing_files,
        min_completion_hold=args.min_completion_hold,
        max_completion_hold=args.max_completion_hold,
        frame_index=frame_index,
    )
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
