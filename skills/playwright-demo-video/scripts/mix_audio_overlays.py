from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def source_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="Add timed overlays, narration, and music.")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    document = json.loads(args.manifest.read_text(encoding="utf-8"))
    base = args.manifest.parent
    source = resolve(base, str(document["source"]))
    output = resolve(base, str(document["output"]))
    overlays = document.get("overlays", [])
    narration = document.get("narration", [])
    music = document.get("music")
    duration = source_duration(source)
    output.parent.mkdir(parents=True, exist_ok=True)

    command = ["ffmpeg", "-y", "-i", str(source)]
    for overlay in overlays:
        command.extend(
            ["-loop", "1", "-framerate", "30", "-i", str(resolve(base, overlay["path"]))]
        )

    music_index: int | None = None
    if music:
        music_index = 1 + len(overlays)
        command.extend(["-i", str(resolve(base, music["path"]))])

    narration_start_index = 1 + len(overlays) + (1 if music else 0)
    for segment in narration:
        command.extend(["-i", str(resolve(base, segment["path"]))])

    filters: list[str] = []
    current = "0:v"
    for index, overlay in enumerate(overlays, start=1):
        windows = overlay.get("windows", [])
        expression = "+".join(
            f"between(t,{float(start)},{float(end)})" for start, end in windows
        )
        if not expression:
            raise ValueError("each overlay requires at least one [start, end] window")
        target = f"v{index}"
        filters.append(
            f"[{current}][{index}:v]overlay=0:0:enable='{expression}'[{target}]"
        )
        current = target
    if overlays:
        filters[-1] = filters[-1].rsplit("[", 1)[0] + "[vout]"
    else:
        filters.append("[0:v]null[vout]")

    audio_labels: list[str] = []
    if music_index is not None:
        volume = float(music.get("volume", 0.2))
        filters.append(
            f"[{music_index}:a]aresample=48000,"
            f"aformat=channel_layouts=stereo,volume={volume}[music]"
        )
        audio_labels.append("[music]")
    for offset, segment in enumerate(narration, start=narration_start_index):
        label = f"n{offset - narration_start_index + 1}"
        start_ms = int(segment["start_ms"])
        volume = float(segment.get("volume", 1.15))
        filters.append(
            f"[{offset}:a]aresample=48000,aformat=channel_layouts=stereo,"
            f"adelay={start_ms}|{start_ms},volume={volume}[{label}]"
        )
        audio_labels.append(f"[{label}]")

    if audio_labels:
        filters.append(
            "".join(audio_labels)
            + f"amix=inputs={len(audio_labels)}:duration=longest:"
            "dropout_transition=0:normalize=0,alimiter=limit=0.95[aout]"
        )

    command.extend(["-filter_complex", ";".join(filters), "-map", "[vout]"])
    if audio_labels:
        command.extend(["-map", "[aout]", "-c:a", "aac", "-b:a", "192k"])
    else:
        command.append("-an")
    command.extend(
        [
            "-t",
            f"{duration:.3f}",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            str(document.get("crf", 20)),
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output),
        ]
    )
    subprocess.run(command, check=True)
    print(output)


if __name__ == "__main__":
    main()
