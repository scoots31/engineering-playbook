---
name: design-review
description: Iterative review loop between the design artifact and the build decision. Each round adds knowledge, refines the design, defines slices, and updates the backlog. A slice reaches Ready when it's defined well enough to build — design reference clear, done criteria set, dependencies known. Build starts when enough slices are Ready. Review continues in parallel. The backlog is the persistent document that makes all of this visible — to the solo and to anyone else they need to communicate with.
---

# Design Review

*Where the work gets defined, not just validated.*

**Core question:** "What do we know well enough to build, and what needs another round?"

This is the loop between design artifact and build decision. It runs as many rounds as the project needs — until enough slices have reached Ready state to start building. It doesn't end when the design is perfect. It ends when there's enough to learn from.

Each round does three things simultaneously:
1. **Refines the design** — adds knowledge, surfaces gaps, updates screens, triggers spikes
2. **Defines slices** — names the units of work, sets done criteria, identifies dependencies
3. **Updates the backlog** — moves slices through states, makes progress visible

---

## When to Run

- **First run:** After the design sprint produces the initial screens and deferred decisions log
- **Subsequent runs:** After each significant addition — new screen, spike result returned, major design change
- **During build:** Continues on items not yet in build while build is progressing on Ready slices
- **On request:** Anytime the solo wants to review state, add knowledge, or check what's next

---

## The Specialist Lenses

For a solo, the AI plays the specialist roles that a team would fill in a real review. Each round applies these lenses to every screen and slice being reviewed. The solo brings domain knowledge and makes final calls.

**PM lens** — Is this solving the right problem for the right person? Does the flow make sense from the user's perspective? What's missing from the story? What would a user hit that we haven't designed for?

**Tech lead lens** — Is this buildable with the stack we have? What are the real dependencies — not just stated ones? What has to exist before this slice can start? What's the complexity risk?

**Data lens** — Where does every visible field come from? Does the data model support what the design implies? What API calls are behind this screen? What doesn't exist yet that the design assumes?

The solo is always the fourth voice — domain expert, final decision maker, the person who knows what the tool is actually for.

---

## Execution

### Step 1: Read Current State

Before the round begins, read:
- All design screens in `docs/design/`
- Current backlog at `docs/backlog.md` (if it exists — first round creates it)
- Deferred decisions log at `docs/design/deferred-decisions.md`
- **To-be process map at `docs/process/to-be-[name].md`** — the agreed process. Every slice should implement a step in it.
- Any spike results in `docs/spikes/`

If the to-be process map doesn't exist, stop before reviewing slices. The process map is what tells you whether the design covers the right things — without it, slice review is just reacting to screens.

> "No to-be process map found. Go to Discover and agree the to-be process before reviewing slices — the map is what we're building against."

Orient out loud: *"We have [N] screens, [N] slices defined so far — [N] Ready, [N] In Review, [N] Blocked. This round we're reviewing [specific focus]."*

### Step 2: Review Each Screen

For each screen being reviewed this round, apply all three lenses and surface findings. Be specific — not "this needs more thought" but "this field implies a historical data store that isn't in the current data model."

For each finding, classify it immediately:

| Finding type | Action |
|---|---|
| Design gap — something missing from the screen | Note it, ask if it should be added |
| Knowledge gap — something we don't know yet | Trigger a research spike with a specific question |
| Slice definition — element is clear enough to name as a unit of work | Define the slice |
| Deferral confirmation — something explicitly not in scope | Mark deferred in backlog |
| Ready signal — slice has everything it needs | Promote to Ready |

Don't bundle findings. Each one gets named and classified before moving to the next.

### Step 2.5: Check Process Coverage

After reviewing screens, cross-reference the defined slices against the to-be process map.

For every step in the to-be map, ask: **is there a slice that implements this step?**

Build a coverage map — one line per process step:

```
Step 1: [step name] → SL-001 (main path) ✅
Step 2: [step name] → SL-003 (main path), SL-007 (branch) ✅
Step 3: [step name] → NO SLICE ASSIGNED ⚠️
Step 4: [step name] → Deferred ⏸
```

**For every uncovered step, surface it as an explicit decision — not a silent gap:**

> "Step 3 in the to-be map — '[step name]' — has no slice assigned. Is this:
> - Background logic handled inside an existing slice?
> - Missing and needs a new slice?
> - Intentionally deferred (should appear in deferred-decisions.md)?"

Get an answer before the round closes. Unresolved coverage gaps block a clean Phase 1 — they surface later as missing behavior during phase test, when they're expensive to fix.

**Positive coverage check too** — slices that can't be mapped to any process step are also a signal. They may be infrastructure (valid), or they may be scope creep (needs a decision).

> "SL-008 (Admin Panel) doesn't map to any step in the to-be process. Is this infrastructure, a deferred feature, or something that should be removed from scope?"

This coverage check runs every round — not just Round 1. As new slices are added and process understanding deepens, gaps that weren't visible before may appear.

### Step 3: Define or Refine Slices

As each element reaches enough clarity, define it as a slice. A slice is the unit of work — what gets built, what done looks like, what has to exist first.

**A slice is ready to define when:**
- The design reference is clear — you can point at the exact element on a screen
- You can describe what it does in one sentence
- You can state 2–3 criteria that would tell you it's built correctly

**A slice is NOT ready to define when:**
- The design for it is still unclear
- A spike is open on it
- It depends on something that hasn't been defined yet

For slices not yet ready — keep them as named items in the backlog with status In Review or Blocked. They get refined in the next round.

**Coherence check — before defining a new slice:**
Does the codebase already express this pattern somewhere? Ask: are we extending something that exists, or creating something new? If extending — build on the existing vocabulary. If new — that's valid, but name it explicitly in the slice notes so the next session isn't surprised by the divergence.

### Step 4: Determine Slice Status

Every slice in the backlog has one of these states at all times:

| Status | Meaning |
|--------|---------|
| `Ready` | Design reference clear, done criteria set, dependencies known — can be built now |
| `In Review` | Identified but needs more refinement before it can be built |
| `Blocked` | Waiting on a specific spike result — named explicitly |
| `Deferred` | Explicitly set aside — not in current scope, trigger condition noted |
| `In Build` | Currently being worked on |
| `Done` | Complete and verified |

**A slice reaches Ready when ALL of these are true:**
- Design reference is unambiguous — specific screen and element
- Done looks like is defined — 2–3 criteria, not vague
- Dependencies are identified and either resolved or not blocking
- No open spike on it
- **Process anchor is set** — which step in the to-be map this slice implements, or explicitly documented as infrastructure/background logic that doesn't map to a user-facing step
- The solo confirms it's clear enough to hand to a builder

This is the answer to "when do we build it." Not when the overall design is done. When this specific slice has these things. The backlog shows you — no ceremony required.

### Step 5: The Build Signal

When enough slices have reached Ready state, build can start. "Enough" is a judgment call — but the right question is:

*"Is there a meaningful set of Ready slices that form a coherent starting point — enough to learn something real from building them?"*

This is usually the first vertical slice through the system: the simplest path that produces something working end to end. Not the most feature-complete. Not the easiest. The one that proves the core loop works.

When that set exists, state it clearly: *"These [N] slices are Ready and form a coherent Phase 1 starting point. Build can begin. Review continues on the remaining [N] slices in parallel."*

Build and review run in parallel from this point. The backlog is what keeps both tracks visible.

### Step 6: Update the Backlog

After every round, update `docs/backlog.md`. This is not a separate step — it happens as the round proceeds. Every slice definition, status change, and spike trigger goes into the backlog in real time.

The backlog is never recreated from scratch. It accumulates. Append and update — the history of how slices moved through states is valuable context.

---

## The Backlog Document

`docs/backlog.md` — created on first design review round, updated every round after.

This document serves two audiences equally: the solo (knowing where they are and what's next) and anyone they need to communicate with (stakeholder, collaborator, future session). It should be immediately readable by someone who wasn't in the room.

---

```markdown
# Backlog — [Project Name]
**Last updated:** [YYYY-MM-DD · Round N]
**Project status:** [In Design Review / In Build / Shipped]

---

## At a Glance

| Status | Count |
|--------|-------|
| ✅ Ready | N |
| 🔄 In Review | N |
| 🔬 Blocked (spike) | N |
| ⏸ Deferred | N |
| 🔨 In Build | N |
| ✓ Done | N |

**Currently in build:** [SL-XXX, SL-XXX]
**Next up (Ready, not started):** [SL-XXX, SL-XXX]
**Open spikes:** [spike topic → blocks SL-XXX]

---

## Backlog

| ID | Name | Phase | Status | Depends on |
|----|------|-------|--------|------------|
| SL-001 | [Name] | 1 | ✅ Ready | — |
| SL-002 | [Name] | 1 | 🔄 In Review | — |
| SL-003 | [Name] | 1 | 🔬 Blocked | Spike: [topic] |
| SL-004 | [Name] | 2 | ⏸ Deferred | — |

---

## Slice Detail

### SL-001 · [Name]
**Status:** ✅ Ready  
**Phase:** 1  
**Design reference:** [screen file — specific element]  
**Description:** [One sentence — what this slice builds]  
**Process anchor:** [to-be process step name] → [main path / branch / exception / infrastructure]  
**Done looks like:**
- [Acceptance criterion 1]
- [Acceptance criterion 2]
- [Acceptance criterion 3]

**Depends on:** [SL-XXX / API: X / none]  
**Notes:** [Anything relevant — decisions made, constraints, spike results that informed this]

---

[Repeat for each slice]

---

## Review Log

### Round N — [YYYY-MM-DD]
**Focus:** [What was reviewed this round]
**Slices promoted to Ready:** [IDs]
**Slices added:** [IDs]
**Spikes triggered:** [Topics]
**Design changes:** [What was updated]
**Next round focus:** [What needs attention next]
```

---

## What the Backlog Is Not

- Not a Gantt chart — no dates, no estimates unless the solo wants them
- Not a requirements document — slices are units of work, not specifications
- Not static — it changes every round, that's the point
- Not exhaustive upfront — slices get added as the design gets clearer

---

## Running Multiple Rounds

Each round has a focus — don't try to review everything equally every time. Let the findings from the previous round drive the focus of the next.

**Round 1 (first design review):** Full first pass on all screens. Everything starts as In Review. Define slices where possible. Identify spikes. Establish the backlog. Run the process coverage check — produce the full coverage map and surface every uncovered to-be step as a decision. No slice reaches Ready on Round 1 without a process anchor.

**Round 2+:** Focus on what moved since last round — spike results returned, design updates, new screens. What can be promoted to Ready? What's still open?

**Parallel to build:** Once build starts, design review rounds continue but focus on slices not yet in build. Each round checks: what's become Ready that wasn't before?

End each round by stating explicitly:
- What moved to Ready this round
- What's still open and why
- What the next round needs to resolve
- Whether build can start or continue

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Waiting for all slices to be Ready before building | Waterfall — defeats the point | Build starts when first meaningful Ready set exists |
| Vague done criteria | "It works" is not a criterion | 2–3 specific, verifiable statements |
| Skipping the data lens | Design implies data that doesn't exist | Every field on every screen gets a "where does this come from" pass |
| One mega-slice per screen | Too large to build, too vague to verify | Break screens into the smallest meaningful unit of work |
| Updating backlog only at the end of a round | Loses the thread | Update as the round proceeds |
| Reviewing without the design artifact open | Working from memory | Always review against the actual HTML screens |
| Letting blocked slices sit without naming the spike | Invisible blockers | Every blocked slice has a named, specific spike question |
| Skipping the process coverage check | Slices pile up around screens, whole process steps go unbuilt | Run coverage map every round — every to-be step must have a slice or an explicit decision |
| Slices reaching Ready without a process anchor | prd-to-plan can't sequence by process order; phase test has no grounding | Process anchor is a Ready requirement, not an optional field |
| Defining a new slice without a coherence check | Creates silent duplicates — two things do the same job, neither done well | Ask if the codebase already expresses this pattern before defining. Extend or explicitly diverge. |
