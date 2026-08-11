# soloframework.app — status

This folder is a **standalone copy** of `docs/communications/`, created 2026-08-10 so the
new splash-page approach could be built without touching the existing, already-shared
`sbf-framework-docs.pages.dev` site (Scott gave that link to a group he doesn't want seeing
this new direction yet). `docs/communications/` was reverted back to exactly what it was
before this work started — nothing there changed.

**Location:** `/Users/scottheinemeier/Developer/engineering-playbook/docs/soloframework/`

This folder is **not yet committed to git** and **not yet deployed anywhere**. It only
exists on this machine right now.

## What's in here, new vs. carried over

New files, built this session:
- `index.html` — the new splash/landing page. Hero line "Team discipline. Without the
  team." Sections: what it is, why it exists, how it runs inside Claude Code/Cursor
  (explicitly addressed — this was the main gap identified), how it helps you build,
  who it's for (newcomer vs. engineer, with a 5-step "what it looks like" journey for
  newcomers), a "why it's free" banner, and a closing CTA.
- `why-its-free.html` — its own page, linked from the nav and the splash page. Covers
  the real reason: removing jargon/cost as a barrier so anyone can build the confidence
  that comes from making something real.
- `solo-companion.html` — the Solo Companion download page (Mac/Windows one-line
  install commands with copy buttons), ported over from an earlier Claude-artifact
  draft into a real hosted page.
- `install-mac.sh`, `install-windows.ps1` — copied in from the Solo Companion repo so
  the download commands on `solo-companion.html` actually resolve once this is live
  (they reference `https://soloframework.app/install-*`).

Carried over unchanged from `docs/communications/`:
- `documentation.html` — the old "Communications" doc index (was `index.html` before
  the rename), now linked from the new splash page's nav as "Documentation."
- `install.html` — the Framework install page (clone + paste-into-Claude/Cursor steps),
  built earlier this session.
- Everything else (decks, guides, FAQ, skills reference, framework-architecture.html,
  etc.) — untouched copies.

Six files have one link updated (`index.html` → `documentation.html`, since the old
index moved): `blog.html`, `guide-qa.html`, `guide-discover.html`,
`backlog-status-reference.html`, `guide-plan.html`, and `install.html`.

## What's still open

1. **Scott is reviewing the splash page copy/design** before deciding to proceed —
   nothing here should be treated as final.
2. **No image yet.** Two photorealistic prompts were drafted (not generated) for a
   hero-style image — one built around architectural scaffolding, one around a series
   of archways/thresholds receding into light — both explicitly avoiding the "person
   alone at a laptop" cliché per Scott's direction. Neither has been generated or
   placed on the page yet.
3. **No Cloudflare Pages project exists for this folder yet.** It needs its own,
   separate from `sbf-framework-docs` (which stays pointed at `docs/communications/`
   and must not change). Domain `soloframework.app` is Scott's, not yet connected to
   anything.
4. **Nothing here is committed or pushed.** When it's ready: `git add` this folder,
   commit, push, create the new Pages project, deploy, then connect the domain.

## Reference — everything else committed and shipped this session

For context, separate from this in-progress splash work, the following were already
committed, pushed, and (where applicable) deployed earlier in this session:

- **Solo Companion** (`~/Developer/Solo Companion`) — mempalace and cloud-push removed,
  cross-platform file-open fix, Mac/Windows one-command installers, first-run setup
  flow replacing the hardcoded default folder. Commits `f546de2`, `22bfc07`, `57509f7`.
- **engineering-playbook** — projects registry split out of the playbook folder into a
  separate `Development Files` folder (created automatically on install), Ren's skill
  file untracked and gitignored (personal, not shipped), the Framework Architecture page
  added with Ren's node removed, and the Install page added to `docs/communications/`
  (the live, shared site). Commits `0df480f` through `caeb328`, pushed and deployed to
  `sbf-framework-docs.pages.dev`.
- Stray uncommitted files from a previous session were resolved: a duplicate
  architecture-page file deleted, and a misplaced plant-ID reference document (`ID.docx`)
  found and moved to `~/Developer/garden-planner/`.
