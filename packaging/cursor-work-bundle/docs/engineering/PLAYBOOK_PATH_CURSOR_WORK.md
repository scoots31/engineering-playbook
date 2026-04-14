# Playbook path (Cursor work bundle)

This bundle is a **normal folder** on disk. Cursor **User rules** cannot read environment variables—every path to these files must be an **absolute path** you paste into Settings → Rules → User rules.

## Choose one location

Example (macOS):

`~/Developer/engineering-playbook-cursor`

Unzip the archive there once, then **do not move** the folder without updating User rules (or re-run the bootstrap prompt in `PASTE-IN-CURSOR-CHAT.md`).

## What to put in User rules

Use the **same** absolute path for:

- `AI_PLAYBOOK.md`
- Each `skills/.../SKILL.md` you reference
- `HANDOFF.template.md`

See `templates/cursor-user-rules-WORK-template.md`.

## Skills: copy vs reference

- **Recommended:** `cp -R` the `skills/` tree into `~/.cursor/skills/` so Cursor discovers skills by name.
- **Alternative:** keep skills only inside this bundle and list **absolute paths** to each `SKILL.md` in User rules (more verbose, fewer copies).

## Submodule mode (rare on work laptop)

If a product repo ever includes this playbook as `playbook/`, use **relative** paths in that repo’s `.cursor/rules` only—see `templates/consumer-cursor-always-apply.mdc`. Global User rules on work usually use the **absolute** bundle path instead.
