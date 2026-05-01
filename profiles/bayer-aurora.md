# Tech Profile — Bayer Aurora (C7 / Spectrum)
**Platform:** Aurora via Spectrum (C7)
**Context:** Internal modules loaded into the Aurora shell — not standalone apps
**Last updated:** 2026-04-20

---

## What's Being Built

Aurora modules are not standalone applications. They are discrete frontend units loaded into the Aurora shell via C7 routing (e.g., `/aurora/admin/...`). The shell handles auth, navigation chrome, and entitlements. The module provides the UI for a specific domain.

**Implications for design and build:**
- No login screen — auth is handled by C7 (Gigya tokens)
- No global nav — that's Aurora's job
- No route-level access control to build — entitlements are C7-managed
- The module's entry point is a route, not an `index.html`

---

## Repository Strategy

**Pattern:** Poly-repo
- APIs (services) live in separate repos from UI code
- UI repos may contain a `services/` folder — these are client-side API connectors, not backend logic
- One module = one repo unless significant shared code requires a mono-repo

**Branching model:**
- `development` → non-production environment
- `main` / `release` → production environment
- Feature branches per story: `feature/<story-or-ticket-id>`
- Work done on feature branches, merged via PR into `development`
- PRs require at least one reviewer from the owning team (Arrow / Endeavour)

**Promotion flow:**
- Merge to `development` → non-prod deployment (automatic or manual CI trigger)
- Merge to `main`/`release` → prod deployment via CI/CD

---

## Frontend Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Framework | React + TypeScript | Required standard |
| Component library | Element | Bayer's internal component library |
| API communication | RTK Query | Preferred pattern for UI → API calls |
| Linting | ESLint — Airbnb or Facebook ruleset | Enforces consistency + security guardrails |
| Type safety | TypeScript strict mode | Reduces ambiguity, enforces structure |

**TypeScript** is not optional — it enforces structure and reduces ambiguity in shared codebases. ESLint catches formatting, consistency, and basic security issues (e.g., prevents secrets in code).

---

## Backend Stack

Backend is explicitly de-scoped for Aurora module work. Frontend modules call existing APIs — they do not own backend logic, databases, or infrastructure.

If API work is needed, it is handled separately by engineering and lives in its own repo.

---

## Authentication and Access

- **Auth:** Handled entirely by C7. Aurora modules inherit Gigya tokens automatically. Do not build login flows.
- **Token exchange:** Ocelot handles downstream token exchange (e.g., to Commerce Cloud or other services). The UI does not manage this.
- **Entitlements:** Menu visibility and route access are governed by C7 entitlements. Restrict modules to roles (e.g., super-admin) through entitlement config — not in-module access control code.

---

## Secrets and Configuration

| Context | Pattern |
|---------|---------|
| UI modules | Faststore / Fastlight parameters — config stored outside code, stable references, values differ per environment |
| Backend / API | Vault (KV preferred over legacy secrets) — requires role IDs and role secrets via Fort Knox |

**Rule:** Never store secrets in code. Never commit `.env` files with real values.

---

## Observability

Bayer's standard observability tool is not declared in this profile. Before the first build on any Aurora project, confirm with the team:
> "Which observability tool is in place for this project — Datadog, CloudWatch, or something else? Is it org-mandated or a team choice?"

Record the answer in `docs/tech-context.md` for the project. If observability is required, add an observability setup infrastructure slice to the backlog before any feature slices start.

---

## CI/CD

- **System:** GitHub Actions (standard — replaces older AWS CodeBuild)
- **Non-prod:** Triggered on merge to `development` (or manually)
- **Prod:** Triggered on merge to `main`/`release`
- **Deployment:** Spectrum packages the module and deploys (e.g., to S3), integrates into Aurora

---

## Quality Gates

| Gate | Tool | When |
|------|------|------|
| Type safety | TypeScript | During development + CI |
| Linting | ESLint (Airbnb/Facebook) | During development + CI |
| Code analysis | CodeQL / SonarQube | Optional — add after initial delivery |

CodeQL and SonarQube are not required for early iterations. Layer them in when engineering formally takes ownership.

---

## Testing

- **Framework:** Jest (implied standard)
- **Approach:** Tests written after functionality exists, not TDD-first for this context
- AI tooling can generate tests based on described workflows and UI behavior
- No strict testing mandate for early iterations — coverage expectations set per team

---

## Local Dev Setup

- Cursor generates project scaffolding, READMEs, and run instructions
- Main friction point: API keys and secrets (handled via Faststore/Fastlight references in config)
- Devs should be able to run the module locally against non-prod APIs from day one

---

## Infrastructure Slices — Always Required

Every Aurora module build requires these slices before any feature slices can start:

| Slice | Description | Blocks |
|-------|-------------|--------|
| Project scaffold | React + TypeScript + ESLint + Element setup | Everything |
| Repo setup | Poly-repo created, branching model established, CI workflows configured | Feature branches |
| RTK Query setup | Base API client configured, non-prod endpoint wired | Any slice that calls an API |
| Spectrum config | C7 module registration, route configured in Aurora | Any slice visible in Aurora |
| Non-prod deployment | First CI run, module visible in Aurora non-prod | All QA |

These are not optional. They are not features. They are prerequisites. Every feature slice depends on them.

---

## Profile Notes

- Backend scope expansion → create `bayer-aurora-fullstack.md`
- Different platform (non-Aurora Bayer project) → create `bayer-[platform].md`
- This profile covers C7/Spectrum Aurora module work only
