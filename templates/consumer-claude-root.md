# Project instructions (Claude Code)

## Playbook (how we work)

**Global mode:** process lives outside this repo. Resolve the playbook root:

1. Environment variable **`ENGINEERING_PLAYBOOK`** if set.
2. Otherwise **`$HOME/Developer/engineering-playbook`**.

Read the canonical delivery doc at:

`<playbook-root>/docs/engineering/AI_PLAYBOOK.md`

Use `<playbook-root>/docs/engineering/HANDOFF.template.md` when creating or updating **`HANDOFF.md`** in this repo (or paste for local-only handoffs).

Follow `<playbook-root>/docs/engineering/PLAN_TO_BUILD_HANDOFF_SOP.md` when implementing from **Plan** artifacts (handoff bundle, slice-first prompts).

**Submodule mode (optional):** if this repository includes `playbook/` as a git submodule, use relative paths instead:

- `playbook/docs/engineering/AI_PLAYBOOK.md`
- `playbook/docs/engineering/HANDOFF.template.md`
- `playbook/docs/engineering/PLAN_TO_BUILD_HANDOFF_SOP.md`

Do not duplicate the full playbook in this file.

## How to work

1. Follow the stage gates in the AI playbook (Plan → Design → Develop → Test → Deploy).
2. When the user names a role (Principal Engineer, QA, PM, Staff), read the matching skill under `<playbook-root>/skills/role-*/SKILL.md` (or `playbook/skills/` in submodule mode).
3. Prefer thin vertical slices; for user-facing changes, include test plan bullets and rollback/feature-flag notes before treating work as done.

## Repo-specific (edit per product)

- **Stack:**
- **How to run tests / lint:**
- **Deploy / env notes:** (link to runbooks if any)
