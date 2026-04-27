---
name: prd-to-plan
description: Turn a PRD into a sequenced, multi-phase implementation plan using tracer-bullet vertical slices. Reduces integration risk by ordering work so each phase is demoable and de-risks the next. Use when user wants to plan implementation from a PRD, asks "how should we sequence this?", or wants a phased build plan before breaking into issues.
---

# PRD to Plan

Turn a PRD into a sequenced, multi-phase implementation plan. The goal is not just task breakdown — it is finding the sequence that reduces integration risk fastest.

## Process

### 1. Read Context Documents

Before doing anything else, read:
- `docs/records-spec.md` — the canonical record format. Every phase and deliverable created this session must conform to it.
- `docs/backlog.md` — existing slices from design review, their Ready status, dependencies
- `docs/process/to-be-[name].md` — the agreed to-be process map
- `docs/tech-context.md` — stack, infrastructure slices, engineering principles
- `docs/design/deferred-decisions.md` — what's in scope vs deferred

If the to-be process map doesn't exist, stop. The process map is the sequencing foundation — without it, slices get ordered by comfort rather than by the process they implement.

If the PRD is a GitHub issue, fetch it: `gh issue view <number>`.

### 2. Explore the Codebase (if mid-project)

If this is not a greenfield project, explore the repo to understand:
- Which existing systems the slices will touch
- What data models are already in place
- Where the integration seams are (API boundaries, DB schema, auth, external services)

### 3. Map Slices to Process Steps

Read the to-be process map. For every Ready slice in the backlog, identify which step in the to-be map it implements.

**Process anchor format per slice:**
`[to-be map step name] → [position in flow: main path / branch / exception]`

Example:
- SL-001 Player Lookup → `Step 1: user searches for player` → main path, entry point
- SL-003 Slot Context Card → `Step 3: system displays slot context` → main path, after lookup
- SL-007 Context Switch → `Step 4: user switches context` → main path, optional action

**Flag uncovered process steps** — steps in the to-be map that have no Ready slice assigned. These are either:
- Missing slices that should be added
- Intentionally deferred (should appear in deferred-decisions.md)
- Background logic that doesn't need a UI slice

Surface uncovered steps explicitly before sequencing:
> "Step 5 in the to-be map — 'system validates eligibility' — has no slice assigned. Is this handled in background logic (covered by an existing slice), or does it need a new slice?"

### 4. Identify Integration Seams

List every layer the slices cut through:
- Data layer (schema, mock→real swap points, data model changes)
- Business logic / service layer
- API / backend endpoints
- Frontend / UI
- External integrations (third-party APIs, auth, external services)
- Infrastructure (from tech-context infrastructure slices)

Flag HIGH RISK seams — places where assumptions made early will be painful to undo later.

### 5. Design Tracer-Bullet Vertical Slices

Each slice cuts through ALL integration layers end-to-end, delivering a narrow but complete path.

**Slice rules:**
- Each slice must be independently demoable or verifiable
- Prefer many thin slices over few thick ones
- The first slice must prove the riskiest assumption in the system. If the current ordering doesn't satisfy this, reorder before presenting the plan.
- Later slices build on confirmed foundations, not on hope
- Horizontal slices (e.g. "build all the DB models first") are not allowed — they defer integration risk

**Every slice gets four anchors in the plan:**
- **Design anchor** — screen + element from the design sprint
- **Data anchor** — mock data fields from data/mock/
- **Done anchor** — 2–3 verifiable criteria
- **Process anchor** — which step in the to-be map this slice implements

The process anchor is what connects the backlog to the agreed process. Solo-build reads it before starting a slice to confirm the implementation serves the right step.

### 5b. Define Deliverables

Once slices are designed, group them into deliverables. A deliverable is the agreed body of work a set of slices collectively produce. The solo agrees to deliverables before build starts — they are the review contract between the AI and the solo.

**Grouping rule:** Group slices by what they collectively deliver to the solo. A natural deliverable is a screen, a user-facing flow, a piece of background logic that enables other screens, or an infrastructure layer. Do not group slices that don't share a visible outcome — they belong in separate deliverables.

**Deliverable types:**
- **Screen** — output is visible UI. Reviewed visually in the browser. Built against mock data.
- **Logic** — output is invisible. Reviewed against evidence: test results, data state, or a simulated flow through affected screens.
- **Integration** — connects real data to a Screen deliverable. May contain both UI slices and data integration slices. Reviewed against both visual output and data evidence.

**Every deliverable carries these fields — all required:**

```
D-[ID] · [Name]

Status: Defined
Type: Screen | Logic | Integration
Phase: [N]

Plain language description:
[What the solo will specifically see, interact with, or have when this
deliverable is complete. Written fresh — not a summary of its slices.
No technical terms. As long as needed.]

Technical description:
[Integration points, constraints, component structure, data flow for
this specific deliverable. Written fresh — not copied from any slice.
As long as needed.]

Screens:
  - [screen file → screen name (primary | affected)]

Acceptance criteria:
  1. [verifiable criterion — flow or capability level, not slice level]
  2. [verifiable criterion]
  3. [verifiable criterion]

Self-verification checklist:
  - [confirms slices work correctly together — flow, handoffs, data passing]
  - [confirms complete user journey through all slices in this deliverable]

Builder confirmation:
Pending build

Slices: SL-[ID], SL-[ID]
References:
  - [source — why vital to this deliverable]
Depends on: [D-ID | none]
Notes: [decisions, constraints, anything non-obvious at the deliverable level]
```

**Field rules:**
- Plain language description and technical description are written fresh and independently at the deliverable level. Neither summarizes the slices beneath it, and neither copies from a phase record above it.
- Screens lists every screen this deliverable touches — primary screen being built and any screens affected by underlying changes.
- Acceptance criteria operate at the flow or capability level, not the slice level. "A user can complete [this flow] from start to finish" not "the search input returns results."
- Self-verification checklist confirms the slices work together — not a re-check of individual slices.

If any required field cannot be defined — missing design reference, unclear outcome, no verifiable criteria — stop. The deliverable must be fully defined and agreed before the plan is approved. A plan with undefined or partial deliverable records is not approvable.

Present deliverables alongside the phased plan. Both are reviewed and approved together.

---

### 5c. Integration Deliverables

For every Screen deliverable that reads from external data, define a companion Logic deliverable for data integration. This is where real API connections, data flow, and UI reactions to live data are built and verified.

**Rules:**
- Always a **Logic** type — reviewed against evidence, not visual inspection
- Always sequences after its Screen companion is Accepted — never in the same phase
- Cannot be fully scoped until the data questions log is fully resolved
- Named: "[Screen Name] — Data Integration"

**Standard done criteria for every integration slice:**
- API connected and returning data in expected shape
- `docs/data-mapping.md` updated from proto to confirmed — field names reconciled, behavior documented
- Mock indicator badge removed from affected screens
- Pagination / filtering / search working correctly (if applicable per data questions log)
- Empty state renders correctly with a real no-results API response
- Error state renders correctly with a real API error
- Loading / in-flight state renders correctly
- All fields rendering from the real source — none hardcoded
- Auth confirmed working in the test environment (if applicable)

**Data questions gate:** If the data questions log still has open entries when defining integration slices, those slices cannot be scoped. Surface it explicitly:
> "Data questions for [entity] are unresolved — the data integration deliverable for [Screen] cannot be fully defined until these are answered. Resolve via research spike or direct API check."

**Sequencing:** Integration deliverables always follow their Screen companions. Where one integration deliverable de-risks data assumptions for multiple Screen deliverables, it may sequence ahead of later Screen deliverables — name this explicitly in the plan.

---

### 6. Sequence by Risk and Process Order

Two sequencing forces in tension — resolve them explicitly:

**Risk order:** Address the hardest, most uncertain, most load-bearing parts first. The first slice must prove the riskiest assumption. If it doesn't, reorder until it does.

**Process order:** Slices that implement earlier steps in the to-be map come before slices that implement later steps. A user can't reach Step 3 if Step 1 isn't built. Follow process order — don't reorder these for convenience.

**When they conflict:** Risk order wins for infrastructure and foundation slices. Process order wins for feature slices once infrastructure is in place. Name the conflict explicitly when it occurs:
> "Step 3 (slot context display) implements an earlier process step than Step 5 (context switch), but Step 5 de-risks the state management approach we haven't proven yet. Building Step 5 first as a tracer."

**Infrastructure slices first, always.** Read `docs/tech-context.md` infrastructure slices — these are prerequisites for everything else and sequence before any feature slice regardless of process order.

For each phase, produce a full phase record — all fields required:

```
Phase [N] · [Name]

Status: Planning
Question this phase answers: [one sentence]
Deliverables: [D-ID, D-ID]

Plain language description:
[What the product can do when this phase is complete — the capability
unlocked. Written fresh — not a summary of its deliverables. As long
as needed.]

Technical description:
[The architectural approach, what gets proven at the system level, what
foundational work this phase establishes. Written fresh. As long as needed.]

Process steps completed: [to-be step names]
Proves / de-risks: [what you now know that you did not before]

Explicitly out of scope:
[Things someone might reasonably expect in this phase but will not find,
and why. Not exhaustive — only the things whose absence would confuse.]

Blocked by: [Phase N | external dependency | none]
Definition of done: [how you know this phase is complete]

Acceptance criteria:
  1. [verifiable criterion — capability level, not deliverable level]
  2. [verifiable criterion]
  3. [verifiable criterion]

Self-verification checklist:
  - [confirms deliverables work correctly together end-to-end]
  - [confirms the phase answers its stated question with evidence]

Builder confirmation:
Pending build

Notes: [decisions, constraints, anything non-obvious at the phase level]
```

**Phase anti-pattern:** A phase is not a time box, a sprint, or a feature list. If the question this phase answers cannot be stated in one sentence, the phase boundary is wrong — redefine it before presenting the plan.

### 7. Flag Open Questions

List any decisions that must be made before implementation can start:
- Architectural choices with meaningful tradeoffs
- Uncovered process steps that need resolution
- Missing information
- Dependencies on other teams, systems, or data

### 8. Present and Confirm

Show the full plan. Ask:
- Does the phase sequencing feel right — does it respect both risk and process order?
- Are there slices that should be merged, split, or reordered?
- Are uncovered process steps accounted for correctly?
- Are any open questions blockers, or can we proceed with a stated assumption?

Iterate until approved. When approved, execute the backlog write immediately — all four steps, in this order, before the session closes.

### 8b. Write the Approved Plan to the Backlog

On solo approval, update `docs/backlog.md` with the full plan. This is not optional and does not wait for the next session.

**Step 1 — Write all phase records.**
Add the Phase records section to `docs/backlog.md` with every phase record in full. Status set to `Planning` on all phases.

**Step 2 — Write all deliverable records.**
Add the Deliverable records section with every deliverable record in full. Status set to `Defined` on all deliverables.

**Step 3 — Update every slice record.**
Go into every slice record in the backlog and add the two fields that only prd-to-plan can set:
- `Phase: [N]` — replace "Pending prd-to-plan"
- `Deliverable: [D-ID]` — replace "Pending prd-to-plan"

Every Ready slice must leave this step with both fields populated. No exceptions.

**Step 4 — Add the Decisions and Change Log section.**
If it doesn't exist, add it to the bottom of `docs/backlog.md`:

```markdown
## Decisions and Change Log

*Append-only. Every material change to the plan is logged here.*

### [YYYY-MM-DD] — Plan approved
Decision: Implementation plan approved. [N] phases, [N] deliverables, [N] slices.
Reason: Plan sequenced by risk and process order. Approved by solo.
Impact: Phase records, deliverable records, and slice phase/deliverable assignments written to backlog.
Confirmed by: Solo
```

After the write is complete, confirm: *"Backlog updated — [N] phases, [N] deliverables, [N] slices. Phase and deliverable assignments written to all slice records. Ready to build."*

### 9. Optional Next Step

Offer to convert the approved plan into GitHub issues in dependency order.
