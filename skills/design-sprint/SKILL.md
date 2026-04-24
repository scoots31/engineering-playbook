---
name: design-sprint
description: Produces a visual HTML artifact for every screen before any code is written. Bridges the discovery brief to the build phase by creating something everyone can point at and make real decisions from. Runs as a collaborative warmer/colder loop — not a one-shot deliverable. Output is HTML screens plus a deferred decisions log that feeds directly into planning.
---

# Design Sprint

*The Rosetta Stone. Runs after discovery, before planning. Nothing gets built until this is done.*

**Core question:** "Do we have something tangible enough to make real build/defer decisions from?"

This is not a design deliverable. It is not a Figma translation exercise. It is a short, timeboxed collaborative session that produces an HTML artifact good enough to point at — and a conversation that surfaces what's in scope for Phase 1 versus what gets deferred. The artifact becomes the shared language for everyone who touches the project after this.

---

## When to Use

- After the discovery brief is complete and the design on-ramp is decided
- Before `prd-to-plan` — planning phases cannot be sequenced without knowing what was approved vs deferred
- When a visual doesn't exist yet (on-ramp 1 or 3) or exists but needs a story layer (on-ramp 2)

This skill always runs after `discover`. The on-ramp decision made at the end of `discover` routes to one of three starting points below.

---

## Three On-Ramps

**On-ramp 1 — From scratch**
No visual exists. The design sprint opens with the discovery brief and produces an HTML artifact through a warmer/colder loop. This is the hardest path and the most common one.

**On-ramp 2 — Figma exists**
Import via Figma MCP. The design sprint reads the Figma as the visual source of truth. The discovery brief provides the story layer on top — the "why" behind each screen. The warmer/colder loop confirms the Figma reflects the story correctly.

**On-ramp 3 — Reference exists**
"Make it feel like ESPN" or "reference this screenshot." The design sprint uses the reference as aesthetic constraint and produces HTML in that direction. The `awesome-design-md` skill can assist with extracting the right aesthetic tokens.

All three on-ramps end in the same place: HTML screens, a walk-through conversation, and a deferred decisions log.

---

## The Solo Assumption

The solo cannot produce the design artifact alone — the AI produces it collaboratively. What the solo brings:
- The discovery brief (the story)
- Domain knowledge ("that field won't exist in the API until Phase 2")
- Warmer / colder judgment — the most important contribution

What the AI brings:
- Design execution
- The HTML artifact
- The walk-through questions that surface build/defer decisions

This works because most people cannot describe what they want visually until they see something wrong. The design sprint is not requirements gathering — it is a series of warmer/colder moments.

---

## Execution

### Step 1: Read the Discovery Brief and Process Maps

Before producing anything, read:
- `docs/discovery-brief.md` — the story, key moments, moment of value, design on-ramp
- `docs/process/to-be-[name].md` — the agreed to-be process map

If no discovery brief exists, stop. Run the `discover` skill first.
If no to-be process map exists, stop. The process map should have been produced during discover — run that step before continuing.

**Cross-reference screens against the to-be map as the sprint progresses.** Every step in the to-be map should have at least one screen that supports it. After each screen is approved, annotate the to-be map with the screen reference. Gaps — steps with no screen — are surfaced as decisions: is this handled in the background, or does it need a UI state?

> "Step 4 in the to-be map — 'system validates eligibility' — doesn't have a screen yet. Is this a background step the user never sees, or does it need an error/confirmation state on screen?"

These gaps are documented in the deferred decisions log, not silently assumed.

### Step 2: Ask the Aesthetic Question (On-ramp 1 and 3 only)

Before writing any HTML, ask one question:

> "Is there a product, app, or aesthetic direction you want this to feel like — or should I make a call and you react to it?"

If they name something (ESPN, Linear, Notion, a screenshot): note it. That's your aesthetic constraint.
If they say "make a call": produce a reasonable starting point and state what direction you chose. They'll correct it in the warmer/colder loop.
If they say "Figma exists": go to on-ramp 2.

Do not skip this question. Skin direction saved two full rounds in testing.

### Step 3: Identify the Hero Screen

From the key moments in the discovery brief, identify the one screen where the system's core value is most visible. This is almost always the moment of value from Zone 3 of the discovery conversation.

**Build this screen first.** All other screens extend from it. Getting the hero screen right — structure and skin — before moving to secondary screens keeps the sprint focused and prevents aesthetic drift across screens.

State your choice: *"The hero screen is [X] because [one sentence on why it shows the moment of value]."*

### Step 4: Build the First Pass — Structure Only

Produce an HTML mockup of the hero screen. First pass discipline:

- **Structure first, skin second.** Layout, information hierarchy, component placement, data relationships. Do not invest heavily in the skin yet.
- Intentionally rough is fine. The goal is: does this layout correctly represent what the person does here?
- Use placeholder data that feels real (real player names, real-looking numbers, realistic states)
- Include all interactive elements that are visible — buttons, filters, toggles, tabs. Every visible interactive element becomes a gate question in the walk-through.
- Serve the file so it can be opened in a browser. Save to `docs/design/sprint-[screen-id].html`.

After producing: *"Here's the first pass. I built it this direction: [one sentence on structure decisions made]. Warmer or colder on the layout before we touch the skin?"*

**Get structure warm before touching skin.** These are two separate passes with two separate questions.

### Step 5: Warmer / Colder Loop

**Sprint length depends on what you brought in.** The loop is faster when the discovery brief is detailed and wireframes or prior screen thinking already exist. When starting from scratch with only a rough idea, expect more rounds — the early passes are surfacing what belongs on the screen, not just how it's arranged. That's normal. The loop ends when there's something good enough to make real decisions from, not when it's perfect.

| Starting condition | Expected rounds on hero screen |
|---|---|
| Detailed discovery brief + wireframes | 2–3 rounds |
| Strong discovery brief, no wireframes | 3–5 rounds |
| Rough idea, early discovery | 5+ rounds, may need to pause and deepen discovery first |

If after 3 rounds the structure is still not warm: stop the design sprint. Go back to `discover` and deepen Zone 2 (the journey) — the structure is unclear because the story isn't clear yet.

Maximum three rounds per screen once structure is warm. Each round:
1. Solo gives warmer/colder on what's in front of them
2. AI adjusts and states what changed and why
3. Repeat

**Round discipline:**
- If they say warmer on structure but cold on skin: do a full skin pass. Treat skin direction as its own question.
- If the same element comes back cold twice: surface the underlying question. "You've been cold on the delta chart twice — is it the format, the data shown, or something else?"
- If they say "good enough, move on": respect it. Note what's thin and move to the next screen.

**Skin pass specifically:**
When the structure is warm but skin is cold, ask one question before rebuilding: *"What should this feel like — is there a product or aesthetic direction to reference?"* Then rebuild the full skin from that direction. Do not incrementally adjust colors — change the design system.

### Step 6: Extend to All Screens

Once the hero screen is approved (structure + skin), extend to remaining screens in this order:
1. The screens immediately before and after the hero in the user journey
2. Any screen that was explicitly called out in the discovery brief key moments
3. Remaining screens in navigation order

Each screen inherits the design system established in the hero screen. The skin does not change screen to screen — only the content and layout patterns.

For each screen: produce it, state what decisions were made, ask for warmer/colder. Move at pace — secondary screens should move faster than the hero because the design language is already settled.

Save each screen to `docs/design/sprint-[screen-id].html`.

### Step 7: The Walk-Through Conversation

Once all screens are at acceptable fidelity, run a walk-through. This is the decision-surface conversation — not a review, not approval. The goal is to make explicit build/defer decisions screen by screen, and to surface the behind-the-scenes work that the design implies but doesn't show.

**Two categories of work surface here, not one:**

**Visible scope** — everything on the screens. Each interactive element is a question: in or out for Phase 1? Organized by screen so decisions are traceable back to what prompted them.

**Implied infrastructure** — backend logic, data models, API requirements, and architecture that must exist before the interface can connect to anything real. This is invisible in the design but the design is what surfaces it. A UI toggle that looks simple may imply a historical data pipeline, a new query, a caching layer. These items belong in the decisions log alongside the visible ones.

For each screen, ask two questions:
> "Is everything visible on this screen in scope for Phase 1, or are we deferring anything?"
> "What has to exist behind this screen before it can work — data, APIs, logic — and is any of that a Phase 1 dependency or something we're not building yet?"

The AI should proactively flag both categories:
- Visible elements that imply multiple data sources or complex queries
- UI controls that look simple but have significant backend implications
- Features that require infrastructure that isn't in scope yet
- Anything that was in the "What We're Not Building Yet" section of the discovery brief

A good example: "The temporal lens chips — 2Y, 1Y, Season, L6, L3, Playoffs — are all visible here. Two questions: first, are all six in scope for Phase 1? Second, behind each lens is a historical aggregation query — do we have that data, and is building that query in Phase 1 or later?"

Document every decision — visible and implied.

### Step 8: Produce the Deferred Decisions Log

After the walk-through, write `docs/design/deferred-decisions.md`. This feeds directly into `prd-to-plan`. Organized by screen so the planner can trace each decision back to the design.

---

```markdown
# Deferred Decisions — [Project or Feature Name]
**Date:** [YYYY-MM-DD]
**Status:** Ready for prd-to-plan

## Phase 1 Scope

### [Screen name]
**Visible — in scope:**
- **[Element]** — [One sentence on what it does]

**Visible — deferred:**
- **[Element]** — [Why deferred]
  - *Trigger to revisit:* [What condition moves this back in]

**Implied infrastructure — in scope:**
- **[Backend item]** — [What it is and why Phase 1 needs it]

**Implied infrastructure — deferred:**
- **[Backend item]** — [What it is and why it's not Phase 1]
  - *Trigger to revisit:* [What condition moves this back in]

[Repeat section for each screen]

## Open Questions

[Things that came up in the walk-through that couldn't be decided — data dependencies, unknowns that need external input, architecture decisions not yet made.]

- [Open question] — *Blocks:* [what it blocks]
```

---

### Step 9: Stakeholder Handoff Package (Optional)

Before closing the sprint, ask one question:

> "Does this need to go to anyone outside the build — a stakeholder, client, approver — before design review begins?"

If no: skip. Continue to Output Summary.

If yes: produce a handoff package at `docs/design/handoff/<YYYY-MM-DD>/`:

| File | Purpose |
|---|---|
| `artifact.html` | Standalone — all screens inlined into one file, opens without a server |
| `artifact.pdf` | PDF render of the HTML — for stakeholders who prefer PDF over a link |
| `feedback-template.md` | Structured markdown for the stakeholder (or solo) to fill in |

Generate the PDF via headless Chrome or the solo's preferred tool — whatever produces a readable PDF of the standalone HTML.

The solo shares whichever format the stakeholder prefers. Completed feedback returns as `docs/stakeholder-feedback/<YYYY-MM-DD>-<topic>.md` — the solo pastes or types what they heard into the template.

`design-review` reads any file in `docs/stakeholder-feedback/` as first-class input on the next round.

**Feedback template (`feedback-template.md`):**

```markdown
# Stakeholder Feedback — <topic>
**Reviewer:** 
**Date:** 
**Artifact reviewed:** docs/design/handoff/<date>/

## Overall reaction
[High-level impression — what felt right, what felt off]

## Per-screen comments
- <screen name>: 
- <screen name>: 

## Concerns / blockers
[Anything that would stop approval]

## Approval status
- [ ] Approved to build
- [ ] Approved with changes (listed above)
- [ ] Needs another round
```

---

## Output Summary

| Artifact | Location | Contents |
|---|---|---|
| Hero screen | `docs/design/sprint-[id].html` | First approved screen, design system established here |
| All screens | `docs/design/sprint-[id].html` | One file per screen, named by wireframe ID |
| Deferred decisions log | `docs/design/deferred-decisions.md` | Approved for Phase 1, deferred, open questions |
| Stakeholder handoff package (optional) | `docs/design/handoff/<date>/` | HTML + PDF + feedback template for async review |

---

## What Comes Next

The deferred decisions log feeds `prd-to-plan`. Phases are sequenced around what was approved — not around what's technically comfortable to build. The HTML screens become the starting point for the frontend — they are not translated into code, they *become* the first frontend code.

- `prd-to-plan` → phases by risk, starting from the approved Phase 1 list
- `to-issues` → GitHub issues in dependency order, each referencing the relevant screen file

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Jumping straight to skin | Structure and skin require separate warmer/colder questions | Get structure warm first, then ask about skin direction |
| Incrementally adjusting colors | Produces neither version correctly | When skin is cold, ask for direction and rebuild the design system |
| Building all screens before hero is approved | Aesthetic drift, rework across all screens | Hero screen approved first, everything else inherits from it |
| Skipping the walk-through | No build/defer decisions, planning inherits too much scope | Walk-through is mandatory — it's the gate, not a nice-to-have |
| Treating the deferred log as optional | prd-to-plan phases get bloated with deferred scope | Every visible element gets a decision: Phase 1 or deferred |
| Perfect fidelity on every screen | Slows the sprint, wrong level of investment | Good enough to point at and make decisions from — not pixel perfect |
| Translating Figma to code | Double work, Figma and HTML go out of sync | HTML artifact IS the first frontend output |

---

## Key Insight

The design sprint does not produce a visual. It produces a **decision surface**.

Two categories of work become visible that couldn't be seen before:

**What's on the screens** — every visible element is a question: *do we build this in Phase 1?* That question cannot be asked against a wireframe or a word document. It can only be asked against something people can see and react to.

**What the screens imply** — backend logic, data models, API requirements, and architecture that must exist before the interface connects to anything real. A UI toggle that looks simple may imply a historical data pipeline. A filter chip may imply a query that doesn't exist yet. The design doesn't show these things — but it's the design that surfaces them.

The deferred decisions log captures both, organized by screen. That log is the real deliverable. The screens are the tool that makes the conversation possible. And `prd-to-plan` cannot sequence phases correctly without it — because phases are built around what's approved and what's implied, not around what's technically comfortable to build first.
