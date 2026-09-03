# GitHub Copilot Skills

A collection of shareable [GitHub Copilot](https://github.com/features/copilot) skills.

## Available skills

- [`playwright-demo-video`](skills/playwright-demo-video/) — Plan, record, edit, and review polished Playwright-based product demo videos.

## Manual installation

To install a skill for the current user on Windows, clone this repository and copy the named skill into the GitHub Copilot skills directory:

```powershell
git clone https://github.com/larohra/skills.git copilot-skills
New-Item -ItemType Directory -Force "$HOME\.github\skills"
Copy-Item -Recurse -Force `
  .\copilot-skills\skills\playwright-demo-video `
  "$HOME\.github\skills\playwright-demo-video"
```

Future releases may offer an `npx` installer; none is published today.
