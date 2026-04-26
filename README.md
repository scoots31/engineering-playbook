# Solo Builder Framework

---

## For AI assistants reading this repo

If you're an AI (Cursor, Claude, or similar) reading this repository to understand how to operate:

**What this is:** A complete lifecycle framework for building software with AI. It contains 29 skills organized into phases — each skill is a `SKILL.md` file in `skills/<name>/`. Always-on skills activate when the user chooses guided or piloted mode — silent by default. One companion skill (`nivya`) is on-demand — the solo invokes her by name to recall and explain, never to do work.

**What to do:**
1. Default session mode is bare — no routing, no always-on. Skills load only when invoked.
2. Mode activation: "guided mode" → read start/SKILL.md + always-on skills. "piloted mode" → read always-on skills, user invokes phases. "bare mode" → silent.
3. For any active phase, read that phase's SKILL.md before executing
4. The to-be process map (produced in Discover) is the contract for every downstream phase — nothing gets built that can't be traced to it
5. Four anchors are required before any slice reaches Ready: design anchor, data anchor, done anchor, process anchor

**Key principle:** Never announce phases or explain the framework to the user. One sentence of orientation, then just start.

**UX principle:** The framework never asks the solo to open a file and fill it in. All document input is captured conversationally — ask the questions, display what needs review in chat, capture the answers, write the file. The only exception is external stakeholders (people outside the conversation) who receive a fillable template because they cannot be interviewed directly.

**Output discipline:** Match response length to the moment. Acknowledgments are one sentence. Confirmations name what was produced and ask the next question. Explanations are only as long as the thing being explained. Never narrate what the solo just witnessed. No paragraph sign-offs after approvals.

**Skill names are never user-facing:** Surface the action in plain language, never the skill name. "Plan out the build sequence" not "run prd-to-plan." Quote blocks and prompts shown to the solo must never contain a skill name.

**No abbreviations in user-facing output:** SBF, MCP, and any code-identifier-style term never appear in output shown to the solo. "The framework" replaces "SBF" in all user-facing context.

**If User Rules / CLAUDE.md aren't configured yet:** see `CURSOR-SETUP-PROMPT.md` (Cursor) or `CLAUDE-CODE-SETUP-PROMPT.md` (Claude Code) for a ready-to-paste first message that activates the framework for the session.

---

A complete lifecycle system for building software with AI — from first idea through deployed and tested. Covers 27 interconnected skills spanning discovery, design, planning, build, QA, testing, and deploy. Works with **Cursor** and **Claude Code**.

---

## What this is

Most AI coding tools help you write code faster. This framework replaces the discipline a real team provides — the PM challenge, the tech review, the design artifact, the QA gate, the process map — so a solo builder has all of it without needing a team.

**29 skills** cover the full lifecycle. **4 always-on skills** activate on guided or piloted mode — silent in bare mode. **1 companion skill** (`nivya`) is on-demand — the solo invokes her by name for recall and explanation. The QA chain is automatic. Every phase has gates. The whole system is built on a process contract — an agreed to-be map that every phase is held accountable to.

→ See [`docs/communications/skills-reference.html`](docs/communications/skills-reference.html) for full detail on every skill.

---

## Workshop — the companion framework

Not every piece of solo-builder work is a product. Most of it is spikes, tools, personal scripts, explorations. For that work, SBF's ceremony costs more than the work itself.

**Workshop** is the companion framework for small / exploratory / non-UI work. Three skills — `scope-check`, `spike`, `land` — held to the principle of explicit disposability.

→ See [`workshop/README.md`](workshop/README.md) for the full companion framework.

The entry question that routes between the two frameworks: **"Who is this for, and how long does it live?"**

---

## Setup — pick your tool

### Cursor

**Step 1 — Clone the repo**
```bash
git clone git@github.com:scoots31/engineering-playbook.git ~/Developer/engineering-playbook
```

**Step 2 — Find your absolute path**
```bash
cd ~/Developer/engineering-playbook && pwd
```
Copy the output — you'll need it in the next step.

**Step 3 — Set up User Rules**

Open `templates/cursor-user-rules-global-playbook.md`. Replace every instance of `[PLAYBOOK_ROOT]` with the path from Step 2.

Then paste the entire contents (below the dashed line) into:
**Cursor → Settings → Rules → User rules**

That's it. Cursor now knows the full framework and will use it automatically.

---

### Claude Code

**Step 1 — Clone the repo** (same as above)
```bash
git clone git@github.com:scoots31/engineering-playbook.git ~/Developer/engineering-playbook
```

**Step 2 — Add to your global CLAUDE.md**

Open (or create) `~/.claude/CLAUDE.md` and add:

```markdown
## Global engineering playbook

**Playbook root:** ~/Developer/engineering-playbook

This playbook contains the Solo Builder Framework — read
~/Developer/engineering-playbook/skills/start/SKILL.md
when opening any new project to route correctly.

For phase skills, role lenses, and always-on skills see:
~/Developer/engineering-playbook/README.md

**Session modes:** Default is bare (no routing, no always-on). Say "guided mode"
to engage the full phase chain and always-on skills. Say "piloted mode" to load
always-on skills and invoke phases manually.
```

Adjust the path if you cloned somewhere else.

---

## How it works

Open a new project in your editor. Describe what you want to build. The `start` skill reads your opening message and routes you — to **Brainstorm** if the idea needs working through, or **Discover** if you know what you want to build. From there the framework runs phase by phase.

**You bring:** the idea, domain knowledge, and final decisions.  
**The framework brings:** specialist thinking, design execution, quality gates, and process accountability.

---

## The phases

| Phase | Skill | What happens |
|-------|-------|--------------|
| Entry | `start` | Routes to Brainstorm, Discover, or Onboard |
| Entry | `onboard` | Brings existing projects into SBF — reads project dir, maps content to gate artifacts, surfaces gaps, places at correct starting phase |
| 0 — optional | `brainstorming` | Idea exploration with process sketch + visual sketch |
| 1 | `discover` | Full product story + as-is/to-be process maps agreed |
| 1.5 | `tech-context` | Stack, constraints, deploy config — referenced by everything downstream |
| 2 | `design-sprint` | HTML visual artifact — all screens, good enough to make real decisions from |
| 2.5 | `data-scaffold` | Realistic mock data layer + proto-API contract |
| 2.6 | `design-review` | Iterative slice definition, process coverage check, backlog built |
| 3 | `prd-to-plan` + `to-issues` | Phased plan sequenced by risk + process order, GitHub issues created |
| 4 | `solo-build` | Slice-by-slice build — four anchors required, feature branch per slice |
| Auto | `code-review-and-quality` → `solo-qa` | 7-check gate + active testing — auto-triggered on code-complete |
| On-demand / Auto | `process-change` | Consistent protocol for to-be map changes — solo-invoked or auto-detected from build, QA, or phase test |
| 5 — explicit | `phase-test` | 7-specialist-stage test — invoke with `/phase-test` when phase is built |
| 6 | `deploy` | Stack-driven deploy — reads tech-context, confirms gate open, verifies live |

---

## Always-on skills

These four run throughout the entire framework — never invoked by the user:

| Skill | Role |
|-------|------|
| `process-mapper` | Produces as-is + to-be process maps; holds to-be as the process contract across all phases |
| `product-continuity` | Institutional memory — decisions, questions, assumptions, risks, handoffs across sessions |
| `framework-health` | Background signal monitor — file existence + handoff + backlog; silent when healthy |
| `retrospective` | Captures observations in the moment; processes at phase end; improves the framework from real usage |

---

## Companion

One on-demand companion skill — invoked by name, never automatic:

| Skill | Role |
|-------|------|
| `nivya` | Conversational recall + explain. Knows the framework and the project's continuity, process, and memory artifacts. Answers questions about decisions, phases, principles, and process — never captures, decides, or builds. Routes explicitly to the right skill with the solo's consent when a conversation produces something that should be logged. Invoked via `/nivya`; addressable by name once loaded. Can run a huddle as a dedicated subagent for focused sessions. |

---

## Communications materials

Pre-built documents for explaining and presenting the framework:

| Document | Purpose |
|----------|---------|
| [`docs/communications/process-map.html`](docs/communications/process-map.html) | Full swimlane — all phases, all lanes, every output and gate |
| [`docs/communications/deck-business.html`](docs/communications/deck-business.html) | 11-slide executive deck — "From How We Work Today to How We Build Tomorrow" |
| [`docs/communications/deck-solo.html`](docs/communications/deck-solo.html) | 12-slide practitioner deck — mechanics, anchors, QA chain, phase test detail |
| [`docs/communications/skills-reference.html`](docs/communications/skills-reference.html) | All 28 framework skills + Nivya (companion) — description, key elements, invoked by, output |

Open any HTML file in a browser. Slide decks use arrow keys to navigate.

---

## What's in this repo

```
skills/                  All 29 framework skills + nivya (companion) — one folder per skill, SKILL.md inside
docs/
  communications/        Process map, slide decks, skills reference
  process/               as-is and to-be maps (created per project)
  continuity/            Session memory, decisions, handoffs (created per project)
  design/                Design sprint HTML artifacts (created per project)
  engineering/           Supporting docs — playbook, handoff template, integration guides
projects.md                               Registry of project names → paths (named resume)
templates/
  cursor-user-rules-global-playbook.md   Paste into Cursor User Rules (replace [PLAYBOOK_ROOT])
```

---

## License

Use and adapt internally as needed. Add a `LICENSE` file if publishing publicly.
