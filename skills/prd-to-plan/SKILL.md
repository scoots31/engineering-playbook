---
name: prd-to-plan
description: Turn a PRD into a sequenced, multi-phase implementation plan using tracer-bullet vertical slices. Reduces integration risk by ordering work so each phase is demoable and de-risks the next. Use when user wants to plan implementation from a PRD, asks "how should we sequence this?", or wants a phased build plan before breaking into issues.
---

# PRD to Plan

Turn a PRD into a sequenced, multi-phase implementation plan. The goal is not just task breakdown — it is finding the sequence that reduces integration risk fastest.

## Process

### 1. Read Context Documents

Before doing anything else, read:
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

**Deliverable type:**
- **Screen** — output is visible. Reviewed visually in the browser.
- **Logic** — output is invisible. Reviewed against evidence: test results, data state, or a simulated flow through affected screens.

**Every deliverable carries three fields:**

- **Technical spec** — what the skill reads during build. Implementation-level, precise, written for the AI. Covers the architecture decisions, integration points, and technical constraints for this deliverable.
- **Solo description** — what the solo sees at review time. Plain language, outcome-focused. "When this deliverable is done, you'll have [X] — here's what it does and how to tell it's working."
- **Acceptance criteria** — the shared contract. Both the skill and the solo read the same criteria. The AI builds and self-verifies against them. The solo reviews against them. One set, agreed before build starts.

**Format per deliverable:**
```
Deliverable [D-ID] — [Name]
Type: Screen | Logic
Technical spec: [implementation-level description — for the AI]
Solo description: [plain-language outcome — for the solo]
Acceptance criteria:
  1. [verifiable criterion]
  2. [verifiable criterion]
  3. [verifiable criterion]
Slices: SL-001, SL-002, SL-003
```

If the deliverable record cannot be defined — missing design reference, unclear outcome, no verifiable criteria — stop. The deliverable must be defined and agreed before the plan is approved. A plan with undefined deliverables is not approvable.

Present deliverables alongside the phased plan. Both are reviewed and approved together. On approval, write the deliverable records to `docs/backlog.md` alongside the slice records.

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

For each phase, show:
- **Phase name** and short description
- **Slices in this phase** — each with its process anchor noted
- **What process steps this phase completes** — which to-be steps are implemented
- **What this phase proves or de-risks**
- **Blocked by** — prior phases or external dependencies
- **Definition of done** — how you know this phase is complete

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

Iterate until approved. When approved, update `docs/backlog.md` with the process anchor for each slice — it must be in the slice record before build starts.

### 9. Optional Next Step

Offer to convert the approved plan into GitHub issues in dependency order.
