# Integrating this playbook with Claude Code

Assume the product repo has this playbook at **`playbook/`** (git submodule).

## 1. Where Claude Code reads instructions

Pick **one** primary pattern (or combine: global + a tiny repo pointer).

### A. Repo root file (common default)

In the **product** repo root, keep a **short** Claude Code instruction file (name per your Claude Code setup, often `CLAUDE.md`).

Copy the body from `playbook/templates/consumer-claude-root.md` and adjust the repo name and any stack-specific lines.

**Rule:** Do not duplicate the full playbook. Link to `playbook/docs/engineering/AI_PLAYBOOK.md` and stage gates there.

### B. Global `~/.claude` + `~/Apps` (no `CLAUDE.md` in the repo)

If you keep **project** context out of git (e.g. only `~/.claude/CLAUDE.md`, `~/.claude/SOP.md`, and `~/Apps/CLAUDE.md`):

1. In **`~/.claude/CLAUDE.md`** (or a project memory file under `~/.claude/projects/...`), add a **short** block for each product repo that lists:
   - Path to the git root
   - **Playbook:** `playbook/docs/engineering/AI_PLAYBOOK.md` (relative to that repo)
   - **Handoff template:** `playbook/docs/engineering/HANDOFF.template.md`
   - **Role skills:** `playbook/skills/role-*/SKILL.md`
2. When opening Claude Code, **cd to the product repo** (or open that folder) so `playbook/` resolves and tools can read files under it.
3. Keep the same rule: do not paste the whole playbook into global files—**link paths** under `playbook/`.

## 2. Same process as Cursor

- Stages and roles are defined in `playbook/docs/engineering/AI_PLAYBOOK.md`.
- Use `playbook/docs/engineering/HANDOFF.template.md` when switching between Claude Code and Cursor.

## 3. Skills / subagents in Claude Code

If Claude Code supports project skills or custom instructions, point them at the same role content under `playbook/skills/*/SKILL.md` (or paste summaries into your root file). Keep one canonical copy in the submodule to avoid drift.

## 4. Submodule reminder

After `git clone`, run `git submodule update --init --recursive` so `playbook/` is populated.
