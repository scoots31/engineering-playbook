# Global playbook mode (all projects, minimal setup)

Use this when you want **one canonical playbook** on disk—**no submodule per repo**—and both **Claude Code** and **Cursor** to follow it on every project.

## Canonical location (this machine)

Default path (adjust if you move the repo):

`~/Developer/engineering-playbook`

Environment variable (optional, for shell scripts only):

`export ENGINEERING_PLAYBOOK="$HOME/Developer/engineering-playbook"`

## What lives globally vs in each project

| Global (playbook repo) | Per project (your app / tool repo) |
|-------------------------|--------------------------------------|
| Stage gates, process | PRDs, blueprints, app-specific `docs/` |
| Role skill definitions (`skills/role-*`) | Stack, build, deploy, secrets |
| Handoff template | `HANDOFF.md` when you need it (often local-only) |
| Hook *examples* | `.cursor/hooks` only if a project needs extra gates |

## Claude Code

1. In **`~/.claude/CLAUDE.md`**, keep a short block that points at the absolute paths under `~/Developer/engineering-playbook/…` (see your file—you should have a “Global engineering playbook” section).
2. **Project facts** stay in that repo (e.g. `BLUEPRINT.md`, Xcode layout)—do not duplicate the full playbook into global files.

## Cursor

1. **User Rules** (Cursor **Settings → Rules → User rules**): paste the snippet from  
   `engineering-playbook/templates/cursor-user-rules-global-playbook.md`  
   once. Update the path if your playbook lives elsewhere.
2. **Personal skills** (optional but recommended): copy `playbook/skills/role-*` into  
   `~/.cursor/skills/`  
   so role lenses apply in every workspace without opening the playbook tree.

## New projects

Create the repo as usual. **No** `git submodule add` required. Optionally add **only** project-specific `.cursor/rules` (globs, stack) in that repo.

## Repos that already have `playbook/` as a submodule

You can **keep** the submodule (pinned copy) or **remove** it to avoid two sources of truth. If you remove it, rely on the global path + `~/.claude` + Cursor User Rules only.
