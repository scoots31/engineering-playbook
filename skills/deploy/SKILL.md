---
name: deploy
description: Deploy orchestrator for the Solo Builder Framework. Reads docs/tech-context.md to determine the deploy method — CI/CD triggered, MCP-triggered, manual, or other. Does not assume a specific platform. Handles both test environment deploy (confirming phase-test environment readiness) and prod deploy (after phase test gate opens). Invoked explicitly after phase test gate is OPEN.
---

# Deploy

*The deploy method lives in tech-context. This skill executes it.*

**Core question:** "Given how this project is configured to deploy, is the phase test gate open — and what's the exact sequence to get this phase to production?"

The deploy skill does not know in advance what the deploy target is. It reads `docs/tech-context.md` to find out, then follows the method defined there. A new project with a different deployment target just needs a properly configured tech-context — the skill adapts.

---

## Two Deploy Moments in the Framework

### Deploy Moment 1 — Test Environment (before phase test)

Phase test Stage 1 (Environment Readiness) requires all Done slices accessible in a test environment. How they got there depends on the tech stack — CI/CD on merge to `development`, a manual trigger, a preview environment. The deploy skill confirms this happened correctly.

This is a **confirmation check**, not an action the deploy skill initiates. If the test environment isn't live, the deploy skill identifies what's missing and how to fix it based on the tech-context deploy configuration.

### Deploy Moment 2 — Production (after phase test gate opens)

The explicit deploy. Phase test gate is OPEN, phase completion record is confirmed, code is merged and ready. The deploy skill executes the production deploy using whatever method tech-context defines.

---

## Step 1 — Read Tech Context

Before anything else, read `docs/tech-context.md`. Extract:

**Deployment target** — where does this live when deployed?
- Examples: Spectrum/C7 (Aurora), Railway, Vercel, Fly.io, AWS, internal server, other

**CI/CD system** — is deploy automated or manual?
- Examples: GitHub Actions, CircleCI, manual CLI, MCP tool, other

**Branch-to-environment mapping** — which branch deploys where?
- Examples: `development` → non-prod · `main` or `release` → prod

**Deploy trigger** — what initiates the deploy?
- Examples: merge to branch (automatic), manual CLI command, MCP tool invocation, push button in dashboard

**Verification method** — how do you confirm the deploy succeeded?
- Examples: CI status check, environment URL accessible, deployment dashboard, health endpoint

If any of these are not defined in tech-context, stop. Ask the solo to add the missing deploy configuration to `docs/tech-context.md` before proceeding.

> "The deploy target isn't defined yet. Before we can deploy, we need to know: where does this live, and how is it deployed? Add this to the Deployment section of the tech setup doc and we'll continue."

---

## Step 2 — Confirm Gate Status

Read `docs/backlog.md`. Find the phase completion record for the phase being deployed.

Confirm:
- Status shows `✅ Phase [N] Complete — Tested and ready to deploy`
- Phase test gate is listed as OPEN
- Phase test report referenced in the record exists

If the gate is not OPEN: stop.
> "Phase [N] gate is not open. Phase testing must pass before deploying. Should we run that now?"

If the phase completion record doesn't exist: stop.
> "No phase completion record found for Phase [N]. Phase test must complete successfully before deploy."

---

## Step 3 — Confirm Code Is Ready

Read the branching model from tech-context. Verify:

- All Done slices for this phase have been merged to the appropriate base branch
- No open feature branches for this phase remain unmerged
- The base branch is in the state expected for a prod deploy

If any slice branches are still open: surface them specifically.
> "SL-007 (Player Overview Card) feature branch hasn't been merged yet. Merge it to [base branch] before proceeding with the prod deploy."

---

## Step 4 — Execute the Deploy

Route to the correct deploy method based on what tech-context defined.

---

### Method A — CI/CD Triggered by Merge

**When:** GitHub Actions, CircleCI, or similar — deploy triggers automatically when code is merged to the production branch.

The deploy may already be in progress if the merge to `main`/`release` happened when the slice was marked Done. If so, confirm CI status rather than triggering a new deploy.

**Steps:**
1. Confirm the production branch (`main`, `release`, or whatever tech-context specifies) has the full phase merged in
2. If not yet merged: merge the base branch (`development` or similar) into the production branch per the branching model
3. Confirm CI/CD pipeline triggered — check the CI system defined in tech-context
4. Monitor until pipeline completes
5. Verify deployment using the verification method from tech-context

**Report:**
```
Deploy — Phase [N]
Method: GitHub Actions on merge to main
Branch: development → main merged
Pipeline: [status — running / passed / failed]
Environment: [URL or confirmation accessible]
Status: DEPLOYED ✅ / FAILED ❌
```

---

### Method B — MCP Tool Triggered

**When:** A connected MCP tool (Railway, Vercel, or other) can trigger the deploy directly.

**Steps:**
1. Confirm the MCP tool is connected and accessible
2. Identify the project and environment in the tool (from tech-context configuration notes)
3. Trigger the deploy via the MCP tool
4. Monitor deployment status until complete
5. Verify using the method defined in tech-context

**Report:**
```
Deploy — Phase [N]
Method: [Tool name] MCP
Project: [project name]
Environment: [target environment]
Triggered: [timestamp]
Status: DEPLOYED ✅ / FAILED ❌
```

---

### Method C — Manual CLI

**When:** Deploy requires running a specific command — a CLI tool, a script, a direct push.

Tech-context should have documented the exact command. The deploy skill surfaces it and confirms the solo has executed it.

**Steps:**
1. Read the deploy command from tech-context
2. Present it to the solo:
   > "Deploy command for this project: `[command from tech-context]`
   > Run this from [directory], confirm it completes successfully, then confirm here."
3. Wait for solo confirmation
4. Log the deploy with timestamp and solo confirmation

**Report:**
```
Deploy — Phase [N]
Method: Manual CLI
Command: [command]
Confirmed by: Solo — [timestamp]
Status: DEPLOYED ✅
```

---

### Method D — Not Yet Defined

**When:** Tech-context exists but doesn't have a deploy configuration.

The solo hasn't defined how this project deploys yet. Surface the gap and ask the right questions to fill it in — using the same approach as tech-context's Path 2 (general solo questions):

1. "Where does this live when it's deployed — what platform or environment?"
2. "Is the deploy automated (CI/CD triggers on git events) or manual (you run a command or click something)?"
3. "What branch or action triggers the production deploy?"
4. "How do you verify the deploy succeeded?"

Once answered, update `docs/tech-context.md` with the deploy configuration, then execute using the appropriate method above.

---

## Step 5 — Verify Deployment

After the deploy completes, confirm the phase is actually live — not just that the deploy pipeline said it succeeded.

**Verification depends on tech-context:**
- URL accessible and loading correctly
- Health endpoint returning expected response
- Module visible in the target environment (e.g., Aurora module registering)
- CI dashboard showing green
- Whatever the project's verification method is

If verification fails after a successful deploy pipeline: this is a deployment issue, not a code issue. The phase test confirmed the code is correct. Surface the environment-specific failure and route appropriately — don't reopen QA.

---

## Step 6 — Update the Phase Completion Record

When deploy is confirmed:

Add to the phase completion record in `docs/backlog.md`:

```
**Deployed:** [YYYY-MM-DD]
**Deploy method:** [CI/CD / Railway MCP / Manual / other]
**Environment:** [prod URL or environment name]
**Verified:** [how verified]
```

The phase completion record now reads: Complete → Tested → Deployed. The full lifecycle for that phase is documented in one place.

---

## What Deploy Does Not Do

- Does not determine the deploy method — that's tech-context's job
- Does not re-run QA or phase test — the gate is already confirmed
- Does not merge feature branches — that happened at solo-qa Done
- Does not assume any specific platform — it reads and routes
- Does not proceed if the phase test gate is not OPEN

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Deploying without confirming gate is OPEN | Shipping untested code | Always confirm phase completion record shows OPEN before deploying |
| Assuming Railway or any specific platform | Breaks for any other stack | Read tech-context, route to the correct method |
| Verifying deploy by pipeline status alone | Pipeline can pass with a broken deploy | Always verify the environment is actually live |
| Reopening QA when deploy verification fails | QA already confirmed the code | Deploy failures are environment issues — route separately |
| Deploying without all phase branches merged | Partial phase ships | Confirm all Done slice branches are merged before triggering |
