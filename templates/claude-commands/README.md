# Claude Code slash commands (templates)

Copy these files into a **product** repository:

`.claude/commands/`

Then invoke with `/playbook-plan`, `/playbook-design`, `/playbook-develop`, `/playbook-test`, `/playbook-review`, `/playbook-handoff`, `/playbook-deploy` (filename stem = command name).

## Requirements

- **Playbook root:** set `ENGINEERING_PLAYBOOK` to your playbook checkout if it is not at `$HOME/Developer/engineering-playbook`. See [`docs/engineering/PLAYBOOK_PATH.md`](../../docs/engineering/PLAYBOOK_PATH.md).
- **Global mode:** commands only **read** the playbook; product facts come from the **current repo** (cwd).
- **Submodule mode:** if the product uses `playbook/` as a submodule, you may instead copy adapted commands that use **relative** paths `playbook/docs/...`—avoid mixing relative and env-based roots without a clear rule.

## Wiring

See [`docs/engineering/integrate-claude-code.md`](../../docs/engineering/integrate-claude-code.md) and [`docs/engineering/claude-code-harness.md`](../../docs/engineering/claude-code-harness.md).
