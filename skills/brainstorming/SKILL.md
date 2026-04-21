---
name: brainstorming
description: Product exploration for ideas that aren't fully formed yet. A genuine collaborative conversation — not a checklist, not a spec session. Explores what you're trying to do and why, surfaces what needs research before it can be designed, and ends with enough clarity to feed Discover. Includes a rough sketch mid-session when the idea benefits from something visual to react to. Use this when the solution isn't clear yet. Skip it when you already know what you want to build.
---

# Brainstorming

*For ideas that need thinking through before they can be articulated. A conversation, not a process.*

**Core question:** "Do we understand this idea well enough to tell its story?"

This is not a requirements session. Not a spec. Not a scrum ceremony. It's the conversation you'd have with a smart colleague over coffee when you've got something rattling around in your head and you want to think it through out loud. The colleague is genuinely interested, asks good questions because they're curious, volunteers a thought when they have one, and knows when to say "I'm not sure that's the right direction."

The process is a backbone — it makes sure nothing important gets missed. It should be invisible. What's visible is the conversation.

---

## When to Use

- You have an idea but the solution isn't clear yet
- You're exploring a capability or direction before committing
- You want a thought partner before articulating the idea formally

**Skip this if** you already know what you want to build. Go straight to `discover`. Brainstorming a fully-formed idea wastes time and can actually muddy clarity you already have.

---

## What Brainstorming Is Not

- Not a feasibility session — "can we build this" goes to Research
- Not a technical design session — architecture goes after Discover and Design Sprint
- Not a spec — the output feeds Discover, not an engineer's backlog
- Not a checklist to run through — if it feels like a form being filled in, something is wrong

---

## The Conversation

No rigid zones. No turn-by-turn script. The conversation goes where it needs to go, with these threads as the backbone:

**The idea itself**
What's the core of it? Not the features — the thing underneath. What problem exists, what opportunity is real, what would be different for someone if this existed? Let them tell it their way first. Don't redirect. Don't refine yet. Just listen and ask one good question to go deeper.

**Who it's for**
Get a real picture of the person, not a user type. What are they doing when this becomes relevant? What do they already have, what are they missing? The more specific this gets, the better the design will be later.

**The value moment**
Every good idea has a moment where it becomes genuinely useful. Find it. "When does this actually matter to them?" This moment is almost always the hero screen in the design sprint — knowing it early shapes everything.

**What's in the idea**
As the conversation develops, start pulling out the capabilities — the things the product actually does. Hold each one lightly. Some are core. Some are nice to have. Some are unknowns that need research before they can be designed. Don't try to resolve that now — just name them and keep going.

**Conversation discipline — the partnership rules:**
- One question per round, but make it the right question — not the next question on a list
- Volunteer a thought when you have one. If something in the idea reminds you of a pattern that works or doesn't work, say so.
- Push back when something doesn't add up. "Earlier you said X but now it sounds like Y — which is closer?" 
- Get interested. If the idea is good, that should be visible in the conversation.
- If the idea is unclear, say so directly rather than asking questions that dance around it.
- Never ask about technology, architecture, or implementation — those come later.

---

## The Rough Sketch Moment

When the conversation has enough shape — you understand who this is for, roughly what they do, and where the value moment lives — produce a rough sketch. Not a design sprint artifact. A thinking tool.

**What triggers it:** The idea is clear enough to picture but still abstract enough that a visual would sharpen the conversation. Usually happens after you understand the value moment.

**What it is:** A single rough HTML screen — intentionally low fidelity — showing approximately what the moment of value looks like. Structure and content only. No polish.

**What it does:** Gives the conversation something to react to. Almost always surfaces things that weren't said — a field that implies a data source, a flow that has a gap, a capability that looked simple but isn't. The sketch doesn't have to be right. It has to be react-able.

**After the sketch:** Ask "warmer or colder?" and follow the thread. One or two rounds of reaction is enough. This is not the design sprint — don't let it become one. The sketch is a thinking tool. The real design comes after Discover.

**If the idea is too unclear to sketch:** That's a signal. Go back to the value moment. "I'm not sure what to show you yet because I can't picture the moment where this becomes useful — can you walk me through it?" If that conversation doesn't resolve it, the idea may need more time before brainstorming can be productive.

---

## Routing — What Comes Out of Brainstorming

This is the other job brainstorming does: routing. Not everything that comes up in the conversation is ready to move forward. The brainstorm surfaces items and sends them to the right place.

**→ Discover**
The core idea is clear. We understand who it's for, what they do, where the value moment is. The brainstorm is done. Hand off to `discover`.

**→ Research**
Something came up that can't be designed until we know if it's possible. Technical feasibility questions, capability unknowns, "can this actually work" items. These get captured and parked — not killed, not pursued mid-brainstorm. Research validates them and brings back enough to inform the design sprint.

*The AI component example:* You say "what if there was an AI component that did X." The brainstorm captures what you want it to do for the user — the experience, the value moment. It does not explore which model, what the API looks like, or whether it's feasible. That goes to Research: "AI capability for X — validate feasibility before designing."

**→ Decompose first**
The idea is actually multiple independent things. Name the pieces, establish how they relate, identify what order they'd be built. Then brainstorm the first piece through the normal flow.

**→ More brainstorming**
The problem isn't clear enough yet. The value moment hasn't surfaced. Keep going — or name what's still unclear and ask the solo to sit with it and come back.

---

## The Routing Table

At the end of the brainstorm, be explicit about what's going where and why.

```
Brainstorm output
├── Core idea ready → DISCOVER
├── Feasibility unknown → RESEARCH (captured, not pursued)
├── Too large → DECOMPOSE → brainstorm each piece
└── Still unclear → more brainstorming or pause and return
```

Don't just say "we should research that." Name what the research question is. "Before we can design the AI evaluation component, we need to know: can we get real-time player data from MFL in a format that's useful for inference, and what's the latency? That's the research question."

---

## Output

Brainstorming doesn't produce a spec. It produces a brief summary — a paragraph or two — of what was understood, what's going to Discover, and what's going to Research. Save to `docs/brainstorm-[date]-[topic].md`.

```markdown
# Brainstorm — [Topic]
**Date:** [YYYY-MM-DD]
**Status:** [Ready for Discover / Pending research / Needs decomposition]

## What We Understand
[2–3 paragraphs. The idea in plain language — who it's for, what they do, 
where the value moment is. Written as a story, not bullet points. 
Good enough that a designer could start sketching from it.]

## Going to Discover
[What's moving forward and why it's ready.]

## Going to Research
[Each item that needs validation before it can be designed. 
One sentence on what the research question actually is.]

## Held for Later
[Capabilities or directions that came up but aren't part of the core idea right now.]
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Running through zones like a checklist | Feels like a form, kills the conversation | Let the conversation go where it needs to, use the backbone to check nothing's missing |
| Asking about technology or architecture | Too early, wrong phase | Stay in what and why — never how |
| Pursuing feasibility mid-brainstorm | Derails the conversation, may be a dead end | Flag it, name the research question, keep going |
| Killing ideas that need research | Loses potentially valuable capabilities | Park them explicitly — Research will bring them back if they're viable |
| Producing a spec | Wrong output for this phase | A brief story summary, not a requirements document |
| Skipping the sketch when the idea would benefit | Misses the chance to sharpen the conversation visually | When you can picture the value moment, show something rough |
| Making the sketch too polished | Becomes a design sprint, not a thinking tool | Intentionally rough — structure only, one screen, no polish |
| Sycophantic affirmation before questions | Kills the partnership feel | Just ask the next good question |

---

## What Comes Next

- **Core idea ready:** `discover` — narrative conversation that builds the full story
- **Research items:** address those first, then return to `discover` with answers
- **Decomposed pieces:** brainstorm the first piece, then `discover` for that piece

Brainstorming never hands off to planning, architecture, or build. It always hands off to Discover — or to Research and back to Discover.
