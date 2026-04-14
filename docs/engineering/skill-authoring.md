# Skill authoring (playbook + Claude Code)

Role lenses in this repo live as **`SKILL.md` files** (Cursor skills and readable by Claude Code when configured). Keep **one canonical definition** under `skills/` in the engineering playbook; avoid pasting divergent copies into chat.

## Frontmatter (required for Cursor-style skills)

```yaml
---
name: role-example
description: One or two sentences written for the model: when should this skill load?
---
```

Treat **`description` as a trigger**, not a marketing summary: it should read like “Use when …”.

## Body structure (v1 — single file)

Match existing role skills:

1. **Inputs** — what the model needs.
2. **Output format** — numbered sections the model must produce.
3. **Checklist** — merge-ready quality bar.
4. Pointer to **`AI_PLAYBOOK.md`** for definition of done where relevant.

## When to upgrade to a folder skill (v2)

If a skill grows past **~100–150 lines** or accumulates **failure modes**, split into a directory:

```text
skill-name/
  SKILL.md           # short: goal, when to use, links to references/
  references/      # deep detail, edge cases
  scripts/         # optional: small helpers the model can run
  examples/        # optional: good/bad output snippets
```

Add a **Gotchas** section (highest signal): ways the model commonly fails *for this repo or domain*.

## Claude Code–specific notes

- **Progressive disclosure:** keep `SKILL.md` thin; move long tables to `references/`.
- **Context fork:** for heavy tool use, running a skill in an isolated subagent can keep the main thread clean—see [`claude-code-harness.md`](claude-code-harness.md).
- **Dynamic context:** if your toolchain supports shell injection in skills (per Claude Code docs), prefer deterministic short commands over huge pasted state.

## Coherence

Prefer extending the **`reuse-before-build`** skill’s mindset (search before add) over inventing parallel “consistency” skills—unless the product truly needs a separate lens.
