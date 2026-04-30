---
name: onboard
description: Brings an existing project into the Solo Builder Framework. Reads the project directory, semantically matches content to the framework gate artifacts, synthesizes matched content into framework-format files with solo confirmation, surfaces gaps as targeted discussion prompts, and loops until the project is fully represented in the framework docs and placed at the correct starting phase.
---

# Onboard

*The framework meets you where you are.*

**Core question:** "What has already been decided and built — and what's the right the framework starting point from here?"

Onboard is for projects that started outside the framework. Discovery was done in conversation. Planning happened in notes. Architecture decisions live in a README. The work is real — it just isn't in framework format. Onboard translates it without redoing it.

---

## When to Run

Invoked when:
- The solo has prior work on a project and wants to bring it into the framework
- Opening message signals existing work: "I have prior work on [project]", "I want to
  pick up [project] using the framework", "I've been working on [project] outside the framework"

`start` routes here when the opening message signals existing work with no the framework context
found. Also invokable directly via `/onboard`.

**Does not fire for new projects** — those go through `start` → `brainstorm` or `discover`.

---

## Step 1 — Get the Project Location

Ask two things only:

1. **Where does the project live?** — absolute path to the project directory
2. **Where do you think you are?** — optional; the solo's sense of how far along they
   are (e.g., "we've done discovery and some planning"). The skill verifies — this is a
   hint, not a constraint.

---

## Step 2 — Read the Project

Scan the project directory. Build a content inventory.

**Read first (highest signal):**
- Root-level markdown files (README.md, NOTES.md, planning docs, etc.)
- Any `docs/` directory contents
- Files with signal words in the name: plan, brief, discovery, design, spec, backlog,
  tasks, notes, ideas, research, scope, requirements, architecture

**Skip:**
- Code files (*.py, *.js, *.ts, *.swift, etc.) — unless no docs exist at all
- Build artifacts, node_modules, .git, dist/, .venv/, __pycache__
- Binary files, images, lock files

For each file read: note filename, rough content type, key topics covered.

---

## Step 3 — Map to the framework Gate Artifacts

For each framework gate file, search the inventory for matching content. Matching is
semantic — content in `ff-eval-notes.md` may be a discovery brief; a `stack.md` may
be tech context. Name doesn't matter. Content does.

| Framework Gate File | Look for |
|---|---|
| `docs/discovery-brief.md` | Use cases, user stories, problem statement, who uses it and why |
| `docs/process/as-is-[project-slug].md` | Current (manual/existing) process description |
| `docs/process/to-be-[project-slug].md` | Target process — the agreed flow the product enables |
| `docs/tech-context.md` | Stack, language, framework, architecture, deployment target |
| `docs/design/sprint-*.html` | Visual design artifact, screens, UI structure |
| `docs/design/deferred-decisions.md` | Scope decisions, what's in/out, deferred items |
| `docs/backlog.md` | Slices, tasks, features, issues — anything that looks like a build list |

Content may be spread across multiple files — synthesize it.

---

## Step 4 — Show Mapping and Confirm

For each match found, show the solo before writing.

> "I found content that maps to your discovery brief across [file-a.md] and [README.md].
> Here's what I'd synthesize:
>
> [preview of synthesized discovery-brief.md content]
>
> Does this capture it, or is something off?"

Solo responses:
- **Confirm** → write the file
- **Edit** → adjust and write
- **Reject** → treat as gap, move on

One mapping at a time. Never write a the framework file without confirmation.

---

## Step 5 — Surface Gaps as Discussion Prompts

After the mapping pass, list what wasn't found. Format each gap as the actual questions
the solo needs to answer — not just a file name.

```
What's missing — let's fill these in:

Tech context:
  - What language and framework is this built in?
  - Where does it deploy? (local, Railway, Vercel, other?)
  - Any external APIs or data sources this relies on?

Process maps:
  - What's the current manual process this replaces, if any?
  - Walk me through the target flow — what does the user do, step by step?
```

Work through gaps in conversation. As each is answered, synthesize into the framework file
and confirm before writing.

---

## Step 6 — Classify Remaining Gaps

After the discussion pass, classify any remaining gaps:

**Undocumented work** — the solo knows the answer; it just hasn't been stated yet.
Ask one more time, then fill it in.

**Work not done yet** — this phase genuinely hasn't happened. This is the starting
point. Do not synthesize a file that doesn't exist in any form.

> "Design sprint hasn't happened yet — that's where you're starting. Everything
> before it is now captured."

---

## Step 7 — Initialize Continuity Docs

Once gate files are confirmed, initialize continuity:

- Create `docs/continuity/` if it doesn't exist
- Write `docs/continuity/current-phase.md` — set to the identified starting phase
- Write `docs/continuity/handoff.md` — current state, what was onboarded, where to start
- Write a seed `docs/continuity/decisions.md` entry for any key decisions surfaced
  during the mapping pass

Do not create empty shells for every continuity file — only what's needed to orient
the first session.

---

## Step 8 — Companion Compatibility Pass

Before exiting, verify the project will sync cleanly with the Solo Companion. Four checks,
in order. Do not skip any — a project that fails these will appear in the companion with
missing or empty content.

**Check 1 — projects.md registration**
Read `~/Developer/engineering-playbook/projects.md`. If the project is not in the table,
add a row: `| [Project Name] | [absolute path to project root] |`
Show the addition to the solo and confirm before writing.

**Check 2 — backlog.md section headers**
Read `docs/backlog.md`. It must contain all three section headers exactly as written:
- `## Phase Records`
- `## Deliverable Records`
- `## Slice Detail`

If any are missing: add the missing skeleton sections. Do not populate them — the framework
fills them in subsequent sessions. The companion silently skips content sync if these headers
are absent.

**Check 3 — handoff.md with Open right now**
Read `docs/continuity/handoff.md`. It must exist and contain an `## Open right now` section.
This section drives the companion's Needs Attention dashboard.

If handoff.md doesn't exist: flag it — Step 7 should have created it. Create it now.
If the section is missing: append it with an empty placeholder.

**Check 4 — Review URL field on slice records**
Scan every slice record in `docs/backlog.md`. Each must have a `Review URL:` field.
If any are missing: add `Review URL: None` to each affected slice. Do not guess URLs —
`None` is correct until the slice is built and a real URL is known.

---

After all four checks pass:

> "Companion compatibility: clean. This project will sync on the next Solo Companion run."

If a check could not be completed, state which one and why. Do not exit until all four
are either passing or explicitly acknowledged as blocked.

---

## Step 9 — Exit with Orientation

> "Onboarding complete. Here's where things stand:
>
> **Created:** discovery-brief.md · tech-context.md · backlog.md (12 slices)
> **Starting phase:** Design Review — backlog needs a round of review before slices
> reach Ready
> **First move:** review the designs and refine slices until they're ready to build
>
> Continuity docs initialized. The framework will run clean from here."

One clear statement. Then stop.

---

## The Loop

Onboard continues until:
- All gate files up to the starting phase exist and are confirmed, OR
- All remaining gaps are classified as "work not done yet" (starting phase identified)

If the solo can't answer a gap question, classify it as starting phase and move on.
The loop does not block indefinitely.

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Writing the framework files without confirmation | Solo loses trust in what was produced | Show preview, confirm, then write |
| Literal filename matching | Misses content in non-standard file names | Read content, match semantically |
| Reading all code files | Token-expensive, low signal | Docs and notes first; code only if no docs exist |
| Treating every gap as a blocker | Onboard never completes | Classify: undocumented (ask) vs. not done yet (starting phase) |
| Presenting all mappings at once | Overwhelming, hard to verify | One mapping at a time, confirm each |
| Redoing phases that are done | Wastes existing work | Translate into the framework format, don't redo |
| Skipping continuity initialization | First real session starts blind | Always write current-phase.md and handoff.md before exiting |
