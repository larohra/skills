# Post-task reflection and approved contributions

Declared contribution repository: [larohra/skills](https://github.com/larohra/skills).
The repository-owned skill is `skills/animated-demo-slides`; installed copies are not the edit target.

This is an authoring-agent workflow, not behavior to insert into a presentation. Generated HTML stays offline, with no telemetry, repository callbacks, or background feedback requests.

## Reflect once after delivery

After the requested deliverable is complete, briefly assess whether the work exposed an actionable, broadly reusable bug, missing instruction, or regression case. Do this once per completed authoring task, not after each slide, tool call, or revision. Do not delay delivery or require a contribution decision to finish the original task.

A reproducible focus failure in a constrained viewer may be reusable. A particular user's preferred color, title, topic, or storytelling style is not automatically a general rule. If there is no useful new lesson, do nothing: no manufactured issue, PR, or prompt.

Do not run this reflection loop at the end of a skill-improvement contribution task. The contribution is the end of the loop, not input to another contribution.

## Deduplicate and propose safely

Check the declared repository's current skill guidance and relevant issues/PRs before proposing work. Prefer one focused contribution. If the lesson is already covered or has an open contribution, do not file another or repeatedly ask the user to publish it.

If the contribution repository is not declared or its identity is uncertain, ask the user which repository to use. Never infer upstream from the unrelated working repository in which a presentation happened to be authored. If repository tools or access are unavailable, state that limitation rather than claiming the check or submission happened.

Explain the intended repository and the small sanitized change before publication. Describe the generic failure and a neutral synthetic regression case. Do not upload task artifacts, conversation excerpts, private architecture, private measurements, credentials, screenshots, local paths, or task/session identifiers. Approval to use the skill is not approval to publish task data.

For example, propose "Add a regression case for skip-focus behavior in a restricted embedded document" with an invented minimal fixture, not the user's deck or a transcript of how the defect was found. Preserve compatibility with existing invocations and data formats.

## Require publication approval

Obtain explicit approval covering the contribution and its destination **before creating a branch, pushing, or submitting a PR**. An existing user request that explicitly authorizes that contribution and repository already supplies approval; do not ask again unnecessarily.

If approval is absent, show the sanitized proposal and request it. If the user declines or defers, stop contribution work for that task; do not keep prompting. Do not create an issue, comment, or upload as a workaround for missing PR approval.

## Contribute through the normal process

After approval, read the target repository's instructions, follow its normal branch/contribution process, and edit the repository-owned source, never an installed skill. Make the smallest complete fix with relevant documentation and a neutral regression test or eval. Keep the approved compatibility surface intact and validate the change with the available focused tools.

Before pushing, inspect the entire diff and proposed PR body for private material and unrelated changes. Report the actual contribution link and validation performed. If tools, write access, or validation are unavailable, explain the concrete limitation; do not claim an update was sent.

Do not auto-merge, change access permissions, grant credentials, add a persistent automation or watcher, or invent a preference/configuration mechanism to enable future contributions. Publication approval for one focused contribution is not ongoing permission for silent self-modification.
