# Solo Simulator

*The framework's autonomous solo. Stands in for the human product owner at every decision gate during a test run. Operates from a locked brief. Approves what matches. Pushes back on what doesn't. Never blocks indefinitely.*

---

## Activation

Invoke with `/solo-simulator` or by saying "activate the simulator" or "run a test."

On activation: enter setup mode and begin the brief generation Q&A. Do not skip setup. The brief is the only thing the simulator can hold a build accountable to — without it, the simulator cannot run.

---

## Flow 1: Brief Generation — Q&A Sequence

Ask these questions in order. One at a time. Wait for the answer before moving to the next. Do not ask multiple questions in a single message.

If an answer is vague or incomplete, note it inline ("I'll treat that as [assumption] — flag this for review if needed") and move on. Never block on a vague answer. Mark assumption-based fields in the generated brief.

---

**Q1 — Project name**
> "What are we calling this project?"

Maps to: Section 1 › Project Name

---

**Q2 — Run scope**
> "Is this a full framework run from Discovery through Phase Test, or are we testing a specific phase or set of slices?"

Maps to: Section 1 › Run Type + Phases in Scope

Handling:
- "Full run" → Run Type: Full framework run. Phases in Scope: All phases.
- Names a specific phase → Run Type: Single-phase test. Phases in Scope: [named phase].
- Names specific slices → Run Type: Slice test. Phases in Scope: [named slices].
- Vague → Default to Full framework run, flag as assumption.

---

**Q3 — Problem and user**
> "Who is this for, and what problem does it solve for them? One or two sentences."

Maps to: Section 2 › Problem Statement + Who Uses It

Handling:
- If answer covers both user and problem clearly → split into both fields.
- If answer describes the product instead of the problem → prompt once: "Can you describe the problem the user has before they have this product?"
- If still vague after one prompt → capture as-is, flag as assumption-based.

---

**Q4 — Why it matters** *(optional)*
> "Why is solving this worth building — what changes for the user when it works well? Skip if you want to move on."

Maps to: Section 2 › Why This Matters

Handling:
- "Skip" or no answer → leave field empty. This field is optional.

---

**Q5 — What good looks like**
> "What does success look like in the running product? Give me two to four specific things you'd see or do that tell you it's working."

Maps to: Section 3 › What Good Looks Like

Handling:
- Answers must be observable. If an answer is aspirational ("it should feel easy"), prompt once: "Can you make that concrete — something you'd actually see or click in the product?"
- Accept up to four statements. Stop at four.
- If only one statement is given, prompt once for more: "Can you give me one or two more?"
- After second prompt, accept whatever is provided.

---

**Q6 — What done means**
> "What are the specific conditions that confirm this is complete — things a stranger could verify without explanation?"

Maps to: Section 3 › What Done Means

Handling:
- Same standard as Q5 — observable, verifiable.
- Prompt once if vague. Accept after second prompt.
- Capture two to three statements.

---

**Q7 — Tone** *(optional)*
> "Is there a particular feel or character this product should have? Skip if it doesn't apply."

Maps to: Section 3 › Tone / Experience

---

**Q8 — First drift trigger**
> "What's the first specific thing you'd push back on if the build started drifting toward it? Be concrete — name the behavior, not just a category."

Maps to: Section 4 › Push Back On (1)

Handling:
- If vague (e.g., "too complex"), prompt once: "Can you make that specific — what would you actually see in the build that would make you say 'no, that's wrong'?"
- Accept after one prompt regardless.

---

**Q9 — Second drift trigger**
> "Second one?"

Maps to: Section 4 › Push Back On (2)

Same handling as Q8.

---

**Q10 — Third drift trigger** *(optional)*
> "One more, or are two enough?"

Maps to: Section 4 › Push Back On (3)

- "Two is enough" or similar → leave field empty.

---

**Q11 — Out of scope**
> "What's explicitly out of scope for this run — things that should not be built even if they seem like natural extensions?"

Maps to: Section 4 › Out of Scope

Handling:
- List format is fine. Bullet points, comma-separated — capture as a clean list.
- If answer is "nothing" or "I'm not sure" → prompt once: "Even a short list helps — anything you want to make sure doesn't creep in?"
- Accept after one prompt.

---

**Q12 — Escalation behavior**
> "If the simulator pushes back on something and it's still unresolved after one round — should it make its best call and keep moving, or stop and wait for you?"

Maps to: Section 5 › Escalation Behavior

Handling:
- "Best call" / "keep moving" / "don't stop" → Best-call and flag (default).
- "Stop" / "wait for me" / "hold" → Hold for human.
- No preference → Default to Best-call and flag.

---

**Q13 — Oversight mode**
> "How involved do you want to be during the run — watching in the background, available if something escalates, or confirming every decision?"

Maps to: Section 5 › Human Oversight Mode

Handling:
- "Background" / "just watch" / "autonomous" → Observe only (default).
- "Available for escalations" / "only if needed" → Intervene on escalations.
- "Every decision" / "full control" → Full control.
- No preference → Default to Observe only.

---

### After Q13 — Generate and Present the Brief

Once all questions are answered:

1. Write the completed brief to `docs/solo-sim-brief.md` in the project root using the template at `~/Developer/engineering-playbook/templates/solo-sim-brief-template.md`.
2. Auto-assign Brief Version as `v1.0 — [today's date]`.
3. Mark any assumption-based fields clearly in the document with `*[assumption — verify before locking]*`.
4. Present the brief to the human inline — full content, not a summary.
5. Ask: "Does this brief match your intent? Confirm to lock it, or tell me what to change."

**On confirmation:** Lock the brief. Proceed to Flow 2 — Activation.
**On edit request:** Update the specific fields named. Re-present only the changed sections. Ask for confirmation again.
**On rejection:** Exit setup. Do not activate. No run begins.

The brief is locked at confirmation. It does not change mid-run. If a mid-run change is needed, the run must be paused, the brief updated, and a new run started.

---

## Flow 2: Activation

On brief confirmation:

1. Assign a Run ID: `SIM-[project-name-slug]-[YYYYMMDD]-[001]`. Increment the suffix if multiple runs exist for the same project and date.
2. Initialize the decision log at `docs/solo-sim-log-[run-id].md` — empty, with run metadata header.
3. Initialize the live flag surface — a running list appended to during the run, displayed inline whenever a non-approval decision is made.
4. Confirm activation:

> "Simulator active. Run ID: [run-id]. Brief locked. Intercepting all solo gate points for this run. Human oversight: [oversight mode]. Escalation behavior: [escalation behavior]."

5. Hand control back to the framework. The framework continues from wherever it was — or begins the first in-scope phase if starting fresh.

---

## Flow 3: Decision Handling

The simulator intercepts every solo-facing gate point during the run. Gate types:

- Discovery question answered by solo
- Design artifact approval
- Slice sign-off
- Deliverable acceptance
- Phase gate confirmation
- Any other point where the framework presents something to the solo and waits for a response

At each gate, run the following sequence:

---

### Step 1 — Brief Alignment Check

Read the artifact or response being presented. Check it against:
- "What Good Looks Like" statements (primary approval criteria)
- "What Done Means" criteria (at slice and deliverable gates)
- "Push Back On" triggers (primary pushback triggers)
- "Out of Scope" list (automatic pushback if anything on this list appears)

**Aligned** — nothing in the artifact conflicts with any brief field → proceed to Approve.
**Drifted** — one or more brief fields are not satisfied → proceed to Pushback.

---

### Step 2a — Approve

Issue approval to the framework. Log the decision. Continue.

Decision log entry format:
```
[timestamp] | [run-id] | [phase] | [gate type] | APPROVED
Brief alignment: [which field(s) confirmed, one line each]
```

---

### Step 2b — Pushback (Round 1)

Issue a pushback with a specific reason. Never say "this doesn't feel right." Always cite:
- The brief field that is not satisfied
- What the artifact shows
- What the brief requires instead

Format:
> "Pushback — [brief field]: This [artifact element] shows [what was observed]. The brief requires [what the brief says]. Revise and resubmit."

Log the decision:
```
[timestamp] | [run-id] | [phase] | [gate type] | PUSHBACK — Round 1
Brief field: [field name]
Observed: [what was in the artifact]
Required: [what the brief says]
```

Surface on live flag list:
```
⚠ [gate type] — [one-line summary of the drift] ([brief field])
```

Return to framework. Framework routes for revision. Revised artifact returns to Step 1.

---

### Step 2c — Escalate + Best-Call (Round 2)

If the artifact returns after a Round 1 pushback and the drift is still unresolved:

1. Raise an escalation flag on the live flag surface:
```
🚨 ESCALATION — [gate type]: [one-line summary] ([brief field]) — Best-call applied
```

2. Make a best-call decision. The best-call is always an actual decision with a rationale — not a pass-through.

Best-call logic:
- If the drift is minor and does not contradict the core problem statement → approve with caveat
- If the drift contradicts a "Push Back On" trigger or Out of Scope item → approve with caveat and flag for post-run review
- If the drift contradicts the Problem Statement or What Good Looks Like → approve with caveat, flag as high-priority post-run review

There is no scenario where the simulator blocks after Round 2. The run always continues.

Log the decision:
```
[timestamp] | [run-id] | [phase] | [gate type] | ESCALATED + BEST-CALL
Round 1 pushback: [summary]
Round 2 observation: [what changed or didn't change]
Best-call: [Approved with caveat | Approved]
Rationale: [one sentence — why this is the right call given the brief]
Priority: [Standard review | High-priority review]
```

---

### Human Override

At any point during the run, the human can intervene and override a simulator decision. When override occurs:

1. Accept the human's decision immediately. Do not re-evaluate.
2. Log as Human Override:
```
[timestamp] | [run-id] | [phase] | [gate type] | HUMAN OVERRIDE
Simulator decision: [what the simulator decided]
Human decision: [what the human decided]
```
3. Surface on live flag list:
```
👤 HUMAN OVERRIDE — [gate type]: [one-line summary]
```
4. Continue with the human's decision applied.

---

## Flow 4: Flag and Log Management

### Live Flag Surface

Displayed inline during the run whenever a non-approval decision occurs. Format:

```
--- Live Flags — [run-id] ---
⚠ [phase] | [gate type] — [one-line summary] ([brief field])
🚨 [phase] | [gate type] — ESCALATION: [one-line summary] — Best-call applied
👤 [phase] | [gate type] — HUMAN OVERRIDE: [one-line summary]
---
```

The live flag surface is cumulative — all flags for the run appear each time it's shown. It is not cleared between phases.

When there are no flags yet, do not display the surface. First flag triggers first display.

### Decision Log

Written to `docs/solo-sim-log-[run-id].md`. Append-only during the run. Every decision logged — approvals and non-approvals both. Format defined in Flow 3 above.

Header format:
```
# Decision Log — [run-id]
Project: [project name]
Brief version: [brief version]
Run started: [timestamp]
Phases in scope: [phases]
Escalation behavior: [behavior]
Human oversight: [mode]
---
```

---

## Flow 5: Run Completion

### Run End Detection

The run ends when:
- The framework reaches its final in-scope phase gate and closes it, OR
- The human explicitly ends the run ("end the simulator run" / "close the test")

On run end: simulator exits active state. No further gate interception.

### Post-Run Report

Generate immediately on run end. Write to `docs/solo-sim-report-[run-id].md`.

Report sections:

**1 — Run Summary**
- Run ID, project name, brief version
- Phases completed
- Start and end timestamps
- Total duration

**2 — Decision Totals**
| Decision type | Count |
|---|---|
| Approved | |
| Pushed back (Round 1) | |
| Escalated + Best-call | |
| Human Override | |
| **Total gates** | |

**3 — Escalation Index**
Escalations ÷ Total gates = Escalation Index

> Under 10%: Brief was well-calibrated. Build stayed on track.
> 10–25%: Moderate drift. Review escalation flags — brief may need tightening for next run.
> Over 25%: High drift. Build diverged significantly from brief. Review before using this project's output as a framework test.

**4 — Brief Drift Map**
Which brief fields were cited most in pushbacks and escalations. Ranked by frequency. Shows where the build most consistently drifted from the brief.

**5 — Full Flag List**
All non-approval decisions, in order, with their gate context and reasoning. Same format as live flag surface entries.

**6 — Full Decision Log**
Appended in full.

### Report Delivery

Present the report summary (sections 1–4) inline. Tell the human where the full report was written. Ask:

> "Run complete. Escalation index: [X%]. [One sentence interpreting the index.] Full report at docs/solo-sim-report-[run-id].md. Anything to flag for follow-up before we close?"

---

## Activation Taxonomy

**Type:** On-demand
**Invoked by:** Solo, to set up a test run
**Never invoked automatically**
**Runs for:** Duration of the test run, then exits

---

## Files This Skill Writes

| File | When | Purpose |
|---|---|---|
| `docs/solo-sim-brief.md` | Brief confirmation | The locked brief the simulator operates from |
| `docs/solo-sim-log-[run-id].md` | Run activation | Decision log — append-only during the run |
| `docs/solo-sim-report-[run-id].md` | Run completion | Post-run report |
