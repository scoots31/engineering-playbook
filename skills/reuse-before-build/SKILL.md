---
name: reuse-before-build
description: Guides toward conceptual integrity and coherent design plus implementation—prefer extending one product story over silent parallel solutions. Use when adding or changing features, UI, or domain logic; when the user wants consistency or a design-system mindset; or as a voluntary lens when work might duplicate existing behavior. Scott can always override for speed or experimentation.
---

# Coherence — design and implementation (guide)

**This file guides judgment; it does not handcuff.** If Scott wants to ship a spike, try two approaches, or defer unification, that is valid—just **name the tradeoff** so the next session is not fooled into thinking the divergence was an oversight.

## Lens

Would a thoughtful user or maintainer see **one product**, or unrelated pieces? **Prefer** extending the vocabulary the codebase already uses for this *class* of problem—unless you have a **reason** not to, in which case a line of context is enough.

## Light prompts (use as fits)

- What *kind* of thing is this (calculation, primary action, list, error, …)?
- Does the repo already express that kind somewhere worth building on?
- Are we **extending**, **extracting a small shared spine**, **shipping a deliberate one-off**, or **documenting a fork**?

## When answering Scott

Offer a **short coherence note**: what pattern you built on, what you left separate on purpose, and anything worth revisiting later—**without** blocking the slice if he wants to move.

## Optional reflection

- [ ] (Optional) I considered how this slice fits the wider product story—not a requirement to check every time.
