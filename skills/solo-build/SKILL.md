---
name: solo-build
description: Slice-by-slice build execution for the solo builder framework. Checks slice status before anything else — only Ready slices can enter build. States the next Ready slice by plan priority — never asks the solo what to work on. Surfaces all four anchors (design, data, done, process) before writing a line of code, and hands off to solo-qa when the slice is code-complete. When no Ready slices exist, reaches Build Active, no Ready slices status — diagnoses blockers and hands off to the right skill. Never builds on a non-Ready slice.
---

# Solo Build

*One slice at a time. In journey order. Anchored to the design.*

**Core question:** "What's the next slice to build, and do we have everything we need to build it correctly?"

This skill is the execution layer of the framework. The backlog tells you what exists and what's Ready. This skill tells you what to build next, how to approach it, and when to hand it off. It does not decide scope — that's already in the backlog. It executes scope correctly.

---

## Slice Selection — What Gets Built Next

Not all Ready slices are equal. The order matters. But before any ordering logic runs, one check happens first.

**Status gate — before anything else.**
Only slices in `Ready` status can enter build. This check runs before slice selection rules, before the four anchors, before any build discussion.

If the next candidate slice is not in `Ready` status, stop:
> "SL-[ID] is [current status] — not Ready. Build cannot start until design review closes the open items and promotes it to Ready."

Name the status. Name the gap. Do not offer alternatives. Do not suggest working on design "while building." If there are no Ready slices at all, surface that directly:
> "There are no Ready slices right now. [N] slices are In Review, pending design review decisions. The next step is finishing design review to promote slices to Ready — not starting build on In Review slices."

This is not negotiable and not a conversation. A slice in any status other than Ready has open decisions that build will contradict.

---

**Plan-driven selection.** When moving to the next slice, read the backlog, identify the highest-priority Ready slice in journey order, and state it:
> "Next up: SL-[ID] — [Name]. It's [N] in journey order and first in priority among Ready slices."

Do not ask the solo "what would you like to work on?" The plan exists. The skill reads it and follows it. If the solo wants to divert from priority order, they say so — and the skill confirms the divergence explicitly before proceeding: *"You've asked to move to SL-[X] instead of SL-[Y] which is next in priority. Confirming that diversion and proceeding."*

---

**Rule 1 — Tracer bullet first.**
Before building any individual screen in full, build the thinnest path all the way through the user journey. The minimum that proves the core loop works end to end — even if every step is minimal. For a player evaluation tool: can you look up a player, see their core evaluation, navigate to the next screen? That thin path first. Then expand each step.

**Rule 2 — Journey order, not parallel.**
Build in the order a user travels through the product. The first screen in the journey before the second. The second before the third. This is not about sequencing features — it's about discovering integration problems in the right order, while the codebase is still small enough to fix them cheaply.

**Rule 3 — Dependencies block.**
A slice cannot enter In Build if its dependencies are not Done. The backlog dependency field is a hard gate here, not a suggestion. If `SL-003` depends on `SL-001`, `SL-001` must be Done before `SL-003` can start. Surface this clearly: *"SL-003 is Ready but depends on SL-001 which is still In Build. Building SL-001 first."*

**Rule 4 — Independent screens as parallel exceptions.**
Screens with no shared infrastructure and no journey dependencies (settings, auth, help) can run alongside the main journey if they're Ready and the solo wants to move them forward. Name them explicitly as parallel rather than letting them bleed into the main build sequence.

**Slice selection statement** — always say it out loud before starting:
> "Building SL-[ID] — [Name]. It's next in journey order, dependencies are clear, and it has all four anchors."

**Deliverable orientation** — if this is the first slice in a deliverable, surface the deliverable context before starting. The solo needs to know what's being delivered before the first line of code is written:

---
> **Starting Deliverable [D-ID] — [Name]** *(Type: Screen | Logic)*
>
> What you'll have when this is done: [solo description]
>
> Acceptance criteria we're building toward:
> 1. [criterion 1]
> 2. [criterion 2]
> 3. [criterion 3]
>
> [N] slices make this up: SL-001 · SL-002 · SL-003
---

If a deliverable record cannot be found for this slice in the backlog, stop:
> "No deliverable record found for SL-[ID]. Run prd-to-plan to define deliverables before build starts."

---

## The Four Anchors — Required Before Starting

Every slice must have all four before a line of code gets written. If any anchor is missing, stop. Resolve it first.

**Anchor 1 — Design anchor**
The exact screen and element this slice builds. Not just the file — the specific component within it.

Format: `[screen-file] → [element name] → [location on screen]`
Example: `sprint-p1.html → Slot context card → top of overview body, below player tabs`

Open the file. Look at the element. Make sure the implementation target is unambiguous.

**Anchor 2 — Data anchor**
The specific mock data fields this slice consumes, and where they live.

Format: `[mock-file] → [field names] → eventual real source per data-mapping.md`
Example: `data/mock/players.json → slot_tag, slot_target, slot_role_text → MFL Rosters API`

The mock data layer is the data source during build. The slice reads from the mock layer, not from hardcoded values in the UI. The data mapping doc shows where each field eventually comes from.

**Anchor 3 — Done anchor**
The 2–3 criteria from the backlog that close this slice. These are what get handed to `solo-qa`.

Format: criteria listed exactly as they appear in the backlog
Example:
- WR2 slot tag renders correctly from mock data
- Slot target number displays with correct formatting (14.2 pts)
- Switch context toggle is present and visible (non-functional in Phase 1)

If the done criteria are vague — "it works" is not a criterion — sharpen them before starting. Concrete and verifiable only.

**Anchor 4 — Process anchor**
The step in the to-be process map this slice implements. Read `docs/process/to-be-[name].md` and identify the step.

Format: `[to-be map file] → [step name] → [position in flow]`
Example: `docs/process/to-be-player-evaluation.md → Step 3: system displays slot context → main path, after player lookup`

If the slice doesn't map to a step in the to-be map, stop and ask: is this slice implementing something that wasn't in the agreed process? That's a decision that needs to be made explicitly — not silently built.

---

## Build Execution

### Before writing code

1. **Create the feature branch** — read `docs/tech-context.md` for the project's branching model, then create the branch:
   - Standard format: `feature/SL-[ID]-[short-slug]`
   - Example: `feature/SL-003-player-overview-card`
   - Branch from the base branch specified in tech-context (e.g., `development` for Bayer Aurora, `main` for a general solo project)
2. State all four anchors explicitly
3. Read the design screen — not from memory, actually open it
4. Read the relevant mock data — know the exact field names
5. State a brief build plan: *"1. Create component structure → verify: renders. 2. Wire mock data → verify: correct values display. 3. Apply styles from design → verify: matches screen."*

### During build

- Build against the design screen, not against a mental model of it
- Pull data from the mock layer — never hardcode values that should come from data
- Match the design closely enough that the QA visual check will pass — not pixel-perfect, but clearly the same thing
- When something in the build conflicts with the design, stop and surface it: *"The design shows X but implementing it reveals Y — do we update the design or adjust the implementation?"* Don't silently resolve it.
- If a discovery during build would affect other slices, flag it: *"Building this slice reveals that SL-007 will need to account for Z — noting in the backlog."*

### Dependency typing — be explicit

Not all dependencies are the same. When a slice has a dependency, name what kind:

| Dependency type | Meaning |
|----------------|---------|
| **Slice** | Another slice must be Done first — shared component, shared state |
| **Infrastructure** | A backend service, API endpoint, or DB table must exist |
| **Data** | A specific mock entity or real data source must be available |
| **Design** | A design decision is still open — spike or review needed first |

Typing the dependency makes it clear what's actually blocking and what can be worked around.

### When build is code-complete

"Code-complete" means: the slice renders correctly against mock data and matches the design screen. It does not mean done. Done requires QA — two stages of it.

State it and trigger the chain:

> "SL-[ID] is code-complete. Committing and running code-review-and-quality."

**Commit the work:**
```
git add [changed files]
git commit -m "SL-[ID] code-complete — [slice name]"
```

Commit message format is deliberate: the slice ID makes it traceable in git history. Do not use vague messages ("wip", "updates", "fix"). Every commit should be traceable to a backlog slice.

Update the backlog: status → `In QA`.

Then invoke `code-review-and-quality` immediately. Do not wait for the solo to trigger it. The handoff is automatic — solo-build to code-review-and-quality to solo-qa is a chain, not a handoff the solo manages.

If code review passes, it invokes solo-qa automatically.  
If code review fails, it returns the slice to In Build with specific notes — fix and resubmit.

**Review delivery:** When the slice produces UI or HTML output, serve it as a viewable page before asking for feedback. Open it in the browser or provide a live local URL. The solo signs off on what they can see — not on a description of what was built.

**Deliverable completion check** — after a slice is marked Done, check if all slices in its deliverable are now Done. If they are:
> "All slices in Deliverable [D-ID] — [Name] are Done. Running deliverable acceptance."
Then trigger solo-qa deliverable acceptance automatically. Do not wait for the solo to ask for it.

---

## On-Demand Views

When the solo says **"show progress"**, return the active deliverable table inline:

```
Deliverable [D-ID] — [Name] (Screen | Logic)
[solo description]

| Slice ID | Description | Deliverable | Type | Status |
|---|---|---|---|---|
| SL-001 | [desc] | [D-ID] | Screen | ✓ Done |
| SL-002 | [desc] | [D-ID] | Screen | In Build |
| SL-003 | [desc] | [D-ID] | Screen | Ready |

Acceptance criteria:
1. [criterion 1] — [verified ✅ | pending]
2. [criterion 2] — [verified ✅ | pending]
3. [criterion 3] — [verified ✅ | pending]
```

When the solo says **"show plan"**, return all deliverables across the full build:

```
| Deliverable | Type | Status | Slices |
|---|---|---|---|
| D-001 — [Name] | Screen | ✓ Accepted | SL-001 · SL-002 |
| D-002 — [Name] | Logic | In Progress | SL-003 (✓) · SL-004 (In Build) · SL-005 (Ready) |
| D-003 — [Name] | Screen | Backlog | SL-006 · SL-007 |
```

Both views surface inline — never "go look at a file." Both also surface automatically at key moments: deliverable start, slice review, deliverable completion.

---

## Mid-Build Discoveries

Build reveals things the design review didn't. How to handle each:

**Minor — implementation detail, doesn't affect design or other slices**
Resolve it, note it in the slice detail in the backlog, continue.

**Design gap — something on the screen isn't buildable as shown**
Stop. Surface it specifically. *"The design shows the slot target updating on context switch but that requires real-time state management that isn't in the current data model. Options: a) simplify to static display in Phase 1, b) add this to the design review for a decision."* Don't silently simplify — get a decision.

**Affects other slices — the build reveals something that changes upstream or downstream slices**
Flag it in the backlog immediately. Note which slices are affected and why. Continue with the current slice if possible, but make the impact visible before the next slice starts.

**Blocks the current slice — a dependency wasn't actually resolved**
Stop the current slice. Move it back to In Review with a note. Pick the next appropriate slice while the blocker is resolved.

**Map-level conflict — the build reveals the to-be map itself is wrong**
Stop the current slice. Move it back to In Review. Invoke `process-change` immediately — this is not a design gap or a dependency issue, it is the agreed process step itself that is incorrect or missing. The current slice stays In Review until process-change completes and a new or revised process anchor is confirmed.

---

## Backlog Updates During Build

The backlog is a live document. Update it as build progresses:

- Slice status: Ready → In Build → In QA → Done
- Dependencies discovered during build: add them
- Slices affected by current build: note them
- Any open items that need design review attention: flag them

Never let the backlog get out of sync with the actual build state. It's the solo's persistent context — if it's stale, the next session starts from the wrong place.

---

## Build Active, No Ready Slices

When all current-phase slices are either Done, In Review, or Deferred — and none are Ready — the build reaches **Build Active, no Ready slices** status. The build is not closed — it is ongoing, waiting for slices to advance to Ready.

**Step 1 — Diagnose.** Read each In Review slice from the backlog. Name the specific reason it isn't Ready:
- Open design decisions → design review needed
- Open spike needed → research-spike
- Blocked on another slice → name the blocking slice and what it needs

**Step 2 — Surface the state:**
> "Build Active, no Ready slices.
> - SL-[ID]: [specific blocker, one line]
> - SL-[ID]: [specific blocker, one line]
>
> [Skill name] is the next step to unblock [slice IDs]. Switching now."

**Step 3 — Hand off** to the right skill. Do not wait for the solo to invoke it.

**Step 4 — Resume.** When the unblocking skill promotes a slice to Ready, it says: *"SL-[ID] is now Ready. Build can resume."* Solo-build picks back up with the newly promoted slice, starting from the status gate.

Build Active, no Ready slices is not a reason to start work on In Review slices. The status gate still applies — always.

---

## What Build Does Not Do

- Does not decide scope — that's the backlog
- Does not verify done — that's solo-qa
- Does not redesign — surfaces conflicts, gets decisions, implements what's decided
- Does not build out of journey order without explicit reason
- Does not start a slice without all four anchors
- Does not hardcode data that should come from the mock layer
- Does not start, discuss, or partially execute any slice not in Ready status — including suggesting to "work on design while building"

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Starting or partially working on a non-Ready slice | Build contradicts the open design decisions — producing work that needs to be redone | Hard stop on non-Ready status. Name the status, name what's needed to reach Ready, offer nothing else |
| Offering "we can knock out X while we build Y" | Rationalizes starting work that isn't anchored — exactly the gap the status gate exists to prevent | One path: promote the slice to Ready first, then build |
| Leaving build after hitting zero Ready slices without diagnosing blockers | The solo doesn't know why they're stuck or where to go next | Surface Build Active, no Ready slices — diagnose each In Review slice, name the right next skill, hand off |
