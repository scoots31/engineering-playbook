#!/usr/bin/env python3
"""Build Cursor-work-only copies of shared docs into the bundle output directory."""
from __future__ import annotations

import re
import sys
from pathlib import Path


def transform_ai_playbook(text: str) -> str:
    text = text.replace(
        "Single source of truth for **how** work runs. Product facts (PRDs, ADRs, runbooks) usually live in the "
        "**product** repository; this file defines stages, roles, and handoffs so Cursor and Claude Code stay aligned.",
        "Single source of truth for **how** work runs. Product facts (PRDs, ADRs, runbooks) usually live in the "
        "**product** repository; this file defines stages, roles, and handoffs for **Cursor** (this bundle is Cursor-only).",
    )
    text = text.replace(
        "1. **One driver per task** — Either Cursor or Claude Code leads a slice; do not edit the same branch blindly in parallel without a handoff.",
        "1. **One driver per task** — Cursor leads a slice; do not edit the same branch blindly in parallel without a written handoff.",
    )
    text = text.replace(
        "Roles are not separate people—they are **lenses**. In Cursor, use matching **skills** from `playbook/skills/` "
        "(installed per `integrate-cursor.md`). In Claude Code, paste the role section or ask the model to adopt that lens and output format.",
        "Roles are not separate people—they are **lenses**. In Cursor, use matching **skills** under `~/.cursor/skills/` "
        "(see `integrate-cursor-work.md` in this bundle) or read the `skills/*/SKILL.md` files under your playbook root from User rules.",
    )
    text = re.sub(
        r"\n\*\*Claude Code:\*\*[^\n]*(?:\n[^\n]*)*",
        "\n",
        text,
        count=1,
    )
    return text


def transform_handoff(text: str) -> str:
    return text.replace(
        "_Use this when switching between Cursor and Claude Code, or between agents/sessions, on the same piece of work._",
        "_Use this when switching between Cursor sessions or collaborators, or between agents, on the same piece of work._",
    )


def transform_workflow_vocab(text: str) -> str:
    text = text.replace(
        "**[`HANDOFF.template.md`](HANDOFF.template.md)** is orthogonal to the table above: use it when **switching tools** "
        "(Cursor ↔ Claude Code) or **sessions**, not as a “stage” in the lifecycle.",
        "**[`HANDOFF.template.md`](HANDOFF.template.md)** is orthogonal to the table above: use it when **switching sessions** "
        "or context, not as a “stage” in the lifecycle.",
    )
    return re.sub(
        r"\n## Claude Code primitives \(optional\)\n\n.*",
        "\n## Cursor skills\n\n"
        "Install role skills globally per `integrate-cursor-work.md` (copy `skills/*` into `~/.cursor/skills/`). "
        "User rules should list absolute paths to this bundle’s `skills/` tree if you skip the copy.\n",
        text,
        flags=re.DOTALL,
    )


def transform_skill_authoring(text: str) -> str:
    text = text.replace("# Skill authoring (playbook + Claude Code)", "# Skill authoring (Cursor)")
    text = text.replace(
        "Role lenses in this repo live as **`SKILL.md` files** (Cursor skills and readable by Claude Code when configured). "
        "Keep **one canonical definition** under `skills/` in the engineering playbook; avoid pasting divergent copies into chat.",
        "Role lenses live as **`SKILL.md` files** (Cursor skills). This bundle ships canonical copies under `skills/`; "
        "install them under `~/.cursor/skills/` or reference them by absolute path in User rules.",
    )
    return re.sub(
        r"\n## Claude Code–specific notes\n\n(?:- .+\n)+",
        "\n",
        text,
    )


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: cursor_work_bundle_transforms.py REPO_ROOT OUT_DIR", file=sys.stderr)
        sys.exit(2)
    root = Path(sys.argv[1])
    out = Path(sys.argv[2])
    eng = root / "docs" / "engineering"
    out_eng = out / "docs" / "engineering"
    out_eng.mkdir(parents=True, exist_ok=True)

    (out_eng / "AI_PLAYBOOK.md").write_text(
        transform_ai_playbook((eng / "AI_PLAYBOOK.md").read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    (out_eng / "HANDOFF.template.md").write_text(
        transform_handoff((eng / "HANDOFF.template.md").read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    (out_eng / "workflow-vocabulary.md").write_text(
        transform_workflow_vocab((eng / "workflow-vocabulary.md").read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    (out_eng / "skill-authoring.md").write_text(
        transform_skill_authoring((eng / "skill-authoring.md").read_text(encoding="utf-8")),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
