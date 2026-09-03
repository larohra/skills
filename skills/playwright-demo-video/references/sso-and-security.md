# SSO and security

## Company SSO workflow

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

## Do not clone browser profiles

Copying Chromium user data is unreliable: OS-encrypted cookies can be
invalidated when another Chrome process opens the copy. Export `storageState`
instead.

## Secrets

- Pass function/API keys through environment variables.
- Seed localStorage with an init script; never type keys while recording.
- Do not print keys, cookie values, tokens, connection strings, or storage state.
- Keep auth state and raw clips outside the repository.
- Remove storage state, copied profiles, and temporary browser artifacts after
  rendering.

## Internal portals

Prefer live capture when the user supplies a stable URL and SSO works.
Otherwise request sanitized screenshots. Never imply a view exists for an
integration without a visual portal; use a clearly labeled narrative card.
