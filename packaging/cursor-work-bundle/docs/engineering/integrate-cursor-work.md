# Integrating this bundle with Cursor (work machine)

Canonical process: [`AI_PLAYBOOK.md`](AI_PLAYBOOK.md). Path rules: [`PLAYBOOK_PATH_CURSOR_WORK.md`](PLAYBOOK_PATH_CURSOR_WORK.md).

This bundle is **Cursor-only** (no Claude Code, no `~/.claude` wiring).

## 1. Global User rules (recommended)

1. Unzip this bundle to a stable path (see `PLAYBOOK_PATH_CURSOR_WORK.md`).
2. Cursor → **Settings → Rules → User rules**.
3. Paste the completed text from `templates/cursor-user-rules-WORK-template.md` (with `{{PLAYBOOK_ROOT}}` and `{{MEMPALACE_CLI}}` replaced), **or** use the chat prompt in `PASTE-IN-CURSOR-CHAT.md` to have the agent generate the final block.

## 2. Skills (recommended)

Copy role skills into your personal Cursor skills directory:

```bash
mkdir -p ~/.cursor/skills
cp -R "{{PLAYBOOK_ROOT}}/skills/"* ~/.cursor/skills/
```

Replace `{{PLAYBOOK_ROOT}}` with your absolute bundle path. Then User rules can say “use the Principal Engineer skill” and Cursor will load `~/.cursor/skills/role-principal-engineer/SKILL.md`.

Do not install custom skills under `~/.cursor/skills-cursor/` (reserved for Cursor).

## 3. Hooks (optional)

See `hooks/examples/` in this bundle. Copy into a product repo’s `.cursor/hooks.json` and `.cursor/hooks/`, or use user-level `~/.cursor/hooks.json` (paths relative to `~/.cursor/`). Make shell scripts executable: `chmod +x .cursor/hooks/*.sh`.

## 4. Project rules (optional)

For **submodule** style inside a product repo, adapt `templates/consumer-cursor-always-apply.mdc` into `.cursor/rules/playbook-core.mdc`. Stack-specific rules stay in separate `.mdc` files.

## 5. Day-to-day

- Open any product repo in Cursor; User rules apply globally.
- Ask for a role explicitly, e.g. “Using the Principal Engineer skill, review this change.”

## 6. MemPalace

Long-term memory is optional. Install and CLI path: [`mempalace/MEMPALACE-INSTALL-WORK.md`](../../mempalace/MEMPALACE-INSTALL-WORK.md). Put the resolved `mempalace` binary path into User rules as `{{MEMPALACE_CLI}}`.
