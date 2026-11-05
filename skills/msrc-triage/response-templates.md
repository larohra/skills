# MSRC response templates

Draft a reply the user can paste into the case. **Always** hand it to the user;
never auto-post. Fill every `<placeholder>` with concrete evidence.

## Universal structure
1. **Acknowledge** the accurate part of the report (respect the finder's work).
2. **State findings with evidence** — `file:line`, commit SHA, PR#, test name,
   MSRC field values.
3. **Scope the impact** — correct any overstatement, with reasoning; separate
   *code claim* from *impact claim*.
4. **Propose a resolution + closure state**, and a **CVE recommendation** when
   relevant.

Tone: factual, precise, collegial. Never dismissive. Distinguish "we observed"
from "the report asserts".

---

## Template: Already-Fixed
> Thank you for the report (VULN-`<####>` / case `<CaseNumber>`). We confirm the
> described behaviour: `<one-line accurate summary of the code claim>` in
> `<path>`. This was remediated in PR **#`<pr>`** (commit `<sha>`, merged
> `<date>`), which changes the behaviour to `<safe behaviour>` and is covered by
> regression test `<test name/path>`.
>
> Scope note: `<if applicable, correct impact framing — e.g. the construct is
> application routing logic rather than a platform authorization control, and the
> path is only reachable via <trigger>, not attacker-controlled input>`, which is
> consistent with the `<Severity>` rating.
>
> As the fix is already in `<branch/release>`, we request closure as **Fixed**.
> `<CVE recommendation if any.>`

## Template: By-Design / Mischaracterized
> Thank you for the report (VULN-`<####>`). Your reading of the code is accurate:
> `<accurate code behaviour>` at `<file:line>`. However, `<construct>` is
> `<application/business logic — e.g. a workflow routing predicate / a
> developer-controlled config>`, not a `<claimed boundary, e.g. authorization>`
> boundary. Reaching the described outcome requires `<enumerate the
> developer-side / privileged preconditions>`, none of which are
> attacker-controllable, so this does not cross a security boundary.
>
> We're treating this as **By Design**. `<Optionally: we will add
> documentation/a fail-loud guard to reduce the footgun — as a hardening
> follow-up, not a security fix.>`

## Template: Needs-Fix (Real, low or moderate)
> Thank you for the report (VULN-`<####>`). We reproduce/confirm the issue:
> `<accurate description>` at `<file:line>`, reachable via `<trigger>`. Assessed
> impact: `<scoped impact>` (`<why it is / isn't higher — preconditions, blast
> radius>`).
>
> Planned remediation: `<the minimal correct fix + defense-in-depth: fail-loud,
> build-time validation, regression test>`, targeted for `<release/next
> version>`. We'll update the case with the PR link. `<CVE recommendation.>`

## Template: Developer-Footgun (hardening, not a vuln)
> Thanks for flagging this (VULN-`<####>`). The behaviour is real —
> `<description at file:line>` — but it can only be triggered by
> `<the developer authoring choice>`; there is no attacker-controlled input path,
> and `<e.g. a runtime warning is emitted>`. It's a usability/robustness sharp
> edge rather than an exploitable vulnerability.
>
> We'll harden it defensively (`<fail-loud / reject-at-build-time>`) as a
> non-security improvement and recommend closing the security case as
> **By Design / Not a Vulnerability**.

## Template: False-Positive
> Thank you for the submission (VULN-`<####>`). We investigated `<path>` at the
> version referenced. The described behaviour does not occur: `<what the code
> actually does, with file:line and, if relevant, the pre-report version from
> git history>`. `<E.g. the predicate fails closed / the input is never reached /
> the value is validated at line N.>`
>
> We're therefore closing this as **Not Reproducible / By Design**. We're happy
> to take another look if you can share a concrete repro against a specific
> commit.

---

## CVE recommendation snippets
- **No CVE:** "Given `<no untrusted-input path / already-fixed pre-disclosure /
  not a security boundary>`, we do not believe a CVE is warranted."
- **CVE warranted:** "We will assign a CVE and coordinate disclosure; target
  release `<...>`."

## Before you hand it over — checklist
- [ ] Every claim cites `file:line`, a SHA, a PR#, a test, or an MSRC field.
- [ ] Accurate parts acknowledged **before** any scoping-down.
- [ ] Code claim and impact claim addressed **separately**.
- [ ] Proposed closure state is explicit (Fixed / By Design / Needs-Fix /
      Not Reproducible).
- [ ] CVE stance stated when relevant.
- [ ] No product code was modified by this skill.
