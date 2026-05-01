---
name: autopilot
description: Autonomous build mode. Builds the full product without solo participation after discovery (or design sprint). Solo-simulator plays every gate. First human touch point is phase test. Refinement cycles handle iteration. Single-session, context-managed.
---

# Autopilot

*The framework builds. The solo reviews the whole.*

**Core question:** "Is the brief complete enough that the simulator can build this without guessing — and what does the finished product need to become?"

Autopilot is for solos who want to reach a finished product fast and iterate on the whole rather than participate in every slice. Discovery (and optionally the design sprint) happens with the solo. Everything after is autonomous — the simulator plays every gate, the framework commits every slice, and the solo sees the product at phase test.

---

## Activation

Explicitly invoked — never auto-routed. The solo asks for autopilot by name (`/autopilot`) or signals autonomous build intent. Never fires in guided, piloted, or bare mode unless directly invoked.

**Prerequisites — stop if any are missing:**
- `docs/discovery-brief.md` exists
- `docs/process/to-be-[slug].md` exists
- `docs/tech-context.md` exists
- `docs/backlog.md` exists with slices (prd-to-plan and to-issues have already run)

If any prerequisite is missing, stop and name exactly what's needed before autopilot can activate.

---

## Entry Points

**Entry Point 1 — Post-discover**
Solo completed discovery. No design sprint. Autopilot builds from process maps and discovery brief alone. The simulator works from a leaner design anchor — more judgment calls during build. Higher likelihood of Refinement cycles needed.

**Entry Point 2 — Post-design-review**
Solo participated in the design sprint and design review. Design artifacts exist in `docs/design/`. Autopilot has a richer anchor — structure confirmed, screens defined. Fewer simulator judgment calls. Tighter first-pass output.

Entry Point 2 is recommended when the product has significant UI or interaction complexity. Entry Point 1 is faster to start but accepts more variability in the output.

---

## Step 1 — Pre-Flight Check

Before a single slice is built, the simulator reads all discovery docs and surfaces judgment gaps — places where the spec doesn't decide and the simulator would have to guess.

**Read:**
- `docs/discovery-brief.md`
- `docs/process/to-be-[slug].md`
- `docs/tech-context.md`
- `docs/design/` contents (if Entry Point 2)
- `docs/backlog.md` — all slices and their anchors

**Discovery quality check — run first:**

If the to-be process map has vague steps, missing edge cases, or no explicit scope boundaries, surface this before gap questions:

> "The to-be map has gaps that will require judgment calls throughout the build. Autopilot output will be less predictable as a result. These are the specific gaps: [list]. Fill them now, or continue with known gaps?"

Solo decides. Capture the decision in the autopilot brief regardless.

**Gap surfacing:**

For each place where the simulator would have to guess, ask the solo directly:

> "Before I start, I need decisions on [N] things the spec doesn't resolve:
>
> 1. [Specific question — edge case, scope boundary, or behavior decision]
> 2. [Next question]
>
> Answer these and I'll start."

Solo answers → captured in `.claude/autopilot-brief.md` as addendum to the locked brief.

Pre-flight gate clears when no unresolved gaps remain. Do not begin building until the gate is clean.

---

## Step 2 — Brief and Begin

Write the locked brief to `.claude/autopilot-brief.md`:
- Discovery doc content (key decisions and scope, not verbatim copy)
- Pre-flight answers
- Entry point used
- Explicit scope boundaries — what is in, what is out
- Edge cases documented
- Design artifacts summary (if Entry Point 2)

Initialize `.claude/autopilot-decisions.md` — the simulator decision log. Every gate decision appended here throughout the build.

Confirm to the solo:

> "Pre-flight complete. Brief locked. Building [product name] — [N] slices across [N] deliverables. First check-in at phase test."

Then begin. No further solo contact until phase test.

---

## Step 3 — Autonomous Build

Build every slice in backlog order. The simulator plays the solo role at every gate. The solo is not contacted during the build.

**At each slice:**
1. Build the slice (same mechanics as solo-build)
2. Simulator-QA: run the same checks as solo-qa — simulator approves what matches the brief, pushes back on drift
3. If QA fails: builder fixes, simulator re-checks. After one failed round, escalate — log the issue and the decision made to `.claude/autopilot-decisions.md`, then continue
4. Commit the slice
5. Update slice status in `docs/backlog.md`
6. Append gate decision to `.claude/autopilot-decisions.md`

**Mid-deliverable checkpoint — fires automatically at slice 4 within any deliverable with more than 4 slices:**
- Update `docs/continuity/handoff.md` — Open right now section
- No solo approval, no pause. Execute and continue building immediately.

**At each deliverable completion:**
- Update `docs/continuity/handoff.md` — what just completed, what's next
- Update `docs/backlog.md` — deliverable marked complete
- Continue to next deliverable without pause

**Context discipline:**
Read from `docs/backlog.md` and `docs/continuity/handoff.md` as source of truth throughout — not conversation history. Write state to disk at every checkpoint. Do not accumulate build output in context beyond what the current slice requires.

---

## Step 4 — Phase Test

When all slices are built and committed, hand off to phase test.

> "Build complete — [N] slices committed across [N] deliverables. Phase test is next — this is your first look at the full product."

Run phase test as normal. Solo reviews the finished product.

**Pass:** proceed to deploy.

**Issues found:** proceed to Refinement.

---

## Step 5 — Refinement

Refinement handles iteration on the built product. It runs within autopilot — no phase rewind, no prior phases re-run. Refinement is only available in autopilot mode.

**Classify before building anything:**

Solo describes what's wrong. Framework classifies each item:

- **Implementation issue** — behavior is off, a display is wrong, a label needs changing, a data flow is broken. Refinement builds this.
- **Structural issue** — a screen needs rethinking, a flow is wrong at the process level, the to-be map doesn't match what was built. Refinement cannot fix this — it requires guided re-entry.

If structural issues are present alongside implementation issues:

> "Some of these are structural — they trace back to design, not implementation. Refinement can handle the implementation items. The structural items need a guided session. Two paths: run Refinement on implementation items now and handle structural separately, or exit to guided and address everything together. Which?"

**For implementation items:**
Build the delta only — changed slices, not the full product. Simulator at every gate. Same mechanics as Step 3, scoped to the affected slices.

After delta is built and committed, run phase test again.

**At each Refinement cycle completion:**

> "Refinement [N] complete. Another pass, or take this back into guided mode and work through it as a participant?"

Two paths:
- **Another Refinement:** return to classification with the solo's next round of feedback
- **Exit to guided:** go to Step 6

---

## Step 6 — Exit to Guided

When the solo chooses to exit autopilot and re-engage as a participant:

Read `docs/continuity/handoff.md`, `docs/backlog.md`, and `docs/design/` (if exists). Orient the solo in one sentence, then route to design review.

> "You've got a built product — [N] refinements applied, [N] open items. Design review will assess what exists and determine what needs to change."

Design review assesses the built product, routes what needs to change to the appropriate phase. The solo is now a guided participant from this point forward.

---

## Output Files

| File | Purpose |
|------|---------|
| `.claude/autopilot-brief.md` | Locked brief — discovery summary + pre-flight answers. Read throughout build, never rewritten mid-session. |
| `.claude/autopilot-decisions.md` | Simulator decision log — every gate decision appended continuously. |
| `docs/continuity/handoff.md` | Updated at slice 4 checkpoint and each deliverable completion. |
| `docs/continuity/current-phase.md` | Updated at build start and at each Refinement cycle. Read by the Solo Companion to surface autopilot state and Refinement cycle. |
| `docs/backlog.md` | Slice and deliverable statuses updated throughout build. |

### current-phase.md format during autopilot

At build start (after pre-flight clears):
```
Phase: Build
Mode: autopilot
Status: Building — [N]/[total] slices complete
Refinement cycle: None
```

During Refinement:
```
Phase: Build
Mode: autopilot
Status: Refinement
Refinement cycle: [N]
Refinement scope: implementation — [N] slices in delta build
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Skipping the pre-flight check | Simulator makes judgment calls the solo never approved — gaps surface as product defects | Pre-flight is mandatory. No build begins without a clean gate. |
| Contacting the solo during the build | Breaks the autonomous contract — gaps should have been caught at pre-flight | Pre-flight handles all questions. Build runs silent. If a genuine blocker emerges, log it and make the best decision from the brief. |
| Using Refinement for structural changes | Refinement builds deltas — it cannot fix a broken process flow or a wrong screen design | Classify first. Structural issues exit to guided. |
| Cycling through Refinement without considering the exit ramp | Solo iterates indefinitely on something that needs guided thought | Surface the exit ramp at every Refinement cycle completion. |
| Reading from conversation history instead of continuity docs | Context compression degrades build coherence late in long sessions | Always read from `docs/backlog.md` and `handoff.md` as source of truth. |
| Treating autopilot output as production-ready without phase test | Autopilot is spec-compliant — it has not been preference-validated | Phase test is mandatory. It is the first human review. |
| Conflating autopilot with solo-simulator | Solo-simulator is a role the framework plays at gates — autopilot is the full autonomous mode that uses it | Autopilot orchestrates the build. Simulator plays the solo at gates within it. |
| Running autopilot on thin discovery | Simulator judgment calls accumulate — output drifts from what the solo actually wanted | Surface discovery gaps at pre-flight. If the to-be map is vague, name it and get a decision before building. |
