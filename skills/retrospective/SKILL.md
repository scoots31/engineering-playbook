---
name: retrospective
description: Continuous learning mechanism for the Solo Builder Framework. Two modes — flag mode captures observations in the moment as lightweight notes (via product-continuity), retro mode processes those notes at defined moments to identify patterns, root causes, and proposed improvements. Distinguishes project-level adjustments from framework-level improvements to the playbook itself. Activates automatically at phase end and after phase test when guided or piloted mode is active. Directly invokable in any mode — including bare — via /retrospective or /retro.
---

# Retrospective

*The framework gets better from being used. This is how.*

**Core question:** "What did we learn — and what specifically should change as a result?"

This skill has two activation paths: automatic (fires at phase end and after phase test when guided or piloted mode is active) and direct invocation (/retrospective or /retro, available in any mode including bare).

This skill has two modes that work together. Flag mode captures observations in the moment without interrupting flow. Retro mode processes those observations at natural pause points — finding patterns, naming root causes, proposing specific improvements, and closing the loop back to the playbook.

---

## Mode 1 — Flag Mode (in the moment)

**Who does this:** product-continuity, as part of its normal session capture.

When anything surfaces during a session that's worth examining — a skill that didn't behave as expected, a step that was harder than it should have been, something that worked better than designed, a gap the framework didn't catch — product-continuity appends a lightweight note to `docs/continuity/retro-notes.md`.

**Format — one line per observation:**
```
[date] [phase] [observation — one sentence, plain English]
```

**Examples:**
```
2026-04-20  Design Review  Process map cross-reference wasn't prompted — had to be done manually
2026-04-20  Solo Build     Four anchors check caught a missing data anchor before build started — worked exactly as designed
2026-04-21  Solo QA        Solo sign-off prompt didn't include the design file path — solo had to find it manually
2026-04-21  Code Review    Stack compliance check referenced wrong tech-context section for RTK Query patterns
```

No analysis. No proposed fix. Just the observation while it's fresh. The retro processes it later.

**Positive observations are captured too.** Something that worked better than expected is as valuable as something that didn't. It should be reinforced, not accidentally removed in a future update.

---

## Mode 2 — Retro Mode (specific moments)

**Trigger points:**
- End of each phase — automatically, before moving to the next
- After phase test — the most revealing moment in the framework
- Explicit invocation — `/retrospective` or `/retro` when something significant needs immediate attention

**Token discipline:** retro mode reads only `docs/continuity/retro-notes.md` — the flagged observations. Not full document reads. Only goes deeper into other documents if a specific note needs clarification.

---

### Step 1 — Read the Flagged Notes

Open `docs/continuity/retro-notes.md`. Read all unprocessed entries (entries since the last retro run, marked with a `—` separator after each retro).

Count the observations. If there are none: silent. No retro output needed. Continue.

---

### Step 2 — Pattern vs One-Off

Group the observations:

**Pattern** — the same issue appears more than once, or the same phase/skill is flagged multiple times. Patterns are framework signals — something in the design of a skill isn't working.

**One-off** — a single incident in a specific context. May be worth noting, but isn't necessarily a framework problem.

**Positive** — something that worked better than expected. Note it separately.

Patterns get full retrospective treatment. One-offs get a brief note. Positives get a reinforcement note.

---

### Step 3 — For Each Pattern, Produce a Retrospective Entry

```markdown
## [Pattern title] — [YYYY-MM-DD]
**Observed:** [N] times across [phases/sessions]
**Level:** Project / Framework

### What happened
[2–3 sentences. What was observed, in plain English. No jargon.]

### Root cause
[Why this happened. Not what happened — why. What in the framework design 
produced this outcome?]

### Impact
[What this cost — time, quality, a missed step, a misunderstanding.]

### Proposed fix
[The specific change that would prevent this. For framework-level issues: 
the exact sentence or section in the SKILL.md that should change, and what 
it should say instead. For project-level issues: the adjustment to how 
this project uses the framework.]

### Decision
- [ ] Update the skill now → [which skill, what changes]
- [ ] Queue for next framework review → [added to framework improvement log]
- [ ] Project adjustment only → [what changes for this project, not the playbook]
```

---

### Step 4 — For Positive Observations

```markdown
## [What worked] — [YYYY-MM-DD]
**Observed:** [N] times / [context]

### What happened
[What worked better than designed or expected.]

### Why it worked
[What in the framework design produced this good outcome.]

### Reinforce
[What should be made more explicit or prominent in the skill so it doesn't 
get accidentally weakened in future updates.]
```

---

### Step 5 — Framework-Level vs Project-Level

Every retrospective entry gets classified:

**Project-level** — this is a adjustment for how this project is running. The skill is fine; the project's specific context needs a different approach. Update `docs/continuity/retrospective.md` only.

**Framework-level** — the skill itself needs to change. The design of the SKILL.md produced a bad outcome. Requires a decision: update now or queue.

**Update now** — if the fix is clear, small, and unambiguous. Make the change to the SKILL.md immediately. Log it in the retrospective entry.

**Queue** — if the fix needs more thought, affects multiple skills, or requires a larger design discussion. Add to `docs/continuity/framework-improvements.md` with enough specificity to act on later.

---

### Step 6 — Archive and Clear

After retro mode completes:

1. Append a separator to `docs/continuity/retro-notes.md`:
   ```
   --- Processed [YYYY-MM-DD] ---
   ```
   Notes above the separator are archived. New observations continue below.

2. Save the structured retrospective entries to `docs/continuity/retrospective.md`.

3. Save any queued framework improvements to `docs/continuity/framework-improvements.md`.

---

## Output Documents

| Document | Contents |
|----------|----------|
| `docs/continuity/retro-notes.md` | Raw flagged observations — one line each, captured in the moment |
| `docs/continuity/retrospective.md` | Processed retrospective entries — patterns, root causes, proposed fixes |
| `docs/continuity/framework-improvements.md` | Queued framework-level improvements — specific enough to act on |

---

## The Feedback Loop

Framework-level improvements that are queued need to eventually make it back into the playbook. `docs/continuity/framework-improvements.md` is the holding place. At the start of a new project — or explicitly when the solo wants to improve the playbook — these queued improvements get reviewed and applied to the relevant SKILL.md files.

This is how the framework evolves. Not through abstract planning, but through real usage revealing what needs to change.

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Full retro after every incident | Interrupts flow, token expensive | Flag in the moment, process at phase end |
| Observations without proposed fixes | Complaints without action | Always end with a specific proposed change |
| Treating all observations as framework problems | Some things are project-specific | Distinguish project-level from framework-level explicitly |
| Skipping positive observations | Framework learns only from failure | Capture what works — reinforce it |
| Queuing improvements without enough specificity | Can't act on "this section needs work" | Queue with the exact change proposed — which skill, what sentence, what it should say |
| Never applying queued improvements | The queue grows, the framework stays v1 | Review framework-improvements.md at the start of each new project |
