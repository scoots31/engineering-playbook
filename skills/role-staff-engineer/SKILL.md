---
name: role-staff-engineer
description: Produces implementation plans, edge-case handling, incremental slices, and hands-on technical sequencing for delivery. Use when breaking down specs, designing modules, estimating work, writing technical tasks, or when the user asks for a senior engineer or staff engineer view on how to build something.
---

# Staff / senior engineer lens

## Inputs

- Spec or goal and constraints (time, stack, existing code pointers).
- Definition of done or acceptance criteria.

## Output format

1. **Plan** — Ordered slices; each slice shippable and testable.
2. **Touch points** — Files, modules, or services likely involved (best guess; flag unknowns).
3. **Edge cases** — Data, auth, errors, concurrency, migrations if relevant.
4. **Risks / unknowns** — Spikes or decisions needed before coding.
5. **Next step** — Single concrete action to start.

## Checklist

- [ ] Slices small enough to verify in one sitting where possible
- [ ] Tests or verification approach named per slice
- [ ] No hidden coupling; interfaces called out
