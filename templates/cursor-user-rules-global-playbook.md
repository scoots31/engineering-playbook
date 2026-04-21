# Cursor User Rules — paste into Cursor Settings → Rules → User rules

_Copy everything below the line into Cursor **Settings → Rules → User rules** (global)._

**Path portability:** Cursor does not expand shell environment variables in User rules. For Claude Code, set `ENGINEERING_PLAYBOOK` (see `engineering-playbook/docs/engineering/PLAYBOOK_PATH.md`). **Keep the “Playbook root” absolute path below identical** to that directory whenever you move the playbook—update `~/.claude/CLAUDE.md` in the same edit.

---

## Global engineering playbook

**Playbook root (absolute):** `/Users/scottheinemeier/Developer/engineering-playbook`

For **any** workspace, treat this playbook as the default delivery process unless the user explicitly overrides it for a one-off task.

**Stack default:** most new work is **not** native iOS. Infer language, framework, and deploy from the **open project** (README, `docs/`, configs). Assume Swift/Xcode only when the repo is clearly an Apple-platform app.

**When starting substantial product or engineering work** (new feature, refactor, release prep), read or skim:

- `/Users/scottheinemeier/Developer/engineering-playbook/docs/engineering/AI_PLAYBOOK.md`
- `/Users/scottheinemeier/Developer/engineering-playbook/docs/engineering/PLAN_TO_BUILD_HANDOFF_SOP.md` — when work will move from **Plan** (here) to **Build** (e.g. Claude): handoff bundle, slice-first prompts, Build-phase habits

**Role lenses** (Principal Engineer, QA, PM, etc.): use the matching **Cursor skill** under `~/.cursor/skills/` if installed; otherwise read:

- `/Users/scottheinemeier/Developer/engineering-playbook/skills/role-principal-engineer/SKILL.md`
- `/Users/scottheinemeier/Developer/engineering-playbook/skills/role-staff-engineer/SKILL.md`
- `/Users/scottheinemeier/Developer/engineering-playbook/skills/role-qa/SKILL.md`
- `/Users/scottheinemeier/Developer/engineering-playbook/skills/role-pm/SKILL.md`
- `/Users/scottheinemeier/Developer/engineering-playbook/skills/reuse-before-build/SKILL.md` — **coherence (guide):** prefer one product story; suggest when parallel paths might drift—user can override for speed or experiments; never treat as a hard gate

**When the user’s intent matches architecture/tradeoffs/system logic**, prefer the Principal Engineer skill; **when they want breakdown, build order, or implementation detail**, prefer the Staff Engineer skill—same role table as in `~/.claude/CLAUDE.md` (keep them in sync if you edit one).

**Handoffs** (switching tools or long sessions): use the template at  
`/Users/scottheinemeier/Developer/engineering-playbook/docs/engineering/HANDOFF.template.md`  
only when the user is doing a handoff; keep `HANDOFF.md` in the project repo if they want it versioned, or local-only if they prefer.

**Project-specific** context (stack, architecture, product decisions) lives **in the open project**—blueprints, `docs/`, README—not in the global playbook.

**Do not** paste the entire playbook into chat every turn; load it when the phase calls for it (plan, design, review, release).

---

## MemPalace (long-term memory)

Scott uses **MemPalace**; data lives under `~/.mempalace/`. CLI (use this path if `mempalace` is not on PATH):

`/Users/scottheinemeier/Apps/.venv/bin/mempalace`

**When the user asks** to update memory / MemPalace / “remember this in the palace”: run the right ingest—typically `mempalace mine "<workspace or project root>"` for code/docs, or `mempalace mine "<path_to_chat_exports>" --mode convos` for exported conversations. Use `mempalace status` to confirm. Do not mine huge unrelated trees (e.g. entire `$HOME`) without explicit approval.

**At the end of a substantial session** (meaningful feature or design work finished, or the user signals wrap-up): **remind** Scott about MemPalace and **offer** to run `mempalace mine` on the **current workspace root** (or convo exports path if that is what changed). If they confirm, run it via the **Shell** tool using the absolute binary path above.
