# Engineering playbook

Reusable delivery system for solo and small-team product work. Use it with **Cursor**, **Claude Code**, or both: the playbook is plain markdown and templates in git—each tool only needs a short pointer in the product repo.

## Use in a product repository

Mount this repo as a **submodule** at `playbook/`:

```bash
git submodule add <your-playbook-repo-url> playbook
git commit -m "Add engineering playbook submodule at playbook/"
```

Clone a repo that already includes the submodule:

```bash
git clone --recurse-submodules <product-repo-url>
# or after a normal clone:
git submodule update --init --recursive
```

### Upgrade the playbook version in a product

```bash
cd playbook
git fetch origin
git checkout <tag-or-branch>   # e.g. v1.0.0 or main
cd ..
git add playbook
git commit -m "Bump engineering-playbook to <tag-or-branch>"
```

## What lives here

| Path | Purpose |
|------|---------|
| `docs/engineering/AI_PLAYBOOK.md` | Canonical process: stages, roles, definitions of done |
| `docs/engineering/HANDOFF.template.md` | Copy to product root as `HANDOFF.md` when switching tools or agents |
| `docs/engineering/integrate-cursor.md` | Wire Cursor (rules, skills, hooks) to this submodule |
| `docs/engineering/integrate-claude-code.md` | Wire Claude Code to the same content |
| `docs/product`, `docs/design`, `docs/tech`, `docs/qa`, `docs/ops` | Empty buckets for **product-specific** docs (optional; often live in the product repo root instead) |
| `templates/` | Snippets to copy into each product repo (thin pointers) |
| `skills/` | Role skills: install under `~/.cursor/skills/` or `.cursor/skills/` in a product |
| `hooks/examples/` | Example Cursor hooks (copy/adapt per product or use user-level hooks) |

## Versioning

Tag releases on this repo (e.g. `v1.0.0`). Product repos pin the submodule to a commit; bump deliberately when you want new playbook behavior.

## Git note (local checkout)

If this folder uses a **separate git directory** (a `.git` file with `gitdir: ...engineering-playbook.git`), that is still a normal Git work tree; `git status`, remotes, and submodules behave the same. After you add a GitHub remote and push, cloning the repo elsewhere will typically give you a standard `.git` directory. If you prefer one folder only, clone fresh from GitHub into `engineering-playbook` and retire the local pair.

## License

Use and adapt internally as needed; add a `LICENSE` file when you publish the repo.
