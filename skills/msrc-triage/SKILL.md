---
name: msrc-triage
description: "Investigate an MSRC / ICM security case, validate whether the reported issue is real and exploitable, check the code timeline and deployment impact, and draft a cited response. Use for MSRC cases, ICM security incidents, VULN submissions, or requests to triage a security report. This skill investigates and drafts a reply only; it never modifies product code."
---

# MSRC / ICM Case Triage

Turn a raw MSRC case into a defensible verdict (**is this a real, exploitable
issue?**) and a ready-to-send response. The method is source-review forensics:
read the claim, read the code, and — critically — **check whether the code today
is the same code the reporter reviewed.**

> **Scope guardrail:** Investigate and draft a response. Do **not** edit product
> code. You may *recommend* the fix and defense-in-depth; you do not implement
> it. Do not auto-post to ICM/MSRC — hand the drafted reply to the user.

## Golden rules

1. **Cite everything.** Every claim in your verdict and response ties to concrete
   evidence: `file.py:123`, a commit SHA, a PR number, a test name, or a specific
   MSRC field value. No hand-waving.
2. **Separate the accurate part from the framing.** Reporters are often *correct
   about the code* but *overstate the impact* (e.g., calling an application
   routing predicate an "AuthZ bypass"). Validate the code claim and the impact
   claim independently.
3. **"Code-review finding" ≠ "observed exploit."** Most MSRC submissions from
   external finders are static source reviews of a public repo, not working
   attacks. Say which one it is.
4. **Timeline first.** Before deep analysis, find out if the issue was already
   fixed. This single step resolves a large fraction of cases. See
   [git-forensics.md](git-forensics.md).
5. **Respectful, factual tone.** Never dismissive, even for a false positive —
   the finder did real work. Acknowledge, then scope.

## Workflow (6 phases)

### Phase 0 — Intake
- Get the **incident ID**: the numeric segment of the portal URL, e.g.
  `portal.microsofticm.com/.../incidents/details/<incident-id>/summary`.
- If the `icm-agency` (ICM) MCP server is available, pull the case (see
  [icm-tools.md](icm-tools.md)). The portal itself requires SSO and can't be
  fetched with web tools — don't try.
- If ICM tooling is **not** available, ask the user to paste: title, claimed
  vector/PoC, affected file paths, severity, and case/finder metadata.

### Phase 1 — Extract the claim
From the incident details (see [icm-tools.md](icm-tools.md)):
- **Title** — usually encodes the affected `path/to/file` plus a one-line
  weakness (e.g. "Fail-open async edge predicate bypasses AuthZ").
- **`MsrcCaseDetails`** custom field (JSON) — Severity, SecurityImpact,
  CaseNumber, SubmissionNumber (`VULN-####`), FinderOrganization,
  `CaseCreationDate`, `LastModificationDate`, RecommendedResolution, CveNumber,
  Public, CloudCritical, AzureHostImpact.
- Also try `get_ai_summary`, `get_incident_context`, `get_mitigation_hints`,
  `get_similar_incidents` — frequently empty; that's fine, note it.

Write the claim in **one sentence**: *"Reporter claims that `<code>` allows
`<attacker>` to `<impact>` because `<mechanism>`."* If you can't, you don't
understand the claim yet — re-read.

### Phase 2 — Locate the code
- Find the file/function named in the title.
- **Watch for indirection:** the cited file may be a thin re-export or wrapper.
  Trace imports to the real implementation and read *that* function.
- Read the specific function end-to-end. Identify the exact line(s) the claim
  hinges on.

### Phase 3 — Timeline forensics *(the crux)*
Determine whether **current code == code at report time.** Full recipe in
[git-forensics.md](git-forensics.md). In short:
- `git log --oneline --follow -- <path>`; compare commit dates to
  `CaseCreationDate` / `LastModificationDate`.
- If the file changed **after** the case opened, reconstruct the pre-report
  version (`git show <commit>~1:<path>`) and diff the cited function — this
  reveals *already-fixed* cases and the exact fixing PR/commit.
- `git blame` the current function to date it; look for a regression test that
  locks in the fixed behavior.

### Phase 4 — Vulnerability-class & exploitability analysis
Apply the rubric in [verdict-rubric.md](verdict-rubric.md):
- Is the cited construct a **genuine security boundary** (authN, authZ, tenant
  isolation, crypto, deserialization, injection sink, path traversal, SSRF), or
  **application/business logic mislabeled** as security?
- **What triggers it?** Attacker-controlled input (remote) vs. a developer
  authoring choice (footgun) vs. something requiring elevated privilege (if so,
  the system is already compromised — the premise is self-defeating).
- **Count the preconditions.** List every condition that must hold
  *simultaneously*. Many ANDs ⇒ far-fetched.
- **Fail-open vs fail-closed** for the exact path.
- Cross-check the reporter's framing against reality, and against MSRC's own
  Severity / CloudCritical / AzureHostImpact / CVE fields.

### Phase 4.5 — Escalation & disclosure gates *(ALWAYS answer these)*
First settle the **deployment model** (Test 0 in
[verdict-rubric.md](verdict-rubric.md)): self-hosted library/SDK vs.
Microsoft-operated service. Then **always** answer both of the following in the
final verdict — even when the user doesn't ask and impact looks zero — because
MSRC's plan-of-action form requires them:

1. **SSIRP / customer-reporting gates** — the three boundary questions:
   **active exploitation** (telemetry/logs/any source), **tenant→service
   compromise** (unauthorized entity crossed into a Microsoft-operated service
   reaching data/secrets), and **inter-tenant (cross-tenant) data exposure**
   likely requiring customer reporting. Back each with the impact tools
   (`get_incident_customer_impact`, `get_impacted_subscription_count`,
   `get_support_requests_crisit`, and the S500 / Priority-0 / ACE tools) from
   [icm-tools.md](icm-tools.md).
2. **Finder public-disclosure concern** — is the finder likely to disclose
   publicly **before** the fix ships? Answer from the case's own signals
   (`Public` flag, `CveNumber` / `PublicDisclosureDate`, `RecommendedResolution`,
   and any embargo / deadline / "go public" language in the discussion). If the
   product repo is public, note the patch-gap / patch-diff risk on merge — but
   keep that **separate** from *finder intent* (it doesn't by itself make the
   answer "yes").

Use the *Escalation & disclosure gates* table in
[verdict-rubric.md](verdict-rubric.md). Do not apply a blanket "no" to all four
gates. For self-hosted code, tenant→service and inter-tenant gates are
structurally not applicable unless a Microsoft-operated boundary is also
involved. Assess active exploitation and finder disclosure from evidence; do not
infer either answer from the deployment model or missing telemetry. Mark a gate
unknown when evidence is unavailable. Any genuine "yes" on a SSIRP gate means
stop and flag SSIRP / incident escalation; a "yes" on the disclosure gate means
tell the user to contact the MSRC case owner via IcM (or email if IcM is
unavailable).

### Phase 5 — Verdict
Classify (see [verdict-rubric.md](verdict-rubric.md)):
`Real-Exploitable` · `Real-Low-Impact` · `Developer-Footgun` · `Already-Fixed`
· `False-Positive` · `Mischaracterized`.

State **actionability**. If actionable, describe the **best fix target** — the
minimal correct fix plus defense-in-depth (prefer *fail-loud* over silent; push
validation to build/config time). **Recommend only — do not implement.**

### Phase 6 — Draft the MSRC response
Pick the matching template in [response-templates.md](response-templates.md).
Every response: **acknowledge accurate parts → cite evidence → scope down impact
with reasoning → propose closure state (+ CVE recommendation).**

## Deliverable format

Present to the user:

1. **Case header** — ID, VULN#, title, MSRC severity/impact, finder.
2. **The claim** — one sentence.
3. **Findings** — code reality (with `file:line`), timeline result (fixed?
   which PR/commit?), deployment model (self-hosted vs. MS-operated),
   exploitability analysis.
4. **Verdict** — one of the six categories + actionability + fix target if any.
5. **Escalation & disclosure gates** *(ALWAYS include — all four)* — a table
   across the three SSIRP gates (active exploitation, tenant→service,
   inter-tenant) **and** the finder public-disclosure gate. Mark each Yes, No,
   Unknown, or N/A with a one-line evidence-cited justification. For
   self-hosted code, tenant→service and inter-tenant are N/A unless a
   Microsoft-operated boundary is involved; assess the other gates from case
   evidence. Call out any patch-gap / merge-timing caveat separately from finder
   intent. A genuine "yes" on any SSIRP gate → flag SSIRP escalation; "yes" on
   disclosure → contact the MSRC case owner.
6. **Drafted MSRC response** — ready to paste, in a quoted block.

Keep it tight and evidence-dense. The user should be able to act on it without
re-opening the case.
