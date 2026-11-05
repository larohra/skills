# ICM tooling cheat-sheet

How to pull an MSRC/ICM case with the `icm-agency` MCP server and extract the
parts that matter. All tools take the **numeric incident ID**.

## Portal URL → incident ID
```
https://portal.microsofticm.com/imp/v5/incidents/details/<incident-id>/summary
                                                          ^^^^^^^^^^^^^
                                                          incident ID
```
The portal requires SSO — you **cannot** fetch it with `web_fetch`/browser
tools. Always go through the ICM MCP server (or ask the user to paste details).

## Which tools to call (and why)

| Tool | Use for | Notes |
| ---- | ------- | ----- |
| `get_incident_details_by_id` | **Primary.** Title, severity, state, tags, custom fields incl. `MsrcCaseDetails`. | Large JSON (~25–30 KB). Save to a temp file and grep rather than reading whole. |
| `get_ai_summary` | Quick machine summary | Often "No AI summary available" — fine. |
| `get_incident_context` | Bridge/discussion summaries, extra metadata | Often "No context available" — fine. |
| `get_mitigation_hints` | Suggested causes/mitigations, similar mitigated incidents | Usually empty for MSRC code-review cases. |
| `get_similar_incidents` | Related prior cases (variant hunting) | Useful to spot repeat patterns/finders. |
| `search_incidents` | Find related cases by team/service/keyword | Wrap all filters in `incidentAdvancedSearchRequest`. |

Don't block on the empty ones — record "not available" and move on. The signal
is almost always in `get_incident_details_by_id`.

## Impact & exploitation signals (for escalation / SSIRP questions)

Every verdict must answer the **escalation & disclosure gates** (active
exploitation, tenant→service compromise, inter-tenant exposure, and finder
public-disclosure) — see [verdict-rubric.md](verdict-rubric.md) → *Escalation &
disclosure gates*. The customer-impact tools give you evidence for the first
three instead of hand-waving. All take the numeric incident ID. If the tools
return an **all-zero** profile, cite it as evidence of no measured customer
impact; do not treat missing or denied data as zero. For self-hosted code,
Microsoft telemetry may not cover consumer deployments, which is not proof that
exploitation is absent. The fourth gate (disclosure) comes from the case
metadata — `Public` / `CveNumber` /
`PublicDisclosureDate` / `RecommendedResolution` (see `MsrcCaseDetails` below) —
not these impact tools.

| Tool | Use for | Notes |
| ---- | ------- | ----- |
| `get_incident_customer_impact` | One-shot roll-up: impacted clouds/regions/services, support-request & CritSit counts, subscription count. | Best first call for escalation questions. |
| `get_impacted_subscription_count` | Impacted subscription totals (auto-detected + comms). | 0 ⇒ no measured blast radius. |
| `get_support_requests_crisit` | Linked support tickets (SRs) and SevA/CritSit. | Any non-zero ⇒ real customers noticed; dig in. |
| `get_impacted_s500_customers` / `get_impacted_azure_priority0_customers` / `get_impacted_ace_customers` | Named high-value / Priority-0 / ACE customer impact. | Populated ⇒ escalate; empty ⇒ note it. |
| `is_specific_customer_impacted` | Check a named customer against the impact list. | "false" isn't proof of safety — cross-check SRs/CritSit. |
| `get_outage_high_priority_events` | High-priority events tied to an outage. | For outage-linked cases. |

Some impact tools may return **Permission denied** for your caller — record that
and rely on the ones that do answer (the roll-up + subscription/SR counts are
usually enough). See [verdict-rubric.md](verdict-rubric.md) → *Escalation &
disclosure gates* for how to turn these signals into a yes/no on each gate.

## Handling the big details payload
The details JSON is usually too large to read at once. Save and search:
```powershell
# after get_incident_details_by_id saved the output to a temp file:
Select-String -Path <tempfile> -Pattern 'MsrcCaseDetails|"title"|Severity|SecurityImpact'
```
Or read specific ranges with the `view` tool + `view_range`.

## The field that matters most: `MsrcCaseDetails`
Inside `customFields`, find the entry with `"Name":"MsrcCaseDetails"`. Its
`StringValue` is an escaped JSON blob.
Unescape and parse it. Key fields:

| Field | Meaning / how you use it |
| ----- | ------------------------ |
| `Title` | Affected `path/to/file` + one-line weakness. Your starting point for Phase 2. |
| `Severity` | MSRC's own rating (Low/Moderate/Important/Critical). Sanity-check your verdict against it. |
| `CaseNumber` | MSRC master case number. |
| `SubmissionNumber` | `VULN-####` — the external submission. |
| `SecurityImpact` | e.g. `SecurityFeatureBypass`, `RemoteCodeExecution`, `ElevationOfPrivilege`, `InformationDisclosure`. Frames the claimed class. |
| `CaseCreationDate` | **Critical for timeline forensics.** When the report was filed. |
| `LastModificationDate` | Last case update — upper bound for "reviewed code". |
| `RecommendedResolution` | e.g. "Fix in Next Version", "By Design". |
| `CveNumber` / `Public` / `PublicDisclosureDate` | CVE + disclosure status. |
| `CloudCritical` / `AzureHostImpact` | `NotDetermined` here usually signals limited/unassessed cloud impact. |
| `FinderOrganization` | External finder ("Unknown"/named org) vs internal. External + "Unknown" ⇒ likely a source-review submission. |
| `SpmOwner` / `ReactOwner` | MSRC-side owners, if you need to route questions. |
| `ReportedCWE` | The CWE the finder assigned, if any — compare to reality in Phase 4. |

## Extracting `MsrcCaseDetails` quickly
The blob is embedded with `\u0022` etc. Pull just that field and JSON-decode it,
e.g. with a short inline Python snippet reading the saved temp file, or by
grepping the `StringValue` and unescaping. Capture the table above into your
Phase 1 notes.

## What to record from Phase 1
A compact header you'll reuse in the final deliverable:
```
Incident: <id>   Case: <CaseNumber>   Submission: <VULN-####>
Title: <title>
MSRC: Severity=<..>  Impact=<..>  Recommended=<..>  CVE=<..>  Cloud=<CloudCritical>/<AzureHostImpact>
Finder: <FinderOrganization>
Dates: created=<CaseCreationDate>  lastMod=<LastModificationDate>
Claim (1 sentence): <...>
```
