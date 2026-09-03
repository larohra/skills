from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


def resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def run(command: list[str]) -> None:
    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr[-4000:])


def main() -> None:
    parser = argparse.ArgumentParser(description="Trim and concatenate Playwright scene videos.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    document = json.loads(args.manifest.read_text(encoding="utf-8"))
    base = args.manifest.parent
    scenes = document.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise ValueError("manifest.scenes must be a non-empty list")

    width = int(document.get("width", 1440))
    height = int(document.get("height", 900))
    fps = int(document.get("fps", 30))
    crf = int(document.get("crf", 22))
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="playwright-demo-stitch-") as temp:
        temp_dir = Path(temp)
        trimmed: list[Path] = []
        for index, scene in enumerate(scenes):
            source = resolve(base, str(scene["path"]))
            start = float(scene.get("start", 0))
            duration = float(scene["duration"])
            if start < 0 or duration <= 0:
                raise ValueError("scene start must be non-negative and duration positive")
            target = temp_dir / f"{index:03d}.mp4"
            run(
                [
                    "ffmpeg",
                    "-y",
                    "-ss",
                    f"{start:.3f}",
                    "-i",
                    str(source),
                    "-t",
                    f"{duration:.3f}",
                    "-vf",
                    f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                    f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,"
                    f"fps={fps},format=yuv420p",
                    "-an",
                    "-c:v",
                    "libx264",
                    "-preset",
                    "medium",
                    "-crf",
                    str(crf),
                    str(target),
                ]
            )
            trimmed.append(target)
        concat = temp_dir / "concat.txt"
        concat.write_text(
            "".join(f"file '{path.as_posix()}'\n" for path in trimmed),
            encoding="utf-8",
        )
        run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat),
                "-c",
                "copy",
                "-movflags",
                "+faststart",
                str(args.output),
            ]
        )
    print(args.output)


if __name__ == "__main__":
    main()
