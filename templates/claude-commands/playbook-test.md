# Engineering playbook — Test

Resolve the playbook root: use environment variable `ENGINEERING_PLAYBOOK` if set and non-empty; otherwise `$HOME/Developer/engineering-playbook`. Verify `docs/engineering/AI_PLAYBOOK.md` exists there.

Run the **Test** stage for the current change or proposal.

1. Read `docs/engineering/AI_PLAYBOOK.md` — **Test** stage and merge bar for user-facing work.
2. Read `skills/role-qa/SKILL.md` and produce: test strategy, cases, exploratory charter, release gate checklist as appropriate to scope.
3. Tie verification to **this repo’s** real commands (test runner, lint) when known from `README` or configs; if unknown, ask once for the canonical command rather than guessing.

**Output:** What to automate vs explore manually, critical cases, data/migration risks if any, and explicit **ready / not ready** for merge with reasons.
