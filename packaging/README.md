# Packaging (Cursor work bundle)

## `cursor-work-playbook.zip`

For machines where **GitHub is unavailable** and you use **Cursor only** (different account than personal). The zip contains:

- Cursor-only editions of shared docs (transformed from the main repo)
- `skills/`, `hooks/examples/`, templates
- Install instructions + a **paste-into-chat** bootstrap for Cursor Agent

### Build (on your personal laptop, inside this repo)

```bash
chmod +x packaging/scripts/build-cursor-work-zip.sh
./packaging/scripts/build-cursor-work-zip.sh
```

Output: **`packaging/dist/cursor-work-playbook.zip`** (text-only tree; typically **well under 20 MB**).

### Transfer

Email attachment, USB, or any approved channel. Unzip on the work laptop, open the folder in Cursor, then follow **`00-START-HERE.md`** or paste the prompt from **`PASTE-IN-CURSOR-CHAT.md`**.

### Maintenance

When you change **`docs/engineering/AI_PLAYBOOK.md`**, **`HANDOFF.template.md`**, **`workflow-vocabulary.md`**, or **`skill-authoring.md`** in the main repo, **re-run the build script** before sending a new zip so the work bundle stays aligned. Hand-edit files under `packaging/cursor-work-bundle/` when you need work-specific wording (User rules template, MemPalace install notes).
