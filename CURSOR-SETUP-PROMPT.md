# Cursor Setup Prompt — First Session on a New Machine

_Use this when you've cloned the repo but haven't pasted the User Rules yet._

---

## How to use

On a fresh machine with the repo cloned, open the project in Cursor and paste the message below into the chat. It tells Cursor everything it needs to operate the framework for this session and reminds you to set up User Rules for persistence.

---

## Paste this into Cursor chat

```
I've cloned the Solo Builder Framework repo. I don't have the User Rules pasted yet — we'll fix that shortly, but for now, please read the following files so you understand the framework for this session:

1. README.md — what this is and how it's organized
2. skills/start/SKILL.md — how to route new projects (includes Workshop pre-check)
3. workshop/README.md — the companion framework for spikes and tools
4. skills/process-mapper/SKILL.md — the always-on process contract
5. skills/product-continuity/SKILL.md — always-on session memory
6. skills/framework-health/SKILL.md — always-on signal monitor
7. skills/retrospective/SKILL.md — always-on improvement capture

After reading, confirm you understand:
- The 4 always-on skills and when they activate (SBF only — Workshop has none)
- The phase routing (start → discover → design-sprint → etc.)
- The Workshop companion — spike-shaped openings route to `workshop/scope-check/SKILL.md`, not Discover
- The four required anchors before any slice can be Ready
- The process contract (to-be map held across all phases)

Then treat this session as if the User Rules were active. When I start describing a project, route it correctly.

**Reminder for me:** After this session, paste the portable User Rules into Cursor → Settings → Rules → User rules. The template is in `templates/cursor-user-rules-global-playbook.md` — replace `[PLAYBOOK_ROOT]` with the output of `pwd` run from the repo root.
```

---

## What this accomplishes

- Cursor reads the framework files and adopts the skill routing for the session
- You can start work immediately without waiting for User Rules to be configured
- The reminder at the bottom ensures User Rules get set up for all future sessions

## Making it permanent

Once User Rules are configured, you won't need this prompt — the rules load automatically on every conversation. One-time setup per machine.
