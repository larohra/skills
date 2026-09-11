"""Check a narration schedule for overlap and uncomfortable timing gaps."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from editorial_common import (
    EditorialInputError,
    emit_json,
    load_json,
    narration_entries,
    require_mapping,
)


def check_narration_gaps(
    entries: list[dict[str, Any]], minimum_gap: float
) -> dict[str, Any]:
    """Return overlap and short-gap diagnostics for narration entries."""
    diagnostics: list[dict[str, Any]] = []
    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for index, entry in enumerate(entries):
        entry_id = entry["id"]
        start = entry["start_seconds"]
        end = entry["end_seconds"]
        if entry_id in seen_ids:
            diagnostics.append(
                {
                    "kind": "duplicate-id",
                    "entry": entry_id,
                    "message": f"Narration entry id '{entry_id}' is repeated.",
                }
            )
        seen_ids.add(entry_id)
        if end <= start:
            diagnostics.append(
                {
                    "kind": "invalid-duration",
                    "entry": entry_id,
                    "message": (
                        f"Narration entry '{entry_id}' ends at {end:.3f}s but starts "
                        f"at {start:.3f}s."
                    ),
                }
            )
        normalized.append(entry)

    ordered = sorted(normalized, key=lambda item: (item["start_seconds"], item["end_seconds"], item["id"]))
    active = ordered[0] if ordered else None
    for current in ordered[1:]:
        if active is None:
            active = current
            continue
        gap = current["start_seconds"] - active["end_seconds"]
        if gap < 0:
            diagnostics.append(
                {
                    "kind": "overlap",
                    "previous": active["id"],
                    "current": current["id"],
                    "gap_seconds": round(gap, 3),
                    "message": (
                        f"'{current['id']}' overlaps '{active['id']}' by "
                        f"{abs(gap):.3f}s."
                    ),
                }
            )
        elif gap < minimum_gap:
            diagnostics.append(
                {
                    "kind": "short-gap",
                    "previous": active["id"],
                    "current": current["id"],
                    "gap_seconds": round(gap, 3),
                    "message": (
                        f"Only {gap:.3f}s separates '{active['id']}' and "
                        f"'{current['id']}'; the configured minimum is "
                        f"{minimum_gap:.3f}s."
                    ),
                }
            )
        if current["end_seconds"] > active["end_seconds"]:
            active = current

    return {
        "tool": "check_narration_gaps",
        "valid": not diagnostics,
        "minimum_gap_seconds": minimum_gap,
        "entries_checked": len(entries),
        "diagnostics": diagnostics,
        "ordered_entries": [
            {
                "id": entry["id"],
                "start_seconds": entry["start_seconds"],
                "end_seconds": entry["end_seconds"],
            }
            for entry in ordered
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fail when narration clips overlap or leave too little breathing room."
    )
    parser.add_argument(
        "schedule",
        type=Path,
        help="JSON with narration_schedule or a claim-evidence manifest with scene narration.",
    )
    parser.add_argument(
        "--minimum-gap",
        type=float,
        default=0.8,
        help="Required gap in seconds between narration clips (default: 0.8).",
    )
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()
    if args.minimum_gap < 0:
        raise EditorialInputError("--minimum-gap must be non-negative")

    document = require_mapping(load_json(args.schedule), "schedule")
    report = check_narration_gaps(narration_entries(document), args.minimum_gap)
    report["schedule"] = str(args.schedule)
    emit_json(report, args.output)
    if not report["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except EditorialInputError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2) from error
