# Engineering playbook

Reusable delivery system for solo and small-team product work. Use it with **Cursor**, **Claude Code**, or both: the playbook is plain markdown and templates in git—each tool only needs a short pointer in the product repo.

## Global mode (recommended for you)

If you want **one playbook for every project** with **no submodule per repo**, follow  
[`docs/engineering/global-for-all-projects.md`](docs/engineering/global-for-all-projects.md)  
and paste the Cursor snippet from  
[`templates/cursor-user-rules-global-playbook.md`](templates/cursor-user-rules-global-playbook.md)  
into **Cursor Settings → Rules → User rules**. Wire **Claude Code** in `~/.claude/CLAUDE.md` the same way.

## Use in a product repository (optional submodule)

Mount this repo as a **submodule** at `playbook/` when you want the playbook **version-pinned inside that product repo** (e.g. team or release reproducibility):

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
| `docs/engineering/PLAN_TO_BUILD_HANDOFF_SOP.md` | **Global SOP:** Plan → Build handoff bundle, prompts, Build-phase habits (every project) |
| `docs/engineering/PLAYBOOK_PATH.md` | Portable playbook root: `ENGINEERING_PLAYBOOK` vs default path |
| `docs/engineering/HANDOFF.template.md` | Copy to product root as `HANDOFF.md` when switching tools or agents |
| `docs/engineering/workflow-vocabulary.md` | Map community workflow phrasing to this playbook’s stages |
| `docs/engineering/claude-code-harness.md` | Claude Code: commands, subagents, skills, one-driver alignment |
| `docs/engineering/skill-authoring.md` | How to write and evolve `SKILL.md` / folder skills |
| `docs/engineering/claude-code-hooks.md` | Claude Code hooks vs Cursor hooks |
| `docs/engineering/mcp-checklist.md` | When and how to add MCP safely per product |
| `docs/engineering/external-curated-resources.md` | Curated community index (non-authoritative) |
| `docs/engineering/integrate-cursor.md` | Wire Cursor (rules, skills, hooks); global + submodule |
| `docs/engineering/integrate-claude-code.md` | Wire Claude Code (CLAUDE.md, commands, agents, MCP) |
| `docs/product`, `docs/design`, `docs/tech`, `docs/qa`, `docs/ops` | Empty buckets for **product-specific** docs (optional; often live in the product repo root instead) |
| `templates/` | Snippets for product repos and Cursor user rules |
| `templates/claude-commands/` | Slash command templates for `.claude/commands/` |
| `templates/claude-agents/` | Read-only subagent templates for `.claude/agents/` |
| `templates/mcp.json.example` | Structural MCP example (replace placeholders) |
| `skills/` | Role skills: install under `~/.cursor/skills/` or `.cursor/skills/` in a product |
| `hooks/examples/` | Example Cursor hooks (copy/adapt per product or use user-level hooks) |

## Versioning

Tag releases on this repo (e.g. `v1.0.0`). **Submodule mode:** product repos pin the submodule to a commit; bump deliberately when you want new playbook behavior. **Global mode:** update the single checkout on disk (and keep Cursor User rules + `~/.claude/CLAUDE.md` paths in sync per [`docs/engineering/PLAYBOOK_PATH.md`](docs/engineering/PLAYBOOK_PATH.md)).

## Git note (local checkout)

If this folder uses a **separate git directory** (a `.git` file with `gitdir: ...engineering-playbook.git`), that is still a normal Git work tree; `git status`, remotes, and submodules behave the same. After you add a GitHub remote and push, cloning the repo elsewhere will typically give you a standard `.git` directory. If you prefer one folder only, clone fresh from GitHub into `engineering-playbook` and retire the local pair.

## Cursor-only work bundle (no GitHub on target machine)

To install the playbook on a **work laptop** with **Cursor only** (locked-down GitHub, email-sized transfer), build a zip on your personal machine:

```bash
./packaging/scripts/build-cursor-work-zip.sh
```

See [`packaging/README.md`](packaging/README.md). Output: `packaging/dist/cursor-work-playbook.zip` — unzip on the work machine, open that folder in Cursor, then follow `00-START-HERE.md` or paste the prompt in `PASTE-IN-CURSOR-CHAT.md`.

## License

Use and adapt internally as needed; add a `LICENSE` file when you publish the repo.
