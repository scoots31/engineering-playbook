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
- Stakeholder feedback at `docs/stakeholder-feedback/*.md` (if any new files since last round)

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

### Step 2.6: Incorporate Stakeholder Feedback (if present)

If new files exist in `docs/stakeholder-feedback/` since the last round, read each one and surface it explicitly before continuing:

> "Stakeholder feedback from [reviewer, date] is in. Overall reaction: [summary]. Approval status: [status]. Let's work through each per-screen comment."

Each per-screen comment becomes a finding classified like any other — design gap, knowledge gap, slice definition, deferral, or ready signal. Blockers listed by the stakeholder must be resolved before any affected slice reaches Ready.

If the approval status is "Approved to build" with no per-screen changes, log the approval in the Review Log and continue. If "Needs another round," that's a signal to schedule another handoff after the current round's changes land.

### Step 2.7: Data Behavior Pass

Required for any screen with external data — lists, feeds, or dynamic fields from an API or database. Skip only if a screen has no external data dependency.

For every screen with external data, ask:

- **Volume:** What's the expected number of records? Can this be 5 or 5,000?
- **List behavior:** Does the user need to search, filter, or sort? Is pagination or lazy loading required?
- **Null and missing fields:** Which fields can be absent? What percentage of real records will have them?
- **Empty state:** What does the screen look like when the API returns zero results?
- **Error state:** What does the screen look like when the API fails or times out?
- **Loading state:** Does the design account for in-flight requests?

Capture every unanswered question in the **data questions log** — appended to `docs/backlog.md`:

```markdown
## Data Questions Log

| Screen | Question | Status | Answer | Source | Resolved |
|--------|----------|--------|--------|--------|---------|
| Player List | Will the list paginate? | Open | — | — | — |
| Player List | Can slot_target be null? | Resolved | Yes, ~15% | API docs | 2026-04-25 |
```

**Gate:** Any UI slice whose design depends on an unresolved data question cannot reach Ready. The question must be answered first — via research spike, direct API check, or stakeholder confirmation. Once answered, update the log to Resolved and update the mock data before dependent slices finalize.

**When questions surface design changes:** If the answer changes what the design needs to show (pagination controls, loading skeleton, empty state layout), treat it as a design gap finding and update the design before defining dependent slices.

---

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
| Skipping the data behavior pass | Scale and behavior questions surface in phase-test instead of design review — expensive to fix that late | Run the pass on every screen with external data, every round |
| Leaving data questions open while promoting slices to Ready | Slices get built against wrong design assumptions — pagination added mid-build, empty states missing | Resolve data questions before dependent slices reach Ready |
| One mega-slice per screen | Too large to build, too vague to verify | Break screens into the smallest meaningful unit of work |
| Updating backlog only at the end of a round | Loses the thread | Update as the round proceeds |
| Reviewing without the design artifact open | Working from memory | Always review against the actual HTML screens |
| Letting blocked slices sit without naming the spike | Invisible blockers | Every blocked slice has a named, specific spike question |
| Skipping the process coverage check | Slices pile up around screens, whole process steps go unbuilt | Run coverage map every round — every to-be step must have a slice or an explicit decision |
| Slices reaching Ready without a process anchor | prd-to-plan can't sequence by process order; phase test has no grounding | Process anchor is a Ready requirement, not an optional field |
| Defining a new slice without a coherence check | Creates silent duplicates — two things do the same job, neither done well | Ask if the codebase already expresses this pattern before defining. Extend or explicitly diverge. |

---

## Enhanced Mode — Multi-Agent Orchestrator

**Tier 2 only. Requires Claude Code with enhanced mode active.**
Tier 1 (standard) behavior is unchanged — this section is skipped if enhanced mode is not active.

**Activation:** Solo says "enhanced mode on" in Claude Code. Flag persists for the session. All design-review rounds in the session use the orchestrator path.

**Graceful degradation:** If enhanced mode is not active, or if running in Cursor, skip this section entirely and run the standard review process above.

---

### What changes in enhanced mode

Instead of one model running all four lenses sequentially, four specialist agents run in parallel — each with its own context, its own instructions, and only the artifacts it needs. They don't see each other's work until synthesis.

The quality improvement comes from genuine independence: agents can't smooth over disagreements they don't know exist. When two agents flag the same element from different angles, that's a strong signal the orchestrator surfaces explicitly.

---

### Orchestrator Process

**Step 1 — Gather artifacts**

Collect the inputs each agent needs:
- Design artifact: `docs/design/sprint-[id].html`
- To-be process map: `docs/process/to-be-[name].md`
- Data mapping: `docs/data-mapping.md` (if exists)
- Backlog: `docs/backlog.md` (if exists)

**Step 2 — Spawn four agents in parallel**

Using Claude Code's Agent tool, spawn all four simultaneously. Pass each agent only its required artifacts plus its specialist instructions from `skills/design-review/agents/`:

| Agent | Instructions | Artifacts |
|---|---|---|
| UX Specialist | `agents/ux-specialist.md` | Design artifact only |
| Data Specialist | `agents/data-specialist.md` | Design artifact + data-mapping.md |
| Process Specialist | `agents/process-specialist.md` | Design artifact + to-be map |
| Scope Specialist | `agents/scope-specialist.md` | Design artifact + backlog.md |

**Step 3 — Collect results**

Wait for all four agents to return. Do not synthesize until all four are complete.

**Step 4 — Cross-signal analysis**

Before presenting findings, scan all four outputs for elements flagged by more than one agent. These are priority signals — independent agents reached the same element from different angles.

> Example: UX agent flags "dynasty value score — no explanation for user." Data agent flags "dynasty value score — source and calculation undefined." Cross-signal: this element is load-bearing and under-defined. Surface it first.

**Step 5 — Synthesize and present**

Structure the output in three tiers:

```
CROSS-SIGNAL FINDINGS (flagged by 2+ agents — address first)
[element]: [what each agent found, what decision is needed]

SPECIALIST FINDINGS
UX: [findings from ux-specialist output]
Data: [findings from data-specialist output]
Process: [findings from process-specialist output]
Scope: [findings from scope-specialist output]

DECISIONS NEEDED BEFORE NEXT ROUND
[numbered list — each a specific decision the solo must make]
```

**Step 6 — Continue as standard**

After presenting the synthesis, continue with the standard design-review process: update backlog, promote Ready slices, state what the next round needs to resolve. The orchestrator output feeds directly into slice definition — cross-signal findings become the highest-priority items to resolve.

---

### Token guidance for enhanced mode

Each agent receives a lean context (only its required artifacts). Shared artifacts benefit from prompt caching — the design sprint HTML is read once and cached; subsequent agents reading it pay a fraction of the first agent's cost. Net token cost is higher than standard mode but significantly lower than four full-context loads.

Use enhanced mode for Round 1 (full first pass) and any round where significant design changes were made. For incremental rounds reviewing small updates, standard mode is sufficient.

