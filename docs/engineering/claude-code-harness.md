# Claude Code harness (commands, agents, skills)

This playbook’s **canonical process** is still [`AI_PLAYBOOK.md`](AI_PLAYBOOK.md). Claude Code adds **primitives** (slash commands, subagents, skills, hooks, MCP) that make that process **repeatable** in the terminal without duplicating prose.

Official reference: [Claude Code documentation](https://code.claude.com/docs).

## Playbook root

Always resolve paths per [`PLAYBOOK_PATH.md`](PLAYBOOK_PATH.md): `ENGINEERING_PLAYBOOK` if set, else `$HOME/Developer/engineering-playbook`.

## Recommended pattern: Command → Agent → Skill

| Primitive | Role | Use it when |
|-----------|------|-------------|
| **Slash command** (`.claude/commands/*.md`) | Starts a **named workflow** | You repeat the same inner loop (plan slice, handoff, test pass). Commands should **link or read** playbook files—not restate them. |
| **Subagent** (`.claude/agents/*.md`) | **Isolated context** for a bounded task | You want a **review**, **research**, or **tool-heavy** pass without polluting the main session. Prefer **read-only** or **branch-isolated** work—see below. |
| **Skill** (`.claude/skills/` or shared markdown under the playbook) | **Durable knowledge** + checklists | The model should load **Principal Engineer**, **QA**, etc. lenses. Canonical copies live under `skills/` in this repo; install per [`integrate-claude-code.md`](integrate-claude-code.md). |

A concrete orchestration walkthrough (community): [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) — treat as **patterns**, not policy; official docs win for tool behavior.

## Align with “one driver per task”

[`AI_PLAYBOOK.md`](AI_PLAYBOOK.md) says **one driver per task**. Subagents are compatible if:

- **Review-only:** subagent reads code and returns findings; **main session** applies edits, **or**
- **Parallel worktrees:** each agent has its own git worktree / branch (no two writers on one dirty tree), **or**
- **Explicit handoff:** subagent produces a patch or plan; human or main session merges deliberately.

Avoid: two agents **editing the same checkout** toward different goals without coordination.

## Minimal `.claude/` layout (global playbook)

In a **product** repo (optional, versioned with the product):

```text
.claude/
  commands/     # copy from playbook templates/claude-commands/
  agents/       # optional; copy from templates/claude-agents/
```

Skills: either symlink from the playbook `skills/` tree into `.claude/skills/`, or configure Claude Code to discover skills from the resolved playbook path (per current Claude Code version—verify in docs).

## Further reading (this repo)

- [`skill-authoring.md`](skill-authoring.md) — shape of playbook and Claude-native skills.
- [`claude-code-hooks.md`](claude-code-hooks.md) — hooks vs Cursor hooks.
- [`mcp-checklist.md`](mcp-checklist.md) — when to add MCP to a product.
- [`external-curated-resources.md`](external-curated-resources.md) — curated community index.
