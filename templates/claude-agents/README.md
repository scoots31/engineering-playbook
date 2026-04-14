# Claude Code subagents (templates)

Copy into a **product** repository under:

`.claude/agents/`

## Intended use

- **Read-only reviewers** for isolated context: Principal Engineer (`principal-engineer-reviewer.md`) and QA (`qa-reviewer.md`).
- Align with **one driver per task** in [`docs/engineering/AI_PLAYBOOK.md`](../../docs/engineering/AI_PLAYBOOK.md): the main session applies changes unless you deliberately use **worktrees** for parallel implementation.

## Playbook path

Agents resolve the playbook via `ENGINEERING_PLAYBOOK` or default `$HOME/Developer/engineering-playbook` — see [`docs/engineering/PLAYBOOK_PATH.md`](../../docs/engineering/PLAYBOOK_PATH.md).

## Further reading

[`docs/engineering/claude-code-harness.md`](../../docs/engineering/claude-code-harness.md)
