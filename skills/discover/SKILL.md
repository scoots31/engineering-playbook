---
name: discover
description: Conversational discovery that builds a shared understanding of what you're trying to create — beginning to end. Not requirements gathering. Not a spec. A story-based brief that feeds the design sprint. Use at the start of any new project or feature, regardless of whether a design exists. Works for solo builders and team-backed projects alike.
---

# Discover

*The table-setter. Run this before anything else — before design, before planning, before building.*

**Core question:** "Do we understand this well enough to make something that shows what it could be?"

This is not requirements gathering. This is not a technical scoping session. This is the conversation that a good engineer or UX person has on day one — the one where they listen, ask the right questions, and build a shared picture of what you're actually trying to create. By the end, everyone in the room would tell the same story.

The output feeds the design sprint, not an engineer's backlog.

---

## When to Use

- Starting any new project or feature — solo or team-backed
- Before any design work begins
- When you have an idea but haven't articulated it fully yet
- When a Figma exists but you still need shared understanding before building

This skill always runs first. The design on-ramp question comes at the end.

---

## How It Works

1. You give the high level overview — what you're trying to build
2. Quick clarity check — confirm shared understanding before going deeper
3. Narrative conversation — adaptive, story-focused, pulling out the use case from beginning to end
4. Output — a brief narrative document and the design on-ramp decision

No plan mode. No pipeline stages. Just a conversation that ends with clarity.

---

## Execution

### Step 1: Receive the Overview

The solo describes what they want to build at a high level. This is their opening — don't interrupt it, don't redirect it. Let them tell it their way.

After they finish, read what they've said carefully. Scan for:
- Who this is for
- What problem or opportunity it addresses
- Any existing context in the project (check for `docs/`, `BLUEPRINT.md`, prior discovery briefs)

### Step 2: Clarity Check

Before the narrative conversation begins, ask one or two questions — maximum — to confirm you understand what this is at the highest level. This is not a challenge. This is not a premise check. This is a good engineer saying "just so I'm on the same page."

**The right kind of clarity question:**
- "When you say [X], do you mean [A] or [B]?"
- "Just to make sure I'm picturing this right — is this primarily for [person] doing [thing]?"

**Not this:**
- "Is there really demand for this?"
- "Have you validated this idea?"
- "What's the ROI?"

One round only. If the overview was clear, skip this entirely and say so — "That's clear, let me ask some questions to get the full picture."

### Step 3: Narrative Conversation

This is the core of the skill. Four zones, always in this order, explored at depth appropriate to the project complexity.

**Zone 1 — Who**
Understand the person doing this. Not a demographic. A real picture.
- Who is this person and what's their context when they use this?
- What are they doing before they open this — what triggered them to come here?
- What do they already know, what do they not know?

**Zone 2 — The Journey**
Walk through what a person actually does from the moment they arrive to the moment they leave. This is the narrative spine of everything that follows.
- "Walk me through what someone does in this from the moment they open it."
- Follow every step. Don't skip ahead. Each step is a potential screen, a potential design decision.
- If a step is vague, go deeper: "And then what happens?" "What do they see there?" "What are they trying to do at that moment?"

**Zone 3 — The Moment It Matters**
Every good product has a moment where it becomes genuinely useful — where the person gets the thing they came for. Find it.
- "Where in that journey does this actually become valuable to them?"
- "What's the payoff moment — the thing they'd tell someone else about?"
- This moment often becomes the hero screen in the design.

**Zone 4 — What Done Looks Like**
How does the person know it worked? What's different for them after using this?
- "When they're done and it worked — what did they accomplish?"
- "What would make them come back?"
- This grounds the design in outcomes, not features.

**Conversation discipline:**
- One or two questions per round — don't overwhelm
- Follow threads that matter, skip threads that don't
- No affirmation before questions — just ask
- If an answer is vague, go one level deeper before moving on
- If something contradicts an earlier answer, surface it: "Earlier you said [X], but now it sounds like [Y] — which is closer?"
- Never ask about technology, architecture, or implementation — that comes later

**Adaptive depth:**

| Signal | Depth |
|--------|-------|
| Clear, specific overview, simple use case | Light — 3 to 5 questions total |
| Moderate complexity, a few open threads | Medium — 5 to 10 questions |
| Vague idea, greenfield, multi-user scenarios | Deep — multi-round conversation |

If the solo says "that's enough, I think we have it" — respect it. Note where clarity is strong and where it's thinner, then proceed.

### Step 4: Produce the Process Maps

Before writing the discovery brief, the process mapper activates to document what was surfaced in the narrative conversation. Two maps — as-is and to-be — saved to `docs/process/`.

**As-is map** — document how the process works today, exactly as described. Do not assume a system exists. The as-is may be entirely manual: emails, spreadsheets, phone calls, paper forms, decisions made in someone's head. Capture it as-is — including the workarounds and the steps that happen outside any system.

Ask any final clarifying questions needed to complete the as-is picture:
- "How does this step happen today — is there a system, or is it manual?"
- "Who else is involved in this process currently?"
- "What's the most common place this goes wrong today?"

Present the as-is map for validation before proceeding:
> "Here's how I've mapped the current process. Does this accurately reflect what happens today — including the exceptions and manual steps?"

Revise until confirmed accurate.

**To-be map** — draft the target process based on the journey conversation. Every step the solo described, every decision point, every outcome. Annotate each step with which zone of the conversation it came from.

Present the to-be map for agreement before design sprint begins:
> "Here's the to-be process — how this will work when the product is built. Before we move to design, does this map reflect what we're building? Are there decision points or branches we haven't covered?"

This agreement is the **process contract**. The to-be map is updated as screens and slices are added, but its agreed structure does not change without an explicit decision.

Save both to `docs/process/`:
- `docs/process/as-is-[name].md`
- `docs/process/to-be-[name].md`

---

### Step 5: Produce the Discovery Brief

When the conversation reaches clarity, produce a brief narrative document. Small on purpose — a good designer doesn't need 40 pages to start sketching.

Save to `docs/discovery-brief.md` in the project. If no `docs/` directory exists, create it.

---

```markdown
# Discovery Brief — [Project or Feature Name]
**Date:** [YYYY-MM-DD]
**Status:** Ready for design sprint

## The Story

[Two to four paragraphs. Written as a narrative — not bullet points, not requirements.
Who this is for, what they're trying to accomplish, how they move through it from start
to finish, and where the moment of value lives. Written the way you'd tell it to a UX
designer on their first day. Someone who reads this should be able to picture it.]

## Key Moments

[The significant points in the journey — derived from the conversation. Not designed yet,
just named and briefly described. These become the design targets.]

- **[Moment name]** — [One sentence describing what's happening here and why it matters]
- **[Moment name]** — [One sentence]
- **[Moment name]** — [One sentence]

## Open Threads

[Anything that came up but wasn't resolved — things that might affect the design but
don't need to be answered before starting. Honest about what we don't know yet.]

- [Open thread]

## What We're Not Building (Yet)

[Anything explicitly set aside for later. Keeps scope honest.]

- [Out of scope item]
```

---

### Step 6: Design On-Ramp

After the brief is written, ask one question:

> "Before we move to design — do you have an existing Figma file we should work from, a product or design you'd like to reference for look and feel, or are we starting from scratch?"

**Their answer routes everything that follows:**

- **Figma exists** → Import it. The design sprint uses the Figma as source of truth. Discovery brief provides the story layer.
- **Reference exists** → Note it in the brief. The design sprint uses it as a constraint and aesthetic starting point.
- **Starting from scratch** → The design sprint opens with the functional story conversation and produces an HTML artifact from the discovery brief.

Document their answer at the bottom of `docs/discovery-brief.md`:

```markdown
## Design On-Ramp

**Path:** [Figma import / Reference-based / From scratch]
**Details:** [Figma link, reference URL, or "none"]
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Asking about technology | Pulls conversation into implementation too early | Stay in what and why — never how |
| Requirements language | "The system shall..." kills narrative thinking | Keep it in story form — "a person does..." |
| Challenging the premise | This isn't the moment for that | Trust that they've decided to build this |
| Over-questioning simple projects | 20 questions for a straightforward tool | Read the complexity, calibrate depth |
| Accepting vague journey steps | "They use the app" is not a step | Go deeper — "and then what do they see?" |
| Skipping the design on-ramp question | Leaves the next step undefined | Always ask it, always document the answer |
| Producing a spec instead of a brief | Wrong output for what comes next | Narrative and key moments only |

---

## Output Summary

| Artifact | Location | Contents |
|---|---|---|
| Discovery brief | `docs/discovery-brief.md` | Story, key moments, open threads, out of scope, design on-ramp |

---

## What Comes Next

The discovery brief feeds the design sprint — not an engineer's backlog, not a requirements document.

- **From scratch** → Design sprint opens with the brief and produces an HTML artifact
- **Figma exists** → Design sprint reads the Figma against the brief
- **Reference exists** → Design sprint uses reference as aesthetic constraint, brief as story

This skill does not hand off to `system-architecture`, `task-breakdown`, or planning. Those come after design — not before.
