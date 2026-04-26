# Solo Builder Framework — Installation

When the user says "install the Solo Builder Framework," "follow the setup instructions," or similar,
execute every step below. The framework installs itself — do not ask the user to run commands or open files.

---

## Step 1 — Resolve the playbook root

The playbook root is the directory containing this INSTALL.md file. Resolve its absolute path.
Use it as [PLAYBOOK_ROOT] throughout the remaining steps.

---

## Step 2 — Install Claude Code configuration

Read `[PLAYBOOK_ROOT]/templates/claude-global-playbook.md`.
Replace every instance of `[PLAYBOOK_ROOT]` with the resolved absolute path.

Check `~/.claude/CLAUDE.md`:
- If it already contains `## Solo Builder Framework`, replace that section with the updated content.
- If it does not contain that section, append the content to the end of the file.

Confirm to the user: "Claude Code configured — mode activation and skills directory are live."

---

## Step 3 — Output Cursor User Rules

Read `[PLAYBOOK_ROOT]/templates/cursor-user-rules-global-playbook.md`.
Replace every instance of `[PLAYBOOK_ROOT]` with the resolved absolute path.

Output the full result to the user with this instruction:
"Paste the following into Cursor → Settings → Rules → User rules (replace any previous install of this framework):"

Then output the full replaced content.

---

## Step 4 — Confirm

Close with: "Installation complete. Say 'guided mode' in any Claude Code or Cursor session to start."
