---
name: solo-build
description: Slice-by-slice build execution for the solo builder framework. Checks slice status before anything else — only Ready slices can enter build. States the next Ready slice by plan priority — never asks the solo what to work on. Surfaces all four anchors (design, data, done, process) before writing a line of code, and hands off to solo-qa when the slice is code-complete. When no Ready slices exist, reaches Build Active, no Ready slices status — diagnoses blockers and hands off to the right skill. Never builds on a non-Ready slice.
---

# Solo Build

*One slice at a time. In journey order. Anchored to the design.*

**Core question:** "What's the next slice to build, and do we have everything we need to build it correctly?"

This skill is the execution layer of the framework. The backlog tells you what exists and what's Ready. This skill tells you what to build next, how to approach it, and when to hand it off. It does not decide scope — that's already in the backlog. It executes scope correctly.

---

## Session Start — Read Before Building

At the start of every build session, before selecting or starting any slice, read these documents:

1. **Records spec** at `docs/records-spec.md` — the canonical record format for slice, deliverable, and phase records
2. **Backlog** — current slice statuses, deliverable structure, phase structure, priority order
3. **Discovery brief** — the agreed problem, users, and constraints
4. **To-be process map** — the agreed process being implemented
5. **Tech context** — stack, conventions, constraints
6. **Data mapping** — field sources and mock data structure
7. **Design sprint artifact(s)** — the visual contract

Do not rely on conversation history or memory from a previous session. Read the current state of these files. If any document is missing, name it before proceeding.

After reading, confirm:
> "Session context loaded: [N] slices in backlog, [N] Ready. Active deliverable: [D-ID] — [Name]. Next slice in priority: SL-[ID]."

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
> **Starting Deliverable [D-ID] — [Name]** *(Type: Screen | Logic | Integration)*
>
> What you'll have when this is done: [plain language description]
>
> Screens: [screen file → screen name (primary | affected)]
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

Read the design file now. Find the element. Before writing a line of code, confirm what you see:
> "Design anchor confirmed: [screen-file] open. [Element name] — [describe what you see: layout, fields, colors, interactions]."

If the element cannot be found in the file, stop. Do not build from memory of what the element might look like.

**Anchor 2 — Data anchor**
The specific mock data fields this slice consumes, and where they live.

Format: `[mock-file] → [field names] → eventual real source per data-mapping.md`
Example: `data/mock/players.json → slot_tag, slot_target, slot_role_text → MFL Rosters API`

The mock data layer is the data source during build. The slice reads from the mock layer, not from hardcoded values in the UI. The data mapping doc shows where each field eventually comes from.

**Anchor 3 — Done anchor**
Two parts: the functional done criteria and the quality contract. Both are read from the backlog before any code is written.

**Functional done criteria** — the 2–3 verifiable statements that close this slice. These are what get handed to `solo-qa` for the browser sign-off.

Format: criteria listed exactly as they appear in the backlog
Example:
- WR2 slot tag renders correctly from mock data
- Slot target number displays with correct formatting (14.2 pts)
- Switch context toggle is present and visible (non-functional in Phase 1)

**Quality contract** — the specific non-functional requirements this slice must satisfy. These are what get checked by `code-review-and-quality` before the slice can advance. They are build requirements, not post-build aspirations. Read them now and treat them as constraints the code must satisfy — not a checklist to verify at the end.

Example:
- If the data fetch fails, the component renders an error state — not a blank screen
- Player name field rejects empty string at submission; error message appears inline
- No values hardcoded in the component — all data comes from the mock layer fields named in the data anchor

If the quality contract is missing from the backlog, stop. The slice is not Ready. Return it to design review.
If the quality contract lines are vague ("handle errors gracefully") — sharpen them to specific behavior before starting. A vague contract gives code review nothing to check.

**Anchor 4 — Process anchor**
The step in the to-be process map this slice implements. Read `docs/process/to-be-[name].md` and identify the step.

Format: `[to-be map file] → [step name] → [position in flow]`
Example: `docs/process/to-be-player-evaluation.md → Step 3: system displays slot context → main path, after player lookup`

If the slice doesn't map to a step in the to-be map, stop and ask: is this slice implementing something that wasn't in the agreed process? That's a decision that needs to be made explicitly — not silently built.

---

## Build Execution

### Before writing code

**Step 0 — Read the full slice spec and design file. This is not optional.**
Before creating a branch or writing any code, read the complete slice record from the backlog — every field, not just the anchors. Then open and read the design file if a design anchor is present. Do not rely on memory of a prior read. Do not skip this for slices that seem simple or familiar.

Confirm both were read by producing a verbatim quote from each:
- An exact string from the slice record — a class name, a field name, a done criterion, a constraint. Word for word, not paraphrased.
- An exact string from the design file — a label, a measurement, a class, specific copy. Word for word, not summarized.

A paraphrase or general description does not count. If you cannot produce a verbatim quote from each file right now, you have not read them. Read them before proceeding. A wrong quote surfaces immediately at review — that is the check.

1. **Create the feature branch** — read `docs/tech-context.md` for the project's branching model, then create the branch:
   - Standard format: `feature/SL-[ID]-[short-slug]`
   - Example: `feature/SL-003-player-overview-card`
   - Branch from the base branch specified in tech-context (e.g., `development` for Bayer Aurora, `main` for a general solo project)
2. State all four anchors explicitly
3. Read the design screen file. Find the anchor element. Report what you see before proceeding.
4. Read the relevant mock data — know the exact field names
5. State a brief build plan that covers both functional steps and quality contract implementation. Contract steps are not an afterthought — they appear in the numbered sequence alongside functional steps:

   *"1. Create component structure → verify: renders. 2. Wire mock data → verify: correct values display. 3. Apply styles from design → verify: matches screen. 4. Implement error state per contract [failure state line] → verify: error renders on simulated failure. 5. Add input validation per contract [validation line] → verify: empty string rejected at submission."*

   If the quality contract has no applicable items for a step type (e.g. a pure display slice with no user inputs), note it explicitly in the plan rather than leaving it out silently.

### During build

- Build against the design screen, not against a mental model of it
- Pull data from the mock layer — never hardcode values that should come from data
- Match the design closely enough that the QA visual check will pass — not pixel-perfect, but clearly the same thing
- When something in the build conflicts with the design, stop and surface it: *"The design shows X but implementing it reveals Y — do we update the design or adjust the implementation?"* Don't silently resolve it.
- If a discovery during build would affect other slices, flag it: *"Building this slice reveals that SL-007 will need to account for Z — noting in the backlog."*
- Comment non-obvious logic as you write it — not as a cleanup pass. If code is doing something that would surprise a reader (a workaround, a subtle invariant, a constraint from the design that isn't obvious from the code), add the comment before moving on. Obvious code needs no comment. Logic that derives from a specific design decision or data model does.

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

"Code-complete" means: the slice renders correctly against mock data and matches the design screen. It does not mean done. Done requires the builder to self-verify, present to the solo, and get sign-off.

**Step 1 — Run the self-verification checklist against the running app, then walk the quality contract.**
Open the running app. Work through every item on the self-verification checklist by looking at the rendered output — not by reading the code. For each item, state what was actually observed:

After the checklist, walk every observable quality contract item in the running app. Don't just confirm the happy path — trigger the failure states, test the edge cases, submit bad input:
- Simulate a failure (disconnect, bad response, empty data) and confirm the error state renders
- Submit empty or invalid input and confirm validation fires at the right point with the right message
- For any security contract line — confirm user-supplied content is not rendered raw

For each contract item walked: state what was triggered and what was observed. If a contract item is not observable in the running app (pure backend logic), note it — code review will cover it. Do not skip observable contract items. Presenting a slice that hasn't been walked through its own contract is the failure mode this step exists to prevent.

```
Builder confirmation:
  ✓/✗ [item] — [what was seen: "the player name 'Josh Allen' renders in the slot row, matching slot_tag in players.json"]
```

The difference:
- ❌ "Data renders correctly." — code assertion, not verification
- ✅ "The player name 'Josh Allen' renders in the slot row — matches `slot_tag: 'Josh Allen'` in players.json." — observed output

Stating what the code is supposed to produce is not valid evidence. Only what was observed in the running output counts. If any item cannot be verified against the running app, fix the blocker first. If any item is flagged (✗), fix it before presenting. Do not present a slice with an unresolved self-verification item.

**Step 2 — Commit the work.**
Execute the commit directly — do not hand this to the solo. Read `docs/tech-context.md` for any project-specific commit conventions, then stage the changed files and commit with message: `SL-[ID] code-complete — [slice name]`.

Commit message format is deliberate: the slice ID makes it traceable in git history. Never use vague messages ("wip", "updates", "fix"). Every commit must be traceable to a backlog slice.

**Step 3 — Update the backlog: status → `In QA`. Write review_url.**
Set slice status to `In QA`. Write the review URL to the `Review URL` field in the slice record — the exact URL where the solo can open the completed work in a browser. If the slice has no previewable output (pure logic, infrastructure), write `None`.

**Step 4 — Present to the solo.**
Show the completed builder confirmation and state readiness for review:

> "SL-[ID] — [Name] is ready for review.
>
> Builder confirmation:
>   ✓ [item] — [what was observed]
>   ✓ [item] — [what was observed]
>
> Done criteria to verify:
>   - [criterion 1]
>   - [criterion 2]
>
> Review: [review_url from slice record]"

**Step 5 — Invoke `code-review-and-quality` immediately.**
Do not wait for the solo to trigger it. The handoff is automatic — solo-build to code-review-and-quality to solo-qa is a chain, not a handoff the solo manages.

If code review passes, it invokes solo-qa automatically.
If code review fails, it returns the slice to In Build with specific notes — fix and resubmit.

**Review delivery:** When the slice produces UI or HTML output, serve it as a viewable page before asking for feedback. Open it in the browser or provide a live local URL. The solo signs off on what they can see — not on a description of what was built.

**Deliverable completion check** — after a slice is marked Done, check if all slices in its deliverable are now Done. If they are, run the deliverable self-verification checklist before triggering acceptance:

**Step 1 — Run the deliverable self-verification checklist.**
This checks that all slices work correctly together — not a re-check of individual slices. Flow, state handoffs, data passing between components, the complete user journey through all slices. Populate the deliverable builder confirmation field in the backlog:

```
Builder confirmation:
  ✓/✗ [item — how slices interact, what was observed]
  ✓/✗ [item — end-to-end flow result]
```

If any item is flagged, fix it before presenting the deliverable for acceptance.

**Step 2 — Present to the solo:**
> "All slices in Deliverable [D-ID] — [Name] are Done. Builder confirmation complete:
>
>   ✓ [deliverable-level item — what was observed]
>   ✓ [deliverable-level item — what was observed]
>
> Acceptance criteria to verify:
>   1. [criterion 1]
>   2. [criterion 2]
>
> Ready for your sign-off."

**Step 3 — Trigger solo-qa deliverable acceptance automatically.** Do not wait for the solo to ask for it. Update deliverable status → `Pending Acceptance`.

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

## When Stuck

**Two failed attempts with no progress on the same problem: stop.**

Do not make a third attempt. Re-read the full slice spec and the design file from scratch — not from memory, not from a prior read in this session. Report what the spec says vs. what was built. Then ask one diagnostic question before touching any code.

**If the solo asks to step back at any point: execute it immediately.**

Do not assess whether a restart is warranted. Do not suggest one more attempt. Do not express confidence that the current approach will work. Stop, re-read the full slice spec and design file, and report what was found. The solo's direction to step back overrides the builder's judgment about progress — without exception.

---

## Backlog Updates During Build

The backlog is a live document. Every status change is written immediately — before moving to the next action. Not at session end. Not after the slice is Done. The moment the status changes, the file changes.

- Slice enters build → **Ready → In Build** — update before writing the first line of code
- Slice is code-complete → **In Build → In QA** — update before triggering code review
- Slice passes code review → **In QA → In Test** — update when solo-qa hands off to phase-test
- Slice passes QA → **In Test → Done** — update before moving to the next slice
- Slice marked Done → **update handoff immediately**: "What was just completed" (this slice's details), "Where we are" (current build state), "Next session picks up at" (next slice in priority). Same pass as the backlog update — not deferred to session end.
- Deliverable all slices Done → **Defined → Pending Acceptance** — update when presenting to solo
- Deliverable solo signs off → **Pending Acceptance → Accepted** — update immediately on sign-off
- A discovery affects another slice → note it in that slice's record now, before continuing

The test: if the session ended right now, would the backlog AND the handoff correctly reflect the build state? If not, both are already out of sync.

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

## Re-Phasing Protocol

When the solo requests moving a slice or deliverable to a different phase during build, this protocol executes in full — no partial execution. A quiet edit to the phase field is not acceptable.

1. Solo states what's moving and why
2. Log the decision immediately in the Decisions and Change Log in `docs/backlog.md`
3. Update the moved item — phase field updated in the slice or deliverable record
4. Update the source phase record — add to "Explicitly out of scope" noting what moved and why
5. Update the destination phase record — add to its deliverables list
6. Assess source phase — does it still answer its stated question with the item removed? If not, update the phase description and question
7. Assess destination phase — does the moved item fit the question that phase answers? If not, update the phase description and question

All seven steps happen in the same action. The log entry and the record updates are never separated. Confirm when complete:
> "SL-[ID] moved from Phase [N] to Phase [N]. Backlog updated — source and destination phase records revised, decision logged."

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

## Session Signals

Passive telemetry. When any of the following events occur, append one line to `.claude/session-signals.tmp` at the project root. Create the file if it doesn't exist. Do not summarize multiple events into one line — one line per event.

**Trigger events:**
- Stuck protocol fires — two failed attempts reached
- Slice rebuilt — builder had to re-read and rebuild after stuck protocol
- Priority deviation — solo explicitly redirected build away from plan priority

**Format:**
```
YYYY-MM-DD | [git user name] | [project name] | build | [signal name]
```

**How to write the signal** — run this command, substituting values:
```
/bin/zsh -c 'echo "$(date +%Y-%m-%d) | $(git config user.name) | [project] | build | [signal]" >> .claude/session-signals.tmp'
```

Get the project name from `docs/continuity/handoff.md` or the project directory name. Write the signal at the moment the trigger condition is confirmed — not at session end.

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Starting or partially working on a non-Ready slice | Build contradicts the open design decisions — producing work that needs to be redone | Hard stop on non-Ready status. Name the status, name what's needed to reach Ready, offer nothing else |
| Offering "we can knock out X while we build Y" | Rationalizes starting work that isn't anchored — exactly the gap the status gate exists to prevent | One path: promote the slice to Ready first, then build |
| Leaving build after hitting zero Ready slices without diagnosing blockers | The solo doesn't know why they're stuck or where to go next | Surface Build Active, no Ready slices — diagnose each In Review slice, name the right next skill, hand off |
| Skipping the self-verification checklist before presenting to the solo | The solo reviews work that the builder hasn't verified — "looks good" reviews happen | Run every self-verification item, populate builder confirmation, present confirmation alongside the work |
| Presenting a deliverable for acceptance without running deliverable-level self-verification | Slice-level Done doesn't catch cross-slice integration bugs | Deliverable self-verification is a separate pass — checks flow, handoffs, and end-to-end journey |
| Moving a slice to a different phase with a quiet field edit | Phase records go out of sync silently — source and destination phases no longer reflect the plan | Execute the full re-phasing protocol — 7 steps, decision logged, all affected records updated |
| Starting a slice without producing a verbatim quote from the slice spec and the design file | Building from memory produces work that contradicts the spec or design — a full rebuild is the cost | Produce verbatim quotes from both files before writing code. A paraphrase is not a quote. No quotes = not read |
| Self-verification that asserts ("data renders correctly") instead of observing | Assertions are code inspection — the same check code-review-and-quality already ran | Open the running app; state what was seen in the rendered output. Observed output only |
| Continuing past two failed attempts on the same problem | Spiral without direction — the solo's time burns while confidence substitutes for diagnosis | Hard stop. Re-read the full slice spec and design file from scratch, report what was found, ask one question |
| Declining or deferring a solo request to step back | The builder's assessment that progress is close does not override the solo's direction | The solo's step-back request is an immediate directive — stop, re-read, report. No exceptions |
