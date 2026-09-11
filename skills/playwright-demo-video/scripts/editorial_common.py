"""Shared helpers for the demo-video editorial QA scripts.

The helpers intentionally use only the Python standard library so the
validation tools work on Windows, macOS, and Linux. FFmpeg is invoked only by
scripts that need to inspect or extract video frames.
"""

from __future__ import annotations

import json
import math
import subprocess
from collections.abc import Iterator
from pathlib import Path
from typing import Any


class EditorialInputError(ValueError):
    """Raised when an editorial manifest or command input is malformed."""


def load_json(path: Path) -> Any:
    """Load a UTF-8 JSON document with an actionable input error."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise EditorialInputError(f"JSON file does not exist: {path}") from error
    except json.JSONDecodeError as error:
        raise EditorialInputError(
            f"Invalid JSON in {path} at line {error.lineno}, column {error.colno}: "
            f"{error.msg}"
        ) from error


def require_mapping(value: Any, field: str) -> dict[str, Any]:
    """Return a JSON object or raise a field-specific error."""
    if not isinstance(value, dict):
        raise EditorialInputError(f"{field} must be an object")
    return value


def require_list(value: Any, field: str) -> list[Any]:
    """Return a JSON array or raise a field-specific error."""
    if not isinstance(value, list):
        raise EditorialInputError(f"{field} must be an array")
    return value


def require_string(value: Any, field: str) -> str:
    """Return a non-empty string or raise a field-specific error."""
    if not isinstance(value, str) or not value.strip():
        raise EditorialInputError(f"{field} must be a non-empty string")
    return value


def require_number(value: Any, field: str) -> float:
    """Return a finite non-negative number used for media timestamps."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise EditorialInputError(f"{field} must be a number")
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise EditorialInputError(f"{field} must be a finite non-negative number")
    return result


def resolve_from(base: Path, value: str) -> Path:
    """Resolve a manifest-relative path without imposing a delivery-root policy."""
    candidate = Path(value)
    return candidate.resolve() if candidate.is_absolute() else (base / candidate).resolve()


def normalize_marker(value: str) -> str:
    """Compare human-declared markers with whitespace-normalized exact matching."""
    return " ".join(value.split()).casefold()


def emit_json(report: dict[str, Any], output: Path | None = None) -> None:
    """Write a stable JSON report to stdout and, optionally, a file."""
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


def iter_manifest_scenes(
    document: dict[str, Any],
) -> Iterator[tuple[int, dict[str, Any], int, dict[str, Any]]]:
    """Yield chapter and scene objects from the documented claim-evidence manifest."""
    chapters = require_list(document.get("chapters"), "chapters")
    if not chapters:
        raise EditorialInputError("chapters must contain at least one chapter")
    for chapter_index, raw_chapter in enumerate(chapters):
        chapter = require_mapping(raw_chapter, f"chapters[{chapter_index}]")
        scenes = require_list(
            chapter.get("scenes"), f"chapters[{chapter_index}].scenes"
        )
        if not scenes:
            raise EditorialInputError(
                f"chapters[{chapter_index}].scenes must contain at least one scene"
            )
        for scene_index, raw_scene in enumerate(scenes):
            scene = require_mapping(
                raw_scene, f"chapters[{chapter_index}].scenes[{scene_index}]"
            )
            yield chapter_index, chapter, scene_index, scene


def narration_entries(document: dict[str, Any]) -> list[dict[str, Any]]:
    """Read a standalone narration schedule or scene-level narration records.

    A standalone ``narration_schedule`` is useful after editorial retiming.
    Otherwise this reads ``narration.start_seconds`` and ``end_seconds`` from
    each scene in the claim-evidence manifest.
    """
    raw_schedule = document.get("narration_schedule", document.get("narration"))
    if isinstance(raw_schedule, list):
        entries = require_list(raw_schedule, "narration_schedule")
        result: list[dict[str, Any]] = []
        for index, raw_entry in enumerate(entries):
            entry = require_mapping(raw_entry, f"narration_schedule[{index}]")
            result.append(
                {
                    "id": require_string(entry.get("id"), f"narration_schedule[{index}].id"),
                    "start_seconds": require_number(
                        entry.get("start_seconds"),
                        f"narration_schedule[{index}].start_seconds",
                    ),
                    "end_seconds": require_number(
                        entry.get("end_seconds"),
                        f"narration_schedule[{index}].end_seconds",
                    ),
                    "claim": entry.get("claim", ""),
                }
            )
        return result

    result = []
    for chapter_index, chapter, scene_index, scene in iter_manifest_scenes(document):
        narration = scene.get("narration")
        if not isinstance(narration, dict):
            continue
        if "start_seconds" not in narration or "end_seconds" not in narration:
            continue
        chapter_id = str(chapter.get("id", chapter_index))
        scene_id = str(scene.get("id", scene_index))
        result.append(
            {
                "id": f"{chapter_id}/{scene_id}",
                "start_seconds": require_number(
                    narration["start_seconds"],
                    f"chapters[{chapter_index}].scenes[{scene_index}].narration.start_seconds",
                ),
                "end_seconds": require_number(
                    narration["end_seconds"],
                    f"chapters[{chapter_index}].scenes[{scene_index}].narration.end_seconds",
                ),
                "claim": narration.get("claim", ""),
            }
        )
    return result


def ffprobe_json(video: Path, entries: str) -> dict[str, Any]:
    """Read selected FFprobe fields using an argument list rather than a shell."""
    try:
        completed = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                entries,
                "-of",
                "json",
                str(video),
            ],
            check=True,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError as error:
        raise EditorialInputError(
            "ffprobe is required but was not found on PATH. Install FFmpeg first."
        ) from error
    except subprocess.CalledProcessError as error:
        detail = error.stderr.strip() or error.stdout.strip()
        raise EditorialInputError(f"ffprobe could not inspect {video}: {detail}") from error
    try:
        return require_mapping(json.loads(completed.stdout), "ffprobe output")
    except json.JSONDecodeError as error:
        raise EditorialInputError("ffprobe returned invalid JSON") from error


def video_duration_seconds(video: Path) -> float:
    """Return a positive media duration from FFprobe."""
    document = ffprobe_json(video, "format=duration")
    format_info = require_mapping(document.get("format"), "ffprobe format")
    raw_duration = format_info.get("duration")
    try:
        duration = float(raw_duration)
    except (TypeError, ValueError) as error:
        raise EditorialInputError(f"ffprobe did not return a duration for {video}") from error
    if duration <= 0:
        raise EditorialInputError(f"video duration must be positive, got {duration}")
    return duration
