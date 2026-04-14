# Playbook root path (portable installs)

Use this so the engineering playbook can live **anywhere** on disk without forking its content. **Global mode** (one playbook, all projects) is the default story; see [`global-for-all-projects.md`](global-for-all-projects.md).

## Resolution order

When docs or slash commands say “resolve the playbook root,” use:

1. **`ENGINEERING_PLAYBOOK`** — If this environment variable is set to a non-empty string, it is the playbook root (absolute path preferred).
2. **Default** — `$HOME/Developer/engineering-playbook`

Shell example:

```bash
export ENGINEERING_PLAYBOOK="$HOME/Developer/engineering-playbook"
```

Add that to `~/.zshrc` (or your profile) if you use a non-default location.

## What reads which signal

| Consumer | Reads `ENGINEERING_PLAYBOOK`? | Notes |
|----------|--------------------------------|--------|
| **Claude Code** (agent following slash commands) | Yes, when the shell/session exposes it | Command bodies instruct the agent to prefer the env var, then default. |
| **Cursor User rules** | No | Cursor does not expand shell env vars in pasted rules. Keep **one** absolute “playbook root” line there and update it when you move the repo (same as today). |
| **`~/.claude/CLAUDE.md`** | Optional | You can hardcode paths or tell yourself to mirror `ENGINEERING_PLAYBOOK`; the agent sees the file text. |

## When you move the playbook directory

Update these in lockstep so nothing drifts:

1. Shell: `ENGINEERING_PLAYBOOK` (if you use it).
2. **Cursor** → Settings → Rules → User rules: every path under the old root (see [`templates/cursor-user-rules-global-playbook.md`](../../templates/cursor-user-rules-global-playbook.md)).
3. **`~/.claude/CLAUDE.md`**: global playbook block paths.
4. Optional: any product `CLAUDE.md` that still points at a submodule `playbook/` (submodule mode).

Do **not** rely on broken symlinks; verify with:

```bash
test -f "${ENGINEERING_PLAYBOOK:-$HOME/Developer/engineering-playbook}/docs/engineering/AI_PLAYBOOK.md" && echo OK
```

## Submodule mode (optional)

If a product repo uses **`playbook/`** as a git submodule, paths are **relative to that repo root** (e.g. `playbook/docs/engineering/AI_PLAYBOOK.md`). That overrides “global root” for files inside that repo only. See [`integrate-claude-code.md`](integrate-claude-code.md).
