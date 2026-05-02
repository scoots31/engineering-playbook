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

**Before routing to a method:** if tech-context records `CI/CD: GitHub Actions` but no `.github/workflows/ci.yml` exists in the project root, run the CI/CD Setup below first, then return to Method A.

---

### CI/CD Setup — one-time configuration, fires when GitHub Actions declared but not yet wired

**Step 1 — Generate the workflow file**

Based on the deployment path in tech-context, generate `.github/workflows/ci.yml`. The framework writes this file entirely — the solo does not write or review YAML. The file is committed as part of setup.

**Internal — per-platform workflow content:**

**Railway:**
```yaml
name: CI/CD
on:
  push:
    branches: [main, development]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Railway
        run: |
          curl -fsSL https://railway.app/install.sh | sh
          railway up --detach
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

**Render:**
```yaml
name: CI/CD
on:
  push:
    branches: [main, development]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Render
        run: curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK }}"
```

**Cloudflare Pages/Workers:**
```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: deploy
```

**Fly.io:**
```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

**AWS App Runner:**
```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}
      - name: Deploy to App Runner
        run: aws apprunner start-deployment --service-arn ${{ secrets.APP_RUNNER_SERVICE_ARN }}
```

**Step 2 — Commit the workflow file**

Commit `.github/workflows/ci.yml` with message: `Add GitHub Actions CI/CD pipeline`.

**Step 3 — Walk the solo through the account-side setup**

This is the only part the solo does. Walk through it step by step in plain language — exactly what to click, exactly what to name each field. Do not assume prior knowledge.

**Railway:**
> "One quick thing to set up — takes about 5 minutes, no technical knowledge needed.
>
> 1. Go to railway.app and open your project
> 2. Click Settings → Tokens → New token. Give it any name and copy it.
> 3. Go to your GitHub repo → Settings → Secrets and variables → Actions → New repository secret
> 4. Name it exactly `RAILWAY_TOKEN` (capital letters, underscore) and paste the token
> 5. Click Add secret
>
> Done. From now on, every push to main runs your tests and deploys automatically."

**Render:**
> "One quick thing to set up — about 3 minutes.
>
> 1. Go to render.com and open your service
> 2. Click Settings → Deploy Hooks → Copy the hook URL
> 3. Go to your GitHub repo → Settings → Secrets and variables → Actions → New repository secret
> 4. Name it exactly `RENDER_DEPLOY_HOOK` and paste the URL
> 5. Click Add secret
>
> Done. Every push to main deploys automatically."

**Cloudflare:**
> "One quick thing to set up — about 5 minutes.
>
> 1. Go to dash.cloudflare.com → My Profile → API Tokens → Create Token
> 2. Use the 'Edit Cloudflare Workers' template, or grant Workers:Edit permission manually. Copy the token.
> 3. Go to your GitHub repo → Settings → Secrets and variables → Actions → New repository secret
> 4. Name it exactly `CLOUDFLARE_API_TOKEN` and paste the token
> 5. Click Add secret
>
> Done."

**Fly.io:**
> "One quick thing — 3 minutes.
>
> 1. In your terminal run: `fly auth token` — copy the token it outputs
> 2. Go to your GitHub repo → Settings → Secrets and variables → Actions → New repository secret
> 3. Name it exactly `FLY_API_TOKEN` and paste the token
> 4. Click Add secret
>
> Done."

**AWS App Runner:**
> "AWS needs a bit more setup — about 15 minutes. I'll walk through each step.
>
> 1. In AWS Console → IAM → Users → Create user. Attach the 'AWSAppRunnerFullAccess' permission directly.
> 2. For that user → Security credentials → Create access key. Copy both the Access Key ID and Secret Access Key.
> 3. In App Runner console → your service → Service overview → copy the Service ARN (it looks like arn:aws:apprunner:...)
> 4. Go to GitHub → your repo → Settings → Secrets and variables → Actions. Add four secrets:
>    - `AWS_ACCESS_KEY_ID` — the access key ID
>    - `AWS_SECRET_ACCESS_KEY` — the secret access key
>    - `AWS_REGION` — your AWS region (e.g. us-east-1)
>    - `APP_RUNNER_SERVICE_ARN` — the service ARN from step 3
>
> Done. This is the most setup of any platform — worth it if you're in the AWS ecosystem."

**Step 4 — Confirm and continue**

After the solo completes the account-side steps:
> "Setup complete. Every push to [base branch] now runs the test suite automatically. Every merge to main deploys. Nothing else to configure."

Proceed to Method A.

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

Tech-context should have documented the exact command. The deploy skill reads it, asks permission, then runs it directly.

**Steps:**
1. Read the deploy command from tech-context
2. State the command and ask permission:
   > "Ready to deploy. Command: `[command from tech-context]`, run from [directory]. Say go and I'll execute it."
3. On confirmation, run the command directly and capture the output
4. Log the deploy with timestamp and output

**Report:**
```
Deploy — Phase [N]
Method: Manual CLI
Command: [command]
Output: [captured output]
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
