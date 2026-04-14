# Engineering playbook — Cursor work bundle

This folder is a **Cursor-only** copy of the engineering playbook (no Claude Code files). Use it on machines where GitHub and other sync options are unavailable.

## Before you start

1. **Unzip** this archive somewhere permanent on the work laptop, for example:
   - macOS: `~/Developer/engineering-playbook-cursor`
   - (Avoid spaces in the path; remember the full path for the next steps.)

2. **Open this folder in Cursor** as the workspace (File → Open Folder → select the unzipped `cursor-work-playbook` folder).

3. **Open** `PASTE-IN-CURSOR-CHAT.md`, copy the entire prompt, paste it into a **new Cursor chat**, and send it. The agent will walk you through User rules text and optional skill installation.

4. **Manual fallback:** read `docs/engineering/integrate-cursor-work.md` and paste `templates/cursor-user-rules-WORK-template.md` into **Cursor → Settings → Rules → User rules**, replacing `{{PLAYBOOK_ROOT}}` and `{{MEMPALACE_CLI}}` with your absolute paths.

## Contents

| Path | Purpose |
|------|---------|
| `docs/engineering/AI_PLAYBOOK.md` | Stages, roles, definitions of done (Cursor-only edition) |
| `docs/engineering/integrate-cursor-work.md` | How to wire Cursor on this machine |
| `docs/engineering/PLAYBOOK_PATH_CURSOR_WORK.md` | Path rules for this bundle |
| `docs/engineering/HANDOFF.template.md` | Optional `HANDOFF.md` for long sessions |
| `skills/` | Role skills — copy to `~/.cursor/skills/` (recommended) |
| `hooks/examples/` | Optional Cursor hooks |
| `templates/` | `consumer-cursor-always-apply.mdc` (submodule mode) + User rules template |
| `mempalace/MEMPALACE-INSTALL-WORK.md` | MemPalace install on a locked-down laptop |

## Updating on your personal machine

From the full `engineering-playbook` git repo (personal laptop), run:

```bash
./packaging/scripts/build-cursor-work-zip.sh
```

Then email or transfer `packaging/dist/cursor-work-playbook.zip` (should be **well under 20 MB**).
