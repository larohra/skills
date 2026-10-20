---
name: deploy-functions-dev-bits
description: Prepare and verify deployment of a Python Azure Functions app that depends on editable, local-path, workspace, or monorepo packages outside the app's upload boundary. Use for azd remote builds, Oryx builds, requirements.txt local references, staged wheels, or “works locally but the deployed Function cannot install my development package.” Preserve extras and unrelated dependencies, protect dirty source edits, verify the real upload artifact, and require fresh approval before any cloud deployment.
---

# Deploy Functions Dev Bits

Turn Python development dependencies into deployable artifacts without changing the developer's
local editable workflow. Treat packaging, upload, remote installation, deployment, and runtime
health as separate boundaries; evidence from one boundary does not prove the next.

## Scope

Use this workflow for Python Azure Functions deployments, especially `azd` deployments that use
remote/Oryx builds. It covers local directories, editable installs, workspace or monorepo packages,
and local transitive dependencies.

Do not imply support for every Azure Functions language or deployment mechanism. Do not deploy,
create infrastructure, change access, or authenticate to a new target merely because this skill
was invoked.

## 1. Establish the deployment boundary

Read repository instructions, then inspect:

- `azure.yaml`, including the selected service and its `project` directory;
- the Function app's `requirements.txt` and any included requirement or constraint files;
- `host.json`, Python/runtime declarations, and the deployment/build mode;
- `.funcignore`, `.gitignore`, deployment-specific excludes, and generated-package directories;
- each editable, relative-path, direct-file, or workspace requirement.

Resolve paths from the file and tool that interpret them. Do not assume a path is relative to the
repository root. Identify which local dependency sources fall outside the service project's upload
boundary. A remote builder cannot install a `file:` or editable path that was never uploaded.

Record the intended Azure target separately from the source package target. Before changing files,
capture:

- the dependency source path, distribution name, requested extras, and build backend;
- its current revision when version-controlled;
- its dirty/untracked state and whether the user intends those edits to be packaged;
- the Function target Python version, operating system, and architecture.

Preserve user changes. Never reset, clean, stash, or overwrite a dirty tree as part of packaging.
If it is unclear whether dirty edits belong in the artifact, stop before building and ask.

## 2. Choose an isolated staging plan

Prefer an owned, uniquely named deploy-staging tree so the checked-in app can retain its editable
development requirement. The staging tree should mirror the configured Function service project,
contain only deployable inputs, and be addressable by the repository's documented deployment
command or configuration.

If the deployment tooling cannot target staging without changing a tracked manifest, present the
smallest reversible manifest change for approval. Do not permanently rewrite a sample or application
requirement unless the user requested that source change.

Start from a clean, newly created wheel-output directory. Reusing a broad `*.whl` glob can silently
select a stale build. Give every owned staging/output path a distinctive name and remember it for
precise cleanup.

## 3. Build the exact local distribution

Use the package's existing build backend and an available compatible Python environment. Prefer:

```text
python -m pip wheel --no-deps --wheel-dir <clean-wheel-output> <local-source>
```

`--no-deps` keeps this step focused on the intended local distribution; it does not prove the full
Function dependency set is resolvable. If the repository already uses `python -m build`, Hatch,
Poetry, PDM, or another documented backend, use that instead of introducing a new one.

Confirm that exactly one expected wheel was produced. Validate:

- wheel distribution name and version match the intended package;
- metadata declares the extras referenced by the Function app;
- package modules and required package data are present;
- the wheel tags are compatible with the target Python, operating system, and architecture;
- native files such as `.pyd`, `.dll`, `.so`, or platform-tagged wheels were not accidentally built
  for Windows when the Function runs on Linux.

A `py3-none-any` wheel is normally portable only if its contents are genuinely pure Python. For
native extensions, build on a compatible target environment or use an already supported wheel;
do not relabel an incompatible wheel.

## 4. Rewrite only the deploy copy

Copy the validated wheel inside the staged Function project so it is within the actual upload
boundary. In the staged requirements graph, replace only the matching local/editable requirement.
Keep every unrelated requirement, include, constraint, marker, index option, and comment intact.

Preserve requested extras. A pip-supported relative wheel form is:

```text
<relative-path>/<distribution>-<version>-<tags>.whl[extra1,extra2]
```

Do not guess syntax. Parse or dry-run the staged requirement with the same pip generation used by
the build when practical. Confirm that the parsed extras remain present.

Inspect included requirement and constraint files recursively. If the wheel metadata or another
requirements file references a second local path outside the upload boundary, package and stage
that distribution too, or stop with an explicit blocker. One staged wheel does not make an
unavailable transitive local dependency deployable.

## 5. Exclude development and sensitive material

The staged upload must not include:

- `local.settings.json`, secrets, credentials, tokens, or connection strings;
- `.venv`, local `.python_packages`, caches, test output, or editor state;
- `.git`, source history, unrelated monorepo directories, or the local package source tree when
  the wheel is sufficient;
- stale wheels or artifacts from earlier attempts.

Ignore files are inputs to packaging, not proof of what was packaged.

## 6. Verify the real package boundary

Run the smallest repository-provided packaging or deployment dry run that exposes the actual
service project, archive, manifest, or upload file list. Inspect the produced artifact when the
tool supports it. Verify that:

- the staged requirements file is the one selected by deployment;
- the intended wheel is present at the exact relative path used by that file;
- excluded secrets and development directories are absent;
- the original outside-the-boundary local path is absent from the staged dependency graph.

For `azd`, confirm the selected service and resolved `azure.yaml` project path from tool output or
an inspectable package artifact. Do not claim that `.funcignore`, a successful wheel build, or a
correct-looking staging directory proves what `azd` uploaded. If the installed toolchain exposes
no non-mutating package artifact or file list, report that upload inclusion remains unverified and
seek authorization for the narrowest next observation; do not call the app deployable yet.

Run an offline/no-index dependency check where feasible so the local wheel cannot be silently
replaced by a registry package. A full online resolver check may still be needed for ordinary
third-party dependencies, but it must not install into the user's working environment.

## 7. Gate cloud actions

Use read-only commands first to identify the existing `azd` environment, subscription, resource
group, Function app, and deployment service. Report mismatches. Do not create infrastructure,
switch subscriptions, broaden permissions, log in, or deploy to a different target without fresh
authorization.

Before a mutating command, show:

- the exact existing target;
- the exact command and service;
- the source revision plus whether dirty edits are included;
- the staged wheel name/version and upload-boundary evidence;
- known limitations, including any unresolved native or transitive dependency.

Ask for approval to deploy that concrete target. Skill invocation, earlier deployments, and
packaging approval are not standing deployment permission.

## 8. Verify an authorized deployment

After approval, deploy with one owner for the live change and preserve command output. A successful
build or deployment command is not sufficient. Verify:

1. remote dependency installation completed without falling back to an unavailable local path;
2. the Function host starts and the expected functions are indexed;
3. a real harmless endpoint or trigger path responds as expected;
4. runtime evidence identifies the intended package version or source revision;
5. available logs or telemetry show no startup/import failure.

Some SDKs or tools download native components on first use. When relevant, verify target operating
system support, outbound access, writable/cache paths, cold-start behavior, and repeat invocation.
Prefer an explicit build-time or supported runtime mechanism over hardcoded assumptions about one
SDK.

Classify the result as deployed and verified, deployed but unverified, packaging blocked, or
deployment failed. State exactly which boundary the evidence reached.

## 9. Clean up safely

Remove only staging directories and wheel outputs created and named by this run. Never use broad
clean commands in a dirty repository. Preserve failed and passing evidence long enough for review,
and leave user-owned source edits and the normal editable development workflow unchanged.

## Report

Return:

```markdown
**Boundary:** <service project and why the local dependency was outside it>
**Packaged source:** <revision/version; dirty edits included or excluded>
**Staged requirement:** <relative wheel requirement with preserved extras>
**Artifact evidence:** <what proved the staged files were or were not selected for upload>
**Target:** <existing Azure target, or not inspected>
**Result:** packaging blocked | ready for deployment approval | deployed but unverified | deployed and verified | failed
**Limits:** <native, transitive, upload, runtime, or telemetry gaps>
**Cleanup:** <owned artifacts removed or intentionally retained>
```
