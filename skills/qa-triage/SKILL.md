---
name: qa-triage
description: Routes unexpected discoveries from testing — bugs, missing requirements, and regressions — to the correct path without derailing active build momentum. Invoked from solo-qa when testing surfaces something that isn't a clean pass or a simple build fix. Can also be invoked directly when the solo spots something outside of a formal QA session.
---

# QA Triage

*Something unexpected surfaced. Don't guess at the path — classify it first, then route it.*

**Core question:** "What exactly was found, where does it live, and what's the right response that doesn't derail what's in flight?"

This skill runs when testing reveals something that isn't covered by solo-qa's two standard outcomes (pass → Done, or fail → back to In Build). Three types of unexpected discovery need their own paths: bugs, missing requirements, and regressions. Treating them the same creates bad fixes — or stalls the build entirely.

---

## When This Runs

Invoked from solo-qa when the solo's sign-off surfaces something unexpected. Also invokable directly when the solo notices something during build, while using the product post-deploy, or any other moment outside the formal QA session.

---

## Step 1 — Classify What Was Found

Three types. Get this right before doing anything else.

**Bug**
The behavior is defined. The implementation doesn't match it. Something was built but doesn't work correctly. The spec exists — the code doesn't follow it.

*Examples: a value displays incorrectly, an interaction doesn't respond, a state doesn't update, an edge case from mock data crashes the component.*

**Missing Requirement**
The behavior was never defined. Nobody specified what should happen here. The implementation may be reasonable — but it was never agreed on. This is a specification gap, not a code defect.

*Examples: the solo looks at an empty state and realizes there's no design for it, a user action leads somewhere that was never discussed, a field behavior in an edge case was assumed but never written down.*

**Regression**
Something that was previously Done and working is now broken. A later slice, a shared component change, or a dependency update caused a slice that passed QA to stop working correctly.

*Examples: a Done slice's data no longer renders after a shared hook was changed, a previously passing interaction breaks after a new screen was added to the navigation.*

---

## Step 2 — Determine Scope

Where does this live and how far does it reach?

| Scope | Meaning |
|-------|---------|
| **Current slice** | Only affects the slice currently in QA |
| **Done slice** | Affects a slice already marked Done |
| **Unbuilt slice** | Relevant to a slice not yet in build |
| **Adjacent slices** | Affects 2–3 slices in the same screen or flow |
| **Flow-level** | Affects a user journey across multiple screens |

---

## Step 3 — Route

**Bugs:**

| Scope | Action |
|-------|--------|
| Current slice | Return to In Build. Specific note — what's wrong and what correct behavior looks like. Re-run full QA chain (code-review-and-quality → solo-qa) when fixed. |
| Done slice (standalone) | Reopen that slice in the backlog: status → In Build. Note what's broken, what caused it, and what the fix needs to achieve. It goes through the full QA chain again before returning to Done. |
| Unbuilt slice | Add a note to that slice's backlog record before it enters build. Continue current QA. Don't pause anything. |
| Adjacent slices | Assess whether the fix for one requires changes to the others before fixing. If yes — fix together, QA together. If no — fix the affected slice, continue with the others. |
| Flow-level | Flag for design review. A flow-level bug usually means something was misunderstood at the design stage, not just implemented incorrectly. Don't try to fix it in QA. |

**Before reopening a Done slice: assess scope.**

When a Done slice bug requires a reopen, assess before marking it In Build: is this a targeted fix or a full rebuild?

- **Targeted fix** — the approach is sound; a specific behavior doesn't work. Proceed: reopen → fix → full QA chain.
- **Full rebuild** — the approach is structurally wrong: wrong design interpretation, architecture that doesn't fit the requirement, wrong assumptions baked in at build start. Surface this to the solo before touching any status. The rollback protocol applies — builder proposes, solo confirms, status cascade and log entry follow.

The distinction matters. A targeted fix goes through the standard QA chain. A full rebuild discards the slice's code and restarts from the spec.

**Missing Requirements:**

| Scope | Action |
|-------|--------|
| Small gap — 1 behavior, current slice | Define it now. Add to the slice's done criteria. Verify it before solo sign-off. Don't make the solo sign off on something with an undefined edge case. |
| Larger gap — slice-level behavior | Create a new slice in the backlog. Current slice ships with an explicit scope note: *"[behavior] deferred to SL-[new ID]."* Solo sign-off proceeds with that scope boundary acknowledged. |
| Multiple slices / a screen | Design review trigger. Pause QA on affected slices. Don't define slice-spanning requirements in a QA session — that's design review's job. |
| Flow-level | Design review trigger. A flow-level missing requirement means the discovery brief or design sprint didn't surface something important. It needs a real conversation, not a quick fix. |
| Map-level gap — the to-be map has no step covering this behavior at all | Invoke `process-change`. This is not a missing requirement within the agreed process — the process itself is incomplete. Process change runs before QA resumes on the affected slice. |

**Regressions:**

| Scope | Action |
|-------|--------|
| Single Done slice | Reopen it. Status → In Build. Root cause note required — what changed that broke it, not just what's broken. Re-run full QA chain before returning to Done. |
| Multiple Done slices | Identify the shared cause first. Fix the root (usually a shared component or hook), then re-QA affected slices together. Don't patch each slice individually if they share a cause. |
| Widespread | Flag immediately before touching anything. Widespread regressions usually mean a shared dependency was changed in a way that breaks assumptions. Diagnose the root, assess the blast radius, then fix from the root outward. |

---

## Step 4 — Document Every Triage Decision

Every triage outcome gets logged in `docs/backlog.md` — in the slice record where it originated, or as a new entry if it generates a new slice.

Format:

```
QA Triage — [date]
Type: [Bug / Missing Requirement / Regression]
Found during: [SL-ID QA sign-off / build / post-deploy]
What was found: [specific description]
Classification: [why this type, not another]
Scope: [current slice / Done slice / unbuilt / adjacent / flow]
Action taken: [exactly what was done and why]
```

This log exists so the next session doesn't have to reconstruct what happened and why a decision was made. Triage decisions that aren't documented get relitigated.

---

## The Triage Principles

**Fix the right thing, not the nearest thing.**
A missing requirement that gets patched as a bug fix produces code that solves the wrong problem. A regression that gets "fixed" in the current slice without finding the root cause reappears in the next build.

**Small scope → fix now. Large scope → pause and route.**
A one-behavior gap in the current slice can be defined and verified in minutes. A flow-level missing requirement cannot. Don't apply the same response to both.

**Momentum is worth protecting — but not at the cost of correctness.**
Triage is fast by design. It routes the discovery and gets out of the way. Bugs in unbuilt slices don't stop current QA. Missing requirements with clean scope boundaries don't stall the whole build. But flow-level issues deserve a real design review, not a quick patch that creates three more gaps.

**Every triage decision is logged.**
The solo builds context over many sessions. A triage decision made today affects what happens in three slices and two sessions from now. Log it.

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Fixing a missing requirement as if it were a bug | Produces code that solves the wrong problem | Classify first — is the behavior defined or not? |
| Defining flow-level requirements during QA | Wrong phase, wrong context | Trigger design review, pause affected slices |
| Patching a regression without finding the root cause | It comes back | Root cause first, then fix |
| Skipping the triage log | Next session starts from the wrong place | Document every decision, every time |
| Pausing all build work for an unbuilt-slice bug note | Unnecessary disruption | Note it, continue — it's not in flight yet |
| Solo sign-off on a slice with an open missing requirement | Undefined behavior ships as if intentional | Define or defer before sign-off |
