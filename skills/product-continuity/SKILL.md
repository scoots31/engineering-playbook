---
name: product-continuity
description: The project's institutional memory. Always-on in guided and piloted mode — silent in bare mode (the default). Loads once at mode activation. Captures decisions with reasoning, outstanding questions needing external input, assumptions being treated as true, known risks, changes, session documentation, glossary terms, and target state documentation for training and wiki use. Activates at key moments throughout every phase. Produces and maintains docs/continuity/ for the life of the project.
---

# Product Continuity

*What gets decided, why it got decided, and what's still open. Nothing important disappears between sessions.*

**Core question:** "If this project paused today and resumed in three months, would the next person — or the next session — be able to pick up exactly where we left off with full context?"

This skill is the project's institutional memory. In a team, this is the person who writes the meeting notes, keeps the decision log, tracks the open questions, maintains the wiki, and makes sure critical context doesn't live only in someone's head. Solo, that context evaporates between sessions. This skill captures it continuously so it doesn't have to be reconstructed.

This skill activates when guided or piloted mode is chosen — not in bare mode (the default). Once loaded, it captures at the right moments throughout every phase without being re-invoked.

---

## When It Activates

**During any session:**
- A decision is made → decision log entry
- A question surfaces that needs outside input → outstanding questions log
- An assumption is stated (explicitly or implied) → assumptions log
- A risk is named → risk register
- Something changes from a previous decision or design → change log
- A new term or concept is introduced with project-specific meaning → glossary

**At the end of every session:**
- Session documentation entry
- Session handoff summary updated

**At phase completion:**
- Target state documentation updated
- Onboarding document refreshed

**At phase transition:**
- Current phase marker updated

---

## Long-Gap Re-entry

When framework-health surfaces a long-gap signal (21+ days since last session) and the solo says yes, run these three checks in sequence. Do not start new work until all three complete or are explicitly skipped.

---

**Check 1 — Codebase state**

Read the last session date from `docs/continuity/handoff.md`. Run `git log` from that date forward. Check for uncommitted changes. Check for open branches not mentioned in the handoff.

Surface anything meaningful:
- Commits since last session that weren't produced in that session (external changes, merges)
- Uncommitted work not flagged in the handoff
- Open branches not accounted for

If clean: "Codebase clean — no changes since last session."

If not: name each finding specifically. Ask whether each is expected before moving to Check 2.

---

**Check 2 — Environment**

Ask the solo to confirm whether the app or service runs. If the project has a known start command (in tech-context.md or the handoff), name it. Check whether any dependency manifest has changed since last session (package.json, requirements.txt, go.mod, or equivalent). If dependencies changed, flag it — don't assume things still work.

> "Environment check: does [the app/service] start and run without errors? Any dependency changes since we last worked?"

Wait for the solo's answer. If they surface an issue, help diagnose before proceeding to Check 3.

---

**Check 3 — Context validity**

Review the three continuity documents most at risk of staleness after a significant gap:

1. `docs/continuity/questions.md` — any questions marked Blocking that are still Open after 21+ days? Name them. They may have been answered (update the log) or may still be blocking (surface for resolution before new work starts).

2. `docs/continuity/assumptions.md` — any Unvalidated assumptions whose validation window has passed? Name them. Ask whether they've been validated or whether they're still being treated as true.

3. `docs/continuity/handoff.md` — read the "Key context to carry" section aloud. Ask: "Does this still hold, or has anything shifted since we last worked?"

At the end of Check 3, produce a re-entry summary:

> "Re-entry check complete. [Codebase: clean / N findings resolved]. [Environment: running / issue resolved]. [Context: all valid / N stale questions or assumptions addressed]. Ready to pick up at [next session action from handoff]?"

The solo's yes moves to normal session flow.

---

## Nivya Conversations

When `nivya` is active in the conversation, product-continuity does not capture passively. Nivya handles the routing — if something said in her conversation should be logged, she will ask the solo first, and only on an explicit yes does capture happen. This prevents exploratory thinking from being recorded as settled decisions.

The solo's guarantee: nothing said to Nivya gets written into `docs/continuity/` without the solo saying yes.

---

## The Documents

All continuity documents live in `docs/continuity/`. Created at the start of the project, maintained for its life. Never recreated — only appended and updated.

---

### 1. Session Log — `docs/continuity/sessions.md`

A running record of every session. Not a transcript — a faithful capture of what mattered. Enough detail that someone reading it can reconstruct what happened and why, without having been there.

**Entry format:**
```markdown
## Session — [YYYY-MM-DD]
**Phase:** [Brainstorm / Discover / Design Sprint / Design Review / Build / QA / Phase Test / etc.]
**Duration:** [Short / Medium / Long]

### What was discussed
[2–4 sentences. The substance of the session — what problem was being worked on, 
what the conversation covered, what directions were explored.]

### What was decided
- [Decision 1 — stated plainly]
- [Decision 2]

### What was produced
- [Artifact or output — e.g., "sprint-p1.html hero screen approved"]
- [Skill run — e.g., "tech-context established, docs/tech-context.md created"]

### What changed from before
- [Change 1 — what it was, what it became]

### Questions surfaced (needing outside input)
- [Question — who needs to answer it]

### Where to pick up
[One clear statement. The single most important thing to orient the next session.]
```

---

### 2. Decision Log — `docs/continuity/decisions.md`

Every significant decision with the reasoning behind it. Not just what was decided — why it was decided, and what alternatives were considered and rejected. This is the document that prevents re-litigating settled decisions and reconstructing lost reasoning.

**What counts as significant:** Any decision that affects the design, the process, the architecture, the scope, or the build sequence. Small implementation details don't need logging. Anything that would affect what gets built or how it works does.

**Entry format:**
```markdown
## [Decision title] — [YYYY-MM-DD]
**Phase:** [when this was decided]
**Status:** Active / Superseded by [link to later decision]

**Decision:** [What was decided, stated plainly in one sentence.]

**Why:** [The reasoning. What made this the right call for this project.]

**Alternatives considered:**
- [Alternative A] — rejected because [reason]
- [Alternative B] — rejected because [reason]

**Tradeoffs acknowledged:**
[What this decision trades off. What will need to be revisited as a result.]

**Affected by:** [Prior decision or constraint that shaped this one, if any]
```

---

### 3. Outstanding Questions — `docs/continuity/questions.md`

Questions that can only be answered by the solo going to the outside world. Not design questions (those get resolved in the sprint). Not technical questions (those go to research spikes). These are questions that require external input: stakeholder decisions, business rules that live in someone's head, data that needs to be retrieved from a system, regulatory requirements, organizational policies.

**Entry format:**
```markdown
## [Question] — [YYYY-MM-DD]
**Surfaced during:** [which phase / session]
**Blocking:** [what can't proceed until this is answered — or "non-blocking"]
**Who can answer:** [specific person, team, or source]
**Status:** Open / Answered [date]

**Answer (when received):**
[The answer, stated plainly. Date received. If it changed any decisions, link to the decision log entry.]
```

Outstanding questions are reviewed at the start of each session. If something has been answered since last session, the entry is updated and any downstream decisions are triggered.

---

### 4. Assumptions Log — `docs/continuity/assumptions.md`

Things being treated as true without verification. Different from outstanding questions (those need active answers). Assumptions are things the project is proceeding on — often without anyone explicitly stating they're assumptions.

The assumptions log makes them visible so they can be watched, validated, and corrected when they turn out to be wrong.

**Entry format:**
```markdown
## [Assumption] — [YYYY-MM-DD]
**Surfaced during:** [which phase]
**What we're assuming:** [The assumption stated plainly.]
**Why we're proceeding on this:** [Why it's reasonable to assume this right now.]
**What happens if it's wrong:** [Impact on design, build, or process.]
**How to validate:** [What would confirm or deny this assumption.]
**Status:** Unvalidated / Validated [date] / Invalidated [date — and what changed]
```

---

### 5. Risk Register — `docs/continuity/risks.md`

Known threats to the project being actively tracked. Different from assumptions (those are things we're treating as true). Risks are things we know could go wrong — and we're watching for them.

**Entry format:**
```markdown
## [Risk] — [YYYY-MM-DD]
**Identified during:** [which phase]
**What could go wrong:** [The risk stated plainly.]
**Likelihood:** High / Medium / Low
**Impact if it happens:** [What would need to change — scope, timeline, architecture.]
**Trigger condition:** [The specific thing that would make this risk real.]
**Watch signal:** [What the solo would notice that suggests this risk is materializing.]
**Mitigation:** [What's being done to reduce likelihood or impact.]
**Status:** Open / Resolved [date — and how]
```

---

### 6. Change Log — `docs/continuity/changes.md`

A record of what changed from a previous decision, design, or plan — and why. The change log is not a git log. It's a product-level record of meaningful changes to scope, design, process, or direction.

**Entry format:**
```markdown
## [Change title] — [YYYY-MM-DD]
**Phase:** [when this change was made]

**What it was:** [Previous state — what was agreed or designed before this.]
**What it became:** [New state — what replaced it.]
**Why it changed:** [The reason — new information, failed assumption, design review finding, QA discovery, etc.]
**What it affects:** [Other decisions, slices, or designs that need to account for this change.]
```

---

### 7. Glossary — `docs/continuity/glossary.md`

Project-specific terminology as it develops. Every project builds its own vocabulary. Without a glossary, each new session — or each new person — has to reconstruct the shared language.

The glossary captures terms that have a specific meaning in this project's context, distinct from their general meaning or from how they might be used elsewhere.

**Entry format:**
```markdown
## [Term]
**Defined:** [YYYY-MM-DD] during [phase]
**Meaning in this project:** [What this term means here, specifically.]
**Distinguished from:** [A similar term or common meaning this is different from, if relevant.]
**First used in:** [Session or document where this term first appeared with this meaning.]
```

---

### 8. Target State Documentation — `docs/continuity/target-state.md`

What we're building — written for humans who weren't in the room. This document is updated as the project progresses and serves as the foundation for training materials, wiki content, and onboarding. Written from the user's perspective, not the builder's.

**Structure:**
```markdown
# [Product or Feature Name] — What It Is and How It Works
**Last updated:** [YYYY-MM-DD]
**Phase coverage:** Through Phase [N]

## What this is
[2–3 sentences. What this product or feature does, for whom, and why it exists. 
Written for someone who has never heard of it.]

## Who uses it
[The user and their context. When they show up, what they're trying to do.]

## How it works — the journey
[Walk through the experience from the user's perspective, step by step.
Written as narrative, not bullet points. How a trainer would explain it to a new user.]

## Key concepts and terms
[The 3–5 concepts a new user needs to understand to use this confidently.
Link to glossary entries for full definitions.]

## What it replaces or improves
[The as-is process this replaces. Written in terms a user of the old process would recognize.]

## What's coming next
[Phase N+1 — what will be added. Sets expectations without overpromising.]
```

Updated after each phase completes. The Phase 1 completion version becomes the training material for Phase 1. Phase 2 adds to it.

---

### 9. Session Handoff — `docs/continuity/handoff.md`

The current state of the project — always reflecting the most recent session. Overwritten at the end of each session with a fresh summary. This is the first thing read at the start of any new session.

**Format:**
```markdown
# Project Handoff — [YYYY-MM-DD]
**Current phase:** [where the project is right now]
**Overall status:** [one sentence — what's happening]

## Where we are
[2–3 sentences. The honest current state. What's Done, what's in progress, what's next.]

## What was just completed
[The most recent session's output — decisions made, artifacts produced, slices done.]

## Open right now
[What's actively in progress or waiting. Anything that was left mid-session.]

## Outstanding questions needing outside input
[The top 2–3 from docs/continuity/questions.md that are currently blocking or most urgent.]

## Next session picks up at
[One clear statement. The single most important thing to do next.]

## Key context to carry
[1–3 things that are easy to forget but matter — a constraint, a decision rationale, 
a risk being watched, an assumption that's relevant right now.]
```

---

### 10. Onboarding Document — `docs/continuity/onboarding.md`

The curated path into this project for someone coming in cold — a new developer, a contractor, a new AI session, a stakeholder who wants to get up to speed. Not every document — the right documents in the right order.

**Format:**
```markdown
# Getting Up to Speed — [Project Name]
**Updated:** [YYYY-MM-DD]

## What this is
[One paragraph from target-state.md — the plain-English summary.]

## The story so far
[2–3 sentences on where the project is and how it got here.]

## Read these first, in this order
1. `docs/continuity/target-state.md` — what we're building and why
2. `docs/discovery-brief.md` — the original use cases and user story
3. `docs/process/to-be-[name].md` — the agreed target process
4. `docs/continuity/decisions.md` — key decisions and their reasoning
5. `docs/backlog.md` — current slice status
6. `docs/continuity/handoff.md` — where we are right now

## Important context
[The 3–5 things someone needs to know that aren't obvious from the documents — 
a constraint, an assumption, a risk, a decision that looks odd without context.]

## What not to change without discussion
[Settled decisions that should not be re-litigated — and a link to the decision log entry for each.]
```

---

### 11. Current Phase Marker — `docs/continuity/current-phase.md`

A single-file, single-source-of-truth record of the project's current framework phase. The cheapest possible read at session start — one file, a handful of lines — so any skill or session can orient itself in one step without parsing longer documents.

Updated at every phase transition. Never duplicated elsewhere.

**Format:**
```markdown
# Current Phase

**Phase:** [Brainstorm / Discover / Design Sprint / Design Review / Plan / Build / QA / Phase Test / Deploy]
**Since:** [YYYY-MM-DD]
**Previous:** [Phase name] (completed [YYYY-MM-DD])
**Next expected:** [Phase name]
**Notes:** [Optional — one line on anything unusual about the current phase, e.g., "re-entered Design Review after QA surfaced a gap"]
```

Written once at project start. Updated by product-continuity at every phase transition. Read at the beginning of every session before any other continuity document.

---

## How It Activates Without Being Invoked

The product-continuity skill listens throughout every phase and captures silently in the background — most captures require no solo input. It speaks only when a decision genuinely requires the solo that no inference can substitute.

**Automatic captures (no solo input needed):**
- Decisions made and documented during any phase → decision log
- Terms defined with project-specific meaning → glossary
- Changes to previous agreements → change log
- Risks named during principal engineer review or design review → risk register

**Surfaces for solo input when:**
- A question can't be answered without outside information → "Adding this to outstanding questions — who's the right person to answer it?"
- An assumption is implied but unstated → "I'm noting an assumption here: [X]. Is that right, and do you know when we can validate it?"

**At session end:**
- Session log entry written
- Handoff document updated
- Target state updated if a phase completed

**On session close signal ("let's close out" or equivalent):**
After writing the session log and updating the handoff, generate a resume prompt and append it to `docs/continuity/handoff.md`:

```markdown
## Resume Prompt
Copy this into your next session to pick up without losing context:

> "Resuming [Project Name]. Last session closed at [Phase / Gate / Slice].
> [One sentence on where things stand]. Continue from there."
```

The solo copies it, pastes it next session. No re-explaining, no cold start.

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Logging decisions without reasoning | Nobody remembers why in three months | Always capture the why and the alternatives considered |
| Outstanding questions with no owner | Questions without owners don't get answered | Always name who can answer it |
| Assumptions that are never revisited | Wrong assumptions silently corrupt the build | Review assumptions log when a new phase starts |
| Session log written as a transcript | Unreadable and unsearchable | Capture what mattered — decisions, outputs, where to pick up |
| Target state updated only at the end | Documentation that's always out of date | Update after each phase completes |
| Glossary skipped because "everyone knows what it means" | New sessions start from scratch on terminology | Capture terms as they develop, not after the fact |
| Handoff document not read at session start | Session opens without orientation | Handoff is always the first thing read |
| Skipping re-entry after a long gap | Codebase drift, broken environment, and stale assumptions surface mid-build instead of at session start | When framework-health flags a 21+ day gap, always run the three-check protocol before starting new work |
