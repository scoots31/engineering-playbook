---
name: enhancement
description: Add a small feature or improvement to an existing production application. Uses existing design, context, and patterns — not a new phase of work. Lite QA, minimal footprint, deploy. If the change needs new design screens or a new process flow, route to SBF design-review instead.
---

# Enhancement

*Extend what exists. Don't reinvent it.*

**Core question:** "What's the smallest change that adds this capability while fitting naturally into what's already there?"

An enhancement is a contained addition to a working product — a new field, a new filter, a small UI improvement, a new configuration option. It is not a new feature phase. If the change requires new design screens, a new process flow, or more than a few hours of build time, route to SBF design-review instead.

---

## Step 1 — Read Existing Context

Before building anything, read what already exists.

- `docs/backlog.md` — what's already built, what's deferred
- `docs/design/` — the existing screens this touches
- `docs/process/to-be-[name].md` — the process flow this fits into
- The relevant code — what patterns are already in use

**Coherence check:** Does the codebase already express this pattern somewhere? Extend it — don't create a parallel solution.

> "This fits alongside [existing thing]. I'll extend [specific location] rather than creating something new."

---

## Step 2 — Scope the Change

State the enhancement in one sentence. If it takes more than one sentence, it may be more than one enhancement — or a new SBF phase.

Confirm:
- Which screen(s) it touches
- Which data fields it needs (existing or new)
- What done looks like — 1-2 specific, verifiable criteria
- What it explicitly does NOT change (the scope boundary)

---

## Step 3 — Build

- Create a feature branch: `enhancement/[short-description]`
- Build against the existing design — open the design file, don't work from memory
- Pull from existing data sources — don't hardcode
- Match existing code patterns — coherence over cleverness
- Touch only what the scope requires

---

## Step 4 — Lite QA

Not the full solo-qa chain. A targeted verification:

- Does the enhancement do what was described?
- Does it render and behave correctly?
- Did it break anything adjacent? Manually check the screens it touches.
- Solo confirms in browser — same standard as solo-qa Part 2, scoped to this change

---

## Step 5 — Deploy

Follow the existing deploy path from `docs/tech-context.md`.

- Commit message: `enhancement: [what was added]`
- Deploy alone — do not bundle with bug fixes or other changes
- Verify in production

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Building without reading existing context | Creates duplicates, breaks patterns | Read the design and code first |
| Scope creep mid-build | Enhancement becomes a phase | State scope in Step 2, hold the line |
| Skipping lite QA | "It looked fine locally" | Verify in the actual environment |
| Bundling with bug fixes or other work | Can't isolate problems | Deploy separately |
| Enhancement that needs new design screens | This is a new SBF phase | Route to design-review instead |
