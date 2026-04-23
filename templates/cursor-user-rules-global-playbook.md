# Cursor User Rules — paste into Cursor Settings → Rules → User rules

_Copy everything **below the dashed line** into Cursor **Settings → Rules → User rules** (global)._

## Before you paste — one substitution required

Cursor does not expand shell variables or `~` in User rules. You must replace `[PLAYBOOK_ROOT]` with the absolute path to where you cloned this repo.

**To find your absolute path:** open a terminal, `cd` to where you cloned the repo, and run `pwd`. Copy that output and replace every instance of `[PLAYBOOK_ROOT]` below before pasting.

Example: if `pwd` returns `/Users/yourname/Developer/engineering-playbook`, replace `[PLAYBOOK_ROOT]` with `/Users/yourname/Developer/engineering-playbook`.

---

## Solo Builder Framework — Global Playbook

**Playbook root (absolute):** `[PLAYBOOK_ROOT]`

This playbook contains the **Solo Builder Framework** — a complete lifecycle system for building software with AI, from first idea through deployed and tested. It covers 27 interconnected skills spanning discovery, design, data, review, planning, build, QA, testing, and deploy.

---

## Entry — how new projects start

When a conversation opens with a project or feature idea and no existing context is found, apply this routing before anything else:

1. **Check for existing context first.** If a discovery brief, blueprint, or active sprint exists — orient to where the project is and continue.
2. **Check for spike-shape.** If the opening sounds like "let me try...", "quick script to...", "see if I can...", "one-shot to...", or any personal-tool language, hand to the Workshop companion framework: `[PLAYBOOK_ROOT]/workshop/scope-check/SKILL.md`. Do not continue SBF routing.
3. **Read what was brought in** (product-shaped work only):
   - Clear idea (who, what, value present) → route to Discover. One warm sentence, then begin.
   - Exploratory, uncertain tone → route to Brainstorm. Engage with the idea directly.
   - Ambiguous → ask one question: *"Do you have a clear picture of what you want to build, or are you still working through the idea?"*
4. **Never announce phases or explain the framework.** One sentence of orientation, then just start.

Full routing logic: `[PLAYBOOK_ROOT]/skills/start/SKILL.md`

---

## Workshop — the companion framework

Workshop covers spike-shaped and tool-shaped work — the stuff that isn't a product. Three skills, all under `[PLAYBOOK_ROOT]/workshop/`:

| Skill | Role |
|-------|------|
| `workshop/scope-check/SKILL.md` | Entry gate — Spike vs Tool vs Product. Routes to Workshop or hands to SBF `start`. |
| `workshop/spike/SKILL.md` | The work — timeboxed, single artifact, running journal. |
| `workshop/land/SKILL.md` | The exit — Toss (capture learning), Keep (personal tool), or Promote (hand to SBF). |

Workshop is a deliberate anti-pattern to SBF — timebox over gates, outcome over process, disposable by default. No always-on skills. No anchors. No phases. See `[PLAYBOOK_ROOT]/workshop/README.md`.

---

## The Framework — phase skills

Each phase has a skill. Read it before executing that phase. Skills are in `[PLAYBOOK_ROOT]/skills/`.

| Phase | Skill | Read when |
|-------|-------|-----------|
| Entry routing | `start/SKILL.md` | Opening a new project |
| Idea exploration | `brainstorming/SKILL.md` | Idea isn't fully formed yet |
| Discovery | `discover/SKILL.md` | Building the full product story |
| Tech stack | `tech-context/SKILL.md` | Establishing stack and constraints |
| Design | `design-sprint/SKILL.md` | Producing the HTML visual artifact |
| Data | `data-scaffold/SKILL.md` | Generating mock data layer |
| Slice definition | `design-review/SKILL.md` | Defining and managing the backlog |
| Planning | `prd-to-plan/SKILL.md` | Sequencing slices into phases |
| Issues | `to-issues/SKILL.md` | Converting plan to GitHub issues |
| Build | `solo-build/SKILL.md` | Slice-by-slice execution |
| QA (auto) | `code-review-and-quality/SKILL.md` | Auto-invoked on code-complete |
| QA (auto) | `solo-qa/SKILL.md` | Auto-invoked after code review passes |
| QA routing | `qa-triage/SKILL.md` | When testing surfaces something unexpected |
| Phase testing | `phase-test/SKILL.md` | Full-phase test before deploy (/phase-test) |
| Deploy | `deploy/SKILL.md` | Stack-driven deploy after gate opens |

Supporting skills: `research-spike`, `grill-me`, `to-prd`, `principal-engineer`, `agent-room`, `tdd`, `frontend-design`, `awesome-design-md`

---

## Always-on skills — never invoked by user

Four skills run throughout the entire framework automatically. Read these so you understand when to activate them:

- `[PLAYBOOK_ROOT]/skills/process-mapper/SKILL.md` — produces and maintains as-is + to-be process maps; holds the to-be map as the process contract across all phases
- `[PLAYBOOK_ROOT]/skills/product-continuity/SKILL.md` — institutional memory across sessions; reads handoff.md at session start, captures decisions/questions/assumptions/risks continuously
- `[PLAYBOOK_ROOT]/skills/framework-health/SKILL.md` — background signal monitor; checks file existence + handoff + backlog At a Glance; silent when healthy; never blocks
- `[PLAYBOOK_ROOT]/skills/retrospective/SKILL.md` — flag observations in the moment, process at phase end; evolves the framework from real usage

---

## Role lenses

When the user's intent matches a role, read that skill first:

| Intent | Skill |
|--------|-------|
| Architecture, tradeoffs, system risk, "is this the right approach?" | `[PLAYBOOK_ROOT]/skills/role-principal-engineer/SKILL.md` |
| Implementation breakdown, build order, edge cases | `[PLAYBOOK_ROOT]/skills/role-staff-engineer/SKILL.md` |
| Scope, sequencing, milestones, "what should we cut?" | `[PLAYBOOK_ROOT]/skills/role-pm/SKILL.md` |
| Test plan, verification, quality review | `[PLAYBOOK_ROOT]/skills/role-qa/SKILL.md` |

---

## General principles

**Stack default:** most work is not native iOS. Infer stack from the open project (README, `docs/`, config files). Assume Swift/Xcode only when the repo is clearly an Apple-platform project.

**Project-specific context** (stack, architecture, product decisions) lives in the open project — not in the global playbook.

**Load skills when the phase calls for them** — do not paste entire skill files into chat every turn. Read when the phase is active.

**Four anchors required before any slice starts:** design anchor (screen + element) · data anchor (mock fields) · done anchor (2–3 criteria) · process anchor (to-be map step). If a slice is missing any anchor, stop and ask.

**Process contract:** the to-be process map agreed in Discover is the contract for every downstream phase. Every feature slice must map to a step in it. Nothing gets built that can't be traced to the agreed process.

---

## MemPalace (long-term memory)

MemPalace data lives under `~/.mempalace/`. Find the CLI path with: `which mempalace` or check the venv at `~/[your-venv-path]/bin/mempalace`.

**When the user asks** to update memory / MemPalace: run `mempalace mine "<project root>"` for code/docs, or `mempalace mine "<path>" --mode convos` for exported conversations. Use `mempalace status` to confirm.

**At the end of a substantial session** (feature shipped, major decisions locked, user signals wrap-up): offer to run `mempalace mine` on the current project root. If confirmed, run it via the Shell tool.

---

## Handoffs

When switching tools or ending a long session, use the handoff template at:
`[PLAYBOOK_ROOT]/docs/engineering/HANDOFF.template.md`

Copy to the project root as `HANDOFF.md` — versioned or local-only, user's choice.
