---
name: solo-build
description: Slice-by-slice build execution for the solo builder framework. Checks slice status before anything else — only Ready slices can enter build. States the next Ready slice by plan priority — never asks the solo what to work on. Surfaces all four anchors and runs a hard design+data correlation gate before any code is written. Hands off to the Review Agent when builder QA is complete — the builder never declares a slice done. Never asks the solo to run terminal commands. Always provides a live link for review.
---

# Solo Build

*One slice at a time. In journey order. Anchored to the design.*

**Core question:** "What's the next slice to build, and do we have everything we need to build it correctly?"

This skill is the execution layer of the framework. The backlog tells you what exists and what's Ready. This skill tells you what to build next, how to approach it, and when to hand it off. It does not decide scope — that's already in the backlog. It executes scope correctly.

**These are not suggestions. They are the rules this skill operates by, without exception:**
- The design file is the contract. Build does not start until it has been fully read and every data point in it is confirmed available.
- The builder never declares a slice done. The Review Agent closes the gate.
- Terminal commands are run directly. The solo is never asked to run a command the builder can run itself.
- Every handoff to the solo includes a live link to the running output.
- No decisions are made unilaterally. Every choice is surfaced to the solo with explicit options.

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

**CI suite check** — if `CI/CD: GitHub Actions` is recorded in `docs/tech-context.md` and a `tests/` directory exists in the project root, run the full test suite before selecting any slice. A red suite means a previous slice introduced a regression. Fix it first — do not start a new slice while the suite is broken. If no `tests/` directory exists yet, skip silently.

After reading, confirm:
> "Session context loaded: [N] slices in backlog, [N] Ready. Active deliverable: [D-ID] — [Name]. Next slice in priority: SL-[ID]."

---

## Slice Selection — What Gets Built Next

**Status gate — before anything else.**
Only slices in `Ready` status can enter build. This check runs before slice selection rules, before the four anchors, before any build discussion.

If the next candidate slice is not in `Ready` status, stop:
> "SL-[ID] is [current status] — not Ready. Build cannot start until design review closes the open items and promotes it to Ready."

Name the status. Name the gap. Do not offer alternatives. Do not suggest working on design "while building." If there are no Ready slices at all:
> "There are no Ready slices right now. [N] slices are In Review, pending design review decisions. The next step is finishing design review to promote slices to Ready — not starting build on In Review slices."

This is not a conversation. A slice in any status other than Ready has open decisions that build will contradict.

---

**Plan-driven selection.** When moving to the next slice, read the backlog, identify the highest-priority Ready slice in journey order, and state it:
> "Next up: SL-[ID] — [Name]. It's [N] in journey order and first in priority among Ready slices."

Do not ask the solo what to work on. The plan exists. Read it and follow it. If the solo wants to divert from priority order, they say so — confirm the divergence explicitly before proceeding: *"Diverting to SL-[X] instead of SL-[Y] which is next in priority. Confirmed."*

---

**Rule 1 — Tracer bullet first.**
Before building any individual screen in full, build the thinnest path all the way through the user journey. The minimum that proves the core loop works end to end — even if every step is minimal. Then expand each step.

**Rule 2 — Journey order, not parallel.**
Build in the order a user travels through the product. The first screen in the journey before the second. This is not about sequencing features — it's about discovering integration problems in the right order, while the codebase is still small enough to fix them cheaply.

**Rule 3 — Dependencies block.**
A slice cannot enter In Build if its dependencies are not Done. The backlog dependency field is a hard gate, not a suggestion. If `SL-003` depends on `SL-001`, `SL-001` must be Done before `SL-003` can start: *"SL-003 is Ready but depends on SL-001 which is still In Build. Building SL-001 first."*

**Rule 4 — Independent screens as parallel exceptions.**
Screens with no shared infrastructure and no journey dependencies can run alongside the main journey if they're Ready and the solo wants to move them forward. Name them explicitly as parallel rather than letting them bleed into the main build sequence.

**Slice selection statement** — always say it before starting:
> "Building SL-[ID] — [Name]. It's next in journey order, dependencies are clear, and it has all four anchors."

**Deliverable orientation** — if this is the first slice in a deliverable, surface the deliverable context before starting:

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

If a deliverable record cannot be found for this slice, stop:
> "No deliverable record found for SL-[ID]. The plan hasn't been set yet — define deliverables before build starts."

---

## The Four Anchors — Required Before Starting

Every slice must have all four before a line of code gets written. If any anchor is missing, stop. Resolve it first.

**Anchor 1 — Design anchor**
The exact screen and element this slice builds. Not just the file — the specific component within it.

Format: `[screen-file] → [element name] → [location on screen]`

**Read the design file now — in full.** Do not skim. Do not rely on a prior read. Open it and read it. The design file is the contract for this slice. Every decision about what to build, how it looks, and what data it shows comes from this file. Nothing else.

After reading, confirm what you see:
> "Design anchor confirmed: [screen-file] open. [Element name] — [describe what you see: layout, fields, colors, interactions, every data-sourced element visible on screen]."

If the element cannot be found in the file, stop. Do not build from memory of what the element might look like.

**When the design source is a Figma file:**

Two additional steps before writing any code:

1. **Extract node properties.** For every element in this slice's scope, extract exact values from Figma node properties — dimensions, spacing, colors, typography. Do not read the design visually and approximate. Extract: then build. Values in code must trace to source values in Figma. Any value that cannot be traced to a Figma node property is an approximation and will fail code review.

2. **Verify the interactive element inventory.** Read the slice record's Notes field. Confirm the interactive element inventory is present. For every element classified as Functional: logic must be wired in this slice or in the named companion slice. For every element classified as Deferred: render as a visible, clearly non-interactive placeholder — not as a working-looking shell. Do not build any interactive element that is not in the inventory. If the inventory is missing, stop — return the slice to design review.

**Anchor 2 — Data anchor**
The specific mock data fields this slice consumes, and where they live.

Format: `[mock-file] → [field names] → eventual real source per data-mapping.md`

The mock data layer is the data source during build. The slice reads from the mock layer, not from hardcoded values in the UI. The data mapping doc shows where each field eventually comes from.

**Anchor 3 — Done anchor**
Two parts: the functional done criteria and the quality contract. Both are read from the backlog before any code is written.

**Functional done criteria** — the 2–3 verifiable statements that close this slice. These are what get handed to the Review Agent for independent verification.

**Quality contract** — the specific non-functional requirements this slice must satisfy. These are build requirements, not post-build aspirations. Read them now and treat them as constraints the code must satisfy — not a checklist to verify at the end.

If the quality contract is missing from the backlog, stop. The slice is not Ready. Return it to design review.
If the quality contract lines are vague ("handle errors gracefully") — sharpen them to specific behavior before starting. A vague contract gives review nothing to check.

**Anchor 4 — Process anchor**
The step in the to-be process map this slice implements.

Format: `[to-be map file] → [step name] → [position in flow]`

If the slice doesn't map to a step in the to-be map, stop and surface it: is this slice implementing something that wasn't in the agreed process? That's a decision for the solo — not something to silently build.

---

## Design + Data Correlation Gate

This gate runs after all four anchors are confirmed, before any branch is created or code written. It is not optional.

**Step 1 — Extract every data-sourced element from the design file.**

Re-read the design file (already open from Anchor 1). Identify every element on the screen that displays, derives from, or depends on data — every field value, label sourced from a record, image, count, calculated value, or conditional state. List them explicitly. Do not assume any element is purely decorative without confirming it.

**Step 2 — Cross-reference against the data anchor.**

For each data-sourced element identified, map it to a specific field in the data spec (mock data file, data-mapping.md, or DB schema). Produce the correlation table:

```
Design element           → Data field             → Source file / table     → Status
[element name]           → [field name]           → [file/table]            → ✓ Confirmed
[element name]           → [field name]           → [file/table]            → ✗ MISSING
```

**Step 3 — Evaluate the table.**

- Every row is ✓ Confirmed → proceed. State: *"Design + data correlation complete. All [N] design data points confirmed in data spec. Proceeding to build."*
- Any row is ✗ MISSING → **hard stop.** Do not open the branch. Do not write any code.

When a MISSING is found:
> "Design + data correlation gate failed. SL-[ID] cannot proceed.
>
> Missing:
> - [design element] requires [field name] — not found in [data spec]
> - [design element] requires [field name] — not found in [data spec]
>
> The design references data that does not exist. Two paths: [A] update the data spec to add the missing fields, or [B] return the slice to design review to revise the design. Which?"

The solo decides. The builder does not resolve this unilaterally.

---

## Build Execution

### Before writing code

**Step 0 — Read the full slice spec and design file. This is not optional.**
Before creating a branch or writing any code, read the complete slice record from the backlog — every field, not just the anchors. Then confirm the design file is still open and current. Do not rely on memory of a prior read. Do not skip this for slices that seem simple or familiar.

Confirm both were read by producing a verbatim quote from each:
- An exact string from the slice record — a class name, a field name, a done criterion, a constraint. Word for word, not paraphrased.
- An exact string from the design file — a label, a measurement, a class, specific copy. Word for word, not summarized.

A paraphrase does not count. If you cannot produce a verbatim quote from each file right now, you have not read them. Read them before proceeding.

**Metrics — initialize or rework check:** Before creating the branch, check `docs/metrics.json`.

- **File doesn't exist** — initialize it:
  ```json
  {
    "project": "[project name from handoff.md]",
    "phase_test": { "result": "in-progress", "refinement_cycles": 0 },
    "slices": {
      "SL-[ID]": { "rework_cycles": 0, "code_review_flags": 0, "refinement_cycles": 0 }
    },
    "summary": { "total_slices": 0, "slices_with_rework": 0, "total_code_review_flags": 0, "phase_test_refinement_cycles": 0 }
  }
  ```
- **File exists, no entry for this slice** — add `"SL-[ID]": { "rework_cycles": 0, "code_review_flags": 0, "refinement_cycles": 0 }` to `slices`.
- **File exists, entry already present** — this is a rework cycle. Increment `rework_cycles` by 1.

**Architecture type gate** — before opening the branch, check the slice's Architecture type field.

- **Leaf node** → proceed normally.
- **Core architecture** → principal engineer review fires first. Do not open the branch until the review is complete.

Invoke principal-engineer with the slice ID, the technical description, and the four anchors. If the PE raises a concern, surface it to the solo before proceeding. If the PE approves, note the approval in the slice record's Notes field and open the branch.

This is not optional. A core architecture slice that enters In Build without a PE review has bypassed the gate that protects the trunk.

**Security class pre-flight** — before opening the branch, read the Security Classification section in `docs/tech-context.md`.

- **Standard only:** No additional pre-flight required. Proceed.
- **Any other class active:** Identify whether this slice touches a data domain relevant to the active class. If it does not touch a sensitive domain, proceed normally.

  If it does touch a sensitive domain: confirm the quality contract's Security field addresses the class-specific requirements. The table below shows what "addressed" means for each class:

  | Class | Security field must cover |
  |---|---|
  | Personal | No PII in logs or error output; PII encrypted at rest; deletion path exists for this record type |
  | Financial | No raw card data; financial record access logged; retention period defined |
  | Authentication | No plaintext credential storage; session tokens expire; credentials not in URLs or logs |
  | Multi-tenant | Tenant ID validated server-side on every query this slice touches; cross-tenant access impossible at query layer |
  | Confidential | Access control enforced server-side; confidential data not in client bundles beyond the user's role |
  | Regulated | Compliance requirements for this slice documented; no new PII collection without disclosure mechanism |

  If the quality contract Security field does not address the class requirements for this slice's data domain, stop and return the slice to design review.

**Slice readiness check** — before opening the branch, confirm four things:
1. **Plain language description is present.** If absent, stop: *"SL-[ID] is missing its plain language description — the solo has no anchor for what this slice delivers. Return to design review to write it before build starts."*
2. **Technical description is present.** If absent, stop: *"SL-[ID] is missing its technical description — the builder has no implementation anchor. Return to design review to write it before build starts."*
3. Can you state what done looks like for this slice as a single concrete observation against the running app? If the done criteria require interpretation to verify, they are too vague — sharpen them now.
4. Is the scope bounded to one user interaction or system behavior? If the slice spans multiple distinct interactions, flag it to the solo before proceeding.

1. **Create the feature branch** — read `docs/tech-context.md` for the project's branching model, then create the branch:
   - Standard format: `feature/SL-[ID]-[short-slug]`
   - Branch from the base branch specified in tech-context
2. State all four anchors explicitly
3. Confirm the design screen file is open and the anchor element is located. Report what you see before proceeding.
4. Read the relevant mock data — confirm the exact field names match what the correlation gate confirmed
5. State a brief build plan that covers both functional steps and quality contract implementation. Contract steps appear in the numbered sequence alongside functional steps — they are not an afterthought:

   *"1. Create component structure. 2. Wire mock data — fields: [names]. 3. Apply styles from design. 4. Implement error state per contract [failure state line]. 5. Add input validation per contract [validation line]."*

### Terminal commands

Run them directly. Every time.

The solo is never asked to run a command in the terminal. Not for installs, not for data scripts, not for servers, not for tests. If a command needs to run, run it.

The only exception: a command that is physically impossible to run — one that requires credentials the builder does not have, or hardware the builder cannot access. In that case, explain specifically why it cannot be run and what is needed. Everything else runs directly.

### During build

- Build against the design screen, not against a mental model of it
- Pull data from the mock layer — never hardcode values that should come from data
- Match the design closely enough that the QA visual check will pass
- When something in the build conflicts with the design, stop and surface it with explicit options: *"The design shows X but implementing it reveals Y. Two paths: [A] or [B]."* The solo decides. Do not resolve design conflicts unilaterally.
- If a discovery during build would affect other slices, flag it: *"Building this slice reveals that SL-007 will need to account for Z — noting in the backlog."*
- Comment non-obvious logic as you write it — not as a cleanup pass. If code is doing something that would surprise a reader (a workaround, a subtle invariant, a constraint from the design that isn't obvious from the code), add the comment before moving on.

### Dependency typing — be explicit

| Dependency type | Meaning |
|----------------|---------|
| **Slice** | Another slice must be Done first — shared component, shared state |
| **Infrastructure** | A backend service, API endpoint, or DB table must exist |
| **Data** | A specific mock entity or real data source must be available |
| **Design** | A design decision is still open — spike or review needed first |

---

## When Build is Code-Complete

"Code-complete" means: the slice renders correctly against mock data and matches the design screen. It does not mean done. The builder does not decide when a slice is done. The Review Agent closes that gate.

### Builder QA

Before signaling anything, the builder runs its own QA pass. This is not self-certification — the builder does not evaluate pass or fail against done criteria. It observes and reports.

**Step 1 — Establish the review port.**

Read `.claude/launch.json`. If absent, read `docs/tech-context.md` for the run command and port, then create `launch.json` at the project root with that command and port. The port in `launch.json` is the single source of truth. The preview server starts on this port. The review link handed to the solo uses this port. These are the same value derived from the same source — there is no separate "review URL" that can diverge from the running port.

Review link format: `http://localhost:[port from launch.json]/[path for this slice]`

**Step 2 — Start the preview server.**

Run `preview_start` using the command from `launch.json`.

**Step 3 — Run the QA observation pass.**

Navigate to the review link. For each item below, state what was observed — not what the code is supposed to produce:

- Screenshot at desktop viewport — describe what renders
- `preview_console_logs` — list any errors (none is a valid observation)
- `preview_network` with filter `failed` — list any failed requests caused by this slice
- Navigate through every interactive element in the slice — describe what happens
- `preview_resize` to mobile (375×812) — screenshot — describe what renders
- Read the actual data store (DB query or file read) — confirm data was written, list what exists

**Step 4 — Produce the QA manifest.**

```
Builder QA manifest — SL-[ID]:
  Desktop render: [what was seen]
  Console: [errors present / none]
  Network: [failed requests caused by this slice / none]
  Interactions: [what each interactive element did when triggered]
  Mobile render: [what was seen]
  Data store read: [what was confirmed to exist in the store]
```

The QA manifest is a record of observations. The builder does not mark items pass or fail. The builder does not state whether done criteria are met. The builder does not say the slice is ready. The Review Agent makes those determinations independently.

**Step 5 — Stop the preview server.**

Run `preview_stop`.

**Step 6 — Commit the work.**

Read `docs/tech-context.md` for any project-specific commit conventions, then stage the changed files and commit: `SL-[ID] code-complete — [slice name]`.

Every commit must be traceable to a backlog slice. Never use vague messages ("wip", "updates", "fix").

**Step 7 — Update the backlog: status → `In QA`. Write review_url.**

Set slice status to `In QA`. The review URL is `http://localhost:[port from launch.json]/[path]` — the same value used in Step 1. If the slice has no previewable output (pure logic, infrastructure), write `None`.

**Step 8 — Generate test file** — if `CI/CD: GitHub Actions` is recorded in `docs/tech-context.md`.

Translate the slice's done criteria into a runnable test file at `tests/test_SL-[ID].py`. Run the full suite. Green → include the test file in the commit. New test immediately fails → fix the test, not the code. Existing test now fails → fix the regression before committing.

If `CI/CD` is not set to `GitHub Actions`, skip entirely.

**Step 9 — Signal the Review Agent.**

> "SL-[ID] — [Name] builder QA complete.
>
> QA manifest:
>   Desktop render: [summary]
>   Console: [summary]
>   Network: [summary]
>   Interactions: [summary]
>   Mobile render: [summary]
>   Data store: [summary]
>
> Review link: [http://localhost:[port]/[path]]
>
> Handing to Review Agent."

The builder's role for this slice is complete at this signal. The builder does not evaluate whether the slice meets its done criteria. The builder does not say the slice passed. The Review Agent runs next.

---

## Review Agent

The Review Agent is an independent agent. It does not receive the builder's QA manifest or any self-assessment from the builder. It forms its own observations from the source files and the running output.

**When Agent tool is available (Claude Code):** Spawn the Review Agent as a sub-agent. Pass it only: the slice ID, the backlog path, the design file path, the data spec path, and the review URL. Nothing else. The Review Agent reads everything it needs independently.

**When running in Cursor (no Agent tool):** Read `skills/review-agent/SKILL.md` and run the full review inline with the same independence standard — no reference to builder observations.

The Review Agent:
1. Reads the design file in full — independently, not from the builder's description
2. Reads the data spec — independently
3. Starts the preview server on the port from `launch.json`
4. Navigates to the review URL and screenshots the output
5. Reads the actual data store — queries or reads the file directly, confirms data exists
6. Cross-references every design data point against the running output — each one is observed or missing
7. Walks every done criterion — each one is observed as met or not met
8. Stops the preview server

The Review Agent returns one of two outputs:

**CLEARED:**
> "Review Agent — SL-[ID] CLEARED.
>
> Design review: [what was observed against the design file]
> Data verification: [what was read from the data store]
> Done criteria:
>   ✓ [criterion] — [what was observed]
>   ✓ [criterion] — [what was observed]
>
> Gate closed. Advancing to In Test."

**GAPS:**
> "Review Agent — SL-[ID] GAPS FOUND.
>
> Gaps:
>   - [specific gap: design element not present, or present but wrong]
>   - [specific gap: data point missing from store]
>   - [specific gap: done criterion not met — what was observed instead]
>
> Returning to builder. Address each gap and signal QA complete again."

The Review Agent never says "not a blocker." A gap is a gap. It is not the Review Agent's role to judge severity — that is the solo's call if they choose to weigh in. If a gap exists, the output is GAPS, full stop.

**After GAPS:** The builder addresses every item in the gap list. No partial fixes. When all gaps are addressed, the builder runs the QA pass again (Steps 1–9 above) and signals complete. The Review Agent runs again from scratch.

**After CLEARED:** Update backlog status to `In Test`. Present to the solo:

> "SL-[ID] — [Name] cleared by Review Agent and ready for your review.
>
> Review link: [http://localhost:[port]/[path]]
>
> Done criteria to verify:
>   - [criterion 1]
>   - [criterion 2]"

The solo reviews at the link. Code review runs automatically next — do not wait for the solo to trigger it.

**Code review:** Spawn `code-review-and-quality` as a sub-agent (Claude Code) or run inline (Cursor). Pass: slice ID, modified file paths, quality contract verbatim from backlog, four anchors. If code review passes, invoke solo-qa automatically. If code review fails, return to In Build with specific notes.

---

## Deliverable Completion

After a slice is marked Done, check if all slices in its deliverable are now Done. If they are:

**Step 1 — Run the deliverable QA pass.**
This checks that all slices work correctly together — not a re-check of individual slices. Flow, state handoffs, data passing between components, the complete user journey through all slices.

The deliverable QA pass follows the same rules as builder QA: observe and report. The builder does not declare the deliverable done.

**Step 2 — Signal the Review Agent for deliverable-level review.**
The Review Agent runs the same independent check across the full deliverable — design correlation, data verification, end-to-end flow, acceptance criteria. Returns CLEARED or GAPS.

**Step 3 — After CLEARED, present to the solo:**
> "All slices in Deliverable [D-ID] — [Name] cleared by Review Agent.
>
> Review link: [http://localhost:[port]/[path for deliverable entry point]]
>
> Acceptance criteria to verify:
>   1. [criterion 1]
>   2. [criterion 2]"

**Step 4 — Trigger solo-qa deliverable acceptance automatically.** Update deliverable status → `Pending Acceptance`.

**Step 5 — Recommend a session boundary.**
> "Deliverable [D-ID] — [Name] is complete and in acceptance. Clean session boundary — the work is coherent and the next deliverable starts fresh. Recommended: update the handoff and close here. Start [next deliverable name] in a new session. Continue now, or close out?"

Wait for the answer. If closing: hand off to product-continuity to update the handoff. If continuing: pick up the next slice in priority order.

---

## Mid-Deliverable Documentation Checkpoint

When a slice reaches In Test and it is the **4th slice in a deliverable that has more than 4 slices total**, pause and run a documentation checkpoint before selecting the next slice.

This fires once per deliverable — only at slice 4.

> "SL-[ID] is In Test — that's 4 slices through [D-ID] — [Name]. [N] slices remain. Updating the handoff before continuing."

Execute without waiting:
1. Update `docs/continuity/handoff.md` — `## Open right now` section: current deliverable, slices completed, slices remaining, next slice in priority
2. Confirm: *"Handoff updated — [D-ID] at 4/[N] slices, [next slice] up next. Continuing."*
3. Pick up the next slice immediately.

---

## On-Demand Views

When the solo says **"show progress"**, return the active deliverable table inline.

When the solo says **"show plan"**, return all deliverables across the full build.

Both views surface inline — never "go look at a file."

---

## Mid-Build Discoveries

**Minor — implementation detail, doesn't affect design or other slices**
Resolve it, note it in the slice detail in the backlog, continue.

**Design gap — something on the screen isn't buildable as shown**
Stop. Surface it with explicit options. *"The design shows X but implementing it reveals Y. Two paths: [A] or [B]."* The solo decides. Do not silently simplify.

**Affects other slices — the build reveals something that changes upstream or downstream slices**
Flag it in the backlog immediately. Note which slices are affected and why. Continue with the current slice if possible, but make the impact visible before the next slice starts.

**Blocks the current slice — a dependency wasn't actually resolved**
Stop the current slice. Move it back to In Review with a note. Pick the next appropriate slice while the blocker is resolved.

**Map-level conflict — the build reveals the to-be map itself is wrong**
Stop the current slice. Move it back to In Review. Invoke `process-change` immediately — this is the agreed process step itself that is incorrect or missing. The current slice stays In Review until process-change completes and a new or revised process anchor is confirmed.

---

## When Stuck

**Two failed attempts with no progress on the same problem: stop.**

Do not make a third attempt. Re-read the full slice spec and the design file from scratch — not from memory. Report what the spec says vs. what was built. Then ask one diagnostic question before touching any code.

**If the solo asks to step back at any point: execute it immediately.**

Do not assess whether a restart is warranted. Do not suggest one more attempt. Stop, re-read the full slice spec and design file, and report what was found. The solo's direction to step back overrides the builder's judgment — without exception.

---

## Rollback

When a slice that has already passed QA (In Test or Done) needs to be rebuilt, this is a rollback — not a stuck situation.

**The builder raises it. The solo confirms it. Nothing changes before confirmation.**

**What triggers a rollback proposal:**
- A regression in a later slice that traces back to this one
- A design decision that invalidates the approach this slice was built on
- Any situation where the work needs to be rebuilt, not just re-QA'd

**When raising a rollback:**
1. State what's being rolled back and why
2. Assess the scope — targeted fix or full rebuild
3. State which scope applies and why
4. Wait for solo confirmation before touching any status or discarding any code

On confirmation, execute the rollback protocol from `docs/records-spec.md` — status cascade, log entry, and if full rebuild, re-read the spec and design file from scratch before writing any new code.

---

## Backlog Updates During Build

The backlog is a live document. Every status change is written immediately — before moving to the next action.

- Slice enters build → **Ready → In Build** — before writing the first line of code
- Builder QA complete → **In Build → In QA** — before signaling the Review Agent
- Review Agent clears → **In QA → In Test** — when CLEARED is returned
- Slice passes QA → **In Test → Done** — before moving to the next slice
- Slice marked Done → update `docs/metrics.json` summary: increment `summary.total_slices`; if rework_cycles > 0, also increment `summary.slices_with_rework`
- Slice marked Done → update handoff immediately: "What was just completed," "Where we are," "Next session picks up at." Same pass as the backlog update — not deferred to session end.
- Deliverable all slices Done → **Defined → Pending Acceptance**
- Deliverable solo signs off → **Pending Acceptance → Accepted**
- A discovery affects another slice → note it in that slice's record now, before continuing

The test: if the session ended right now, would the backlog AND the handoff correctly reflect the build state? If not, both are already out of sync.

---

## Build Active, No Ready Slices

When all current-phase slices are either Done, In Review, or Deferred — and none are Ready:

**Step 1 — Diagnose.** Read each In Review slice. Name the specific reason it isn't Ready.

**Step 2 — Surface the state:**
> "Build Active, no Ready slices.
> - SL-[ID]: [specific blocker, one line]
>
> [Skill name] is the next step to unblock [slice IDs]. Switching now."

**Step 3 — Hand off** to the right skill. Do not wait for the solo to invoke it.

**Step 4 — Resume.** When the unblocking skill promotes a slice to Ready: *"SL-[ID] is now Ready. Build can resume."*

Build Active, no Ready slices is not a reason to start work on In Review slices. The status gate still applies — always.

---

## Re-Phasing Protocol

When the solo requests moving a slice or deliverable to a different phase during build, all seven steps execute — no partial execution:

1. Solo states what's moving and why
2. Log the decision immediately in the Decisions and Change Log in `docs/backlog.md`
3. Update the moved item — phase field updated
4. Update the source phase record — add to "Explicitly out of scope"
5. Update the destination phase record — add to its deliverables list
6. Assess source phase — does it still answer its stated question? If not, update
7. Assess destination phase — does the moved item fit? If not, update

Confirm when complete:
> "SL-[ID] moved from Phase [N] to Phase [N]. Backlog updated — source and destination phase records revised, decision logged."

---

## What Build Does Not Do

- Does not decide scope — that's the backlog
- Does not declare a slice done — the Review Agent closes the gate
- Does not self-certify — observations only, never pass/fail evaluations
- Does not redesign — surfaces conflicts, gets decisions from the solo, implements what's decided
- Does not build out of journey order without explicit reason
- Does not start a slice without all four anchors and a passing correlation gate
- Does not hardcode data that should come from the mock layer
- Does not start, discuss, or partially execute any slice not in Ready status
- Does not ask the solo to run terminal commands
- Does not hand off work without a live review link
- Does not make decisions unilaterally — every choice goes to the solo

---

## Session Signals

When any of the following events occur, append one line to `.claude/session-signals.tmp` at the project root. Create the file if it doesn't exist. One line per event.

**Trigger events:**
- Stuck protocol fires — two failed attempts reached
- Slice rebuilt — had to re-read and rebuild after stuck protocol
- Priority deviation — solo explicitly redirected build away from plan priority
- Correlation gate failed — design data point had no confirmed source in data spec
- Review Agent returned GAPS — gap count ≥ 2

**Format:**
```
YYYY-MM-DD | [git user name] | [project name] | build | [signal name]
```

Run directly:
```
/bin/zsh -c 'echo "$(date +%Y-%m-%d) | $(git config user.name) | [project] | build | [signal]" >> .claude/session-signals.tmp'
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Rule |
|---|---|---|
| Starting a slice without reading the design file in full | Build contradicts the design because the builder worked from a prior read or a mental model | Read the design file now, for this slice, before writing any code. Every time. |
| Starting a slice without running the correlation gate | Build references data that doesn't exist — discovered at QA instead of at gate | Correlation gate runs every slice, after four anchors, before the branch opens |
| Builder declares a slice done or passes its own done criteria | The builder is not a neutral judge of its own work | Builder signals QA complete and stops. Review Agent closes the gate. |
| Builder says "not a blocker" | Severity is the solo's call, not the builder's | GAPS is GAPS. Return the gap list. The solo decides what to do with it. |
| Self-cert language ("data renders correctly") | A claim about the code, not an observation of the output | State what was seen in the running app. Observed output only. |
| Asking the solo to run a terminal command | Solo should not need to open a terminal | Run it directly. If physically impossible, explain specifically why and what is needed. |
| Handing off without a review link | The solo cannot review work they can't see | Every handoff includes a live link derived from the launch.json port. No exceptions. |
| Preview on a different port than the review link | Broken link handed to the solo | One port, from launch.json, used for preview server and review link — same value, same source. |
| Resolving a design conflict unilaterally | Silently changing scope | Stop. Surface with two explicit options. Solo decides. |
| Starting or partially working on a non-Ready slice | Build contradicts open design decisions | Hard stop on non-Ready status. Name the status, name what's needed to reach Ready. |
| Skipping the mid-deliverable documentation checkpoint | Stale handoff if session ends mid-deliverable | Checkpoint at slice 4 of a 5+ slice deliverable is mandatory and automatic. |
| Continuing past two failed attempts on the same problem | Spiral without direction | Hard stop. Re-read spec and design file from scratch, ask one question. |
| Declining a solo step-back request | Builder's confidence does not override solo's direction | Step-back is an immediate directive. Stop, re-read, report. No exceptions. |
