# Claude Code hooks vs Cursor hooks

Both tools can run **hooks** (scripts or handlers) around agent actions. Configuration **is not shared** between Cursor and Claude Code—document and copy patterns per tool.

## Cursor

- Config: **`.cursor/hooks.json`** at project root or **`~/.cursor/hooks.json`** for user-wide hooks.
- Examples in this repo: [`hooks/README.md`](../../hooks/README.md) and [`hooks/examples/`](../../hooks/examples/).

## Claude Code

- Config and hook directories follow **Claude Code’s** layout (see [Hooks](https://code.claude.com/docs/en/hooks) in the official docs).
- Community patterns and examples appear in projects such as [shanraisshan/claude-code-hooks](https://github.com/shanraisshan/claude-code-hooks); treat as **reference**, validate against current Anthropic docs.

## Policy suggestions (playbook stance)

| Class | Suggested use |
|-------|----------------|
| **Safety** | Block or confirm destructive commands (`rm -rf`, mass `git reset`, production DB). |
| **Hygiene** | Post-edit formatters or linters so CI stays green without debating style in chat. |
| **Audit** | Log tool names or outcomes for later review (avoid secrets in logs). |

Avoid hooks that **silently “fix”** ambiguous behavior without telling the user—they hide mistakes and make bisection harder.

## Product vs global

- **Global:** only hooks you trust on every repo (e.g. format on save for common file types).
- **Project:** product-specific gates (e.g. migration reminders, contract tests).

Keep Cursor and Claude hook behavior **philosophically aligned** (same safety bar), even if the JSON differs.
