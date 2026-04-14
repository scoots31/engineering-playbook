# Paste this entire block into Cursor chat (Agent mode)

You are helping me finish installing the **Cursor-only engineering playbook** from the folder open as my workspace (the unzipped `cursor-work-playbook` bundle).

**Assume:** the workspace root is the playbook bundle root. If it is not, ask me for the absolute path to that folder before continuing.

Do the following in order:

1. **Read** `00-START-HERE.md` and `docs/engineering/integrate-cursor-work.md` in the workspace and summarize the install steps in ≤8 bullets.

2. **Resolve `PLAYBOOK_ROOT`:** the absolute path to the workspace root (the folder containing `docs/`, `skills/`, `templates/`). Confirm it exists by checking for `docs/engineering/AI_PLAYBOOK.md`.

3. **Produce final Cursor User rules text:**
   - Read `templates/cursor-user-rules-WORK-template.md`.
   - Replace every `{{PLAYBOOK_ROOT}}` with the actual absolute path (no trailing slash).
   - For `{{MEMPALACE_CLI}}`: if I already have MemPalace, run `which mempalace` in the terminal and use that absolute path; if not found, leave the MemPalace subsection as instructions telling me to install per `mempalace/MEMPALACE-INSTALL-WORK.md` and then re-run this step, or use placeholder text `REPLACE_WITH_MEMPALACE_PATH` and explain what to fill in.

4. **Output** a single fenced code block titled **Paste into Cursor → Settings → Rules → User rules** containing the **complete** final rules (ready to copy-paste). Do not omit the MemPalace section unless I asked to remove it.

5. **Optional skills install:** give exact shell commands to copy `skills/*` into `~/.cursor/skills/` (create directory if needed), using the workspace path. Warn that copying is optional if User rules already point at `skills/` under `PLAYBOOK_ROOT`.

6. **Hooks:** one sentence pointing to `hooks/examples/` and that hooks are optional.

7. **MemPalace:** if not installed, point me to `mempalace/MEMPALACE-INSTALL-WORK.md` and the smallest path to a working CLI on macOS (pipx/pip/venv) without assuming I can use GitHub beyond what that file says.

Stay concise; no need to paste the whole playbook into chat—only the User rules block and commands.

---

_End of paste block._
