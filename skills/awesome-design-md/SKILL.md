---
name: awesome-design-md
description: Use DESIGN.md files to ground UI generation in a specific brand's design language. Fetch a design system reference from the awesome-design-md collection and drop it into the project so every AI-generated UI component matches the chosen aesthetic. Use when starting a new page, dashboard, or component and you want a consistent visual identity — not generic AI output.
---

# Awesome DESIGN.md

DESIGN.md is a plain-text design system document that AI agents read to generate consistent UI. It lives in your project root alongside AGENTS.md. Any AI coding agent reads it automatically and uses it to make typography, color, spacing, and component decisions.

## When to Use

- Starting a new page or UI component and want a specific aesthetic
- Building a product UI and want it to feel like a well-known design-forward product
- Replacing generic "AI slop" with intentional visual identity
- When the user says "make it feel like Notion" / "Linear-style" / "Stripe-clean"

## Collection Source

Browse available DESIGN.md files at: https://getdesign.md

Notable styles relevant to product and tool work:

| Brand | Aesthetic |
|-------|-----------|
| Linear | Minimal dark, tight spacing, keyboard-first |
| Notion | Clean editorial, warm grays, calm hierarchy |
| Stripe | Precision white, authoritative typography |
| Figma | Tooling-focused, high information density |
| Claude | Warm terracotta accent, editorial layout |
| Cursor | Sleek dark, gradient accents, developer-native |
| Raycast | Dark chrome, vibrant gradients, launcher-feel |
| Vercel | Black/white precision, Geist font, zero decoration |
| Superhuman | Premium dark, keyboard-first, purple glow |

## Process

### 1. Identify the aesthetic target

Ask the user (or infer from context): which brand's design language fits this project? Consider:
- Who are the users? (developers → Cursor/Warp; PMs → Linear/Notion; consumers → Stripe/Apple)
- What's the tone? (serious/premium vs. playful vs. utilitarian)
- Light or dark default?

### 2. Fetch the DESIGN.md

Direct the user to copy the DESIGN.md from `https://getdesign.md/<brand>/design-md` into their project root as `DESIGN.md`.

If the user wants you to reference it directly in context, ask them to paste the contents.

### 3. Apply it

Once DESIGN.md is in the project root:
- Reference it before generating any UI code
- Apply the color tokens, typography scale, spacing system, and component patterns it defines
- Do NOT override DESIGN.md choices with personal aesthetic preferences — the file is the spec

### 4. Adapt for project constraints

DESIGN.md files are inspiration, not law. Adapt where needed:
- If the project uses a dark theme override from `CLAUDE.md` or project config (e.g. `--bg:#090806`), honor that instead
- If the project has existing CSS variables, map DESIGN.md tokens onto them rather than creating parallel systems
- Note any conflicts between DESIGN.md and existing project styles — surface them to the user before generating code

## Key Principle

DESIGN.md does for visual design what AGENTS.md does for engineering behavior: it gives the AI a shared, explicit reference so outputs are consistent and intentional. One file, project-wide consistency.
