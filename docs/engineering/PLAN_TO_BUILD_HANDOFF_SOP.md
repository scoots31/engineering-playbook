# Standard operating process: Plan → Build handoff (every project)

**Purpose:** When **discovery / research / planning** happen in one place (often **Cursor**) and **implementation** happens in another (often **Claude Code**, **Claude** web/projects, or another coding agent), this SOP defines **what artifacts must exist**, **what to paste or attach per Build task**, and **how to run the Build phase** for **efficiency** (small context, clear done) and **accuracy** (no silent scope drift or duplicate domain logic).

**Scope:** Tool-agnostic. “Plan driver” and “Build driver” can be any combination you use; the **contracts** are what matter.

**Related:** [`AI_PLAYBOOK.md`](AI_PLAYBOOK.md) (stages, roles), [`HANDOFF.template.md`](HANDOFF.template.md) (mid-flight session switch), [`global-for-all-projects.md`](global-for-all-projects.md) (where the playbook lives).

---

## 1. When this SOP applies

Use this SOP whenever:

- There is a **meaningful Plan phase** (problem, constraints, success metrics, sequencing) **before** a multi-step Build, **or**
- You **switch tools or models** between “figure it out” and “ship it,” **or**
- More than one person/agent touches the same repo and you need a **shared definition of done**.

Skip heavy ceremony for **one-line fixes**; still keep **one sentence of intent** in the task prompt.

---

## 2. Vocabulary (align with your head)

| Term | Meaning here |
|------|----------------|
| **Capability group** | Umbrella domain (e.g. *billing*, *auth*, *player evaluation*). |
| **Capability** | A discrete user-visible outcome inside that group. |
| **Requirement** | A specific behavior or constraint **inside** one capability. |
| **Slice / milestone** | A **bounded delivery unit**: thin vertical increment **or** a planning package with **acceptance** and **dependencies**—the usual **unit of work** you hand to Build. |
| **Shared spine** | Domain or technical artifact used **across** capabilities (e.g. one pricing engine, one parameter table, one ingest pipeline)—**implement once, consume many**. |

Slices **sequence** work; they do not replace **capability → requirement** traceability. Each slice should **name** which capabilities it advances.

---

## 3. Required outputs from Plan (the Build handoff bundle)

Before Build treats work as “ready,” the **product repo** (or agreed doc tree) should contain **at minimum**:

| # | Artifact | What “good” looks like |
|---|----------|------------------------|
| 1 | **North star / principles** | Locked **decisions** and non-goals (e.g. `VISION.md`, `Brainstorm Notes.md`, or a short **Decisions** section). Build does not reopen these without an explicit change request. |
| 2 | **Plan charter** | One file the team agrees is **L0**: scope, sequencing, gates (e.g. `PLAN.md`, `ROADMAP.md`). Includes **where** slice docs live. |
| 3 | **Coherence / reuse guardrails** | Explicit rules: **shared spines**, no duplicate domain math, one pattern for repeated flows (may live **inside** the Plan charter as a section—see Fantasy example `PLAN.md` §3). |
| 4 | **Scope / MVP statement** | What v1 **must** demonstrate; narrow **carve-outs** only (avoid a giant “non-goals” dump that contradicts MVP). |
| 5 | **Per-slice (milestone) packages** | For **each** Build chunk: problem, **in/out of scope**, **acceptance** (testable), dependencies, risks, links to schemas/APIs. |
| 6 | **Data / API / entity inventory** (when relevant) | Tables, fields, ids—so Build does not guess from chat memory. |
| 7 | **Open decisions log** | ID, question, chosen option **or** “deferred with owner.” Build must not resolve these silently. |

**Nice-to-have (add as soon as useful):**

- **Wireframes or UX acceptance** for user-facing slices (Design stage).  
- **ADRs** for irreversible choices.  
- **Traceability matrix** (capability ↔ slice ↔ requirement id) for regulated or large efforts.

---

## 4. How to prompt Build: hybrid, slice-first (recommended)

### 4.1 Do **not** rely on “read the entire plan and improvise” as the only instruction

Whole-plan-only prompts tend to:

- **Burn context** on narrative you already wrote.  
- **Reorder** work in ways that **skip dependencies** or gates.  
- **Miss reuse rules** and re-implement shared spines in feature folders.

### 4.2 Do **not** use slice-only prompts with **zero** global guardrails

Slice-only risks **local optimization**: contradicts a global decision or duplicates a spine another slice owns.

### 4.3 Recommended pattern: **slice package + thin global layer**

For **each** Build task or PR:

1. **Attach the slice doc(s)** (or equivalent milestone spec) that define **this** chunk: acceptance, out of scope, dependencies.  
2. **Attach or inline by reference** the **thin global layer**:  
   - Plan charter section on **reuse / shared spines** (or this SOP §5 prompt block).  
   - **Principles / Decisions** that apply to *all* slices (short excerpt or “read `…` Decisions section only”).  
3. **State the branch goal in one sentence** and what **done** means (copy acceptance bullets).

**Optional instruction to the Build driver:**  
> “Derive a **task checklist** from the attached slice only. Do **not** expand scope beyond the slice’s **out of scope** table. If you need a decision, **stop** and list options with IDs from the open-decisions log.”

---

## 5. Copy-paste prompt blocks (adapt names/paths)

### 5.1 Stable “Build driver” system preamble (keep in project `CLAUDE.md`, repo AGENTS.md, or Claude project instructions)

```text
You are the Build driver for <PROJECT_NAME>.

Sources of truth (read relevant sections only; do not contradict locked Decisions):
- <PATH_OR_LINK_TO_PRINCIPLES_OR_BRAINSTORM>
- <PATH_TO_PLAN_CHARTER> — including the reuse / shared-spine section if present
- The attached slice doc(s) for THIS milestone only

Rules:
- Implement from written acceptance; do not expand scope beyond the slice’s stated out-of-scope list.
- Shared domain logic (<LIST SPINES: e.g. auth, pricing, league parameters>) lives in one place; feature code consumes it—no silent duplicate formulas or parallel “save” patterns.
- If the slice is ambiguous or conflicts with a Decision, stop and ask rather than inventing.
```

### 5.2 Per-task prompt (repeat each slice / PR)

```text
Task: Implement <SLICE_ID_OR_NAME> as specified in <SLICE_DOC_PATH>.

Attach:
- Slice doc (full)
- Any schema/migration notes linked from the slice
- Open decisions: only rows tagged relevant to this slice

Goal (one sentence): <…>

Acceptance (must all be true): <paste bullets>

Explicit non-goals for this change: <paste from slice>

Coherence check: name which shared spine(s) you will use or extend; do not re-derive <e.g. pricing rules | slot targets | auth session shape>.
```

---

## 6. How to run the Build phase for efficiency and accuracy

### 6.1 Work **one slice (or one PR) at a time**

Finish **acceptance** for that slice before starting the next, unless the Plan explicitly allows **parallel** tracks with **no shared file conflict** (still: one driver per branch per `AI_PLAYBOOK`).

### 6.2 Refresh context at **slice boundaries**, not every message

At the start of a new slice:

- Re-attach the **slice doc + global guardrails + decisions excerpt**.  
- Optionally update **`HANDOFF.md`** from [`HANDOFF.template.md`](HANDOFF.template.md) when switching tools or after a long pause.

### 6.3 Use the **same PR / review question** every time

From your Plan charter (adapt if needed):

> “Which **capability** does this serve, which **shared spine** does it use or extend, and did we **avoid duplicating** domain logic?”

### 6.4 When Build should **stop and ask**

- Open decision not resolved in the slice.  
- Conflict between slice and Decisions.  
- Need to **fork** a shared pattern (requires explicit one-line rationale or ADR).

### 6.5 Optional coherence lens

Load `skills/reuse-before-build/SKILL.md` in Cursor when **designing** the slice; Build can still follow §5 prompts without loading the skill.

---

## 7. Relationship to `HANDOFF.template.md`

| Situation | Use |
|-----------|-----|
| **Plan → Build** (first time implementing a slice) | This SOP **§3 bundle + §5 prompts**; HANDOFF optional unless context is huge. |
| **Mid-slice tool switch** (Cursor ↔ Claude, session break) | **HANDOFF.md** from template: branch, done so far, next single step, tests. |
| **End of slice, start of next** | New **§5.2** task prompt + fresh attach list; trim chat if the tool does not auto-summarize. |

---

## 8. Evolving this SOP

When a project discovers a **new shared spine** or a **recurring handoff gap**, add a row to that project’s Plan guardrails table and, if the pattern is universal, propose an update to **this file** in the engineering-playbook repo.

---

*Last updated: playbook maintainer with Scott workflow (Plan in Cursor, Build in Claude family).*
