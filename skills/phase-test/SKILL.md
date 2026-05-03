---
name: phase-test
description: Full-phase testing orchestrator for the Solo Builder Framework. Invoked explicitly by the solo when they decide a phase is built. Sequences seven specialist lenses — environment readiness, use case creation, data validation, testing, regression, and acceptance review — and produces a single gate decision: ready to deploy or hold with specific items to resolve. Never invoked automatically. The solo makes the deliberate call.
---

# Phase Test

*Slice QA confirms each piece was built correctly. Phase test confirms the whole thing works.*

**Core question:** "Does this phase — as a complete, integrated experience — solve what we set out to solve, with real data, end to end?"

This is not a repeat of slice QA. Slice QA verified each slice against its done criteria in isolation. Phase test verifies the slices working together as a product — real data, full journeys, integration points between screens, and the original intent from the discovery brief.

---

## When to Invoke

The solo invokes `/phase-test` when they have made a deliberate decision: this phase is built. Not when the last slice hits Done automatically — when the solo looks at the backlog and says "we're done with Phase 1."

**Readiness — three states:**

**Ready (invoke now)**
- All current-phase slices show `In Test` in the backlog — meaning solo-qa has signed off on each one individually
- All open qa-triage items from the build phase are resolved, or explicitly deferred to a future phase with a backlog entry
- All integration deliverables are Accepted — not just the Screen companions
- No new slices are being added — scope is frozen for this phase
- The solo can describe the core user journey without checking the design

**Not yet (hold off)**
- Any slice is still In Build, In QA, or blocked — not yet reached `In Test`
- Open qa-triage items from the build phase haven't been classified yet
- Integration deliverables were scoped but haven't been Accepted
- The solo isn't sure what's left — uncertainty means the backlog isn't current, not that nothing's left

**Overdue (invoke now — you're drifting)**
- All slices have been `In Test` for multiple sessions and new slices keep being added that weren't in the original plan
- The solo is running solo-qa on slices that already show `In Test`
- Changes are being made as polish or "small improvements" rather than resolving a specific open item
- Scope is expanding to absorb work that could be Phase 2

The key reframe: phase test isn't evidence you're done — it's the process for finding out if you are. The criteria above confirm you've built what you planned. Phase test confirms that what you built actually works.

---

## What Phase Test Reads

Before any specialist lens runs, read:

- `docs/records-spec.md` — canonical record formats and status definitions; confirms what each status means before any status transitions are made
- `docs/discovery-brief.md` — the original use cases, the problem being solved, the user and their need
- `docs/design/sprint-[id].html` — the design artifact, all screens, the intended journey
- `docs/backlog.md` — all In Test slices, their done criteria, their design and data anchors, and the phase record being tested
- `docs/data-mapping.md` — field names, API sources, expected data shapes
- `docs/tech-context.md` — stack, API patterns, environment configuration

---

## The Seven Specialist Lenses

Run in sequence. Each stage must complete before the next begins — except Stages 4 and 5, which run together.

---

### Stage 1 — Environment Readiness

*Pre-flight. Nothing else runs until this passes.*

The environment readiness lens confirms the test environment is actually ready to test against. Testing against a misconfigured environment produces false results — passes that will fail in production, failures that are actually config problems.

**Check each of the following:**

**Mock data is no longer the active source**
- Mock indicator badge is removed from all screens
- `data/mock/` is not the active data layer — real APIs or DB are the source
- No components still importing directly from the mock layer

**Environment is pointed at real systems**
- API endpoints in config point to test environment, not localhost mock servers
- Database connection (if applicable) is pointing at test DB, not local
- Auth (if applicable) is configured for the test environment

**All Done slices are deployed**
- Every slice with status `✓ Done` in the backlog is present and accessible in the test environment
- No "works locally, not deployed yet" slices

**Environment is stable**
- The app loads without errors
- No console errors on initial load
- No obvious broken states before any interaction

**Report:**
```
Environment Readiness
✅ Mock layer inactive — real APIs active
✅ All Done slices deployed
✅ App loads clean
❌ Auth not configured for test environment — [specific issue]

Status: NOT READY — resolve before continuing.
```

If anything fails: stop. List exactly what's missing. Do not proceed to Stage 2 until the environment is confirmed ready.

---

### Stage 2 — Use Case Creator

*Builds the test plan every other specialist works from.*

The use case creator lens reads the discovery brief and design sprint artifact, then derives a structured test plan. This is not invented — it's extracted from what was already agreed on.

**Derive test scenarios from:**

- **Primary use cases** — every use case in the discovery brief becomes a test scenario. These are the core journeys the product was built to support.
- **Design journey** — walk the design sprint screens in order. Each screen-to-screen transition is a scenario step.
- **Edge cases** — the mock data was seeded with edge cases (empty states, boundary values, long names, nulls). Each edge case from the mock layer becomes a test scenario.
- **Done criteria** — each slice's done criteria gets a test scenario. These were how we defined "built correctly" — now they get tested in the live environment.

**Test scenario format:**
```
Scenario [N]: [Name]
Source: [discovery brief / design screen / edge case / done criteria]
Precondition: [what state the system needs to be in]
Steps:
  1. [action]
  2. [action]
  3. [action]
Expected outcome: [what should happen, specifically]
Data dependency: [what real data this requires]
```

**Output:** A numbered test plan. Every specialist from Stage 3 onward works from this plan. It is the shared reference for the rest of the phase test.

---

### Stage 3 — Data Specialist

*Confirms real data is flowing correctly before anyone walks a scenario.*

The data specialist lens verifies the mock-to-real transition actually worked — not just that config points at the right place, but that data is reading and writing correctly through the full stack.

**Read operations — for each data entity in `docs/data-mapping.md`:**
- Call the API endpoint (or query the DB) and confirm it returns data
- Compare the response shape against `data-mapping.md` — do field names match?
- Confirm the field values appear correctly in the UI — data is rendering, not hardcoded
- Check that empty/null responses are handled (the edge cases from mock data are now real scenarios)

**Write operations — for any slice that writes data:**
- Execute the write action in the test environment
- Confirm the data persists (read it back after writing)
- Confirm the UI reflects the written state
- Confirm a failed write is handled gracefully

**API contract validation:**
- Every field in `data-mapping.md` that was listed as "eventual real source" — confirm that source is now connected and returning the expected shape
- Flag any mismatches between what data-mapping.md expected and what the real API returns

**Report:**
```
Data Specialist
✅ Players API — returning expected shape, all fields present
✅ Read confirmed — slot_target rendering from API (not mock)
❌ Write — save action not persisting: POST /players/update returning 404
✅ Empty state — no-data scenario handled correctly

Issues found: 1 — logged.
```

Any data issue that would make test scenarios unreliable: route to `qa-triage` before the tester runs on affected scenarios. Flag which scenarios are blocked and which can proceed.

---

### Stages 4 + 5 — Orchestration

**When Agent tool is available (Claude Code):** Spawn Stage 4 (Tester) and Stage 5 (Regression Specialist) as concurrent sub-agents using the Agent tool. Pass each agent the full test plan from Stage 2, the relevant backlog slices, and its specialist instructions below. Wait for both to return before proceeding to Stage 6.

**When running in Cursor (no Agent tool):** Run Stage 4 fully, then Stage 5 fully, in sequence. Same steps — no skipping. Just one model, sequential.

---

### Stage 4 — Tester (runs with Stage 5)

*Walks every scenario from the test plan. Records evidence, not assumptions.*

The tester lens executes each scenario from the test plan produced in Stage 2. This is active testing — not reading code, not inspecting config. Walking the product the way a user would.

**For each scenario:**

1. Set up the precondition
2. Execute each step
3. Observe the outcome
4. Compare against expected outcome
5. Record pass or fail with specific evidence

**Evidence standard:**
- ✅ "Navigated to player overview → slot context card rendered with slot_target `14.2` from API"
- ❌ "Save action executed → changes not reflected on return to list screen. Expected: updated record. Actual: stale data showing pre-save values."

Not "it seemed to work." Named evidence every time.

**When a scenario fails:**
- Record the failure with full evidence
- Invoke `qa-triage` — classify (bug / missing requirement / regression), scope it, route it
- Continue with the next scenario — don't stop the full test run for one failure
- Note which subsequent scenarios may be affected by the failure

**Edge case scenarios:**
- Execute the edge cases derived from the mock data
- Empty states, boundary values, null handling — these were built for and now need to be verified against real conditions

**Output:** Pass/fail per scenario with evidence. Failure count and list of open qa-triage items.

---

### Stage 5 — Regression Specialist (runs with Stage 4)

*Re-walks Done slices to confirm later work didn't break earlier work.*

The regression specialist lens specifically focuses on integration points — the places where slices connect to each other. A slice can pass QA in isolation and fail when another slice changes shared state, shared components, or shared navigation.

**For each Done slice in the backlog:**

1. Navigate to the slice's screen in the test environment
2. Verify the slice's done criteria still hold — each criterion, with evidence
3. Specifically check integration points:
   - Does state from a prior screen reach this slice correctly?
   - Does action on this screen correctly update state used by a later screen?
   - Does shared navigation include this screen without breaking adjacent screens?
   - Does shared component behavior remain consistent?

**What to look for:**
- A Done slice whose data no longer renders correctly after a later API connection was made
- A Done slice whose layout breaks because a shared component was modified for a later slice
- A Done slice whose navigation is broken because a later screen was added to the route structure

**When regression is found:**
- Record what was working and what's now broken
- Invoke `qa-triage` — classify as regression, identify the root cause (which later change caused it)
- Note whether the regression affects only this slice or adjacent ones

**Output:** Pass/fail per Done slice with integration point evidence. Regression count and root cause notes.

---

### Stage 6 — Acceptance Reviewer

*Runs after Stages 4 and 5 complete. The PM lens on the whole phase.*

The acceptance reviewer lens asks a different question than every other stage: not "does it work" but "does it solve the problem?" This is the lens that goes back to the discovery brief and asks whether the product that was built matches the intent that was defined.

**Read the discovery brief. For each use case:**

- Can a user actually accomplish this? Not "is the screen there" — can a real person complete the task?
- Does the experience match the intent? The discovery brief describes what the user needs. Does the built product deliver that?
- Are there gaps between what was designed and what was built that affect the user's ability to accomplish their goal?
- Does the product hold together as a coherent experience — or does it feel like individual slices that don't flow?

**The acceptance question for each use case:**
> "A user who needs to [use case] can now [accomplish goal] — and the experience feels like it was designed for them, not assembled from parts."

Pass or fail. With specific evidence if it fails.

**What acceptance review is not:**
- Not re-running technical tests (the tester and regression specialist did that)
- Not redesigning (design review's job)
- Not finding new features to add (scope discipline)

It's asking: did we build the right thing, and does a person using it feel like we did?

**Process-level mismatch:** If the acceptance reviewer determines that the delivered experience doesn't match the discovery intent at the *process* level — not a missing feature, not a design gap, but the agreed steps in the to-be map were wrong or incomplete — invoke `process-change` before the gate decision. The gate stays on HOLD until process-change completes.

**Output:** Pass/fail per use case. Summary of whether Phase 1 achieves its intent. Specific gaps named if it doesn't.

---

## Stage 7 — Gate Decision

The orchestrator synthesizes all specialist outputs into a single gate decision.

**Collect:**
- Environment readiness: pass / issues resolved
- Data specialist: open issues count
- Tester: pass/fail count, open issues
- Regression specialist: regression count, open issues
- Acceptance reviewer: use case pass/fail

**Gate decision format:**
```
Phase Test — [Phase Name] — [date]

Environment:    ✅ Ready
Data:           ✅ All reads/writes confirmed
Testing:        12/14 scenarios passed — 2 open issues
Regression:     8/8 Done slices passing
Acceptance:     3/3 use cases: intent confirmed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GATE: HOLD

Open before deploy:
  1. [open issue] — [what it is, which scenario]
  2. [open issue] — [what it is, which scenario]

Once resolved and re-tested: gate opens. No full re-run required — 
only the affected scenarios need to be re-walked.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Or:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GATE: OPEN — ready to deploy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**HOLD does not mean start over.** It means: here is the specific list of what needs to be resolved. Fix those items, re-test the affected scenarios, and the gate opens. The full phase test does not re-run — only the affected areas.

---

## When the Gate Opens — Phase Completion Record

When the gate opens, the orchestrator does one final thing before handing to deploy: appends a **phase completion record** to `docs/backlog.md`.

This is the definitive statement that a chunk of work is finished. Not a technical log — a clear declaration the solo can point at, share with a stakeholder, or orient from at the start of the next session.

**Format — appended to the bottom of `docs/backlog.md`:**

```
---

## ✅ Phase [N] Complete — [Phase Name]
**Completed:** [YYYY-MM-DD]
**Status:** Tested and ready to deploy

### What was delivered
[2–3 plain-English sentences. What capability exists now that didn't before. 
Written for a stakeholder, not a developer. No slice IDs, no technical jargon.]

### Slices completed
[N] slices — all Done and verified

### Test confirmation
Phase test gate: OPEN  
Report: docs/phase-test-[phase]-[date].md  
Use cases verified: [N/N]  
Regressions found: [0 / N resolved]  

### What comes next
[Phase N+1] — [one sentence describing what the next phase will deliver]

---
```

**Before appending the phase completion record**, confirm version control is clean:
- All Done slices have been pushed and merged per the branching model in `docs/tech-context.md`
- No open feature branches for this phase — every slice branch is merged
- The base branch (`development` or `main`) reflects the full phase

If any slice branches are still open: merge them before marking the phase complete. The phase completion record must reflect a clean, unified state — not a mix of merged and unmerged work.

4. **Update `docs/metrics.json`** — write the phase test outcome (create the file if it doesn't exist):
   - `phase_test.result` → `"pass"`
   - `phase_test.refinement_cycles` → read `docs/continuity/current-phase.md`: if `Refinement cycle:` is present and not "None", use that integer value; otherwise 0
   - `summary.phase_test_refinement_cycles` → same value as above

**Why this lives in the backlog:**
The backlog is the document everyone already reads — the solo at session start, the framework for context, a stakeholder wanting a status. Adding the phase completion record there means the full story is in one place: slice-by-slice progress AND phase-by-phase milestones. No hunting across multiple documents to understand where the project stands.

**When the gate opens, execute these backlog updates immediately — before handing to deploy:**

1. **Update all slice statuses** — every slice in this phase moves from `In Test` to `Done` in `docs/backlog.md`. This is what `Done` means: built, QA signed-off, and phase-verified end-to-end.
2. **Update the phase record status** — in the phase record in `docs/backlog.md`, update `Status: In Progress` to `Status: Completed`. Also populate the phase-level `Builder confirmation` field with the phase test results summary.
3. **Update At a Glance** — reflect the new Done counts and Completed phase status.

**What "tested and ready to deploy" means:**
- All phase slices are `Done` in the backlog — updated in step 1 above
- Phase record shows `Completed` in the backlog — updated in step 2 above
- Phase test gate is OPEN (confirmed in the report)
- No open qa-triage items from the phase test
- Acceptance reviewer confirmed use case intent

That status line is not a guess or an optimistic label. It's a confirmed statement with receipts in the phase test report — and the backlog record matches it.

---

## Re-Testing After a Hold

When qa-triage items from phase test are resolved:

1. The tester re-runs only the failed scenarios — not the full test plan
2. The regression specialist re-checks only the affected slices
3. If the acceptance reviewer flagged gaps, those use cases are re-walked
4. Environment and data don't re-run unless the fix touched config or APIs

The gate opens when all hold items are cleared.

---

## Output — Phase Test Report

Saved to `docs/phase-test-[phase]-[date].md`. Referenced by the deploy step.

Contains:
- Environment readiness confirmation
- Full test plan with pass/fail per scenario
- Data specialist findings
- Regression results per Done slice
- Acceptance review per use case
- All open issues and their resolution status
- Gate decision with date

---

## Session Signals

Passive telemetry. When any of the following events occur, append one line to `.claude/session-signals.tmp` at the project root. Create the file if it doesn't exist. One line per event.

**Trigger events:**
- Phase-test HOLD — gate decision is HOLD (one or more blocking failures remain unresolved)

**Format:**
```
YYYY-MM-DD | [git user name] | [project name] | test | phase-test HOLD
```

**How to write the signal:**
```
/bin/zsh -c 'echo "$(date +%Y-%m-%d) | $(git config user.name) | [project] | test | phase-test HOLD" >> .claude/session-signals.tmp'
```

Get the project name from `docs/continuity/handoff.md` or the project directory name. Write the signal at the moment the HOLD decision is logged — before surfacing it to the solo.

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Invoking phase-test before all current-phase slices are In Test | Testing an incomplete build produces unreliable results | Confirm all slices reached In Test (solo-qa signed off) before invoking |
| Skipping environment readiness | Everything downstream is unreliable | Stage 1 must pass before anything else runs |
| Stopping the full test run on first failure | Misses other failures; incomplete picture | Route to qa-triage, continue with other scenarios |
| Treating acceptance review as a repeat of testing | Different question entirely | Tester asks "does it work?" — acceptance asks "is it the right thing?" |
| Full re-run after fixing a hold item | Wasteful and unnecessary | Re-test only affected scenarios |
| Solo sign-off at the phase level without phase test | Slice QA alone isn't sufficient | Phase test is the gate before deploy — not optional |
| Continuing to add slices when all planned slices are Done | Scope creep disguised as due diligence — the gate exists to answer whether the plan was right | When the backlog is clean and all slices Done, invoke phase test rather than expanding scope |
