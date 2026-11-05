# GitHub Copilot Skills

A collection of shareable [GitHub Copilot](https://github.com/features/copilot) skills.

## Available skills

- [`animated-demo-slides`](skills/animated-demo-slides/) — Create polished animated SVG-based slide presentations for technical explanations, demos, and design reviews.
- [`design-excellence`](skills/design-excellence/) - Apply design-director-level refinement to any visual output (decks, dashboards, HTML, spreadsheets, PDFs, charts): build a functional version, then silently elevate it through a systematic protocol.
- [`deploy-functions-dev-bits`](skills/deploy-functions-dev-bits/) — Prepare Python Azure Functions apps with local, editable, or monorepo dependencies for verified deployment.
- [`feature-issue-creator`](skills/feature-issue-creator/) - Turn feature ideas and conversation context into clear GitHub tracking issues through focused questions and approval before publishing.
- [`msrc-triage`](skills/msrc-triage/) — Investigate MSRC / ICM security reports, validate code and impact, and draft a cited response.
- [`playwright-demo-video`](skills/playwright-demo-video/) — Plan, record, edit, and review polished Playwright-based product demo videos.
- [`run-simple-spike`](skills/run-simple-spike/) — Run a small, evidence-backed engineering spike with one question, one explicit pass criterion, and one tiny real flow on the intended runtime.

## Portable playbook workflow

This repository is the public, generic source for skills that are safe to share across playbooks. Private playbooks may sync from this repository by allowlisting public skill paths, currently including `skills/run-simple-spike/` and `skills/msrc-triage/`.

Keep personal capture workflows, private repository automation, raw session state, approval receipts, private resource identifiers, credentials, tenant-specific values, and user-specific assumptions out of this repository. If a lesson depends on private evidence, publish only the generalized behavior and verification pattern.

## Validation

Run the dependency-free skill metadata and privacy-tripwire check before publishing:

```powershell
python .\scripts\validate_skills.py
```

## Installation

### Preferred: GitHub CLI

With GitHub CLI 2.90.0 or newer, install a skill with:

```powershell
gh skill install larohra/skills playwright-demo-video --agent github-copilot --scope user --pin v1.0.0
```

After `msrc-triage` is merged, pin to the commit that includes it until a
versioned release includes the skill:

```powershell
gh skill install larohra/skills msrc-triage --agent github-copilot --scope user --pin <commit-sha>
```

### Manual fallback

To install the skill for the current user on Windows, clone this repository and copy it to the Copilot skills directory:

```powershell
git clone https://github.com/larohra/skills.git copilot-skills
New-Item -ItemType Directory -Force "$HOME\.copilot\skills"
Copy-Item -Recurse -Force `
  .\copilot-skills\skills\msrc-triage `
  "$HOME\.copilot\skills\msrc-triage"
```

After a manual installation, restart Copilot CLI or run `/skills reload`.
