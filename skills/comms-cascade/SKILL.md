---
name: comms-cascade
description: Sub-agent skill. Updates all framework communications docs when a version ships. Invoked by the curator with a structured brief. Writes, commits, pushes, and deploys to Cloudflare in one pass.
activation: Sub-agent — invoked via Agent tool by framework-curator or Ren. Never invoked directly by the solo.
---

# Comms Cascade

You are a sub-agent executing a framework communications update. You have been given a brief describing what shipped. Your job is to update every relevant communications doc, commit, push to GitHub, and deploy to Cloudflare. You execute — you do not propose or ask for approval.

---

## Input

You receive a brief in this format:

```
Version: v[X.Y.Z]
Date: [YYYY-MM-DD]
Summary: [one paragraph — what this version delivers, plain language]
Skills affected: [comma-separated list of skill names, or "none"]
Watchfor items: [specific things solos should watch for, or "none"]
Guide sections affected: [which guides are relevant, or "none"]
```

---

## Doc Inventory — Review Every File

Read each file before deciding whether it needs an update. Update only what is relevant to this version. Do not add filler entries.

### Always update

| File | What to add |
|---|---|
| `CHANGELOG.md` | New `## v[X.Y.Z] — [DATE] — RECOMMENDED` entry with summary and file list |
| `docs/communications/blog.html` | New blog entry at the top of the entries section |

### Update if skills were affected

| File | What to update |
|---|---|
| `docs/communications/skills-reference.html` | Update the card(s) for affected skills — description, version badge if shown |

### Update if watchfor items were provided

| File | What to check and add |
|---|---|
| `docs/communications/guide-build.html` | Add to the "Watch For" section if build-relevant |
| `docs/communications/guide-design-sprint.html` | Add if design-sprint-relevant |
| `docs/communications/guide-discover.html` | Add if discover-relevant |
| `docs/communications/guide-plan.html` | Add if plan-relevant |
| `docs/communications/guide-deploy.html` | Add if deploy-relevant |
| `docs/communications/guide-phase-test.html` | Add if phase-test-relevant |
| `docs/communications/guide-qa.html` | Add if QA-relevant |
| `docs/communications/guide-data-review.html` | Add if data-relevant |

### Update if process flow changed

| File | What to update |
|---|---|
| `docs/communications/process-map.html` | Update step descriptions or flow if process changed |

### Review but rarely change

| File | When to update |
|---|---|
| `docs/communications/getting-started.html` | Only if setup or onboarding behavior changed |
| `docs/communications/faq.html` | Only if this version answers a common question |
| `docs/communications/index.html` | Only if a new page was added or a major nav change |
| `docs/communications/backlog-status-reference.html` | Only if status chain changed |

### Never touch

| File | Reason |
|---|---|
| `docs/communications/deck-business.html` | Manually maintained — stakeholder deck |
| `docs/communications/deck-solo.html` | Manually maintained — solo deck |
| `docs/communications/enterprise-integration.html` | Unlinked reference page |
| `docs/communications/robots.txt` | Static |
| `docs/communications/generate_communications_decks.py` | Script — not a doc |

---

## Blog Entry Format

Add at the top of the blog entries section in `blog.html`. Match the existing style exactly — read 2-3 recent entries first.

```html
<article class="blog-entry">
  <div class="entry-meta">
    <span class="entry-date">[Month D, YYYY]</span>
    <span class="entry-version">v[X.Y.Z]</span>
  </div>
  <h2>[Title — plain language, what this delivers]</h2>
  <p>[One paragraph. What changed, why it matters, what solos will notice. No jargon.]</p>
  <p>[Optional second paragraph if the change is significant enough to warrant it.]</p>
</article>
```

---

## CHANGELOG Entry Format

Add at the top of `CHANGELOG.md`, above the previous latest version. Match existing format:

```markdown
## v[X.Y.Z] — [YYYY-MM-DD] — RECOMMENDED

**[Title]**

[One paragraph summary — same as blog, slightly more technical]

### What changed
- [file or skill]: [what specifically changed]
- [file or skill]: [what specifically changed]

### Action required
[None for existing projects / or specific action if required]

---
```

---

## Execution Order

1. Read the brief
2. Read CHANGELOG.md — understand recent version history
3. Read blog.html — understand recent entry style
4. Read each file in the "Always update" list — write updates
5. Read each file in the conditional lists that applies — write updates where relevant
6. Verify: read back each file you updated and confirm the addition looks correct and matches surrounding style
7. Commit all changes:
   ```
   git -C ~/Developer/engineering-playbook add -A
   git -C ~/Developer/engineering-playbook commit -m "v[X.Y.Z] — comms cascade"
   ```
8. Push:
   ```
   git -C ~/Developer/engineering-playbook push
   ```
9. Deploy to Cloudflare:
   Read the token from `~/.claude/projects/-Users-scottheinemeier-Apps/memory/reference_cloudflare_deploy.md`, then run:
   ```
   cd ~/Developer/engineering-playbook/docs/communications
   export CLOUDFLARE_API_TOKEN="[token from reference file]"
   wrangler pages deploy . --project-name sbf-framework-docs
   ```
10. Report back to the curator: which files were updated, commit hash, deploy confirmed.

---

## Quality Rules

- Read before writing — never add to a file without reading it first
- Match style exactly — read adjacent entries and match formatting, tone, and length
- No filler — if a section isn't relevant to this version, skip it
- Plain language in blog — no skill names, no internal jargon, write for a solo builder not a developer
- Verify after writing — read back each updated section before committing
