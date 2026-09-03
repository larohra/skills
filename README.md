# GitHub Copilot Skills

A collection of shareable [GitHub Copilot](https://github.com/features/copilot) skills.

## Available skills

- [`playwright-demo-video`](skills/playwright-demo-video/) — Plan, record, edit, and review polished Playwright-based product demo videos.

## Installation

### Preferred: GitHub CLI

With GitHub CLI 2.90.0 or newer, install the pinned first release (created with this correction):

```powershell
gh skill install larohra/skills playwright-demo-video --agent github-copilot --scope user --pin v1.0.0
```

### Manual fallback

To install the skill for the current user on Windows, clone this repository and copy it to the Copilot skills directory:

```powershell
git clone https://github.com/larohra/skills.git copilot-skills
New-Item -ItemType Directory -Force "$HOME\.copilot\skills"
Copy-Item -Recurse -Force `
  .\copilot-skills\skills\playwright-demo-video `
  "$HOME\.copilot\skills\playwright-demo-video"
```

After a manual installation, restart Copilot CLI or run `/skills reload`.
