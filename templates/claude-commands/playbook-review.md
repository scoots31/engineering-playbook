# Engineering playbook — Principal review

Resolve the playbook root: use environment variable `ENGINEERING_PLAYBOOK` if set and non-empty; otherwise `$HOME/Developer/engineering-playbook`. Verify `docs/engineering/AI_PLAYBOOK.md` exists there.

Run a **Principal Engineer** pass on the current diff, design, or proposal (architecture, tradeoffs, risk, maintainability, blast radius)—**not** a line-by-line style nit unless tied to correctness or safety.

1. Read `docs/engineering/AI_PLAYBOOK.md` for principles and stage context.
2. Read `skills/role-principal-engineer/SKILL.md` and follow its output format.
3. Prefer **read-only** inspection unless the user asked for edits; if suggesting changes, separate **must-fix** vs **should-fix** vs **nice-to-have**.

**Output:** Summary, tradeoffs, risks, maintainability notes, and a clear recommendation (proceed / proceed with conditions / pause and redesign).
