# Solo Builder Framework — Installation

When the user says "install the Solo Builder Framework," "follow the setup instructions," or similar,
execute every step below. The framework installs itself — do not ask the user to run commands or open files.

---

## Step 1 — Resolve the playbook root

The playbook root is the directory containing this INSTALL.md file. Resolve its absolute path.
Use it as [PLAYBOOK_ROOT] throughout the remaining steps.

---

## Step 2 — Resolve and create the projects root

The projects root is a folder kept separate from the playbook, so a solo's own project work
never lives inside the framework's own repo. It sits next to the playbook root, named
`Development Files` — e.g. if [PLAYBOOK_ROOT] is `/Users/name/Developer/engineering-playbook`,
the projects root is `/Users/name/Developer/Development Files`. Resolve its absolute path and
use it as [PROJECTS_ROOT] throughout the remaining steps.

Create the folder if it does not already exist.

Check for `[PROJECTS_ROOT]/projects.md`. If it does not exist, create it with this content:

```
# Projects Registry

Maps project names to absolute paths. One row per project. Used by the framework
to resume a named project — "guided on [name]" or `/guided [name]`.

Add your own projects below.

| Name | Path |
|------|------|
```

---

## Step 3 — Install Claude Code configuration

Read `[PLAYBOOK_ROOT]/templates/claude-global-playbook.md`.
Replace every instance of `[PLAYBOOK_ROOT]` with the resolved playbook root, and every
instance of `[PROJECTS_ROOT]` with the resolved projects root.

Check `~/.claude/CLAUDE.md`:
- If it already contains `## Solo Builder Framework`, replace that section with the updated content.
- If it does not contain that section, append the content to the end of the file.

Confirm to the user: "Claude Code configured — mode activation and skills directory are live."

---

## Step 4 — Output Cursor User Rules

Read `[PLAYBOOK_ROOT]/templates/cursor-user-rules-global-playbook.md`.
Replace every instance of `[PLAYBOOK_ROOT]` with the resolved playbook root, and every
instance of `[PROJECTS_ROOT]` with the resolved projects root.

Output the full result to the user with this instruction:
"Paste the following into Cursor → Settings → Rules → User rules (replace any previous install of this framework):"

Then output the full replaced content.

---

## Step 5 — Confirm

Close with: "Installation complete. Your projects folder is at [PROJECTS_ROOT] — that's where Solo Companion should point too, if you're using it. Say 'guided mode' in any Claude Code or Cursor session to start."
