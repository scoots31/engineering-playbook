# External curated resources (community)

This file is an **index**, not playbook policy. Official **[Claude Code documentation](https://code.claude.com/docs)** and **`AI_PLAYBOOK.md`** remain authoritative for how *you* ship.

## Primary curated repo

**[shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)** — large, well-linked catalog of Claude Code patterns (commands, subagents, skills, hooks, MCP, workflows, tips). Use it for **ideas and wiring examples**; verify behavior against Anthropic docs as the product evolves.

## High-signal topics to borrow (selectively)

| Topic | Why it matters for this playbook |
|-------|----------------------------------|
| **Slash commands** for inner loops | Maps to our stage gates without duplicating `AI_PLAYBOOK.md` in chat. |
| **Subagents for isolation** | Fits “one driver” when used as review-only or worktree-isolated work. |
| **Skills as folders** | Progressive disclosure when role lenses grow large—see [`skill-authoring.md`](skill-authoring.md). |
| **CLAUDE.md / rules splitting** | Keeps root instructions short; links into playbook—see [`integrate-claude-code.md`](integrate-claude-code.md). |
| **Hooks** (separate repo) | [claude-code-hooks](https://github.com/shanraisshan/claude-code-hooks) — compare to our Cursor examples under [`hooks/`](../../hooks/). |
| **Compaction / rewind discipline** | Protects context and avoids “fix forward forever” when the model drifts. |
| **Sandboxing / permissions** | Reduces prompt fatigue; align with org security policy before wide rollout. |
| **Small PRs, squash merge** | Matches our merge hygiene and rollback story for user-facing work. |
| **Cross-model review** | Optional QA pass with a different model/tooling—still under human judgment. |

## Related community projects (optional depth)

The same README indexes other workflow stacks (Spec Kit, Superpowers, etc.). Pull patterns only when they **reduce drift** from `AI_PLAYBOOK.md`, not when they introduce a second process.

## Disclaimer

Community repos are **not** warranties of correctness or security. Review any script or hook before running it against production systems.
