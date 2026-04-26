# Hole #1 — Non-Visual Products Design Notes

**Status:** Design in progress — not ready to cascade. Pick up here.

**Date of conversation:** April 25, 2026

---

## The Original Problem Statement

The design sprint is screen-centric. It produces an HTML artifact (`docs/design/sprint-*.html`) that everything downstream traces to. API services, data pipelines, CLI tools, and background integrations have no equivalent path. The design sprint phase has no non-visual on-ramp.

---

## How the Thinking Evolved

### First instinct — add a "logic sprint" skill
Initial proposal: a new skill peer to design-sprint that produces a contract artifact instead of HTML screens. Rejected as the wrong level of solution — it treats the symptom (no non-visual skill) rather than the cause (the framework is locked to HTML as an artifact format).

### The real reframe — generalize the artifact, not the skill
Scott's insight: the design sprint's *purpose* is universal — make decisions explicit in a reviewable artifact before any code is written. The HTML file is just one expression of that purpose. Whether you're designing an API or a data workflow, there IS some kind of work document that gets produced. Replace "HTML screens" with "design artifact" — a document produced by the design sprint phase that can be any format the product type warrants. The framework reads it the same way at every downstream point.

**Artifact types by product:**
- Visual product → HTML screens (current)
- API → contract document: endpoints, request/response shapes, error codes, auth pattern
- Data pipeline → flow document: sources, transformations, output schema, failure modes
- CLI → command reference: commands, flags, output formats, exit codes, error messages
- Background service → behavior contract: triggers, processing logic, success/failure states, retry behavior

All AI-producible. All viewable by the solo directly or exportable (PDF, Word, etc.). All readable by the framework downstream.

### Where the framework depends on HTML specifically
Every place that needs to be generalized to "design artifact":
- `design-sprint` — explicitly produces `sprint-*.html`, rendered in a browser
- `framework-health` — file existence check looks for `sprint-*.html`
- `design-review` — reads the HTML artifact, solo views in browser, slices validated against rendered screens
- `prd-to-plan` — Screen deliverables "trace to a screen in the design sprint artifact"
- `solo-build` — design anchor traces to a sprint screen
- `solo-qa` — verifies built slice against design anchor
- `phase-test` Stage 2 + Stage 4 — derives scenarios from design artifact, walks them

### The new specialist skill question
Same way `frontend-design` handles the visual craft so the solo doesn't need to know UI design, a non-visual equivalent is needed. The solo building an API doesn't know REST conventions, error patterns, auth patterns. The specialist asks only product-level questions, derives the technical design itself, and produces the artifact. The solo approves — they don't design.

**Product-level questions the solo CAN answer:**
- What does this system need to accomplish? (already in discovery brief)
- Who or what calls it / feeds it / consumes it?
- What does each step in the to-be map need from it?

**Technical decisions the specialist makes itself:**
- REST vs other patterns, endpoint naming, error handling, auth approach
- Schema design, data types, transformation logic
- CLI structure, flag conventions, output formatting

Principle: **Framework executes, solo responds** — extended to non-visual design.

### The deeper problem Scott surfaced
For visual products, the solo verifies work by opening a browser and looking at it. No technical knowledge required. That natural verification path disappears for non-visual products. This breaks more than just design-sprint.

**Full blast radius for a non-technical solo on a non-visual product:**

**tech-context** — stack decisions, architecture choices, framework selection. A non-technical PM cannot answer "what language, what database, what deployment target." This is actually the first place it breaks — before design sprint even runs.

**solo-build verification** — for visual, the solo opens a browser. For non-visual, how does a non-technical solo verify an API endpoint was built correctly? They can't run `curl`. They can't read a JSON response.

**solo-qa** — QA for a non-visual product means making API calls, running CLI commands, triggering pipeline runs. A non-technical solo cannot do this.

**phase-test Stages 3 and 4** — data validation and scenario execution require technical execution for non-visual products. Walking a scenario isn't clicking screens — it's making API calls and validating responses.

**The unifying principle agreed upon:**
For non-visual products, the framework takes on the verification responsibility because the solo can't verify manually the way they can look at a screen. **The framework executes verification, the solo reviews results.** The AI makes the API calls, runs the tests, validates the responses — and surfaces outcomes in plain language for solo approval at the product level.

---

## What's Been Agreed

1. The fix is not a new parallel track — it's generalizing the existing framework to be artifact-format-agnostic.
2. "Design artifact" replaces "HTML screens" everywhere in the framework. Format determined by product type.
3. A new specialist skill is needed — the non-visual equivalent of `frontend-design`. Asks only product-level questions, makes all technical design decisions itself.
4. tech-context needs a non-technical solo mode for non-visual products — makes reasonable defaults, asks only product-level questions.
5. solo-build, solo-qa, and phase-test need a non-visual verification mode — framework executes, solo reviews results.
6. This is a multi-skill cascade, not a single skill addition.

---

## Open Design Questions — Need Answers Before Cascade

**1. tech-context for non-technical solo**
- What product-level questions does it ask when the product is non-visual?
- What technical decisions does it make on the solo's behalf (language, framework, deployment)?
- What defaults does it apply and how does it explain them in plain language?

**2. The new specialist skill**
- What is it named? (discussed: `logic-design`, `system-design`, `contract-design` — not decided)
- What is its step-by-step process?
- What product-level questions does it ask? (needs to be answerable by a non-technical PM)
- How does it derive technical design decisions from product intent?
- What does the artifact look like for each non-visual product type? (format, structure, what sections)
- How does the solo review and approve it?

**3. solo-build for non-visual products**
- When a slice is Logic type on a non-visual product, how does the framework verify the build?
- Does the framework execute code, make API calls, check responses automatically?
- What does the solo sign off on — a result report in plain language?

**4. solo-qa for non-visual products**
- If the solo cannot manually test, what does the QA step look like?
- Does the framework execute the tests? What evidence does it produce?
- What is the solo's role — reviewing output, not executing tests?

**5. phase-test for non-visual products**
- Stage 2 (use case creator): how do test scenarios work for APIs/pipelines — not user journeys but system behaviors?
- Stage 4 (tester): does the framework make API calls, run pipeline triggers, check outputs itself?
- Stage 6 (acceptance reviewer): same — does this still work at the product level for non-visual products?

**6. Artifact generalization mechanics**
- Does framework-health's file existence check look for any file in `docs/design/` or does it need to know the artifact type?
- How does prd-to-plan reference a non-HTML design artifact in slice anchors?
- How does solo-build's design anchor reference a section of a non-HTML document?

**7. Product type detection**
- When does the framework determine "this is a non-visual product"?
- During discovery? During tech-context? At design sprint routing?
- What's the signal — product type declared in discovery brief, or detected from to-be map?

---

## Scope Assessment

This is the largest change contemplated in the framework to date. It touches:
- `skills/design-sprint/SKILL.md` — product-type routing, artifact generalization
- New specialist skill (non-visual design) — full new SKILL.md
- `skills/tech-context/SKILL.md` — non-technical solo mode
- `skills/design-review/SKILL.md` — contract review mode
- `skills/prd-to-plan/SKILL.md` — generalize artifact anchor references
- `skills/solo-build/SKILL.md` — non-visual verification mode
- `skills/solo-qa/SKILL.md` — non-visual QA mode
- `skills/phase-test/SKILL.md` — Stages 2, 4 non-visual mode
- `skills/framework-health/SKILL.md` — generalize file existence check
- Full communications cascade (skills-reference, process-map, blog, potentially deck slides)

Recommended approach: design each skill change separately before cascading. Start with the new specialist skill and tech-context (the entry points), then work downstream.

---

## Resume Prompt

> "Resuming Hole #1 — non-visual products. Design conversation is documented in `docs/hole-1-non-visual-products.md` in the engineering-playbook. We've agreed on the principles (artifact generalization, new non-visual design specialist, framework-executes-verification). The open design questions are listed. Start by designing the new specialist skill — what it asks, how it works, what it produces — and the tech-context non-technical solo mode. Then work downstream from there."
