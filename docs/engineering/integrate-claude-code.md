# Integrating this playbook with Claude Code

Assume the product repo has this playbook at **`playbook/`** (git submodule).

## 1. Root instructions file

In the **product** repo root, keep a **short** Claude Code instruction file (name per your Claude Code setup, often `CLAUDE.md`).

Copy the body from `playbook/templates/consumer-claude-root.md` and adjust the repo name and any stack-specific lines.

**Rule:** Do not duplicate the full playbook. Link to `playbook/docs/engineering/AI_PLAYBOOK.md` and stage gates there.

## 2. Same process as Cursor

- Stages and roles are defined in `playbook/docs/engineering/AI_PLAYBOOK.md`.
- Use `playbook/docs/engineering/HANDOFF.template.md` when switching between Claude Code and Cursor.

## 3. Skills / subagents in Claude Code

If Claude Code supports project skills or custom instructions, point them at the same role content under `playbook/skills/*/SKILL.md` (or paste summaries into your root file). Keep one canonical copy in the submodule to avoid drift.

## 4. Submodule reminder

After `git clone`, run `git submodule update --init --recursive` so `playbook/` is populated.
