# SSO and security

## Choose the authentication mode

Choose the mode from the authentication environment:

1. For a managed work portal, Conditional Access, device compliance,
   tenant-sensitive SSO, or an explicit request to use an authenticated work
   profile, start with a dedicated persistent Chrome or Edge profile.
2. For an application whose login is represented by cookies, local storage, and
   IndexedDB, use exported `storageState` and test it in a fresh context.
3. If a storage-state context is rejected by browser-bound authentication,
   switch to a dedicated persistent profile on that machine.

These are alternative reuse strategies, not required sequential layers. Once a
dedicated profile is necessary and working, reuse that profile for follow-up
sessions. Export `storageState` from it only when a separate clean/isolated
context is useful, and keep using it only if that context passes the same
authentication and tenant checks.

Persistent profiles are more compatible with managed SSO but retain broader
browser history and state, can introduce stale tenant/account choices or UI
popups, and allow only one owning browser process. Storage-state contexts are
useful for clean, repeatable recording scenes when the target application
accepts them.

Do not weaken or bypass Conditional Access. A persistent profile is a way to
preserve an approved browser session, not a policy workaround.

## Portable storage-state workflow

1. Open the target portal with Playwright MCP.
2. Click **Sign in**.
3. Let the user complete account selection, password, MFA, or consent
   interactively. Never ask for those values in chat.
4. Confirm the authenticated project/page is visible.
5. Export decrypted Playwright state from the authenticated MCP page:

```javascript
async (page) => {
  await page.context().storageState({
    path: "C:\\path\\to\\storage-state.json",
    indexedDB: true
  });
  return page.url();
}
```

Use `browser_run_code_unsafe` only for this controlled agent-authored snippet.

6. Launch native Playwright with `browser.new_context(storage_state=...)`.
7. Wait through the SSO redirect chain and confirm authenticated project text.

## Device-bound persistent profile workflow

Some managed Windows environments require Chrome or Edge to present device
identity that is not preserved in `storageState`. Symptoms include a
"You can't get there from here" page, a request for an organization-approved
browser extension, or a policy that requires a compliant device/client.

Create a new profile directory dedicated to the target portal. The user does
not need to create a Chrome "work profile":

```powershell
uv run --with playwright python .\scripts\open_persistent_browser.py `
  --profile-name azure-portal `
  --browser chrome `
  --url "https://portal.azure.com/"
```

The script creates the directory automatically under
`$env:LOCALAPPDATA\ms-playwright-demo-video`. If Playwright MCP is being
configured directly and Node.js is available, use the equivalent persistent
profile option:

```powershell
npx "@playwright/mcp@latest" --browser chrome `
  --user-data-dir "$env:LOCALAPPDATA\ms-playwright-mcp\azure-portal"
```

Let the user complete SSO in that browser once, close it normally, and reuse
the same directory on later runs on that physical machine. A persistent profile
can be opened by only one browser process at a time.

For native Playwright recording, use the same dedicated directory:

```python
with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=profile_dir,
        channel="chrome",
        headless=False,
        viewport={"width": 1440, "height": 900},
        record_video_dir="raw",
        record_video_size={"width": 1440, "height": 900},
    )
```

Prefer headed recording for device-compliance flows unless a tested headless
context demonstrably retains access. Close the authentication context before
opening the recording context with the same profile.

If Chrome still fails an organization policy, retry with `-Browser msedge` and
a different dedicated profile directory. Use only organization-approved
browsers and extensions.

## Tenant and account verification

A clean browser profile isolates cookies and local browser data, but Windows
device SSO can still select a connected operating-system account. Portals can
also restore a server-side last-used tenant or directory.

- Use a tenant-qualified target URL when the application supports one. For
  Azure Portal, use
  `https://portal.azure.com/?tenant=<tenant-id-or-domain>#home`.
- Treat a `#EXT#` principal as a guest projection, not proof that the intended
  home tenant was selected.
- Verify the authenticated tenant/directory in the UI before recording.
- If the wrong tenant appears, stop before capture. Relaunch with a new
  dedicated profile name plus the explicit tenant-qualified URL.

Do not infer successful authentication from `body` visibility alone. Reject
known Conditional Access error text and wait for a portal-specific title,
landmark, or expected authenticated element.

## Never reuse the default browser profile

Do not point Playwright at the user's normal Chrome/Edge data directory. Do not
copy that directory, attach over CDP to work around profile locks, or move a
dedicated profile between physical machines. Encrypted or device-bound state
may be invalidated, and the profile contains sensitive authenticated material.

## Secrets

- Pass function/API keys through environment variables.
- Seed localStorage with an init script; never type keys while recording.
- Do not print keys, cookie values, tokens, connection strings, or storage state.
- Keep auth state, dedicated profiles, and raw clips outside the repository.
- Remove storage state, obsolete profiles, and temporary browser artifacts only
  when they are explicitly owned by the current capture. Do not destructively
  clean up a shared profile or cloud resource based on appearance alone.
- Retain a dedicated persistent profile only with the user's intent to reuse
  it. Report its path and warn that it contains sensitive authenticated state.
- A capture lock may record owner, scope, expiry, and release only. It is
  coordination metadata, never a place to store credentials, cookies, tokens,
  storage state, or a secret-bearing URL.

## Internal portals

Prefer live capture when the user supplies a stable URL and SSO works.
Otherwise request sanitized screenshots. Never imply a view exists for an
integration without a visual portal; use a clearly labeled narrative card.
