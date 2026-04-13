# AI delivery playbook

Single source of truth for **how** work runs. Product facts (PRDs, ADRs, runbooks) usually live in the **product** repository; this file defines stages, roles, and handoffs so Cursor and Claude Code stay aligned.

## Principles

1. **One driver per task** — Either Cursor or Claude Code leads a slice; do not edit the same branch blindly in parallel without a handoff.
2. **Small vertical slices** — Ship thin end-to-end increments with tests and rollback in mind.
3. **Written handoffs** — When switching tools or sessions, update `HANDOFF.md` (see `HANDOFF.template.md`).
4. **Pin the playbook** — If the product uses a `playbook/` submodule, it pins a specific commit; upgrade when you choose. (Global playbook mode skips this.)
5. **Coherence — one product, one story** — The app should feel like **one intentional system**, not a pile of one-off decisions. The same ideas (rules, flows, visual language, “how we do X”) should resolve to **shared meaning** in design and **shared implementation** in code unless the product deliberately draws a line—and then that line is explicit.

## Coherence (design + implementation mindset)

This is a **stance**, not a checklist of widgets. It is **conceptual integrity**: what the product *means* and *does* stays aligned across screens, modules, and sessions. New work should **extend the story** the codebase already tells, not start a parallel story because a session forgot to look.

**What it implies (practice follows from the mindset):**

- **Design:** recurring user problems get recurring patterns (language, layout, affordances). Exceptions are **designed**, not accidental.
- **Implementation:** domain behavior and cross-cutting UX live in **clear homes**; new features **plug in** or **generalize** what exists before inventing a second engine for the same job.
- **Review:** ask “does this match how we already do this class of thing?” before merge. Drift is a bug.

**When:** continuously in **Design** and **Develop**; visible in **Test** and **Review** when things feel inconsistent or duplicated.

**How tools support it:** Principle (5) above; **Principal** and **Staff** lenses surface coherence risk; the **`reuse-before-build`** skill is a **compact reminder** of how that mindset turns into concrete questions in a given repo (search, extend, document real exceptions). Stack-specific conventions belong in **project** `.cursor/rules` or product docs—not in a generic playbook.

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
| **Coherence** (mindset; skill is a shorthand) | `reuse-before-build` — turn “one product, one story” into repo-specific questions before building |

## Files to keep fresh in the product repo

- `HANDOFF.md` — only when mid-flight handoff is needed; otherwise optional.
- Product-specific `docs/` or your team’s usual locations for PRDs and ADRs.

## Updating this playbook

Change this repository, tag a release, then bump the `playbook/` submodule in each product when ready.
