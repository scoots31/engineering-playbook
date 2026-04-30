---
name: start
description: The front door to the solo builder framework. Reads what the person brought into the conversation and routes them to the right starting point — Brainstorm or Discover — without making them think about which phase they're in. Fires automatically via CLAUDE.md and Cursor rules when a new project or feature conversation begins. Never fires mid-build, mid-QA, or when existing project context already exists.
---

# Start

*The entry point. The user just talks. This figures out where they are and where to begin.*

**Core question:** "Is this idea clear enough to tell its story, or does it need thinking through first?"

The user never sees this skill working. They open Claude or Cursor, describe what's on their mind, and the conversation begins in the right place. No phase announcements. No process explanation. Just a partner who reads the room and starts from the right spot.

---

## When This Fires

This skill fires automatically — via CLAUDE.md rule (Claude Code) and Cursor rules (Cursor) — when ALL of the following are true:

- The conversation is new or the opening message describes a project or feature idea
- No existing project context is found (`BLUEPRINT.md`, `docs/discovery-brief.md`, active sprint, open issues being discussed)
- The user hasn't already explicitly invoked another skill

**It does NOT fire when:**
- The project is mid-build and the user is continuing existing work
- An existing discovery brief or blueprint is already in place
- The conversation is about a specific bug, task, or question in an ongoing build
- Another skill is already active

If context already exists — read it, orient to where the project is, and continue from there. Don't restart the process.

---

## Named Project Resume

If the opening message contains "guided on [name]", "/guided [name]", "resume [name]", or "pick up [name]":

1. Read `[PLAYBOOK_ROOT]/projects.md` — find the row matching the name (case-insensitive)
2. If found: read `[path]/docs/continuity/handoff.md` — orient in one sentence, close with direct action prompt. Do not run routing logic.
3. If not found: stop. "I don't have [name] in the projects registry. What's the path to that project?" — add the entry, then resume.

> "Picking up [project] — [one sentence on current state from handoff]. Ready to start [unit of work X]? Say go."

---

## Step 1: Check for Existing Context

Before reading what the person brought in, scan for project context:

- `BLUEPRINT.md` — project is in flight, continue from there
- `docs/discovery-brief.md` — discovery is done, check if design sprint is next
- `docs/design/` — design exists, check if planning is next
- Active GitHub issues or sprint — in build phase, continue

If any of these exist, do not run the routing logic. Orient to the current state and continue.

**Resume pattern:** If the opening message contains "Resuming [project]" or similar resume-pattern language AND `docs/continuity/handoff.md` exists — skip routing entirely. Read the handoff, orient from it in one sentence, and continue. Do not re-run routing logic. Do not ask what phase they're in.

> "Picking up from [where handoff says] — [one sentence on current state]. Let's go."

**Deployed project, new work:** If existing context is found AND all phase records in `docs/backlog.md` are at `Deployed` status — do not continue the old work. Route to the new cycle protocol below. A deployed project with new work is not a resume — it is a new cycle starting from a stable foundation.

---

## Step 2: Read What They Brought

Before classifying into Shape A/B/C, check for **existing-project shape** — work that belongs in `onboard`, not the new-project routing chain.

**Existing-project shape signals:**
- "I have prior work on [project]", "I've been working on [project] outside the framework"
- "I want to bring [project] into the framework"
- "I want to pick up [project] and start using the framework"
- A file path is mentioned with no framework context found in that directory

If the opening is existing-project shaped, route to `onboard`. Do not run Shape A/B/C routing.

---

Before classifying into Shape A/B/C, also check for **spike-shape** — work that belongs in the Workshop companion framework, not the main build flow.

**Spike-shape signals:**
- "Let me try...", "quick script to...", "see if I can...", "one-shot to...", "I'm curious about..."
- Short time horizon implied (hours to days, not weeks)
- No mention of users other than the solo
- "Just want to explore" / "just a test"
- Personal tool / utility language ("a little tool for me that...")

If the opening is spike-shaped, hand off to `scope-check` instead of continuing. Do not announce the handoff — just run `scope-check`'s one question.

If the opening is unambiguously product-shaped (users, indefinite lifespan, meaningful scope), continue with Shape A/B/C classification below.

If ambiguous between spike and product, ask one question: *"Is this something you're trying out for yourself, or something you want other people to use?"* Route based on the answer.

---

The opening message almost always falls into one of three shapes:

**Shape A — Clear idea**
They know what they want to build. The who, the what, and roughly the value are present, even if not perfectly articulated. Signals:
- "I want to build X that does Y for Z"
- "I need a tool that..."
- They've built something similar and know the shape
- The description has enough specificity to start asking story questions

**Shape B — Exploratory**
They're thinking out loud. The idea is a direction, a capability, a "what if." Signals:
- "I've been thinking about..."
- "What if we could..."
- A question more than a description
- Uncertain about who it's for or what it actually does
- Multiple possibilities being held at once

**Shape C — Ambiguous**
Could be either. Not enough signal to call it.

---

## Step 3: Route

**Shape A → Discover**
Say something like: *"That's clear enough to work with — let me ask a few questions to build the full picture before we get to design."* Then run the `discover` skill. Don't explain the framework. Don't announce phases. Just start the conversation.

**Shape B → Brainstorm**
Say something like: *"Sounds like the idea is still taking shape — let's think through it together."* Then run the `brainstorming` skill. Same rule — no framework explanation, no phase announcement. Just engage with the idea.

**Shape C → One question**
Ask the one question that resolves it: *"Do you have a clear picture of what you want to build, or are you still working through the idea?"* Route based on the answer.

---

## The Tone of the Routing

This is not a system announcement. The user should not feel like they just got processed.

**Not this:**
> "I'll now begin the Discovery phase of the Solo Builder Framework. This phase consists of four zones..."

**This:**
> "That's clear enough to start from — let me ask a few things to get the full picture."

Or:
> "Sounds like the idea is still forming. Let's think it through before we try to articulate it."

One sentence. Warm. Then just start. The framework is invisible.

---

## Routing Summary

```
New conversation opens
│
├── Existing framework context found
│   ├── Active phases in progress → orient and continue, don't restart
│   └── All phases at Deployed status → new cycle protocol
│
├── Resume prompt found + handoff.md exists → orient from handoff, skip routing
│
└── No existing context
    ├── Existing-project shape → `onboard`
    ├── Spike-shape → Workshop `scope-check`
    └── Product-shape (or ambiguous resolved to product)
        ├── Clear idea (Shape A) → Discover
        ├── Exploratory (Shape B) → Brainstorm
        └── Ambiguous (Shape C) → one question → route
```

---

## Deployed Project — New Cycle

When a project is found at Deployed status and new work is being discussed, do not
re-run discovery, do not recreate docs, do not touch existing phase records.
Everything that was built stays exactly as it is — Phase 1 (or the most recent deployed
phase) is complete and its record is read-only. The new cycle adds on top of it.

**Step 1 — Orient on what was shipped**
Read `docs/backlog.md` phase summary and `docs/continuity/handoff.md`. One sentence:
what the product does and what was built in the last deployed phase.

**Step 2 — Understand the new work**
If not already described in the opening message, ask one question:
*"What are you adding?"*

**Step 3 — Scope to the right starting point**
Based on what's described:
- New capability or new user journey → route to `discover`
- Defined new screens with known requirements → route to `design-review` with new slices
- Small bounded addition (one feature, one screen) → route to `enhancement`
- Bug or regression → route to `bug-fix`

The routing is invisible. One sentence of orientation, then start the appropriate skill.

**Step 4 — Open a new phase in the existing backlog**
Before routing: add a new Phase record to `docs/backlog.md`.
- Name: Phase 2 (or Phase N continuing the sequence)
- Status: Planning
- Do not modify any existing phase records — deployed phases are read-only from here

**Step 5 — Update the handoff**
Rewrite `docs/continuity/handoff.md` to reflect the new cycle: previous phase complete,
new phase starting, where to begin.

**Step 6 — Orient and proceed**
> "[Project] Phase [N-1] is live. Adding [one sentence on new work]. [Next move]."

Then start. Nothing more.

---

## What Never Happens Here

- No explanation of the framework or its phases
- No asking what phase they want to be in
- No list of options ("Would you like to brainstorm, discover, or plan?")
- No re-routing mid-conversation based on the process — only based on what's actually needed
- No announcing which skill is being invoked
