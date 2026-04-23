---
name: bug-fix
description: Fix a production bug correctly — reproduce first, find the root cause, make the smallest fix, verify nothing adjacent broke, deploy. For issues in live systems, not for development-time errors caught before deploy.
---

# Bug Fix

*Reproduce before touching anything. Root cause before writing code.*

**Core question:** "What's actually broken, why is it broken, and what's the smallest change that fixes it without breaking anything else?"

This skill is for production issues — something that was working and now isn't, or something that never worked correctly in the live environment. It is not for development-time errors or pre-deploy issues (those surface through solo-qa and phase-test).

---

## Step 1 — Reproduce

Before reading any code, reproduce the bug. If you can't reproduce it, you don't have a bug — you have a report.

- What exact steps trigger it?
- Is it consistent or intermittent?
- What environment — prod only? All environments?
- Who is affected — all users, specific accounts, specific data shapes?

State the reproduction recipe in one paragraph. If you can't write it, the bug isn't understood yet.

> "Cannot reproduce: [what was tried]. Before proceeding — [one specific question that would help isolate it]."

---

## Step 2 — Isolate the Root Cause

The symptom and the root cause are different things. Fixing the symptom brings the bug back.

Read the code. Find where the symptom originates. Then ask: **why does the code do that?**

Common root cause types:

| Type | Signal |
|---|---|
| **Logic error** | Condition evaluates incorrectly, edge case not handled |
| **Data assumption** | Code assumed data shape that production data violates |
| **State problem** | Order of operations issue, race condition, stale data |
| **Integration failure** | API, DB, or external service behaving differently than expected |
| **Config drift** | Production environment differs from development in a meaningful way |

Name the root cause explicitly before touching code:
> "Root cause: [what and why]. The fix is at [specific location]."

---

## Step 3 — Make the Smallest Fix

The fix should touch as little code as possible. Production is live. Every line changed is a line that can introduce a new problem.

- Fix the root cause, not the symptom
- Do not refactor while fixing — note refactor opportunities, execute them separately
- Do not improve adjacent code — scope is the bug, nothing else
- If the fix requires significant refactoring to implement cleanly, surface it: "The clean fix requires refactoring X — do you want the minimal fix now + a separate slice for the cleanup?"

---

## Step 4 — Regression Check

Before declaring the fix done, verify nothing adjacent broke.

- Run the reproduction steps — confirm the bug is gone
- Run any existing tests that touch this code path
- Manually walk any feature that shares code with the fix
- Check edge cases the bug revealed (if the bug was a data assumption, check other places the same assumption was made)

Format:
```
✅ Bug reproduction: [steps] → no longer triggers
✅ Adjacent: [feature/path] — unaffected
✅ Edge cases: [what was checked]
```

---

## Step 5 — Deploy

Read `docs/tech-context.md` for the deploy method. Follow the same deploy path as the framework.

Production fix deploy discipline:
- Commit message: `fix: [what was broken] — root cause: [one line]`
- Deploy the fix alone — do not bundle with other changes
- Verify in production after deploy — confirm the bug is gone in the live environment, not just locally

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Fixing before reproducing | May be fixing the wrong thing | Reproduce first — always |
| Fixing the symptom | Bug comes back | Find and fix the root cause |
| Refactoring while fixing | Expands blast radius | Note it, fix it separately |
| Bundling with other changes | Can't isolate regressions | Deploy the fix alone |
| Not verifying in production | Fix works locally, broken in prod | Verify in the live environment after deploy |
| Skipping the regression check | Fix introduces a new bug | Walk adjacent paths before declaring done |
