# Shared Ideas

Maintained by the framework curator. Add ideas through a curator conversation — do not
edit this file directly. Ideas require owner sign-off before any framework work begins.

**Status chain:** `Proposed → Approved → In Progress → Done` (or `Rejected`)
**Owner sign-off required:** any status change from Proposed to Approved or Rejected

---

## Framework

---

### READY — Verbatim quote hardening — pre-build read gate
**Added by:** @scotth + Ren
**Date:** 2026-04-30
**Status:** Approved
**Idea:** Strengthen the pre-build read gate in solo-build Step 0. Currently requires "one specific observation" from the design file and slice record — too easy to fake from memory. Change to require a verbatim quote: an exact string from the file (class name, label, measurement, done criteria text). Can only come from actually opening the file. Wrong quote = solo catches it at review.
**Scope:** `skills/solo-build/SKILL.md` — Step 0 only.

---

### READY — Language audit script + curator Stop hook
**Added by:** @scotth + Ren
**Date:** 2026-04-30
**Status:** Approved
**Idea:** Shell script at `scripts/language-audit.sh` that greps every SKILL.md for soft language patterns: should, try to, when possible, if possible, consider, may, might, ideally, where applicable, as needed. Outputs file + line number + flagged text. Curator decides what to harden — script finds candidates only. Wired as a Stop hook on the engineering-playbook so it fires at the end of every curator session, catching regression immediately.
**Scope:** New `scripts/language-audit.sh`, new Stop hook in engineering-playbook `.claude/settings.json`.

---

### READY — Session signal system
**Added by:** @scotth + Ren
**Date:** 2026-04-30
**Status:** Approved
**Idea:** Passive telemetry across all machines. Every framework project gets a `.claude/session-signals.tmp` file. Skills in Build, QA, and Test phases append one-line signals when notable events occur — stuck protocol fired, slice rebuilt, QA caught missed self-verification, handoff stale, code review failed, phase-test HOLD, priority deviation. Stop hook reads the temp file, appends a structured line to `shared/session-log.md` in the engineering-playbook repo, pushes it, clears the temp file. Scott pulls the repo and sees what's happening across all machines.
**Signal format:** `2026-04-30 | user | project | phase | signal1, signal2`
**Design decisions locked:** Engineering-playbook always at `~/Developer/engineering-playbook` (new install convention). Build, QA, Test phases only. Push fails → write to `shared/pending-signals.tmp`, included in next successful push.
**Scope:** New `shared/session-log.md`, signal append instructions in `skills/solo-build/SKILL.md`, `skills/solo-qa/SKILL.md`, `skills/code-review-and-quality/SKILL.md`, `skills/phase-test/SKILL.md`. Stop hook wired via onboard Check 5 (already exists for handoff hook — add session log push alongside it).

---

### READY — Design sprint wireframe-first round one
**Added by:** @scotth + Ren
**Date:** 2026-04-30
**Status:** Done — 2026-05-01
**Idea:** Round one of the design sprint produces structure and layout only — no styling. Solo reacts to whether the layout is right before color and typography come in. Style follows in round two once structure is confirmed. Separates structural decisions from style decisions. Faster first round, better feedback quality.
**Scope:** `skills/design-sprint/SKILL.md` — round one instructions.

---

### READY — Start: lighter re-entry read for returning projects
**Added by:** @scotth + Ren
**Date:** 2026-04-30
**Status:** Approved
**Idea:** When start detects an existing project, it currently reads the full handoff. Change to read `## Open right now` first — that section exists specifically for orientation. Only read the full handoff if that section is unclear or incomplete. Small token saving that compounds across every returning session.
**Scope:** `skills/start/SKILL.md` — re-entry path only.

---

### READY — Discover: lighter path for clear problems
**Added by:** @scotth + Ren
**Date:** 2026-04-30
**Status:** Approved
**Idea:** Discover currently runs all four zones in full. Add an orienting question at the start: "How clear is the problem space?" If strong conviction — compress zones 1 and 2 into a confirmation pass, spend real time on zones 3 and 4 (process and moment of value). Zones 3 and 4 always run in full regardless of path taken. Zones 1-2 compression only when the solo has clear, stated conviction.
**Scope:** `skills/discover/SKILL.md` — opening routing question + compressed path for zones 1-2.

---

### READY — Design review + build: parallel pipeline model with soft prompts
**Added by:** @scotth + Ren
**Date:** 2026-04-30
**Status:** Approved — design session required before execution
**Idea:** Design review and build run as two parallel paths once minimum threshold is met. Design review feeds build continuously — not a sequential phase handoff. Build start condition: 3 deliverables Ready minimum, at least one infrastructure deliverable, OR 1 screen deliverable fully specified. After each screen reaches Ready, soft prompt fires: "Build now or design next screen first?" When build queue drops to one deliverable, soft prompt fires: "Queue running low — go design more screens or keep building?" Multi-session advanced path (two separate Claude instances, handoff as coordination layer) is a future capability — Scott tests single-session model first, quietly, before any documentation or release.
**Scope:** `skills/design-review/SKILL.md`, `skills/solo-build/SKILL.md`, `skills/framework-health/SKILL.md`, `skills/start/SKILL.md`, `skills/product-continuity/SKILL.md`, `docs/records-spec.md` (handoff two-stream structure). Large cascade — dedicated design session required.

---

### READY — Fold prd-to-plan into design-review exit
**Added by:** @scotth + Ren
**Date:** 2026-04-30
**Status:** Approved — design session required before execution (linked to parallel pipeline item above)
**Idea:** Prd-to-plan's sequencing logic moves into design-review's exit step. By the time the build-start prompt fires, the sequence is already in front of the solo. No separate phase, no extra decision point. Prd-to-plan as a standalone skill is retired or repurposed.
**Scope:** `skills/design-review/SKILL.md`, `skills/prd-to-plan/SKILL.md` (retire), all references across skills, docs, templates, communications. Large cascade — execute in same session as parallel pipeline change.

---

### READY — Solo-build: session slice limit + framework-health nudge
**Added by:** @scotth + Ren
**Date:** 2026-04-30
**Status:** Done — 2026-05-01 (redesigned as deliverable-boundary triggers, not slice count)
**Idea:** Context compaction in long build sessions is a root cause of the "builder not reading files" failure — not just a discipline issue. Mitigation: solo-build recommends maximum 3-4 slices per session. After that, commit, close, start fresh. Framework-health nudges after the 3rd slice: "3 slices completed this session — good point to commit and start fresh before context compresses." Not a hard stop, a visible signal.
**Scope:** `skills/solo-build/SKILL.md`, `skills/framework-health/SKILL.md`.

---

### READY — Retrospective: clear path to curator action
**Added by:** @scotth + Ren
**Date:** 2026-04-30
**Status:** Done — 2026-05-01
**Idea:** Retro observations accumulate but have no defined path to the curator. Two additions: (1) retrospective phase-end output explicitly asks "are any of these framework-level?" — if yes, solo appends to shared/ideas.md in the same pass. (2) Framework-health at session start checks whether retro notes from last phase have been reviewed and framework-level observations logged. If not, surfaces it before session starts.
**Scope:** `skills/retrospective/SKILL.md`, `skills/framework-health/SKILL.md`.

---

### READY — Deploy: auto-detect method + outcome-based confirmation
**Added by:** @scotth + Ren
**Date:** 2026-04-30
**Status:** Done-by-proxy — 2026-05-01
**Idea:** Deploy currently asks the solo to choose a deployment method. Tech-context already has the deployment target and platform. Change: deploy reads tech-context and determines method automatically. Confirmation is outcome-based plain language, not method-based technical language: "This deploys to Railway via your GitHub Actions pipeline. When complete your app will be live at [url]. Proceed?" Solo confirms the outcome they expect, not the technical method. Solos lean on the framework heavily at deploy — this removes a decision they shouldn't have to make.
**Scope:** `skills/deploy/SKILL.md`.

---

### NEEDS DESIGN — Product-continuity: lazy document creation
**Added by:** @scotth + Ren
**Date:** 2026-04-30
**Status:** Proposed
**Idea:** Product-continuity creates all 11 document shells at session start regardless of whether there's content. Only create a document when first content exists. Handoff and decisions log always needed — create immediately. Others created on first entry. Risk: Solo Companion may depend on specific continuity documents existing. Must check companion sync logic (sync.py, parsers.py) before executing — any document the companion reads must exist even if empty.
**Scope:** `skills/product-continuity/SKILL.md` — pending companion sync logic review.

---

### Onboard skill — backlog phase archiving
**Added by:** @scotth
**Date:** 2026-04-30
**Status:** Proposed
**Idea:** When a project accumulates multiple completed phases across many cycles, the backlog
grows unwieldy. Design a lightweight archiving mechanism that moves completed phase records
to an archive section (or separate file) while keeping them accessible for reference. The
active backlog stays focused on the current cycle's work.
**Notes:** Agreed to add this as a pending design item. Scope TBD — could be as simple as
an `## Archived Phases` section at the bottom of backlog.md, or a separate
`docs/backlog-archive.md`. Don't design until we have a real project that needs it.

---

## Solo Companion

*No items yet.*

---

## General

*No items yet.*
