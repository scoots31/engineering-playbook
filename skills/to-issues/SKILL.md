---
name: to-issues
description: Converts an approved prd-to-plan implementation plan into GitHub issues in dependency order. Each issue is self-contained — design reference, process anchor, done criteria, and dependencies included. Invoked after the solo approves the plan from prd-to-plan.
---

# To Issues

*The plan is approved. Now make it executable.*

**Core question:** "Given the approved phase plan, what is the exact set of GitHub issues that needs to be created, in what order, with what content?"

---

## When to Run

Immediately after the solo approves the phased plan from `prd-to-plan`. The plan is the source of truth — this skill converts it into trackable, self-contained GitHub issues.

---

## Process

### Step 1 — Confirm Prerequisites

Before creating any issues, confirm:
- The implementation plan is approved (not still under discussion)
- A GitHub repo exists and `gh` CLI is authenticated
- The backlog has process anchors on every Ready slice

If `gh` is not authenticated: `gh auth login` and follow the prompts.

---

### Step 2 — Determine Issue Structure

Each slice in the plan becomes one GitHub issue. The issue must be self-contained — a builder should be able to start the slice from the issue alone without reading any other document.

**Required fields per issue:**

```
Title: [SL-XXX] [Slice Name]

## What this builds
[One sentence description from the backlog]

## Design reference
[Screen file + specific element]
e.g. docs/design/sprint-v1.html → Player Search input + results list

## Process anchor
[to-be map step this slice implements]
e.g. to-be-lookup.md → Step 1: user searches → main path

## Data anchor
[Mock data fields this slice reads]
e.g. data/mock/players.json → id, name, position, team

## Done looks like
- [Acceptance criterion 1]
- [Acceptance criterion 2]
- [Acceptance criterion 3]

## Depends on
[SL-XXX issue link / none]

## Notes
[Any relevant constraints, spike results, or decisions that informed this slice]
```

---

### Step 3 — Create in Dependency Order

Create issues in dependency order — blockers first. If SL-003 depends on SL-001, SL-001 is created first so its issue number can be referenced in SL-003's "Depends on" field.

Use the `gh` CLI:

```bash
gh issue create \
  --title "[SL-001] Player Search" \
  --body "$(cat <<'EOF'
## What this builds
Search input that queries the player database and returns a filtered results list.

## Design reference
docs/design/sprint-v1.html → Player Search input + results list

## Process anchor
to-be-lookup.md → Step 1: user searches → main path

## Data anchor
data/mock/players.json → id, name, position, team, status

## Done looks like
- Search returns matching players on keystroke (debounced)
- Empty state displayed when no results found
- No console errors on valid and invalid input

## Depends on
None
EOF
)" \
  --label "Phase 1" \
  --label "Ready"
```

After creation, note the issue number returned. Reference it in dependent issues.

---

### Step 4 — Group by Phase

Apply labels to make phase grouping visible:
- `Phase 1`, `Phase 2`, etc. — from the plan
- `Ready` — slices that are Ready to build
- `Infrastructure` — infrastructure slices
- `Blocked` — slices waiting on a dependency

Create labels if they don't exist:
```bash
gh label create "Phase 1" --color "0075ca"
gh label create "Ready" --color "0e8a16"
gh label create "Infrastructure" --color "e4e669"
```

---

### Step 5 — Confirm and Report

After all issues are created, report:

```
Issues created — Phase 1

SL-001 Player Search → #12 (Ready)
SL-002 Player Results Card → #13 (Ready, depends on #12)
SL-003 Search Filters → #14 (Ready, depends on #12)
SL-004 API Integration Layer → #11 (Infrastructure, no dependencies — first in queue)

Phase 2 slices: SL-005 through SL-009 → created, labeled Phase 2

View all: gh issue list --label "Phase 1"
```

---

## What To Issues Does Not Do

- Does not modify the plan — it converts, not designs
- Does not create issues for Deferred slices — only Ready slices
- Does not set assignees or milestones — the solo handles that
- Does not create issues for infrastructure slices not yet in the backlog — those come from tech-context and must be added to the backlog first

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Creating all issues at once without dependency order | Dependent issue references don't exist yet | Create blockers first, note issue numbers, reference in dependents |
| Vague issue titles | Builder can't identify the slice at a glance | Always: `[SL-XXX] [Slice Name]` |
| Omitting the process anchor | Disconnects the issue from the agreed process | Process anchor is required — copy from the backlog slice record |
| Creating issues before plan is approved | Issues get created for a plan that may change | Confirm explicit solo approval before running |
