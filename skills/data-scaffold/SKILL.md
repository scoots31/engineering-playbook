---
name: data-scaffold
description: Generates realistic fake data for screens that don't have real APIs yet. Makes design review actually useful — screens with real-looking data produce better decisions than screens with placeholder text. Fake data lives in one mock layer, not scattered through the UI, so swapping to real data later is a replacement not a rewrite. The mapping document that comes out of this skill is the first draft of the API contract.
---

# Data Scaffold

*Fake it until the real data arrives. But fake it correctly.*

**Core question:** "What would this screen look like with real data — and where will that data eventually come from?"

This is not Lorem Ipsum. This is not `field1: "value"`. This is realistic data that makes a screen feel like a working product, generated from what we know about the domain — even before a single API endpoint exists.

The output is two things:
1. **A mock data layer** — one place where all fake data lives, easy to swap out for real data without touching the UI
2. **A data mapping document** — every fake field mapped to its eventual real source. This is the first draft of the API contract.

---

## Why This Matters

In real teams, developers resist fake data because they think of it as throwaway work. Write it now, throw it away when the real API comes. That framing is wrong — and it leads to bad fakes that make the problem worse (Lorem Ipsum, placeholder numbers, fields named `item1`).

The reframe: **fake data is a proto-specification.** Every field you generate is a decision about what the real data needs to look like. The mapping document isn't a reminder to replace it later — it's the earliest version of the API contract. When real data sources get wired up, the developer looks at the mapping and knows exactly what shape the response needs to come in.

For a solo with AI, this step is fast. The AI generates realistic data from domain knowledge, labels it clearly, and documents every field's eventual home. What takes a developer a frustrated afternoon takes one focused session.

---

## When to Run

- After the design sprint produces screens — before or during design review
- When design review surfaces a field or dataset that doesn't exist yet
- When build starts on the frontend and real APIs aren't ready
- Any time a screen has placeholder text where data should be

Runs before or alongside design review — not after. The value of data scaffold is that design review happens against realistic data, not against empty states.

---

## What Makes Good Fake Data

**Realistic, not random.** Fake player names should be real-sounding names. Fake scores should be in the range actual scores live in. Fake timestamps should be in formats the real system would use. Someone looking at the screen should not immediately know the data is fake.

**Domain-accurate.** If the real system uses fantasy football scoring, fake data uses realistic fantasy football point values — not `12.3` for every week because it's easy to type. Variance matters. Outliers matter. Empty states matter.

**Structurally honest.** The shape of the fake data should match the shape the real data will have — or as close as we can get given what we know. Field names should be plausible API names, not UI labels. `player_name` not `Name`. `slot_week_delta` not `Delta`.

**Consistently labeled.** Every place fake data appears — in code, in the UI, in comments — is marked as mock. No ambiguity about what's real and what isn't.

---

## Execution

### Step 1: Inventory the Screens

Read all design screens in `docs/design/`. For each screen, identify every piece of data that appears — every field, every number, every label that would come from a real data source rather than being static UI text.

Group by data entity. A player screen might have: player identity fields, roster context fields, slot target fields, week-by-week performance data. Each group is a data entity that will eventually map to an API endpoint or database table.

### Step 2: Understand What We Know

Before generating anything, ask the solo what they know about the data:

- What data sources exist or are planned? (MFL API, internal DB, third-party, etc.)
- For each data entity — do we know the real field names, or are those TBD?
- Are there any real data samples available, even partial?
- What are the realistic ranges and formats? (point values, date formats, IDs)

One round of questions. Don't over-ask — reasonable assumptions can be made for things like numeric ranges and date formats. Ask about things only the solo knows — data source identity, any known field names, domain-specific constraints.

### Step 3: Generate the Mock Data Layer

Create `data/mock/` in the project. This is where all fake data lives — one place, clearly named, completely separate from the UI.

**File structure:**
```
data/mock/
├── mock-index.js          # or mock-index.py — exports all mock data
├── players.json           # player identity and profile data
├── roster.json            # roster context, slot assignments
├── performance.json       # week-by-week performance data
├── [entity].json          # one file per data entity
└── README.md              # explains mock layer, links to mapping doc
```

Every mock file starts with a header comment:

```json
{
  "_mock": true,
  "_note": "PLACEHOLDER DATA — not connected to real API. See docs/data-mapping.md for field sources.",
  "_entity": "player_performance",
  "data": [...]
}
```

Generate the data with:
- Real-looking values in domain-accurate ranges
- Enough records to show realistic list states (not just one row)
- At least one edge case — a bye week, a zero score, a missing field — so empty states are tested
- Consistent IDs that cross-reference between entities

**Flag data behavior candidates:** For any entity that is a list or pulls from an external API with scale implications, add a flag to the data-mapping.md connection status table. These entities need the data behavior pass in design review before dependent UI slices can reach Ready:

| Entity | Mock file | Real source | Status | Data behavior candidate |
|--------|-----------|-------------|--------|------------------------|
| Players | data/mock/players.json | MFL API | ⏳ Pending | ✓ List — needs data behavior pass |
| Performance | data/mock/performance.json | Internal DB | ⏳ Pending | ✓ List — needs data behavior pass |

### Step 4: Wire the Mock Layer to the Screens

Update the design screens to pull from the mock layer instead of having data hardcoded in the HTML. The UI should not know or care whether data is real or mock — it just reads from the data source.

How this looks depends on the stack:

**Static HTML screens (design sprint artifacts):**
```html
<script src="../../data/mock/mock-index.js"></script>
<script>
  // MOCK DATA — replace MockData with real API call when available
  const player = MockData.players.find(p => p.id === 'JJ-001');
  renderPlayerHeader(player);
</script>
```

**Python/Flask backend:**
```python
# mock_data.py — PLACEHOLDER — replace with real DB/API calls
# See docs/data-mapping.md for field sources
def get_player(player_id):
    return MOCK_PLAYERS.get(player_id)
```

**Frontend framework:**
```js
// api/mock.js — PLACEHOLDER DATA LAYER
// Swap this file for api/real.js when APIs are ready
export const getPlayer = (id) => mockPlayers.find(p => p.id === id);
```

The pattern is always the same: **the mock layer is a seam.** The UI calls a function. In development, that function returns mock data. In production, that same function calls the real API. The UI code doesn't change — only the data layer underneath it.

### Step 5: Add the Mock Indicator

Anywhere mock data is active, make it visible during development. Not intrusive — but unambiguous.

For design screens, a small badge in the corner:
```html
<div class="mock-indicator">⚡ Mock data</div>
```

```css
.mock-indicator {
  position: fixed; bottom: 12px; right: 12px;
  background: rgba(245,166,35,0.9); color: #000;
  font: 700 11px/1 monospace; padding: 4px 8px;
  border-radius: 4px; letter-spacing: 0.06em;
  z-index: 9999;
}
```

For code, a consistent comment pattern:
```python
# MOCK — replace with: PlayerAPI.get(player_id)
```

The indicator disappears automatically when the real data layer is connected. No cleanup required.

### Step 6: Write the Data Mapping Document

`docs/data-mapping.md` — the proto-API contract. Every fake field, mapped to its eventual real source. This document is what makes the fake data valuable beyond the immediate moment.

---

```markdown
# Data Mapping — [Project Name]
**Created:** [YYYY-MM-DD]
**Status:** Mock data active — [N] of [N] entities connected to real sources

This document maps every field in the mock data layer to its eventual real data source.
It is the first draft of the API contract. Update it as real sources get connected.

---

## Connection Status

| Entity | Mock file | Real source | Status |
|--------|-----------|-------------|--------|
| Player identity | `data/mock/players.json` | MFL Players API | ⏳ Pending |
| Roster context | `data/mock/roster.json` | MFL Rosters API | ⏳ Pending |
| Performance data | `data/mock/performance.json` | Internal DB — weekly_scores | ⏳ Pending |

---

## Field Mapping

### Player Identity

| Mock field | Mock example | Real source | Real field name | Notes |
|------------|-------------|-------------|-----------------|-------|
| `id` | `"JJ-001"` | MFL Players API | `playerID` | MFL uses string IDs |
| `name` | `"Justin Jefferson"` | MFL Players API | `name` | Full name, no truncation |
| `position` | `"WR"` | MFL Players API | `position` | Uppercase abbreviation |
| `nfl_team` | `"MIN"` | MFL Players API | `team` | 3-letter abbreviation |
| `jersey` | `18` | MFL Players API | `jerseyNumber` | Integer |
| `status` | `"Active"` | MFL Players API | `status` | Active / IR / Taxi |

### Performance Data

| Mock field | Mock example | Real source | Real field name | Notes |
|------------|-------------|-------------|-----------------|-------|
| `week` | `1` | Internal DB | `week_number` | 1-indexed, season week |
| `actual_pts` | `17.4` | Internal DB | `points_scored` | Float, 1 decimal |
| `slot_target` | `14.2` | Computed | — | Calculated from slot config |
| `delta` | `3.2` | Computed | — | actual_pts − slot_target |

[Continue for each entity]

---

## Connecting Real Data

When a real data source is ready:

1. Create the real data function in `api/real.js` (or equivalent)
2. Update connection status table above
3. Run the full screen against real data — verify field names match
4. Remove the mock indicator badge
5. Delete the mock file for that entity

The UI code does not change. Only the data layer underneath.
```

### Step 7: Update Mock After Data Questions Resolve

When the data questions log (in `docs/backlog.md`) has newly resolved entries, update the mock data layer to reflect confirmed behavior. This step and slice finalization happen together — not sequentially.

For each resolved question, update the relevant mock file:

- **Pagination confirmed:** Add edge case records — last page (1 record), empty page (0 records), single-result list
- **Null fields confirmed:** Seed the expected percentage of records with null values matching the real-world rate
- **Empty state confirmed:** Add a named empty-state record set that can be activated during development
- **Error state confirmed:** Add an error response mock for testing gracefully degraded UI states
- **Volume confirmed:** Ensure enough records to reflect real list behavior (10+ if large lists expected)

Update `docs/data-mapping.md` with a "Behavior notes" column in the connection status table:

| Entity | Mock file | Real source | Status | Data behavior candidate | Behavior notes |
|--------|-----------|-------------|--------|------------------------|----------------|
| Players | data/mock/players.json | MFL API | ⏳ Pending | ✓ | Paginates at 25, slot_target null ~15% |

The mock indicator badge stays active. The mock layer now reflects confirmed real-world behavior — not just placeholder structure — so UI slices are built against realistic conditions from the start.

---

## Realistic Data Generation Guidelines

| Domain | Guidance |
|--------|---------|
| **Fantasy football scores** | WR: 6–22 pts typical range, 0–5 for bad weeks, 25+ for outlier. Don't use the same number twice. |
| **Player names** | Use real NFL player names from known rosters — makes design review feel authentic |
| **Dates / weeks** | Use actual calendar weeks for the season being mocked. W7 bye for Minnesota in 2026 is real. |
| **IDs** | Use a consistent format — `JJ-001` or `player_13141` — that looks like a real ID scheme |
| **Percentages / computed fields** | Calculate from the fake raw data — don't just write "64%", actually compute 9/14 |
| **Empty / edge states** | Always include at least: one bye week, one worst-case score, one missing-data scenario |
| **List lengths** | Enough rows to show a real list (10+ for tables), not just 3 showcase rows |

---

## Swapping to Real Data — The Checklist

When a real data source is ready to connect:

- [ ] Real API/DB returns data in the shape documented in `data-mapping.md`
- [ ] Field names reconciled — mock names updated to match real names if different
- [ ] Real function created in the data layer (not in the UI)
- [ ] Tested against real data — all screens render correctly
- [ ] Edge cases tested — empty state, missing fields, error state
- [ ] Mock file for this entity deleted
- [ ] Connection status updated in `data-mapping.md`
- [ ] Mock indicator badge gone from affected screens

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|---|---|---|
| Lorem Ipsum / placeholder text | Unusable for design review — nothing feels real | Domain-accurate data that looks like real output |
| Hardcoding data directly in UI | Scattered, impossible to swap cleanly | One mock layer, one place, referenced by UI |
| Same value for every record | Doesn't reveal layout issues with real variance | Generate with realistic range and outliers |
| Field names that are UI labels | Creates disconnect from real API shape | Use plausible API field names from the start |
| Skipping edge cases | Empty states untested until production | Always include bye week, zero score, missing field |
| Forgetting to label it | Confusion about what's real | Mock indicator badge + comment pattern everywhere |
| Delaying data scaffold until build | Design review happens against empty screens | Run data scaffold before or during first design review |
