---
name: reuse-before-build
description: Requires searching for existing implementations and shared UI or domain modules before adding parallel solutions. Use when adding features, new screens, calculations, API clients, or buttons that might duplicate behavior elsewhere; when the user asks for consistency, DRY, shared components, or a single source of truth; or before implementing domain logic that may already exist.
---

# Reuse before build

## Before writing new code

1. **Search the codebase** (symbols, filenames, prior features) for the same domain concept or very similar UX (e.g. “distance”, “mileage”, “route”, “submit”, “primary action button”).
2. **If something exists** — extend it, parameterize it, or extract a shared module/component used by both call sites. **Do not** add a second independent implementation unless the user explicitly approves a fork.
3. **If nothing exists** — implement once in a clear home (folder/module naming matches domain); note in PR/summary where future similar work should plug in.

## UX consistency

- Same **user intent** (e.g. “process my request”, “confirm destructive action”) → same **interaction pattern** and **visual role** (primary vs secondary), unless the spec documents an intentional exception.
- New screens reuse existing button, form, layout, and loading/error primitives when the stack has them.

## Output when advising Scott

- **Found:** list existing symbols/paths to reuse.
- **Gap:** what is missing and the smallest addition to make reuse possible.
- **Risk:** where duplication would hurt (bugs, drift, partial fixes).

## Checklist

- [ ] Searched for prior implementation of this domain rule or pattern
- [ ] Chosen extend/extract over copy-paste
- [ ] Intentional differences (if any) are explicit in code comment or doc
