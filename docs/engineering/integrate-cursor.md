# Integrating this playbook with Cursor

Assume the product repo has this playbook at **`playbook/`** (git submodule).

## 1. Rules (project)

Copy or adapt files from `playbook/templates/` into the product repo:

- `consumer-cursor-always-apply.mdc` → `.cursor/rules/playbook-core.mdc`

Tight, product-specific rules (stack, security, file patterns) stay in **additional** `.mdc` files in the same product’s `.cursor/rules/`.

## 2. Skills (personal vs project)

**Option A — Personal** (all repos on your machine):

- Copy each folder under `playbook/skills/<name>/` to `~/.cursor/skills/<name>/`.

**Option B — Project** (versioned with the product):

- Copy to `.cursor/skills/<name>/` in the product repo.

Do not install custom skills under `~/.cursor/skills-cursor/` (reserved for Cursor).

## 3. Hooks

See `playbook/hooks/examples/`:

- Copy `hooks.json.fragment.md` guidance and scripts into the product’s `.cursor/hooks.json` and `.cursor/hooks/`, **or**
- Install safety-only hooks once at user level: `~/.cursor/hooks.json` (paths relative to `~/.cursor/`).

Make shell scripts executable: `chmod +x .cursor/hooks/*.sh`

## 4. Cursor CLI (optional)

Global preferences: `~/.cursor/cli-config.json`. Project overrides: `.cursor/cli.json` merged from repo root downward.

## 5. Day-to-day

- Open the product repo in Cursor so the agent sees `.cursor/rules` and the `playbook/` tree.
- Ask for a role explicitly, e.g. “Using the Principal Engineer skill, review this change.”
