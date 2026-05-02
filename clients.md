# Client Context Registry

Known client design libraries. Read by the `client-context-design` skill when invoked without a declared project path.

Each entry points to the local path of the client's context file. Every person using the framework clones each library to the same path on their machine.

---

| Client | Context File | Local Path | Notes |
|--------|-------------|------------|-------|
| Bayer | context.md | `~/Developer/bayer-ux-library/` | Production design system. See BUILD-BRIEF.md for library setup. |

---

## Adding a New Client

1. Create a design library repo with the standard structure (README, BUILD-BRIEF, context.md, components/, tokens/, patterns/, regional/)
2. Add a row to this table
3. Clone the repo to the listed local path on every machine that will use it
4. To use in a project: add `client_context: [path]/context.md` to the project's `CLAUDE.md`
