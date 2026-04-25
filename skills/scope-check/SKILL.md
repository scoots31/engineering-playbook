---
name: scope-check
description: Entry gate for Workshop. Asks one question — who is this for and how long does it live? — then routes to Workshop (spike/tool) or hands to the framework (product).
---

# Workshop — Scope Check

*The front door. One question, one routing decision.*

**Core question:** "Is this a product, a tool, or a spike?"

---

## When to run

At the start of any new piece of work that isn't obviously a product. If the solo
opens with "I want to try...", "quick script to...", "let me see if...", "I'm
curious about...", "one-shot to...", route here first.

If the opening is clearly a product — "I want to build an app that other people
will use" — skip Workshop entirely and go to the framework `start`.

---

## The one question

**"Who is this for, and how long does it live?"**

The answer routes:

| Answer | Shape | Next step |
|---|---|---|
| "Me, right now. Hours to days." | **Spike** | `spike` skill with a timebox |
| "Me, ongoing. Personal utility." | **Tool** | `spike` skill framed as Keep-intent |
| "Other people, indefinitely." | **Product** | Hand to the framework `start` |

If the solo is uncertain, ask one clarifying question. Don't proceed on ambiguity.

---

## The challenge

If the solo says "spike" but describes user-facing behavior, auth, accounts, or
external sharing — challenge. "You said spike, but you mentioned users. Is this
actually a product?" The principle of **explicit disposability** means the solo
names the shape honestly.

If they confirm it's a spike despite user mentions, capture those mentions as
**graduation triggers** — the signals that will later force promotion via `land`.

---

## Timebox

Every spike gets a timebox. Default: 2 hours. Stretch: 1 day. Work scoped beyond
a day — challenge. It may be a Tool or a Product, not a spike.

Tools get a scope, not a timebox — "it does X" with a clear stopping point.

---

## Output

A one-paragraph frame:
- Shape (spike / tool)
- Outcome (the question to answer or the thing to make work)
- Timebox (for spikes) or scope (for tools)
- Graduation triggers (signals that would force promotion)

Hand off to `spike`.

---

## What scope-check does not do

- Does not route everything to the framework. If it routes everything to the framework, the companion
  framework doesn't exist.
- Does not let the solo pick Workshop to avoid ceremony when the work is actually
  a product. Hold the line.
