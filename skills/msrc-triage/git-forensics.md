# Git timeline forensics

**The highest-leverage step in the whole triage.** Many MSRC submissions are
static source reviews of a *public* repo. By the time you look, the code may have
been refactored or fixed. Before analysing exploitability, answer:

> **Is the code today the same code the reporter reviewed — and if not, was the
> reported behaviour already fixed?**

## Inputs you need
- The affected `path/to/file` (from the case title).
- `CaseCreationDate` and `LastModificationDate` (from `MsrcCaseDetails`).

## Step 1 — History of the file
```powershell
git --no-pager log --oneline --follow -- <path>
```
`--follow` survives renames/moves. Note the commit dates.

## Step 2 — Compare dates
Line up commit dates against `CaseCreationDate`:
- **No commits after the case opened** ⇒ current code ≈ reviewed code. Analyse
  the current code directly.
- **A commit landed after the case opened** ⇒ **suspect already-fixed or
  refactored.** Proceed to Step 3 and compare the commit date with the case
  creation and last-modification dates.

```powershell
git --no-pager show -s --format='%H%nAuthorDate: %ad%nCommitDate: %cd%nSubject: %s' <commit>
```

## Step 3 — Reconstruct the pre-report code
Look at the file **as it was just before** the suspicious commit:
```powershell
git --no-pager show <commit>~1:<path> > $env:TEMP\pre.txt
```
Then locate the cited function in `pre.txt` and compare it to `HEAD`. You're
looking for a behavioural flip — e.g. `return True` (fail-open) becoming
`return False` (fail-closed), a missing check being added, an unsafe sink being
removed.

Tip: grep the old file for the function/keywords before reading:
```powershell
Select-String -Path $env:TEMP\pre.txt -Pattern 'def <fn>|return True|return False|except|await'
```

## Step 4 — Date the current line
Confirm when the current (possibly fixed) behaviour was introduced:
```powershell
git --no-pager blame -L <start>,<end> <path>
```
Cross-check the blame commit/PR and its date against the case timeline.

## Step 5 — Find the regression test
A real fix usually ships a test. Search the package's tests for the function or
the behaviour:
```
grep for: <function_name>, the warning string, "not traversed" / "fail" / the CWE keyword
```
If a test asserts the *secure* behaviour, cite it in the response — it's strong
evidence the fix is intentional and locked in.

## Interpreting the result

| Timeline finding | Verdict implication |
| ---------------- | ------------------- |
| Fixing commit **after** case date, behaviour flipped to safe, test present | **Already-Fixed.** Cite PR/commit/test; request closure as Fixed. |
| No relevant change; code still matches the claim | Proceed to full exploitability analysis (Phase 4). The issue is *live* if exploitable. |
| Code was refactored but behaviour unchanged | Note the move (avoid citing stale paths); analyse current behaviour. |
| File/function no longer exists | Confirm removal commit; likely Already-Fixed / not-applicable. |

## Cautions
- The cited path may be a **re-export wrapper** now; the real logic (and its
  history) may live elsewhere. Run the history commands on the file that holds
  the *actual* implementation.
- Distinguish **author date** from **commit date**; use commit date for "when it
  landed on the branch you're reviewing."
- Cross-fork MSRC cases: make sure you're on the branch/remote that actually
  ships to the affected consumers.
