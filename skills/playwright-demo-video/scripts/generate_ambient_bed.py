from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a subtle license-free ambient WAV.")
    parser.add_argument("output", type=Path)
    parser.add_argument("--duration", type=float, required=True)
    parser.add_argument("--level", type=float, default=1.0)
    args = parser.parse_args()

    if args.duration <= 0:
        raise ValueError("duration must be positive")
    if not 0 < args.level <= 2:
        raise ValueError("level must be greater than 0 and at most 2")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fade_out = max(0.0, args.duration - 5)
    expression = (
        f"{0.016 * args.level}*sin(2*PI*110*t)"
        f"+{0.010 * args.level}*sin(2*PI*164.81*t)"
        f"+{0.007 * args.level}*sin(2*PI*220*t)"
    )
    audio_filter = (
        "lowpass=f=900,highpass=f=70,aecho=0.8:0.35:900:0.18,"
        f"afade=t=in:st=0:d=3,afade=t=out:st={fade_out}:d=5,"
        f"atrim=duration={args.duration},asetpts=N/SR/TB,"
        "aformat=channel_layouts=stereo"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"aevalsrc={expression}:s=48000:d={args.duration + 1}",
            "-af",
            audio_filter,
            str(args.output),
        ],
        check=True,
    )
    print(args.output)


if __name__ == "__main__":
    main()
