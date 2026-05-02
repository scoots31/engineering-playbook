# Solo Builder Framework — Changelog

Each release is labeled with a severity:

- **BREAKING** — must update before starting a new session; old behavior no longer works as documented
- **RECOMMENDED** — new capability or meaningful behavior change; existing sessions unaffected but worth pulling soon
- **MINOR** — correction, clarification, or small fix; pull at your convenience

---

## v1.9.0 — 2026-05-02 — RECOMMENDED

**Solo Companion — Search and Capture**

Two new capabilities that extend Solo Companion from a read-only project viewer into a full memory interface.

**Search** — Query both project records and MemPalace from a single search box. Two-pass engine: natural language and keyword-only queries run concurrently, results merged by best cosine score per source. Memory results display with markdown rendering (headers, bold, bullets, inline code), source filename label, and match percentage. Filter chips narrow to project records or memory only. Requires MemPalace to be installed; gracefully absent if not.

**Capture** — New write capability. A dedicated Capture page lets the solo type freeform notes, decisions, or ideas into MemPalace directly from the companion. Each capture saves as a dated markdown file in `~/Developer/mempalace-captures/` and is immediately mined into the palace — searchable within seconds.

### Files changed
- `Solo Companion/app.py` — `/search` route (two-pass engine, markdown rendering, filter chips), `/capture` + `/capture/save` routes, tunnel/tag stripping corrected to actual MemPalace format

### Action required
None. Search requires MemPalace installed at the standard path. Capture creates `~/Developer/mempalace-captures/` automatically on first save.

---

## v1.8.0 — 2026-05-02 — RECOMMENDED

**Project-level metrics collection**

The framework now automatically produces `docs/metrics.json` during every build — no configuration required.

**What gets tracked:**

- **Rework rate** — each time a slice is selected for build after previously reaching In QA (code review returned it or QA failed), `rework_cycles` increments for that slice. When the slice reaches Done, the summary updates: `total_slices` and, if rework occurred, `slices_with_rework`.
- **Phase test outcome** — when the phase test gate opens, the framework writes `phase_test.result = "pass"` and reads the refinement cycle count from `current-phase.md` (autopilot builds only).
- **Refinement cycles** — autopilot increments `phase_test.refinement_cycles` at each Refinement cycle completion.

**How it works:** solo-build initializes `docs/metrics.json` at the start of the first slice. All counters are increment-only — they accumulate across the full build. The file follows a fixed JSON schema that Solo Companion reads via `sync.py` to surface per-project and cross-project metrics.

**Slice quality checks (pre-build)**

Two lightweight checks added to catch rework risk before build starts rather than after:

- **`prd-to-plan` — slice quality scan at plan approval.** Before presenting the plan, the skill scans every Ready slice for verifiable done criteria (at least two observable outcomes, not behavioral descriptions) and specific quality contract lines (at least two checkable requirements, not aspirational language). Slices that fail either check must be sharpened or split before the plan is approved.
- **`solo-build` — pre-flight at branch open.** After the metrics check and before the feature branch is created, a quick two-question check: can done be stated as a single concrete observation, and is the scope bounded to one interaction or behavior? Not a gate — a prompt to catch softness before context is committed.

**Rationale:** Complexity score (post-build) is a scoreboard. These checks are a rework-risk signal: they catch ambiguous slices at the point where sharpening is cheapest. Breaking a slice into smaller units doesn't reduce Build Complexity — it improves clean first-pass rate, which is what actually matters.

### Files changed
- `skills/solo-build/SKILL.md` — metrics init + rework check before feature branch; summary update at slice Done; pre-flight slice readiness check added
- `skills/autopilot/SKILL.md` — rework increment at QA failure; refinement cycle counter; `docs/metrics.json` added to Output Files
- `skills/phase-test/SKILL.md` — step 4 in "When the Gate Opens": write outcome + refinement cycles
- `skills/prd-to-plan/SKILL.md` — slice quality scan added to Section 8 (plan approval)
- `docs/records-spec.md` — `metrics.json` section: full schema, field definitions, who writes what and when
- `docs/curator-context.md` — decisions log entry

### Action required
None for existing projects. `docs/metrics.json` will be created automatically at the start of the next build session. No backfill is needed for projects already in build — the file picks up from the current state forward.

---

## v1.7.0 — 2026-05-02 — RECOMMENDED

**Automated testing, CI/CD pipeline integration, and seven deployment paths**

Three connected capabilities shipped together:

**Automated test generation** — When a slice reaches code-complete and the project has `CI/CD: GitHub Actions` in tech-context, the framework generates `tests/test_SL-[ID].py` from the slice's done criteria. The full suite runs before every commit. A red suite blocks the commit until the regression is fixed. Tests accumulate as a regression floor across the build. Autopilot includes the same step in its autonomous loop.

**CI/CD Setup** — One-time configuration at first deploy. When GitHub Actions is declared but `.github/workflows/ci.yml` doesn't exist, the deploy skill generates the complete workflow file and walks the solo through only the manual step: pasting a token or API key into GitHub. Plain-language, click-by-click instructions per platform. Solo never writes or reviews YAML.

**Seven named deployment paths** — Tech-context now maps to one of seven fully-supported paths: Local Mac, Cloudflare Pages/Workers, Railway, Render, Fly.io, AWS App Runner, No pipeline. Observability recommendation auto-maps to the selected path. Solo answers plain-language questions; framework maps internally.

### Files changed
- `skills/tech-context/SKILL.md` — deployment question reframed, CI/CD question added, seven paths taxonomy, observability mapping updated
- `skills/solo-build/SKILL.md` — CI suite check at session start, test generation step (Step 1.5) between self-verify and commit
- `skills/deploy/SKILL.md` — CI/CD Setup section with per-platform workflow YAML and plain-language walkthrough
- `skills/autopilot/SKILL.md` — test generation + suite run added to autonomous build loop
- `docs/records-spec.md` — `Test file` field added to slice record
- `docs/communications/guide-build.html` — test generation documented in code-complete flow
- `docs/communications/guide-deploy.html` — seven deployment paths table, CI/CD Setup section added
- `docs/communications/skills-reference.html` — tech-context and deploy cards updated
- `docs/communications/process-map.html` — CI/CD Setup node added to deploy lane
- `docs/communications/blog.html` — v1.7.0 entry

### Action required
None for existing projects. CI/CD and test generation are opt-in — the framework skips both when `CI/CD` is not set to `GitHub Actions` in tech-context. Existing projects built without CI/CD continue unchanged.

---

## v1.6.0 — 2026-05-01 — RECOMMENDED

**Autopilot — autonomous build mode**

New phase skill: `autopilot`. Alternative to `solo-build` for the Build phase — the solo chooses which mode. Autopilot builds the full product without solo participation after discovery or design sprint. Solo-simulator plays every gate. First human touch point is phase test. Refinement cycles handle delta iteration after phase test.

Key elements: mandatory pre-flight check surfaces judgment gaps before any build begins; discovery quality guard flags thin to-be maps; deliverable boundary writes enforced automatically; context discipline via continuity docs throughout; Refinement cycles classify issues (implementation vs. structural) and build only the delta; exit ramp to guided mode at any Refinement cycle completion.

Nothing in the existing framework changes. All updates are additive — solo-build is untouched, all routing logic is unchanged. Autopilot is explicitly invoked only.

**Action required:** None for existing sessions. Pull to get the new skill available.

---

## v1.5.4 — 2026-05-01 — RECOMMENDED

**Retrospective redesign — session-present listening model + cross-machine retro log**

The retrospective was passive — it waited for phase end to process observations. Signals from inside a session had no path to the framework owner across machines. Two gaps, one redesign.

Retrospective now runs in listening mode throughout every guided and piloted session. Three trigger types capture observations without interrupting flow: **framework-detected** (stuck protocol fired, code review failed twice, builder self-corrected, solo-qa caught missed verification, priority deviation, rollback), **solo-expressed** (any dissatisfaction signal — "why did that happen", "that's not what I expected", "that took way longer than it should have"), and **explicit-flag** (solo says "note this", "flag this", "add this to the retro"). Mid-session acknowledgment is one line: "Noted — flagging that." Capture format: `YYYY-MM-DD | user | project | phase | trigger-type | observation`.

Captures write to two places: `.claude/retro-notes.tmp` (session buffer) and `docs/continuity/retro-notes.md` (per-project persistence). At session end, the Stop hook (session-signal-push.sh) pushes retro notes to `shared/retro-log.md` in the engineering-playbook repo alongside session signals. Push failure holds notes in `shared/pending-retro.tmp` for the next successful push.

The framework curator reads `shared/retro-log.md` at session start in owner mode — the only consumer of the cross-machine log. Same-day skip logic: if a `--- Reviewed YYYY-MM-DD ---` separator already exists for today, the curator skips the surface. Framework skills never read the log.

### Files changed
- `skills/retrospective/SKILL.md` — full rewrite: listening mode section, three trigger types, capture format, session-end surface, retro mode updated to read .claude/retro-notes.tmp
- `skills/framework-curator/SKILL.md` — Retro Log section added: session start check, same-day skip logic, separator append after review
- `skills/onboard/SKILL.md` — Check 5 note updated to document retro-notes.tmp handling
- `scripts/session-signal-push.sh` — extended to handle retro-notes.tmp alongside session-signals.tmp; pending-retro.tmp on push failure
- `shared/retro-log.md` — new cross-machine log file

### Action required
None for existing projects — the Stop hook extension is backward-compatible. Retro notes will start flowing on next session that triggers the Stop hook.

---

## v1.5.3 — 2026-05-01 — RECOMMENDED

**Solo-build — deliverable boundary triggers**

Build sessions had no natural stopping point tied to meaningful work units. Sessions could drift mid-deliverable, creating context compression risk and incomplete handoff records.

Two triggers added:

**Mid-deliverable checkpoint** — fires automatically when slice position equals 4 within a deliverable that has more than 4 slices. Framework updates the `## Open right now` section in handoff.md immediately and continues building. No solo approval, no pause. Fires once per deliverable. Protects continuity in the event of unexpected context compression.

**Deliverable completion recommendation** — when a deliverable is fully accepted, the framework surfaces a soft session boundary recommendation: the work is coherent, the handoff has something meaningful to record, and the next deliverable starts fresh without inheriting this session's context. Solo can close out or continue — explicit choice, not a forced stop.

### Files changed
- `skills/solo-build/SKILL.md` — Deliverable completion Step 4 added; Mid-Deliverable Documentation Checkpoint section added; two new anti-patterns

### Action required
None — takes effect in the next build session.

---

## v1.5.2 — 2026-05-01 — RECOMMENDED

**Design sprint — wireframe-first round one + element naming pass**

Round one of the design sprint was producing visually finished artifacts before structure was confirmed. Solos were giving feedback on color and typography when the underlying layout hadn't been agreed on yet. Two changes:

**Wireframe-first round one** — round one now produces structure only: white background, dark text, gray borders, system fonts. No color, no typography decisions, no skin of any kind. The constraint is absolute — color and typography are not part of round one. The solo confirms structure is correct before any skin decisions are made. Skin direction is given explicitly by the solo after structure is confirmed warm.

**Element naming pass** — after producing the round one HTML, the builder walks every interactive element in the artifact in order: names the component type and expected behavior. The solo corrects anything misidentified before layout feedback begins. This prevents a builder from silently categorizing a filter as decorative or a search box as non-functional without the solo's awareness.

### Files changed
- `skills/design-sprint/SKILL.md` — Step 4 rewritten: round one is structure only (monochrome palette, system fonts); element naming pass added after HTML production; Step 5 round discipline updated with explicit skin-direction trigger; anti-pattern added

### Action required
None — takes effect in the next design sprint session.

---

## v1.5.1 — 2026-05-01 — RECOMMENDED

**Figma fidelity rules — interactive element classification, node property enforcement, Check 10**

Three real-world failure modes on a Figma-sourced project drove this change: the builder was reading Figma visually instead of extracting exact node properties, elements in the frame were being missed because there was no systematic inventory, and interactive elements (filters, search boxes, pagination) were being rendered as visual shells with no wired logic.

The fix is a classification gate at design review that forces a decision before build starts. Every interactive element visible in a Figma frame scope must be classified as one of three things: **Functional** (logic will be wired in this slice), **Deferred** (logic comes in a future slice — a companion slice must be created in the backlog now), or **Out of scope** (element appears in Figma but is not part of this product). There is no fourth option. The builder cannot make this decision silently during coding.

At build start, the builder extracts exact node properties (spacing, color, typography) from Figma Dev Mode or MCP before writing any code — not visual estimates. Functional elements require wired logic, not a shell. Deferred elements render as explicit non-interactive placeholders, not working-looking components that accept input and do nothing.

Code review gains Check 10 — Design fidelity — which runs on all Figma-sourced slices. Sub-checks: (10a) interactive element inventory present in the Notes field, (10b) every inventoried element built, (10c) classifications honored in implementation, (10d) a representative sample of visual values traceable to Figma node properties. Non-Figma slices skip Check 10 entirely — stated explicitly in the review report.

### Files changed
- `skills/design-review/SKILL.md` — interactive element inventory added to slice definition; inventory + companion-slice requirement added to Ready gate
- `skills/solo-build/SKILL.md` — Anchor 1 expanded with Figma-specific pre-build steps; missing inventory = stop, return to design review
- `skills/code-review-and-quality/SKILL.md` — Check 10 added; report format updated; stale "Nine-check" header fixed
- `docs/records-spec.md` — design anchor field definition expanded with Figma-specific requirements
- `docs/curator-context.md` — decisions log updated

### Action required
Existing slices with a Figma design anchor should have an interactive element inventory added to their Notes field before the next build session. Slices already Done are unaffected. New Figma-sourced slices cannot reach Ready without the inventory.

---

## v1.5.0 — 2026-05-01 — RECOMMENDED

**Rollback protocol — formal mechanism for undoing completed work**

When a slice that has already passed QA (In Test or Done) needs to be rebuilt, it is a rollback — not a stuck situation. Stuck is failure to make progress on active work. Rollback is about undoing completed work. The framework now has a formal protocol for this instead of treating it as an ad-hoc decision.

The protocol distinguishes two scopes before any action is taken. A **targeted fix** means the approach is sound — a specific behavior is wrong and can be corrected without discarding the implementation. A **full rebuild** means the approach itself is structurally wrong: wrong design reading, wrong architecture, or wrong assumptions baked in from the start. The builder makes this assessment and states which scope applies. The solo confirms before anything changes. No status updates, no code discarded, nothing changes before confirmation.

On confirmation, the cascade runs: a rollback log entry is written, slice status reverts to In Build, the deliverable automatically moves from Accepted to Pending Acceptance (because the condition for Accepted is factually no longer met), and if the phase was Completed it reverts to In Progress. For full rebuilds, all existing code for the slice is discarded and the spec and design file are re-read from scratch before any new code is written.

qa-triage is updated to surface the same targeted-fix vs. full-rebuild assessment when a Done slice bug is reopened — the scope determines whether to use the standard reopen path or invoke the rollback protocol.

### Files changed
- `docs/records-spec.md` — rollback protocol section added; qa-triage added to Who Captures What table; rollback log entry format defined
- `skills/solo-build/SKILL.md` — Rollback section added parallel to When Stuck
- `skills/qa-triage/SKILL.md` — targeted-fix vs. full-rebuild assessment added after Bugs routing table
- `docs/curator-context.md` — decisions log updated

### Action required
None. Existing sessions unaffected. The protocol is invoked only when a Done or In Test slice needs to be rebuilt.

---

## v1.4.2 — 2026-05-01 — MINOR

**Plain language audit — skill names and internal jargon removed from solo-facing output**

Twelve targeted edits across four skill files. The Output Contract rule — skill names, abbreviations, and framework-speak never appear in what the solo reads — was being violated in a handful of quoted output examples and gate decision templates.

Specific removals: `qa-triage` replaced with "open issues" in framework-health session close prompts and phase-test gate templates; a git pull command removed from the update-available prompt (the skill should execute it, not hand it to the solo); "process mapper" and "prd-to-plan" removed from between-phase messages in design-review and solo-build. Internal builder routing instructions that use skill names were left unchanged — those are correct.

### Files changed
- `skills/framework-health/SKILL.md`
- `skills/design-review/SKILL.md`
- `skills/solo-build/SKILL.md`
- `skills/phase-test/SKILL.md`
- `docs/curator-context.md` — decisions log updated

### Action required
None. Editorial only — no behavior change.

---

## v1.4.1 — 2026-05-01 — RECOMMENDED

**Quality contract scaffold — four required categories; security added as Check 9**

The quality contract field added in v1.4.0 is now structured into four required categories: Failure states, Edge cases, Input validation, and Security. Each category must be addressed or explicitly marked `N/A — [reason]`. A blank category is not acceptable — the writer must affirm they thought about it. Design review's Ready gate now enforces the scaffold: an unscaffolded or blank-category contract blocks a slice from reaching Ready.

Solo-build updated in two places: the build plan format now includes explicit steps for observable quality contract items (simulate failure, trigger validation, submit bad input), and the Step 1 self-verification walkthrough now requires triggering failure states, testing edge cases, and submitting bad input in the running app before declaring code-complete. The happy path alone no longer satisfies self-verification.

Code review gains Check 9 — a fixed five-sub-check security gate that runs on every slice regardless of what the quality contract says. Sub-checks: (9a) input sanitization — no raw innerHTML or unescaped user-supplied content; (9b) data scoping — data scoped to the authenticated user; (9c) auth checks are server-side — client-side-only access control is a fail; (9d) injection prevention — user input not concatenated into queries or commands; (9e) no secrets in client-visible code. All five are binary pass/fail with specific violation reporting. Failures route back to build, same as checks 1–8. Check 9 is independent of the quality contract — it catches universal security baselines that a per-slice contract might not surface.

### Files changed
- `skills/design-review/SKILL.md` — four-category scaffold added to quality contract field; Ready gate updated
- `skills/solo-build/SKILL.md` — build plan includes contract steps; Step 1 self-verification walks observable contract items
- `skills/code-review-and-quality/SKILL.md` — Check 9 Security added; output format and pass routing updated
- `docs/curator-context.md` — decisions log updated

### Action required
Existing slices in design review should have their quality contract field updated to use the four-category format before build starts. A blank category is not valid — mark it `N/A — [reason]` if it doesn't apply.

---

## v1.4.0 — 2026-05-01 — RECOMMENDED

**Quality contract — new required field on every slice; code review upgraded to Check 8**

AI-generated code was passing done criteria and browser sign-off while omitting error handling, edge case coverage, and input validation — the behaviors that separate prototype-quality code from production-ready code. Two root causes: non-functional requirements weren't written before build started, so the builder had no obligation to produce them; code review was forming its own judgment about quality rather than checking against a pre-written spec, which defaulted to optimism.

A new `Quality contract:` field sits alongside `Done criteria:` in every slice record. Written during design review, before build starts. Contains specific, verifiable non-functional requirements — error handling behavior, edge case coverage, validation rules. Each line names a specific behavior: what fails, what the system does, what is validated. "Handle errors gracefully" is not a valid contract line. The quality contract is required at the Ready gate — a slice without a quality contract cannot reach Ready.

Code review gains Check 8: the quality contract is read before the code is read, then each contract line is checked against the implementation with adversarial specificity. A try/catch that swallows errors silently does not satisfy "user sees an error message." A validation check on the wrong event does not satisfy "rejects at submission." The contract is the spec; the code either satisfies it or it doesn't. Check 8 failures route back to build.

The Solo Companion now surfaces quality contract status: parsers.py added `Quality contract` to SLICE_FIELDS, db.py added the column to the slices table, sync.py stores the field, and the cloud viewer shows a quality gate indicator in the slice overlay.

### Files changed
- `skills/design-review/SKILL.md` — `Quality contract:` field added to slice template; Ready gate requires it; anti-pattern added
- `skills/solo-build/SKILL.md` — Anchor 3 now surfaces quality contract as a build requirement
- `skills/code-review-and-quality/SKILL.md` — Check 8 added; "Before Running Checks" updated to require quality contract; output format updated
- `docs/curator-context.md` — decisions log updated
- `Solo Companion/parsers.py` — `Quality contract` added to SLICE_FIELDS
- `Solo Companion/db.py` — `quality_contract TEXT` column added with safe migration
- `Solo Companion/sync.py` — quality_contract parsed and stored
- `Solo Companion/push.py` — field included in snapshot
- `solo-companion-cloud/src/index.js` — quality gate indicator added to slice overlay

### Action required
New slices created during design review will get the quality contract field automatically. Existing slices in Ready status should have their quality contract filled in before the corresponding build session starts — a slice can remain Ready without one, but code review will block it at Check 8.

---

## v1.3.4 — 2026-04-30 — RECOMMENDED

**Session signal system — passive telemetry across all machines**

Four skills now append one-line signals to `.claude/session-signals.tmp` when notable failures occur during a build session: stuck protocol fired, slice rebuilt, priority deviation (solo-build); QA caught missed self-verification (solo-qa); code review failed (code-review-and-quality); phase-test HOLD (phase-test). A Stop hook wired via onboard Check 5 reads the tmp file at session end, appends structured lines to `shared/session-log.md` in the engineering-playbook repo, pushes, and clears the file. If push fails, signals are held in `shared/pending-signals.tmp` and included in the next successful push.

**Signal format:** `YYYY-MM-DD | user | project | phase | signal name`

### Files changed
- `skills/solo-build/SKILL.md` — Session Signals section added
- `skills/solo-qa/SKILL.md` — Session Signals section added
- `skills/code-review-and-quality/SKILL.md` — Session Signals section added
- `skills/phase-test/SKILL.md` — Session Signals section added
- `skills/onboard/SKILL.md` — Check 5 updated to wire session signal push hook alongside handoff hook
- `scripts/session-signal-push.sh` — new push script
- `shared/session-log.md` — new log file

### Action required
Existing projects won't have the session signal hook until they run onboard again, or add it manually to `.claude/settings.json` at the project root (see onboard Check 5 for the exact JSON).

---

## v1.3.3 — 2026-04-30 — MINOR

**Language audit script wired as curator Stop hook**

New `scripts/language-audit.sh` greps all `SKILL.md` files for soft language patterns: `should`, `try to`, `when possible`, `if possible`, `consider`, `ideally`, `where applicable`, `as needed`. Outputs file + line number + flagged text. Curator decides what to harden — the script finds candidates only. Wired as a Stop hook on the engineering-playbook so it fires at the end of every curator session.

### Files changed
- `scripts/language-audit.sh` — new script
- `.claude/settings.json` (engineering-playbook) — Stop hook added

### Action required
None. Hook fires automatically in curator sessions going forward.

---

## v1.3.2 — 2026-04-30 — MINOR

**Onboard now sets up handoff staleness hook in project**

Onboard Step 8 has a new Check 5: creates or updates `.claude/settings.json` at the project root with a Stop hook that warns when `docs/backlog.md` has been modified more recently than `docs/continuity/handoff.md`. Silent when handoff is current. Every project onboarded through the framework gets this automatically — no manual wiring needed.

Also: pre-build read gate (solo-build Step 0) strengthened from "state one specific observation" to "produce a verbatim quote — exact string from the file, word for word." A paraphrase no longer qualifies. This closes the loophole where a builder could satisfy the gate from memory rather than from actually reading the file.

### Files changed
- `skills/onboard/SKILL.md` — Check 5 added to Step 8
- `skills/solo-build/SKILL.md` — Step 0 verbatim quote requirement

### Action required
Existing projects won't have the hook until they run onboard again, or you can add it manually to `.claude/settings.json` in the project root using the command from the skill file.

---

## v1.3.1 — 2026-04-30 — MINOR

**Observability tool decision added to tech-context**

Tech context now explicitly asks whether runtime observability is required and which tool is in place — Datadog, CloudWatch, or none. The choice is mutually exclusive and locked at tech-context time. If a tool is declared, an observability setup infrastructure slice is required in the backlog before any feature slices start. The Bayer Aurora profile now prompts for this confirmation since the org standard is not declared at the profile level.

### Files changed
- `skills/tech-context/SKILL.md` — new question 9, Path 1 confirmation update, Observability row in Stack table, infrastructure slice note
- `profiles/bayer-aurora.md` — new Observability section with confirmation prompt

### Action required
None for existing projects — this only applies to new tech-context runs.

---

## v1.3.0 — 2026-04-30 — RECOMMENDED

**Onboard companion pass, shared ideas backlog, deployed-project new cycle**

### What changed

**Companion compatibility pass (onboard)**
Onboard now ends with a four-check pass verifying the project will sync cleanly with the
Solo Companion: projects.md registration, backlog.md section headers, handoff.md with
`## Open right now`, and `Review URL` field on slice records. A project that fails these
checks shows as empty in the companion. The pass fills or flags each gap before exiting.

**Shared ideas backlog (framework-curator)**
New `shared/ideas.md` in the playbook repo. The framework curator can log proposed ideas
from any session and surface pending approvals at session start. Two modes: owner (can
approve/reject/execute) and contributor (propose only). Mode is determined by presence of
`Framework role: owner` in the loaded context — set in the private CLAUDE.md on Scott's
machine, absent from all other installs. Contributor installs redirect direct framework
file edits to the ideas backlog.

**Deployed project — new cycle (start)**
The start skill now detects when all phases in an existing project are at `Deployed` status.
Instead of continuing old work, it routes to a new cycle protocol: orients on what was
shipped, asks what's being added, scopes to the right starting phase, opens a new phase in
the existing backlog, and updates the handoff. Deployed phases are read-only — the new
cycle adds on top of the prior record without touching it.

**Framework files guardrail**
Explicit rule added to CLAUDE.md and Cursor contributor rules: framework files in `skills/`,
`docs/`, and `templates/` are only modified via the framework-curator workflow. Direct edits
outside a curator session redirect to the curator.

### Action required

- **Owner install:** pull to get the new skill changes. No config changes needed — the
  `Framework role: owner` line has been added to your private CLAUDE.md automatically.
- **Contributor install (Cursor):** pull and re-paste Cursor rules from
  `templates/cursor-user-rules-global-playbook.md`. The contributor mode section is new
  and won't be active until the rules are updated.

---

## v1.2.0 — 2026-04-29 — RECOMMENDED

**Builder discipline, review_url field, project isolation**

### What changed

**Pre-build read gate (solo-build)**
Before writing any code, the builder must read the full slice record and design file, then state one concrete observation from each. This is Step 0 — not optional, not skippable for familiar slices.

**Evidence-based self-verification (solo-build)**
Self-verification must be run against the running app, not by reading code. Each checklist item requires a named observation ("the player name 'Josh Allen' renders in the slot row") not an assertion ("data renders correctly").

**Stuck protocol (solo-build)**
Two failed attempts on the same problem: hard stop. Re-read the full slice spec and design file before touching code. If the solo asks to step back at any point, execute it immediately — no assessment, no "one more try." Solo direction overrides builder judgment without exception.

**review_url field (records-spec, solo-build, solo-qa)**
Formal new field on every slice record. Builder writes the URL at code-complete (Step 3). solo-qa reads it for the sign-off prompt. `None` for slices with no previewable output. Never left blank.

**projects.md removed from repo**
The projects registry (`projects.md`) is now local-only and git-ignored. Each user maintains their own. Framework installs no longer carry personal project paths from other users. If upgrading: your local `projects.md` is untouched — only the tracked version was removed.

### Action required
- Add `Review URL:` field to any in-progress slice records that are missing it
- If you have a `projects.md` in your local repo, it will remain — git will no longer track it

---

## v1.1.0 — 2026-04-27 — RECOMMENDED

**Plan-driven build selection, status gate, Build Active terminology**

### What changed

**Plan-driven slice selection (solo-build)**
The builder now reads the backlog and states the next Ready slice by plan priority. Never asks the solo what to work on. If the solo diverts from priority, the builder confirms the diversion explicitly before proceeding.

**Build Active, no Ready slices (solo-build)**
Renamed from "Build Pause." Reflects that the build is ongoing and waiting — not stopped due to a problem. All references updated.

**Watchfor addition (guide-build)**
New watchfor item: "Asking the solo what to work on next." The plan drives selection, not the solo's prompt.

### Action required
None. Existing projects and slice records are unaffected.

---

## v1.0.0 — 2026-04-27 — FOUNDATIONAL

**Canonical records specification, status chain, three-level verification**

### What changed

**records-spec.md — new canonical reference**
Defines every field in every record type: Phase, Deliverable, Slice. Two descriptions per record (plain language for the solo, technical for the builder). Neither is optional, neither is copied from another level.

**Three-level verification model**
Every record type now carries: self-verification checklist, acceptance criteria, and builder confirmation. Builder confirmation is populated at presentation time — not before. It is a gate check in solo-qa and deliverable acceptance.

**Integration deliverable type**
Third deliverable type alongside Screen and Logic. Connects real data to a Screen deliverable. Always sequences after its Screen companion is Accepted. Can spawn new slices mid-build when real data reveals gaps.

**In Test status**
New slice state between QA sign-off and phase-test completion. Eliminates the ambiguity between "passed QA against mock data" and "verified against real data." solo-qa moves slices to In Test. phase-test moves them to Done.

**Done vs Accepted clarified**
Done lives at the slice level. Accepted lives at the deliverable level. A deliverable is not Accepted by the sum of its slice approvals — it requires its own verification pass and solo sign-off.

**Re-phasing protocol**
Seven-step formal process for moving work between phases. All seven steps execute in the same action — log entry and record updates are never separated.

**Backlog Status Reference page**
New standalone communications page with all three status grids, flow chains, and ownership table.

### Action required
Existing slice records missing the new fields (plain language description, technical description, builder confirmation, self-verification checklist) should be updated before the next build session on that slice. Slices already Done are unaffected.

---

## How to update

**Cursor:** ask Cursor to pull the latest from GitHub and re-run the framework install prompt.

**Claude Code:** pull the repo and reload your session. The framework reads skills at activation time — no reinstall needed.

Questions or issues: open a GitHub issue or reach out directly.
