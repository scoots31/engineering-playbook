# Backlog Records Specification

**Audience:** Framework skills and curator. This is the canonical definition of every record type in `docs/backlog.md` — what each object contains, what each field means, and what valid looks like.

**Rule:** Every skill that reads or writes backlog records reads this document first. No skill invents fields. No skill omits required fields.

---

## Record Types

There are three record types in every backlog:

1. **Phase** — a group of deliverables that together prove one meaningful capability
2. **Deliverable** — a group of slices that together produce one complete output
3. **Slice** — the atomic unit of build work

Each level checks what only that level can see:
- Slice verification: does this specific element work correctly on its own?
- Deliverable verification: do all the slices work correctly together as a complete thing?
- Phase verification: do all the deliverables work correctly together as a complete capability?

---

## Status Structures

### Slice Statuses

| Status | Meaning |
|--------|---------|
| `In Review` | Identified but needs more definition before it can be built |
| `Blocked` | Waiting on a named dependency — named explicitly |
| `Deferred` | Explicitly set aside — trigger condition noted |
| `Ready` | Fully defined, can be built now |
| `In Build` | Work is active on this slice |
| `In QA` | Code complete, solo-qa running |
| `In Test` | QA passed, phase-test running |
| `Done` | Built and verified against its data anchor |

### Deliverable Statuses

| Status | Meaning |
|--------|---------|
| `Defined` | Record created, not yet started |
| `Active` | At least one slice is In Build |
| `Pending Acceptance` | All slices Done, awaiting solo sign-off |
| `Accepted` | Solo signed off — this deliverable is complete |

### Phase Statuses

| Status | Meaning |
|--------|---------|
| `Planning` | Phase is being defined — deliverables and slices being sequenced |
| `Ready for Build` | Phase fully defined, all deliverables Defined, build can start |
| `In Progress` | At least one deliverable is Active |
| `Completed` | All deliverables in this phase are Accepted |

---

## Descriptions — Rules That Apply at Every Level

Every record type carries two description fields. These rules apply to all of them without exception:

**Plain language description**
Written for the solo. No technical terms. Describes what the solo will see, have, or be able to do when this object is complete. As long as it needs to be to be unambiguous — if four sentences are needed, use four sentences.

**Technical description**
Written for the builder. Covers architecture decisions, integration points, constraints, edge cases, and approach. As precise as the implementation requires.

**Critical rule: descriptions are written fresh at every level.**
A phase description is not a summary of its deliverables. A deliverable description is not a summary of its slices. Each description answers the question "what does this object deliver?" from the perspective of its own scope. Copying or paraphrasing from one level to another is a failure — it means the author didn't think about what the object needs to communicate independently.

| Level | Plain language describes | Technical description covers |
|-------|--------------------------|------------------------------|
| Phase | What the product can do when this phase is complete — the capability unlocked | The architectural approach, what gets proven at the system level, what foundational work this phase establishes |
| Deliverable | What the solo will specifically see, interact with, or have — the concrete output | Integration points, constraints, component structure, data flow for this specific deliverable |
| Slice | What specific element or behavior the solo will observe | Exact implementation approach — method, data shape, component, edge cases |

---

## Verification Model — Rules That Apply at Every Level

Every record type carries the same three verification fields. The scope changes at each level — the structure does not.

**Self-verification checklist**
What the builder checks before presenting to the solo. At the slice level: does this element work correctly on its own. At the deliverable level: do the slices work correctly together — flow, state handoffs, data passing between components, complete user journey. At the phase level: does the complete capability work end-to-end across all deliverables.

Not a re-check of the level below. A check of what only this level can see.

**Acceptance criteria**
The shared contract. Builder self-verifies against it. Solo reviews against the same list. One set of criteria, agreed before build starts, used by both parties independently.

**Builder confirmation**
Populated by the builder at presentation time — before the solo is asked to review. Each self-verification item listed with confirmed/flagged status and a brief note on what was observed. Not a narrative. A checklist with evidence.

The solo then does their own independent pass against the acceptance criteria. Two independent checks against the same list. Solo signs off. Object moves to its next status.

---

## Slice Record

```
SL-[ID] · [Name]

Status: [In Review | Blocked | Deferred | Ready | In Build | In QA | In Test | Done]
Phase: [N — assigned during prd-to-plan, blank until then]
Deliverable: [D-ID — assigned during prd-to-plan, blank until then]

Plain language description:
[What the solo will see or have when this slice is done. Fresh — not copied
from the deliverable. As long as needed to be unambiguous.]

Technical description:
[What the builder needs to know — implementation approach, constraints,
edge cases. As long as needed.]

Design anchor: [screen file — specific element]
Data anchor: [file path — specific fields | Pending data-scaffold]
Process anchor: [to-be step name] → [main path | branch | exception | infrastructure]

References:
  - [source — why the builder must read this to execute the slice correctly]

Done criteria:
  - [verifiable statement]
  - [verifiable statement]
  - [verifiable statement — 2-3 total]

Self-verification checklist:
  - [what the builder confirms this specific slice does correctly]
  - [what the builder confirms before presenting]

Builder confirmation:
[Populated at presentation time — not before]
  ✓/✗ [item — what was observed]
  ✓/✗ [item — what was observed]

Review URL: [URL where this slice's output can be previewed | None]

Test file: [tests/test_SL-[ID].py | None — populated by builder at code-complete when CI/CD is configured]

Depends on: [SL-XXX | D-ID | external dependency | none — explicit always]
Notes: [Decisions made, constraints discovered, spike results, non-obvious things.
        Not a summary of what the slice does — that's the descriptions above.]
```

### Slice field definitions

**ID** — Sequential identifier. Assigned when the slice is first named. Never changes. Never reused if a slice is removed.

**Name** — One short noun phrase describing what this slice builds. Not a user story. Not a verb phrase. "Player Search Results List" not "Build the search results."

**Design anchor** — The specific screen file and specific element within it that this slice builds. If you cannot point at an exact element, the slice is not ready to define.

**When the design source is a Figma file**, the design anchor carries two additional requirements that apply from design review through code review:

**Node properties, not visual approximation.** Every value used in implementation — dimensions, spacing, colors, typography — must be extracted from Figma node properties. Visual approximation is not acceptable and is a code review failure. If the Figma MCP is available, extract values directly. If not, use Figma's Dev Mode inspect panel. Either way: source values, not estimates.

**Interactive element inventory.** Every interactive element visible in the slice's design scope must be classified before the slice reaches Ready. An interactive element is anything that implies user action and expected behavior: search inputs, filters, sort controls, pagination, tabs that change content, toggles, dropdowns, form fields, date pickers, modals triggered by user action.

Three valid classifications — no others:

| Classification | Meaning |
|---|---|
| **Functional** | Logic is wired in this slice, or in a named companion slice within the same deliverable — slice ID required |
| **Deferred** | Shell rendered as a visible non-interactive placeholder; a companion logic slice exists in the backlog — slice ID required |
| **Out of scope** | Not rendered, or rendered visibly disabled, with an explicit note in the slice record |

There is no fourth option. An interactive element rendered as a working-looking shell with no wired logic, no deferred slice on record, and no explicit scope decision is a framework failure — it is an unauthorized product decision made silently at build time. The classification is a design review responsibility, not a build-time judgment call. The inventory lives in the slice record's Notes field.

**Data anchor** — The specific mock data file and specific fields this slice reads. Blank until data-scaffold runs — marked "Pending data-scaffold" not omitted. A slice with no data dependency states "None" explicitly.

**Process anchor** — Which step in the to-be map this slice implements and where in the flow. If infrastructure, state what it enables. A slice with no process anchor cannot reach Ready.

**Done criteria** — 2–3 verifiable statements that confirm the slice is built correctly. Each criterion must be checkable without ambiguity — either it is true or it is not. "Search returns results" is not a criterion. "Entering a player name returns a filtered list within 300ms with no console errors" is.

**References** — Any source — internal document, external URL, API spec, stakeholder feedback, spike result, prior decision — that a builder must read to execute this slice correctly. If the builder could complete the slice without it, it does not belong here. If missing it would produce the wrong result or require a redo, it belongs here. Each entry states what it is and why it is required.

**Depends on** — Other slices or external things that must exist before this slice can start. Named explicitly — not "backend" but "SL-003" or "API: player search endpoint confirmed." None is a valid answer and must be stated explicitly.

**Review URL** — The URL where the completed slice can be previewed. Written by the builder at code-complete, alongside the status update to `In QA`. A local server URL, running preview path, or deployed preview link — whatever the solo needs to open the work in a browser. `None` for slices with no previewable output (pure logic, infrastructure). Never left blank.

**Test file** — Path to the pytest file generated for this slice at code-complete. Written by the builder alongside the commit when `CI/CD: GitHub Actions` is configured in tech-context. Format: `tests/test_SL-[ID].py`. `None` when CI/CD is not configured for the project. Never left blank when CI/CD is active.

**Notes** — The why and the non-obvious. Things that would surprise a builder who had not been in the room. Not a summary of what the slice does.

### Slice Ready gate

A slice reaches Ready only when ALL of these are true:
- Plain language description written
- Technical description written
- Design anchor is unambiguous — specific screen and specific element
- Process anchor is set — or explicitly documented as infrastructure
- Done criteria defined — 2–3 verifiable statements
- Self-verification checklist defined
- Dependencies identified — resolved or explicitly not blocking
- No open spike on it
- Data anchor filled OR explicitly marked Pending data-scaffold
- Solo confirms it is clear enough to hand to a builder

---

## Deliverable Record

```
D-[ID] · [Name]

Status: [Defined | Active | Pending Acceptance | Accepted]
Type: [Screen | Logic | Integration]
Phase: [N]

Plain language description:
[What the solo will specifically see, interact with, or have when this
deliverable is complete. Fresh — not a summary of its slices. As long
as needed.]

Technical description:
[Integration points, constraints, component structure, data flow for
this specific deliverable. As long as needed.]

Screens:
  - [screen file → screen name (primary | affected)]
  - [screen file → screen name (primary | affected)]

Acceptance criteria:
  1. [verifiable criterion — flow or capability level, not slice level]
  2. [verifiable criterion]
  3. [verifiable criterion]

Self-verification checklist:
  - [confirms slices work correctly together — flow, handoffs, data passing]
  - [confirms complete user journey through all slices in this deliverable]

Builder confirmation:
[Populated at presentation time — not before]
  ✓/✗ [item — what was observed]
  ✓/✗ [item — what was observed]

Slices: SL-[ID], SL-[ID], SL-[ID]
References:
  - [source — why vital to this deliverable]
Depends on: [D-ID | none]
Notes: [decisions, constraints, anything non-obvious at the deliverable level]
```

### Deliverable types

**Screen** — output is visible UI. Reviewed visually in the browser. Built against mock data. Done when all slices are Done and solo has signed off.

**Logic** — output is invisible. Reviewed against evidence: test results, data state, simulated flow through affected screens.

**Integration** — connects real data to a Screen deliverable. May contain both UI slices (design changes revealed by real data) and data integration slices (API wiring). Reviewed against both visual output and data evidence. Always sequences after its Screen companion is Accepted. Can spawn new slices mid-build when real data reveals gaps — the integration deliverable is not Accepted until all slices, including discovered ones, are Done.

### Done vs Accepted

**Done** lives at the slice level. A slice is Done when it is built and verified against the data source defined in its own data anchor — mock or real, whichever that slice was built against. Done is always unambiguous.

**Accepted** lives at the deliverable level. A deliverable is Accepted when all its slices are Done AND the solo has signed off against the acceptance criteria. This is where integration complexity and cross-slice behavior is verified.

---

## Phase Record

```
Phase [N] · [Name]

Status: [Planning | Ready for Build | In Progress | Completed]

Plain language description:
[What the product can do when this phase is complete — the capability
unlocked. Fresh — not a summary of its deliverables. As long as needed.]

Technical description:
[The architectural approach, what gets proven at the system level, what
foundational work this phase establishes. As long as needed.]

Question this phase answers: [one sentence]
Deliverables: [D-ID, D-ID, D-ID]
Process steps completed: [to-be step names]
Proves / de-risks: [what you now know that you did not before]

Explicitly out of scope:
[Things someone might reasonably expect to find in this phase but will not,
and why. Not an exhaustive list of everything not built — only the things
whose absence would confuse or surprise.]

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
[Populated at phase completion — not before]
  ✓/✗ [item — what was observed]
  ✓/✗ [item — what was observed]

Notes: [decisions, constraints, anything non-obvious at the phase level]
```

### Phase anti-pattern

A phase is not a time box, a sprint, or a feature list. A phase defined by "everything we can finish in two weeks" or "all the screens" has no question it is answering — it is a bucket, not a proof. If you cannot state the question a phase answers in one sentence, the phase boundary is wrong.

### Phase status transitions

| Transition | Trigger |
|---|---|
| Planning → Ready for Build | Plan approved by solo |
| Ready for Build → In Progress | First deliverable goes Active |
| In Progress → Completed | Last deliverable reaches Accepted |

---

## Backlog Document Structure

`docs/backlog.md` is the single source of truth for everything about the project plan. It carries five sections in this order:

```
1. At a Glance       — current state summary, counts by status
2. Phase records     — all phases with full records
3. Deliverable records — all deliverables with full records
4. Slice records     — all slices with full records
5. Decisions and Change Log — append-only history
```

---

## Decisions and Change Log

Append-only. Every material change to the plan is logged here — re-phasing, scope additions, deferrals, dependency changes, design pivots that affect slices. The history of why decisions were made is as important as the decisions themselves.

```markdown
### [YYYY-MM-DD] — [What changed]
Decision: [what was decided]
Reason: [why]
Impact: [what records were updated]
Confirmed by: Solo
```

### Re-phasing protocol

When a slice or deliverable needs to move to a different phase, this protocol executes in full — no partial execution:

1. Solo confirms the move and the reason
2. Log the decision in the Decisions and Change Log
3. Update the moved item — phase field updated
4. Update the source phase — "Explicitly out of scope" updated to note what moved and why
5. Update the destination phase — deliverables list updated
6. Assess source phase — does it still answer its stated question with the item removed? If not, update the phase definition
7. Assess destination phase — does the moved item fit the question that phase answers? If not, update the phase definition

All seven steps happen in the same action. The log entry and the record updates are never separated.

---

### Rollback protocol

When a slice that has passed QA (status: In Test or Done) needs to be rebuilt, the rollback protocol executes in full. No status changes before the solo confirms.

**Triggers:**
- A regression found in a later slice that traces back to this one
- A design decision that invalidates the approach this slice was built on
- Builder-solo agreement that a clean restart is the right call

**Targeted fix vs. full rebuild:**
- **Targeted fix** — the approach is sound; a specific behavior doesn't work. Fix the behavior, re-run the full QA chain.
- **Full rebuild** — the approach is structurally wrong: design was misread at build start, architecture doesn't fit the requirement, wrong assumptions are baked in. Discard the slice's code. Builder re-reads the spec and design file from scratch before writing any new code.

Builder proposes which scope applies and why. Solo confirms before any status changes or code is discarded.

**Protocol (all steps in the same action — never separated):**

1. Builder states the case: which slice, what's wrong, targeted fix or full rebuild, and why
2. Solo confirms
3. Log the rollback in the Decisions and Change Log (format below)
4. Update the slice record: status → In Build, reason noted in Notes field
5. Cascade to the deliverable: if Accepted → Pending Acceptance. Automatic — the condition for Accepted is no longer met.
6. Cascade to the phase: if Completed → In Progress. Automatic — the condition for Completed is no longer met.
7. If full rebuild: discard the slice's code, re-read the spec and design file from scratch, report what was found before writing any code.

**Rollback log entry:**

```
### [YYYY-MM-DD] — Rollback: SL-[ID] [slice name]
Scope: [Targeted fix | Full rebuild]
Trigger: [Regression from SL-XX | Design decision — [what changed] | Builder-solo agreement]
What's wrong: [specific description]
Status before: [In Test | Done]
Deliverable: [D-ID: Accepted → Pending Acceptance | No cascade — deliverable not Accepted]
Phase: [Phase N: Completed → In Progress | No cascade — phase not Completed]
Confirmed by: Solo
```

---

## Who Captures What and When

| Skill | Owns |
|---|---|
| `design-review` | Births slice records. Captures: ID, name, status, plain language description, technical description, design anchor, process anchor, done criteria, self-verification checklist, dependencies, references, notes. Marks data anchor as Pending if data-scaffold has not run. Leaves phase and deliverable blank — marked pending. |
| `data-scaffold` | Fills data anchor on every slice it creates mock data for. Goes back into the slice record and completes that field. |
| `prd-to-plan` | Creates all deliverable and phase records — full records, all fields. Goes back into every slice record and adds phase and deliverable assignment. Nothing leaves prd-to-plan with blank phase or deliverable fields on Ready slices. |
| `solo-build` | Updates status throughout the lifecycle. Populates builder confirmation at slice, deliverable, and phase presentation time. Writes review_url to the slice record at code-complete. Executes re-phasing protocol when needed. |
| `solo-qa` | Drives slice from In QA toward In Test. May add notes to slice record. |
| `phase-test` | Drives phase from In Test toward Completed. |
| `qa-triage` | Assesses Done slice bugs for rollback scope (targeted fix vs. full rebuild). Surfaces rollback proposal to solo. Does not execute status changes — rollback protocol in solo-build owns that. |
| `solo-build` / `autopilot` | Creates and maintains `docs/metrics.json` — initialized at first slice, updated at rework events and slice Done, finalized at phase test gate open. |
| `phase-test` | Writes phase test outcome to `docs/metrics.json` when gate opens. |

---

## metrics.json

`docs/metrics.json` is the project-level metrics file. Created automatically by solo-build or autopilot at the start of the first slice. Read by Solo Companion to surface build health per project and across projects.

**Schema:**

```json
{
  "project": "[project name from handoff.md]",
  "phase_test": {
    "result": "in-progress | pass",
    "refinement_cycles": 0
  },
  "slices": {
    "SL-001": {
      "rework_cycles": 0,
      "code_review_flags": 0,
      "refinement_cycles": 0
    }
  },
  "summary": {
    "total_slices": 0,
    "slices_with_rework": 0,
    "total_code_review_flags": 0,
    "phase_test_refinement_cycles": 0
  }
}
```

**Field definitions:**

| Field | Written by | When |
|-------|-----------|------|
| `project` | solo-build / autopilot | File initialization |
| `phase_test.result` | phase-test | Gate opens — set to `"pass"` |
| `phase_test.refinement_cycles` | autopilot (Refinement) | Each Refinement cycle completion; phase-test reads from current-phase.md at gate open |
| `slices.[ID].rework_cycles` | solo-build / autopilot | Slice selected for build and already has an entry (prior In QA → back to In Build) |
| `slices.[ID].code_review_flags` | Reserved — not yet wired | Future: code-review-and-quality will populate |
| `slices.[ID].refinement_cycles` | Reserved — not yet wired | Future: autopilot Refinement delta slices |
| `summary.total_slices` | solo-build / autopilot | Updated each time a slice reaches Done |
| `summary.slices_with_rework` | solo-build / autopilot | Updated each time a slice reaches Done with rework_cycles > 0 |
| `summary.total_code_review_flags` | Reserved | Future |
| `summary.phase_test_refinement_cycles` | phase-test / autopilot | Same value as phase_test.refinement_cycles |

**Rules:**
- Never delete the file during a build — only append and increment
- Never reset counters — they accumulate across the full build
- `summary` must stay in sync — recalculate after every Done transition

