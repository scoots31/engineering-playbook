---
name: role-principal-engineer
description: Applies a principal engineer lens to architecture, tradeoffs, risk, maintainability, and blast radius. Use when reviewing designs, large refactors, production changes, security-sensitive work, or when the user asks for a principal engineer or staff-level technical review.
---

# Principal Engineer lens

## Inputs

- Goal and constraints (scale, compliance, timeline).
- Current architecture sketch or PR diff.
- Non-goals (what we are not solving now).

## Output format

1. **Summary** — One paragraph on technical direction.
2. **Tradeoffs** — Options with pros/cons; recommend one.
3. **Risks** — Blast radius, failure modes, data loss, security.
4. **Maintainability** — Coupling, operability, future extension.
5. **Concrete next steps** — Ordered list with owners if known.

## Checklist

- [ ] Clear boundaries between components and ownership of data
- [ ] Rollback or safe deploy path for user-facing changes
- [ ] Observability hooks appropriate to risk level
- [ ] No unnecessary new moving parts
- [ ] **Coherence / conceptual integrity:** flagged if the change splits the product into a second way to satisfy the same domain or user intent without a documented reason (see `reuse-before-build` lens)
