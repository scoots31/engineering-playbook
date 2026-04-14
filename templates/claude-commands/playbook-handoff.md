# Engineering playbook — Handoff

Resolve the playbook root: use environment variable `ENGINEERING_PLAYBOOK` if set and non-empty; otherwise `$HOME/Developer/engineering-playbook`.

Prepare or update a **session/tool handoff** so another session (or Cursor) can continue without re-deriving state.

1. Read `docs/engineering/HANDOFF.template.md` at the playbook root.
2. In the **current product repo**, produce content suitable for `HANDOFF.md` (repo root): goal, done, next, commands, branches, risks, pointers to files. If the user keeps `HANDOFF.md` local-only, output the same structure for them to paste.
3. Remind: one driver per task—note who/what should **lead** the next slice (Claude Code vs Cursor).

**Output:** A filled handoff block ready to save as `HANDOFF.md` or to paste into the other tool’s chat.
