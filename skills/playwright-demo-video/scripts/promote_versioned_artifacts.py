"""Safely promote explicitly named versioned demo deliverables.

The script only moves existing aliases and copies explicitly named versioned
files below an explicit delivery directory. It never scans, deletes, or touches
browser profiles, storage state, credentials, or paths outside that directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from editorial_common import EditorialInputError, emit_json, load_json, require_mapping

SENSITIVE_PATH_TOKENS = {
    "auth",
    "browser",
    "cookie",
    "cookies",
    "credential",
    "credentials",
    "profile",
    "profiles",
    "secret",
    "secrets",
    "storage",
    "storage-state",
    "token",
    "tokens",
    ".env",
}


@dataclass(frozen=True)
class Artifact:
    source: Path
    alias: Path


@dataclass(frozen=True)
class PromotionPlan:
    version: str
    archive_dir: Path
    artifacts: tuple[Artifact, ...]
    manifest_path: Path
    checksums_path: Path


def _is_sensitive_path(path: Path) -> bool:
    return any(
        token in part.casefold()
        for part in path.parts
        for token in SENSITIVE_PATH_TOKENS
    )


def _validate_root(delivery_dir: Path) -> Path:
    root = delivery_dir.resolve()
    if not root.is_dir():
        raise EditorialInputError(f"delivery directory must be an existing directory: {root}")
    if root.parent == root:
        raise EditorialInputError("refusing to use a filesystem root as the delivery directory")
    if root.is_symlink() or _is_sensitive_path(root):
        raise EditorialInputError(
            "delivery directory must not be a symlink or a browser/authentication-sensitive path"
        )
    return root


def _safe_relative(value: Any, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise EditorialInputError(f"{field} must be a non-empty relative path")
    path = Path(value)
    if path.is_absolute() or path.drive or any(part in {"", ".", ".."} for part in path.parts):
        raise EditorialInputError(f"{field} must be a simple relative path without '..': {value!r}")
    if _is_sensitive_path(path):
        raise EditorialInputError(
            f"{field} is not allowed to reference browser/authentication-sensitive data: {value!r}"
        )
    return path


def _inside_root(root: Path, relative: Path, field: str) -> Path:
    candidate = (root / relative).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise EditorialInputError(f"{field} escapes the delivery directory") from error
    current = root
    for part in relative.parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise EditorialInputError(f"{field} may not traverse symlinks: {relative}")
    return candidate


def _versioned_filename(filename: str, version: str) -> bool:
    return bool(
        re.search(
            rf"(^|[._-]){re.escape(version)}(?=$|[._-])",
            filename,
            flags=re.IGNORECASE,
        )
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_plan(document: dict[str, Any], delivery_dir: Path) -> PromotionPlan:
    """Validate every action before moving or copying a single artifact."""
    root = _validate_root(delivery_dir)
    version = document.get("version")
    if not isinstance(version, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", version):
        raise EditorialInputError(
            "plan.version must use only letters, numbers, dots, underscores, and hyphens"
        )
    archive_relative = _safe_relative(document.get("archive_dir", "archive"), "archive_dir")
    archive_dir = _inside_root(root, archive_relative, "archive_dir")
    raw_artifacts = document.get("artifacts")
    if not isinstance(raw_artifacts, list) or not raw_artifacts:
        raise EditorialInputError("plan.artifacts must be a non-empty array")

    artifacts: list[Artifact] = []
    seen_aliases: set[Path] = set()
    seen_sources: set[Path] = set()
    for index, raw_artifact in enumerate(raw_artifacts):
        field = f"artifacts[{index}]"
        artifact = require_mapping(raw_artifact, field)
        source_relative = _safe_relative(artifact.get("source"), f"{field}.source")
        alias_relative = _safe_relative(artifact.get("alias"), f"{field}.alias")
        source = _inside_root(root, source_relative, f"{field}.source")
        alias = _inside_root(root, alias_relative, f"{field}.alias")
        if not _versioned_filename(source.name, version):
            raise EditorialInputError(
                f"{field}.source must contain version {version!r} as a filename token"
            )
        if source == alias:
            raise EditorialInputError(f"{field}.source and alias cannot be the same path")
        if source in seen_sources:
            raise EditorialInputError(f"{field}.source is repeated: {source_relative}")
        if alias in seen_aliases:
            raise EditorialInputError(f"{field}.alias is repeated: {alias_relative}")
        if not source.is_file() or source.is_symlink():
            raise EditorialInputError(
                f"{field}.source must be an existing non-symlink regular file: {source_relative}"
            )
        if alias.exists() and (not alias.is_file() or alias.is_symlink()):
            raise EditorialInputError(
                f"{field}.alias must be absent or a non-symlink regular file: {alias_relative}"
            )
        seen_sources.add(source)
        seen_aliases.add(alias)
        artifacts.append(Artifact(source=source, alias=alias))

    if seen_sources & seen_aliases:
        conflict = next(iter(seen_sources & seen_aliases))
        raise EditorialInputError(
            "a source cannot also be another artifact's alias: "
            f"{conflict.relative_to(root)}"
        )
    for artifact in artifacts:
        for field, path in (("source", artifact.source), ("alias", artifact.alias)):
            try:
                path.relative_to(archive_dir)
            except ValueError:
                continue
            raise EditorialInputError(
                f"artifacts may not place a {field} inside archive_dir: "
                f"{path.relative_to(root)}"
            )

    manifest_path = _inside_root(
        root, Path(f"promotion-{version}.manifest.json"), "generated manifest"
    )
    checksums_path = _inside_root(
        root, Path(f"checksums-{version}.sha256"), "generated checksums"
    )
    if manifest_path.exists() or checksums_path.exists():
        raise EditorialInputError(
            "refusing to overwrite promotion metadata; choose a new version or archive "
            f"the existing named metadata: {manifest_path.name}, {checksums_path.name}"
        )
    for artifact in artifacts:
        if artifact.source in {manifest_path, checksums_path} or artifact.alias in {
            manifest_path,
            checksums_path,
        }:
            raise EditorialInputError("artifact names may not conflict with generated metadata")
        if artifact.alias.exists():
            archive_target = archive_dir / version / "previous" / artifact.alias.relative_to(root)
            if archive_target.exists():
                raise EditorialInputError(
                    "refusing to overwrite an existing named archive target: "
                    f"{archive_target}"
                )
    return PromotionPlan(
        version=version,
        archive_dir=archive_dir,
        artifacts=tuple(artifacts),
        manifest_path=manifest_path,
        checksums_path=checksums_path,
    )


def _stage_copy(source: Path, alias: Path, expected_sha256: str) -> Path:
    alias.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw_path = tempfile.mkstemp(
        prefix=".demo-video-promotion-", suffix=alias.suffix, dir=alias.parent
    )
    os.close(descriptor)
    staged = Path(raw_path)
    try:
        shutil.copy2(source, staged)
        if _sha256(staged) != expected_sha256:
            raise EditorialInputError(f"staged checksum does not match source: {source.name}")
        return staged
    except (EditorialInputError, OSError):
        staged.unlink(missing_ok=True)
        raise


def _link_or_copy_exclusive(source: Path, destination: Path) -> None:
    """Create a destination without replacing any existing file.

    A hard link is atomic and avoids a second data copy on supported local file
    systems. The exclusive-copy fallback keeps the same no-overwrite property
    when hard links are unavailable.
    """
    try:
        os.link(source, destination)
        return
    except FileExistsError as error:
        raise EditorialInputError(
            f"refusing to overwrite existing file: {destination}"
        ) from error
    except OSError:
        pass
    try:
        with source.open("rb") as input_handle, destination.open("xb") as output_handle:
            shutil.copyfileobj(input_handle, output_handle)
    except FileExistsError as error:
        raise EditorialInputError(
            f"refusing to overwrite existing file: {destination}"
        ) from error


def _archive_named_alias(alias: Path, archive_target: Path, expected_sha256: str) -> None:
    """Archive a known alias without replacing either path."""
    _link_or_copy_exclusive(alias, archive_target)
    if _sha256(archive_target) != expected_sha256:
        raise EditorialInputError(f"archive checksum does not match alias: {alias.name}")
    alias.unlink()


def _publish_staged_alias(staged: Path, alias: Path, expected_sha256: str) -> None:
    """Publish a staged copy without replacing an alias created by another process."""
    _link_or_copy_exclusive(staged, alias)
    if _sha256(alias) != expected_sha256:
        raise EditorialInputError(f"promoted alias checksum mismatch: {alias.name}")


def _write_new_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    except FileExistsError as error:
        raise EditorialInputError(f"refusing to overwrite existing file: {path}") from error


def promote(plan: PromotionPlan, delivery_dir: Path) -> dict[str, Any]:
    """Archive named existing aliases, promote staged copies, and verify SHA-256 aliases."""
    root = _validate_root(delivery_dir)
    for artifact in plan.artifacts:
        if not artifact.source.is_file() or artifact.source.is_symlink():
            raise EditorialInputError(
                "versioned source changed after preflight and is no longer a safe regular "
                f"file: {artifact.source.relative_to(root)}"
            )
    source_hashes = {artifact.source: _sha256(artifact.source) for artifact in plan.artifacts}
    archive_targets: dict[Path, tuple[Path, str]] = {}
    for artifact in plan.artifacts:
        if artifact.alias.exists():
            archive_target = (
                plan.archive_dir
                / plan.version
                / "previous"
                / artifact.alias.relative_to(root)
            )
            archive_targets[artifact.alias] = (archive_target, _sha256(artifact.alias))

    staged: list[tuple[Artifact, Path]] = []
    archived: list[dict[str, str]] = []
    promoted: list[dict[str, str]] = []
    try:
        for artifact in plan.artifacts:
            staged.append(
                (artifact, _stage_copy(artifact.source, artifact.alias, source_hashes[artifact.source]))
            )

        for artifact, staged_path in staged:
            archive = archive_targets.get(artifact.alias)
            if archive is not None:
                archive_target, alias_sha256 = archive
                archive_target.parent.mkdir(parents=True, exist_ok=True)
                if archive_target.exists() or not artifact.alias.exists():
                    raise EditorialInputError(
                        "refusing to overwrite or race an alias/archive target: "
                        f"{artifact.alias}"
                    )
                _archive_named_alias(artifact.alias, archive_target, alias_sha256)
                archived.append(
                    {
                        "alias": str(artifact.alias.relative_to(root)),
                        "archived_to": str(archive_target.relative_to(root)),
                    }
                )
            if artifact.alias.exists():
                raise EditorialInputError(
                    f"refusing to overwrite alias created during promotion: {artifact.alias}"
                )
            try:
                _publish_staged_alias(
                    staged_path, artifact.alias, source_hashes[artifact.source]
                )
            except (EditorialInputError, OSError):
                if archive is not None and archive_target.exists() and not artifact.alias.exists():
                    _link_or_copy_exclusive(archive_target, artifact.alias)
                raise
            promoted.append(
                {
                    "source": str(artifact.source.relative_to(root)),
                    "alias": str(artifact.alias.relative_to(root)),
                    "sha256": source_hashes[artifact.source],
                }
            )
        created_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        manifest = {
            "tool": "promote_versioned_artifacts",
            "version": plan.version,
            "created_at": created_at,
            "archived": archived,
            "artifacts": promoted,
        }
        _write_new_file(
            plan.manifest_path, json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        )
        _write_new_file(
            plan.checksums_path,
            "".join(
                f"{artifact['sha256']}  {artifact['alias']}\n" for artifact in promoted
            ),
        )
        return {
            "tool": "promote_versioned_artifacts",
            "dry_run": False,
            "valid": True,
            "version": plan.version,
            "archived": archived,
            "promoted": promoted,
            "manifest": str(plan.manifest_path.relative_to(root)),
            "checksums": str(plan.checksums_path.relative_to(root)),
        }
    finally:
        for _artifact, staged_path in staged:
            staged_path.unlink(missing_ok=True)


def preview(plan: PromotionPlan, delivery_dir: Path) -> dict[str, Any]:
    """Describe the exact named files that --apply would change."""
    root = _validate_root(delivery_dir)
    archived = []
    promoted = []
    for artifact in plan.artifacts:
        if artifact.alias.exists():
            archived.append(
                {
                    "alias": str(artifact.alias.relative_to(root)),
                    "archived_to": str(
                        (
                            plan.archive_dir
                            / plan.version
                            / "previous"
                            / artifact.alias.relative_to(root)
                        ).relative_to(root)
                    ),
                }
            )
        promoted.append(
            {
                "source": str(artifact.source.relative_to(root)),
                "alias": str(artifact.alias.relative_to(root)),
                "sha256": _sha256(artifact.source),
            }
        )
    return {
        "tool": "promote_versioned_artifacts",
        "dry_run": True,
        "valid": True,
        "version": plan.version,
        "archived": archived,
        "promoted": promoted,
        "manifest": str(plan.manifest_path.relative_to(root)),
        "checksums": str(plan.checksums_path.relative_to(root)),
        "safety": (
            "No files were changed. --apply only moves the listed existing aliases, "
            "copies the listed versioned files, and writes the two named metadata files."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Safely archive known aliases and promote explicit versioned demo artifacts. "
            "Dry-run is the default; pass --apply after reviewing the JSON preview."
        )
    )
    parser.add_argument("plan", type=Path, help="Promotion plan JSON")
    parser.add_argument(
        "--delivery-dir",
        type=Path,
        required=True,
        help="Existing non-sensitive delivery directory containing every named artifact.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Perform the reviewed archive/copy operation; otherwise emit only a preview.",
    )
    args = parser.parse_args()

    document = require_mapping(load_json(args.plan), "promotion plan")
    plan = validate_plan(document, args.delivery_dir)
    report = promote(plan, args.delivery_dir) if args.apply else preview(plan, args.delivery_dir)
    emit_json(report)


if __name__ == "__main__":
    try:
        main()
    except EditorialInputError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2) from error
