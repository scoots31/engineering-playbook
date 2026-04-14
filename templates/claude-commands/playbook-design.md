# Engineering playbook — Design

Resolve the playbook root: use environment variable `ENGINEERING_PLAYBOOK` if set and non-empty; otherwise `$HOME/Developer/engineering-playbook`. Verify `docs/engineering/AI_PLAYBOOK.md` exists there.

Run the **Design** stage for the user’s task in the **open project**.

1. Read `docs/engineering/AI_PLAYBOOK.md` — **Design** stage: UX acceptance criteria where relevant, technical approach, coherence with existing patterns.
2. Read `skills/role-staff-engineer/SKILL.md` for execution-oriented design breakdown; pull `skills/role-principal-engineer/SKILL.md` if architecture, blast radius, or major tradeoffs dominate.
3. Optionally read `skills/reuse-before-build/SKILL.md` for coherence nudges (user may override for speed).

**Output:** Design summary, acceptance criteria (including error/empty/loading where user-facing), approach and alternatives dismissed, open questions for **Develop**, and any ADR note if the decision should be recorded in the product repo.
