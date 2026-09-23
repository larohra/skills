---
name: run-simple-spike
description: Plan and run a small, evidence-backed engineering spike or proof of concept. Use when asked to test whether an integration works, reproduce a runtime boundary failure, or prove one technical assumption with a tiny real flow; not for routine edits or broad production qualification.
---

# Run Simple Spike

Run the smallest useful experiment that answers one engineering question with real evidence. Prefer the intended runtime boundary over mocks when the question is about transport, quoting, authentication shape, serialization, platform behavior, or tool integration.

## Use this skill when

Use this for a bounded spike, proof of concept, repro, or assumption check where the outcome should be a clear pass, fail, or inconclusive result backed by commands, traces, screenshots, logs, or code output.

Do not use it for routine implementation, broad audits, product qualification, load testing, security review, or exploratory research without a concrete pass criterion.

## Define the spike

State the spike contract before building anything:

- **Question:** the single assumption being tested.
- **Pass criterion:** the observable result that would prove the assumption.
- **Tiny flow:** the shortest realistic path through the actual boundary.
- **Safety bounds:** what will not be changed, persisted, published, or accessed.
- **Evidence to keep:** the exact output, artifact, or observation needed to support the conclusion.

Ask at most one clarifying question if the pass criterion or target boundary is unknowable. Otherwise, make a reasonable conservative assumption and proceed.

## Build the smallest real flow

Prefer a throwaway fixture, minimal script, local sample, or isolated test command over modifying production code. Use existing repository tooling and package managers; do not add dependencies unless the spike cannot answer the question without them.

Keep the experiment close to the real boundary:

- For command, shell, quoting, or process behavior, run the command shape on the target shell or runtime.
- For HTTP, RPC, queue, file, serialization, or plugin boundaries, exercise a real request or message with harmless data.
- For framework behavior, create the smallest route, handler, function, component, or test that invokes the framework path.
- For cloud or shared resources, use read-only checks first and avoid mutations unless the user already approved the exact target and consequence.

Do not treat mocks, inferred behavior, or documentation alone as proof when the spike is about runtime integration.

## Capture evidence while preserving privacy

Record enough evidence for another engineer to understand the result, but scrub anything not needed for the conclusion.

Keep out of public notes and committed files:

- credentials, tokens, secrets, cookies, connection strings, and storage state;
- private repository names, tenant names, subscription IDs, hostnames, account IDs, or internal resource identifiers;
- raw session transcripts, approval receipts, personal preferences, and private user data;
- proprietary logs or payloads beyond the minimal sanitized excerpt needed to explain behavior.

Use placeholders such as `<repo>`, `<tenant>`, `<resource-id>`, or `<correlation-id>` when an identifier is structurally useful but not public-safe.

## Interpret the result

Distinguish the boundary that was tested from nearby untested claims. A useful spike conclusion is usually one of:

- **Pass:** the tiny real flow met the pass criterion.
- **Fail:** the flow reached the intended boundary and contradicted the assumption.
- **Inconclusive:** the flow did not reach the intended boundary, so the result cannot answer the question.

If the first attempt fails because of setup, fixture, permissions, timing, or harness issues, fix the harness once when the correction is obvious and still within scope. Do not keep expanding the spike until it becomes a feature implementation.

## Report the outcome

Keep the report short and evidence-backed:

```markdown
**Question:** Can <assumption> work across <boundary>?

**Pass criterion:** <observable result>.

**Flow run:** <command or tiny path>.

**Result:** Pass | Fail | Inconclusive.

**Evidence:** <sanitized command output, artifact path, trace excerpt, or observation>.

**Limits:** <what this does not prove>.

**Recommended next step:** <one concrete follow-up, only if needed>.
```

If the spike created temporary files, remove them unless they are the evidence artifact or the user asked to keep them. If it changed repository files, keep the diff minimal and clearly labeled as spike support rather than production-ready code.
