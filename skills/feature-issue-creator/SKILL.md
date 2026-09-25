---
name: feature-issue-creator
description: Turn a feature idea and relevant conversation context into a self-contained GitHub tracking issue through focused probing questions and explicit draft approval. Use when asked to create, flesh out, productionize, or update a feature request or tracking issue, including an existing empty issue. Ask for the board link when missing. Do not use for bug reports, implementation, or routine status-only edits.
---

# Feature Issue Creator

Produce a concise feature contract that an engineer unfamiliar with the conversation can implement and a reviewer can verify. Draft first; publish only after the user approves the exact content and destination.

## 1. Establish context

- Use relevant conversation history and supplied links before asking questions. If prior discussions are referenced, retrieve only relevant history when available; otherwise ask for the missing decisions. Treat tentative ideas as proposals, not commitments.
- Require a board URL. Ask for it if absent; an issue URL is not a board URL. Confirm the target GitHub repository if the board does not identify it unambiguously.
- Accept an optional existing issue URL. If none is supplied, plan to create a new issue; do not require the user to create an empty one.
- Read the board's conventions, the existing issue and relevant comments, and applicable repository issue templates using read-only tools. If access fails, explain the limitation and ask for the needed content; do not guess or change permissions.
- Preserve existing decisions, task status, links, and unrelated content. An issue described as empty may not be empty. Board membership, labels, assignees, milestones, and project fields are separate changes, not implicit permission.

## 2. Probe the gaps

Briefly distinguish confirmed facts from unresolved decisions. Ask one focused question at a time, starting with the uncertainty that most affects scope or acceptance. Use the host's question tool when available. Skip questions already answered; offer concrete options when helpful without choosing for the user.

Probe only relevant gaps:

- **Problem and outcome:** Who needs this, what fails today, and what observable result makes the feature successful?
- **Boundary:** What is included in this release, explicitly excluded, and deferred?
- **Delivery:** Which concrete artifacts are required, and how will each be accepted?
- **Requirements and dependencies:** What behavior, failure handling, compatibility, performance, security, or operational constraints apply? Which prerequisites or external teams can block delivery?
- **Customer contract:** Which public APIs, schemas, configuration, defaults, errors, or documented guarantees change? What migration or compatibility policy is needed?
- **Front matter:** What does "front matter" mean in this repository, and which files, fields, defaults, validation rules, or versions change? Do not assume it means this skill's YAML metadata.
- **Production readiness:** What testing, rollout, rollback, telemetry, documentation, ownership, or support work is required?

Challenge vague phrases such as "production-ready" or "fast" with measurable acceptance criteria. Do not invent thresholds, owners, dates, dependencies, or decisions. Resolve blocking ambiguity or explicitly agree to track it as an open question. Use "None" or "Not applicable" only when established; unknown is not none.

## 3. Draft the issue

Use the following content in every draft. Preserve required repository template headings and map these sections into them; add missing sections rather than dropping required content. Expand acronyms on first use, name the affected components, and explain decisions without relying on "as discussed" or links alone.

```markdown
Title: <specific feature outcome>

## Problem and outcome
<Affected users, current limitation, and intended observable outcome.>

## Scope
<Included components, scenarios, and release boundary.>

## Deliverables
- [ ] <Concrete artifact and its completion evidence; link existing work where known.>

## Goals and Non-Goals
**Goals:** <Success criteria.>
**Non-goals:** <Explicit exclusions and deferred work.>

## Requirements and Dependencies
**Requirements:** <Testable behavior and operational constraints.>
**Dependencies:** <Prerequisites, linked work, and confirmed owners or unresolved ownership.>

## Customer contract changes needed
<Before/after public behavior, compatibility, migration, and documentation; or a confirmed reason none are needed.>

## Front matter changes needed
<Repository-specific meaning, affected files/fields, before/after values, defaults, and validation; or a confirmed reason none are needed.>

## Acceptance and rollout
- [ ] <Observable acceptance check and how it will be verified.>
<Required test coverage, release/rollback approach, telemetry, and support readiness.>

## Risks and open questions
<Unresolved decisions, delivery risks, and confirmed decision owners; distinguish proposals from commitments.>

## References
<Board, relevant issues, specifications, and supporting evidence.>
```

Keep each fact in one primary section. Track deliverables with checkboxes; mark them complete only with evidence. Add other sections only when they affect implementation or acceptance.

## 4. Review before publishing

Show the complete proposed title and body, the exact repository or existing issue URL, whether this creates or updates an issue, and any proposed metadata or board changes. For updates, identify what existing content will be replaced or preserved.

Ask for explicit approval of that preview. A request to "create," "update," or "post it" before seeing the draft is not approval of its contents. Requested revisions require a revised preview and fresh approval.

Until approved, do not create or edit an issue, post comments, attach issue artifacts, or change board items or metadata. Keep previews in the conversation or a local draft, not on the issue.

## 5. Publish and verify

After approval, re-read the destination issue before updating it. If it changed since preview, reconcile the changes and obtain approval again rather than overwriting someone else's work.

Use the host's designated GitHub issue creation/update tools when available, otherwise the GitHub CLI. Apply only the approved changes. Add to the board or alter metadata only if those exact actions were included in the approved preview.

Read back the resulting issue and any approved board changes. Report the issue link and any incomplete action accurately. If a write times out or has an uncertain result, check the current state before retrying to avoid duplicate issues or comments. Never treat a partial failure as complete or silently broaden access to finish.
