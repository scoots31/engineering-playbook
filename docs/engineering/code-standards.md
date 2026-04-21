# Code Standards
**Scope:** All builds in the Solo Builder Framework
**Status:** Standing reference — always in play, never optional
**Referenced by:** `code-review-and-quality`, `solo-build`, `solo-qa`

---

## The Core Principle

Code is read more than it's written. The next person to touch a slice — or the AI in the next session — should be able to understand it without asking questions. Write for that reader.

---

## Standards

### 1. One Pattern Per Process

If there's already a way to do something in this codebase, use it. Don't introduce a second approach for the same problem. Two ways to fetch data, two component structures for the same pattern, two file naming conventions — all of these create maintenance debt. 

**Check:** before implementing something, look for how it's already done. Match it.

---

### 2. No Hardcoded Values That Belong Elsewhere

Data that should come from the mock layer comes from the mock layer. Config that should come from environment variables comes from environment variables. Display strings that will eventually come from an API do not live inline in the component.

**Check:** every literal value in the code should be explainable. "This is a label" is fine. "This is a number that will eventually come from the API" is not — it goes in mock data.

---

### 3. Built to Expand

The next slice should be able to add to this without restructuring it. Don't write code that works for exactly one use case in a way that makes the second use case a rewrite.

**Check:** if the next slice in the journey needs to extend what this slice built, can it do so by adding rather than changing?

---

### 4. No Dead Code

No commented-out experiments. No unused imports. No functions that exist but are never called. No console.log left from debugging. Code that isn't running has no place in the codebase — it creates noise and misleads the next reader.

**Check:** every line of code should be either running or deleted.

---

### 5. Scope Discipline

Only what the slice requires. No extra fields added "while we're here." No adjacent improvements. No speculative features. If something is noticed that's out of scope, surface it — don't build it.

**Check:** does every line of code in this commit trace back to the slice's done criteria or design anchor?

---

### 6. Functions and Components Have Purpose Comments

Any function or component that isn't completely obvious from its name gets a one-line comment explaining what it does and why. Not what the code says — why it exists.

```typescript
// Normalizes slot target from the mock layer before display.
// API will return raw float; display format is one decimal place.
function formatSlotTarget(value: number): string {
  return value.toFixed(1);
}
```

**Check:** could someone new to this file understand what each function does without reading its implementation?

---

### 7. Complex Logic Gets Inline Explanation

If a piece of logic required thinking to write, it requires a comment to explain. This includes: non-obvious conditionals, data transformations, anything that handles edge cases, anything that will look wrong to a reader who doesn't know why it was written that way.

**Check:** is there any logic that would make a reader pause and wonder why?

---

### 8. Known Tradeoffs Are Named

If a decision was made that trades off one thing for another — correctness for speed, completeness for Phase 1 scope, ideal architecture for practical delivery — name it in a comment. Don't leave the next reader guessing whether it was intentional or a mistake.

```typescript
// Phase 1: context switch is display-only. Real-time state management 
// deferred to SL-014. Toggle is present but non-functional.
```

---

## Stack-Specific Standards

Stack-specific standards are defined in `docs/tech-context.md` for the active project. Code standards apply universally; tech context adds the stack-specific layer on top.

**Examples of what tech context adds:**
- TypeScript: strict mode, no `any` types
- ESLint: Airbnb ruleset, enforced in CI
- RTK Query: all API calls through the base client, no raw `fetch`
- Component library: Element components over custom implementations where available

When in doubt: read `docs/tech-context.md`.

---

## What "Meets Standards" Means

A slice meets code standards when:

| Check | Criteria |
|-------|----------|
| Pattern | Uses existing patterns — no new approaches for existing problems |
| Data | All values that should come from mock/config/API do — nothing hardcoded that shouldn't be |
| Expandability | Next slice can extend this without restructuring |
| Clean | No dead code, no debug leftovers, no unused imports |
| Scoped | Nothing built beyond the slice's done criteria |
| Documented | Functions have purpose comments, complex logic is explained, tradeoffs named |
| Stack | Meets the standards in docs/tech-context.md |

All seven. Not most. All.
