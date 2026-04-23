---
name: security-patch
description: Address a security vulnerability in a production system — understand the exposure, verify the codebase is actually affected, apply the minimal fix, confirm it's closed, deploy urgently. Speed and correctness are equally required.
---

# Security Patch

*Speed matters. Correctness matters more.*

**Core question:** "What's the exposure, what closes it, and how fast can we ship a verified fix?"

Security patches have different urgency than other support work. They also carry higher risk — a patch that doesn't fully close the vulnerability is worse than a known-open one, because it creates false confidence. Never trade verification for speed.

---

## Step 1 — Understand the Vulnerability

Before touching anything, understand what you're dealing with:

- What is the vulnerability? (CVE ID, description, attack vector)
- What's the severity? (Critical / High / Medium / Low)
- Is this codebase actually exposed? Many CVEs affect packages in ways a specific project doesn't use
- What's the attack surface — who can trigger this, under what conditions?
- Is there a known exploit in the wild?

State the exposure clearly:
> "Vulnerability: [what]. This codebase is exposed because [specific usage]. Severity: [level]. Attack vector: [who/how]."

If the codebase is not actually exposed — the vulnerable code path isn't used — document that explicitly and close it. Don't patch what isn't exposed.

---

## Step 2 — Identify the Fix

**Package vulnerability** — a dependency has the CVE:
- Is there a patched version available?
- Does the patched version have breaking changes?
- If no patch exists: is there a workaround, or can the vulnerable feature be disabled?

**Code vulnerability** — the application code itself is the issue:
- What's the exact exploit path?
- What's the minimal change that closes it?
- Is the fix in input validation, auth, output encoding, or logic?

If no clean fix exists and the exposure is critical, raise it immediately rather than shipping a partial fix.

---

## Step 3 — Apply the Fix

Minimal footprint — same principle as bug-fix, higher stakes.

- Fix only what closes the vulnerability
- Do not refactor alongside the patch
- Do not bundle unrelated changes

Commit messages:
- Package fix: `deps: security patch [package] [old] → [new] — [CVE ID]`
- Code fix: `fix: close [vulnerability type] in [location] — [CVE ID or brief description]`

---

## Step 4 — Verify the Fix Closes It

Non-negotiable. A patch that doesn't close the vulnerability is worse than the original exposure.

- Reproduce the attack vector before the patch (if safe to do so in a non-production environment)
- Confirm the attack vector is closed after the patch
- Audit the codebase for the same vulnerability pattern elsewhere — don't fix one instance and miss three others

---

## Step 5 — Deploy Urgently

Security patches skip the normal deploy queue. Deploy as soon as the fix is verified.

- Deploy to production immediately — do not wait for a scheduled release
- Verify in production that the vulnerability is closed
- Document: CVE/issue ID, what was fixed, when deployed, severity, attack surface

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Patching without confirming exposure | Wasted effort, or wrong scope | Confirm the codebase actually uses the vulnerable path |
| "Close enough" verification | False confidence, still open | Reproduce the attack vector, confirm it's closed |
| Bundling with other changes | Harder to isolate regressions | Patch alone |
| Delaying because the fix is complex | Every hour is active exposure | Ship minimal fix now, clean up later |
| Fixing one instance, missing others | Same vulnerability elsewhere | Audit the pattern across the full codebase |
| No post-deploy verification | Patch may not have taken effect | Verify in production, not just locally |
