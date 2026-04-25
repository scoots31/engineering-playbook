---
name: process-change
description: Consistent protocol for handling changes to the agreed to-be process map — regardless of where the change surfaces or what caused it. Invoked directly by the solo or auto-detected by solo-build, qa-triage, or phase-test when a map-level conflict is found. Seven steps: capture trigger → document change → three-tier impact scan → solo decides → execute → re-prioritize → solo confirms.
---

# Process Change

*The process map is the contract. When it needs to change, change it deliberately — not silently.*

**Core question:** "What changed in the process, what does it touch across everything in flight, and what's the new sequence once we absorb it?"

This skill exists because process map changes are inevitable — and where they surface is unpredictable. A stakeholder emails a new requirement. A demo reveals a gap nobody could see until something was built. A developer hits a technical constraint that makes a agreed step impossible. A solo review of completed work reveals the original step was misunderstood.

The source doesn't matter. The protocol is always the same.

---

## When This Runs

**Solo-invoked:** The solo realizes the to-be map needs to change and invokes this skill directly.

**Framework-detected:** Three skills auto-detect a map-level conflict and invoke this skill:

- **solo-build** — discovers during build that the to-be map itself is wrong (not a design gap, not a dependency issue — the process step the slice is anchored to is incorrect or missing)
- **qa-triage** — surfaces a missing requirement where the to-be map has no step covering the behavior at all
- **phase-test** — acceptance reviewer determines the built experience doesn't match the discovery intent at the process level

In all cases, the current work pauses. Process change runs to completion before anything resumes.

---

## Step 0 — Gate Check

Before anything else: confirm the to-be process map exists.

Read `docs/process/to-be-[name].md`. If it doesn't exist, stop:

> "No to-be process map found. Process change requires an agreed process to change. Run discover first to establish the to-be map, then return here."

If the to-be map exists, continue.

---

## Step 1 — Capture the Trigger

Document what surfaced the need for this change before anything else. Four source types:

| Source | Description |
|--------|-------------|
| **Stakeholder input** | External party communicated a change — email, Slack, meeting, comment on a document |
| **Demo gap** | Stakeholder or solo viewed a working build and identified a mismatch between expectation and reality |
| **Technical constraint** | Build or technical review revealed that an agreed step cannot be implemented as designed |
| **Solo realization** | Solo recognized — during build, QA, or review — that the process was described or understood incorrectly |

Log the trigger immediately in product-continuity:

```
Process Change Trigger — [date]
Source: [Stakeholder input / Demo gap / Technical constraint / Solo realization]
What surfaced: [specific description — what was said, shown, or discovered]
Invoking skill: [solo-build / qa-triage / phase-test / direct]
```

This log entry is permanent. Even if the decision is to absorb the change with no map update, the trigger is recorded.

---

## Step 2 — Document the Change

State precisely what is changing in the to-be process map. Three change types:

**Refinement** — an existing step is modified. The step exists, the intent was right, the description was wrong or incomplete.

**Addition** — a new step must be added. Something was missing from the map entirely.

**Restructure** — the sequence, branching, or flow of steps changes. Steps may move, merge, split, or be reordered.

Present the change to the solo in this format:

```
Process Change — [Change Type]

Current step (or gap location): [exact text from to-be map, or "no step exists for this behavior"]

Proposed change: [what the step should say / where the new step goes / how the structure shifts]

Why this change: [the trigger from Step 1, stated plainly]
```

Wait for solo confirmation before proceeding. The solo must agree to the change before the impact scan runs — running an impact scan on an unapproved change wastes time and creates confusion.

---

## Step 3 — Three-Tier Impact Scan

With the change confirmed, scan all work across three tiers. Every item in each tier gets an explicit verdict — nothing is assumed safe.

### Tier 1 — Scheduled work (Ready / Blocked / Deferred)

Slices not yet in build. These are the easiest to adjust — they haven't been built yet.

For each Ready, Blocked, or Deferred slice:
- Does it trace to the changed step via its process anchor?
- Does the change affect what it needs to build?

**Verdict per slice:** Still valid as-is · Needs updated process anchor · Needs updated scope · Remove from backlog (step no longer exists) · New slice required

### Tier 2 — In-progress work (In Build / In QA)

Work actively underway. These require the most care — partially-built or verified work may need to be revised.

For each In Build or In QA slice:
- Is its process anchor the step that changed?
- Does the change affect what's being built right now?

**Verdict per slice:** Continue as-is · Pause, update scope, resume · Move back to In Review, redefine before continuing

### Tier 3 — Completed work (Done / Accepted)

Slices already verified and deliverables already accepted. Do not assume these are safe — a process change can retroactively affect completed work.

For each Done slice and Accepted deliverable:
- Did it implement the step that changed?
- Does the change mean the completed work is now incorrect?

**Verdict per slice/deliverable:** Still valid · Reopen — needs rework before phase test · Note for phase test — phase-test acceptance reviewer will re-assess

Present the full scan as a table before moving to Step 4:

```
Impact Scan — [Change Type] affecting [step name]

Tier 1 — Scheduled
| Slice | Status | Process Anchor Match | Verdict |
|-------|--------|---------------------|---------|
| SL-004 | Ready | ✓ Direct match | Needs updated scope |
| SL-007 | Blocked | — | Still valid |

Tier 2 — In Progress
| Slice | Status | Process Anchor Match | Verdict |
|-------|--------|---------------------|---------|
| SL-003 | In Build | ✓ Direct match | Pause, update scope, resume |

Tier 3 — Completed
| Slice/Deliverable | Status | Process Anchor Match | Verdict |
|-------------------|--------|---------------------|---------|
| SL-001 | Done | ✓ Direct match | Still valid |
| D-001 — [Name] | Accepted | — | Still valid |
```

---

## Step 4 — Solo Decides

Present the scan. Wait for the solo to make explicit decisions on every item that isn't "still valid."

Decision options per affected item:

| Decision | Meaning |
|----------|---------|
| **Revise** | Update the slice scope, process anchor, or done criteria — keep it in the backlog |
| **Retire** | Remove the slice from the backlog — the step it was implementing no longer exists |
| **Reopen** | Move a Done slice back to In Review — it needs rework before the phase can proceed |
| **Create** | A new slice is needed to cover the change — add it to the backlog |
| **Absorb** | The change is minor enough to handle within the existing slice scope — no structural change needed |

The solo approves each verdict from the impact scan — or overrides with a different decision. Do not proceed to execution until every affected item has a decision.

---

## Step 5 — Execute

With all decisions made, execute in this order:

**1. Update the to-be map**
Apply the agreed change to `docs/process/to-be-[name].md`. Mark changed steps with `[updated YYYY-MM-DD]` inline so the history is visible.

**2. Update the backlog**
For every affected slice: apply the solo's decision. Update process anchors, scope descriptions, done criteria, and deliverable records where needed. Create new slices and deliverable records where the solo decided `Create`. Retire slices where the solo decided `Retire`.

**3. Update or create deliverable records**
If the change requires new deliverables or modifies existing ones: update the deliverable fields (technical spec, solo description, acceptance criteria). New deliverables get full three-field records before they can enter build.

**4. Reopen Done slices where decided**
Move slice status from Done back to In Review. Note what changed and what needs to be revised. These slices must go through the full build → code review → solo-qa chain again before returning to Done.

**5. Log to product-continuity**
Append a process change record:

```
Process Change — [date]
Trigger: [source + what surfaced it]
Change: [Refinement / Addition / Restructure] — [brief description]
To-be map: updated [step name]
Slices affected: [list]
Decisions: [list of Revise / Retire / Reopen / Create / Absorb per affected item]
New slices created: [list or none]
Deliverables updated: [list or none]
```

---

## Step 6 — Re-Prioritize

With the backlog updated, re-sequence all work. The change may have shifted what matters most.

Surfaces an explicit sequence across three categories:

**Active work (what resumes first)**
In-progress slices that were paused, ordered by:
1. Risk — slices that were paused mid-build and have the most context to recover
2. Dependency unblocking — slices whose completion unblocks the most downstream work

**Revised scheduled work (what comes next)**
Ready slices after applying the verdicts from Step 4, ordered by:
1. Process order — sequence that follows the updated to-be map
2. Journey order — user journey flow, first screen before second

**New work from the change**
Newly created slices from `Create` decisions. These get positioned in the sequence by:
1. Whether they are prerequisites for existing scheduled work
2. Process order in the updated to-be map

Present the proposed sequence to the solo:

```
Proposed sequence after this change:

Resume first:
  1. SL-003 — [name] (was paused mid-build, scope updated)

Then:
  2. SL-004 — [name] (scope revised, ready to build)
  3. SL-009 — [name] (new slice from this change)
  4. SL-005 — [name] (unaffected, next in journey order)

Deferred / blocked:
  SL-007 — [name] (still blocked on SL-004)
```

---

## Step 7 — Solo Confirms

Hard gate. The solo explicitly confirms the updated state before any build work resumes.

Show a single confirmation summary:

```
Process Change Complete — [date]

To-be map: [step name] — [Refined / Added / Restructured]

Backlog changes:
  Revised: [N] slices
  Retired: [N] slices
  Reopened: [N] slices
  Created: [N] new slices

Deliverables updated: [list or none]

Next up: SL-[ID] — [name]. Ready to resume?
```

The solo says yes. Build resumes from the proposed sequence.

If the solo has a different starting point in mind, adjust — the sequence is a proposal, not a mandate. But the summary confirmation is not optional. Work does not resume until the solo has seen and approved the updated state.

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Absorbing a process change silently during build | The map and the build diverge — future phases trace to wrong steps | Invoke process-change, even for changes that seem small |
| Running the impact scan on an unapproved change | Wastes time; creates confusion if the change itself gets revised | Get Step 2 approval first, then scan |
| Assuming Done slices are safe | A process change can make completed work incorrect | Tier 3 scan is mandatory — every Done slice gets a verdict |
| Re-prioritizing without the solo's input | The solo may have context about priorities that isn't in the backlog | Present the proposed sequence in Step 6, wait for solo confirmation |
| Skipping the product-continuity log | The change becomes invisible history — next session has no context for why the backlog looks different | Log every change, every time, even minor ones |
| Resuming build without Step 7 confirmation | The solo hasn't seen the updated state — they're approving work they don't have full context on | Hard gate. No exceptions. |
| Treating cause as the classification criterion | The protocol for a stakeholder change and a solo realization is identical — what varies is the trigger log | Cause determines what to log in Step 1, not how to run the rest |
