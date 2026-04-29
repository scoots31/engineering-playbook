---
name: tech-context
description: Establishes the technical stack, architecture constraints, and engineering principles before design review, planning, or build. Routes to a known profile (Bayer Aurora, etc.) or asks questions to build one for a general solo project. Output is docs/tech-context.md — referenced by design review, data scaffold, plan, and build for the life of the project.
---

# Tech Context

*Established once. Referenced everywhere. Nothing gets built without it.*

**Core question:** "What are we building on, and what constraints does that create?"

Tech context is not architecture design. That comes later with a principal engineer lens. This is the foundational information that makes every downstream decision — design, data, slices, build — technically grounded from the start.

It runs after Discover and before Design Sprint. By the time screens are being designed and slices are being defined, the technical constraints are already known. Infrastructure slices get identified correctly. Done criteria get written with the right technical specificity. Dependencies get typed accurately.

---

## Routing — Two Paths

### Path 1 — Known Profile (Bayer or other org with established stack)

Ask two questions:

**Question 1:** "Is this a solo personal project or an organizational project?"

If organizational: **Question 2:** "Which organization and platform?"
- Bayer → Aurora? → load `profiles/bayer-aurora.md`
- Bayer → [other platform]? → load that profile, or create one if it doesn't exist
- [Other org] → load that org's profile, or create one

Load the profile. Confirm the key constraints with the solo before proceeding:
> "I've loaded the [profile name] tech profile. For this project: [3-4 key constraints from the profile]. Does this match the context you're working in?"

If yes — produce `docs/tech-context.md` from the profile. Done.
If something differs — note the delta, update for this project only. The profile stays canonical.

### Path 2 — General Solo (no established profile)

Ask questions to establish the stack. One at a time. Stop when there's enough to fill the tech context document.

**Questions to cover:**

1. **Deployment target** — "Where does this live when it's done? Web app, internal tool, mobile, API, something else?"

2. **Frontend** — "What's your frontend stack, or do you want a recommendation?" 
   - If they have one: note it
   - If they want a recommendation: suggest based on project type (React + TypeScript for most web work, simpler for internal tools)

3. **Backend / data** — "Does this need a backend, or is it frontend-only connecting to existing APIs?"
   - If backend needed: "What language/framework, or do you want a recommendation?"

4. **Component library** — "Are you using a component library, or building from the design system we created?"

5. **API communication** — "How is the frontend talking to data? REST, GraphQL, direct DB?"

6. **Auth** — "Does this need authentication? Handled by something external or built in?"

7. **Deployment / hosting** — "Where is this deployed? Railway, Vercel, internal server, something else?"

8. **Existing principles** — "Do you have coding standards, linting rules, or engineering principles to follow, or should we establish them?"

When enough is known, summarize and confirm:
> "Based on what you've shared: [brief stack summary]. Before I write this up — anything else that would constrain how we build?"

Then produce `docs/tech-context.md`.

---

## Output — docs/tech-context.md

Created once per project. Referenced by design review, data scaffold, plan, and build. Never recreated — only updated when the stack changes.

```markdown
# Tech Context — [Project Name]
**Profile:** [Bayer Aurora / General Solo / Custom]
**Created:** [YYYY-MM-DD]
**Last updated:** [YYYY-MM-DD]

---

## What's Being Built

[One paragraph. What type of thing this is — module, app, tool, API — 
and any platform constraints that affect design and build decisions.]

---

## Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Frontend | [React + TypeScript / other] | |
| Component library | [Element / custom / none] | |
| API communication | [RTK Query / REST / GraphQL] | |
| Backend | [Python Flask / Node / de-scoped] | |
| Auth | [C7/Gigya / Clerk / custom / none] | |
| Database | [PostgreSQL / none / external] | |
| Deployment | [Spectrum C7 / Railway / Vercel] | |
| CI/CD | [GitHub Actions / other] | |
| Linting | [ESLint Airbnb / other] | |
| Testing | [Jest / pytest / TBD] | |

---

## Architecture Constraints

[Things the design and build must account for that aren't obvious from the stack alone.]

- [Constraint 1 — e.g., "Module loads inside Aurora shell — no login screen, no global nav"]
- [Constraint 2 — e.g., "Backend de-scoped — UI calls existing APIs only"]
- [Constraint 3]

---

## Engineering Principles

[Standards and rules that apply to this project. From profile or established in this session.]

- [Principle 1 — e.g., "TypeScript strict mode — no any types"]
- [Principle 2 — e.g., "ESLint Airbnb ruleset — enforced in CI"]
- [Principle 3 — e.g., "No secrets in code — Faststore/Fastlight for config"]
- [Principle 4]

---

## Branching and Delivery

- **Repo strategy:** [Poly-repo / Mono-repo]
- **Branches:** [development → non-prod · main/release → prod]
- **Feature branches:** [feature/<ticket-id>]
- **PR requirements:** [Reviewer count, teams]
- **CI trigger:** [On merge / manual]

---

## Infrastructure Slices Required

[Slices that must be Done before any feature slice can start. 
Identified from the tech stack and platform constraints.]

| Slice | Description | Blocks |
|-------|-------------|--------|
| [Name] | [What it sets up] | [What depends on it] |

---

## Secrets and Config

[How config and secrets are managed for this project.]

- [Pattern — e.g., "Faststore/Fastlight for UI config parameters"]
- [Pattern — e.g., "Never commit .env with real values"]

---

## Runtime

[How to start the app locally. Used by the Solo Companion to surface a Start & Review button
when the app is not running. Omit for projects with no local server (static exports, APIs without
a dev server, etc.).]

- **Start command:** `[full command to start the local server, run from the project root]`
- **App port:** `[port the server listens on — used for the port-alive check]`

---

## Profile Reference

[Which profile this was built from, or "general solo" if built from scratch.]
[Profile path if applicable: ~/Developer/engineering-playbook/profiles/bayer-aurora.md]
```

---

## How Downstream Skills Use This

**Design Sprint** — architecture constraints inform what can be designed. Aurora module constraints mean no login screen in the designs.

**Data Scaffold** — stack determines mock data format and the data layer pattern. RTK Query projects get a mock RTK slice. Flask projects get a mock Python module.

**Design Review** — infrastructure slices get added to the backlog based on the tech context. These are required prerequisites, not features.

**Plan** — slice done criteria are written with technical specificity from the stack. "RTK Query endpoint wired and returning mock data" not "data displays correctly."

**Build** — the tech context is the build bible. Stack, principles, branching model, secrets pattern — all referenced here.

**Solo Companion** — reads `Start command` and `App port` from the `## Runtime` section at sync time. These power the Start & Review button — when a slice has a review URL and the app is stopped, the companion starts it automatically. If the Runtime section is absent, the companion falls back to Review-only mode (no Start & Review).

---

## Adding a New Profile

When a new organizational context comes up that will be used again:

1. Create `~/Developer/engineering-playbook/profiles/[org]-[platform].md`
2. Document: what's being built, stack table, architecture constraints, engineering principles, branching/delivery, infrastructure slices, secrets/config
3. Reference it in future tech-context runs for that context

Current profiles:
| Profile | Path | Context |
|---------|------|---------|
| Bayer Aurora | `profiles/bayer-aurora.md` | Aurora modules via C7/Spectrum |

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Running tech context after Design Sprint | Screens get designed without platform constraints | Always before Design Sprint |
| Running tech context after Design Review | Infrastructure slices get missed | Always before Design Review |
| Rebuilding tech context each session | Loses continuity | Create once, update when stack changes |
| Using profile defaults without confirming | Project may differ from profile | Always confirm key constraints before proceeding |
| Skipping infrastructure slices | Feature slices have no foundation to build on | Infrastructure slices are always first in the backlog |
