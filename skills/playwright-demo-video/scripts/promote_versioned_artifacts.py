"""Safely promote explicitly named versioned demo deliverables.

The script only archives existing aliases and copies explicitly named versioned
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
import stat
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from editorial_common import EditorialInputError, emit_json, load_json, require_mapping

SENSITIVE_PATH_TOKENS = {
    ".env",
    "auth",
    "browser",
    "chrome",
    "chromium",
    "cookie",
    "cookies",
    "credential",
    "credentials",
    "firefox",
    "msedge",
    "profile",
    "profiles",
    "safari",
    "secret",
    "secrets",
    "storage",
    "storage-state",
    "token",
    "tokens",
    "user data",
}


@dataclass(frozen=True)
class Artifact:
    source_relative: Path
    alias_relative: Path


@dataclass(frozen=True)
class PromotionPlan:
    version: str
    archive_relative: Path
    artifacts: tuple[Artifact, ...]
    manifest_relative: Path
    checksums_relative: Path


@dataclass
class PendingArtifact:
    artifact: Artifact
    source: Path
    alias: Path
    source_sha256: str
    archive_relative: Path | None
    archive_target: Path | None
    alias_sha256: str | None
    staged: Path | None = None
    archived: bool = False
    published: bool = False


def _is_sensitive_path(path: Path) -> bool:
    return any(
        token in part.casefold()
        for part in path.parts
        for token in SENSITIVE_PATH_TOKENS
    )


def _absolute_without_resolving(path: Path) -> Path:
    return Path(os.path.abspath(str(path.expanduser())))


def _is_unsafe_link(path: Path) -> bool:
    """Treat POSIX links and Windows reparse points as unsafe path traversal."""
    if path.is_symlink():
        return True
    attributes = getattr(path.lstat(), "st_file_attributes", 0)
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _first_symlink_component(path: Path) -> Path | None:
    """Return the first existing symlink in an unresolved path."""
    absolute = _absolute_without_resolving(path)
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current = current / part
        if current.exists() and _is_unsafe_link(current):
            return current
    return None


def _validate_root(delivery_dir: Path) -> Path:
    supplied = _absolute_without_resolving(delivery_dir)
    symlink = _first_symlink_component(supplied)
    if symlink is not None:
        raise EditorialInputError(
            f"delivery directory may not be or traverse a symlink: {symlink}"
        )
    if not supplied.is_dir():
        raise EditorialInputError(
            f"delivery directory must be an existing directory: {supplied}"
        )
    if supplied.parent == supplied:
        raise EditorialInputError("refusing to use a filesystem root as the delivery directory")
    if _is_sensitive_path(supplied):
        raise EditorialInputError(
            "delivery directory must not be a browser/authentication-sensitive path"
        )
    return supplied.resolve()


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
    """Verify a relative path remains below the trusted root without symlinks."""
    if relative.is_absolute() or relative.drive or any(part == ".." for part in relative.parts):
        raise EditorialInputError(f"{field} must remain a simple relative path")
    current = root
    for part in relative.parts:
        current = current / part
        if current.exists() and _is_unsafe_link(current):
            raise EditorialInputError(f"{field} may not traverse symlinks: {relative}")
    candidate = root / relative
    try:
        candidate.resolve(strict=False).relative_to(root)
    except ValueError as error:
        raise EditorialInputError(f"{field} escapes the delivery directory") from error
    return candidate


def _mkdir_under_root(root: Path, relative: Path, field: str) -> Path:
    """Create only the named destination parents, rejecting links and files."""
    _inside_root(root, relative, field)
    current = root
    for part in relative.parts:
        current = current / part
        if current.exists():
            if _is_unsafe_link(current) or not current.is_dir():
                raise EditorialInputError(f"{field} is not a safe directory: {current}")
        else:
            current.mkdir()
            if _is_unsafe_link(current) or not current.is_dir():
                raise EditorialInputError(f"{field} could not create a safe directory: {current}")
    return _inside_root(root, relative, field)


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


def _is_under(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _archive_relative(plan: PromotionPlan, artifact: Artifact) -> Path:
    return (
        plan.archive_relative
        / plan.version
        / "previous"
        / artifact.alias_relative
    )


def _archive_target(root: Path, plan: PromotionPlan, artifact: Artifact) -> Path:
    relative = _archive_relative(plan, artifact)
    return _inside_root(root, relative, f"archive target for {artifact.alias_relative}")


def _validate_regular_file(path: Path, field: str) -> None:
    if not path.is_file() or _is_unsafe_link(path):
        raise EditorialInputError(f"{field} must be an existing non-symlink regular file: {path}")


def validate_plan(document: dict[str, Any], delivery_dir: Path) -> PromotionPlan:
    """Validate every planned action before staging or changing an artifact."""
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
        _validate_regular_file(source, f"{field}.source")
        if alias.exists():
            _validate_regular_file(alias, f"{field}.alias")
        seen_sources.add(source)
        seen_aliases.add(alias)
        artifacts.append(Artifact(source_relative, alias_relative))

    if seen_sources & seen_aliases:
        conflict = next(iter(seen_sources & seen_aliases))
        raise EditorialInputError(
            "a source cannot also be another artifact's alias: "
            f"{conflict.relative_to(root)}"
        )
    for artifact in artifacts:
        source = _inside_root(root, artifact.source_relative, "artifact source")
        alias = _inside_root(root, artifact.alias_relative, "artifact alias")
        if _is_under(source, archive_dir) or _is_under(alias, archive_dir):
            raise EditorialInputError(
                "artifacts may not place a source or alias inside archive_dir: "
                f"{artifact.source_relative} / {artifact.alias_relative}"
            )

    manifest_relative = Path(f"promotion-{version}.manifest.json")
    checksums_relative = Path(f"checksums-{version}.sha256")
    manifest_path = _inside_root(root, manifest_relative, "generated manifest")
    checksums_path = _inside_root(root, checksums_relative, "generated checksums")
    if manifest_path.exists() or checksums_path.exists():
        raise EditorialInputError(
            "refusing to overwrite promotion metadata; choose a new version or archive "
            f"the existing named metadata: {manifest_path.name}, {checksums_path.name}"
        )
    plan = PromotionPlan(
        version=version,
        archive_relative=archive_relative,
        artifacts=tuple(artifacts),
        manifest_relative=manifest_relative,
        checksums_relative=checksums_relative,
    )
    for artifact in artifacts:
        source = _inside_root(root, artifact.source_relative, "artifact source")
        alias = _inside_root(root, artifact.alias_relative, "artifact alias")
        if source in {manifest_path, checksums_path} or alias in {manifest_path, checksums_path}:
            raise EditorialInputError("artifact names may not conflict with generated metadata")
        if alias.exists():
            archive_target = _archive_target(root, plan, artifact)
            if archive_target.exists():
                raise EditorialInputError(
                    "refusing to overwrite an existing named archive target: "
                    f"{archive_target}"
                )
    return plan


def _stage_copy(source: Path, parent: Path, suffix: str, expected_sha256: str) -> Path:
    descriptor, raw_path = tempfile.mkstemp(
        prefix=".demo-video-promotion-", suffix=suffix, dir=parent
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


def _stage_content(parent: Path, suffix: str, content: str) -> Path:
    descriptor, raw_path = tempfile.mkstemp(
        prefix=".demo-video-promotion-", suffix=suffix, dir=parent
    )
    staged = Path(raw_path)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        return staged
    except OSError:
        staged.unlink(missing_ok=True)
        raise


def _link_or_copy_exclusive(source: Path, destination: Path) -> None:
    """Create a destination without replacing an existing file."""
    try:
        os.link(source, destination)
        return
    except FileExistsError as error:
        raise EditorialInputError(
            f"refusing to overwrite existing file: {destination}"
        ) from error
    except OSError:
        pass
    created_destination = False
    try:
        with source.open("rb") as input_handle:
            with destination.open("xb") as output_handle:
                created_destination = True
                shutil.copyfileobj(input_handle, output_handle)
    except FileExistsError as error:
        raise EditorialInputError(
            f"refusing to overwrite existing file: {destination}"
        ) from error
    except OSError as error:
        if created_destination:
            try:
                destination.unlink()
            except OSError as cleanup_error:
                raise EditorialInputError(
                    f"failed to create {destination}; temporary partial file could not be "
                    f"removed: {cleanup_error}"
                ) from error
        raise EditorialInputError(f"failed to create {destination}: {error}") from error


def _remove_expected(path: Path, expected_sha256: str, label: str) -> None:
    """Remove only a regular file this run can prove it created."""
    _validate_regular_file(path, label)
    if _sha256(path) != expected_sha256:
        raise EditorialInputError(
            f"refusing to remove {label}; its checksum changed during promotion: {path}"
        )
    path.unlink()


def _archive_named_alias(alias: Path, archive_target: Path, expected_sha256: str) -> None:
    """Move a named alias by creating a verified archive before removing it."""
    _link_or_copy_exclusive(alias, archive_target)
    try:
        if _sha256(archive_target) != expected_sha256:
            raise EditorialInputError(
                f"archive checksum does not match alias: {alias.name}"
            )
        alias.unlink()
    except (EditorialInputError, OSError):
        if (
            alias.is_file()
            and not _is_unsafe_link(alias)
            and archive_target.is_file()
            and not _is_unsafe_link(archive_target)
            and _sha256(alias) == expected_sha256
            and _sha256(archive_target) == expected_sha256
        ):
            archive_target.unlink()
        raise


def _publish_staged_alias(staged: Path, alias: Path, expected_sha256: str) -> None:
    """Publish a staged copy without replacing an alias created by another process."""
    _link_or_copy_exclusive(staged, alias)
    try:
        if _sha256(alias) != expected_sha256:
            raise EditorialInputError(f"promoted alias checksum mismatch: {alias.name}")
    except (EditorialInputError, OSError):
        if alias.is_file() and not _is_unsafe_link(alias) and _sha256(alias) == expected_sha256:
            alias.unlink()
        raise


def _rollback(
    pending: list[PendingArtifact],
    published_metadata: list[tuple[Path, str]],
) -> list[str]:
    """Restore known aliases in reverse order after a failed promotion."""
    rollback_errors: list[str] = []
    for path, checksum in reversed(published_metadata):
        try:
            _remove_expected(path, checksum, "generated promotion metadata")
        except EditorialInputError as error:
            rollback_errors.append(str(error))
    for item in reversed(pending):
        try:
            if item.published:
                _remove_expected(item.alias, item.source_sha256, "generated delivery alias")
                item.published = False
            if item.archived:
                if (
                    item.archive_target is None
                    or item.alias_sha256 is None
                    or item.alias.exists()
                ):
                    raise EditorialInputError(
                        f"cannot safely restore archived alias: {item.artifact.alias_relative}"
                    )
                _link_or_copy_exclusive(item.archive_target, item.alias)
                if _sha256(item.alias) != item.alias_sha256:
                    raise EditorialInputError(
                        f"restored alias checksum mismatch: {item.artifact.alias_relative}"
                    )
                _remove_expected(
                    item.archive_target,
                    item.alias_sha256,
                    "generated archive entry",
                )
                item.archived = False
        except (EditorialInputError, OSError) as error:
            rollback_errors.append(str(error))
    return rollback_errors


def _inspect_pending(plan: PromotionPlan, root: Path) -> list[PendingArtifact]:
    """Re-check every named path without creating files or directories."""
    manifest_path = _inside_root(root, plan.manifest_relative, "generated manifest")
    checksums_path = _inside_root(root, plan.checksums_relative, "generated checksums")
    if manifest_path.exists() or checksums_path.exists():
        raise EditorialInputError("promotion metadata appeared after plan validation")

    pending: list[PendingArtifact] = []
    for artifact in plan.artifacts:
        source = _inside_root(root, artifact.source_relative, "artifact source")
        alias = _inside_root(root, artifact.alias_relative, "artifact alias")
        _validate_regular_file(source, f"versioned source {artifact.source_relative}")
        if alias.exists():
            _validate_regular_file(alias, f"existing alias {artifact.alias_relative}")
            archive_relative = _archive_relative(plan, artifact)
            archive_target = _archive_target(root, plan, artifact)
            if archive_target.exists():
                raise EditorialInputError(
                    "archive target appeared after plan validation: "
                    f"{archive_relative}"
                )
            alias_sha256 = _sha256(alias)
        else:
            archive_relative = None
            archive_target = None
            alias_sha256 = None
        pending.append(
            PendingArtifact(
                artifact=artifact,
                source=source,
                alias=alias,
                source_sha256=_sha256(source),
                archive_relative=archive_relative,
                archive_target=archive_target,
                alias_sha256=alias_sha256,
            )
        )
    return pending


def _stage_pending(root: Path, pending: list[PendingArtifact]) -> None:
    """Stage all source copies after all read-only preflight checks pass."""
    try:
        for item in pending:
            source = _inside_root(root, item.artifact.source_relative, "artifact source")
            alias = _inside_root(root, item.artifact.alias_relative, "artifact alias")
            _validate_regular_file(source, f"versioned source {item.artifact.source_relative}")
            if item.archive_target is None and alias.exists():
                raise EditorialInputError(
                    f"alias appeared after plan validation: {item.artifact.alias_relative}"
                )
            if item.archive_target is not None:
                _validate_regular_file(alias, f"existing alias {item.artifact.alias_relative}")
                if _sha256(alias) != item.alias_sha256:
                    raise EditorialInputError(
                        f"existing alias changed after plan validation: {item.artifact.alias_relative}"
                    )
            parent = _mkdir_under_root(
                root,
                item.artifact.alias_relative.parent,
                f"parent for {item.artifact.alias_relative}",
            )
            item.source = source
            item.alias = _inside_root(root, item.artifact.alias_relative, "artifact alias")
            item.staged = _stage_copy(
                source, parent, item.alias.suffix, item.source_sha256
            )
    except (EditorialInputError, OSError):
        for item in pending:
            if item.staged is not None:
                item.staged.unlink(missing_ok=True)
        raise


def promote(plan: PromotionPlan, delivery_dir: Path) -> dict[str, Any]:
    """Archive aliases, promote a complete named set, or roll all known changes back."""
    root = _validate_root(delivery_dir)
    pending = _inspect_pending(plan, root)
    _stage_pending(root, pending)
    staged_files = [item.staged for item in pending if item.staged is not None]
    published_metadata: list[tuple[Path, str]] = []
    try:
        manifest_path = _inside_root(root, plan.manifest_relative, "generated manifest")
        checksums_path = _inside_root(root, plan.checksums_relative, "generated checksums")
        archived = [
            {
                "alias": str(item.artifact.alias_relative),
                "archived_to": str(item.archive_relative),
            }
            for item in pending
            if item.archive_relative is not None
        ]
        promoted = [
            {
                "source": str(item.artifact.source_relative),
                "alias": str(item.artifact.alias_relative),
                "sha256": item.source_sha256,
            }
            for item in pending
        ]
        manifest = {
            "tool": "promote_versioned_artifacts",
            "version": plan.version,
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "archived": archived,
            "artifacts": promoted,
        }
        root_parent = _mkdir_under_root(root, Path(), "delivery directory")
        staged_manifest = _stage_content(
            root_parent,
            ".manifest.json",
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        )
        staged_files.append(staged_manifest)
        staged_checksums = _stage_content(
            root_parent,
            ".sha256",
            "".join(f"{item['sha256']}  {item['alias']}\n" for item in promoted),
        )
        staged_files.append(staged_checksums)
        for item in pending:
            if item.archive_target is not None:
                if item.archive_relative is None:
                    raise EditorialInputError(
                        f"missing archive relative path: {item.artifact.alias_relative}"
                    )
                archive_parent = _mkdir_under_root(
                    root,
                    item.archive_relative.parent,
                    f"parent for archive {item.artifact.alias_relative}",
                )
                archive_target = _inside_root(
                    root,
                    item.archive_relative,
                    f"archive target for {item.artifact.alias_relative}",
                )
                if (
                    archive_target != item.archive_target
                    or archive_target.exists()
                    or not item.alias.exists()
                    or item.alias_sha256 is None
                ):
                    raise EditorialInputError(
                        "refusing to overwrite or race an alias/archive target: "
                        f"{item.artifact.alias_relative}"
                    )
                if archive_parent != archive_target.parent:
                    raise EditorialInputError(
                        f"archive target parent changed during promotion: {archive_target}"
                    )
                _archive_named_alias(item.alias, archive_target, item.alias_sha256)
                item.archived = True
            if item.alias.exists():
                raise EditorialInputError(
                    f"refusing to overwrite alias created during promotion: {item.alias}"
                )
            if item.staged is None:
                raise EditorialInputError(
                    f"missing staged artifact: {item.artifact.source_relative}"
                )
            _publish_staged_alias(item.staged, item.alias, item.source_sha256)
            item.published = True

        _inside_root(root, plan.manifest_relative, "generated manifest")
        _inside_root(root, plan.checksums_relative, "generated checksums")
        _publish_staged_alias(staged_manifest, manifest_path, _sha256(staged_manifest))
        published_metadata.append((manifest_path, _sha256(staged_manifest)))
        _publish_staged_alias(staged_checksums, checksums_path, _sha256(staged_checksums))
        published_metadata.append((checksums_path, _sha256(staged_checksums)))
    except (EditorialInputError, OSError) as error:
        rollback_errors = _rollback(pending, published_metadata)
        if rollback_errors:
            raise EditorialInputError(
                f"{error}; rollback needs attention: {'; '.join(rollback_errors)}"
            ) from error
        raise
    finally:
        for staged in staged_files:
            staged.unlink(missing_ok=True)

    return {
        "tool": "promote_versioned_artifacts",
        "dry_run": False,
        "valid": True,
        "version": plan.version,
        "archived": archived,
        "promoted": promoted,
        "manifest": str(plan.manifest_relative),
        "checksums": str(plan.checksums_relative),
    }


def preview(plan: PromotionPlan, delivery_dir: Path) -> dict[str, Any]:
    """Describe the exact named files that --apply would change."""
    root = _validate_root(delivery_dir)
    pending = _inspect_pending(plan, root)
    archived = [
        {
            "alias": str(item.artifact.alias_relative),
            "archived_to": str(item.archive_relative),
        }
        for item in pending
        if item.archive_relative is not None
    ]
    promoted = [
        {
            "source": str(item.artifact.source_relative),
            "alias": str(item.artifact.alias_relative),
            "sha256": item.source_sha256,
        }
        for item in pending
    ]
    return {
        "tool": "promote_versioned_artifacts",
        "dry_run": True,
        "valid": True,
        "version": plan.version,
        "archived": archived,
        "promoted": promoted,
        "manifest": str(plan.manifest_relative),
        "checksums": str(plan.checksums_relative),
        "safety": (
            "No delivery files were changed. --apply stages the listed sources, then "
            "either promotes the complete named set and its metadata or rolls known "
            "changes back without overwriting another file."
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
