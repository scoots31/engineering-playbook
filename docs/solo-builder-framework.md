# Solo Builder Framework — Working Document
**Started:** 2026-04-20
**Updated:** 2026-04-20
**Status:** Design sprint skill built. Brainstorming integration next.

---

## The Core Problem

Solo builders using Claude or Cursor drift toward waterfall. The phase model (Brainstorm → Research → Planning → Build → QA → Deploy) feels sequential, so each phase gets completed before the next starts. There's no external forcing function — no standup, no sprint end, no teammate waiting — to say "good enough, move."

The agile reframe: **replace "phase complete" with "enough to learn from."**

---

## The Missing Team Dynamic

In a real team, judgment is distributed:
- PM says the problem is real
- Tech lead says the approach is buildable  
- Designer says the experience makes sense
- Stakeholders react to something tangible

Solo, you don't have that. Claude defaults to building what you describe rather than challenging whether you're ready to build it.

The skills library we've built is essentially a roster of specialists:
- `grill-me` — skeptical PM
- `agent-room` — architecture review panel
- `tdd` — QA engineer
- `prd-to-plan` — tech lead breaking work into slices
- `discover` — the day-one engineer/UX conversation
- `design-sprint` — the UX designer producing the shared artifact

What's missing is the **connective tissue** — a flow, a sequence, gates that tell you when to move and who to call next.

---

## The Central Insight: UX as Rosetta Stone

At Scott's day job, the Figma design is not a deliverable — it's a **shared language**. It's the thing everyone points at. Engineers, stakeholders, PMs, data people all react to it. Requirements get clarified because someone looks at a mockup and asks "where does this number come from?" Stakeholders give better feedback because they're reacting to something tangible.

Solo with Claude today, UX comes last because Claude defaults to building what's technically tractable. The sequence gets inverted — build the backend, then skin it. You never have the shared artifact to pressure-test your thinking against.

**The missing piece is a Figma-equivalent moment that has to happen before Claude writes code.**

The design artifact surfaces two categories of work that couldn't be seen before:
- **Visible scope** — every element on screen becomes a build/defer decision
- **Implied infrastructure** — backend logic, data models, APIs that must exist before the interface works. A simple-looking toggle may imply a historical data pipeline. The design doesn't show this — but it's what surfaces the question.

---

## The Design Sprint as the Core Gate

Between Discovery and Planning sits a **Design Sprint** — a short, timeboxed collaborative session where you and the AI produce a working visual good enough to make real decisions from. Not pixel-perfect. Good enough to point at.

That HTML artifact becomes the Rosetta Stone for four conversations:
- **Data** — "Where does this field come from? Do we have this in the API?"
- **Process** — "How does someone actually get from this screen to that one?"
- **Scope** — "Is this element in Phase 1 or not?" — organized by screen
- **Phase start** — the build begins from something concrete, not from a description

The design artifact also collapses two steps into one: it's not a Figma that has to be translated into code — it's HTML that **becomes** the starting point for the frontend.

The output is two things: the HTML screens + a **deferred decisions log** that captures both visible scope decisions and implied infrastructure decisions, organized by screen. That log feeds directly into `prd-to-plan`.

---

## Two Entry Points — Not One

The framework has two distinct starting points depending on what the solo brings:

**Entry 1 — You know the solution.**
The idea is clear. Brainstorming isn't needed. Go straight to Discover → Design Sprint → Plan → Build. The solo brings the idea; the AI runs the discovery conversation and produces the design artifact.

**Entry 2 — You're exploring an idea.**
The problem is real but the solution isn't clear yet. Brainstorming is the right first step. But brainstorming changes when the design sprint is available — it doesn't have to stay abstract. A rough sketch mid-brainstorm gives the conversation something to react to. Data questions surface. Process gaps appear. Scope becomes visible early. The brainstorm produces directional clarity AND a rough visual, both of which feed into Discover.

This is how it works in a real room. Nobody brainstorms in pure text for an hour and then draws later. The sketch happens during ideation — someone puts something on the whiteboard and the conversation gets sharper immediately.

**The brainstorming skill needs to incorporate this.** A rough sketch mid-session is not the design sprint output — it's a thinking tool. The design sprint comes after Discover and produces the real artifact. But the brainstorm sketch is what gets the idea clear enough for Discover to be productive.

---

## Three Design On-Ramps

All three lead to the same place: a visual artifact everyone can point at.

**On-ramp 1 — From scratch**
Warmer/colder loop. Structure first pass → structure warm → skin direction question → skin pass → approved hero screen → extend to all screens → walk-through conversation → deferred decisions log.

**On-ramp 2 — Figma exists**
Import via Figma MCP. Design sprint uses it as source of truth. Discovery brief provides the story layer on top.

**On-ramp 3 — Reference exists**
"Make it feel like ESPN" or "reference this screenshot." System uses it as aesthetic constraint, produces something in that direction. `awesome-design-md` skill handles aesthetic extraction.

The system asks one question to route: **"Do you have a Figma, a reference, or are we starting from scratch?"**

---

## The Solo System Assumption

The solo cannot produce the design artifact themselves — the system must produce it collaboratively. The solo brings:
- The idea
- Domain knowledge ("that field won't exist until Phase 2")
- "Warmer / colder" judgment — the most important contribution

The AI brings:
- Design execution
- The HTML artifact
- Walk-through questions that surface build/defer decisions
- The deferred decisions log

This works because most people can't describe what they want visually until they see something wrong. The design conversation is not requirements gathering — it's a series of warmer/colder moments.

---

## Always-On Skills

These four skills activate when the user chooses **auto-pilot** or **assisted** mode. In bare mode (the default), they do not load. Once activated, they persist for the session — they do not reload on each skill invocation.

| Skill | Active across | Function |
|-------|--------------|----------|
| `process-mapper` | Discover → Phase Test | Maintains as-is + to-be process maps. Cross-references screens, slices, and test scenarios against the agreed process. Flags drift. |
| `product-continuity` | All phases, all sessions | Captures decisions with reasoning, outstanding questions, assumptions, risks, changes, glossary, session logs, and target state documentation. Updates handoff at session end. |
| `framework-health` | All phases, all sessions | Background health monitor. Checks signals — file existence, handoff, backlog At a Glance — not full document reads. Surfaces one issue at a time with recovery path. Silent when healthy. Never blocks. |
| `retrospective` | All phases, all sessions | Flag mode captures observations in the moment (via product-continuity). Retro mode processes at phase end and after phase test — patterns, root causes, proposed fixes. Evolves the playbook from real usage. |

---

## The Framework Flow

```
ENTRY POINT
│
├── Exploring an idea?
│   └── 0. BRAINSTORM (enhanced)
│          └── brainstorming skill — idea exploration + rough sketch mid-session
│          └── Output: directional clarity + rough visual → feeds Discover
│          └── ← NEEDS REVISION to incorporate design sprint sketch moment
│
└── Know what you want to build?
    └── Skip to Discover
    
1. DISCOVER
   └── discover skill — narrative conversation, beginning to end use case
   └── process-mapper activates — as-is process documented (manual or digital), to-be map agreed and validated
   └── Output: discovery-brief.md + docs/process/as-is-[name].md + docs/process/to-be-[name].md + design on-ramp decision

1.5 TECH CONTEXT  ← BUILT
   └── Routes: Solo → questions to build stack · Bayer → which profile?
   └── Bayer profiles: bayer-aurora (C7/Spectrum) · more added as needed
   └── Output: docs/tech-context.md — referenced by every downstream skill
   └── Infrastructure slices identified here — prerequisites before any feature slice

2. DESIGN SPRINT  ← BUILT
   └── On-ramp A: from scratch → hero screen → warmer/colder → all screens → walk-through
   └── On-ramp B: Figma import → read via MCP → story layer on top
   └── On-ramp C: reference → aesthetic constraint → produce in that direction
   └── process-mapper cross-references screens against to-be map — gaps flagged and decided
   └── Output: docs/design/sprint-[id].html (all screens) + deferred-decisions.md + to-be map annotated with screen refs

2.5 DATA SCAFFOLD  ← BUILT (runs before or alongside design review)
   └── Generates realistic fake data for all screen data entities
   └── Creates mock data layer in data/mock/ — one seam, easy to swap
   └── Output: data/mock/[entity].json + docs/data-mapping.md (proto-API contract)
   └── Mock indicator badge on screens during development

2.6 DESIGN REVIEW  ← BUILT (iterative loop — runs as many rounds as needed)
   └── Round 1: full first pass, all screens, define initial slices, trigger spikes
   └── Round N: refine slices, promote to Ready, update backlog
   └── process-mapper cross-reference every round — coverage map against to-be, uncovered steps surfaced as decisions
   └── Process anchor required on every slice before it reaches Ready
   └── Build signal: enough slices Ready to form a coherent Phase 1 starting point
   └── Continues in parallel with build for remaining slices
   └── Output: docs/backlog.md — ID, Name, Process Anchor, Description, Dependency, Status per slice
             + review log appended each round

3. PLAN
   └── prd-to-plan → phases sequenced from backlog (Ready slices), by risk not comfort
   └── to-issues → GitHub issues from Ready slices, each referencing design screen

4. BUILD  ← BUILT (solo-build skill)
   └── Tracer bullet first — thinnest path through full journey before expanding
   └── Journey order — first screen before second, dependencies block
   └── Four anchors required before starting any slice:
       design anchor (screen + element) · data anchor (mock fields) · done anchor (criteria) · process anchor (to-be step)
   └── Mid-build discoveries surfaced immediately — never silently resolved
   └── Code-complete → status: In QA → hand to solo-qa

5. QA / ACCEPTANCE  ← BUILT
   └── Triggered automatically — solo-build invokes code-review-and-quality on code-complete
   └── code-review-and-quality → 7 checks: pattern, data sourcing, expandability, cleanliness, scope, docs, stack
   └── On pass: logs confirmation in backlog → auto-invokes solo-qa
   └── solo-qa Part 1 (AI) → gate check + full spec review + active testing with evidence + design fidelity
   └── solo-qa Part 2 (solo) → browser sign-off: visual, behavior, criteria in practice
   └── Unexpected discovery → qa-triage: classifies (bug / missing req / regression), scopes, routes, logs
   └── Done = code review logged + AI verified with evidence + solo confirmed in browser
   └── No solo sign-off while an open missing requirement exists — define or defer it first

5.5 PHASE TEST  ← BUILT (/phase-test)
   └── Solo invokes explicitly when all phase slices are Done — deliberate decision, not automatic
   └── Stage 1: Environment readiness — pre-flight gate, nothing runs until this passes
   └── Stage 2: Use case creator — derives test plan from discovery brief + design + backlog
   └── Stage 3: Data specialist — mock→real swap confirmed, API/DB read/write verified
   └── Stage 4 + 5: Tester + Regression specialist (run together)
       Tester walks every scenario with named evidence
       Regression re-walks all Done slices, checks integration points between slices
   └── Stage 6: Acceptance reviewer — PM lens: does what was built match discovery brief intent?
   └── Stage 7: Gate decision — OPEN (deploy) or HOLD (specific items to resolve)
   └── HOLD: fix affected items, re-test affected scenarios only — no full re-run
   └── Failures at any stage → qa-triage (test run continues on unaffected scenarios)
   └── Output: docs/phase-test-[phase]-[date].md
   └── Gate OPEN → phase completion record appended to backlog.md:
       "Phase [N] Complete — tested and ready to deploy" + what was delivered + what comes next

6. DEPLOY  ← BUILT
   └── Reads docs/tech-context.md — deploy method entirely determined by stack
   └── Confirms phase test gate OPEN before anything runs
   └── Confirms all phase branches merged
   └── Routes to correct deploy method:
       Method A: CI/CD triggered by merge (GitHub Actions, etc.)
       Method B: MCP tool triggered (Railway, Vercel, etc.)
       Method C: Manual CLI (command from tech-context)
       Method D: Not yet defined → asks questions, updates tech-context, then deploys
   └── Verifies environment is actually live — not just pipeline green
   └── Updates phase completion record: Complete → Tested → Deployed
```

---

---

## Key Constraints

- Works in both Claude Code and Cursor — never assume one tool
- Design artifact is HTML, not Figma — it's the first real output of the build
- System must produce design collaboratively — cannot assume solo has design skills
- Agile not waterfall — "enough to learn from" not "phase complete"
- Timeboxed — every phase has a natural end, not a completion criteria
- Portable — being built to work for any solo, not just Scott
- Two entry points — the system routes to brainstorm or discover based on clarity of the idea

---

## Skills Built for This System

| Skill | Role in System | Status |
|-------|---------------|--------|
| `start` | Front door — reads the opening, routes to Brainstorm or Discover automatically | ✅ Built |
| `tech-context` | Establishes stack + constraints before design — routes to profile or builds from questions | ✅ Built |
| `research-spike` | Timeboxed investigation of a specific unknown — callable from any phase | ✅ Built |
| `design-review` | Iterative review loop — defines slices, manages backlog, signals when to build | ✅ Built |
| `data-scaffold` | Generates realistic fake data + mock layer + data mapping doc (proto-API contract) | ✅ Built |
| `discover` | Day-one conversation, sets the table, routes to design on-ramp | ✅ Built |
| `design-sprint` | Produces HTML artifact + deferred decisions log | ✅ Built |
| `brainstorming` | Product exploration — sketch moment, research routing, feeds Discover | ✅ Built |
| `grill-me` | Stress-tests plans before committing | ✅ Built |
| `to-prd` | Synthesizes context into PRD | ✅ Built |
| `prd-to-plan` | Phases implementation by risk, from deferred decisions log | ✅ Built |
| `to-issues` | Breaks plan into GitHub issues | ✅ Built |
| `agent-room` | Multi-perspective decisions | ✅ Built |
| `solo-build` | Slice-by-slice execution — four anchors, journey order, dependency blocking | ✅ Built |
| `solo-qa` | Two-part verification — active AI testing with evidence + solo browser sign-off required for Done | ✅ Built |
| `qa-triage` | Routes unexpected QA discoveries — bugs, missing requirements, regressions — to the correct path | ✅ Built |
| `phase-test` | Full-phase testing orchestrator — 7 specialist lenses, gate decision, required before deploy | ✅ Built |
| `tdd` | Test-driven build (technique, invoked from solo-build) | ✅ Built |
| `code-review-and-quality` | 7-check quality gate — auto-invoked by solo-build, chains to solo-qa on pass | ✅ Built |
| `principal-engineer` | Architecture review lens — invokable at consequential moments, not always-on | ✅ Built |
| `process-mapper` | As-is + to-be process maps — always-on from discover through phase test, never invoked by user | ✅ Built |
| `product-continuity` | Institutional memory — sessions, decisions, questions, assumptions, risks, changes, glossary, target state, handoff | ✅ Built |
| `framework-health` | Background monitor — signal checks only, one issue at a time, silent when healthy, never blocks | ✅ Built |
| `retrospective` | Continuous learning — flags in the moment, processes at phase end, evolves the playbook | ✅ Built |
| `deploy` | Stack-driven deploy — reads tech-context, routes to correct method, confirms gate open, verifies environment live | ✅ Built |
| `frontend-design` | Aesthetic guidance for HTML artifact | ✅ Built |
| `awesome-design-md` | On-ramp 3 — reference-based design | ✅ Built |

---

## Next Session Picks Up At

**The gates** — what makes each phase transition unavoidable without feeling like bureaucracy? The deferred decisions log gates Design Sprint → Plan. Others still need definition.

**How phases reshape** — now that the full entry flow is solved (Start → Brainstorm or Discover → Design Sprint → Plan → Build), revisit whether the original phase names still make sense or need renaming for clarity.

---

## Companion framework: Workshop

SBF covers product-shaped work. Most solo-builder work isn't that shape. **Workshop** (see `workshop/README.md`) is the companion for spike-shaped and tool-shaped work.

Scope boundary: SBF handles anything with external users or indefinite lifespan. Workshop handles everything else. The `scope-check` skill at Workshop's entry holds the line; `land` at Workshop's exit provides the bridge back to SBF when a spike graduates into a product.

Workshop's load-bearing principles are deliberately the inverse of SBF's: timebox over gates, outcome over process, disposable by default, single artifact, explicit graduation.
