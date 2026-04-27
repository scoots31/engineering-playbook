# Claude Code Setup — First Session on a New Machine

_Use this only if you haven't run the full install yet. After the install, this file is not needed._

---

## Normal install (recommended)

Tell Claude Code:

```
Read ~/Developer/engineering-playbook/INSTALL.md and follow the instructions.
```

Claude will write the framework block to `~/.claude/CLAUDE.md` and output the Cursor User Rules for you to paste. One step, fully automated.

---

## Session-only primer (if you need to work before installing)

If you're not ready to install yet, paste the message below into Claude Code to prime the framework for this session only. It won't persist — you'll need to run the full install before your next session.

```
I've cloned the Solo Builder Framework repo to ~/Developer/engineering-playbook (adjust if different).
I haven't run the install yet — for now, please read the following files so you understand the
framework for this session:

1. ~/Developer/engineering-playbook/README.md — what this is and how it's organized
2. ~/Developer/engineering-playbook/skills/start/SKILL.md — how to route new projects

The session mode model: default is bare. Say "guided mode" to engage the full phase chain and
always-on skills. Say "piloted mode" to load always-on skills and invoke phases manually.

Treat this session as if the install had been run. When I start describing a project, route correctly.
```
