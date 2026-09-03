from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a tiled video contact sheet.")
    parser.add_argument("video", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--interval", type=float, default=12)
    parser.add_argument("--columns", type=int, default=3)
    parser.add_argument("--rows", type=int, default=3)
    parser.add_argument("--tile-width", type=int, default=480)
    args = parser.parse_args()

    if args.interval <= 0 or args.columns <= 0 or args.rows <= 0:
        raise ValueError("interval, columns, and rows must be positive")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(args.video),
            "-vf",
            f"fps=1/{args.interval},scale={args.tile_width}:-1,"
            f"tile={args.columns}x{args.rows}",
            "-frames:v",
            "1",
            "-update",
            "1",
            str(args.output),
        ],
        check=True,
    )
    print(args.output)


if __name__ == "__main__":
    main()
