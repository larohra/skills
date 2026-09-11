# Automated editorial QC

The scripts in this reference make repeated checks cheap and consistent. They
produce JSON for records and automation, but they do not replace a reviewer
watching the demo. Run `python .\scripts\<name>.py --help` for the current
arguments and write all generated files outside the repository with the raw
media.

The Python QA tools are cross-platform when Python 3.9+ and (for video
operations) FFmpeg/FFprobe are on `PATH`. Examples use Windows PowerShell because the
existing narration/prerequisite workflow is Windows-oriented; on macOS/Linux,
use the same arguments with forward-slash paths and the local Python command.

## Keep media and editorial inputs separate

`claim-evidence.json` drives only the new editorial validators and frame
extractor. The existing `stitch_clips.py` and `mix_audio_overlays.py` retain
their separate inputs, respectively `clips.json` and `mix.json`; examples for
both live in `examples/`. By default, the claim contract's `video.source`
points to the intended delivery candidate or another existing reviewable cut.
Point it to a silent master only when the user requested that separate
artifact; never point it to a raw-clip or mix manifest itself.

## Typical final-QC sequence

```powershell
# Only when the user explicitly requests a silent master, use the existing
# clip manifest. Do not pass claim-evidence.json to stitch_clips.py.
# python .\scripts\stitch_clips.py .\clips.json .\deliverables\demo-silent-v1.mp4
# Otherwise do not create this file; set claim-evidence.json video.source to
# the intended delivery candidate or another existing reviewable cut.

# Validate the plan before capture. Placeholder frames are acceptable here.
python .\scripts\validate_claim_evidence.py .\claim-evidence.json --allow-missing-files
python .\scripts\validate_continuity.py .\claim-evidence.json

# Confirm actual telemetry vocabulary before writing trace narration.
python .\scripts\inventory_trace_spans.py .\sanitized-trace-export.json `
  --expect-span "demo.request" --expect-dependency-type HTTP

# Inspect every planned proof point from the approved review source.
python .\scripts\extract_scene_qc.py .\claim-evidence.json .\qc
python .\scripts\validate_claim_evidence.py .\claim-evidence.json `
  --frame-index .\qc\index.json
python .\scripts\check_narration_gaps.py .\claim-evidence.json --minimum-gap 0.8
python .\scripts\detect_static_waits.py .\deliverables\demo-v1.mp4 `
  --output .\qc\static-waits.json

# After timing/narration approval, use the existing mix input format.
python .\scripts\mix_audio_overlays.py .\mix.json

# Review the promotion preview before making the delivery aliases.
python .\scripts\promote_versioned_artifacts.py .\promotion-plan.json `
  --delivery-dir .\deliverables
python .\scripts\promote_versioned_artifacts.py .\promotion-plan.json `
  --delivery-dir .\deliverables --apply
```

`extract_scene_qc.py` writes `index.json`, exact midpoint/evidence/claim and
transition frames in `frames/`, and a contact sheet when FFmpeg can tile the
frames. It samples immediately before and after each declared transition so a
short, visually jarring cut is not hidden by a coarse periodic contact sheet.
Use `--dry-run` to review planned timestamps without running FFmpeg.

## Claim evidence and continuity

| Tool | Input | Output and failure behavior |
| --- | --- | --- |
| `validate_claim_evidence.py` | `claim-evidence.json`; optional final frame index | JSON report with missing fields, files, marker declarations, and completion-hold violations. A supplied index must be non-dry-run and every credited frame must exist. |
| `validate_continuity.py` | `claim-evidence.json` | JSON report that checks durable identity separately from declared aliases. Fails for identity/alias mismatches, unknown linked evidence-shot IDs, reused before/after frames, or reverse evidence timing. |
| `check_narration_gaps.py` | `narration_schedule` JSON or scene narration in the manifest | JSON schedule ordered by time plus overlap and minimum-gap diagnostics. Nonzero exit for every overlap or short gap; default minimum is 0.8 seconds. |

The example manifest documents the shared schema. A standalone retimed schedule
can be as small as:

```json
{
  "narration_schedule": [
    {"id": "opening", "start_seconds": 0.0, "end_seconds": 3.2},
    {"id": "outcome", "start_seconds": 4.1, "end_seconds": 7.4}
  ]
}
```

All machine checks validate declared artifacts and metadata. They cannot prove
that a frame's pixels are truthful or that a clipped UI reflects the whole
system, so retain the visual and editorial review gate.

For example, a passing narration report has a compact, machine-readable shape:

```json
{
  "tool": "check_narration_gaps",
  "valid": true,
  "minimum_gap_seconds": 0.8,
  "entries_checked": 2,
  "diagnostics": []
}
```

The QC extraction index uses the same style and maps every generated frame back
to a scene, timestamp, and reason:

```json
{
  "id": "qc-0003",
  "scene_id": "session-resumes",
  "kind": "claim",
  "timestamp_seconds": 24.8,
  "file": "frames/qc-0003.png"
}
```

## Video pacing

`detect_static_waits.py` samples the input with FFmpeg at a small grayscale
resolution, calculates mean frame-to-frame differences, and groups long runs
under a configurable threshold. It reports likely static regions but exits
successfully by default:

```powershell
python .\scripts\detect_static_waits.py .\demo-v1.mp4 `
  --interval 0.5 --threshold 0.005 --minimum-duration 3
```

Use `--fail-on-static` only in a deliberate release gate after tuning the
threshold for the product. A useful, readable completion hold can look static;
tiny animations can hide an unwanted wait; and pixel similarity says nothing
about product progress. The report states these limitations and can include
raw sample differences with `--include-samples`.

## Telemetry inventory

`inventory_trace_spans.py` accepts only a local structured export such as
OTLP-style `resourceSpans` JSON or an exported dependency list. It makes no
network calls, accepts no endpoint or credential arguments, and outputs only
aggregated span names and dependency names/types:

```powershell
python .\scripts\inventory_trace_spans.py .\examples\trace-export.json `
  --expect-span "demo.request" --expect-dependency-type HTTP
```

Sanitize exports before using them. The inventory helps avoid narration about a
span or dependency type that the capture does not actually expose; it does not
prove trace correlation or reveal safe values to show on screen.

## Versioned delivery promotion

Use
[`examples/artifact-promotion-plan.json`](../examples/artifact-promotion-plan.json)
as a plan template. It names a versioned source and one stable delivery alias
per artifact:

```json
{
  "version": "v2",
  "archive_dir": "archive",
  "artifacts": [
    {"source": "demo-v2.mp4", "alias": "demo-latest.mp4"}
  ]
}
```

The script is dry-run by default. With `--apply`, it:

1. validates every source and alias before changes;
2. moves only an existing, explicitly named alias to
   `archive/<version>/previous/`;
3. copies each explicit versioned source to its alias without overwriting;
4. verifies source and alias SHA-256 values;
5. writes `promotion-<version>.manifest.json` and
   `checksums-<version>.sha256`.

It rejects absolute paths, parent traversal, symlinks (including nested archive
descendants), duplicate names, filesystem roots, existing metadata/archive
targets, unversioned source names, and browser/authentication-sensitive path
components. If a later named artifact or metadata write fails, it rolls back
the named aliases/archive entries it created rather than leaving a mixed
release; a concurrent external edit that prevents safe rollback is reported
explicitly. It does not scan, overwrite, or touch profile directories, storage
state, cookies, credentials, tokens, or paths outside the explicit delivery
directory. Review the JSON preview before passing `--apply`.

## JSON reports

Each check prints a stable JSON object to stdout and supports `--output` where
an output report is appropriate. Reports contain `tool`, `valid`, check counts,
diagnostics, and the applied thresholds or safety notes. This makes them useful
in a local release checklist without encouraging unattended claims about visual
truth.
