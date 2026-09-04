---
name: playwright-demo-video
description: Create and edit polished web-product demo videos using Playwright and FFmpeg, including segmented browser recording, company SSO authentication, telemetry-aware scene stitching, narration, subtle background music, visual highlights, title cards, metrics, storyboards, and MP4 delivery. Use for requests to record a product demo, browser walkthrough, narrated screen capture, sales or launch video, Playwright video, or to enhance an existing demo without re-recording it.
---

# Playwright Demo Video

Create the smallest coherent story, record independent scenes, remove real-time
waits during editing, and preserve the original capture before enhancing it.

## Workflow

1. **Check the machine**
   - Run `scripts/check_prereqs.ps1`.
   - Prefer `uv run --with playwright python ...` instead of adding Playwright
     to the repository.
   - Use installed Chrome; Playwright video works in headless mode.

2. **Write the story before automating**
   - Define the claim each scene proves, required IDs/metrics, expected result,
     and fallback.
   - Use short title cards between major chapters.
   - Prepare controlled warm/stale sessions or test data before recording.
   - Read [references/storyboarding.md](references/storyboarding.md).

3. **Reconnoiter with Playwright MCP**
   - Navigate every page, wait for rendered state, and capture accessibility
     snapshots before writing selectors.
   - Prefer roles, labels, IDs, and exact text over generated CSS classes.
   - Map dialogs, tabs, tables, and deep links before the recorded run.

4. **Authenticate safely**
   - Never request, receive, type, log, or store passwords/MFA values.
   - Let the user complete company SSO interactively once.
   - For managed work portals, Conditional Access, device compliance, or
     tenant-sensitive SSO, start with Chrome or Edge in a dedicated,
     machine-local persistent profile.
   - For applications whose authentication is fully represented by cookies,
     local storage, and IndexedDB, prefer Playwright
     `storageState({ indexedDB: true })` and verify it in a fresh context.
   - Create persistent profile directories automatically; never attach to,
     copy, or modify the user's default browser profile.
   - Verify the authenticated tenant/directory before recording. Browser profile
     isolation does not necessarily isolate Windows device SSO or server-side
     tenant selection.
   - Read [references/sso-and-security.md](references/sso-and-security.md).

5. **Record segmented scenes**
   - Default to 1440×900, device scale 1, light color scheme, H.264 delivery.
   - Record one page/scene at a time. Close the page/context to finalize WebM.
   - Record `video_start`, `content_start`, and `content_end`; trim browser load
     time later.
   - Keep telemetry ingestion, deployment, retries, and long waits outside the
     recorded clips. Resume recording after the result is queryable.
   - Add unobtrusive scene badges in DOM for narrative continuity.
   - Read [references/playwright-recording.md](references/playwright-recording.md).

6. **Stitch the silent master**
   - Create a JSON scene manifest and run:
     `python scripts/stitch_clips.py manifest.json output.mp4`.
   - Preserve the raw/original master. Insert new scenes by splitting/stitching;
     do not re-record working scenes.

7. **Enhance non-destructively**
   - Prefer narration plus very subtle music for technical demos.
   - Generate narration with `scripts/generate_narration.ps1`.
   - Generate a license-free ambient bed with
     `python scripts/generate_ambient_bed.py`.
   - Build transparent highlight PNGs and apply them only during relevant time
     windows.
   - Mix audio/overlays with
     `python scripts/mix_audio_overlays.py manifest.json`.
   - Read [references/editing-and-audio.md](references/editing-and-audio.md).

8. **Review and clean**
   - Run `scripts/make_contact_sheet.py` and inspect opening, closing, key
     transitions, highlights, and internal pages.
   - Check `ffprobe` duration/codecs and `volumedetect` audio levels.
   - Verify every scenario's expected marker/ID through UI or telemetry.
   - Delete storage-state files, obsolete profiles, raw clips, keys, and
     temporary screenshots. Retain a dedicated persistent profile only when the
     user intentionally wants machine-local session reuse, and identify it as
     sensitive authenticated state.
   - Retain final videos, storyboard, results, and scripts.

## Quality contract

- Tell one capability-first story; do not record aimless navigation.
- Use real IDs and measured timings only when safe and intentional.
- Label browser timing as client-observed, not a service SLA.
- Show correlation by copying/searching the same ID across surfaces.
- Show pre/post state for lifecycle claims such as idle → active → idle.
- Do not imply a portal view exists; use an honest card for invisible
  integrations.
- Keep music beneath narration. Aim near `-24 dB` mean and below `-2 dB` peak.
- Preserve a silent original and create a separate enhanced output.

## Resources

- `scripts/check_prereqs.ps1` — validate Chrome, FFmpeg, uv, and SAPI voices.
- `scripts/open_persistent_browser.py` — create or reopen a dedicated Chrome or
  Edge profile for interactive SSO.
- `scripts/generate_narration.ps1` — generate Windows narration WAVs.
- `scripts/generate_ambient_bed.py` — create a subtle license-free music bed.
- `scripts/stitch_clips.py` — trim and concatenate scene recordings.
- `scripts/mix_audio_overlays.py` — composite highlights, narration, and music.
- `scripts/create_highlight_overlay.py` — create reusable transparent callouts.
- `scripts/make_contact_sheet.py` — create visual QC contact sheets.
- `references/sso-and-security.md` — company SSO and credential cleanup.
- `references/playwright-recording.md` — selectors, segmented capture, waits.
- `references/editing-and-audio.md` — narration, music, highlights, FFmpeg.
- `references/storyboarding.md` — scene and voiceover templates.
