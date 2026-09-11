# Playwright recording

## Reconnaissance

- Navigate and wait for `domcontentloaded` plus a meaningful **visible**
  element. A locator's DOM existence or nonzero count is not enough for a
  readable capture.
- Use accessibility snapshots to discover roles and names.
- Record deep URLs after navigation stabilizes.
- Prefer `get_by_role`, `get_by_label`, IDs, and exact text.
- Avoid generated CSS classes and coordinates unless necessary.

## Verify a recordable frame

For a portal or dense application surface, treat these as separate checks:

1. Target a locator that resolves to a visible match, not a hidden duplicate in
   the DOM.
2. Scroll that match into view and check its bounding box/visibility after
   layout settles.
3. Make the text readable at the recording viewport; a technically visible row
   behind a sticky header or at the viewport edge is not proof.
4. Dismiss consent dialogs, product tours, notifications, account menus, and
   other popovers that block the target.
5. Take a verification screenshot outside the repository before starting video.
   Inspect it for the target, required markers, tenant/account context, and
   unexpected sensitive content.

For example, await a locator's visible state and then call
`scroll_into_view_if_needed()` before the recorded action. Do not turn a DOM
count into an `nth()` selector until the intended visible match is clear.

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

## Capture ownership for shared state

Shared persistent profiles and mutable cloud resources need coordination even
when they are technically accessible. Before capture, create a small,
time-bound lock record in the team's approved coordination location. See
[`examples/capture-lock.json`](../examples/capture-lock.json) for the fields:

| Field | Purpose |
| --- | --- |
| `owner` | Person or automation currently responsible for capture. |
| `scope` | Exact dedicated browser profile and/or mutable demo resource scope. |
| `acquired_at`, `expires_at` | Time limit so abandoned captures do not block teammates indefinitely. |
| `release_note` | Explicit handoff/release instruction. |

Renew an expiring lock deliberately, release it explicitly after capture, and
do not reuse a lock for a different scope. The record is coordination metadata
only: never put a URL with embedded credentials, cookies, tokens, passwords,
MFA material, storage state, or other secrets in it.

Do not delete, reset, stop, or clean up a profile/resource merely because it
looks stale. Limit cleanup to artifacts that the active lock or another
explicit ownership record covers. A dedicated profile is sensitive
authenticated state even when it contains no exportable password.

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
without a page. Before recording, make the badge, target, and required visible
markers readable in the verification screenshot. Use the
claim-evidence manifest to map that frame to the narration claim.
