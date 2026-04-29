# Session Metrics Log

Tracks token usage and session data per project to enable framework vs. no-framework comparisons over time.

**How to log:** At the end of a project or phase, pull the session files from `~/.claude/projects/` and record the numbers below. The parse script in the notes column can be run any time.

---

## Fields

| Field | What it means |
|---|---|
| Project | Name of the project |
| Framework | Yes / No |
| Phase | Which phase (Discovery, Build, Test, etc.) or Full Project |
| Sessions | Number of Claude Code sessions |
| Turns | Total turns across all sessions |
| Output tokens | Total output tokens (most reliable measure — input is skewed by caching) |
| Shipped | What was actually produced |
| Date range | When the work happened |
| Notes | Anything notable — rework, scope changes, stuck sessions |

---

## Log

| Project | Framework | Phase | Sessions | Turns | Output tokens | Shipped | Date range | Notes |
|---|---|---|---|---|---|---|---|---|
| Solo Companion | Yes | Build (Phase 1) | 4 | 1,942 | 1,492,258 | 24 slices, companion app | 2026-04-28 – 2026-04-29 | Includes Ren + curator sessions |

---

## Pending — Projects to Backfill

These ran before this log existed. Pull if a comparison becomes useful.

- CTL Library / CTL Trips — multiple sessions in `~/.claude/projects/-Users-scottheinemeier-Apps/`, no framework
- Weekly Budget — same dir, no framework

---

## How to Pull Numbers for a Session Directory

```
python3 -c "
import json, glob, os

def parse_session(path):
    tokens_in, tokens_out, turns = 0, 0, 0
    first_ts = last_ts = None
    with open(path) as f:
        for line in f:
            try:
                obj = json.loads(line)
                ts = obj.get('timestamp')
                if ts:
                    if not first_ts: first_ts = ts
                    last_ts = ts
                usage = obj.get('message', {}).get('usage', {})
                if usage:
                    tokens_in += usage.get('input_tokens', 0)
                    tokens_out += usage.get('output_tokens', 0)
                    turns += 1
            except: pass
    return tokens_in, tokens_out, turns, first_ts, last_ts

project_dir = os.path.expanduser('~/.claude/projects/YOUR-PROJECT-DIR')
total_in = total_out = total_turns = 0
for f in glob.glob(project_dir + '/*.jsonl'):
    ti, to, turns, first, last = parse_session(f)
    if ti + to > 0:
        print(f'{os.path.basename(f)[:36]}: out={to:,} turns={turns} [{first[:10] if first else \"?\"}]')
        total_in += ti; total_out += to; total_turns += turns
print(f'TOTAL: out={total_out:,} turns={total_turns}')
"
```

Replace `YOUR-PROJECT-DIR` with the directory name from `~/.claude/projects/`.

---

## Notes on Interpretation

- **Input tokens are unreliable** — Claude Code's prompt caching means cached tokens don't appear in the log the same way. Use output tokens as the primary comparison metric.
- **Turns are a proxy for conversation sprawl** — high turns with low output per turn often signals rework or clarification loops.
- **Output tokens per turn** is the most useful derived metric — framework sessions should trend lower as context is structured and handoffs are clean.
- **Fair comparisons require similar project complexity** — don't compare a 24-slice build against a one-off script fix.
