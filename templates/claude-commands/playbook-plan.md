# Engineering playbook — Plan

Resolve the playbook root: use environment variable `ENGINEERING_PLAYBOOK` if set and non-empty; otherwise `$HOME/Developer/engineering-playbook`. Verify `docs/engineering/AI_PLAYBOOK.md` exists there. (See playbook doc `docs/engineering/PLAYBOOK_PATH.md`.)

Run the **Plan** stage for the user’s current task in the **open project** (repository root = product facts only).

1. Read `docs/engineering/AI_PLAYBOOK.md` at the playbook root — apply the **Plan** stage and principles (one driver, small slices, written handoffs when switching tools).
2. Read `skills/role-pm/SKILL.md` at the playbook root for PM-style scope and sequencing unless the user asks for a different lens.
3. Ground answers in this **product repo**: `README`, `docs/`, issues, or what the user pasted. Do not assume stack from the global playbook.

**Output:** Problem statement, constraints, success metrics, explicit **out of scope**, key risks/unknowns, and the recommended next stage (usually **Design**).
