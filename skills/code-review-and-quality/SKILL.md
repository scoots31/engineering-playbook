---
name: code-review-and-quality
description: Seven-check quality gate that runs automatically when solo-build marks a slice code-complete. Checks pattern compliance, data sourcing, expandability, cleanliness, scope discipline, documentation, and stack compliance. On pass: logs confirmation in the backlog slice detail and automatically invokes solo-qa. On fail: returns specific notes, slice goes back to In Build.
---

# Code Review and Quality

*Seven checks. All must pass. No exceptions, no partial passes.*

**Triggered by:** solo-build on code-complete. Never invoked manually.

**Input required:** the slice ID and the committed code. The four anchors (design, data, done, process) are read from the backlog before checks begin.

---

## Before Running Checks

Read the backlog entry for the slice. Confirm all four anchors are present:
- Design anchor: the screen file and element this slice implements
- Data anchor: the mock data fields this slice consumes
- Done anchor: the 2–3 criteria that close this slice
- Process anchor: the to-be step this slice implements

If any anchor is missing from the backlog, stop:
> "Code review cannot run — the [anchor name] anchor is missing from the backlog entry for SL-[ID]. Resolve the anchor and resubmit."

---

## The Seven Checks

Run all seven. Each returns ✅ pass or ❌ fail with a specific note.

### Check 1 — Pattern compliance
Does this slice follow the patterns already established in the project? Look for: component structure, naming conventions, state management approach, how data flows from the mock layer to the UI. A slice that invents a new pattern where an existing one fits is a fail.

**Pass:** Implementation follows established project patterns.  
**Fail:** Names the specific divergence and which existing pattern should have been followed.

### Check 2 — Data sourcing
Are all displayed values traced to the mock data layer? Open the data anchor file. Verify every value shown in the UI comes from the mock layer — not from hardcoded strings or inline objects in the component.

**Pass:** Every displayed value has a traceable source in the mock layer.  
**Fail:** Names the specific hardcoded value and the mock field it should come from.

### Check 3 — Expandability
Is this slice built to accommodate what's coming, not just today? Look for: data structures that can accommodate the fields that will arrive in later phases, component interfaces that don't assume single-use. Not over-engineering — just not boxing out the next slice.

**Pass:** No structural choices that will require rework in the next 2–3 slices.  
**Fail:** Names the specific decision that creates the rework risk and what the low-cost alternative is.

### Check 4 — Cleanliness
No debug artifacts. No dead code. No commented-out experiments. No console.log / print / dump statements. No TODO comments left in (surface them to the backlog instead).

**Pass:** Code is clean — only what's needed for this slice.  
**Fail:** Names the specific artifact and line.

### Check 5 — Scope discipline
Did the slice build exactly what the done criteria ask for — no more, no less? Extra features added "while we're here" are a fail. Underimplemented done criteria are a fail.

**Pass:** Implementation matches the done criteria exactly.  
**Fail:** Names what was added beyond scope, or which done criterion is missing coverage.

### Check 6 — Documentation
Non-obvious behavior is commented. Complex logic has a one-line explanation of why, not what. Tradeoffs made during build are named. Anything a future reader would be surprised by is noted.

**Pass:** Non-obvious behavior is explained in the code.  
**Fail:** Names the specific logic that needs a comment and why it's non-obvious.

### Check 7 — Stack compliance
Does the slice follow the standards in `docs/tech-context.md`? Look for: correct use of the specified framework, no unapproved dependencies, architecture decisions consistent with what tech-context establishes.

**Pass:** Slice is compliant with tech-context standards.  
**Fail:** Names the specific deviation and the tech-context rule it violates.

---

## Output

**Report format — always surface this:**

```
Code review — SL-[ID] [slice name]

Check 1 — Pattern compliance    ✅ / ❌
Check 2 — Data sourcing         ✅ / ❌
Check 3 — Expandability         ✅ / ❌
Check 4 — Cleanliness           ✅ / ❌
Check 5 — Scope discipline      ✅ / ❌
Check 6 — Documentation         ✅ / ❌
Check 7 — Stack compliance      ✅ / ❌
```

For each ❌: one sentence naming the specific problem and what the fix is.

---

**On pass (all 7 ✅):**

Update the backlog entry for SL-[ID]:
> Code review passed — [date]

Then invoke solo-qa immediately. Do not wait for the solo to trigger it.

**On fail (any ❌):**

Do not invoke solo-qa. State the failures clearly:
> "SL-[ID] did not pass code review. [N] check(s) failed:
> - Check [N]: [specific problem and fix]
>
> Slice is back In Build. Fix the flagged items and code-complete again."

Update the backlog: slice status → `In Build`.

---

## Session Signals

Passive telemetry. When any of the following events occur, append one line to `.claude/session-signals.tmp` at the project root. Create the file if it doesn't exist. One line per event.

**Trigger events:**
- Code review failed — any check returned ❌

**Format:**
```
YYYY-MM-DD | [git user name] | [project name] | build | code review failed
```

**How to write the signal:**
```
/bin/zsh -c 'echo "$(date +%Y-%m-%d) | $(git config user.name) | [project] | build | code review failed" >> .claude/session-signals.tmp'
```

Get the project name from `docs/continuity/handoff.md` or the project directory name. Write the signal immediately after logging the failure — before returning the slice to build.
