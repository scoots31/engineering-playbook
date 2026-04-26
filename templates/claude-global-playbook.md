## Solo Builder Framework

**Playbook root:** [PLAYBOOK_ROOT]

---

### Session modes

Default is **bare** — no routing, no always-on. Skills load only when invoked.

- "guided mode" → read `[PLAYBOOK_ROOT]/skills/start/SKILL.md`. Full phase chain. Always-on fires.
- "guided on [name]" or "/guided [name]" → read `[PLAYBOOK_ROOT]/projects.md`, find the matching name, read `[path]/docs/continuity/handoff.md`, orient in one sentence, close with direct action prompt. Do not re-run routing logic. If name not found, ask for the path and add it to the registry.
- "piloted mode" → read always-on skills once, then wait for user to invoke phases.
- "bare mode" → return to default. Silent until invoked.

---

### Always-on skills

Fire on `guided` or `piloted` mode activation. One load, persist for the session.

- `[PLAYBOOK_ROOT]/skills/process-mapper/SKILL.md`
- `[PLAYBOOK_ROOT]/skills/product-continuity/SKILL.md`
- `[PLAYBOOK_ROOT]/skills/framework-health/SKILL.md`
- `[PLAYBOOK_ROOT]/skills/retrospective/SKILL.md`

---

### Skills directory

All skills: `[PLAYBOOK_ROOT]/skills/`. Read a skill's `SKILL.md` only when that phase is active.

Phase skills: `start` · `brainstorming` · `discover` · `tech-context` · `design-sprint` · `data-scaffold` · `design-review` · `prd-to-plan` · `to-issues` · `solo-build` · `solo-qa` · `phase-test` · `deploy`

Supporting skills: `research-spike` · `grill-me` · `to-prd` · `principal-engineer` · `agent-room` · `tdd` · `frontend-design` · `qa-triage` · `onboard`

Workshop (spike/tool work): `scope-check` · `spike` · `land`

Support (post-deploy on-demand): `bug-fix` · `enhancement` · `dependency-upgrade` · `security-patch`

Companion (on-demand recall + explain): `nivya` — invoke with `/nivya`; addressable by name once loaded. Recall only — never captures, decides, or builds. Routes to the right skill with consent.

---

### Handoffs

`[PLAYBOOK_ROOT]/docs/engineering/HANDOFF.template.md` → copy to project root as `HANDOFF.md`.
