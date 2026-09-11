---
name: playwright-demo-video
description: Create and edit polished web-product demo videos using Playwright and FFmpeg, including segmented browser recording, company SSO authentication, telemetry-aware scene stitching, narration, subtle background music, visual highlights, title cards, metrics, storyboards, and MP4 delivery. Use for requests to record a product demo, browser walkthrough, narrated screen capture, sales or launch video, Playwright video, or to enhance an existing demo without re-recording it.
---

# Playwright Demo Video

Create the smallest coherent visual argument, record independent scenes, remove
real-time waits during editing, and preserve the original capture before
enhancing it. Use a claim-evidence contract so narration says only what a
viewer can see.

## Workflow

1. **Check the machine**
   - Run `scripts/check_prereqs.ps1`.
   - Prefer `uv run --with playwright python ...` instead of adding Playwright
     to the repository.
   - The QA scripts use Python 3.9+ standard library features; frame/video
     checks also need FFmpeg and FFprobe.
   - Use installed Chrome; Playwright video works in headless mode when the
     authentication flow has been verified there.

2. **Approve the visual argument before capture**
   - Draft `claim-evidence.json`. Give each chapter one capability and
     materially distinct user value; its scenes may form one coherent proof
     across UI, telemetry, and cloud surfaces.
   - Give each scene one narrow claim, exact proof frames/markers, expected
     result, correlation IDs, narration timing, fallback, and lifecycle
     before/after identity where relevant.
   - Test a prospective title/capability card: it must add new user value, not
     merely change surfaces. Consolidate adjacent chapters that prove the same
     value before final rendering.
   - Obtain structure approval before capture. Read
     [references/claim-evidence-manifest.md](references/claim-evidence-manifest.md).

3. **Reconnoiter and verify the frame**
   - Navigate every page, wait for rendered state, and capture accessibility
     snapshots before writing selectors.
   - DOM existence is not capture readiness: target a visible match, scroll it
     into an unobscured readable position, dismiss blocking popovers, and take
     a verification screenshot before recording.
   - Prefer roles, labels, IDs, and exact text over generated CSS classes.
   - Map dialogs, tabs, tables, and deep links before the recorded run.
   - Read [references/playwright-recording.md](references/playwright-recording.md).

4. **Authenticate and reserve capture safely**
   - Never request, receive, type, log, or store passwords/MFA values.
   - Let the user complete company SSO interactively once.
   - For shared profiles or mutable cloud resources, publish a scoped,
     time-bound capture lock with owner, scope, expiry, and explicit release.
     It is coordination metadata only, never a credential store.
   - Use a dedicated machine-local persistent profile only when needed; never
     use the user's default profile or perform cleanup outside explicit capture
     ownership.
   - Read [references/sso-and-security.md](references/sso-and-security.md) and
     [references/playwright-recording.md](references/playwright-recording.md).

5. **Record segmented scenes**
   - Default to 1440×900, device scale 1, light color scheme, H.264 delivery.
   - Record one page/scene at a time. Close the page/context to finalize WebM.
   - Record `video_start`, `content_start`, and `content_end`; trim browser load
     time later.
   - Keep telemetry ingestion, deployment, retries, and long waits outside the
     recorded clips. Resume recording after the result is queryable.
   - Add unobtrusive scene badges in DOM for narrative continuity.
   - Keep the approved lock current and release it explicitly when capture ends.

6. **Review a silent rough cut**
   - Keep the existing clip manifest separate from the claim contract:
     `python scripts/stitch_clips.py clips.json deliverables/silent-master.mp4`.
     Set `claim-evidence.json`'s `video.source` to that silent master and
     preserve it as the raw/original master.
   - Extract scene midpoints, claim timestamps, evidence frames, and transition
     frames with
     `python scripts/extract_scene_qc.py claim-evidence.json qc`.
   - Inspect the silent proof chain. Fix the capture or structure before
     narration; do not produce final audio or render before that review is
     approved.

7. **Preview timing and narration**
   - Generate narration with `scripts/generate_narration.ps1` and schedule
     speech with at least 0.8 seconds of breathing room:
     `python scripts/check_narration_gaps.py claim-evidence.json`.
   - Narrate capability claims, not clicks. If a narration claim cannot point to
     a visible frame, fix the capture, revise the narration, or remove it.
     Never claim invisible telemetry or unseen surfaces.
   - Hold readable outcome/status/response evidence for roughly 3–5 seconds
     before narration asserts completion. Obtain timing/narration approval.

8. **Produce the final mix**
   - Prefer narration plus very subtle music for technical demos.
   - Generate a license-free ambient bed with
     `python scripts/generate_ambient_bed.py`.
   - Build transparent highlight PNGs and apply them only during relevant time
     windows.
   - Keep the existing mix manifest separate from the claim contract and mix
     audio/overlays with `python scripts/mix_audio_overlays.py mix.json`.
   - Read [references/editing-and-audio.md](references/editing-and-audio.md).

9. **Run final QC and promote**
   - Run `validate_claim_evidence.py`, `validate_continuity.py`,
     `check_narration_gaps.py`, and `detect_static_waits.py`. Review generated
     claim frames, transitions, and midpoints rather than treating a report as
     proof.
   - Inventory a sanitized telemetry export with
     `inventory_trace_spans.py` before asserting named spans/dependencies.
   - Run `promote_versioned_artifacts.py` in dry-run mode, review its JSON, then
     use `--apply` to archive only named prior aliases and create checksummed
     delivery aliases.
   - Check `ffprobe` duration/codecs and `volumedetect` audio levels.
   - Verify every scenario's expected marker/ID through UI or telemetry.
   - Delete only explicitly owned capture artifacts. Retain a dedicated
     persistent profile only when the user intentionally wants machine-local
     session reuse, and identify it as sensitive authenticated state.
   - Retain final videos, storyboard, results, and scripts.

## Quality contract

- Tell one capability-first chapter story; do not record aimless navigation.
- A chapter can cross surfaces, but a scene cannot make unrelated claims.
- Use several evidence shots when one claim needs a context/action/result chain.
- Use real IDs and measured timings only when safe and intentional.
- Label browser timing as client-observed, not a service SLA.
- Show correlation by copying/searching the same ID across surfaces.
- Show pre/post state for lifecycle claims such as idle → active → idle.
- Do not imply a portal view exists; use an honest card for invisible
  integrations.
- Do not narrate what a reviewer cannot point to in a visible frame.
- Keep music beneath narration. Aim near `-24 dB` mean and below `-2 dB` peak.
- Preserve a silent original and create a separate enhanced output.

## Resources

- `scripts/check_prereqs.ps1` — validate Chrome, FFmpeg, FFprobe, Python 3.9+, uv,
  and SAPI voices.
- `scripts/open_persistent_browser.py` — create or reopen a dedicated Chrome or
  Edge profile for interactive SSO.
- `scripts/generate_narration.ps1` — generate Windows narration WAVs.
- `scripts/generate_ambient_bed.py` — create a subtle license-free music bed.
- `scripts/stitch_clips.py` — trim and concatenate scene recordings.
- `scripts/mix_audio_overlays.py` — composite highlights, narration, and music.
- `scripts/create_highlight_overlay.py` — create reusable transparent callouts.
- `scripts/make_contact_sheet.py` — create visual QC contact sheets.
- `scripts/validate_claim_evidence.py` — validate declared visual evidence,
  marker coverage, completion holds, and files.
- `scripts/check_narration_gaps.py` — fail on narration overlap or short gaps.
- `scripts/extract_scene_qc.py` — extract claim/evidence/midpoint/transition
  frames and a contact sheet.
- `scripts/detect_static_waits.py` — flag likely static regions for review.
- `scripts/validate_continuity.py` — distinguish durable identity from aliases.
- `scripts/inventory_trace_spans.py` — inventory local sanitized span/dependency
  exports without live queries.
- `scripts/promote_versioned_artifacts.py` — safely promote named versioned
  deliverables after dry-run review.
- `references/sso-and-security.md` — company SSO and credential cleanup.
- `references/playwright-recording.md` — selectors, segmented capture, waits.
- `references/editing-and-audio.md` — narration, music, highlights, FFmpeg.
- `references/claim-evidence-manifest.md` — approval-gated storyboard contract
  and manifest template.
- `references/editorial-qc.md` — QC commands, JSON reports, and safety limits.
- `references/storyboarding.md` — concise chapter and scene orientation.
- `examples/clip-manifest.json` — existing `stitch_clips.py` input template.
- `examples/mix-manifest.json` — existing `mix_audio_overlays.py` input template.
- `examples/claim-evidence-manifest.json` — editorial contract template.
