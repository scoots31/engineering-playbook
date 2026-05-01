---
name: retrospective
description: Continuous learning mechanism for the Solo Builder Framework. Session-present in guided and piloted mode — actively listens throughout the session for framework signals, solo-expressed dissatisfaction, and explicit flags. Captures observations to .claude/retro-notes.tmp (pushed to shared/retro-log.md at session end) and docs/continuity/retro-notes.md (per-project persistence). Processes observations at phase end to identify patterns, root causes, and improvements. Distinguishes project-level adjustments from framework-level improvements.
---

# Retrospective

*The framework gets better from being used. This is how.*

**Core question:** "What did we learn — and what specifically should change as a result?"

This skill has two modes that work together. **Listening mode** is always active during guided and piloted sessions — capturing observations in the moment without interrupting flow. **Retro mode** processes those observations at phase end — finding patterns, naming root causes, proposing specific improvements, and closing the loop back to the playbook.

---

## Listening Mode — Always Active in Guided and Piloted Sessions

The retrospective is present throughout every session in guided or piloted mode. It is not waiting to be invoked — it is listening. When a capture-worthy moment occurs, it writes the observation immediately and continues. No interruption to the flow of work.

**Where captures go:**
- `.claude/retro-notes.tmp` — session buffer, pushed to `shared/retro-log.md` at session end via Stop hook, then cleared. This is what reaches the framework curator across all machines.
- `docs/continuity/retro-notes.md` — per-project persistent store, read by retro mode at phase end.

Both files receive every capture.

---

### What triggers a capture

**Framework-detected signals**
The framework itself produced a notable outcome — something worth examining:
- Stuck protocol fired (two failed attempts on the same problem)
- Code review returned a fail — especially if the same check failed twice
- Builder stated a file was read, then produced output inconsistent with it (self-correction)
- Solo-qa caught something that self-verification missed
- Builder deviated from priority order without explicit solo direction
- A slice rolled back after passing QA

When any of these occur: capture immediately. No solo prompt needed.

**Solo-expressed dissatisfaction or confusion**
The solo said something that signals the output wasn't what they expected:
- "Why did that happen?"
- "That's not what I expected"
- "Why is it doing this?"
- "That took way longer than it should have"
- "That doesn't feel right"
- "I thought we already handled this"
- Any expression of frustration at a framework output, not just a specific bug

When any of these surface: acknowledge briefly, capture, continue.
> "Noted — flagging that."

Do not resolve and move on silently. The observation is as important as the fix.

**Explicit flags**
The solo directly asks to capture something:
- "Note this"
- "Flag this"
- "Add this to the retro"
- "I want to come back to this"
- "Remember this for later"

Capture immediately and confirm:
> "Flagged: [one sentence summary of what was captured]."

---

### Capture format

One line per observation, appended to both files:

```
YYYY-MM-DD | [git user name] | [project name] | [phase] | [trigger-type] | [observation]
```

**Trigger types:** `framework-detected` · `solo-expressed` · `explicit-flag`

**Examples:**
```
2026-05-01 | Scott Heinemeier | ctl-product | Build | framework-detected | Code review failed twice on SL-014 — same data sourcing check both times
2026-05-01 | Scott Heinemeier | ctl-product | Build | solo-expressed | "why is it doing this" — builder loaded wrong mock file after anchor confirmation
2026-05-01 | Scott Heinemeier | ctl-product | Build | explicit-flag | Mock data structure won't match API shape — full reshape needed when real data arrives
2026-05-01 | Scott Heinemeier | ctl-product | Design Review | framework-detected | Four anchors check caught missing process anchor before build started — worked as designed
```

Positive observations are captured too. Something that worked better than expected is as valuable as something that didn't.

**Get the project name** from `docs/continuity/handoff.md` or the project directory name.

**How to write the capture:**
```
/bin/zsh -c 'echo "$(date +%Y-%m-%d) | $(git config user.name) | [project] | [phase] | [trigger-type] | [observation]" >> .claude/retro-notes.tmp'
```
And the same line appended to `docs/continuity/retro-notes.md`.

---

### Session-end surface

Before product-continuity closes the session, surface what was captured:

If nothing was captured: silent. No retro output needed.

If observations exist:
> "Retro — [N] observation(s) this session:
>   [framework] [one-line summary]
>   [solo] [one-line summary]
>   [flag] [one-line summary]
>
> Any of these need more thought before we close?"

Wait for the answer. If yes: go to retro mode on the flagged items immediately. If no: close. The Stop hook pushes `.claude/retro-notes.tmp` to `shared/retro-log.md` automatically — no manual step needed.

---

## Retro Mode — Phase End Processing

**Trigger points:**
- End of each phase — automatically, before moving to the next
- After phase test — the most revealing moment in the framework
- Explicit invocation — `/retrospective` or `/retro`

**Token discipline:** reads only `docs/continuity/retro-notes.md` and any current `.claude/retro-notes.tmp`. Not full document reads.

---

### Step 1 — Read the Flagged Notes

Open `docs/continuity/retro-notes.md`. Read all unprocessed entries (entries since the last retro run, marked with a `—` separator). Also check `.claude/retro-notes.tmp` for observations captured this session that haven't yet been processed.

If there are none: silent. No retro output needed. Continue.

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

**Project-level** — an adjustment for how this project is running. The skill is fine; the project's specific context needs a different approach. Update `docs/continuity/retrospective.md` only.

**Framework-level** — the skill itself needs to change. Requires a decision: update now or queue.

**Update now** — if the fix is clear, small, and unambiguous. Make the change to the SKILL.md immediately. Log it in the retrospective entry.

**Queue** — if the fix needs more thought, affects multiple skills, or requires a larger design discussion. Add to `docs/continuity/framework-improvements.md` with enough specificity to act on later.

---

### Step 6 — Archive and Clear

After retro mode completes:

1. Append a separator to `docs/continuity/retro-notes.md`:
   ```
   --- Processed [YYYY-MM-DD] ---
   ```

2. Save structured retrospective entries to `docs/continuity/retrospective.md`.

3. Save queued framework improvements to `docs/continuity/framework-improvements.md`.

---

## Output Documents

| Document | Contents |
|----------|----------|
| `.claude/retro-notes.tmp` | Session buffer — pushed to shared/retro-log.md at session end, then cleared |
| `docs/continuity/retro-notes.md` | Per-project persistent observations — one line each |
| `docs/continuity/retrospective.md` | Processed retrospective entries — patterns, root causes, proposed fixes |
| `docs/continuity/framework-improvements.md` | Queued framework-level improvements — specific enough to act on |

`shared/retro-log.md` in the engineering-playbook repo is the cross-project, cross-machine view. Written by the Stop hook. Read only by the framework curator.

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Resolving a solo dissatisfaction signal without capturing it | The moment is gone — the pattern never forms | Capture first, then resolve. "Noted — flagging that." is one second. |
| Full retro analysis in the moment | Interrupts flow, token expensive | Capture the raw observation now, process at phase end |
| Observations without proposed fixes | Complaints without action | Always end retro mode entries with a specific proposed change |
| Treating all observations as framework problems | Some things are project-specific | Distinguish project-level from framework-level explicitly |
| Skipping positive observations | Framework learns only from failure | Capture what works — reinforce it |
| Queuing improvements without enough specificity | Can't act on "this section needs work" | Queue with the exact change proposed — which skill, what sentence, what it should say |
| Silent session-end when observations exist | Solo closes without knowing what was captured | Surface the session-end summary — let the solo decide if anything needs more thought |
