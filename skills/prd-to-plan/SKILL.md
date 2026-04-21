---
name: prd-to-plan
description: Turn a PRD into a sequenced, multi-phase implementation plan using tracer-bullet vertical slices. Reduces integration risk by ordering work so each phase is demoable and de-risks the next. Use when user wants to plan implementation from a PRD, asks "how should we sequence this?", or wants a phased build plan before breaking into issues.
---

# PRD to Plan

Turn a PRD into a sequenced, multi-phase implementation plan. The goal is not just task breakdown — it is finding the sequence that reduces integration risk fastest.

## Process

### 1. Load the PRD

Work from whatever is in the conversation. If the user passes a GitHub issue number or URL, fetch it with `gh issue view <number>`.

### 2. Explore the codebase

If you haven't already, explore the repo to understand:
- Which existing systems the PRD will touch
- What data models are already in place
- Where the integration seams are (API boundaries, DB schema, auth, external services)

### 3. Identify the integration seams

Before sequencing anything, list every layer the feature cuts through:
- Data layer (schema, migrations, data model changes)
- Business logic / service layer
- API / backend endpoints
- Frontend / UI
- External integrations (third-party APIs, webhooks, auth)
- Tests and observability

Call out any seams that are HIGH RISK — places where assumptions made early will be painful to undo later.

### 4. Design tracer-bullet vertical slices

Break the PRD into vertical slices. Each slice cuts through ALL integration layers end-to-end, delivering a narrow but complete path.

<vertical-slice-rules>
- Each slice must be independently demoable or verifiable
- Prefer many thin slices over few thick ones
- The first slice should prove the riskiest assumption in the system
- Later slices build on confirmed foundations, not on hope
- Horizontal slices (e.g. "build all the DB models first") are not allowed — they defer integration risk
</vertical-slice-rules>

### 5. Sequence by risk, not by comfort

Order the slices so that:
1. **Phase 1** proves the hardest, most uncertain, or most load-bearing part of the system first
2. Each subsequent phase can be built with confidence because the prior phase resolved its dependencies
3. The last phases are additive (polish, edge cases, non-critical paths)

For each phase, show:
- **Phase name** and short description
- **Slices in this phase** (numbered list, one-line each)
- **What this phase proves or de-risks**
- **Blocked by** (prior phases or external dependencies)
- **Definition of done** — how you know this phase is complete

### 6. Flag open questions

List any decisions that must be made before implementation can start:
- Architectural choices with meaningful tradeoffs
- Missing information in the PRD
- Dependencies on other teams, systems, or data

### 7. Present and confirm

Show the full plan to the user. Ask:
- Does the phase sequencing feel right?
- Are the right risks being addressed first?
- Are there slices that should be merged, split, or reordered?
- Are any open questions blockers, or can we proceed with a stated assumption?

Iterate until approved.

### 8. Optional next step

Offer to run `/to-issues` to convert the approved plan into GitHub issues in dependency order.
