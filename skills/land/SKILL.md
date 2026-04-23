---
name: land
description: The Workshop exit skill. Three outcomes — Toss (capture learning, archive), Keep (personal tool with minimal hygiene), Promote (hand to SBF with a prepared brief).
---

# Workshop — Land

*The exit. The load-bearing skill. Without an explicit landing, spikes silently
become shipped products.*

**Core question:** "What now — toss, keep, or promote?"

---

## The three outcomes

### Toss

The spike didn't work, or worked but isn't worth keeping. The outcome is the
**learning**, not the code.

Actions:
1. Summarize the journal into 3-5 bullets: what was tried, what happened, what
   surprised, what it means for future attempts
2. Write the summary to MemPalace as a `spike` memory — so the same exploration
   doesn't get redone six months later
3. Archive the code — move to `archive/spikes/[name]/` or delete if truly worthless
4. Done

### Keep

The spike worked. It's a personal tool now. It runs, does its job, and that's
enough.

Actions:
1. One-pass hygiene:
   - Rename anything named `temp` or `test` to something real
   - Add a one-line header comment or README: what it does, how to run it
   - Remove hardcoded secrets (move to env / config)
   - One sanity re-run end-to-end to confirm it still works
2. Freeze. Resist the urge to "clean it up properly." It's a tool, not a product.
3. Log to MemPalace as a `tool` memory — what it is, where it lives, how to run it

### Promote

The spike worked AND the work is crossing into product territory. Graduation
triggers fired, or the solo wants to ship this to others.

Actions:
1. **Stop treating it as spike code.** The existing code is now a prototype, not
   the foundation. Expect to rewrite parts.
2. Prepare a handoff brief:
   - What the spike proved (the working outcome)
   - What's in the code today vs what's not
   - What the graduation triggers revealed about scope
   - Known hacks and shortcuts that must not survive promotion
3. Hand to SBF `start` with the brief as the opening context
4. From here, the Solo Builder Framework runs. Discover, design sprint, the full chain.

---

## The honest conversation

`land` is not an automatic classifier. It asks directly: "What now?"

If the solo says "Keep" but describes users, challenge. "You said Keep for personal
use, but you mentioned sharing. Is this actually a Promote?"

If the solo says "Promote" but the spike is barely working, challenge. "You want
to promote, but the outcome isn't solid yet. Extend the spike or promote with a
known-risky foundation?"

---

## The anti-drift guardrail

The failure mode Workshop guards against: **spikes silently becoming shipped
products**. If `land` never runs, that failure happens by default. Every spike
ends with a `land` conversation. Every one.

No exceptions, no shortcuts, no "I'll land it later." Later is how production code
ends up full of spike hacks.

---

## MemPalace integration

Both Toss and Keep write to MemPalace. This is where Workshop compounds over time —
the library of learnings and personal tools becomes the solo's actual knowledge base.

Promote does not write to MemPalace directly — SBF's product-continuity takes over
from there.
