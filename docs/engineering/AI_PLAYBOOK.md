# AI delivery playbook

Single source of truth for **how** work runs. Product facts (PRDs, ADRs, runbooks) usually live in the **product** repository; this file defines stages, roles, and handoffs so Cursor and Claude Code stay aligned.

## Principles

1. **One driver per task** — Either Cursor or Claude Code leads a slice; do not edit the same branch blindly in parallel without a handoff.
2. **Small vertical slices** — Ship thin end-to-end increments with tests and rollback in mind.
3. **Written handoffs** — When switching tools or sessions, update `HANDOFF.md` (see `HANDOFF.template.md`).
4. **Pin the playbook** — If the product uses a `playbook/` submodule, it pins a specific commit; upgrade when you choose. (Global playbook mode skips this.)
5. **One source of truth per concept** — Do not accumulate parallel implementations for the same domain rule or the same user intent (e.g. one mileage/route calculator, one pattern for “process this request” buttons—shared look **and** shared code path unless the product spec deliberately splits them).

## Reuse, consistency, and shared primitives

This is **build and design discipline**, not a separate product phase. Apply it during **Design** and **Develop** (and catch violations in **Test** / **Review**).

| Rule | What it means |
|------|----------------|
| **Search before add** | Before writing new logic or UI for an existing capability, search the repo for prior art (same domain words, similar screens, existing utilities). |
| **Extend or extract** | Prefer extending a module or extracting a shared helper/component over copy-paste “second way.” |
| **Same intent → same contract** | If two flows mean the same thing to the user (submit, confirm, calculate, export…), they should share behavior and presentation unless UX explicitly requires a difference—and then document why. |
| **Document intentional forks** | If two paths must differ, add a short comment or ADR so the next session does not “unify” them by accident. |

**Where it lives in tooling:** playbook principle above + **`reuse-before-build` skill** (checklist). **Principal Engineer** and **Staff Engineer** skills should call out duplication risk during review and implementation planning. Optional **project** `.cursor/rules` can add stack-specific patterns (e.g. “all distance math lives in `geo/`”).

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
| **Reuse / consistency** (skill, not a persona) | `reuse-before-build` — search before add; one implementation per domain concept; shared UI patterns for the same intent |

## Files to keep fresh in the product repo

- `HANDOFF.md` — only when mid-flight handoff is needed; otherwise optional.
- Product-specific `docs/` or your team’s usual locations for PRDs and ADRs.

## Updating this playbook

Change this repository, tag a release, then bump the `playbook/` submodule in each product when ready.
