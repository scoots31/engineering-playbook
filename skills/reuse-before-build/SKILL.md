---
name: reuse-before-build
description: Upholds conceptual integrity and coherent design plus implementation—one product story, shared patterns for the same intent, avoid parallel one-off solutions. Use when adding or changing features, UI, or domain logic; when the user asks for consistency, a design system mindset, DRY, or single source of truth; or when work risks inventing a second way to do what the app already does.
---

# Coherence — design and implementation

This skill is a **lens**, not a catalog of components. Hold the whole product in view: **would a user or the next maintainer see one coherent system, or unrelated pieces glued together?**

## Mindset

- **Same meaning → same machinery** (unless the spec intentionally splits them—then say so in code or docs).
- **Extend the language of the codebase** before introducing a new dialect for the same idea.
- **Drift is debt** — a second path for the same job will diverge, break under partial fixes, and confuse everyone later.

## How that turns into action (this repo, this task)

Ask briefly:

1. **What class of thing is this?** (calculation, action, form, list, error path, …)
2. **Does the app already “speak” that class somewhere?** Search, read siblings, follow existing patterns.
3. **Are we extending a home, extracting a shared spine, or documenting a deliberate exception?** Avoid silent third options.

## When answering Scott

State in plain terms: how this fits **one product story**, what you reused or generalized, and any **intentional** exception worth recording.

## Minimal check

- [ ] Coherence: one story extended, not a parallel invention sketched only for this screen
