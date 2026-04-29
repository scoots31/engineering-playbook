# Solo Builder Framework — Changelog

Each release is labeled with a severity:

- **BREAKING** — must update before starting a new session; old behavior no longer works as documented
- **RECOMMENDED** — new capability or meaningful behavior change; existing sessions unaffected but worth pulling soon
- **MINOR** — correction, clarification, or small fix; pull at your convenience

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
