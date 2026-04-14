# Integrating this playbook with Cursor

Canonical process: [`AI_PLAYBOOK.md`](AI_PLAYBOOK.md). Portable root: [`PLAYBOOK_PATH.md`](PLAYBOOK_PATH.md).

## Global vs submodule

| Mode | Playbook location | Typical wiring |
|------|-------------------|----------------|
| **Global (recommended)** | Checkout lives outside each product (e.g. `~/Developer/engineering-playbook`). | **Cursor User rules** from [`templates/cursor-user-rules-global-playbook.md`](../../templates/cursor-user-rules-global-playbook.md) + optional personal skills under `~/.cursor/skills/`. See [`global-for-all-projects.md`](global-for-all-projects.md). |
| **Submodule (optional)** | `playbook/` inside the product repo. | Copy from `playbook/templates/` into `.cursor/` using **relative** paths in rules. |

Global mode does **not** require a `playbook/` folder in the product repo. Submodule mode does.

## 1. Rules (project) — submodule mode

Copy or adapt files from `playbook/templates/` into the product repo:

- `consumer-cursor-always-apply.mdc` → `.cursor/rules/playbook-core.mdc`

Tight, product-specific rules (stack, security, file patterns) stay in **additional** `.mdc` files in the same product’s `.cursor/rules/`.

## 1b. Rules — global mode

Use **User rules** (Settings → Rules) with absolute paths to the shared playbook checkout. Do not also ship conflicting always-apply project rules that duplicate the whole playbook unless you intend a narrow override.

## 2. Skills (personal vs project)

**Option A — Personal** (all repos on your machine):

- Copy each folder under `playbook/skills/<name>/` (submodule) or from your global playbook checkout to `~/.cursor/skills/<name>/`.

**Option B — Project** (versioned with the product):

- Copy to `.cursor/skills/<name>/` in the product repo.

Do not install custom skills under `~/.cursor/skills-cursor/` (reserved for Cursor).

## 3. Hooks

See `playbook/hooks/examples/` (submodule) or `engineering-playbook/hooks/examples/` (global checkout):

- Copy `hooks.json.fragment.md` guidance and scripts into the product’s `.cursor/hooks.json` and `.cursor/hooks/`, **or**
- Install safety-only hooks once at user level: `~/.cursor/hooks.json` (paths relative to `~/.cursor/`).

Make shell scripts executable: `chmod +x .cursor/hooks/*.sh`

**Claude Code parity:** Cursor hooks ≠ Claude Code hooks—policy and safety bar should still align. See [`claude-code-hooks.md`](claude-code-hooks.md).

## 4. Cursor CLI (optional)

Global preferences: `~/.cursor/cli-config.json`. Project overrides: `.cursor/cli.json` merged from repo root downward.

## 5. Day-to-day

- **Submodule:** open the product repo so the agent sees `.cursor/rules` and the `playbook/` tree.
- **Global:** open any product repo; User rules already point at the shared playbook path.
- Ask for a role explicitly, e.g. “Using the Principal Engineer skill, review this change.”
