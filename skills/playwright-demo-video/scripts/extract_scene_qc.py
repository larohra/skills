"""Extract deterministic review frames from a claim-evidence video manifest."""

from __future__ import annotations

import argparse
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

from editorial_common import (
    EditorialInputError,
    emit_json,
    iter_manifest_scenes,
    load_json,
    require_mapping,
    require_number,
    require_string,
    resolve_from,
    video_duration_seconds,
)


def _scene_timeline(scene: dict[str, Any], field: str) -> tuple[float, float]:
    timeline = require_mapping(scene.get("timeline"), f"{field}.timeline")
    start = require_number(timeline.get("start_seconds"), f"{field}.timeline.start_seconds")
    end = require_number(timeline.get("end_seconds"), f"{field}.timeline.end_seconds")
    if end <= start:
        raise EditorialInputError(f"{field}.timeline.end_seconds must be after start_seconds")
    return start, end


def plan_qc_frames(
    document: dict[str, Any], transition_offset: float
) -> list[dict[str, Any]]:
    """Plan scene midpoint, evidence, claim, and transition review frames."""
    if transition_offset < 0:
        raise EditorialInputError("transition offset must be non-negative")
    planned: list[dict[str, Any]] = []
    previous_scene: tuple[str, float, float] | None = None
    seen: set[tuple[str, str, int]] = set()

    def add(scene_id: str, kind: str, timestamp: float, reason: str) -> None:
        key = (scene_id, kind, round(timestamp * 1000))
        if key not in seen:
            seen.add(key)
            planned.append(
                {
                    "scene_id": scene_id,
                    "kind": kind,
                    "timestamp_seconds": round(timestamp, 3),
                    "reason": reason,
                }
            )

    for chapter_index, _chapter, scene_index, scene in iter_manifest_scenes(document):
        scene_path = f"chapters[{chapter_index}].scenes[{scene_index}]"
        scene_id = require_string(scene.get("id"), f"{scene_path}.id")
        start, end = _scene_timeline(scene, scene_path)
        add(
            scene_id,
            "midpoint",
            (start + end) / 2,
            "Scene midpoint checks readable composition and the primary proof.",
        )

        evidence_shots = scene.get("evidence_shots", [])
        if not isinstance(evidence_shots, list):
            raise EditorialInputError(f"{scene_path}.evidence_shots must be an array")
        for evidence_index, raw_evidence in enumerate(evidence_shots):
            evidence = require_mapping(
                raw_evidence, f"{scene_path}.evidence_shots[{evidence_index}]"
            )
            timestamp = require_number(
                evidence.get("timestamp_seconds"),
                f"{scene_path}.evidence_shots[{evidence_index}].timestamp_seconds",
            )
            add(
                scene_id,
                "evidence",
                timestamp,
                "Declared evidence timestamp checks the planned proof frame.",
            )

        narration = scene.get("narration")
        if isinstance(narration, dict) and "claim_timestamp_seconds" in narration:
            timestamp = require_number(
                narration["claim_timestamp_seconds"],
                f"{scene_path}.narration.claim_timestamp_seconds",
            )
            add(
                scene_id,
                "claim",
                timestamp,
                "Narration claim timestamp checks that the spoken claim is visible.",
            )

        if previous_scene is not None:
            previous_id, _previous_start, previous_end = previous_scene
            boundary = start
            add(
                previous_id,
                "transition-before",
                max(0.0, min(previous_end, boundary - transition_offset)),
                "Frame immediately before the chapter/scene transition.",
            )
            add(
                scene_id,
                "transition-after",
                min(end, boundary + transition_offset),
                "Frame immediately after the chapter/scene transition.",
            )
        previous_scene = (scene_id, start, end)

    return sorted(
        planned, key=lambda item: (item["timestamp_seconds"], item["scene_id"], item["kind"])
    )


def _manifest_video(document: dict[str, Any], base: Path, override: Path | None) -> Path:
    if override is not None:
        return override.resolve()
    video = require_mapping(document.get("video"), "video")
    source = require_string(video.get("source"), "video.source")
    return resolve_from(base, source)


def _run_ffmpeg(command: list[str]) -> None:
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError as error:
        raise EditorialInputError(
            "ffmpeg is required but was not found on PATH. Install FFmpeg first."
        ) from error
    except subprocess.CalledProcessError as error:
        raise EditorialInputError(f"ffmpeg failed with exit code {error.returncode}") from error


def extract_frames(
    video: Path,
    planned: list[dict[str, Any]],
    output_dir: Path,
    *,
    width: int,
    overwrite: bool,
) -> list[dict[str, Any]]:
    """Extract planned frames with FFmpeg and return index entries."""
    frames_dir = output_dir / "frames"
    targets = [frames_dir / f"qc-{index:04d}.png" for index in range(1, len(planned) + 1)]
    existing = [path for path in targets if path.exists()]
    if existing and not overwrite:
        raise EditorialInputError(
            "refusing to overwrite existing QC frames; choose an empty output directory "
            "or pass --overwrite: " + ", ".join(str(path) for path in existing[:3])
        )
    frames_dir.mkdir(parents=True, exist_ok=True)
    indexed: list[dict[str, Any]] = []
    for index, (point, target) in enumerate(zip(planned, targets), start=1):
        command = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-nostdin",
            "-y",
            "-ss",
            f"{point['timestamp_seconds']:.3f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-vf",
            f"scale={width}:-2",
            str(target),
        ]
        _run_ffmpeg(command)
        indexed.append(
            {
                "id": f"qc-{index:04d}",
                **point,
                "file": str(Path("frames") / target.name),
            }
        )
    return indexed


def create_contact_sheet(
    output_dir: Path,
    frame_count: int,
    *,
    columns: int,
    tile_width: int,
    overwrite: bool,
) -> Path:
    """Tile sequential QC frames with FFmpeg without relying on shell globbing."""
    if columns <= 0 or tile_width <= 0:
        raise EditorialInputError("contact-sheet columns and tile width must be positive")
    contact_sheet = output_dir / "contact-sheet.png"
    if contact_sheet.exists() and not overwrite:
        raise EditorialInputError(
            f"refusing to overwrite existing contact sheet: {contact_sheet}"
        )
    rows = max(1, math.ceil(frame_count / columns))
    _run_ffmpeg(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-nostdin",
            "-y",
            "-framerate",
            "1",
            "-start_number",
            "1",
            "-i",
            str(output_dir / "frames" / "qc-%04d.png"),
            "-vf",
            (
                f"scale={tile_width}:-2,trim=end_frame={frame_count},"
                f"tile={columns}x{rows}:padding=8:margin=8"
            ),
            "-frames:v",
            "1",
            str(contact_sheet),
        ]
    )
    return contact_sheet


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Extract scene midpoint, evidence, narration-claim, and transition frames "
            "from a claim-evidence manifest."
        )
    )
    parser.add_argument("manifest", type=Path, help="Claim-evidence manifest JSON")
    parser.add_argument("output_dir", type=Path, help="Directory for QC frames and index.json")
    parser.add_argument(
        "--video",
        type=Path,
        help="Override manifest video.source without editing the manifest.",
    )
    parser.add_argument(
        "--transition-offset",
        type=float,
        default=0.25,
        help="Seconds on either side of each transition (default: 0.25).",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=960,
        help="Output frame width in pixels (default: 960).",
    )
    parser.add_argument(
        "--columns",
        type=int,
        default=4,
        help="Contact-sheet columns (default: 4).",
    )
    parser.add_argument(
        "--tile-width",
        type=int,
        default=360,
        help="Contact-sheet tile width (default: 360).",
    )
    parser.add_argument(
        "--no-contact-sheet",
        action="store_true",
        help="Extract frames and index only.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Write the planned machine-readable index without invoking FFmpeg.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace only this tool's named QC frames, index, and contact sheet.",
    )
    args = parser.parse_args()
    if args.width <= 0:
        raise EditorialInputError("--width must be positive")

    document = require_mapping(load_json(args.manifest), "manifest")
    video = _manifest_video(document, args.manifest.parent, args.video)
    planned = plan_qc_frames(document, args.transition_offset)
    if not planned:
        raise EditorialInputError("manifest did not contain any extractable QC points")
    index_path = args.output_dir / "index.json"
    if index_path.exists() and not args.overwrite:
        raise EditorialInputError(
            f"refusing to overwrite existing QC index: {index_path}; use --overwrite"
        )

    duration: float | None = None
    if not args.dry_run:
        if not video.is_file():
            raise EditorialInputError(f"video does not exist: {video}")
        duration = video_duration_seconds(video)
        out_of_range = [
            point
            for point in planned
            if point["timestamp_seconds"] > duration
        ]
        if out_of_range:
            raise EditorialInputError(
                "QC timestamp exceeds video duration "
                f"({duration:.3f}s): {out_of_range[0]['scene_id']} at "
                f"{out_of_range[0]['timestamp_seconds']:.3f}s"
            )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    frames = (
        []
        if args.dry_run
        else extract_frames(
            video,
            planned,
            args.output_dir,
            width=args.width,
            overwrite=args.overwrite,
        )
    )
    contact_sheet: str | None = None
    if not args.dry_run and not args.no_contact_sheet:
        contact_sheet = str(
            create_contact_sheet(
                args.output_dir,
                len(frames),
                columns=args.columns,
                tile_width=args.tile_width,
                overwrite=args.overwrite,
            ).relative_to(args.output_dir)
        )
    report = {
        "tool": "extract_scene_qc",
        "manifest": str(args.manifest),
        "video": str(video),
        "video_duration_seconds": duration,
        "dry_run": args.dry_run,
        "contact_sheet": contact_sheet,
        "frames": frames if not args.dry_run else planned,
    }
    emit_json(report, index_path)


if __name__ == "__main__":
    try:
        main()
    except EditorialInputError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2) from error
