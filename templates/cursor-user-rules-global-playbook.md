# Cursor User Rules — paste into Cursor Settings → Rules → User rules

_Copy everything below the line into Cursor **Settings → Rules → User rules** (global).  
Replace the path if your playbook is not at `~/Developer/engineering-playbook`._

---

## Global engineering playbook

**Playbook root (absolute):** `/Users/scottheinemeier/Developer/engineering-playbook`

For **any** workspace, treat this playbook as the default delivery process unless the user explicitly overrides it for a one-off task.

**Stack default:** most new work is **not** native iOS. Infer language, framework, and deploy from the **open project** (README, `docs/`, configs). Assume Swift/Xcode only when the repo is clearly an Apple-platform app.

**When starting substantial product or engineering work** (new feature, refactor, release prep), read or skim:

- `/Users/scottheinemeier/Developer/engineering-playbook/docs/engineering/AI_PLAYBOOK.md`

**Role lenses** (Principal Engineer, QA, PM, etc.): use the matching **Cursor skill** under `~/.cursor/skills/` if installed; otherwise read:

- `/Users/scottheinemeier/Developer/engineering-playbook/skills/role-principal-engineer/SKILL.md`
- `/Users/scottheinemeier/Developer/engineering-playbook/skills/role-qa/SKILL.md`
- `/Users/scottheinemeier/Developer/engineering-playbook/skills/role-pm/SKILL.md`

**Handoffs** (switching tools or long sessions): use the template at  
`/Users/scottheinemeier/Developer/engineering-playbook/docs/engineering/HANDOFF.template.md`  
only when the user is doing a handoff; keep `HANDOFF.md` in the project repo if they want it versioned, or local-only if they prefer.

**Project-specific** context (stack, architecture, product decisions) lives **in the open project**—blueprints, `docs/`, README—not in the global playbook.

**Do not** paste the entire playbook into chat every turn; load it when the phase calls for it (plan, design, review, release).
