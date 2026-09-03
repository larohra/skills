# Playwright recording

## Reconnaissance

- Navigate and wait for `domcontentloaded` plus a meaningful visible element.
- Use accessibility snapshots to discover roles and names.
- Record deep URLs after navigation stabilizes.
- Prefer `get_by_role`, `get_by_label`, IDs, and exact text.
- Avoid generated CSS classes and coordinates unless necessary.

## Native recording pattern

```python
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    )
    context = browser.new_context(
        storage_state="storage-state.json",
        viewport={"width": 1440, "height": 900},
        record_video_dir="raw",
        record_video_size={"width": 1440, "height": 900},
    )
    page = context.new_page()
    video = page.video
    created = time.monotonic()
    page.goto(url, wait_until="domcontentloaded")
    page.get_by_role("heading", name="Expected").wait_for()
    content_start = time.monotonic()
    # Scene actions...
    content_end = time.monotonic()
    page.close()
    context.close()
    raw_path = video.path()
```

Store `start = content_start - created` and
`duration = content_end - content_start`; trim those values during stitching.

## Segment instead of one take

Use independent clips for title cards, browser workflows, trace inspection,
state-before/state-after views, and closing results. This allows retries,
removes dead time, and makes later insertions possible.

## Async telemetry

Do not record a multi-minute ingestion wait. Finish the interaction clip, wait
or poll outside recording, then start the trace clip once the ID is searchable.

## Controlled data

Pre-seed deterministic sessions and markers. Capture expected IDs and metrics
into JSON. Verify history markers or trace IDs after recording.

## Visual narrative

Inject a fixed, non-interactive badge with the scene number, capability, and
one-sentence claim. Use title cards for major transitions and integrations
without a page.
