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

## Step 1: Check for Existing Context

Before reading what the person brought in, scan for project context:

- `BLUEPRINT.md` — project is in flight, continue from there
- `docs/discovery-brief.md` — discovery is done, check if design sprint is next
- `docs/design/` — design exists, check if planning is next
- Active GitHub issues or sprint — in build phase, continue

If any of these exist, do not run the routing logic. Orient to the current state and continue.

---

## Step 2: Read What They Brought

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
├── Existing context found → orient and continue, don't restart
│
└── No existing context
    ├── Clear idea (Shape A) → Discover
    ├── Exploratory (Shape B) → Brainstorm  
    └── Ambiguous (Shape C) → one question → route
```

---

## What Never Happens Here

- No explanation of the framework or its phases
- No asking what phase they want to be in
- No list of options ("Would you like to brainstorm, discover, or plan?")
- No re-routing mid-conversation based on the process — only based on what's actually needed
- No announcing which skill is being invoked
