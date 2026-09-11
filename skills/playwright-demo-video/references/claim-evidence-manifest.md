# Claim-evidence manifest

Use a claim-evidence manifest before capture and keep it alongside the silent
rough cut. It turns a demo from a sequence of plausible clicks into a reviewable
argument: every narrated statement has a planned, readable visual proof.

The reusable example is
[`examples/claim-evidence-manifest.json`](../examples/claim-evidence-manifest.json).
It uses synthetic identifiers only. Copy it outside the repository with the
raw clips and generated QA frames; do not put authenticated state, endpoints,
tokens, customer names, or secrets in a manifest.

## Editorial units

A **chapter** proves one capability and one materially distinct user value. A
chapter can contain a coherent sequence across browser UI, runtime telemetry,
and a cloud portal: a durable-resume chapter, for example, can show an idle
session, its resumed user response, and the same session ID in telemetry.

A **scene** has one narrow claim. It can have multiple evidence shots because
one claim often needs a small proof chain (context, action, then result) or
needs the same correlation ID on separate surfaces. Do not use those shots to
make unrelated claims merely because the surface changed. Split an unrelated
claim into a new scene, and start a new chapter only if its user value is
materially different.

Before adding a title or capability card, run this uniqueness test: *does this
chapter give the viewer a new user value that the preceding chapter did not
already prove?* A different portal, tab, or telemetry view is not enough.
Before the final render, consolidate adjacent chapters that prove the same
end-to-end user value; retain multiple scenes inside the surviving chapter.

## Approval-gated production flow

1. Draft the storyboard and claim-evidence manifest. Review the chapter
   uniqueness rationale, evidence chain, continuity records, and fallbacks.
   Obtain approval before capture.
2. Cut a **silent rough cut** and extract planned proof frames. Review whether
   the visual argument works without narration.
3. Add timings and make a narration preview. Check gaps and ensure spoken
   claims land on their evidence. Obtain approval before final audio or final
   rendering.
4. Produce the final mix from the preserved silent master.
5. Run final QC, inspect the proof frames, and promote the versioned delivery.

This gate prevents expensive audio and rendering work from locking in an
unapproved narrative structure. It is a review discipline, not an excuse to
add process when the demo is small.

## Required shape

All timeline values are seconds in the final silent-master timeline, not
wall-clock timestamps.

| Level | Required fields | Meaning |
| --- | --- | --- |
| Top level | `schema_version`, `video`, `chapters` | `video.source` is the silent master used by frame extraction. |
| Chapter | `id`, `capability`, `user_value`, `distinct_value_from_prior`, `scenes` | State why its value differs from earlier material, including the first chapter. |
| Scene | `id`, `claim`, `timeline`, `evidence_shots`, `required_visible_markers`, `expected_result`, `correlation_ids`, `narration`, `fallback` | One scene makes one related claim. Set `correlation_ids` to `[]` only with a `correlation_rationale`. |
| Evidence shot | `id`, `file`, `timestamp_seconds`, `role`, `visible_markers`, `hold_start_seconds`, `hold_end_seconds` | `file` is an exact capture or extracted proof frame. `role` is `context`, `action`, `outcome`, `response`, `status`, or `telemetry`. |
| Narration | `claim`, `start_seconds`, `end_seconds`, `claim_timestamp_seconds`, `visible_hold_seconds`, `asserts_completion` | `claim_timestamp_seconds` is when the voiceover makes the core assertion. |
| Lifecycle continuity | `lifecycle_claim: true` and `continuity` | Declare linked before/after evidence, the durable identity, and any aliases separately. |

`correlation_ids` entries have a `name`, a synthetic-or-approved `value`, and
usually a `surfaces` list. They let reviewers find the same identifier across
the proof chain without mistaking a matching label for a lifecycle identity.

For a lifecycle claim, `continuity` has this shape:

```json
{
  "expected_identity": {"name": "session_id", "value": "session-demo-001"},
  "before": {
    "evidence_shot_id": "idle-before",
    "identity": {"name": "session_id", "value": "session-demo-001"},
    "aliases": [{"name": "generation", "value": "generation-1"}]
  },
  "after": {
    "evidence_shot_id": "completed-after",
    "identity": {"name": "session_id", "value": "session-demo-001"},
    "aliases": [{"name": "generation", "value": "generation-2"}]
  },
  "expected_aliases": [
    {"name": "generation", "before": "generation-1", "after": "generation-2"}
  ]
}
```

The identity must remain the same on both sides. Aliases may stay the same or
change when declared explicitly, but aliases never substitute for the
identity. `validate_continuity.py` reports those categories separately.

## Evidence and narration rule

If a narration claim cannot be pointed to in a specific visible frame, fix the
capture, revise the narration, or remove the claim. Never claim invisible
telemetry, unseen portal state, or a backend effect merely because it is
plausible.

For narration that asserts completion, show an outcome, status, or response
with all required markers **readably for about 3–5 seconds before** the claim
timestamp. Use `hold_start_seconds` and `hold_end_seconds` on the relevant
evidence shot plus `visible_hold_seconds` in narration. The validator fails a
hold under three seconds and warns when it runs materially beyond five; adjust
those thresholds only when the content justifies it.

The validator uses a deliberately limited deterministic strategy:

- checks required manifest fields, timing, IDs, declared marker coverage, and
  evidence-file existence;
- can confirm that frame extraction produced a claim frame for each scene;
- does **not** OCR pixels or infer product behavior from images.

Declare a marker only after a reviewer can point to it in the referenced frame.
Use the generated contact sheet and exact frames for the human visual check.

## Planning and validation

During storyboard review, placeholder evidence files are normal:

```powershell
python .\scripts\validate_claim_evidence.py `
  .\examples\claim-evidence-manifest.json --allow-missing-files
python .\scripts\validate_continuity.py `
  .\examples\claim-evidence-manifest.json
python .\scripts\check_narration_gaps.py `
  .\examples\claim-evidence-manifest.json --minimum-gap 0.8
```

After the silent cut exists, use real frame paths, extract review frames, then
validate file presence and frame-index coverage:

```powershell
python .\scripts\extract_scene_qc.py .\manifest.json .\qc
python .\scripts\validate_claim_evidence.py .\manifest.json `
  --frame-index .\qc\index.json
```

Read [`editorial-qc.md`](editorial-qc.md) for every QA script, its JSON output,
and safety boundaries.
