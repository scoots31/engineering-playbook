---
name: solo-qa
description: Verifies that a completed slice is actually done — not just code-complete. Invoked automatically by code-review-and-quality after it passes. Part 1 is AI verification against the full slice spec with active testing. Part 2 is the solo's sign-off in the browser — required, never skipped, cannot be performed by the AI.
---

# Solo QA

*Code-complete is not done. Done requires two signatures — the AI and the solo.*

**Core question:** "Did we build the right thing — and does the solo confirm it in practice?"

This skill runs after `code-review-and-quality` has passed and logged its confirmation. Code quality is not solo-qa's job — that's already been confirmed. Solo-qa covers the two things code review cannot verify:

1. **The AI confirms:** the slice was built against its full spec — requirements, done criteria, and design — verified actively, not by reading code and assuming
2. **The solo confirms:** it looks right, feels right, and the criteria hold in practice when they actually use it

Neither alone is sufficient. The AI can verify criteria technically and still miss something only the solo's eye would catch. The solo's sign-off is not a rubber stamp — it's a genuine check the AI cannot perform.

---

## When This Runs

Invoked automatically by `code-review-and-quality` after it passes. Not before. Not manually. The chain is:

```
solo-build declares code-complete
  → code-review-and-quality runs
    → PASS: logs confirmation, invokes solo-qa
    → FAIL: returns to In Build
```

If solo-qa is invoked without a code review confirmation in the backlog, stop immediately:
> "No code review confirmation found for SL-[ID]. Run `/code-review-and-quality` first."

---

## Part 1 — AI Verification

The AI runs this part. The solo is not involved yet.

### Step 0 — Gate Check

Read `docs/backlog.md`. Find the slice record. Confirm the code review pass is logged in the slice detail:
*"Code review passed [date]..."*

If it's not there, stop. Do not proceed. Return the message above.

---

### Step 1 — Read the Full Slice Spec

This is not the same as reading the done criteria. Read all four anchors from the backlog slice record:

**Design anchor** — which screen, which element, where on screen. Open the design file. Look at the element being verified. Know exactly what it's supposed to look like and contain.

**Data anchor** — which mock file, which fields, what the eventual real source is. Open `data/mock/[entity].json`. Note the actual values in the fields this slice consumes. These are what you'll verify against in the running slice.

**Done anchor** — the 2–3 criteria that close this slice. Read them exactly as written. These are what get verified next.

**Process anchor** — which step in the to-be process map this slice implements. Confirms the slice built the right thing, not just something that matches the design.

Don't skip this step. Verifying criteria without first reading the full spec is how things get marked Done that weren't built against the design.

---

### Step 2 — Active Verification of Done Criteria

Open the slice running in preview. Walk through each done criterion actively. Named evidence only — not assumptions from reading code.

The difference:
- ❌ "The code reads `slot_target` from the mock layer." (code inspection, not verification)
- ✅ "The rendered value is `14.2` — matches `slot_target: 14.2` in `data/mock/players.json`. Not hardcoded." (active verification)

For each criterion:

**Render checks** — is the element present and visible? Look at it in the preview. Not in the source. In the running output.

**Data checks** — do the values match the mock data exactly? Cross-reference what's rendered against the mock file values. If `players.json` has `slot_target: 14.2` and the screen shows `14.2` — pass. If it shows `14.0` or any other value — fail and name why.

**Edge case checks** — the mock data was seeded with edge cases for this moment. Check them. If the mock has an empty state, a long name, a null value — verify those render without breaking.

**Interactive element checks** — elements specified as present but non-functional in Phase 1 should be present and visible. They don't need to work. They need to exist.

Format each criterion:
```
✅ [Criterion] — [evidence: what was observed and where]
❌ [Criterion] — [what was observed vs. what was expected, specifically]
```

If any criterion fails: stop. Return to In Build with a specific note. Do not proceed to design fidelity check. The slice is not ready for sign-off.

---

### Step 3 — Design Fidelity

With the design screen open alongside the running slice, compare:

- **Layout and structure** — does the component hierarchy match? Are sections in the right order?
- **Data rendering** — are values rendering from the mock layer, not hardcoded? (Cross-check with mock file if anything looks off)
- **Interactive elements** — present as specified, even if non-functional in Phase 1
- **Edge and empty states** — the mock data has these seeded; verify they surface correctly
- **Mock indicator badge** — if mock data is active, the badge should be visible

This is not pixel-perfect comparison. The standard is: would a person looking at both the design and the implementation say these are clearly the same thing?

If design fidelity fails: stop. Return to In Build with specific notes. Not "the layout is off" — "the slot context card is positioned below the player tabs in the design but renders above them in the implementation."

---

### AI Verification Conclusion

If all checks pass:
> "AI verification complete for SL-[ID]. Done criteria met with evidence, design fidelity confirmed. Ready for solo sign-off."

If anything fails:
> "Returning SL-[ID] to In Build. [Specific issue and what needs to be fixed before resubmission.]"

Update backlog status accordingly.

---

## Part 2 — Solo Sign-Off

The AI cannot do this part. This requires the solo to actually look at the thing running in a browser — not a screenshot, not a preview summary.

When AI verification passes, present the solo with a clear, structured sign-off request:

---

> **SL-[ID] [Name] — ready for your sign-off**
>
> AI verification passed. Please open these two things side by side:
> - Running slice: [review_url from slice record]  
> - Design reference: [design file path] → [element name]
>
> Confirm each of these:
> 1. [Done criterion 1 — exactly as written in the backlog]
> 2. [Done criterion 2]
> 3. [Done criterion 3]
>
> Does this look right and match the design? Any issues before we mark it Done?

---

Wait for the solo's response. Do not mark Done until they confirm.

**Solo responses:**

| Response | Action |
|----------|--------|
| "Yes / Looks good / Done" | Mark In Test, update backlog, check if dependent slices unblock |
| "Almost — [small thing]" | Fix it, re-present. No need to re-run full AI verification for minor adjustments |
| "No — [specific issue]" | Return to In Build if it's a build issue. Flag for design review if it's a design issue |
| "Something feels off but I can't place it" | Ask one focused question: "Is it the layout, the data, or the behavior?" Narrow it, then decide path forward |

---

## Marking In Test

When solo confirms:

1. Update backlog: slice status → `In Test`
2. Add to slice detail: *"QA passed [date]. Verified: [done criteria summary]. Code review: passed. AI verification: passed. Solo sign-off: confirmed."*
3. Check if any slices were blocked on this one — if so, they can now move to Ready or In Build
4. Update At a Glance counts in the backlog header

The slice moves to `Done` when phase-test completes and the gate opens. `In Test` means: QA passed, waiting on phase-level verification.

**Then handle version control** — read `docs/tech-context.md` for the project's branching model and follow it:

| Branching model | Action on Done |
|-----------------|----------------|
| **Feature branch + PR** (e.g., Bayer Aurora) | Push the feature branch, open a PR to `development`. PR title: `SL-[ID] — [slice name]`. Body: done criteria met, code review passed, solo sign-off confirmed. |
| **Feature branch, solo merge** (general solo, no PR review) | Push the feature branch, merge to `development` or `main`. Delete the feature branch after merge. |
| **Trunk-based** (single branch, no feature branches) | Push the commit directly. |

When in doubt, read the branching model from `docs/tech-context.md` — it was established before build started and is the authority.

**Commit message on merge (if squashing):**
```
SL-[ID] Done — [slice name]

Done criteria verified. Code review passed. Solo sign-off confirmed.
```

Done is permanent unless a later slice reveals a regression — in which case, reopen with a specific note about what regressed and why.

---

## Deliverable Acceptance

When all slices in a deliverable are In Test, solo-qa runs a deliverable-level acceptance check. This is triggered automatically by solo-build — not by the solo. It is separate from and in addition to individual slice sign-offs. A deliverable is not accepted by the sum of its slice approvals — it requires its own verification pass.

### Step 1 — Read the Deliverable Record

From `docs/backlog.md`, read the full deliverable record. The fields needed for this check:
- **Plain language description** — what gets presented to the solo at acceptance time; read this exactly, don't paraphrase
- **Technical description** — what was supposed to be built at the implementation level; confirms scope
- **Screens** — which screens this deliverable touches (primary and affected); confirms what to open in the browser
- **Acceptance criteria** — what gets verified; these are the same criteria agreed before build started
- **Self-verification checklist** — what the builder should have confirmed before triggering this check
- **Builder confirmation** — already populated by the builder at presentation time; read it before running your own verification. If it's missing or empty, stop: the builder did not complete their self-verification. Return to In Build.

Also read the **type** — it determines the verification method.

### Step 2 — Verify Against Acceptance Criteria

**Screen deliverable:**
Open the full deliverable experience in the browser — not individual slices in isolation, but the complete flow or screen as the solo will experience it. Verify each acceptance criterion against what's running:
```
✅ [Criterion] — [evidence: what was observed and where]
❌ [Criterion] — [what was observed vs. what was expected, specifically]
```
If any criterion fails, identify which slice introduced the gap. Return that slice to In Build with a specific note. The deliverable is not accepted until all criteria pass.

**Logic deliverable:**
Evidence-based verification:
- Run the affected test suite and confirm all tests pass
- Verify data state matches expected output
- Walk through affected screens to confirm the logic surfaces correctly
- Document each criterion with named evidence in the same format above

**Integration deliverable — UX impact check:**
For Logic deliverables where any slice's data anchor points to a real API or database (not the mock layer), run this check before presenting the acceptance prompt.

Review the running experience with live data against the original Screen deliverable's design. Ask:
> "Does live data produce anything a user would see or interact with that the design didn't account for — field values at scale, list behavior, empty or error state appearance, pagination controls, loading states?"

- **No:** Continue to the acceptance prompt.
- **Yes:** Do not present the acceptance prompt. Surface the gap with specific evidence:

> "Live data reveals a UX gap in [Screen]: [what the design assumed] vs. [what real data produces]. Flagging for design review before accepting this deliverable."

Flag for design review with the specific evidence. Move affected Screen deliverable slices back to In Review. The integration deliverable acceptance waits until design review completes and the affected UI slices are rebuilt and re-verified.

### Step 3 — Deliverable Acceptance Prompt

When all criteria are verified, present the solo with a clear acceptance prompt — distinct from a slice sign-off:

---
> **Deliverable [D-ID] — [Name] — ready for acceptance** *(Screen | Logic)*
>
> All [N] slices are In Test. Here's what was delivered:
> [solo description]
>
> Acceptance criteria — all verified:
> 1. [criterion 1] ✅
> 2. [criterion 2] ✅
> 3. [criterion 3] ✅
>
> *[Screen deliverable: Running at [URL] — open it and confirm the full experience.]*
> *[Logic deliverable: Evidence: [brief summary of evidence — test results, data state, affected screens verified].]*
>
> Does this deliverable meet the contract? Accept to proceed.

---

Wait for the solo's response. Do not advance to the next deliverable until they accept.

**Solo responses:**

| Response | Action |
|----------|--------|
| "Yes / Accepted / Looks right" | Record acceptance, check for phase gate |
| "Almost — [specific gap]" | Identify which criterion failed, which slice owns it, return to In Build |
| "No — [issue]" | Triage: is this a build issue (return to In Build) or a design issue (flag for design review) |

### Step 4 — Record Acceptance

When the solo accepts:
1. Update backlog: deliverable status → `Accepted`
2. Add acceptance record: `"Accepted [date]. Criteria verified. Solo sign-off confirmed."`
3. Check if all deliverables in the phase are now Accepted — if so, surface the phase gate:
> "All deliverables in this phase are accepted. Phase gate: all slices In Test, all deliverables accepted. Ready for Phase Test when you are."

---

## When Testing Surfaces Something Unexpected

Not everything that surfaces during QA is a clean pass or a simple build fix. Three types of unexpected discovery need their own paths:

- **Bug** — behavior is defined, implementation doesn't match it
- **Missing requirement** — behavior was never defined; nobody specified what should happen here
- **Regression** — something previously Done and working is now broken

When any of these surface — during AI verification or solo sign-off — invoke `qa-triage` immediately. Do not improvise a fix without classifying what was found first. Treating a missing requirement as a bug produces code that solves the wrong problem. Patching a regression without finding the root cause brings it back in the next slice.

`qa-triage` classifies the discovery, determines its scope, routes it to the correct path, and logs the decision. It is designed to be fast — small-scope discoveries get resolved and QA continues. Flow-level issues get routed to design review without stalling everything else.

**The one rule before invoking triage:** do not let the solo sign off on a slice that has an open missing requirement. Undefined behavior that ships with a sign-off becomes assumed behavior. Define it or explicitly defer it to a new slice before the sign-off prompt goes out.

---

## The Done Definition — In Full

A slice moves through four confirmed states before reaching Done:

| Check | Who | Status after |
|-------|-----|------|
| Code quality | `code-review-and-quality` | — (still In QA) |
| Gate confirmation | `solo-qa` | — (begins Part 1) |
| Done criteria | AI (solo-qa Part 1) | — (still In QA) |
| Design fidelity | AI (solo-qa Part 1) | — (still In QA) |
| Visual confirmation | Solo (Part 2) | — |
| Behavior confirmation | Solo (Part 2) | — |
| Criteria confirmation | Solo (Part 2) | **In Test** |
| Phase-level verification | `phase-test` | **Done** |

All required. In order. The slice reaches `In Test` when solo signs off. It reaches `Done` when phase-test confirms the full phase works end-to-end. Solo sign-off is the slice gate and cannot be skipped or substituted. Phase-test is the phase gate and cannot be skipped or substituted.

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Starting Part 1 without gate confirmation | Code review may not have run | Check backlog for logged confirmation first |
| Verifying criteria by reading code | Code inspection ≠ active verification | Open the preview, look at running output |
| "The code reads from mock data" as evidence | That's code review, not QA | Cross-reference rendered values against the mock file |
| Marking Done without solo sign-off | The solo's eye is the final gate | Always wait — never skip |
| Solo confirming from memory ("I looked at it earlier") | Solo needs to see it running at this moment | Open the browser, look at it live, then confirm |
| Vague solo confirmation ("seems fine") | Not a real sign-off | Walk through each done criterion explicitly |
| Returning to In Build without specific notes | Builder doesn't know what to fix | Always include exact issue and what the fix needs to achieve |
| Fixing design issues inside QA | Wrong phase for that work | Surface it, flag for design review |
