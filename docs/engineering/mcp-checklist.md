# MCP checklist (per product)

Use [Model Context Protocol](https://code.claude.com/docs/en/mcp) when a project genuinely needs **external tools, APIs, or data** beyond the repo. Do not add MCP servers “because we can.”

## Before adding a server

- [ ] **Purpose** — What user or agent task does this unblock?
- [ ] **Least privilege** — Narrow scopes, read-only where possible, no broad filesystem unless required.
- [ ] **Secrets** — API keys live in env or secret manager, not committed config.
- [ ] **Default off** — Can new contributors work without it? Document opt-in.
- [ ] **Ownership** — Who upgrades the server when the vendor API changes?
- [ ] **Failure mode** — What happens when MCP is down (degraded mode, clear error)?

## Configuration surface

- Claude Code commonly uses **`.mcp.json`** at repo root (and team settings); see current docs for precedence with `.claude/settings.json`.
- **Never commit** real tokens; use env var references per tool docs.

## Template

See [`templates/mcp.json.example`](../../templates/mcp.json.example) for a minimal structural example (replace placeholders, validate JSON).

## Review cadence

Re-read MCP config when:

- upgrading Claude Code or MCP SDKs,
- onboarding a new collaborator,
- shipping anything that touches **PII, payments, or production** data paths.
