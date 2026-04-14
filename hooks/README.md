# Hooks (Cursor examples + Claude Code pointer)

## Cursor

These examples are meant to be **copied** into a product repository:

- `.cursor/hooks.json` at the product root (project hooks), or
- `~/.cursor/hooks.json` for user-wide hooks (paths relative to `~/.cursor/`).

See `examples/` for a destructive-command guard and merge notes.

**Verify** in Cursor: Hooks settings tab and Hooks output channel after saving `hooks.json`.

## Claude Code

Claude Code uses a **different** hooks configuration and directory layout than Cursor. See [`docs/engineering/claude-code-hooks.md`](../docs/engineering/claude-code-hooks.md) and the official [Hooks](https://code.claude.com/docs/en/hooks) documentation. Keep **policy** (safety, hygiene, audit) aligned across tools even if the JSON differs.
