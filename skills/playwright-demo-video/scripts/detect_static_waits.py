"""Flag likely static waits using low-resolution FFmpeg frame differences.

The result is deliberately a review aid. Similar frames can represent a useful
status hold, and small animations can mask an unhelpful wait, so this script
does not fail unless --fail-on-static is explicitly requested.
"""

from __future__ import annotations

import argparse
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

from editorial_common import EditorialInputError, emit_json, video_duration_seconds


def normalized_difference(previous: bytes, current: bytes) -> float:
    """Return the mean absolute 8-bit pixel difference normalized to 0..1."""
    if len(previous) != len(current) or not previous:
        raise EditorialInputError("frame samples must be non-empty and equally sized")
    return sum(abs(left - right) for left, right in zip(previous, current)) / (
        len(previous) * 255
    )


def detect_static_regions(
    differences: list[float],
    *,
    interval: float,
    threshold: float,
    minimum_duration: float,
) -> list[dict[str, float]]:
    """Group consecutive low-difference sample intervals into review regions."""
    regions: list[dict[str, float]] = []
    start: float | None = None
    values: list[float] = []

    def finish(end: float) -> None:
        nonlocal start, values
        if start is not None and end - start >= minimum_duration:
            regions.append(
                {
                    "start_seconds": round(start, 3),
                    "end_seconds": round(end, 3),
                    "duration_seconds": round(end - start, 3),
                    "mean_difference": round(sum(values) / len(values), 6),
                    "max_difference": round(max(values), 6),
                }
            )
        start = None
        values = []

    for interval_index, difference in enumerate(differences, start=1):
        interval_start = (interval_index - 1) * interval
        interval_end = interval_index * interval
        if difference <= threshold:
            if start is None:
                start = interval_start
            values.append(difference)
        else:
            finish(interval_start)
    finish(len(differences) * interval)
    return regions


def sample_frames(
    video: Path,
    *,
    interval: float,
    sample_width: int,
    sample_height: int,
) -> list[bytes]:
    """Sample consistently sized grayscale frames through a shell-free FFmpeg call."""
    try:
        completed = subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-nostdin",
                "-i",
                str(video),
                "-vf",
                (
                    f"fps=1/{interval},scale={sample_width}:{sample_height}:"
                    "flags=area,format=gray"
                ),
                "-f",
                "rawvideo",
                "-",
            ],
            check=True,
            capture_output=True,
        )
    except FileNotFoundError as error:
        raise EditorialInputError(
            "ffmpeg is required but was not found on PATH. Install FFmpeg first."
        ) from error
    except subprocess.CalledProcessError as error:
        detail = error.stderr.decode(errors="replace").strip()
        raise EditorialInputError(f"ffmpeg could not sample {video}: {detail}") from error

    frame_size = sample_width * sample_height
    if len(completed.stdout) % frame_size:
        raise EditorialInputError("ffmpeg returned an incomplete grayscale frame sample")
    return [
        completed.stdout[offset : offset + frame_size]
        for offset in range(0, len(completed.stdout), frame_size)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Flag likely static/dead video regions from deterministic low-resolution "
            "frame-difference sampling. Review results before cutting."
        )
    )
    parser.add_argument("video", type=Path, help="Video to sample")
    parser.add_argument(
        "--interval",
        type=float,
        default=0.5,
        help="Seconds between sampled frames (default: 0.5).",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.005,
        help="Maximum normalized mean pixel difference considered static (default: 0.005).",
    )
    parser.add_argument(
        "--minimum-duration",
        type=float,
        default=3.0,
        help="Report static runs at least this long in seconds (default: 3.0).",
    )
    parser.add_argument(
        "--sample-width",
        type=int,
        default=64,
        help="Low-resolution sample width (default: 64).",
    )
    parser.add_argument(
        "--sample-height",
        type=int,
        default=36,
        help="Low-resolution sample height (default: 36).",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=10000,
        help="Fail before sampling an unexpectedly long video (default: 10000).",
    )
    parser.add_argument(
        "--include-samples",
        action="store_true",
        help="Include each frame-to-frame difference in the JSON report.",
    )
    parser.add_argument(
        "--fail-on-static",
        action="store_true",
        help="Exit nonzero when likely static regions are found.",
    )
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()
    if (
        args.interval <= 0
        or args.threshold < 0
        or args.minimum_duration <= 0
        or args.sample_width <= 0
        or args.sample_height <= 0
        or args.max_samples <= 1
    ):
        raise EditorialInputError("sampling interval, sizes, duration, and limits must be positive")
    if not args.video.is_file():
        raise EditorialInputError(f"video does not exist: {args.video}")

    duration = video_duration_seconds(args.video)
    estimated_samples = math.ceil(duration / args.interval) + 1
    if estimated_samples > args.max_samples:
        raise EditorialInputError(
            f"estimated {estimated_samples} samples exceeds --max-samples {args.max_samples}; "
            "increase --interval or raise the explicit limit"
        )
    frames = sample_frames(
        args.video,
        interval=args.interval,
        sample_width=args.sample_width,
        sample_height=args.sample_height,
    )
    if len(frames) < 2:
        raise EditorialInputError("video did not yield enough sample frames to compare")
    differences = [
        normalized_difference(previous, current)
        for previous, current in zip(frames, frames[1:])
    ]
    regions = detect_static_regions(
        differences,
        interval=args.interval,
        threshold=args.threshold,
        minimum_duration=args.minimum_duration,
    )
    report: dict[str, Any] = {
        "tool": "detect_static_waits",
        "video": str(args.video),
        "duration_seconds": round(duration, 3),
        "sample_count": len(frames),
        "interval_seconds": args.interval,
        "threshold": args.threshold,
        "minimum_duration_seconds": args.minimum_duration,
        "likely_static_regions": regions,
        "limitations": [
            "A deliberate readable status hold can look static and should not be cut blindly.",
            "Small animated elements can hide a dead wait from pixel-difference sampling.",
            "This report detects visual similarity, not product progress or narration quality.",
        ],
    }
    if args.include_samples:
        report["differences"] = [
            {
                "at_seconds": round((index + 1) * args.interval, 3),
                "normalized_difference": round(value, 6),
            }
            for index, value in enumerate(differences)
        ]
    emit_json(report, args.output)
    if args.fail_on_static and regions:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except EditorialInputError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2) from error
