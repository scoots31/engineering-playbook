---
name: dependency-upgrade
description: Safely update project dependencies — audit what's outdated, check for breaking changes, update methodically one at a time, test, deploy. Use for routine upgrades, security-flagged packages, or compatibility requirements.
---

# Dependency Upgrade

*Update methodically. One at a time. Verify before shipping.*

**Core question:** "What needs to update, why, and what's the safest path to get there without breaking the running system?"

---

## Step 1 — Audit

Read `docs/tech-context.md` for the stack, then inventory the current state using the appropriate tool for the stack (e.g. `npm audit`, `pip list --outdated`, `bundle outdated`).

Produce a prioritized list:
```
🔴 Security flagged: [package] [current] → [target]
🟡 Major (breaking changes likely): [package] [current] → [target]
🟢 Minor/patch (safe): [package] [current] → [target]
```

Security-flagged packages always go first, regardless of complexity.

---

## Step 2 — Check Breaking Changes

For every major version update, read the changelog before touching anything.

- What changed between current and target?
- Are there API changes that affect this codebase?
- Are there config changes required?
- Are there peer dependency requirements?

Do not upgrade a major version without reading the migration guide. "It's probably fine" is how production breaks.

---

## Step 3 — Update Methodically

Update one dependency at a time (or one logical group for tightly coupled packages). After each update:

1. Verify the app still starts
2. Run existing tests if they exist
3. Smoke test the critical paths this package touches

Do not batch all updates in one commit. Isolation means you know exactly what broke if something breaks.

Commit after each successful update:
`deps: upgrade [package] [old-version] → [new-version]`

---

## Step 4 — Verify

After all planned updates are complete:

- Full smoke test of the application's critical paths
- Check anything that touched a dependency with breaking changes
- Verify no unresolved peer dependency warnings remain

---

## Step 5 — Deploy

Follow the deploy path from `docs/tech-context.md`.

- Deploy during low-traffic periods when possible
- Know the rollback path before deploying — how to revert to the previous lockfile if needed
- Verify in production that the application is running correctly after deploy

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Upgrading everything at once | Can't isolate what broke | One at a time |
| Skipping the changelog on major versions | Breaking change blindsides you | Read it before upgrading |
| Not verifying in production | Different environments, different failures | Confirm in production after deploy |
| Deferring security-flagged packages | Known vulnerability stays in production | Security flags go first |
| Upgrading during high-traffic periods | Higher blast radius if something breaks | Low-traffic windows when possible |
| No rollback plan | Stuck if deploy goes wrong | Know how to revert before you start |
