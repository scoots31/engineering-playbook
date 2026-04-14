# Engineering playbook — Develop

Resolve the playbook root: use environment variable `ENGINEERING_PLAYBOOK` if set and non-empty; otherwise `$HOME/Developer/engineering-playbook`. Verify `docs/engineering/AI_PLAYBOOK.md` exists there.

Run the **Develop** stage: implementation aligned with an agreed design (or a minimal spike if the user explicitly wants exploration).

1. Read `docs/engineering/AI_PLAYBOOK.md` — **Develop** stage and minimum bar before merge for user-facing changes.
2. Read `skills/role-staff-engineer/SKILL.md` for incremental rollout, edge cases, and sequencing.
3. Prefer extending existing code paths in this repo; if a deliberate one-off is chosen, say so briefly so later work does not “fix” it accidentally (coherence principle in `AI_PLAYBOOK.md`).

**Output:** Concrete change list or patch-oriented plan, files likely touched, test hooks to add/update, and rollback/feature-flag notes if the change is user-facing.
