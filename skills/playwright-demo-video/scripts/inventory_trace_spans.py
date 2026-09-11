"""Inventory named spans and dependency types from a sanitized local export."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from editorial_common import EditorialInputError, emit_json, load_json

SPAN_CONTAINER_NAMES = {"spans", "traces", "telemetryspans", "scopeSpans".casefold()}
DEPENDENCY_CONTAINER_NAMES = {
    "dependencies",
    "dependency",
    "dependencytelemetry",
    "remotedependencydata",
}


def _first_string(mapping: dict[str, Any], names: tuple[str, ...]) -> str | None:
    for name in names:
        value = mapping.get(name)
        if isinstance(value, str) and value.strip():
            return value
    return None


def _walk(value: Any, container: str = "") -> Iterator[tuple[dict[str, Any], str]]:
    if isinstance(value, list):
        for item in value:
            yield from _walk(item, container)
    elif isinstance(value, dict):
        yield value, container
        for key, child in value.items():
            yield from _walk(child, str(key).casefold())


def inventory_export(document: Any) -> dict[str, Counter[str]]:
    """Collect aggregate names without emitting potentially sensitive attributes."""
    span_names: Counter[str] = Counter()
    dependency_names: Counter[str] = Counter()
    dependency_types: Counter[str] = Counter()
    for mapping, container in _walk(document):
        keys = {str(key).casefold() for key in mapping}
        has_span_identity = bool(
            keys
            & {
                "spanid",
                "span_id",
                "traceid",
                "trace_id",
                "parentspanid",
                "parent_span_id",
            }
        )
        is_span = (
            container in SPAN_CONTAINER_NAMES
            or has_span_identity
            or "spanname" in keys
        )
        is_dependency = (
            container in DEPENDENCY_CONTAINER_NAMES
            or "dependencytype" in keys
            or "dependency_type" in keys
            or (
                isinstance(mapping.get("type"), str)
                and "dependency" in str(mapping["type"]).casefold()
            )
        )
        if is_span:
            name = _first_string(mapping, ("name", "spanName", "span_name", "operationName"))
            if name is not None:
                span_names[name] += 1
        if is_dependency:
            name = _first_string(mapping, ("name", "dependencyName", "dependency_name"))
            dependency_type = _first_string(
                mapping, ("dependencyType", "dependency_type", "type", "kind")
            )
            if name is not None:
                dependency_names[name] += 1
            if dependency_type is not None:
                dependency_types[dependency_type] += 1
    return {
        "span_names": span_names,
        "dependency_names": dependency_names,
        "dependency_types": dependency_types,
    }


def _as_rows(values: Counter[str]) -> list[dict[str, Any]]:
    return [
        {"name": name, "count": count}
        for name, count in sorted(values.items(), key=lambda item: (-item[1], item[0]))
    ]


def _missing(
    expected: list[str], observed: Counter[str], *, ignore_case: bool
) -> list[str]:
    if ignore_case:
        observed_names = {name.casefold() for name in observed}
        return [name for name in expected if name.casefold() not in observed_names]
    return [name for name in expected if name not in observed]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Inventory named spans and dependency types from a sanitized exported JSON "
            "file. This tool performs no network calls and does not read credentials."
        )
    )
    parser.add_argument(
        "export",
        type=Path,
        help="Sanitized local JSON export, such as OTLP resourceSpans or dependency records.",
    )
    parser.add_argument(
        "--expect-span",
        action="append",
        default=[],
        metavar="NAME",
        help="Expected span name; repeat for each required name.",
    )
    parser.add_argument(
        "--expect-dependency-type",
        action="append",
        default=[],
        metavar="TYPE",
        help="Expected dependency type; repeat for each required type.",
    )
    parser.add_argument(
        "--ignore-case",
        action="store_true",
        help="Compare expected names case-insensitively.",
    )
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()

    inventory = inventory_export(load_json(args.export))
    missing_spans = _missing(
        args.expect_span, inventory["span_names"], ignore_case=args.ignore_case
    )
    missing_dependency_types = _missing(
        args.expect_dependency_type,
        inventory["dependency_types"],
        ignore_case=args.ignore_case,
    )
    report = {
        "tool": "inventory_trace_spans",
        "export": str(args.export),
        "valid": not missing_spans and not missing_dependency_types,
        "span_names": _as_rows(inventory["span_names"]),
        "dependency_names": _as_rows(inventory["dependency_names"]),
        "dependency_types": _as_rows(inventory["dependency_types"]),
        "expected": {
            "span_names": args.expect_span,
            "dependency_types": args.expect_dependency_type,
            "missing_span_names": missing_spans,
            "missing_dependency_types": missing_dependency_types,
        },
        "safety": (
            "The inventory is derived only from the supplied local export and reports "
            "aggregate names/types, not trace IDs, attributes, endpoints, or secrets."
        ),
    }
    emit_json(report, args.output)
    if not report["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except EditorialInputError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2) from error
