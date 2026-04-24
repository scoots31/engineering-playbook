# Claude Code Setup Prompt — First Session on a New Machine

_Use this when you've cloned the repo but haven't added the playbook block to `~/.claude/CLAUDE.md` yet._

---

## How to use

On a fresh machine with the repo cloned, open any project in Claude Code and paste the message below. It tells Claude Code everything it needs to operate the framework for this session and reminds you to make the setup permanent via `~/.claude/CLAUDE.md`.

---

## Paste this into Claude Code

```
I've cloned the Solo Builder Framework repo to ~/Developer/engineering-playbook (adjust if different). I haven't added the playbook block to ~/.claude/CLAUDE.md yet — we'll fix that shortly, but for now, please read the following files so you understand the framework for this session:

1. ~/Developer/engineering-playbook/README.md — what this is and how it's organized
2. ~/Developer/engineering-playbook/skills/start/SKILL.md — how to route new projects (includes Workshop pre-check)
3. ~/Developer/engineering-playbook/workshop/README.md — the companion framework for spikes and tools
4. The session mode model: default is bare (no routing, no always-on). Say "auto-pilot mode" to engage the full phase chain and always-on skills. Say "assisted mode" to load always-on skills and invoke phases manually.

After reading, confirm you understand:
- The 3 session modes: bare (default), assisted, auto-pilot — and what each activates
- The phase routing (start → discover → design-sprint → etc.)
- The Workshop companion — spike-shaped openings route to workshop/scope-check/SKILL.md, not Discover
- The four required anchors before any slice can be Ready
- The process contract (to-be map held across all phases)
- The `nivya` companion skill — on-demand recall and explanation. I can invoke it with `/nivya` and then address her by name ("Nivya, what did we decide about X?"). She never captures, decides, or builds; she routes to framework skills only with my explicit consent.

Then treat this session as if the playbook block in ~/.claude/CLAUDE.md were active. When I start describing a project, route it correctly.

**Reminder for me:** After this session, add the playbook block to `~/.claude/CLAUDE.md` so future sessions activate the framework automatically. The snippet is in `README.md` under "Claude Code → Step 2".
```

---

## What this accomplishes

- Claude Code reads the framework files and adopts the skill routing for the session
- You can start work immediately without waiting for the global `CLAUDE.md` block to be in place
- The reminder at the bottom ensures `~/.claude/CLAUDE.md` gets updated for all future sessions

## Making it permanent

Once the playbook block is in `~/.claude/CLAUDE.md`, you won't need this prompt — the framework loads automatically on every Claude Code session. One-time setup per machine.
