"""Focused tests for deterministic demo-video editorial QA logic."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from check_narration_gaps import check_narration_gaps
from detect_static_waits import detect_static_regions, normalized_difference
from extract_scene_qc import plan_qc_frames
from inventory_trace_spans import inventory_export
from promote_versioned_artifacts import preview, promote, validate_plan
from validate_claim_evidence import validate_manifest
from validate_continuity import validate_continuity


def example_manifest() -> dict[str, object]:
    return json.loads(
        (SKILL_DIR / "examples" / "claim-evidence-manifest.json").read_text(
            encoding="utf-8"
        )
    )


class ClaimEvidenceTests(unittest.TestCase):
    def test_example_manifest_is_valid_for_pre_capture_review(self) -> None:
        report = validate_manifest(
            example_manifest(),
            SKILL_DIR,
            allow_missing_files=True,
            min_completion_hold=3.0,
            max_completion_hold=5.0,
        )
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["checked"], {"chapters": 2, "scenes": 2})

    def test_completion_claim_requires_readable_hold_before_narration(self) -> None:
        manifest = example_manifest()
        narration = manifest["chapters"][0]["scenes"][0]["narration"]
        narration["visible_hold_seconds"] = 1.0
        report = validate_manifest(
            manifest,
            SKILL_DIR,
            allow_missing_files=True,
            min_completion_hold=3.0,
            max_completion_hold=5.0,
        )
        self.assertFalse(report["valid"])
        self.assertTrue(
            any("visible_hold_seconds" in issue["path"] for issue in report["errors"])
        )


class NarrationAndFramePlanningTests(unittest.TestCase):
    def test_detects_overlap_and_short_gap(self) -> None:
        report = check_narration_gaps(
            [
                {"id": "opening", "start_seconds": 0.0, "end_seconds": 2.0},
                {"id": "tight", "start_seconds": 2.4, "end_seconds": 3.0},
                {"id": "overlap", "start_seconds": 2.9, "end_seconds": 4.0},
            ],
            0.8,
        )
        self.assertFalse(report["valid"])
        self.assertEqual(
            {diagnostic["kind"] for diagnostic in report["diagnostics"]},
            {"short-gap", "overlap"},
        )

    def test_detects_overlap_with_longer_earlier_narration(self) -> None:
        report = check_narration_gaps(
            [
                {"id": "long", "start_seconds": 0.0, "end_seconds": 10.0},
                {"id": "nested-one", "start_seconds": 1.0, "end_seconds": 2.0},
                {"id": "nested-two", "start_seconds": 3.0, "end_seconds": 4.0},
            ],
            0.8,
        )
        overlaps = [
            diagnostic for diagnostic in report["diagnostics"] if diagnostic["kind"] == "overlap"
        ]
        self.assertEqual({diagnostic["current"] for diagnostic in overlaps}, {"nested-one", "nested-two"})
        self.assertTrue(all(diagnostic["previous"] == "long" for diagnostic in overlaps))

    def test_qc_plan_covers_claims_evidence_midpoints_and_transitions(self) -> None:
        planned = plan_qc_frames(example_manifest(), 0.25)
        kinds = {point["kind"] for point in planned}
        self.assertTrue(
            {"midpoint", "evidence", "claim", "transition-before", "transition-after"}
            <= kinds
        )
        self.assertTrue(
            any(
                point["scene_id"] == "request-completed"
                and point["kind"] == "claim"
                and point["timestamp_seconds"] == 10.5
                for point in planned
            )
        )


class StaticWaitTests(unittest.TestCase):
    def test_difference_and_static_region_grouping(self) -> None:
        self.assertEqual(normalized_difference(b"\x00\xff", b"\x00\x00"), 0.5)
        regions = detect_static_regions(
            [0.0, 0.001, 0.002, 0.0, 0.0, 0.0, 0.1],
            interval=0.5,
            threshold=0.005,
            minimum_duration=2.0,
        )
        self.assertEqual(len(regions), 1)
        self.assertEqual(regions[0]["start_seconds"], 0.0)
        self.assertEqual(regions[0]["duration_seconds"], 3.0)


class ContinuityAndInventoryTests(unittest.TestCase):
    def test_identity_and_aliases_are_checked_separately(self) -> None:
        manifest = example_manifest()
        good = validate_continuity(manifest)
        self.assertTrue(good["valid"], good["errors"])
        self.assertTrue(good["warnings"])

        manifest["chapters"][1]["scenes"][0]["continuity"]["after"]["identity"][
            "value"
        ] = "session-demo-999"
        bad = validate_continuity(manifest)
        self.assertFalse(bad["valid"])
        self.assertTrue(
            any("identity continuity failed" in issue["message"] for issue in bad["errors"])
        )

    def test_inventory_counts_otlp_spans_and_dependencies(self) -> None:
        trace_export = json.loads(
            (SKILL_DIR / "examples" / "trace-export.json").read_text(encoding="utf-8")
        )
        inventory = inventory_export(trace_export)
        self.assertEqual(inventory["span_names"]["demo.request"], 1)
        self.assertEqual(inventory["span_names"]["demo.resume"], 1)
        self.assertEqual(inventory["dependency_types"]["HTTP"], 1)


class ArtifactPromotionTests(unittest.TestCase):
    def test_promotes_named_versioned_artifacts_and_archives_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "demo-v2.mp4").write_bytes(b"new video")
            (root / "demo-v2.manifest.json").write_text('{"version":"v2"}\n')
            (root / "demo-latest.mp4").write_bytes(b"old video")
            (root / "demo-latest.manifest.json").write_text('{"version":"v1"}\n')
            document = {
                "version": "v2",
                "artifacts": [
                    {"source": "demo-v2.mp4", "alias": "demo-latest.mp4"},
                    {
                        "source": "demo-v2.manifest.json",
                        "alias": "demo-latest.manifest.json",
                    },
                ],
            }
            plan = validate_plan(document, root)
            self.assertTrue(preview(plan, root)["dry_run"])
            report = promote(plan, root)

            self.assertTrue(report["valid"])
            self.assertEqual((root / "demo-latest.mp4").read_bytes(), b"new video")
            self.assertEqual(
                (root / "archive" / "v2" / "previous" / "demo-latest.mp4").read_bytes(),
                b"old video",
            )
            self.assertTrue((root / "promotion-v2.manifest.json").is_file())
            self.assertTrue((root / "checksums-v2.sha256").is_file())

    def test_rejects_sensitive_or_escaping_artifact_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "demo-v2.mp4").write_bytes(b"new video")
            with self.assertRaisesRegex(ValueError, "sensitive"):
                validate_plan(
                    {
                        "version": "v2",
                        "artifacts": [
                            {
                                "source": "demo-v2.mp4",
                                "alias": "storage-state.json",
                            }
                        ],
                    },
                    root,
                )

    def test_rejects_source_that_is_another_alias(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "demo-v2.mp4").write_bytes(b"versioned source")
            (root / "demo-v2.manifest.json").write_text("{}\n")
            with self.assertRaisesRegex(ValueError, "another artifact's alias"):
                validate_plan(
                    {
                        "version": "v2",
                        "artifacts": [
                            {"source": "demo-v2.mp4", "alias": "demo-v2.manifest.json"},
                            {
                                "source": "demo-v2.manifest.json",
                                "alias": "demo-latest.manifest.json",
                            },
                        ],
                    },
                    root,
                )
            with self.assertRaisesRegex(ValueError, "without '..'"):
                validate_plan(
                    {
                        "version": "v2",
                        "artifacts": [
                            {"source": "demo-v2.mp4", "alias": "../demo-latest.mp4"}
                        ],
                    },
                    root,
                )


if __name__ == "__main__":
    unittest.main()
