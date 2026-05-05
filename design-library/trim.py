#!/usr/bin/env python3
"""
trim.py — produce styles-bundled.json for repo distribution.

Reads the full styles.json (local only, gitignored) and writes a
category-diverse subset to styles-bundled.json (tracked in git).

Target: ~500 entries, maximising category variety and data richness.
Extracted entries (source: "extracted") are always included.

Usage:
    python3 trim.py [--target 500]
"""
import json
import argparse
from pathlib import Path
from collections import defaultdict

HERE = Path(__file__).parent


def richness(entry):
    """Score an entry by data quality — higher is better."""
    score = 0
    ds = entry.get("style", {}).get("fullResult", {}).get("designSystem", {})
    if ds.get("northStar"):
        score += 4
    if ds.get("colors"):
        score += 2
    if ds.get("typography"):
        score += 2
    if ds.get("tags"):
        score += 1
    if ds.get("industry"):
        score += 1
    return score


def get_category(entry):
    ds = entry.get("style", {}).get("fullResult", {}).get("designSystem", {})
    return (ds.get("category") or "unknown").lower().strip()


def trim(target=500):
    src = HERE / "styles.json"
    if not src.exists():
        print("styles.json not found — run seed.py first.")
        return

    with open(src) as f:
        data = json.load(f)

    # Support both flat list and {styles: [...]} wrapper formats
    entries = data["styles"] if isinstance(data, dict) and "styles" in data else data

    # Always keep extracted entries
    extracted = [e for e in entries if e.get("source") == "extracted"]
    refero = [e for e in entries if e.get("source") != "extracted"]

    remaining = target - len(extracted)
    if remaining <= 0:
        result = extracted
    else:
        # Group by category, sort each group by richness descending
        by_category = defaultdict(list)
        for e in refero:
            by_category[get_category(e)].append(e)

        for cat in by_category:
            by_category[cat].sort(key=richness, reverse=True)

        # Proportional sample: each category gets a share proportional to its size
        total_refero = len(refero)
        sampled = []
        for cat, group in sorted(by_category.items()):
            share = max(1, round(len(group) / total_refero * remaining))
            sampled.extend(group[:share])

        # If we overshot, trim by lowest richness; if undershot, top up from highest
        sampled.sort(key=richness, reverse=True)
        sampled = sampled[:remaining]

        result = extracted + sampled

    out = HERE / "styles-bundled.json"
    with open(out, "w") as f:
        json.dump({"source": "bundled", "styles": result, "count": len(result)}, f, separators=(",", ":"))

    size_mb = out.stat().st_size / 1_048_576
    cats = {get_category(e) for e in result if e.get("source") != "extracted"}
    print(f"Written {len(result)} entries to styles-bundled.json")
    print(f"Size: {size_mb:.1f} MB")
    print(f"Categories covered: {len(cats)}")
    print(f"Extracted entries included: {len(extracted)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=500)
    args = parser.parse_args()
    trim(args.target)
