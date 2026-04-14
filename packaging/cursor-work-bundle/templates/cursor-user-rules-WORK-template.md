# Cursor User Rules — work bundle (paste into Settings → Rules → User rules)

_Replace every `{{PLAYBOOK_ROOT}}` with the absolute path to this unzipped bundle (the folder that contains `docs/`, `skills/`, `templates/`). Replace `{{MEMPALACE_CLI}}` with the absolute path to the `mempalace` binary, or remove the MemPalace section until installed._

---

## Global engineering playbook (Cursor work bundle)

**Playbook root (absolute):** `{{PLAYBOOK_ROOT}}`

For **any** workspace, treat this playbook as the default delivery process unless the user explicitly overrides it for a one-off task.

**Stack default:** infer language, framework, and deploy from the **open project** (README, `docs/`, configs). Do not assume a stack not evidenced by the repo.

**When starting substantial product or engineering work** (new feature, refactor, release prep), read or skim:

- `{{PLAYBOOK_ROOT}}/docs/engineering/AI_PLAYBOOK.md`

**Role lenses** (Principal Engineer, QA, PM, etc.): use the matching **Cursor skill** under `~/.cursor/skills/` if installed; otherwise read:

- `{{PLAYBOOK_ROOT}}/skills/role-principal-engineer/SKILL.md`
- `{{PLAYBOOK_ROOT}}/skills/role-staff-engineer/SKILL.md`
- `{{PLAYBOOK_ROOT}}/skills/role-qa/SKILL.md`
- `{{PLAYBOOK_ROOT}}/skills/role-pm/SKILL.md`
- `{{PLAYBOOK_ROOT}}/skills/reuse-before-build/SKILL.md` — **coherence (guide):** prefer one product story; suggest when parallel paths might drift—user can override for speed or experiments; never treat as a hard gate

**When the user’s intent matches architecture/tradeoffs/system logic**, prefer the Principal Engineer skill; **when they want breakdown, build order, or implementation detail**, prefer the Staff Engineer skill.

**Handoffs** (long sessions or context switches): use the template at  
`{{PLAYBOOK_ROOT}}/docs/engineering/HANDOFF.template.md`  
only when the user is doing a handoff; keep `HANDOFF.md` in the project repo if they want it versioned, or local-only if they prefer.

**Project-specific** context (stack, architecture, product decisions) lives **in the open project**—blueprints, `docs/`, README—not in the global playbook.

**Do not** paste the entire playbook into chat every turn; load it when the phase calls for it (plan, design, review, release).

---

## MemPalace (long-term memory)

MemPalace stores data under `~/.mempalace/` by default. CLI path (use absolute path in Shell tool if `mempalace` is not on PATH):

`{{MEMPALACE_CLI}}`

**When the user asks** to update memory / MemPalace / “remember this in the palace”: run the right ingest—typically `mempalace mine "<workspace or project root>"` for code/docs, or per MemPalace docs for conversation exports. Use `mempalace status` to confirm. Do not mine huge unrelated trees (e.g. entire `$HOME`) without explicit approval.

**At the end of a substantial session** (meaningful feature or design work finished, or the user signals wrap-up): **remind** the user about MemPalace and **offer** to run `mempalace mine` on the **current workspace root** if they confirm.
