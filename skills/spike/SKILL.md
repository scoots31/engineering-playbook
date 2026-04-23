---
name: spike
description: The Workshop execution skill. Timeboxed exploratory work with a single artifact and a running journal of what was tried and what happened.
---

# Workshop — Spike

*The work itself. One outcome, one artifact, one running journal.*

**Core stance:** outcome-first, not process-first. No gates, no anchors, no phases.
Just the work and a record of it.

---

## The frame carried in from scope-check

- Shape (spike or tool)
- Outcome (the question or the thing to make work)
- Timebox or scope
- Graduation triggers

If any of these are missing, stop and run `scope-check` first. Don't spike into
the void.

---

## The running journal

A single file — `spike-journal.md` next to the work — with dated entries as things
happen:

- What was tried
- What happened (including what broke)
- What surprised
- What the current best guess is

The journal is the primary artifact besides the code. It is what gets mined at
`land` time. It is not a process map. It is not documentation. It is a narrative
of the attempt, written as it happens.

---

## Hygiene during the spike

- **Single file bias** — keep the work in as few files as possible. Sprawl during
  a spike is a signal something has changed.
- **No tests during the spike.** If you want tests, you've probably left spike
  territory.
- **No abstractions.** Hardcode values. Inline everything. Abstractions are for
  things that live.
- **No README yet.** The journal is the README for now.

---

## Timebox enforcement

When the timebox is up:
- Outcome reached → `land` with Keep or Toss decision
- Outcome *almost* reached → one extension allowed (max: 50% of original timebox).
  After that, `land` regardless. Extensions beyond that are a signal it's not a spike.
- Outcome unreachable → `land` with Toss, capture the learning

---

## Graduation triggers — watch for them

Any of these mid-spike means pause and reconsider:
- "Can I share this with X?"
- "Should I add auth?"
- "Someone else wants to use this"
- The work is growing past its timebox for the third time
- You're adding a second file because the first got too long

When a graduation trigger fires, stop spiking. Run `land` with Promote intent.

---

## What spike does not do

- Does not produce a design artifact (no UI to design, or the UI is the code)
- Does not map a process (there isn't one yet)
- Does not set up CI, tests, deploy, or any other infrastructure
- Does not invoke SBF's always-on skills — process-mapper, product-continuity,
  framework-health, retrospective are sized for bigger work

---

## Output

The work (code / notebook / script) + the spike journal. Handed to `land`.
