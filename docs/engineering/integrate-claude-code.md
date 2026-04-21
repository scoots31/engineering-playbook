# Integrating this playbook with Claude Code

Canonical process: [`AI_PLAYBOOK.md`](AI_PLAYBOOK.md). **Plan → Build handoff:** [`PLAN_TO_BUILD_HANDOFF_SOP.md`](PLAN_TO_BUILD_HANDOFF_SOP.md). Playbook path resolution: [`PLAYBOOK_PATH.md`](PLAYBOOK_PATH.md).

## Choose a consumption mode

| Mode | When to use | Playbook paths |
|------|----------------|----------------|
| **Global (default for Scott)** | One playbook on disk; every product repo follows it without a submodule. | Resolve via `ENGINEERING_PLAYBOOK` or `$HOME/Developer/engineering-playbook`. See [`global-for-all-projects.md`](global-for-all-projects.md). |
| **Submodule (optional)** | Team wants the playbook **pinned** inside the product repo at `playbook/`. | Use paths relative to repo root: `playbook/docs/engineering/AI_PLAYBOOK.md`. |

Do **not** mix global and submodule for the **same** process text in one workflow without a clear rule—pick one source of truth per repo.

## 1. Global `~/.claude/CLAUDE.md` (recommended)

Keep a **short** block that:

- Points at the resolved playbook root (after `PLAYBOOK_PATH` rules).
- Lists role skill paths under `skills/role-*/SKILL.md`.
- Links `docs/engineering/HANDOFF.template.md` and `docs/engineering/PLAN_TO_BUILD_HANDOFF_SOP.md` (one line each).
- Does **not** paste the full playbook.

Set `ENGINEERING_PLAYBOOK` in your shell so slash commands and agents can resolve the same root without hardcoding.

## 2. Product repo `CLAUDE.md` (thin pointer)

In the **product** repo root, keep **project facts** (stack, how to run tests, deploy notes). Copy/adapt from [`templates/consumer-claude-root.md`](../../templates/consumer-claude-root.md).

### `CLAUDE.md` hygiene

- **Short files:** prefer linking the playbook over pasting stage gates.
- **Split large rules:** use `.claude/rules/` (per [Claude Code memory / rules](https://code.claude.com/docs/en/memory)) for monorepos or long stack-specific policy.
- **One obvious “run the tests” story:** a new contributor should be able to run the canonical test command from what’s in repo + global playbook behavior.

## 3. Submodule mode (optional)

Assume the product has **`playbook/`** as a git submodule.

1. Product `CLAUDE.md` should link `playbook/docs/engineering/AI_PLAYBOOK.md` (relative path).
2. After `git clone`, run `git submodule update --init --recursive`.
3. Role skills: use paths under `playbook/skills/` in that repo.

## 4. Slash commands and subagents (harness)

Copy templates from this repo into the **product** repo (versioned with the product):

| Template folder | Destination | Invoke |
|-----------------|---------------|--------|
| [`templates/claude-commands/`](../../templates/claude-commands/) | `.claude/commands/` | `/playbook-plan`, `/playbook-design`, etc. |
| [`templates/claude-agents/`](../../templates/claude-agents/) | `.claude/agents/` | Per Claude Code agent UX |

Details: [`claude-code-harness.md`](claude-code-harness.md).

## 5. Same process as Cursor

- Stages and roles: `AI_PLAYBOOK.md`.
- Handoffs: `HANDOFF.template.md` → `HANDOFF.md` in the product when switching tools or long sessions.

## 6. Skills

Canonical role skills live under **`skills/`** in the engineering playbook. Options:

- **Symlink** into `.claude/skills/` from the resolved playbook path, or
- **Copy** when you need a pinned snapshot (accept drift on upgrade).

Authoring guidance: [`skill-authoring.md`](skill-authoring.md).

## 7. Hooks and MCP

- Hooks: [`claude-code-hooks.md`](claude-code-hooks.md) (and compare Cursor [`hooks/README.md`](../../hooks/README.md)).
- MCP: [`mcp-checklist.md`](mcp-checklist.md), example [`templates/mcp.json.example`](../../templates/mcp.json.example).

## 8. Further reading

- [`workflow-vocabulary.md`](workflow-vocabulary.md) — map community “Research → … → Ship” to our stages.
- [`external-curated-resources.md`](external-curated-resources.md) — curated community index (non-authoritative).
