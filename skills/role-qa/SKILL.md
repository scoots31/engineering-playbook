---
name: role-qa
description: Builds test strategy, cases, exploratory charters, and release gates. Use when planning verification, before release, after substantial features, or when the user asks for QA, testing, or quality review.
---

# QA lens

## Inputs

- Acceptance criteria and user-facing scope.
- Risk areas (payments, auth, migrations, concurrency).
- Existing automated test coverage (if known).

## Output format

1. **Test strategy** — What must be automated vs exploratory.
2. **Test cases** — Bullet list: preconditions, steps, expected result (happy + key negatives).
3. **Exploratory charter** — Time-boxed mission, areas to stress, data variants.
4. **Release gate** — Checklist: regressions, monitoring, rollback verified.

## Checklist

- [ ] Critical paths covered for this change
- [ ] Edge cases: empty, error, loading, permissions, offline/slow (if relevant)
- [ ] Migrations / backfill / idempotency called out if applicable
- [ ] Definition of done matches `playbook/docs/engineering/AI_PLAYBOOK.md` for user-facing work
