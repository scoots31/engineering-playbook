---
name: solo-build
description: Slice-by-slice build execution for the solo builder framework. Selects the right slice to build next based on dependency order and user journey sequence, surfaces all four anchors (design, data, done, process) before writing a line of code, and hands off to solo-qa when the slice is code-complete. Never builds ahead of the journey. Never starts a slice without all four anchors.
---

# Solo Build

*One slice at a time. In journey order. Anchored to the design.*

**Core question:** "What's the next slice to build, and do we have everything we need to build it correctly?"

This skill is the execution layer of the framework. The backlog tells you what exists and what's Ready. This skill tells you what to build next, how to approach it, and when to hand it off. It does not decide scope — that's already in the backlog. It executes scope correctly.

---

## Slice Selection — What Gets Built Next

Not all Ready slices are equal. The order matters.

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

---

## Backlog Updates During Build

The backlog is a live document. Update it as build progresses:

- Slice status: Ready → In Build → In QA → Done
- Dependencies discovered during build: add them
- Slices affected by current build: note them
- Any open items that need design review attention: flag them

Never let the backlog get out of sync with the actual build state. It's the solo's persistent context — if it's stale, the next session starts from the wrong place.

---

## What Build Does Not Do

- Does not decide scope — that's the backlog
- Does not verify done — that's solo-qa
- Does not redesign — surfaces conflicts, gets decisions, implements what's decided
- Does not build out of journey order without explicit reason
- Does not start a slice without all four anchors
- Does not hardcode data that should come from the mock layer
