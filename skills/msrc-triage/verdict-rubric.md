# Verdict rubric — is it real, and how bad?

Use after you've read the code (Phase 2) and run the timeline (Phase 3). Work
the tests below, then pick a verdict category.

## Test 0 — What's the deployment model?
Ask this **first**, because it bounds every impact claim: is the affected code a
**self-hosted library / SDK / sample** that developers deploy into *their own*
subscription and tenant, or a **Microsoft-operated (multi-tenant) service**?

| Deployment model | What it means for impact |
| ---------------- | ------------------------ |
| **Self-hosted library / SDK** (an OSS framework package, a NuGet/PyPI module, a sample app) | Blast radius is confined to a single consumer's own deployment. There is **no Microsoft service boundary and no inter-tenant boundary** at this layer, so the SSIRP/escalation gates (active exploitation, tenant→service compromise, cross-tenant exposure) are structurally **N/A** — per-user/tenant isolation is the *consumer's* responsibility. Microsoft also has **no telemetry** on consumer self-hosted deployments, so "active exploitation" can't be observed centrally. |
| **Microsoft-operated service** | Microsoft owns the trust boundaries. Escalation gates genuinely apply; pull the impact tools and answer each explicitly. |

> For a self-hosted library, the relevant impact boundary is the consumer's own
> deployment. Naming the model up front prevents a framework-level issue from
> being overstated as a Microsoft-operated service compromise.

Record the model in one line; it feeds directly into *Escalation & disclosure
gates* below.

## Test 1 — Is this a real security boundary?
A weakness only matters if it crosses a boundary the system is *supposed* to
enforce. Ask: **what boundary does the reporter claim is breached?**

Genuine security boundaries / sinks:
- **AuthN** (identity), **AuthZ** (permission), **tenant/user isolation**
- **Crypto** (weak/again-used keys, bad randomness, missing verification)
- **Deserialization** of untrusted data (pickle, YAML, etc.)
- **Injection sinks** (SQL/shell/template/XPath), **path traversal**, **SSRF**
- **Secret exposure**, **privilege escalation**

Frequently **mislabeled** as security (usually app/business logic):
- Workflow/graph **routing predicates**, feature flags, retry/branch conditions
- Input *validation* that is UX/robustness, not a trust boundary
- Config a developer fully controls in their own process

> Example: a **workflow routing predicate** may be framed as an "AuthZ bypass".
> Routing predicates decide which executor handles a message; they are
> application logic, not necessarily a platform authorization control. Validate
> the code claim, then independently establish whether it guards a real boundary.

**Shared-key management endpoints & "IDOR".** An access-control / IDOR claim only
crosses a boundary if the system has a **per-user identity model** to bypass.
Control-plane / management endpoints protected by a single shared secret (e.g.
Azure Functions `AuthLevel.FUNCTION` = one function key for all callers) are a
**single trust boundary**: every key-holder is equally authorized, so "user A
reads user B's object" isn't meaningful unless the *app* layers its own identity.
Treat these as `Mischaracterized` / `By-Design` at the framework layer, and note
that per-user isolation is the consumer's responsibility. Also check the IDs are
unguessable (e.g. server-generated random GUIDs), which defeats enumeration.

If it's not a real boundary → lean `Mischaracterized` (still validate the code
claim honestly).

## Test 2 — What actually triggers it?
| Trigger | Meaning | Severity pull |
| ------- | ------- | ------------- |
| **Attacker-controlled input** (remote, unauthenticated) | Real external vector | ↑↑ |
| Authenticated-but-low-priv input | Real, needs an account | ↑ |
| **Developer authoring choice** (e.g. writes an async predicate, sets a flag) | *Footgun*, not an attack — no external actor can force it | ↓↓ |
| **Requires elevated privilege / admin on another component** | Premise self-defeating: if the attacker already has that, the system is compromised regardless | ↓↓↓ |

No path from **untrusted input** to the sink ⇒ not a practical vulnerability,
however ugly the code.

## Test 3 — Count the preconditions
List every condition that must hold **simultaneously** for impact. For example:
1. Developer uses an edge condition **as a security gate**, AND
2. that condition is **async**, AND
3. the behavior is reachable in the runtime and version consumers actually use.

These are independent conditions, all developer-side and none attacker-forcible,
which points toward a footgun rather than an external attack. The more
conjunctive, developer-side preconditions, the less plausible the attack.

## Test 4 — Fail-open vs fail-closed (for the exact path)
- **Fail-open** = on error/unknown, access/flow is *allowed*. Genuinely risky
  *if* it guards a real boundary.
- **Fail-closed** = on error/unknown, access/flow is *denied*. Safe default.

Confirm which the code actually does **at HEAD** (timeline may have flipped it).
State it with `file:line`.

## Cross-checks
- **Reporter's CWE / framing vs reality** — do they match? Note overstatement.
- **MSRC's own fields** — `Severity`, `CloudCritical`, `AzureHostImpact`, `CVE`.
  `Low` + `NotDetermined` + no CVE + "Fix in Next Version" corroborates a
  limited-impact finding. If your analysis wildly disagrees with MSRC's rating in
  *either* direction, re-check your work and call it out explicitly.
- **Observed exploit vs code review** — is there a working PoC, or is this a
  static reading? Say so.

## Escalation & disclosure gates (SSIRP / customer-reporting)
MSRC triage always asks a second question beyond "is it real?": **does this need
to be escalated** to a security incident or customer notification, and **could
the finder go public before the fix ships?** These **four gates are mandatory in
every verdict** — MSRC's plan-of-action form requires them — so address each
explicitly. Use Yes / No / Unknown / N/A according to the available evidence.
Back the first three with the impact tools in [icm-tools.md](icm-tools.md) →
*Impact & exploitation signals* and Test 0; back the fourth from the case's
disclosure metadata (`Public`,
`CveNumber` / `PublicDisclosureDate`, `RecommendedResolution`, and any
embargo/deadline language in the discussion).

| Gate | Answer "yes" only if… | Evidence to assess |
| ---- | --------------------- | -------------------------------------------------- |
| **Active exploitation** (telemetry, logs, any source) | Concrete evidence of a live attack — non-zero support requests / CritSit, an observed PoC in the wild, or detection telemetry. | Assess available telemetry, reports, and public evidence. Missing telemetry is not proof of no exploitation; mark Unknown if evidence is unavailable. |
| **Tenant→service boundary breach → service compromise (data/secrets)** | An unauthorized party crossed into a **Microsoft-operated** service and reached data/secrets. | N/A for self-hosted code unless a Microsoft-operated boundary is also involved; otherwise cite the service impact evidence. |
| **Inter-tenant boundary failure → cross-tenant exposure, likely customer-reportable** | Data crosses between **different customers' tenants** across a Microsoft-managed boundary. | N/A for self-hosted code unless a Microsoft-managed multi-tenant boundary is also involved; assess evidence for any such boundary. |
| **Finder public disclosure before fix** | The **finder** signals intent to publish before the fix ships — an embargo/deadline, a "going public" statement, a reserved/public CVE, or `Public: true` / a set `PublicDisclosureDate`. | Assess the case metadata and discussion. Absence of a disclosure signal may support No; deployment model alone does not establish finder intent. |

Rules of thumb:
- **Answer all four every time** — they're required by MSRC's plan-of-action
  form. Use Yes / No / Unknown / N/A as supported by evidence; do not turn
  missing information into No.
- For self-hosted libraries, tenant→service and inter-tenant gates are
  structurally N/A unless a Microsoft-operated boundary is also involved.
  Active exploitation and finder disclosure remain evidence-based; neither is
  ruled out by the deployment model.
- A **non-zero** support-request / CritSit / S500 / Priority-0 count flips the
  posture — investigate before answering.
- Separate **"could a consumer misuse it to expose their own users"** (app-layer
  risk → guidance) from **"does a Microsoft boundary fail"** (the actual gate).
- **Disclosure gate is about the *finder*, not the repo.** A public product repo
  creates patch-diff / patch-gap risk once the fix merges — flag it and
  recommend coordinating merge timing with the case owner — but that's *separate*
  from the finder threatening early disclosure. Answer "yes" only on real finder
  intent (embargo/deadline, reserved/public CVE, `Public: true`).
- If any **SSIRP** gate is genuinely "yes", stop and tell the user it needs
  SSIRP / incident escalation — that's beyond a normal case response. If the
  **disclosure** gate is "yes", tell the user to contact the MSRC case owner via
  IcM (or email if IcM is unavailable).

## Verdict categories
Pick one (a case can be e.g. *Already-Fixed* **and** *Mischaracterized* — lead
with the most decision-relevant):

| Verdict | When | Typical response template |
| ------- | ---- | ------------------------- |
| **Real-Exploitable** | Real boundary + untrusted-input trigger + preconditions plausible + present at HEAD | Needs-Fix (+ likely CVE) |
| **Real-Low-Impact** | Real boundary but limited trigger/impact/preconditions | Needs-Fix or Fix-Next-Version |
| **Developer-Footgun** | Only a developer can trigger it; no external actor | By-Design or Needs-Fix (fail-loud hardening) |
| **Already-Fixed** | Timeline shows behaviour remediated before/independently | Already-Fixed |
| **Mischaracterized** | Code claim accurate but boundary/impact overstated | By-Design or Already-Fixed, with scope correction |
| **False-Positive** | Code claim itself is wrong (path exists but behaviour isn't as described) | False-Positive |

## Actionability & fix targeting (recommend only — never implement)
If actionable, describe the **minimal correct fix** and **defense-in-depth**:
- Prefer **fail-loud over silent**: raise/reject rather than silently drop or
  allow.
- Push checks to **build/validation/config time** so misuse is caught early
  (e.g. reject unsupported constructs when the workflow/graph is compiled).
- Add/adjust a **regression test** that locks in the safe behaviour.
- Note whether a fix already exists (from Phase 3) so effort isn't duplicated.

Remember the scope guardrail: you *recommend* these; you do not edit product
code in this skill.
