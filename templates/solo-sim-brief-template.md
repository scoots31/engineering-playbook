# Solo Simulator Brief
*Version: [auto-assigned on confirmation] — [date]*

---

## Section 1: Project Identity

**Project Name:**
> What is this product called?

**Run Type:**
> Choose one: `Full framework run` | `Single-phase test` | `Slice test`
> Full framework run = Discovery through Phase Test. Single-phase = one named phase only. Slice test = one or more named slices only.

**Phases in Scope:**
> List the phases this run covers. Example: Discovery, Design Sprint, Build Phase 1, Phase Test.
> For full framework runs, write: All phases.

---

## Section 2: Problem and Purpose

**Problem Statement:**
> One or two sentences. What problem does this product solve, and for whom?
> Bad: "A gift tracker app." Good: "People consistently forget gift occasions or buy last-minute, low-effort gifts. This solves the planning and tracking problem so thoughtful gifting becomes a habit, not a scramble."

**Who Uses It:**
> Who is the end user? Include any relevant context about their situation, constraints, or habits that should shape product decisions.

**Why This Matters:** *(optional)*
> Why is solving this worth the effort? What changes for the user when this works well?

---

## Section 3: Definition of Good

**What Good Looks Like:**
> Write 2–4 specific statements. These are the primary criteria the simulator uses to approve decisions.
> Each statement should be observable — something you could confirm by looking at the running product.
> Example: "The user can add a gift occasion in under 30 seconds." Not: "It should be easy to use."

1.
2.
3.
4. *(optional)*

**What Done Means:**
> What specific, observable conditions confirm this product is complete?
> These close the acceptance review at Phase Test. Write them so a stranger could verify them without explanation.

1.
2.
3.

**Tone / Experience:** *(optional)*
> If the product has a particular feel or character it should have, describe it here.
> Example: "Calm and practical — no gamification, no streaks, no guilt."

---

## Section 4: Drift Watchlist

> These fields drive the simulator's pushback logic. When the build drifts toward any of these, the simulator flags it specifically.

**Push Back On (1) — Required:**
> The first specific thing the simulator should flag if the build moves toward it.
> Bad: "Too complex." Good: "Any screen that requires more than two taps to complete the primary action — this is a quick-capture tool, not a management dashboard."

**Push Back On (2) — Required:**
> Second specific drift trigger.
> Bad: "Scope creep." Good: "Any feature that serves the builder's interest in the data rather than the user's need to act on it — analytics, charts, and export features are out."

**Push Back On (3) — Optional:**
> Third specific drift trigger.
> Bad: "Bad UX." Good: "Any empty state that leaves the user without a clear next action — every empty screen must tell the user exactly what to do first."

**Out of Scope:**
> Explicit list of things that should NOT be built in this run. Anything the simulator sees moving toward this list triggers an automatic pushback.
> Example: "No social features. No recurring reminders. No mobile-specific UI."

---

## Section 5: Run Parameters

**Escalation Behavior:**
> What happens when the simulator pushes back once and the issue is still unresolved?
> Choose one: `Best-call and flag` (default) | `Hold for human`
> Best-call: simulator makes a judgment call, logs it, flags it for review, and keeps the run moving.
> Hold for human: simulator stops and waits. Use only when human is available to respond in real time.

**Human Oversight Mode:**
> How involved is the human during this run?
> Choose one: `Observe only` (default) | `Intervene on escalations` | `Full control`
> Observe only: human can watch the live flag surface but the simulator runs autonomously.
> Intervene on escalations: human is notified on escalations and can override before the run continues.
> Full control: every decision is presented to the human for confirmation. Defeats the purpose of the simulator for most runs.

---

## Confirmation Checklist

Before locking this brief, verify:

- [ ] Problem Statement names a specific user and a specific problem
- [ ] "What Good Looks Like" statements are observable, not aspirational
- [ ] "What Done Means" criteria could be verified by a stranger
- [ ] At least two "Push Back On" triggers are defined
- [ ] Out of Scope list exists (even if short)
- [ ] Escalation Behavior is chosen
- [ ] Human Oversight Mode is chosen

When all boxes are checked, the brief is ready to lock. Once locked, it does not change mid-run.
