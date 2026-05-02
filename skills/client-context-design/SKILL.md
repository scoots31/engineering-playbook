---
name: client-context-design
description: Loads a client's design system context from a local library repo. Generic and reusable — works with any client that has a context.md file. Fires automatically at design sprint start when a project declares a client_context path, or invoked manually for quick builds that need brand context without a full project structure.
---

# Client Context Design

*Load the client's design language before building anything.*

---

## What This Skill Does

Reads a client context file (`context.md`) from a local design library repo and makes it active for the session. Once loaded, the design sprint knows:

- The client's design tokens (colors, typography, spacing, elevation)
- The component inventory — what exists, what each piece is for
- The screen and layout patterns
- Regional variance rules — what's fixed globally vs. what changes by market
- The quick-build reference — minimum needed to produce on-brand work fast

With context loaded, two paths are available:

**Path 1 — Existing design.** A Figma file exists. The framework uses context knowledge + Figma MCP to implement it accurately — knowing what it's looking at, not guessing at component purpose or token values.

**Path 2 — New design.** No Figma file. The framework uses the context as the complete design system constraint and builds from scratch within the client's conventions. The quick-build reference drives this path.

---

## Activation

**Automatic** — fires at the start of design sprint when the project's `CLAUDE.md` declares:
```
client_context: ~/Developer/[client-library-repo]/context.md
```

**Manual** — invoked directly for quick builds that don't have a full project structure. Say `/client-context-design` or "load client context."

---

## Execution

### On Activation

1. **Locate the context file.**

   If the project `CLAUDE.md` declares a `client_context` path: read that file directly.

   If invoked manually with no declared path: check `~/Developer/engineering-playbook/clients.md` for registered clients and present the list. If the right client isn't listed, ask:
   > "What's the path to the client context file?"

2. **Read the context file.** Load all sections: tokens, component inventory, patterns, regional variance rules, quick-build reference.

3. **Confirm what's loaded.** One sentence:
   > "Loaded [client] design context — [X] components, [Y] screen patterns, regional variance rules for [markets if listed]. Context is active."

4. **Ask the fork question:**
   > "Do you have an existing design to work from, or are we building new?"

---

### Path 1 — Existing Design

The solo has a Figma file.

1. Ask for the Figma file link or file name.
2. Load the file via Figma MCP.
3. Cross-reference what you find against the loaded context:
   - Identify which components from the inventory appear in this file
   - Note any tokens that differ from the context (regional variant? custom one-off?)
   - Flag any components or patterns not in the context library (new additions to document later)
4. Surface a brief orientation:
   > "This file uses [X components from the library]. I see [any differences or unknowns]. Ready to proceed with the design sprint from this file."
5. Continue into design sprint on-ramp 2 (Figma exists). The context is the interpretive layer — use it throughout to understand what you're implementing, not just what you're seeing.

---

### Path 2 — New Design

No Figma file. Building from scratch within client conventions.

1. Confirm which market/region this design is for. Load the applicable regional variance rules.
2. Surface the quick-build reference as the active design system:
   > "Building for [market]. Active design system: [essential colors], [essential type], [essential components]. Ready to start."
3. Continue into design sprint on-ramp 1 (from scratch). Treat the quick-build reference as the aesthetic constraint — same role as "make it feel like ESPN" but the client's own system.
4. Every design decision during the sprint must be traceable to the loaded context. If a choice isn't in the context, surface it as a decision:
   > "This pattern isn't in the context library — using [X] which is closest to [Y component]. Should I note this as a new pattern for the library?"

---

## After the Sprint

At the close of any session that used this skill, ask:
> "Did we introduce anything new — components, patterns, tokens — that isn't in the context library yet? If so, I can note what should be added."

Capture any additions as notes and direct the solo to update the library in a separate pass. The library grows as Bayer projects accumulate.

---

## Clients Registry

Known client libraries are registered in `~/Developer/engineering-playbook/clients.md`. When invoked manually, read this file to present available clients before asking for a path.

---

## What This Skill Is Not

- Not a replacement for the Figma MCP on Path 1 — the MCP still pulls the actual file. This skill provides the interpretive layer.
- Not a design generator — it loads context so the design sprint can run correctly. The design sprint skill does the design work.
- Not Bayer-specific — any client with a `context.md` in the correct format can use this skill.
