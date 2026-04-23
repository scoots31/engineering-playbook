---
name: research-spike
description: A timeboxed investigation into a specific unknown that's blocking a decision in the current phase. Can be invoked from any phase — Brainstorm, Discover, Design Sprint, Plan, or Build. Not open-ended research. A question with a deadline. Returns a clear answer and routes control back to the phase that called it.
---

# Research Spike

*A question with a deadline. Not a topic with open-ended exploration.*

**Core question:** "Do we know enough about this specific thing to make a decision and move forward?"

A spike is not a research project. It's not "go learn about AI" or "look into API options." It's a single, well-formed question that's blocking progress in the current phase — investigated just enough to unblock it, then done. The output is a decision, not a document.

This skill can be called from anywhere in the framework:
- **Brainstorming** — "can we actually do this capability before we commit to the idea?"
- **Discover** — "we need to understand how this data source works before we can design the flow"
- **Design Sprint** — "is this interaction feasible or are we designing something that can't be built?"
- **Plan** — "is this architecture viable before we commit phases to it?"
- **Build** — "we've hit an unknown on how to implement X — need to investigate before proceeding"

---

## What Makes a Good Spike Question

A spike question is specific, answerable, and has a clear "enough to decide" threshold.

**Good spike questions:**
- "Can we get real-time player data from the MFL API at latency useful for live evaluation — and what are the rate limits?"
- "Is there a Python library that handles OAuth2 with token refresh we can use, or do we need to build it?"
- "What does it actually cost to run Claude Sonnet on 10,000 evaluations per day at our expected payload size?"
- "Can the browser render 500 rows of live data without virtualization, or do we need a different approach?"

**Not spike questions:**
- "Research AI options" — too broad, no answer shape
- "Look into the MFL API" — no specific question, no threshold
- "Understand the competitive landscape" — that's a different kind of work (use `competitive-landscape` skill)
- "Figure out the architecture" — that's planning, not spiking

If the question can't be answered yes/no/partially with a specific finding, it's not ready to be a spike yet. Sharpen it first.

---

## Spike Domains

A spike can investigate anything that's blocking a decision:

| Domain | Examples |
|--------|---------|
| **API / Integration** | Rate limits, authentication, data shape, latency, cost |
| **Data** | Does this data exist, what format, how fresh, what's the access model |
| **Technical feasibility** | Can this be built with the stack we have, what's the complexity |
| **AI / ML capability** | Can a model do this reliably, what's the prompt shape, what's the cost |
| **Design pattern** | How do other products handle this interaction, what's the precedent |
| **Performance** | Will this be fast enough, what are the constraints |
| **Third-party** | Does this service do what we need, what are the limitations |

---

## Execution

### Step 1: Name the Spike

Before investigating anything, write the spike question in one sentence. If it takes more than one sentence, it's more than one spike.

> "The spike question is: [specific question]. We need to know this before we can [what it unblocks]."

State what phase called the spike and what decision it's blocking. This keeps the investigation focused and gives the return answer the right shape.

### Step 2: Set the Timebox

Name the constraint before starting. A spike is not done when you've learned everything — it's done when you have enough to decide.

| Spike complexity | Timebox |
|---|---|
| Quick lookup — docs, pricing, a test call | One round of investigation |
| Moderate — multiple sources, a working example needed | Two to three rounds |
| Deep — proof of concept required, multiple unknowns | Flag it: this may be more than one spike |

If the investigation is expanding beyond its timebox, stop. Surface what you've found so far and ask: "This is going deeper than expected — do you want to continue the spike or proceed with what we have?"

Never let a spike become open-ended research. The timebox is the discipline.

### Step 3: Investigate

Go find the answer. Use whatever tools are available and appropriate — web search, API docs, running a test, reading source code, examining a working example.

Investigation discipline:
- Stay on the question. If you find something interesting but adjacent, note it and keep going.
- Look for the specific thing that unblocks the decision — not the complete picture.
- If you find a definitive answer early, stop. Don't keep investigating once the question is answered.
- If multiple conflicting answers exist, surface the conflict — that's the finding.

### Step 4: Return the Answer

The spike answer has three parts:

**Finding** — what did the investigation actually turn up? Specific, factual, no fluff.

**Confidence** — how certain is this answer?
- `High` — verified directly, tested, from primary source
- `Medium` — strongly indicated, secondary source, not tested end-to-end
- `Low` — partial information, conflicting sources, needs a proof of concept to confirm

**Implication** — what does this mean for the phase that called the spike? This is the most important part. Not just "here's what we found" but "here's what this means for what you were doing."

Format:

```
## Spike Result — [Question]
**Called from:** [Phase]
**Finding:** [What was found — specific and factual]
**Confidence:** [High / Medium / Low] — [one sentence on why]
**Implication:** [What this means for the calling phase — what can now be decided]
**Unblocked:** [The decision or design element that can now proceed]

## If confidence is Medium or Low
**What would confirm it:** [The smallest thing needed to raise confidence — a proof of concept, a test call, a vendor confirmation]
**Proceed anyway?** [Recommendation — yes with caveat / no, needs confirmation / yes, low risk]
```

### Step 5: Route Back

After returning the answer, explicitly hand control back to the calling phase:

- **Brainstorm called it** → return to the brainstorm with the finding. If the capability is viable, the idea can move forward. If not, the idea needs reshaping or the capability gets parked.
- **Discover called it** → return to the discovery conversation with the data. The story can now be told more accurately.
- **Design Sprint called it** → return to the walk-through. The deferred decisions log can now be updated with a real answer.
- **Plan called it** → return to phase sequencing. The architecture decision can be made.
- **Build called it** → return to the implementation. The approach is now known.

Don't let the spike become a detour. The phase that called it is waiting. Return with the answer and keep moving.

**Design Review backlog lifecycle:**
When design-review triggers a spike, the blocked slice stays at `Blocked (spike)` in the backlog until the spike returns. Saving the result to `docs/spikes/` is not enough — design-review must run a round to process it. In that round: if confidence is High or Medium, the slice can be promoted toward Ready. If confidence is Low, surface it as a decision: run a second spike, proceed with a named assumption, or defer the slice. The slice does not move from Blocked automatically — it takes a design-review round to close the loop.

---

## When a Spike Produces More Spikes

Sometimes the answer to one question surfaces another unknown. That's fine — but name it explicitly rather than expanding the current spike.

> "The spike answered the main question, but it surfaced a related unknown: [new question]. Do you want to run a second spike on that, or proceed with what we have and note it as a risk?"

Two focused spikes are better than one sprawling investigation.

---

## Saving the Spike

Save spike results to `docs/spikes/spike-[date]-[topic].md`. Brief — just the formatted result above. This creates a record that other phases can reference and prevents re-investigating the same question later.

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Broad research question | No clear answer shape, investigation never ends | Sharpen to one specific question before starting |
| Ignoring the timebox | Spike becomes a research project | Stop at "enough to decide," surface what you have |
| Answering more than the question | Scope creep, loses focus | Note adjacent findings, stay on the question |
| Not stating the implication | Finding without meaning | Always connect the finding to what the calling phase can now do |
| Running multiple questions in one spike | Tangled findings, hard to act on | One spike, one question |
| Spiking things that don't need spiking | Procrastination dressed as research | If you can make a reasonable assumption and correct later, do that instead |
| Never coming back | Spike becomes a detour | Timebox enforces the return — the calling phase is waiting |

---

## The Discipline

A spike is a question with a deadline. The moment you have enough to make a decision, the spike is done. Return the answer, state what it unblocks, and hand control back to the phase that called it.

Research that doesn't conclude is just procrastination with better documentation.
