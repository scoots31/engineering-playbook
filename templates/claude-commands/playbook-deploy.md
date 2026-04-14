# Engineering playbook — Deploy

Resolve the playbook root: use environment variable `ENGINEERING_PLAYBOOK` if set and non-empty; otherwise `$HOME/Developer/engineering-playbook`. Verify `docs/engineering/AI_PLAYBOOK.md` exists there.

Run the **Deploy** slice: checklist, monitoring, rollback, and blast-radius sanity for **shipping** what was built (merge to main, release, or env promotion—scope per user).

1. Read `docs/engineering/AI_PLAYBOOK.md` — **Deploy** stage and Ops + PE where blast radius is high.
2. Read `skills/role-principal-engineer/SKILL.md` if production, data, or security blast radius is material; otherwise keep output short and actionable.
3. Use **project repo** runbooks, CI, or `docs/ops` if present; do not invent infra.

**Output:** Pre-deploy checklist, rollback/feature-flag position, what to watch after deploy, and who should be on call / notified if applicable.
