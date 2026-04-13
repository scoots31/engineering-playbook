# AI delivery playbook

Single source of truth for **how** work runs. Product facts (PRDs, ADRs, runbooks) usually live in the **product** repository; this file defines stages, roles, and handoffs so Cursor and Claude Code stay aligned.

## Principles

1. **One driver per task** — Either Cursor or Claude Code leads a slice; do not edit the same branch blindly in parallel without a handoff.
2. **Small vertical slices** — Ship thin end-to-end increments with tests and rollback in mind.
3. **Written handoffs** — When switching tools or sessions, update `HANDOFF.md` (see `HANDOFF.template.md`).
4. **Pin the playbook** — If the product uses a `playbook/` submodule, it pins a specific commit; upgrade when you choose. (Global playbook mode skips this.)
5. **Coherence — one product, one story (guide, not gate)** — *Prefer* that the app feel like **one intentional system**: similar problems tend toward **similar patterns** in design and **shared homes** in code. When the product **deliberately** does something differently, that is fine—**say it out loud** (brief comment, note, or ADR) so later work does not “fix” it back to sameness by accident. Speed and learning still matter; this principle **nudges**, it does not veto Scott’s calls.

## Coherence (design + implementation mindset)

This is a **stance to steer by**, not a compliance checklist. It is **conceptual integrity** in the small: what the product *means* and *does* **tends to align** across screens and modules because you **look for the existing story** before writing a new one. When a one-off is the right call, **make that choice consciously**—no need to force abstraction on day one.

**Gentle implications (use judgment):**

- **Design:** recurring problems *often* deserve recurring patterns; **designed** exceptions beat accidental drift.
- **Implementation:** *usually* worth asking whether this feature **extends** something that already exists before starting a parallel path—then choose what fits the slice.
- **Review:** a useful question is “does this match how we already treat this *class* of thing?”—not a merge blocker by itself, a **quality bar** you dial up over time.

**When:** mostly **Design** and **Develop**; notice it in **Test** / **Review** when something feels off.

**How tools support it:** Principle (5); **Principal** and **Staff** lenses can **raise** coherence tradeoffs; the **`reuse-before-build`** skill is a **short reminder** of questions to ask—**optional to load**, never a substitute for Scott’s priorities. Stack-specific detail stays in **project** rules or product docs.

## Stages (gates)

| Stage | Outcome | Typical “role” skills |
|-------|---------|------------------------|
| **Plan** | Problem, constraints, success metrics, out of scope | PM, Product |
| **Design** | UX acceptance criteria + technical approach | UX, Principal Engineer |
| **Develop** | Implementation matching design, ADRs only when needed | Staff / Senior Engineer |
| **Test** | Automated + exploratory + data/migration risks | QA |
| **Deploy** | Checklist, monitoring, rollback | Ops + Principal Engineer (blast radius) |

**Minimum bar before merge (user-facing change):** test plan bullets + rollback or feature-flag story.

## Roles (how to invoke)

Roles are not separate people—they are **lenses**. In Cursor, use matching **skills** from `playbook/skills/` (installed per `integrate-cursor.md`). In Claude Code, paste the role section or ask the model to adopt that lens and output format.

| Role | Lens |
|------|------|
| **Principal Engineer** | Architecture, tradeoffs, risk, maintainability, blast radius |
| **Senior / Staff Engineer** | Execution plan, edge cases, incremental rollout |
| **Project Manager** | Scope, sequencing, dependencies, schedule risks |
| **UX** | Flows, states, empty/error/loading, accessibility acceptance criteria |
| **QA** | Test strategy, cases, exploratory charters, release gate |
| **Product** | Problem statement, metrics, rollout, analytics |
| **Coherence** (mindset; optional lens) | `reuse-before-build` — gentle questions before building; Scott overrides when speed or exploration wins |

## Files to keep fresh in the product repo

- `HANDOFF.md` — only when mid-flight handoff is needed; otherwise optional.
- Product-specific `docs/` or your team’s usual locations for PRDs and ADRs.

## Updating this playbook

Change this repository, tag a release, then bump the `playbook/` submodule in each product when ready.
