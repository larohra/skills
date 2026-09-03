from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def box(value: str) -> tuple[int, int, int, int]:
    parts = tuple(int(item.strip()) for item in value.split(","))
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("expected x,y,width,height")
    x, y, width, height = parts
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("width and height must be positive")
    return x, y, x + width, y + height


def point(value: str) -> tuple[int, int]:
    parts = tuple(int(item.strip()) for item in value.split(","))
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("expected x,y")
    return parts


def color(value: str) -> tuple[int, int, int, int]:
    normalized = value.removeprefix("#")
    if len(normalized) != 6:
        raise argparse.ArgumentTypeError("expected a six-digit hex color")
    return (
        int(normalized[0:2], 16),
        int(normalized[2:4], 16),
        int(normalized[4:6], 16),
        255,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a transparent demo highlight PNG.")
    parser.add_argument("output", type=Path)
    parser.add_argument("--rect", required=True, type=box, help="x,y,width,height")
    parser.add_argument("--label-box", required=True, type=box, help="x,y,width,height")
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--arrow-start", required=True, type=point)
    parser.add_argument("--arrow-end", required=True, type=point)
    parser.add_argument("--color", type=color, default=color("#38bdf8"))
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument(
        "--font-bold",
        default=r"C:\Windows\Fonts\segoeuib.ttf",
    )
    parser.add_argument(
        "--font-regular",
        default=r"C:\Windows\Fonts\segoeui.ttf",
    )
    args = parser.parse_args()

    image = Image.new("RGBA", (args.width, args.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    accent = args.color
    draw.rounded_rectangle(
        args.rect,
        radius=14,
        outline=accent,
        width=6,
        fill=(*accent[:3], 20),
    )
    draw.rounded_rectangle(
        args.label_box,
        radius=12,
        fill=(8, 17, 31, 232),
        outline=accent,
        width=3,
    )
    bold = ImageFont.truetype(args.font_bold, 24)
    regular = ImageFont.truetype(args.font_regular, 17)
    draw.text(
        (args.label_box[0] + 14, args.label_box[1] + 10),
        args.title,
        font=bold,
        fill="white",
    )
    draw.text(
        (args.label_box[0] + 14, args.label_box[1] + 43),
        args.subtitle,
        font=regular,
        fill=(203, 213, 225, 255),
    )
    draw.line([args.arrow_start, args.arrow_end], fill=accent, width=6)
    angle = math.atan2(
        args.arrow_end[1] - args.arrow_start[1],
        args.arrow_end[0] - args.arrow_start[0],
    )
    for delta in (2.55, -2.55):
        endpoint = (
            args.arrow_end[0] + 18 * math.cos(angle + delta),
            args.arrow_end[1] + 18 * math.sin(angle + delta),
        )
        draw.line([args.arrow_end, endpoint], fill=accent, width=6)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)
    print(args.output)


if __name__ == "__main__":
    main()
