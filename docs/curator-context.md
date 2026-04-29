# Curator Context

**Audience:** Framework curator only. This document is never deployed to Cloudflare and is never solo-facing.

**Purpose:** The reasoning behind every load-bearing decision in the Solo Builder Framework, organized so the curator can make changes without re-litigating what was already decided, and without accidentally breaking something whose purpose wasn't obvious from the code alone.

**How to use it:** Read this before any curator session. When a change is proposed, check it against the relevant section here before drafting the cascade. After any change is executed, add an entry to the Decisions Log at the bottom.

---

## Contents

1. [What This Framework Is and Explicitly Is Not](#1-what-this-framework-is-and-explicitly-is-not)
2. [Load-Bearing Principles — Full Reasoning](#2-load-bearing-principles--full-reasoning)
3. [Activation Taxonomy — All Seven Types](#3-activation-taxonomy--all-seven-types)
4. [Session Modes — Why Three, Not Two](#4-session-modes--why-three-not-two)
5. [The Four Anchors — Why These Four](#5-the-four-anchors--why-these-four)
6. [Always-On Skills — Why These Four Are Always-On](#6-always-on-skills--why-these-four-are-always-on)
7. [The QA Chain — Why It Is a Chain](#7-the-qa-chain--why-it-is-a-chain)
8. [The Output Contract — Rule-by-Rule Reasoning](#8-the-output-contract--rule-by-rule-reasoning)
9. [Skill Design Notes — Non-Obvious Decisions](#9-skill-design-notes--non-obvious-decisions)
10. [Dual-Tool Matrix — Claude Code vs Cursor](#10-dual-tool-matrix--claude-code-vs-cursor)
11. [File Index and Cascade Map](#11-file-index-and-cascade-map)
12. [Decisions Log](#12-decisions-log)

---

## 1. What This Framework Is and Explicitly Is Not

### What It Is

The Solo Builder Framework is a **discipline replacement**, not a coding assistant wrapper. The problem it solves is this: when a developer works on a real team, judgment is distributed across roles — a PM challenges whether the problem is real, a tech lead challenges whether the approach is sound, a designer produces the visual contract everyone points at, a QA engineer verifies independently. Solo, using Claude or Cursor without this framework, none of that judgment exists. The AI defaults to building what the user describes rather than challenging whether they're ready to build it.

The framework restores those functions by giving each function a dedicated skill, sequencing them in the right order, and using gates to enforce that each function has happened before the next begins.

**The central design insight** is that UX must come before code, not after. At Scott's day job, the Figma design is the shared language — engineers, stakeholders, PMs, and data people all point at it. Requirements get clarified because someone looks at a mockup and asks "where does this number come from?" Without this artifact, Claude defaults to building what's technically tractable: backend first, UI skinned on top. The design sprint skill creates the Figma-equivalent moment. It produces an HTML artifact before any backend planning, and that artifact becomes the visual contract for every decision downstream — data, process, scope, and build.

**A non-obvious consequence of HTML over Figma:** the design sprint output IS the frontend starting point. Figma requires translation into code. HTML doesn't. This is why the framework produces HTML and not a design tool export.

**The agile reframe:** the framework is explicitly not waterfall. Phase gates do not mean "this phase is complete and perfect." They mean "this phase has produced enough to learn from." The discovery brief doesn't have to be exhaustive. The design artifact doesn't have to be pixel-perfect. The backlog doesn't have to cover every slice. Each phase produces the minimum the next phase needs to be productive.

### What It Is Not

- **Not a prompt library.** Individual skills are not reusable prompts. They are stateful, sequential processes that read project-specific documents, produce project-specific documents, and pass those documents to the next phase. Running a skill in isolation without its prerequisites will produce wrong output.

- **Not a coding assistant.** The framework doesn't help write better code faster. It helps decide what to build, verify it was built correctly, and maintain a record of every decision that was made. Code quality is one check in a QA chain, not the primary concern.

- **Not a team collaboration tool.** The framework is designed for a single solo builder working with an AI. Collaboration hooks exist (stakeholder feedback template, design handoff package) but the primary operator is always the solo.

- **Not an AI pair programmer.** The framework's job is not to help the solo code. It's to replace the team dynamics a solo doesn't have access to.

- **Not applicable to spike/tool work.** The Workshop companion framework (scope-check, spike, land) handles non-product work — personal scripts, explorations, one-shot tools. The main framework's ceremony costs more than the work when applied to a personal tool that may be thrown away after a weekend. The routing question that distinguishes them: "Who is this for, and how long does it live?"

---

## 2. Load-Bearing Principles — Full Reasoning

These ten principles are what make the framework what it is. Changing any of them changes the framework's identity, not just its behavior. The curator must flag any proposal that touches these and confirm whether the change is intentional.

---

### Principle 1: Process-first — the to-be map is the contract

**What it means:** Before any screen is designed, any slice defined, or any line of code written, the to-be process map is agreed on in the discover phase. Every screen in the design sprint must trace to a step in the to-be map. Every slice in the backlog must have a process anchor naming the to-be step it implements. Every test scenario in phase test must derive from a path through the to-be map. Nothing in any phase proceeds without this contract.

**Why it exists:** Without a process contract, build decisions default to comfort and familiarity. A developer builds the screen they know how to build, not the process step the product is supposed to implement. A design decision looks correct visually but doesn't implement the agreed behavior. A test scenario covers the happy path but misses the branch the process requires. The to-be map is the thing everyone is accountable to — it prevents "we built the wrong thing" from surfacing at phase test, when it's maximally expensive.

**What it prevents specifically:**
- Screens designed for visual appeal that don't support any agreed process step
- Slices built because they're interesting or easy, not because they implement the process
- Test scenarios derived from the design rather than from the agreed process (different scope)
- Phase test finding that the product doesn't match the discovery intent, requiring rework

**What "changing it" would actually mean:** Removing the process anchor requirement from Ready criteria means slices can be defined and built without verifying they implement the agreed process. At that point, the framework has no mechanism to confirm the product does what was agreed in discovery. It becomes a coding assistance tool with design gates, not a discipline replacement.

**Where it appears in code:** process anchor is a Ready gate in `skills/design-review/SKILL.md`. Process anchor is required before build starts in `skills/solo-build/SKILL.md`. Process-mapper cross-references screens against to-be map in every design sprint and design review round. Phase test Stage 6 acceptance reviewer evaluates against the discovery brief, which is the prose version of the to-be process.

---

### Principle 2: Four anchors required — design, data, done, process

**What it means:** Every slice must have all four anchors defined before any code is written. Missing any one of them stops build immediately. There are no exceptions, no "we'll add it later," no "this one is simple enough to skip the anchor."

**Why each anchor is separate and necessary:**

**Design anchor** prevents building from memory. The format requires naming the specific screen file AND the specific element within it. "It's in the player overview screen" is not a design anchor. "sprint-p1.html → Slot context card → top of overview body, below player tabs" is. Without the element specificity, a developer builds from their mental model of the design, which drifts from the actual design file. The instruction is to open the file and look at the element, not to recall it.

**Data anchor** prevents hardcoded values. The format requires naming the specific mock data file AND the specific field names within it. "It reads from mock data" is not a data anchor. "data/mock/players.json → slot_tag, slot_target, slot_role_text" is. Without field-level specificity, developers hardcode values that "look right" from the design artifact rather than pulling them from the data layer. Code review catches this, but the anchor prevents the hardcoding from happening in the first place.

**Done anchor** prevents vague completion criteria. The format requires 2–3 specific, verifiable statements — not "it works" or "looks like the design." Without precise criteria, solo-qa has nothing to verify actively. The criteria are also what the solo confirms in the browser during sign-off. Vague criteria produce subjective sign-offs ("it seems fine") rather than explicit criterion-by-criterion confirmation.

**Process anchor** prevents building something that matches the design but doesn't implement the agreed process. Added after the first three anchors proved insufficient — a slice could pass all three and still implement the wrong thing if the to-be process step wasn't specified. The format names the to-be map file, the step name, and its position in the flow (main path / branch / exception / infrastructure).

**What "changing it" would mean:** Removing any one anchor removes the failure mode protection that anchor provides. Removing the process anchor would break the process-first principle. Removing the done anchor means solo-qa can't verify actively. Removing the design anchor means build drifts from the design file. All four are required or the framework loses a category of quality protection.

**Where it appears in code:** `skills/design-review/SKILL.md` (Ready gate requires all four), `skills/solo-build/SKILL.md` (four anchors surfaced before code is written), `skills/solo-qa/SKILL.md` (reads all four anchors at the start of Part 1).

---

### Principle 3: Gates between phases — explicit named confirmation, two-option direct question

**What it means:** Every phase transition requires a gate: the output that enables the next phase must exist, a named confirmation must fire listing the actual output files produced, and a direct two-option question must be asked ("Start the next phase now, or close out here?"). The gate format is not negotiable — no passive language, no implied continuation, no "good stopping point" soft close.

**Why the gate format is specified down to the phrasing:**

Phase gates serve two functions. The structural function is enforcing that the next phase has its required inputs. The behavioral function is creating an explicit decision point so the solo knows a phase ended and can choose whether to continue. Without an explicit question, sessions drift — the solo doesn't realize a phase completed, something new starts without the gate artifacts, and the framework loses track of state.

The format rule ("list specific files, not categories; ask one direct question with two named options") exists because:
- "Your files are ready" doesn't tell the solo what was produced
- "Would you like to continue?" doesn't name the options clearly
- "I can either plan the build sequence or start building SL-001 directly" is the right form — each path in one sentence, then the question

The prohibition on "good stopping point" language is specific: that phrase invites drift. It suggests the phase is partially done, leaves an opening for "let me keep going just a bit," and produces no clear decision. The direct question closes the loop.

**What "changing it" would mean:** If gates became optional, phases would blur together, required inputs would be missing when the next phase reads them, and the solo would lose orientation. If the gate format became passive ("your discovery brief is ready"), the behavioral function would fail — no explicit decision, no clean handoff, no visible transition point.

**Where it appears in code:** `skills/framework-health/SKILL.md` (phase gate format defined in detail), `CLAUDE.md` (Output Contract section on transitions).

---

### Principle 4: Always-on ≠ user-invoked

**What it means:** The four always-on skills (process-mapper, product-continuity, framework-health, retrospective) activate automatically when guided or piloted mode is chosen. They are never invoked by the solo. They run throughout their designated phases without being re-invoked.

**Why automatic activation is essential:**

The value of always-on skills is that they run at the moments the solo would be least likely to remember to invoke them. Product-continuity captures decisions at the moment they're made — if it were on-demand, it would only run when the solo remembered to invoke it after a decision, which is exactly when the decision's reasoning is most likely to be paraphrased imprecisely. Framework-health checks phase gate integrity between phases — if it were on-demand, it would only run when the solo already suspected something was wrong, which defeats the purpose. Process-mapper cross-references screens against the to-be map during design sprint — if it were on-demand, the cross-reference would happen after screens are approved, when it's harder to change them.

**What "making them on-demand" would cost:** The always-on skills perform exactly the functions that the solo would forget to perform if they had to remember. They're always-on because that's the only way to guarantee they run at the right moments.

**Where it appears in code:** All four SKILL.md files have explicit "Never invoked manually" or equivalent language. `CLAUDE.md` lists always-on skills under their own session mode activation block. `README.md` has a dedicated always-on table. `solo-builder-framework.md` separates always-on from phase skills explicitly.

---

### Principle 5: Activation taxonomy is fixed

**What it means:** Every skill has exactly one activation type from the seven-type taxonomy: Framework entry, Framework-routed, Phase skill, On-demand, Auto, Supporting, or Always-On. Skills cannot drift between categories without a deliberate framework-level decision.

**Why it matters:**

The activation type determines when a skill runs, who triggers it, and what the chain looks like. A skill that drifts from Auto to Phase skill (meaning the solo invokes it instead of the previous skill in the chain triggering it automatically) breaks the chain. If solo-qa becomes solo-invoked instead of auto-triggered by code-review-and-quality, some slices will skip code review before QA runs. If framework-health becomes on-demand instead of always-on, health checks only happen when the solo suspects a problem.

Activation taxonomy also governs how skills are described in the communications materials. Calling an Auto skill "on-demand" in skills-reference.html would give the solo a wrong mental model of how the chain works.

**The seven types:**
- **Framework entry:** start only. Fires automatically on new conversation. Never invoked.
- **Framework-routed:** skills the framework routes to from another skill (e.g., solo-build routes to code-review-and-quality). Not invoked by solo.
- **Phase skill:** invoked explicitly by the solo to enter a phase (e.g., `/phase-test`).
- **On-demand:** invoked by the solo when needed (grill-me, research-spike, principal-engineer).
- **Auto:** triggered by the preceding skill in a chain (code-review-and-quality, solo-qa). Never invoked directly.
- **Supporting:** used by other skills as sub-routines or references (tdd, frontend-design, awesome-design-md).
- **Always-On:** activate at mode selection, run throughout their designated phases (process-mapper, product-continuity, framework-health, retrospective).

**Where it appears in code:** `skills-reference.html` badge on each skill card. `README.md` always-on table and supporting skills note. `CLAUDE.md` session mode block.

---

### Principle 6: Continuous capture

**What it means:** Product-continuity captures decisions, questions, assumptions, risks, changes, and session state throughout every session without being re-invoked. Flag mode (via product-continuity) captures retro observations in the moment throughout every phase.

**Why continuous is the right model:**

The decisions that matter most are made mid-conversation when the solo is focused on the problem, not on documentation. If capture were session-end-only, the solo would have to reconstruct reasoning from memory — "we decided to use X because..." rather than "we decided to use X because the B approach would require a data model change that would affect Phase 2 slices, which we established was too expensive at this stage." The specificity of the reasoning gets lost.

Retro observations are the same: the observation has the most signal immediately after the event, not at phase end when it's processed. Flag mode preserves the raw observation ("process map cross-reference wasn't prompted — had to be done manually") so retro mode has real material to work with.

**What "changing it" would mean:** Moving to session-end-only capture would mean all reasoning captured during a session is reconstructed rather than recorded. Over multiple sessions, the decision log would contain accurate facts but imprecise reasoning — which is exactly what causes re-litigation of settled decisions.

---

### Principle 7: Stop on missing prerequisites — name the gap, name the recovery path

**What it means:** When a skill's required inputs are missing, the skill stops immediately. It does not work around the gap, attempt partial execution, or suggest alternatives. It names the specific missing input and the specific action needed to get it.

**Why stopping is the right behavior:**

Proceeding without prerequisites produces work that contradicts what would have been decided if the prerequisite existed. If design review runs without a to-be process map, slices get defined against screens alone — and process coverage gaps won't be discovered until phase test, where they're expensive to fix. If solo-build runs without all four anchors, the build starts from an incomplete specification. If code review runs without the four anchors in the backlog, it can't check the process anchor. The stop prevents the more expensive rework.

"Name the gap, name the recovery path" is equally important. "I cannot proceed" with no further information leaves the solo with no path forward. "Design review cannot run without a to-be process map. Go to Discover and agree the process first — it takes one conversation." gives the solo exactly what they need.

**What "changing it" would mean:** Allowing skills to proceed with partial prerequisites would mean quality of output varies based on what inputs are available. Over time, the framework would accumulate outputs of varying quality from sessions where prerequisites were skipped. The stop behavior is what makes the outputs reliable.

---

### Principle 8: One sentence of orientation, then start

**What it means:** When a skill activates, it says one sentence of orientation and then begins doing the work. It never announces what phase is running. It never explains the framework. It never lists what it's about to do. It orients once and starts.

**Why the framework must be invisible:**

The solo is working on their product. Every second spent explaining the framework is a second taken from the product. Phase announcements ("I'm now beginning the Discovery phase") make the framework self-referential — the system talking about the system. They give the solo the impression they're navigating a process rather than building something.

The contrast is important: "I'll now begin the Discovery phase of the Solo Builder Framework. This phase consists of four zones..." is the wrong model. "That's clear enough to start from — let me ask a few things to get the full picture." is the right model. The second version is what a good teammate says. The first version is what a system announces.

**Why "then start" is specified:** One sentence of orientation is not a license to spend several messages setting context before beginning. The orientation names where we are, the very next message starts the work.

---

### Principle 9: Output Contract — authoritative in CLAUDE.md

**What it means:** All output behavior across all skills is governed by the Output Contract in `CLAUDE.md`. That file is the authority. When a curator change touches output behavior, the Output Contract is updated first. All other files that describe output behavior are secondary and must align with it.

**Why a single authoritative source:**

Without a single authoritative source for output rules, individual skills drift toward their own styles over time. One skill uses skill names in output. Another hands commands to the solo. A third writes three-paragraph sign-offs after approvals. The Output Contract is what prevents this. Because all 38 skills must follow it and it lives in one place, a change to the contract propagates everywhere.

**Why CLAUDE.md specifically (not a standalone document):** CLAUDE.md is loaded into every Claude Code session automatically. Skills don't have to look it up — it's always in context. Putting the Output Contract anywhere else would require skills to explicitly read it, which would be fragile.

**Where it appears in code:** `~/.claude/CLAUDE.md` (authoritative), `templates/cursor-user-rules-global-playbook.md` (copy for Cursor), `templates/claude-global-playbook.md` (copy for Claude). When these fall out of sync, Cursor and Claude Code behave differently.

---

### Principle 10: Framework executes, solo responds

**What it means:** The framework never asks the solo to open a file and fill it in, copy a command and run it, or take any mechanical execution action. All input from the solo is captured conversationally — the framework asks questions, the solo answers, the framework writes the files. All terminal commands are executed by the framework — either directly (for routine operations) or after explicit permission (for significant or destructive operations).

**Why this is a load-bearing principle:**

The solo's role is vision, product thinking, domain knowledge, and final approval. Every mechanical task handed to the solo is an interruption of that role. More practically: when a command is handed to the solo to run, they may run it from the wrong directory, with incorrect context, or not at all. The command either doesn't run (lost in the conversation) or runs incorrectly (wrong path, wrong flag). The framework running commands directly is not just more convenient — it's more reliable.

**The one exception:** external stakeholders who receive fillable templates. A stakeholder reviewing a design can't be interviewed conversationally because they're not in the session. They receive a fillable template because that's the only mechanism available. This is the only case where the solo is asked to hand something to another person to fill in — not to fill in themselves.

**What "changing it" would mean:** Any step in any skill that requires the solo to perform a mechanical action (run a command, copy a file, fill in a field) is a violation. Finding one is a bug to fix, not a feature to document.

---

## 3. Activation Taxonomy — All Seven Types

Every skill must belong to exactly one type. When a skill is added or modified, confirm its type is correct and consistent with how it's described everywhere it appears.

### Framework Entry
**What it is:** Fires automatically when a new project conversation begins. The solo never invokes it.
**Skills:** `start` only.
**Why only one:** There's only one front door to the framework. Multiple entry skills would create routing ambiguity.
**Key behavior:** start fires automatically via CLAUDE.md rule (Claude Code) and Cursor rules (Cursor). It does NOT fire when existing project context is found — it orients to the existing state instead.

### Framework-Routed
**What it is:** Runs when another skill routes to it as part of normal phase flow. Not invoked by the solo.
**Skills:** Most phase skills fall here for their primary invocation path (discover, design-sprint, data-scaffold, design-review, prd-to-plan, to-issues, solo-build, deploy).
**Key behavior:** These skills run because the framework chain led to them, not because the solo explicitly asked for them. The routing is invisible.

### Phase Skill
**What it is:** Invoked explicitly by the solo when they decide to enter a phase.
**Skills:** `phase-test` is the clearest example — the solo explicitly invokes it because they've decided the phase is built. The solo makes this judgment; automation can't.
**Why "explicit" matters:** Phase-test's manual invocation is a design decision. Automating it would trigger testing before the solo is confident the phase is complete. The framework signals readiness (framework-health nudge) but the call is the solo's.

### On-Demand
**What it is:** Skills the solo invokes when they need them.
**Skills:** grill-me, research-spike, principal-engineer, onboard, qa-triage, process-change, nivya, all Workshop skills (scope-check, spike, land), all Support skills (bug-fix, enhancement, dependency-upgrade, security-patch).
**Key behavior:** These skills don't activate unless the solo requests them. Some can also be triggered by other skills (qa-triage is invoked automatically when unexpected discoveries surface in solo-qa and phase-test, but can also be directly invoked).

### Auto
**What it is:** Triggered by the preceding skill in a chain. Never invoked directly by the solo.
**Skills:** `code-review-and-quality`, `solo-qa`.
**Why auto-triggering matters:** The auto trigger removes the solo's ability to skip a step. "Just this once, I'll skip code review" is how quality degrades. Auto-triggered means every slice gets the same treatment regardless of how confident the solo feels.
**Key behavior:** If the solo somehow invokes solo-qa directly without a code review pass logged in the backlog, solo-qa stops immediately and refuses to proceed.

### Supporting
**What it is:** Skills used by other skills as sub-routines or called by the solo for specific techniques.
**Skills:** tdd, frontend-design, awesome-design-md, code-review-and-quality (also Auto — dual role in the chain).
**Key behavior:** Supporting skills can be invoked directly for their technique without running a full phase.

### Always-On
**What it is:** Activate once at mode selection (guided or piloted), persist for the session, run throughout their designated phases without re-invocation.
**Skills:** process-mapper, product-continuity, framework-health, retrospective.
**Key behavior:** Silent in bare mode. Never invoked by the solo. Run at the right moments automatically. See Section 6 for the reasoning behind each.

---

## 4. Session Modes — Why Three, Not Two

The framework has three modes: **guided**, **piloted**, and **bare**. The existence of piloted (the middle mode) is the non-obvious decision.

### Why Not Just Guided and Bare

**The problem with only two modes:** A solo builder who knows the framework and is continuing an existing project doesn't need the full guided chain — they know which phase they're in, they know the routing. But they do need continuity: product-continuity should be capturing decisions, framework-health should be monitoring signals, the session should close with a proper handoff. Bare mode provides none of that.

**Piloted fills the real need:** Piloted loads the four always-on skills once and then waits for the solo to invoke phases explicitly. The always-on skills provide continuity without the overhead of the full guided chain.

**Cost reasoning:** Guided loads all always-on skills AND runs the start routing and full phase chain. This is the right model for new projects and unfamiliar territory — highest context cost, highest guidance. Piloted loads only always-on skills — moderate cost, right for builders who know the phase chain and want to invoke it deliberately. Bare loads nothing — zero overhead, right for single-skill sessions or focused execution work.

### Mode Switching Mid-Project

Modes can be switched within a project. The documented pattern is:
- New project, unfamiliar phase → guided
- Continuing project, familiar phase → piloted
- Single-skill session (one bug, one deployment) → bare

Switching is not destructive. Moving from guided to piloted mid-project doesn't lose context — product-continuity already captured the session state. Moving from piloted to bare just stops the always-on skills for that session.

---

## 5. The Four Anchors — Why These Four

The four anchors are the answer to "what does a slice need before build can start?" Each anchor was added to prevent a specific failure mode that was identified as a real pattern.

### Why "Four" Is Not Arbitrary

Before there were four anchors, there were three: design, data, done. Process was added after it became clear that slices could satisfy all three and still implement the wrong thing. A slice could have a clear design reference, correct mock data fields, and verifiable done criteria — and build a screen that didn't implement any step in the agreed to-be process. The process anchor closes that gap.

The set of four is complete: they cover what to build (design anchor), what data to use (data anchor), what "done" means (done anchor), and which step in the agreed process is being implemented (process anchor). Adding a fifth anchor would require identifying a failure mode not covered by these four. Removing any one anchor re-exposes the failure mode it was designed to prevent.

### Design Anchor — Specificity to Element, Not Screen

The format is: `[screen-file] → [element name] → [location on screen]`. The screen file alone is not sufficient. A screen may have ten elements — specifying the screen but not the element means the developer builds from their interpretation of which element to build, which may differ from what was intended.

The instruction to open the file and look at the element (not recall it from memory) is equally important. Design files change between sessions. A developer building from memory of a screen that was modified two sessions ago is building against stale information.

### Data Anchor — Field-Level Specificity, Not File-Level

The format is: `[mock-file] → [field names] → eventual real source per data-mapping.md`. Pointing to the mock file without naming the fields is not sufficient. Without field names, the developer may pull the right file but hardcode specific values from it ("the slot target is 14.2, I'll use that") rather than reading the field dynamically. The field names in the anchor are what code review Check 2 (data sourcing) verifies against.

### Done Anchor — Concrete and Verifiable Only

The explicit prohibition on vague criteria ("it works," "looks like the design") is not aesthetic — it's functional. Solo-qa Part 1 verifies done criteria with named evidence. If a criterion is vague, there's no way to produce evidence for it. "It looks right" cannot be verified with "the rendered value is 14.2 which matches slot_target: 14.2 in players.json." Only concrete criteria can be actively verified.

### Process Anchor — The Contract Connection

The format is: `[to-be map file] → [step name] → [position in flow]`. The process anchor is what connects the slice to the to-be map that was agreed in discovery. Without it, there's no mechanism to verify that the build is implementing the agreed process rather than just building screens. It's also what phase test Stage 6 (acceptance reviewer) evaluates against — without process anchors on every slice, the acceptance review has no precise contract to verify.

Infrastructure slices (routing, authentication, shared components with no direct process step) must be explicitly documented as infrastructure in the process anchor field, not left blank. A blank process anchor means the anchor was skipped. An explicit "infrastructure — no process step" is an intentional documentation.

---

## 6. Always-On Skills — Why These Four Are Always-On

### process-mapper

**Active across:** discover through phase test.

**Why always-on, not on-demand:** The to-be map is agreed during the discover conversation. If process-mapper were on-demand, it would be invoked after the conversation to document what was agreed — which means the documentation is a reconstruction of memory, not a capture of the agreement as it was being formed. The value is that process-mapper is present during the discover conversation, hears the to-be process being described, asks clarifying questions, and produces the map from the primary source.

**Critical behavior to preserve:** process-mapper cross-references every design sprint screen against the to-be map, and every slice definition in design review against the to-be map. These cross-references must happen as part of those phases, not as separate passes. If process-mapper cross-referencing were pulled out of the design sprint and design review flows, process coverage gaps would not be surfaced until phase test — too late.

### product-continuity

**Active across:** all phases, all sessions.

**Why always-on, not on-demand:** Decisions are made throughout every session. The most important decisions are often made when the solo is focused on the problem, not on documentation. If product-continuity were on-demand, the solo would invoke it when they realized something important happened — which is after the fact, when specificity of reasoning has already degraded.

**Critical behavior to preserve:** The Nivya exception. When Nivya is active, product-continuity does not capture passively. Nivya handles the routing — only on explicit solo yes does capture happen. This is a deliberate safety boundary: exploratory thinking with Nivya should not be recorded as settled decisions. If this behavior were removed, every sentence said to Nivya could end up in the decision log regardless of whether the solo intended it as a decision.

**The resume prompt:** product-continuity generates a resume prompt at session close that the solo copies and pastes into the next session. This is the mechanism by which cold-start overhead is eliminated. Every session that reads the handoff document and the resume prompt starts with full context. Removing or weakening this behavior would degrade the continuity that makes multi-session projects tractable.

### framework-health

**Active across:** all phases, all sessions.

**Why always-on, not on-demand:** Framework-health checks happen at specific moments: mode activation, between phases, and at session end. If it were on-demand, it would only run when the solo suspected something was wrong — exactly the wrong timing. The value is proactive detection before a problem affects the session.

**The token discipline is a design constraint, not a style choice:** framework-health checks file existence and the backlog At a Glance section. It does NOT read full documents. This is deliberate. A health monitor that reads every document at every phase transition would consume significant context and slow down every session. The signal-based approach (file exists / doesn't exist, backlog counts look consistent / inconsistent) catches the same issues with a fraction of the cost. Only when a signal is wrong does framework-health read the relevant document.

**One issue at a time:** When multiple things are wrong, framework-health surfaces the most important one first. This is a UX decision, not a technical limitation. A list of six problems is overwhelming and produces paralysis or triage overhead. One problem with a recovery path produces action.

**Silent when healthy:** No output when everything is running correctly. This is essential: if framework-health spoke at every phase transition to confirm health, the solo would start ignoring it. Output from framework-health must always mean something. Silence is the confirmation of health.

### retrospective

**Active across:** all phases, all sessions (flag mode), phase end and after phase test (retro mode).

**Why always-on for flag mode:** Observations have the highest signal immediately after the event. "The process map cross-reference wasn't prompted — had to be done manually" has more specificity and accuracy immediately after it happens than it would at phase end reconstruction. Flag mode preserves this signal as a one-line note without interrupting flow.

**Why retro mode fires at phase end, not after every flag:** Processing every observation as it occurs interrupts the session. Phase end is the natural pause point. The backlog of flagged observations has enough volume at phase end to identify patterns (same issue appearing multiple times) versus one-offs.

**The framework-level vs project-level distinction is critical:** A project-specific adjustment (this project has an unusual data model, so this review step runs differently) should NEVER modify a SKILL.md. A SKILL.md change for one project's quirk would break the skill for all other projects. The distinction must be made explicitly on every retrospective entry.

---

## 7. The QA Chain — Why It Is a Chain

### The Chain Structure

```
solo-build declares code-complete
  → code-review-and-quality (auto-triggered)
    → PASS: logs confirmation, auto-invokes solo-qa
    → FAIL: slice returns to In Build
```

### Why Auto-Trigger Removes Solo Discretion

The automatic trigger is not a convenience feature — it's a quality guarantee. If any step in the chain were on-demand, the solo would occasionally skip it. "This slice is straightforward, I'll skip code review." "I've been looking at this all session, I know it looks right." The chain ensures every slice gets the same treatment regardless of how simple it seems or how confident the solo feels.

If code-review-and-quality were on-demand, it would be the most frequently skipped step — it runs between the work being done and the review the solo actually cares about. The auto-trigger is what makes it happen.

### Why Code Review Runs Before Solo-QA

Code review catches implementation problems (hardcoded data, broken patterns, scope creep, missing documentation) before the solo's time is spent on sign-off. If the slice has a hardcoded value that code review would catch, there's no point spending the solo's attention on a browser sign-off for a slice that needs to be rebuilt anyway. The ordering minimizes total work.

### The Evidence Standard in solo-qa

The distinction between code inspection and active verification is the most important behavioral requirement in the QA chain.

- "The code reads `slot_target` from the mock layer" — this is code inspection. It tells you what the code is supposed to do. It does not tell you whether the rendered output is correct.
- "The rendered value is `14.2` — matches `slot_target: 14.2` in `data/mock/players.json`. Not hardcoded." — this is active verification. It tells you what the solo or a user would actually see.

Without the evidence standard, Part 1 of solo-qa becomes code review again — reading code and trusting it works, which code-review-and-quality already did. The evidence standard ensures solo-qa is genuinely a different check.

### Why the Solo's Browser Sign-Off Cannot Be Substituted or Skipped

The AI can verify that every done criterion is technically met. It cannot verify that the product feels right in use, that a human looking at it would understand it, or that something visually correct from a technical perspective is actually what was intended. The solo using the product in a browser is a fundamentally different type of verification.

The prohibition on solo confirming from memory ("I looked at it earlier") exists because "earlier" means the slice may have changed since the last look. The sign-off is supposed to verify the current state, not a remembered state.

### The QA Chain and the Deliverable Level

Slice sign-offs are necessary but not sufficient. When all slices in a deliverable are Done, solo-qa runs a deliverable-level acceptance check — the complete experience, not individual slices in isolation. A deliverable is not accepted by the sum of its slice approvals. This exists because slice isolation can hide integration issues: two slices that each pass QA in isolation may fail when experienced together (navigation doesn't flow correctly, shared state is inconsistent, the end-to-end journey has a gap).

---

## 8. The Output Contract — Rule-by-Rule Reasoning

The Output Contract lives in `CLAUDE.md` and is authoritative. This section explains the non-obvious rules.

### Skill names never in user-facing output

**The rule:** Never say "run prd-to-plan" or "invoke solo-qa" in any output the solo sees. Always surface the action in plain language: "plan out the build sequence," "verify the slice is done."

**Why:** Skill names are internal routing identifiers. They mean nothing to the solo, and exposing them makes the framework self-referential — the system talking about its own internal architecture. The solo cares about the action, not the skill that performs it. Using skill names in output also creates a coupling: if a skill is renamed, every output that used the old name becomes stale.

**Quote blocks and prompts:** Any text shown to the solo in a quote block (like a sign-off prompt or a gate confirmation) must also be free of skill names. If a quote block says "I'll now run solo-qa," the solo reads it. It's output.

### No terminal commands handed to the solo

**The rule:** Never paste a command for the solo to copy and run. Execute the command directly, or (for significant/destructive operations) describe what's about to happen and ask permission, then execute it.

**Why:** Three failure modes occur when commands are handed to the solo:
1. The solo pastes it in the wrong directory or with wrong context
2. The solo reads it, intends to run it, gets interrupted, and forgets
3. The solo modifies it slightly based on a misunderstanding

All three produce errors that are harder to debug than if the framework had run the command correctly in the first place. The framework running commands directly eliminates all three.

**What "significant/destructive" means:** git push, rm -rf, dropping database tables, anything that can't be undone. For these, the framework describes what it's about to do and asks permission — then executes. The ask-then-execute pattern means permission is given with full information.

### Review is always visual — serve the result before asking for feedback

**The rule:** When build produces something reviewable (a screen, a component, an HTML artifact), the framework opens it in the browser or provides the URL before asking the solo for feedback. Never ask for feedback on something the solo can't see.

**Why:** "Does this look right?" while the solo cannot see what was built is a meaningless question. The solo can't evaluate something they haven't seen. The feedback request must come after the result is accessible.

**Where this applies:** End of design sprint (walk-through conversation happens after screens are served), end of each solo-build slice (serve before solo sign-off), any time a design change is made.

### Match response weight to moment

**The rule:** An approval is one sentence. A completed task states what was produced and asks the next question. No narrating what the solo just watched happen. No paragraph-length sign-offs.

**Why:** Responses longer than the moment warrants interrupt the solo's flow and bury the next action in text. If the solo approved something and the framework spends a paragraph confirming the approval and summarizing what was decided, the solo has to read through all of it to find out what to do next. Matching weight to moment means the solo always knows what the next action is without parsing narrative.

**"No narrating what the solo just watched happen":** If the solo watched a slice being built, the framework doesn't need to explain what was built. They watched it. The output is what was produced and what's next.

### Phase announcements never appear

**The rule:** Never say "I'll now begin the Discovery phase" or "I'm starting the Design Sprint."

**Why:** Phase announcements are the framework talking about itself. The solo is trying to build a product, not navigate a framework. A phase announcement interrupts the conversation to explain the system to the person who already knows they're using the system. One sentence of orientation ("let me ask a few things to get the full picture") then just start is the alternative — it's what a good teammate does.

### No abbreviations in solo-facing output

**The rule:** SBF (Solo Builder Framework) never appears in output shown to the solo. MCP never appears. Any code-identifier-style term (design-review, prd-to-plan, solo-qa) never appears in output shown to the solo. Use "the framework" everywhere SBF would appear.

**Why:** These are internal identifiers. They're meaningful to the curator and to the AI reading the SKILL.md files. They mean nothing to the solo and make the framework feel like a technical system rather than a thinking partner. "The framework routes to design review" sounds like a system announcement. "Let's start reviewing the design" sounds like a conversation.

### Transitions — specific format requirements

Phase gate format: "[Phase] complete. Outputs: [file 1] · [file 2]. Gate cleared. Start [next phase] now, or close out here?"

The format specifies:
- Name the phase that just completed (not the next one — the next phase hasn't started)
- List actual filenames, not categories ("discovery-brief.md · as-is-player-eval.md" not "discovery documents")
- One direct question with two named options

Two-path fork format: "Two paths: [action 1 in one sentence], or [action 2 in one sentence]. Which?"

Both paths must be named. Neither should be implied as the "right" choice. No hedging language.

---

## 9. Skill Design Notes — Non-Obvious Decisions

This section covers only skills where a curator making a change could easily get something wrong without knowing why it was written the way it was. Skills that are straightforward are omitted.

### start

**Why the three pre-routing checks come before Shape A/B/C:**
The most common mistake would be routing "I want to pick up this project" to brainstorm. The pre-routing checks (existing project context found, resume prompt detected, existing-project shape in message, spike-shape in message) filter these before Shape A/B/C routing runs. Shape A/B/C is only for genuine new-project messages.

**Why Shape C uses one question, not a menu:**
Giving the solo a menu of options ("Would you like to brainstorm, discover, or plan?") makes the framework visible — they're selecting a phase. One question ("Do you have a clear picture of what you want to build, or are you still working through the idea?") resolves the ambiguity without exposing the routing logic.

**Why start does NOT fire when existing project context exists:**
start is a routing skill for new conversations. If the project is already in flight, routing would restart the process from the wrong place. When context exists, start reads it, orients, and continues — it doesn't re-run the routing logic.

### discover

**Why Zone 3 (moment of value) produces the hero screen:**
Zone 3 is where the product's core value is most visible — the moment the user gets the thing they came for. Starting the design sprint's hero screen from this moment anchors the design in the product's purpose. If the hero screen were chosen by other criteria (easiest to design, most feature-complete), the design sprint would optimize for the wrong thing.

**Why the design on-ramp question comes after the brief is written:**
If asked before, the conversation anchors around tool availability ("I have a Figma") rather than the idea. The brief captures the story regardless of what design assets exist. The on-ramp question then determines how the design sprint uses those assets.

**Why technology is never discussed in discover:**
Technology questions during discovery pull the conversation from "what and why" to "how." This produces two failure modes: the solo describes a technical solution rather than a user problem, and constraints from the current tech stack narrow the design before the problem space is understood. Technology is discussed in tech-context, which runs after discover and before design sprint.

### design-sprint

**Why HTML over Figma:**
The design sprint produces HTML because HTML becomes the frontend. Figma requires translation — someone has to interpret the design and write HTML/CSS that matches it. The HTML artifact from the design sprint IS the starting point. This eliminates a translation step and ensures the design artifact is directly buildable. When a developer reads the design anchor "sprint-p1.html → Slot context card," they're looking at the actual file the frontend will extend.

**Why warmer/colder, not one-shot:**
Most people can't describe what they want visually until they see something wrong. This is a known phenomenon — articulating visual preferences is much easier in reaction to a proposal ("warmer") than in the abstract ("I want something clean"). The warmer/colder loop exploits this deliberately. One-shot design production would require the solo to describe what they want before they've seen anything, which most solos cannot do accurately.

**Enhanced mode (multi-agent orchestrator):** Claude Code only. Uses the Claude Code Agent tool to spawn four specialist agents in parallel. This capability doesn't exist in Cursor. The design-review SKILL.md has explicit "Tier 2 only. Requires Claude Code with enhanced mode active" and "skip this section entirely if running in Cursor." This must be preserved in any curator edit to design-review.

### design-review

**Why no slice reaches Ready on Round 1 without a process anchor:**
Round 1 is the first full pass. The process coverage map should be produced on Round 1 to identify all uncovered to-be steps. If slices could reach Ready on Round 1 without a process anchor, slices would be built before the coverage map identifies which to-be steps still have no slice. Process coverage gaps would be discovered in phase test instead of design review — when they're expensive to fix.

**Why "build starts when enough slices are Ready" is intentionally vague:**
"Enough" is a judgment call that can't be automated. The criterion is: does this set of slices form a coherent starting point that will produce something working end to end? That's a product judgment, not a count. Specifying a minimum number (e.g., "at least 5 slices") would either be too low (allowing a build to start with unrelated slices) or too high (forcing waterfall-style completion of all design before any build).

**Why the data behavior pass is required:**
Data questions (pagination, null handling, empty states, error states, volume) surface during phase test at high cost when not addressed during design review. The data behavior pass was added after this pattern was identified. It's required, not optional, for any screen with external data. The gate rule (data questions must be resolved before dependent UI slices reach Ready) exists because building a screen against unresolved data assumptions requires rework when the answers change the design.

**The coherence check before defining new slices:**
Before defining any new slice, check whether the codebase already expresses this pattern. This prevents silent duplicates — two slices that each do the same thing, neither done well because the overlap isn't visible. "Extend the existing pattern" or "explicitly diverge from it" are both valid choices. What's not valid is defining a new slice without checking whether something already exists.

### solo-build

**Why plan-driven selection, never "what would you like to work on?":**
The plan was agreed on. The backlog has priority order. Asking the solo what to work on next is the skill abdicating its job. The skill reads the backlog and states the next Ready slice by plan priority. This is not about the solo losing control — if the solo wants to divert from priority, they say so and the skill confirms the diversion explicitly ("You've asked to move to SL-X instead of SL-Y which is next in priority. Confirming that diversion and proceeding."). The diversion is explicit and deliberate, not silent.

**Why the status gate runs before everything else:**
A non-Ready slice has open design decisions. Building it contradicts those open decisions — whatever is built will need to be rebuilt or modified when the decisions close. The status gate isn't just quality control; it's protecting the solo from doing work that will need to be undone.

**Why tracer bullet first:**
The thinnest path through the full user journey proves integration before the codebase is large. Integration problems found when the codebase has 3 slices are cheap to fix. Integration problems found when the codebase has 15 slices are expensive. Tracer bullet forces integration problems to surface early.

**What "Build Active, no Ready slices" communicates:**
The previous name was "Build Pause." This was rejected because it implies the build has stopped due to a problem. "Build Waiting" and "Build Holding" were also rejected as too passive. "Build Active, no Ready slices" communicates the build is ongoing and waiting for slices to advance to Ready — not stopped, not broken, not paused. The distinction matters because the action is different: don't stop, go unblock the slices.

### product-continuity

**The Nivya exception:**
When Nivya is active in the conversation, product-continuity does not capture passively. This is a deliberate safety boundary. Nivya is for recall and exploration — the solo can think out loud with Nivya without those thoughts being recorded as decisions. If product-continuity captured every sentence from a Nivya conversation, exploratory thinking would contaminate the decision log. The rule: only what the solo explicitly says yes to (Nivya asks, solo confirms) gets written.

**Why product-continuity has 11 distinct document types:**
Each document serves a different retrieval need. The decision log is for "why was this decided?" The questions log is for "what needs an outside answer?" The assumptions log is for "what are we treating as true without proof?" The handoff is for "where do we pick up next session?" These are fundamentally different questions that require different document structures. Combining them would make each harder to use for its specific purpose.

### framework-health

**Why the framework update check runs at mode activation only:**
Checking for framework updates mid-session interrupts flow for something that should be resolved at the start. If an update is available, the solo decides at the beginning of the session whether to pull it. Once that decision is made, it doesn't need to be raised again. The mid-session update check was identified as an anti-pattern and is explicitly called out in the SKILL.md.

**The 21-day gap threshold for re-entry:**
21 days is long enough for meaningful codebase drift (other changes, stale branches), environment changes (dependency updates, config drift), and assumption staleness (things treated as true that may no longer be). Shorter gaps (one week) don't typically produce enough drift to warrant the re-entry protocol overhead. The threshold is explicitly 21 days — under that, silent.

**The phase test readiness nudge fires condition:**
All current-phase slices Done AND zero open qa-triage items. Both conditions are required. "All slices Done" without resolving qa-triage items means unclassified issues from the build phase — these would surface in phase test at higher cost if not resolved first. The nudge fires once only. If the solo isn't ready, they say so and it doesn't repeat.

### retrospective

**Why flag mode uses product-continuity as the capture mechanism:**
Flag mode observations are one-line notes appended to retro-notes.md. Product-continuity is already running throughout every session. Having retrospective use a separate capture mechanism would require the solo to maintain awareness of two background capture processes. Using product-continuity as the capture vehicle means there's one background process, not two.

**Why retro mode processes at phase end, not after every observation:**
Phase end is when enough observations have accumulated to identify patterns. A single observation after one session isn't a pattern — it might be a project-specific quirk. Three observations of the same issue across three sessions is a pattern worth fixing. Processing at phase end also has the right context: the full phase just completed, and the retrospective can evaluate what worked and what didn't across the whole phase.

### phase-test

**Why Stage 1 (environment readiness) blocks all other stages:**
Testing against a misconfigured environment produces false results — passes that will fail in production, failures that are actually config problems. All seven stages work against the assumption that the environment is correctly configured. If that assumption is wrong, every finding is unreliable. Stage 1 confirms the assumption holds before anything else runs.

**Why Stages 4 and 5 run together:**
The tester (walks scenarios) and regression specialist (re-walks Done slices) are independent — neither depends on the other's findings to proceed. Running them in parallel reduces total test time. Their findings are synthesized in Stage 7.

**Why HOLD means "fix specific items and re-test affected scenarios" not "re-run everything":**
A full re-run after fixing one item would be wasteful and discouraging. The HOLD output specifies exactly which scenarios failed and why. After fixes, only the affected scenarios need re-walking. This is the right scope for partial re-testing.

**Why the acceptance reviewer (Stage 6) runs after testing (Stages 4 and 5):**
The acceptance reviewer asks a PM-level question: "Does this solve the problem we set out to solve?" This requires knowing whether the product works (Stages 4 and 5 confirm this). If the product has multiple failing scenarios, there's no point asking whether it solves the original problem — the question can't be answered honestly until the product is working.

### code-review-and-quality

**Why "all seven checks must pass, no partial passes":**
A partial pass gives the impression that the slice is "mostly ready" while actually leaving quality problems unresolved. A slice with six passing checks and one failing check has a specific problem that needs to be fixed. Marking it as mostly-passed would let it proceed to solo-qa with a known issue, which would then fail QA anyway. The all-pass requirement means every slice that proceeds to solo-qa is clean — no known issues that QA will catch.

---

## 10. Dual-Tool Matrix — Claude Code vs Cursor

The framework runs in two tools. Most behavior is identical. The differences are explicit and must be maintained consistently.

| Behavior | Claude Code | Cursor |
|---|---|---|
| Framework configuration file | `~/.claude/CLAUDE.md` | User Rules (paste from template) |
| Session mode activation | Reads from CLAUDE.md | Reads from User Rules |
| Output Contract source | CLAUDE.md | User Rules (cursor-user-rules-global-playbook.md) |
| Hook wiring | `.claude/settings.json` | Not available |
| Enhanced mode (design-review multi-agent) | Available — uses Agent tool | Not available — skip enhanced mode section |
| Framework update check | `git fetch` + `rev-list` — available in both | Same command, runs in both |
| MemPalace integration | Available — CLI at ~/.venv/bin/mempalace | Not available |
| Framework curator | Always Claude Code — never Cursor | Not used for curator work |
| code-review-and-quality as independent session | Recommended — fresh Claude session has no build context, gives independent eyes | Not applicable — Cursor context is per-conversation |
| Always-on skill loading | CLAUDE.md triggers on mode activation | User Rules triggers on mode activation |
| Named project resume | CLAUDE.md reads projects.md | User Rules reads projects.md |

### The Cursor Dual-File Rule

This is the most common curator error. Cursor reads from the INSTALLED rules file, not the template. When any behavior change affects Cursor:

**Two files must always be updated in the same curator pass:**
- `templates/cursor-user-rules-global-playbook.md` — the source template for new machine setup
- `~/.cursor/rules/solo-builder-start.mdc` — the installed rules that Cursor actually reads

Updating only the template means the current machine's Cursor continues to use the old behavior. Updating only the installed file means new machines that set up from the template get the old behavior. Both must be updated together without exception.

### Claude Code Exclusive Features

**Enhanced mode in design-review:** The multi-agent orchestrator in design-review uses Claude Code's Agent tool to spawn four specialist agents in parallel. This tool doesn't exist in Cursor. The design-review SKILL.md has explicit tier gating ("Tier 2 only. Requires Claude Code with enhanced mode active"). Any edit to design-review must preserve this gating and not remove the "skip in Cursor" instruction.

**Hook wiring:** Claude Code settings.json hooks. Cursor has no equivalent. Any behavior the framework achieves through hooks in Claude Code must have a Cursor alternative (User Rules instruction, if possible) or be documented as Claude Code-only.

**MemPalace:** The MemPalace CLI is a Claude Code tool. It's available via the `mempalace` command. Cursor has no access to it.

**Framework curator:** The curator skill is used exclusively in Claude Code sessions with Scott. It is never run in Cursor. Curator changes that affect Cursor behavior are executed in Claude Code and then verified in the installed Cursor rules file.

---

## 11. File Index and Cascade Map

### Files in Scope for Curator

These files may be changed in any curator session. The curator is responsible for keeping them consistent with each other.

| File | Purpose | Changes when |
|------|---------|-------------|
| `skills/*/SKILL.md` | Behavior instructions for each skill | Skill behavior, routing, output, or anchors change |
| `docs/records-spec.md` | Canonical field definitions for Slice, Deliverable, Phase records | Record format, status chain, verification model, re-phasing protocol change. Skills read this first — any record-level behavior change starts here |
| `README.md` | AI-facing overview + external overview | Skill count, phase list, always-on table, repo structure change |
| `docs/solo-builder-framework.md` | Full phase chain + principles source | Phase flow, skill table, always-on list, session modes, gates change |
| `docs/communications/skills-reference.html` | All skill cards + sidebar nav | Any skill added, removed, or described differently |
| `docs/communications/process-map.html` | Swimlane of all phases and lanes | Phase flow, skill placement, gate outputs change |
| `docs/communications/deck-business.html` | Executive deck (11 slides) | Material framework changes affecting the story told to business audiences |
| `docs/communications/deck-solo.html` | Practitioner deck (12 slides) | Phase flow, mechanics, QA chain, anchors change |
| `docs/communications/guide-build.html` | Build phase guide | solo-build, code-review-and-quality, solo-qa, qa-triage behavior changes |
| `docs/communications/guide-qa.html` | QA phase guide | solo-qa, code-review-and-quality behavior changes |
| `docs/communications/guide-phase-test.html` | Phase test guide | phase-test behavior changes |
| `docs/communications/guide-discover.html` | Discover phase guide | discover, process-mapper behavior changes |
| `docs/communications/backlog-status-reference.html` | Status reference for Slice/Deliverable/Phase | Any status name change, new status added, ownership change |
| `docs/communications/index.html` | Communications hub | New docs added, existing docs renamed or removed |
| `docs/communications/blog.html` | Release notes | Significant framework changes — always included in the cascade for any material behavior change |
| `templates/cursor-user-rules-global-playbook.md` | Cursor User Rules source template | Any behavior change affecting Cursor |
| `templates/claude-global-playbook.md` | Claude global playbook template | Any behavior change affecting Claude Code |
| `~/.claude/CLAUDE.md` | Installed Claude rules — authoritative Output Contract | Output Contract changes (always first), session modes, routing logic |
| `~/.cursor/rules/solo-builder-start.mdc` | Installed Cursor rules | Same changes as cursor-user-rules-global-playbook.md — always together |
| `CURSOR-SETUP-PROMPT.md` | Session-only Cursor primer | New always-on skill added, session modes change |
| `CLAUDE-CODE-SETUP-PROMPT.md` | Session-only Claude Code primer | New always-on skill added, reading list changes |
| `projects.md` | Named project registry | New project added |
| `docs/curator-context.md` | This file | Any load-bearing decision changes — add to Decisions Log |

### Files Out of Scope for Curator

| File/Directory | Why out of scope |
|---|---|
| `docs/process/` | Project-specific process maps, not framework files |
| `docs/continuity/` | Project-specific continuity docs, not framework files |
| `docs/design/` | Project-specific design artifacts |
| `references/` | Reference materials, not framework instructions |
| `templates/claude-agents/` | Project-level agent templates, not framework |
| `templates/claude-commands/` | Project-level command templates, not framework |
| `packaging/dist/` | Built artifacts |

### Cascade Map — Change Type to Affected Files

**Adding a new skill:**
1. `skills/[new-skill]/SKILL.md` — create
2. `README.md` — add to phases table or supporting skills list
3. `docs/solo-builder-framework.md` — add to skills table
4. `docs/communications/skills-reference.html` — add nav entry + skill card in correct category section
5. `docs/communications/process-map.html` — add lane entry if it appears on the swimlane
6. `templates/cursor-user-rules-global-playbook.md` — add to correct skills list
7. `templates/claude-global-playbook.md` — same
8. `~/.cursor/rules/solo-builder-start.mdc` — same (always together with template)
9. If always-on: `CURSOR-SETUP-PROMPT.md` + `CLAUDE-CODE-SETUP-PROMPT.md` reading lists
10. If it changes a phase guide: relevant `docs/communications/guide-*.html`

**Retiring a skill:**
1. Check for references in all other `skills/*/SKILL.md` files first — grep for the skill name
2. `skills/[skill]/SKILL.md` — delete
3. All items from "adding a new skill" cascade, in reverse
4. Any other SKILL.md that references the retired skill — update those references

**Changing a skill's behavior:**
1. `skills/[skill]/SKILL.md` — update
2. `docs/communications/skills-reference.html` — update skill card description + key elements if behavior changed materially
3. `docs/communications/process-map.html` — update if the skill's place in the phase flow changed
4. Relevant `docs/communications/guide-*.html` — update if a phase guide covers this behavior
5. If always-on behavior changed: `README.md` always-on table + `docs/solo-builder-framework.md` always-on section
6. If activation type changed: update badge in `skills-reference.html` + all documentation describing the activation

**Changing a load-bearing principle:**
1. `~/.claude/CLAUDE.md` — if Output Contract principle, update here FIRST
2. Every `skills/*/SKILL.md` that implements the principle — find by grep
3. `docs/solo-builder-framework.md` — key constraints section + relevant phase description
4. `README.md` — AI-facing section if the principle appears there
5. All `docs/communications/*.html` that articulate the principle to external audiences
6. Both templates and installed Cursor rules if the principle affects output behavior
7. `docs/curator-context.md` — update this file + add to Decisions Log

**Changing session modes or routing:**
1. `~/.claude/CLAUDE.md` — session modes section
2. `README.md` — session modes table
3. `docs/solo-builder-framework.md` — session hygiene section
4. `skills/start/SKILL.md` — routing logic
5. `templates/cursor-user-rules-global-playbook.md`
6. `templates/claude-global-playbook.md`
7. `~/.cursor/rules/solo-builder-start.mdc` (always with template)
8. `CURSOR-SETUP-PROMPT.md` + `CLAUDE-CODE-SETUP-PROMPT.md`

**Changing Output Contract behavior:**
1. `~/.claude/CLAUDE.md` — ALWAYS FIRST. It is the authority.
2. All `skills/*/SKILL.md` files that implement the changed behavior (grep for the relevant behavior pattern)
3. Both templates (cursor-user-rules, claude-global-playbook)
4. `~/.cursor/rules/solo-builder-start.mdc`
5. NOT the communications docs — the Output Contract is AI-facing, not user-facing

**Downstream check — always ask before finalizing any cascade:**
Does this change affect the build phase (solo-build), the QA chain (code-review-and-quality, solo-qa), the phase test, or deploy? If yes, those skills and their guide pages are in the cascade.

---

## 12. Decisions Log

Append an entry after every curator session. Format: date, what changed, why, what was rejected.

---

### 2026-04-27 — Status gate terminology: "Build Pause" → "Build Active, no Ready slices"

**What changed:** Renamed the state when all current-phase slices are Done/In Review/Deferred and none are Ready. Files changed: `skills/solo-build/SKILL.md`, `docs/communications/guide-build.html`.

**Why:** "Build Pause" implies the build has stopped due to a problem. "Build Waiting" and "Build Holding" were considered and rejected as too passive. "Build Active, no Ready slices" communicates the build is ongoing and the system is waiting for slices to advance to Ready — the appropriate action is to go unblock slices, not investigate a problem.

**What was rejected:** "Build Waiting" (too passive, implies the builder is waiting for something external), "Build Holding" (similar problem).

---

### 2026-04-27 — Plan-driven slice selection added to solo-build

**What changed:** solo-build now reads the backlog and states the next Ready slice by plan priority. It never asks the solo what to work on. If the solo diverts from priority, the skill confirms the diversion explicitly before proceeding. File changed: `skills/solo-build/SKILL.md`.

**Why:** Asking the solo what to work on next abdicates the skill's job. The plan exists. Following the plan is the skill's responsibility.

---

### 2026-04-27 — Framework audit: 10 clear fixes

**What changed:** Ten editorial/content/Output Contract fixes across 10 files:
- `docs/solo-builder-framework.md`: removed stale working-doc header; "assisted" → "piloted" ×2
- `CURSOR-SETUP-PROMPT.md`: "assisted" → "piloted"; removed nonexistent `workshop/README.md` reference
- `CLAUDE-CODE-SETUP-PROMPT.md`: removed nonexistent `workshop/README.md` reference
- `README.md`: skill count 29 → 38 (×3); removed broken workshop link
- `skills/deploy/SKILL.md`: Method C now runs command directly instead of handing to solo
- `skills/awesome-design-md/SKILL.md`: Step 2 now WebFetch + write directly instead of handing to solo
- `skills/design-sprint/SKILL.md`: duplicate step "4." in Figma on-ramp renumbered to "5."
- `skills/onboard/SKILL.md`: all "the the" / stray-word artifacts removed
- `skills/prd-to-plan/SKILL.md`: skill name `/to-issues` removed from user-facing Step 9
- `skills/tdd/SKILL.md`: all 5 broken relative file links removed (tests.md, mocking.md, deep-modules.md, interface-design.md, refactoring.md)

**Why "assisted" was wrong:** "Assisted" was a legacy name for what became "piloted." The rename happened but wasn't fully propagated. Three occurrences were found in the framework doc and setup prompts.

**Why workshop/README.md references were wrong:** Workshop was integrated into the main skills/ directory. A separate workshop/ subdirectory was never created.

---

### 2026-04-27 — code-review-and-quality SKILL.md created from scratch

**What changed:** The skill directory was a dead symlink to `/Users/scottheinemeier/.claude/plugins/agent-skills/skills/code-review-and-quality` — a path that doesn't exist. The symlink was removed and a real SKILL.md was written. File: `skills/code-review-and-quality/SKILL.md` (new).

**Why the content is correct:** The 7 checks were already fully specified in `skills-reference.html` and `docs/solo-builder-framework.md` as the authoritative descriptions of what this skill does. The SKILL.md was written to match those descriptions exactly. No behavior was invented — the implementation was written to match the documented specification.

**The 7 checks:** pattern compliance, data sourcing, expandability, cleanliness, scope discipline, documentation, stack compliance.

---

### 2026-04-27 — agent-room deleted

**What changed:** `skills/agent-room/SKILL.md` deleted. All references removed from `docs/solo-builder-framework.md` (×2), `docs/communications/skills-reference.html` (nav + card), `docs/communications/guide-build.html` (skill block), `templates/cursor-user-rules-global-playbook.md`, `templates/claude-global-playbook.md`.

**Why:** agent-room was an external download from author "hungv47" (MIT license, v2.0) — not created for this framework. It referenced four non-existent companion skills (review-chain, system-architecture, task-breakdown, competitive-landscape from the same external skill set). It saved reports to `.agents/meta/` — not a framework path. Scott confirmed it was never used.

---

### 2026-04-27 — docs/curator-context.md created

**What changed:** This file created as Step 2 of the Framework Audit Initiative.

**Why:** As the framework grows in complexity, curator sessions need reliable access to the reasoning behind decisions — not just the instructions themselves. Git history and MemPalace are too many steps removed from the actual files being changed. This document puts the reasoning adjacent to the work.

**Pending work from audit:**
- ~~Backlog items 001, 003, 004, 005, 006, 007~~ — all resolved (see 2026-04-27 entries below)
- Step 3 of audit initiative: design and wire curator hook in `.claude/settings.json`
- Step 4 of audit initiative: communications docs reconciliation pass against audit findings
- Plain language audit: solo-facing output across all skills — not yet executed

---

### 2026-04-27 — Framework-wide language pass: directives not suggestions

**What changed:** Two-pass audit across 14 SKILL.md files. Eliminated soft/suggestive language throughout — every instruction that read as a recommendation now reads as a directive with defined consequence.

**Pass 1 (modal swaps where enforcement context was already defined):**
- `data-scaffold/SKILL.md`: "The UI should not know or care" → "must not know or care"
- `phase-test/SKILL.md`: "should reflect a clean, unified state" → "must reflect"
- `principal-engineer/SKILL.md`: "the PE should assess" → "the PE assesses"
- `retrospective/SKILL.md`: "It should be reinforced" → "Reinforce it"
- `tdd/SKILL.md`: "Tests should verify behavior" → "Tests verify... must not change"
- `to-issues/SKILL.md`: "a builder should be able" → "must be able"
- `to-prd/SKILL.md`: two "should" swaps in user story requirements
- `design-review/SKILL.md`: "Every slice should implement" → "must implement"

**Pass 2 (full rewrites adding action + consequence where none existed):**
- `design-sprint/SKILL.md`: uncovered process steps now require immediate surface as a decision; "secondary screens should move faster" → factual; "should proactively flag" → "flag proactively"
- `prd-to-plan/SKILL.md`: "first slice should prove" → rewrite adding reorder requirement; process order → "don't reorder these for convenience"; backlog anchor → "must be in the record before build starts"
- `process-mapper/SKILL.md`: three "should" instances rewritten — to-be map traces are now "must" with explicit consequence ("never silently absorbed"); drift clause adds explicit decision requirement and process-change invocation
- `framework-health/SKILL.md`: "should reflect" → "Verify... reflect... flag it — don't wait to be asked"
- `brainstorming/SKILL.md`: "should reflect a step" → "must reflect... no clean mapping is a signal — process sketch needs more work"
- `dependency-upgrade/SKILL.md`: "when possible" clause replaced with explicit high-traffic-window confirmation protocol

**Why:** Surface-level "should → must" swaps were correctly identified as insufficient. The real problem is instructions that describe a required state without defining what the AI does when that state isn't met. Pass 2 targets those — instructions now carry an action path and a consequence.

**What was rejected:** Simple find-replace across all instances. The two-pass strategy was chosen because ~30 of the 84 hits were quality descriptions of output (acceptable), ~24 were inside quotes/templates (not actionable) — blanket replacement would have corrupted those.

---

### 2026-04-27 — Backlog item 006: canonical record format for slice, deliverable, and phase

**What changed:** Six skills updated, one new spec document created.

**New file — `docs/records-spec.md`:** Canonical specification for all three record types (Slice, Deliverable, Phase). Every skill that reads or writes backlog records must read this first. Contains: status structures for all three types, full field definitions, two-description rule, three-level verification model, Done vs Accepted distinction, re-phasing protocol (7 steps), decisions and change log format, skill ownership table.

**Skills updated:**
- `design-review/SKILL.md`: reads records-spec.md first; full new slice record format embedded with field rules; At a Glance Traffic section; Ready gate expanded to 10 conditions; new anti-patterns for missing descriptions, copying across levels, blank fields
- `data-scaffold/SKILL.md`: new Step 3.5 — immediately update slice records after generating mock files; slices with Pending data-scaffold cannot reach Ready
- `prd-to-plan/SKILL.md`: reads records-spec.md first; full deliverable record format (Integration as third type); full phase record format with anti-pattern; Step 8b post-approval backlog write protocol (4 steps)
- `solo-build/SKILL.md`: reads records-spec.md first; 5-step code-complete protocol with builder confirmation; deliverable completion 3-step protocol; re-phasing protocol (7 steps); new anti-patterns
- `solo-qa/SKILL.md`: deliverable acceptance reads new record fields (plain language, technical, screens, acceptance criteria, self-verification checklist, builder confirmation); slices move to `In Test` (not Done) after solo sign-off; Done is reserved for phase-test completion; deliverable status uses `Accepted` (not `✓ Accepted`)
- `phase-test/SKILL.md`: reads records-spec.md; readiness gate checks for `In Test` (not Done); gate-open protocol explicitly updates slice statuses to `Done` and phase status to `Completed` in backlog

**Core decisions made:**

*Two descriptions at every level.* Every record carries a plain language description (solo audience) and a technical description (builder audience), both written fresh at that level — never copied or paraphrased from another level. A phase description is not a summary of its deliverables.

*Three-level verification.* Self-verification checklist + acceptance criteria + builder confirmation at slice, deliverable, and phase. Each level checks what only that level can see. Slice: does this element work on its own. Deliverable: do the slices work together. Phase: does the complete capability work end-to-end.

*Integration deliverable as third type.* Screen | Logic | Integration. Integration connects real data to a Screen deliverable — contains both UI slices and data integration slices; always sequences after its Screen companion is Accepted; can spawn new slices when real data reveals gaps. This resolved the ambiguity around when Done means mock data vs real data.

*Done vs Accepted.* Done lives at the slice level (built and verified against its data anchor). Accepted lives at the deliverable level (solo signed off). These were previously conflated.

*Status naming — no duplicates.* Deliverable statuses renamed to Defined | Active | Pending Acceptance | Accepted to eliminate collision with slice-level In Review and In Build.

*Re-phasing protocol.* 7-step formal process when a slice/deliverable moves phases. Requires solo confirmation, decision log entry, and update of source + destination phase records. All 7 steps in the same action.

*In Test introduced.* Slice reaches `In Test` after solo-qa sign-off. Reaches `Done` only after phase-test gate opens. Eliminates ambiguity about whether a Done slice has been phase-verified.

**What was rejected:** Making Done mean "verified at any data layer" without distinguishing mock vs real — rejected because it made Done ambiguous and deferred the hard question. Making the integration work part of the Screen deliverable — rejected because it conflated two distinct review modes (visual vs evidence-based) and obscured whether real-data work was actually complete.

---

### 2026-04-27 — Framework backlog items 001, 003, 004, 005, 007 verified resolved

**What was found:** All five remaining backlog items against solo-build were already addressed in the current `skills/solo-build/SKILL.md` — resolved by the records-spec cascade (item 006) without a separate targeted fix for each. Verified by reading the SKILL.md directly.

- **001 (design sprint files ignored):** Session Start Step 7 reads design sprint artifacts; "Before writing code" Step 3 requires reading and reporting the anchor element from the file before writing code.
- **003 (re-asking captured info):** Session Start reads all discovery/design docs upfront; four anchors come from the backlog record — the information is already present, no reason to ask.
- **004 (status updates delayed):** "Backlog Updates During Build" section added explicit "Not at session end" language; every transition listed with immediacy.
- **005 (commenting not happening during build):** "During build" added "Comment non-obvious logic as you write it — not as a cleanup pass."
- **007 (terminal commands handed to solo):** Code-complete Step 2 says "Execute the commit directly — do not hand this to the solo."

**Why they were resolved without being explicitly targeted:** The records-spec work restructured the session start, code-complete protocol, and backlog update protocol in ways that addressed these behaviors as a side effect of making the skill coherent. The backlog items described symptoms; the records-spec work addressed the underlying structure.

**Remaining:** Plain language audit — not yet executed.

---

### 2026-04-29 — Pre-build read gate, evidence-based self-verification, review_url field, stuck protocol

**Source:** Notes from the Solo Companion project build session (2026-04-28), captured in `docs/continuity/framework-improvements.md` and `docs/continuity/handoff.md` in the solo-companion project.

**What changed:** Four additions to `skills/solo-build/SKILL.md`, one to `docs/records-spec.md`, one to `skills/solo-qa/SKILL.md`, three watchfor items to `docs/communications/guide-build.html`.

**1 — Pre-build read gate (Proposals 1 + 3)**
Added Step 0 to "Before writing code": builder must read the full slice record and open the design file before writing any code. Confirmed by stating one specific observation from each. Cannot be skipped for slices that seem familiar. Source: SL-011 was rebuilt from scratch because the builder inferred the layout from memory instead of reading the design file (right-side panel built instead of centered modal).

**Why the evidence requirement:** "I read it" is not verifiable. Requiring the builder to produce one concrete observation from each document closes the gap between "read" and "skimmed" or "assumed from context."

**2 — Evidence-based self-verification (Proposal 3)**
Updated Step 1 of code-complete: self-verification must be run against the running app, not the code. Every checklist item requires a statement of what was actually observed in the rendered output. "Data renders correctly" is explicitly invalid. Source: builder was listing self-verification items by reading code and assuming the output was correct — the same check code-review-and-quality already ran. Four hours were lost in one session before the solo forced a restart.

**Why the evidence standard matches solo-qa Part 1:** solo-qa already had the correct standard ("rendered value is X — matches field Y in mock file Z"). Self-verification was the missing enforcement of that same standard earlier in the chain.

**3 — review_url field on slice records (Proposal 2)**
Added `Review URL` field to the slice record template in `docs/records-spec.md` and its field definition. Builder writes it at code-complete alongside the status → In QA update. It is the exact URL where the solo can open the completed work in a browser. `None` for non-previewable slices. solo-qa reads it from the record (not reconstructed informally). Source: Solo Companion already expected this field (renders a "▶ Review" button in the companion app); the framework had no formal definition for it.

**4 — Stuck protocol (Proposal 3)**
Added "When Stuck" section to solo-build: two failed attempts with no progress → stop. Re-read the full slice spec and design file from scratch before any further code changes. Report what was found. Ask one diagnostic question. And: the solo's explicit request to step back is an immediate directive — the builder does not evaluate whether it is warranted, does not suggest one more attempt, does not express confidence that the current approach will work. Source: builder refused the solo's direct requests to step back twice in the same session while stuck on an HTML rendering issue with unclosed brackets. "Being confident progress is close" is not a valid reason to override the solo.

**What was rejected:** Requiring the builder to produce longer evidence statements before build (e.g., a full walkthrough of the design file). Rejected as too slow for routine slices. One specific observation from each document is the minimum that proves the file was actually read — not so burdensome that it creates friction on fast slices, not so light that memory substitutes for reading.

**Files changed:** `skills/solo-build/SKILL.md`, `docs/records-spec.md`, `skills/solo-qa/SKILL.md`, `docs/communications/guide-build.html`, `docs/curator-context.md`.

---

### 2026-04-29 — CHANGELOG.md + versioned releases + projects.md isolation

**Context:** Framework now has multiple users. Need release discipline so users can understand what changed and whether they must update.

**Changes made:**
- `CHANGELOG.md` created at repo root — versioned entries with BREAKING / RECOMMENDED / MINOR severity labels and explicit action required per release. Machine and human readable. Backfilled to v1.0.0.
- `skills/framework-curator/SKILL.md` — Step 5 updated: curator now writes a CHANGELOG entry, tags the commit, and pushes with `--tags` on every change. Version bump rules documented (major/minor/patch).
- Documentation cascade table updated: `CHANGELOG.md` added as always-updated on every change.
- `projects.md` removed from repo tracking and added to `.gitignore`. Replaced with empty template. Personal project paths were leaking to other users' installs — the start skill was resuming the wrong person's projects on fresh installs.

**Version anchors:**
- v1.0.0 → commit `9af130f` — records-spec cascade
- v1.1.0 → commit `9093629` — plan-driven selection + Build Active
- v1.2.0 → commit `c456257` — builder discipline + review_url + projects.md fix

**Files changed:** `CHANGELOG.md` (new), `skills/framework-curator/SKILL.md`, `docs/curator-context.md`, `.gitignore`, `projects.md` (removed from tracking).

---

### 2026-04-29 — solo-qa: "Done" → "In Test" in deliverable acceptance section (bug fix)

**What changed:** Three instances of "Done" in the Deliverable Acceptance section of `skills/solo-qa/SKILL.md` were using the wrong status. The canonical definition at the bottom of the same file (lines 296–309) is unambiguous: slices reach `In Test` after solo sign-off and only reach `Done` after phase-test completes. The three ambiguous lines created a false reading that deliverable acceptance could trigger when all slices were solo-signed-off (i.e., effectively Done), allowing phase test to be skipped.

**Root cause:** This was a framework bug, not solely a builder compliance failure. The deliverable acceptance section was written with "Done" as shorthand for "passed QA" — but in the canonical status chain, Done has a precise meaning reserved for phase-test completion. The inconsistency gave builders a plausible reading that bypassed the phase gate.

**Lines fixed in `skills/solo-qa/SKILL.md`:**
- Line 192: "When all slices in a deliverable are Done" → "In Test"
- Line 243: "All [N] slices are Done." → "All [N] slices are In Test."
- Line 274: "all slices Done" → "all slices In Test"

**What was rejected:** Adding a more explicit warning block at the top of the Deliverable Acceptance section. Rejected — fixing the status terminology is the right correction. A warning block treats the symptom; correcting the language treats the cause.

**Files changed:** `skills/solo-qa/SKILL.md`, `docs/curator-context.md`.

---

### 2026-04-29 — solo-simulator skill added

**What it is:** A new on-demand skill that stands in for the human solo at every framework decision gate during a test run. Operates from a locked brief generated via a 13-question Q&A sequence. Approve / pushback / escalate + best-call decision logic. Produces a live flag surface during the run and a persistent decision log + post-run report.

**Why it was built:** Three converging needs: (1) framework testing without a human at every gate, (2) token usage comparison data between framework and no-framework builds, (3) long-term autopilot mode for the framework. The same skill serves all three purposes at increasing levels of sophistication.

**Activation taxonomy:** On-demand. Invoked with `/solo-simulator`. Never auto-loaded. Runs for the duration of the test run, then exits.

**Design decisions:**
- Brief is locked at confirmation — never changes mid-run. Mid-run changes require a new run.
- Pushback is always specific — cites the exact brief field and states observed vs. required. Never vague.
- Never blocks after Round 2 — escalate + best-call keeps the run moving regardless.
- Human override always possible — logged as a distinct decision type, not overwritten.
- Live flag surface is observability only — not a control gate. Run continues without human action.
- Every decision logged including approvals — the log is the full calibration record.

**First test project:** Gift Tracker (Option C from test project selection). Scott runs non-framework version; simulator runs framework version. Metrics captured in `docs/session-metrics.md`.

**Non-visual product note:** This build revealed that the framework's design sprint phase doesn't apply to skill files. A spec pass (defining exact structure and format of each output file before writing) was used instead. This is the first real data point for closing Hole #1 (non-visual products).

**Files created:** `skills/solo-simulator/SKILL.md`, `templates/solo-sim-brief-template.md`.
**Files updated:** `README.md` (skill count 38→39), `docs/solo-builder-framework.md`, `templates/cursor-user-rules-global-playbook.md`, `templates/claude-global-playbook.md`, `~/.claude/CLAUDE.md`, `docs/curator-context.md`.
