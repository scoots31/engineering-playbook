# Cursor User Rules — paste into Cursor Settings → Rules → User rules

_Copy everything **below the dashed line** into Cursor **Settings → Rules → User rules** (global)._

## Before you paste — one substitution required

Cursor does not expand shell variables or `~` in User rules. You must replace `[PLAYBOOK_ROOT]` with the absolute path to where you cloned this repo.

**To find your absolute path:** open a terminal, `cd` to where you cloned the repo, and run `pwd`. Copy that output and replace every instance of `[PLAYBOOK_ROOT]` below before pasting.

Example: if `pwd` returns `/Users/yourname/Developer/engineering-playbook`, replace `[PLAYBOOK_ROOT]` with `/Users/yourname/Developer/engineering-playbook`.

---

## Solo Builder Framework — Global Playbook

**Playbook root (absolute):** `[PLAYBOOK_ROOT]`

---

## Session mode

Default is **bare** — no routing, no always-on. Skills load only when invoked.

- "auto-pilot mode" → read `[PLAYBOOK_ROOT]/skills/start/SKILL.md`. Full phase chain. Always-on fires.
- "assisted mode" → read always-on skills once, then wait for user to invoke phases.
- "bare mode" → return to default. Silent until invoked.

---

## Always-on skills

Fire on `auto-pilot` or `assisted` mode activation. One load, persist for the session.

- `[PLAYBOOK_ROOT]/skills/process-mapper/SKILL.md`
- `[PLAYBOOK_ROOT]/skills/product-continuity/SKILL.md`
- `[PLAYBOOK_ROOT]/skills/framework-health/SKILL.md`
- `[PLAYBOOK_ROOT]/skills/retrospective/SKILL.md`

---

## Skills directory

All skills: `[PLAYBOOK_ROOT]/skills/`. Read a skill's `SKILL.md` only when that phase is active.

Phase skills: `start` · `brainstorming` · `discover` · `tech-context` · `design-sprint` · `data-scaffold` · `design-review` · `prd-to-plan` · `to-issues` · `solo-build` · `solo-qa` · `phase-test` · `deploy`

Supporting skills: `research-spike` · `grill-me` · `to-prd` · `principal-engineer` · `agent-room` · `tdd` · `frontend-design` · `qa-triage`

Workshop (spike/tool work): `scope-check` · `spike` · `land`

Support (post-deploy on-demand): `bug-fix` · `enhancement` · `dependency-upgrade` · `security-patch`

---

## MemPalace

End of substantial session: offer `mempalace mine "<project root>"`.

---

## Handoffs

`[PLAYBOOK_ROOT]/docs/engineering/HANDOFF.template.md` → copy to project root as `HANDOFF.md`.
