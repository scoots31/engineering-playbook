---
name: framework-health
description: Background health monitor for the Solo Builder Framework. Always-on in guided and piloted mode — silent in bare mode (the default). Never sits in the critical path. Activates at mode selection, between phases, and session end. Checks signals — file existence and the handoff + backlog At a Glance section — not full document reads. Only goes deeper when a signal is wrong. Surfaces one issue at a time with a specific recovery path. Never blocks progress.
---

# Framework Health

*Runs in the background. Surfaces problems. Never blocks.*

**Core question:** "Is the framework running as designed — and if something is missing, what's the recovery path?"

This skill is a health monitor, not a gatekeeper. Everything in the framework continues at full speed when things are healthy. The health monitor only speaks when something is wrong or missing — and when it does, it's specific, it offers the recovery path, and it steps back.

It does not read every document. It checks signals.

---

## Token Discipline — Signals First, Documents Only on Exception

**Primary inputs (always):**
- `docs/continuity/handoff.md` — current phase, what's open, where to pick up. One page by design.
- Backlog At a Glance section only — slice counts by status. Not individual slice records.

**Secondary inputs (only when a signal is wrong):**
- The specific document relevant to the gap — not all documents, the one document.

**File existence checks (no read required):**
These confirm expected outputs exist without reading their contents.

| Phase complete | Expected files |
|---------------|---------------|
| Discover | `docs/discovery-brief.md` · `docs/process/as-is-*.md` · `docs/process/to-be-*.md` |
| Tech context | `docs/tech-context.md` |
| Design sprint | `docs/design/sprint-*.html` · `docs/design/deferred-decisions.md` |
| Design review | `docs/backlog.md` with Ready slices |
| Data scaffold | `data/mock/` · `docs/data-mapping.md` |
| Phase test | `docs/phase-test-*.md` · phase completion record in backlog |

A missing file is a signal. Read it only if the signal needs clarification.

---

## When It Activates

### Mode Activation (replaces session start)

When guided or piloted mode activates, run these checks in order:

**1. Framework version check — runs first, before reading any project documents.**

Resolve the playbook root from User Rules / CLAUDE.md (the path configured during setup — never hardcode it). Then run:

```
git -C <PLAYBOOK_ROOT> fetch origin --quiet
git -C <PLAYBOOK_ROOT> rev-list HEAD..origin/main --count
```

If count > 0:
> "Framework update available — [N] new commit(s) on origin/main. Pull latest before we start? (`git -C <PLAYBOOK_ROOT> pull`)"

Wait for yes or no. If yes: pull, confirm success, continue. If no: log "framework update deferred" to the session handoff and continue. Do not raise it again this session.

If count = 0: silent. Continue.

**2. Read project state.** Read `docs/continuity/handoff.md`. Read the backlog At a Glance section. Run existence checks for the current phase.

If everything is in order: orient the session from the handoff and continue. No output needed — health is silent when healthy.

If something is out of sync: surface it before new work begins.

> "Before we start — the design sprint screens exist but the deferred decisions log is missing. That's needed before design review can run. Should we produce it now, or was this intentional?"

One issue. Specific. Recovery path offered. Then step back.

**3. Long-gap check.** The handoff date parsed in Step 2 is compared to today. If the gap is 21 or more days, surface this before any other orientation:

> "Last session was [N] days ago. Before we pick up new work, a re-entry check is worth running — codebase state, environment, and whether the open decisions still hold. Run the re-entry check now, or skip straight to [next action from handoff]?"

If yes: product-continuity runs the long-gap re-entry protocol. No new work starts until the check completes or the solo explicitly skips it.

If no: orient from the handoff as normal. Log "long-gap re-entry skipped" to the session handoff.

If the gap is fewer than 21 days: silent. Continue.

---

### Between Phases

When one phase completes and the next is about to begin, run the existence check for the completed phase.

If expected outputs are all present: silent. Continue.

If something is missing:

> "Moving from design sprint to design review — the to-be process map hasn't been annotated with screen references yet. The process mapper handles this step. Should we do that cross-reference before starting design review?"

The solo can say yes or "skip it for now." If skipped, log it as an open item in the session handoff. Don't repeat it unless it becomes blocking.

**Phase gates are also natural session boundaries.** The gate output — discovery brief, design files, backlog — is what the next phase reads, not conversation history. A fresh session that reads that output starts with full context and zero overhead. When a gate passes, fire the gate confirmation immediately — before any transition work begins:

> "**[Phase name] complete.** Outputs: [file 1] · [file 2]. Gate cleared.
> Start [next phase] now, or close out here?"

Wait for the answer. Do not assume. If continuing: load the next phase. If closing: hand off to product-continuity.

Format rules:
- Name the phase that just completed, not the one coming next
- List the specific files produced — not categories, actual filenames
- One question, two options, nothing else

**When there's a genuine two-path fork** (e.g. design review complete → either prd-to-plan or solo-build depending on state), name both paths explicitly in one sentence each, then ask which:

> "**Design review complete.** Outputs: backlog.md. Gate cleared.
> Two paths: plan out the build sequence from the backlog, or start building SL-001 directly. Which?"

Same discipline — no suggestions, no hedging, no filler. One sentence per option, one question.

---

### During the Session — Session Hygiene Reminder

Once per session, at a natural pause — after a gate passes, after a slice ships, after a significant decision lands — surface:

> "Good pause point. Whenever you're ready to close out, just let me know — I'll wrap up properly and give you a prompt to pick up next session without losing anything."

Fire once only. If the solo isn't ready, they say so and the reminder doesn't repeat. This is ambient awareness, not urgency. Do not fire mid-task or while a slice is actively in progress.

---

### Within a Phase — Milestone Lines

At meaningful completions within a phase, surface a single line of location context. Not every message — only when a real milestone lands:

- A zone completes in discover
- Hero screen approved in design sprint
- All screens approved and walk-through complete
- A slice ships in build
- A phase test gate opens

Format: `[Phase] — [what just completed]. [What's next or remaining.]`

Examples:
> "Design sprint — hero approved. 3 screens remaining."
> "Discover — zones 1–3 complete. On-ramp question next."
> "Build — SL-004 done. 2 slices remaining in Phase 1."

One line. No explanation. Silent if nothing meaningful just completed.

---

### Session End

Check three things only:

1. **Handoff current?** — Was `docs/continuity/handoff.md` updated this session? If not, prompt product-continuity to update it before closing.

2. **Backlog accurate?** — Do the At a Glance counts reflect what actually happened this session? If a slice moved to Done but the count wasn't updated, flag it.

3. **Open qa-triage items?** — Are there unresolved triage items from this session? Name them so the next session doesn't start blind.

> "Before we close — 2 qa-triage items from today are still open: [SL-004 missing requirement] and [SL-006 regression root cause]. Adding to the handoff so next session picks them up."

---

## What It Watches

**Framework version currency**
At mode activation, checks whether the local engineering-playbook is behind `origin/main`. Surfaces once if an update is available — with the pull command ready to run. Never repeats after the solo acknowledges it.

**Long-gap detection**
At mode activation, the date in handoff.md is compared to today. A gap of 21+ days triggers a re-entry recommendation before the session begins. Silent for shorter gaps. Never repeats after acknowledged.

**Phase gate integrity**
Expected outputs present before the next phase runs. Checks by file existence — not by reading the files.

**Skill chain integrity**
The automatic chain (solo-build → code-review-and-quality → solo-qa) should complete without gaps. The signal is the code review confirmation logged in the backlog slice detail. If a slice is In QA without that confirmation logged, surface it.

> "SL-007 is showing In QA but there's no code review confirmation in the slice record. Code review may not have run. Should we run it now before your sign-off?"

**Backlog currency**
Slice statuses should reflect actual state. If the At a Glance counts look inconsistent with what's been described as happening, flag it. Don't read every slice — read the header counts only.

**Open items accumulating**
- qa-triage items unresolved for more than one session → surface
- Outstanding questions in product-continuity unanswered for multiple sessions → surface the top one, not all of them
- Assumptions unvalidated that were marked as blocking → surface

**Scope drift signal**
If a slice is being built that has no backlog entry, the four anchors check in solo-build will catch it. The health monitor's signal here is simpler: if the solo describes work being done and there's no corresponding slice status in the backlog, flag it.

**Phase test readiness**
When the backlog At a Glance section shows all current-phase slices at Done — none In Progress, In QA, or In Review — and no open qa-triage items from the build phase remain, surface once:

> "All Phase [N] slices are Done. Phase test is the next step whenever you're ready — it confirms the whole thing works end to end. One tip: if the build happened in Cursor, running code review in Claude Code gives independent eyes — the reviewing session has no context of the build conversation. The reverse works too."

Fire once only. If the solo isn't ready, they say so and the nudge doesn't repeat. Do not fire mid-build when slices are still active — only when the At a Glance section is clean.

---

## How It Surfaces Issues

**One issue at a time.** The most important gap first. Not a list of everything wrong.

**Specific, not vague.**
- ❌ "Something may be missing from the design sprint phase."
- ✅ "The deferred decisions log (`docs/design/deferred-decisions.md`) doesn't exist yet. That's the gate between design sprint and plan. Should we produce it now?"

**Recovery path always included.**
Never just name the problem. Name the problem and the next action.

**Non-blocking.**
The solo can say "not now" and keep moving. The health monitor logs the open item to the session handoff and checks again at session end. It doesn't repeat mid-session unless the item becomes genuinely blocking.

**Silent when healthy.**
No output when everything is running correctly. The absence of health monitor output is confirmation that the framework is running as designed.

---

## What It Does Not Do

- Does not read full documents when a file existence check is sufficient
- Does not approve steps before they run — checks after the fact
- Does not surface more than one issue at a time
- Does not repeat an issue the solo has acknowledged and chosen to defer
- Does not block the chain — the chain runs regardless
- Does not replace the skills it monitors — it surfaces gaps, not fixes them

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Reading all documents to check health | Token-expensive, slow | Check signals — file existence + handoff + backlog At a Glance |
| Surfacing all issues at once | Overwhelming, creates the bottleneck we're avoiding | One issue, most important first |
| Blocking progress while checking | Defeats the purpose | Check after the fact, surface gaps, never halt |
| Repeating a deferred issue mid-session | Interrupts flow | Log it to handoff, check again at session end |
| Output when everything is healthy | Creates noise, trains the solo to ignore it | Silent when healthy — output is always meaningful |
| Checking for framework updates mid-session | Interrupts flow for something that should be resolved at session start | Version check runs once at mode activation only — never mid-session |
| Running re-entry check for short gaps | Overhead without payoff — short gaps don't produce meaningful drift | Threshold is 21 days. Under that, silent. |
| Surfacing the phase test readiness nudge before all slices are Done | Creates noise mid-build | Check At a Glance — all current-phase slices Done and zero open qa-triage items before firing |
| "Suggested next move for you" language | Hedging, passive, invites ambiguity — the solo has to ask what to do next | Name the phase complete, list outputs, ask a direct question with named options |
| Offering two paths without naming them clearly | Solo doesn't know what each path actually does | Name each option in one sentence, then ask which — never describe options in a run-on clause |
