# Solo Builder Framework

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
- `tdd` — QA engineer
- `prd-to-plan` — tech lead breaking work into slices
- `discover` — the day-one engineer/UX conversation
- `design-sprint` — the UX designer producing the shared artifact

What's missing is the **connective tissue** — a flow, a sequence, gates that tell you when to move and who to call next.

---

## The Central Insight: UX as Visual Contract

At Scott's day job, the Figma design is not a deliverable — it's a **shared language**. It's the thing everyone points at. Engineers, stakeholders, PMs, data people all react to it. Requirements get clarified because someone looks at a mockup and asks "where does this number come from?" Stakeholders give better feedback because they're reacting to something tangible.

Solo with Claude today, UX comes last because Claude defaults to building what's technically tractable. The sequence gets inverted — build the backend, then skin it. You never have the shared artifact to pressure-test your thinking against.

**The missing piece is a Figma-equivalent moment that has to happen before Claude writes code.**

The design artifact surfaces two categories of work that couldn't be seen before:
- **Visible scope** — every element on screen becomes a build/defer decision
- **Implied infrastructure** — backend logic, data models, APIs that must exist before the interface works. A simple-looking toggle may imply a historical data pipeline. The design doesn't show this — but it's what surfaces the question.

---

## The Design Sprint as the Core Gate

Between Discovery and Planning sits a **Design Sprint** — a short, timeboxed collaborative session where you and the AI produce a working visual good enough to make real decisions from. Not pixel-perfect. Good enough to point at.

That HTML artifact becomes the visual contract and decision surface for four conversations:
- **Data** — "Where does this field come from? Do we have this in the API?"
- **Process** — "How does someone actually get from this screen to that one?"
- **Scope** — "Is this element in Phase 1 or not?" — organized by screen
- **Phase start** — the build begins from something concrete, not from a description

The design artifact also collapses two steps into one: it's not a Figma that has to be translated into code — it's HTML that **becomes** the starting point for the frontend.

The output is two things: the HTML screens + a **deferred decisions log** that captures both visible scope decisions and implied infrastructure decisions, organized by screen. That log feeds directly into `prd-to-plan`.

---

## Entry Points

The framework has three distinct starting points depending on what the solo brings:

**Entry 1 — You know the solution.**
The idea is clear. Brainstorming isn't needed. Go straight to Discover → Design Sprint → Plan → Build. The solo brings the idea; the AI runs the discovery conversation and produces the design artifact.

**Entry 2 — You're exploring an idea.**
The problem is real but the solution isn't clear yet. Brainstorming is the right first step. But brainstorming changes when the design sprint is available — it doesn't have to stay abstract. A rough sketch mid-brainstorm gives the conversation something to react to. Data questions surface. Process gaps appear. Scope becomes visible early. The brainstorm produces directional clarity AND a rough visual, both of which feed into Discover.

This is how it works in a real room. Nobody brainstorms in pure text for an hour and then draws later. The sketch happens during ideation — someone puts something on the whiteboard and the conversation gets sharper immediately.

**The brainstorming skill needs to incorporate this.** A rough sketch mid-session is not the design sprint output — it's a thinking tool. The design sprint comes after Discover and produces the real artifact. But the brainstorm sketch is what gets the idea clear enough for Discover to be productive.

**Entry 3 — You have prior work outside the framework.**
Discovery, planning, notes, and decisions exist — but not in SBF format. Don't restart. Run `onboard` — it reads the project directory, semantically matches content to gate artifacts, synthesizes with confirmation, surfaces what's missing as targeted discussion prompts, and places the project at the correct starting phase. From there, normal SBF flow takes over.

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

These four skills activate when the user chooses **guided** or **piloted** mode. In bare mode (the default), they do not load. Once activated, they persist for the session — they do not reload on each skill invocation.

| Skill | Active across | Function |
|-------|--------------|----------|
| `process-mapper` | Discover → Phase Test | Maintains as-is + to-be process maps. Cross-references screens, slices, and test scenarios against the agreed process. Flags drift. |
| `product-continuity` | All phases, all sessions | Captures decisions with reasoning, outstanding questions, assumptions, risks, changes, glossary, session logs, and target state documentation. Updates handoff at session end. On 21+ day gaps, runs three-check re-entry protocol: codebase state, environment, context validity. |
| `framework-health` | All phases, all sessions | Background health monitor. Checks signals — file existence, handoff, backlog At a Glance — not full document reads. Detects 21+ day session gaps and routes to re-entry. Surfaces one issue at a time with recovery path. Silent when healthy. Never blocks. |
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
│          └── Gate: judgment — clear enough for a productive discovery conversation
│
└── Know what you want to build?
    └── Skip to Discover
    
1. DISCOVER
   └── discover skill — narrative conversation, beginning to end use case
   └── process-mapper activates — as-is process documented (manual or digital), to-be map agreed and validated
   └── Output: discovery-brief.md + docs/process/as-is-[name].md + docs/process/to-be-[name].md + design on-ramp decision
   └── Gate: discovery-brief.md exists + to-be map agreed

1.5 TECH CONTEXT  ← BUILT
   └── Routes: Solo → questions to build stack · Bayer → which profile?
   └── Bayer profiles: bayer-aurora (C7/Spectrum) · more added as needed
   └── Output: docs/tech-context.md — referenced by every downstream skill
   └── Infrastructure slices identified here — prerequisites before any feature slice
   └── Gate: docs/tech-context.md exists

2. DESIGN SPRINT  ← BUILT
   └── On-ramp A: from scratch → hero screen → warmer/colder → all screens → walk-through
   └── On-ramp B: Figma import → read via MCP → story layer on top
   └── On-ramp C: reference → aesthetic constraint → produce in that direction
   └── process-mapper cross-references screens against to-be map — gaps flagged and decided
   └── Output: docs/design/sprint-[id].html (all screens) + deferred-decisions.md + to-be map annotated with screen refs
   └── Optional output: docs/design/handoff/<date>/ — shareable package (HTML + PDF + feedback template) for stakeholder review
   └── Gate: sprint-[id].html + deferred-decisions.md exist

2.5 DATA SCAFFOLD  ← BUILT (runs before or alongside design review)
   └── Generates realistic fake data for all screen data entities
   └── Creates mock data layer in data/mock/ — one seam, easy to swap
   └── Output: data/mock/[entity].json + docs/data-mapping.md (proto-API contract)
   └── Mock indicator badge on screens during development
   └── Gate: data/mock/ populated + docs/data-mapping.md exists

2.6 DESIGN REVIEW  ← BUILT (iterative loop — runs as many rounds as needed)
   └── Round 1: full first pass, all screens, define initial slices, trigger spikes
   └── Round N: refine slices, promote to Ready, update backlog
   └── Reads docs/stakeholder-feedback/*.md as first-class input — per-screen comments become findings, blockers gate Ready
   └── process-mapper cross-reference every round — coverage map against to-be, uncovered steps surfaced as decisions
   └── Data behavior pass — required for every screen with external data: volume, list behavior, nulls, empty/error/loading states
       → Produces data questions log in docs/backlog.md
       → Unresolved question blocks dependent UI slices from Ready
       → Questions resolved via research spike, API check, or stakeholder confirmation
       → Mock data updated after questions resolve, before dependent slices finalize
   └── Process anchor required on every slice before it reaches Ready
   └── Build signal: enough slices Ready to form a coherent Phase 1 starting point
   └── Continues in parallel with build for remaining slices
   └── Output: docs/backlog.md — ID, Name, Process Anchor, Description, Dependency, Status per slice
             + data questions log
             + review log appended each round
   └── Gate: backlog.md with a coherent set of Ready slices for Phase 1

3. PLAN
   └── prd-to-plan → phases sequenced from backlog (Ready slices), by risk not comfort
   └── to-issues → GitHub issues from Ready slices, each referencing design screen
   └── Gate: GitHub issues created for Phase 1 Ready slices

4. BUILD  ← BUILT (solo-build skill)
   └── Tracer bullet first — thinnest path through full journey before expanding
   └── Journey order — first screen before second, dependencies block
   └── Four anchors required before starting any slice:
       design anchor (screen + element) · data anchor (mock fields) · done anchor (criteria) · process anchor (to-be step)
   └── Mid-build discoveries surfaced immediately — never silently resolved
   └── Map-level conflict — if build reveals the to-be map itself is wrong, invoke process-change immediately. Current slice moves to In Review until process-change completes.
   └── Code-complete → status: In QA → hand to solo-qa
   └── Gate (per slice): four anchors confirmed + solo sign-off in browser
   └── Deliverables — slices roll up into deliverables. A deliverable is the agreed body of work a set of slices collectively produce.
       Two types:
       · Screen — output is visible. Reviewed visually in the browser.
       · Logic — output is invisible. Reviewed against evidence (test results, data state, simulated flow through affected screens).
       Three fields per deliverable:
       · Technical spec — what the skill reads. Implementation-level, written for the AI.
       · Solo description — what the solo sees. Plain language, outcome-focused, written for the human.
       · Acceptance criteria — shared contract. AI builds and self-verifies against it. Solo reviews against it. One set of criteria, agreed before build starts.
   └── Integration deliverables — every Screen deliverable with external data gets a companion Logic deliverable for data integration
       · Always sequences after its Screen companion is Accepted
       · Cannot be fully scoped until data questions log is resolved
       · Named: "[Screen Name] — Data Integration"
       · Standard done criteria: API connected, data-mapping.md confirmed, pagination/filter/search, empty/error/loading states, auth
   └── Two review levels: slice approval (unit of work complete) + deliverable acceptance (full body of work done and matching the build contract)
   └── Two views available at any time during build:
       · "show progress" — active deliverable, all slices, current status, acceptance criteria
       · "show plan" — all deliverables across the full build, delivered / in progress / backlog

5. QA / ACCEPTANCE  ← BUILT
   └── Triggered automatically — solo-build invokes code-review-and-quality on code-complete
   └── code-review-and-quality → 7 checks: pattern, data sourcing, expandability, cleanliness, scope, docs, stack
   └── On pass: logs confirmation in backlog → auto-invokes solo-qa
   └── solo-qa Part 1 (AI) → gate check + full spec review + active testing with evidence + design fidelity
   └── solo-qa Part 2 (solo) → browser sign-off: visual, behavior, criteria in practice
   └── Unexpected discovery → qa-triage: classifies (bug / missing req / regression / map-level gap), scopes, routes, logs
   └── Map-level gap — if qa-triage surfaces a missing requirement where the to-be map has no step at all, invoke process-change before QA resumes on that slice
   └── Done = code review logged + AI verified with evidence + solo confirmed in browser
   └── No solo sign-off while an open missing requirement exists — define or defer it first
   └── Integration deliverable acceptance — UX impact check before accepting: does live data produce anything the design didn't account for? If yes → flag for design review, affected UI slices reopen
   └── Deliverable acceptance — when all slices in a deliverable are Done, solo-qa runs a deliverable-level check:
       Screen deliverable: visual pass against acceptance criteria in browser
       Logic deliverable: evidence pass — test results, data state, or simulated flow through affected screens
   └── Gate: all phase slices at ✓ Done status

5.5 PHASE TEST  ← BUILT (/phase-test)
   └── Solo invokes explicitly when all phase slices are Done — deliberate decision, not automatic
   └── Deliverable-structured pass — walks each deliverable in the phase, confirms deliverable acceptance was completed, then verifies all deliverables hold together in integration
   └── Stage 1: Environment readiness — pre-flight gate, nothing runs until this passes
   └── Stage 2: Use case creator — derives test plan from discovery brief + design + backlog
   └── Stage 3: Data specialist — mock→real swap confirmed, API/DB read/write verified
   └── Stage 4 + 5: Tester + Regression specialist (run together)
       Tester walks every scenario with named evidence
       Regression re-walks all Done slices, checks integration points between slices
   └── Stage 6: Acceptance reviewer — PM lens: does what was built match discovery brief intent? If process-level mismatch found, invoke process-change — gate stays HOLD until complete.
   └── Stage 7: Gate decision — OPEN (deploy) or HOLD (specific items to resolve)
   └── HOLD: fix affected items, re-test affected scenarios only — no full re-run
   └── Failures at any stage → qa-triage (test run continues on unaffected scenarios)
   └── Output: docs/phase-test-[phase]-[date].md
   └── Gate OPEN → phase completion record appended to backlog.md:
       "Phase [N] Complete — tested and ready to deploy" + what was delivered + what comes next
   └── Gate: phase-test OPEN required before deploy

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
- Framework writes, solo responds — the framework never asks the solo to open a file and fill it in, and never hands the solo a terminal command to run. All input is captured conversationally; all commands are executed by the AI. If a command requires permission, the AI asks and then runs it. The only exception for file fills is external stakeholders (people outside the conversation) who receive a fillable template because they cannot be interviewed directly.
- Review is always visual — when a build produces something reviewable, the AI serves it or opens it in the browser before asking for feedback. The solo looks at the work, then responds. Feedback on a description of work is not review.
- Output discipline — responses match the weight of the moment. Acknowledgments one sentence. Confirmations: what was produced + next question. No narrating what the solo just saw happen. No paragraph-length sign-offs after approvals.
- Skill names are never user-facing — the action is surfaced in plain language, never the skill name. Quote blocks and prompts shown to the solo must never contain a skill name.
- No abbreviations in user-facing output — SBF, MCP, and any code-identifier-style term never appear in output shown to the solo. "The framework" replaces "SBF" in all user-facing context.

---

## Skills Built for This System

| Skill | Role in System | Status |
|-------|---------------|--------|
| `start` | Front door — reads the opening, routes to Brainstorm, Discover, or Onboard automatically | ✅ Built |
| `onboard` | Brings existing projects into SBF — reads project directory, semantically maps content to gate artifacts, synthesizes with confirmation, places at correct starting phase | ✅ Built |
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
| `solo-build` | Slice-by-slice execution — four anchors, journey order, dependency blocking | ✅ Built |
| `solo-qa` | Two-part verification — active AI testing with evidence + solo browser sign-off required for Done | ✅ Built |
| `qa-triage` | Routes unexpected QA discoveries — bugs, missing requirements, regressions — to the correct path | ✅ Built |
| `process-change` | Consistent protocol for to-be map changes at any phase — capture trigger, three-tier impact scan, re-prioritize, confirm. Solo-invoked or auto-detected from build, QA, or phase test. | ✅ Built |
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
| `framework-curator` | Tends the framework itself — proposes, previews, and executes changes to skills and documentation | ✅ Built |
| `nivya` | On-demand companion — recall and explain only. Reads framework + project continuity + process maps + MemPalace. Answers questions without capturing, deciding, or building. Routes to the right skill with explicit consent when a conversation produces something that belongs in the record. | ✅ Built |
| `solo-simulator` | On-demand autonomous test runner — stands in for the solo at every framework gate during a test run. Operates from a locked brief generated via Q&A. Approves aligned artifacts, pushes back on drift with specific brief-field citations, escalates after one unresolved round with a best-call decision. Produces a live flag surface during the run and a post-run decision log and report. | ✅ Built |

---

## Workshop Skills

Invokable via slash command. Never auto-loaded. For work that isn't a product — spikes, personal tools, exploratory builds. Bare mode by default.

| Skill | Role | Status |
|-------|------|--------|
| `scope-check` | Entry gate — who is this for, how long does it live? Routes to Workshop or SBF | ✅ Built |
| `spike` | Workshop execution — timeboxed work, single artifact, running journal | ✅ Built |
| `land` | Workshop exit — Toss (capture learning), Keep (personal tool), or Promote (hand to SBF) | ✅ Built |

---

## Support Skills

Invokable via slash command. Never auto-loaded. For post-deploy work on live systems — too focused for a full SBF phase.

| Skill | Role | Status |
|-------|------|--------|
| `bug-fix` | Reproduce, root cause, smallest fix, regression check, deploy | ✅ Built |
| `enhancement` | Small addition to existing feature — uses existing design context, lite QA, deploy | ✅ Built |
| `dependency-upgrade` | Audit, check breaking changes, update one at a time, verify, deploy | ✅ Built |
| `security-patch` | Confirm exposure, minimal fix, verify closed, deploy urgently | ✅ Built |

---

## Phase Gates

Every phase transition has a gate — the output that enables the next phase. The gate is structural, not ceremonial: the next phase reads what this phase produced. If the output doesn't exist, framework-health surfaces it.

| From | To | Gate |
|---|---|---|
| Brainstorm | Discover | Judgment — clear enough for a productive discovery conversation |
| Discover | Design Sprint | discovery-brief.md + to-be map agreed |
| Tech Context | Design Sprint | docs/tech-context.md exists |
| Design Sprint | Design Review | sprint-[id].html + deferred-decisions.md exist |
| Design Review | Plan | backlog.md with a coherent set of Ready slices for Phase 1 |
| Plan | Build | GitHub issues created for Phase 1 Ready slices |
| Build (per slice) | QA | Four anchors confirmed + code-complete declared |
| QA | Done | Solo sign-off confirmed in browser |
| All slices Done | Phase Test | Solo invokes explicitly |
| Phase Test | Deploy | Gate OPEN decision |

---

## Session Hygiene

Context fills over time. Long sessions with guided or piloted mode active accumulate context from always-on skills, phase work, and conversation history. Three levers manage this — match each one to the work at hand.

### Three levers

**Mode — match to guidance needed**
- `guided` — full framework chain + always-on. Highest context cost. Right for new projects and unfamiliar territory.
- `piloted` — always-on loads once, phase skills on demand. Moderate cost. Right for builders who know the framework and want continuity without the full chain.
- `bare` — nothing loads until invoked. Zero overhead. Right for focused execution, single-skill sessions, or when you know exactly what you need.

Mode can be switched mid-project. If a session starts on a familiar phase, drop to piloted. If you need one specific skill, go bare.

**Session length — end at gates, not mid-phase**
Phase gates are natural session reset points. The gate output is what the next phase reads — not conversation history. A fresh session that reads the gate output starts with full context and zero overhead.

Rule of thumb: one phase = one session. For long build phases: one sprint's slices = one session. When a gate passes, framework-health surfaces it as a clean close point. product-continuity captures state and generates a resume prompt. The next session reads the handoff and continues — nothing lost.

**Model — match to the type of thinking**
Heavy thinking work (design, architecture, discovery, planning) — use your strongest model. The reasoning load is real and the model earns its cost.

Execution work (build, bug-fix, dependency upgrades, QA) — a faster, lighter model often outperforms a heavier one: lower cost, quicker responses, less overthinking.

This applies equally in Cursor (model settings before starting) and Claude Code (`--model` flag at launch). Don't default to your strongest model for every session.

### Closing a session

When you're ready to wrap up — or when framework-health notes a clean close point after a gate or a natural pause — say **"let's close out."** product-continuity captures state, writes the session log, updates the handoff, and generates a resume prompt. Copy it. Use it next session.

### Resuming a session

Open a new session and paste the resume prompt. `start` reads it, orients from the handoff in one sentence, and continues. No re-explaining, no cold start, no routing.

---

## Companion framework: Workshop

SBF covers product-shaped work. Most solo-builder work isn't that shape. Workshop is the companion for spike-shaped and tool-shaped work — invokable via `/scope-check`.

Scope boundary: SBF handles anything with external users or indefinite lifespan. Workshop handles everything else. `/scope-check` holds the line at entry; `/land` provides the bridge back to SBF when a spike graduates into a product.

Workshop's load-bearing principles are deliberately the inverse of SBF's: timebox over gates, outcome over process, disposable by default, single artifact, explicit graduation.
