# Workflow vocabulary (two zoom levels)

Some community writeups (including curated external references) use **Research → Plan → Execute → Review → Ship**. This playbook uses **Plan → Design → Develop → Test → Deploy** in [`AI_PLAYBOOK.md`](AI_PLAYBOOK.md). They describe the same work at different granularity.

## Mapping

| Community / harness phrasing | This playbook | Notes |
|------------------------------|----------------|--------|
| **Research** | **Plan** (early) + **Design** (discovery) | Spikes, reading code, constraints, options. |
| **Plan** | **Plan** | Problem, scope, success metrics, out of scope. |
| **Execute** | **Develop** | Implementation matching design; small vertical slices. |
| **Review** | **Test** + **Design/Develop** review moments | Automated + exploratory + **Principal Engineer** lens when blast radius is high. |
| **Ship** | **Deploy** + merge discipline | Checklists, monitoring, rollback; PR merge as the last mile of “ship.” |

## Handoffs and tools

**[`HANDOFF.template.md`](HANDOFF.template.md)** is orthogonal to the table above: use it when **switching tools** (Cursor ↔ Claude Code) or **sessions**, not as a “stage” in the lifecycle.

**[`PLAN_TO_BUILD_HANDOFF_SOP.md`](PLAN_TO_BUILD_HANDOFF_SOP.md)** is the **global SOP** for moving from **Plan** outputs to **Build** (artifact bundle, slice-first prompts, how to run Build for efficiency)—use at **milestone boundaries**, not only mid-session handoffs.

## Claude Code primitives (optional)

Slash commands, subagents, and skills are **how** you run the stages in Claude Code; they do not replace the stages. See [`claude-code-harness.md`](claude-code-harness.md).
