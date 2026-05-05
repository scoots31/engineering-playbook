#!/usr/bin/env python3
"""
Design library search — finds the closest style matches for a product description.
Used by the design-sprint skill at the Design Identity step.

Usage:
  python search.py "dark productivity SaaS tool"
  python search.py "fintech dashboard light minimal" --top 5
  python search.py "photography portfolio editorial" --format json
"""
import argparse
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# Prefer full library when available locally; fall back to bundled repo version
_full = os.path.join(_HERE, "styles.json")
_bundled = os.path.join(_HERE, "styles-bundled.json")
LIBRARY = _full if os.path.exists(_full) else _bundled

# Category keyword maps — expands single-word product categories into related terms
CATEGORY_EXPANSIONS = {
    "productivity": ["productivity", "work", "task", "project", "todo", "calendar", "planning", "tool"],
    "fintech": ["fintech", "finance", "financial", "banking", "bank", "money", "payment", "invest", "trading", "crypto", "wealth"],
    "saas": ["saas", "software", "platform", "dashboard", "admin", "tool", "app", "workspace"],
    "ecommerce": ["ecommerce", "shop", "store", "retail", "product", "checkout", "cart", "buy"],
    "portfolio": ["portfolio", "personal", "designer", "photographer", "creative", "agency", "studio", "freelance"],
    "editorial": ["editorial", "magazine", "media", "news", "blog", "publishing", "content"],
    "ai": ["ai", "artificial intelligence", "machine learning", "model", "llm", "assistant", "chatbot"],
    "healthcare": ["health", "healthcare", "medical", "wellness", "fitness", "therapy"],
    "entertainment": ["entertainment", "music", "video", "streaming", "gaming", "game", "media"],
    "developer": ["developer", "dev", "code", "coding", "engineering", "api", "cli", "docs", "documentation"],
    "food": ["food", "restaurant", "coffee", "beverage", "drink", "dining"],
    "travel": ["travel", "trip", "flight", "hotel", "accommodation", "booking"],
    "real_estate": ["real estate", "property", "housing", "architecture", "home"],
    "fashion": ["fashion", "luxury", "clothing", "apparel", "brand", "style"],
    "education": ["education", "learning", "course", "school", "training", "teach"],
}

MOOD_KEYWORDS = {
    "minimal": ["minimal", "clean", "simple", "whitespace", "sparse", "restrained"],
    "bold": ["bold", "dramatic", "strong", "impactful", "vivid", "striking"],
    "dark": ["dark", "midnight", "obsidian", "black", "night", "shadow"],
    "light": ["light", "white", "bright", "airy", "paper", "cream", "warm"],
    "technical": ["technical", "engineering", "precision", "systematic", "blueprint", "grid", "mono"],
    "editorial": ["editorial", "typographic", "print", "magazine", "journal"],
    "playful": ["playful", "fun", "friendly", "approachable", "whimsical", "colorful"],
    "premium": ["premium", "luxury", "elegant", "refined", "sophisticated", "high-end"],
}


def tokenize(text):
    """Lowercase and split text into words."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def expand_query(query_words):
    """Add category and mood expansions to query words."""
    expanded = set(query_words)
    for word in query_words:
        for category, terms in CATEGORY_EXPANSIONS.items():
            if word in terms or word == category:
                expanded.update(terms)
        for mood, terms in MOOD_KEYWORDS.items():
            if word in terms or word == mood:
                expanded.update(terms)
    return expanded


def normalize(entry):
    """
    Normalize an entry to a flat dict regardless of whether it came from
    the Refero detail API (nested under 'style' + 'fullResult.designSystem')
    or was produced by our own extract.py (already flat).
    """
    # Refero detail format: top-level key is 'style'
    style = entry.get("style", entry)
    ds = style.get("fullResult", {}).get("designSystem", {})

    # Prefer designSystem fields; fall back to top-level fields for extracted entries
    north_star = ds.get("northStar") or style.get("northStar") or entry.get("northStar") or ""
    site_name = style.get("siteName") or entry.get("siteName") or ""
    color_scheme = style.get("colorScheme") or entry.get("colorScheme") or ""
    industry = style.get("industry") or ds.get("category") or entry.get("industry") or ""
    tags = ds.get("tags") or entry.get("tags") or []
    url = style.get("url") or entry.get("url") or ""
    source = entry.get("source", "refero")

    # Colors: designSystem format is [{name, hex}], extract.py format is [{name, hex, usage}]
    colors = ds.get("colors") or entry.get("colors") or []

    # Typography: designSystem has a list of role objects; extract.py has a fonts list
    fonts = []
    ds_typo = ds.get("typography") or []
    if ds_typo and isinstance(ds_typo, list):
        for t in ds_typo:
            fam = t.get("fontFamily") or t.get("family") or ""
            if fam and fam not in fonts:
                fonts.append(fam)
    if not fonts:
        fonts = entry.get("fonts") or style.get("fonts") or []

    return {
        "siteName": site_name,
        "northStar": north_star,
        "colorScheme": color_scheme,
        "industry": industry,
        "tags": tags,
        "colors": colors,
        "fonts": fonts,
        "url": url,
        "source": source,
        "_raw": entry,
    }


def score_entry(norm, query_words, expanded_query):
    """Score a normalized entry against the query. Higher is better."""
    score = 0

    north_star = norm["northStar"].lower()
    site_name = norm["siteName"].lower()
    color_scheme = norm["colorScheme"].lower()
    industry = norm["industry"].lower()
    tags = " ".join(norm["tags"]).lower()
    colors = " ".join(c.get("name", "") for c in norm["colors"]).lower()
    fonts = " ".join(norm["fonts"]).lower()

    haystack_words = tokenize(f"{north_star} {site_name} {colors} {fonts} {industry} {tags}")
    scheme_words = tokenize(color_scheme)

    # Direct query word matches in north star (highest weight)
    for word in query_words:
        if word in north_star:
            score += 4
        if word in site_name:
            score += 2
        if word in industry:
            score += 3
        if word in tags:
            score += 2

    # Expanded query matches
    for word in expanded_query - query_words:
        if word in haystack_words:
            score += 1

    # Color scheme alignment
    if "dark" in query_words and "dark" in scheme_words:
        score += 3
    if "light" in query_words and "light" in scheme_words:
        score += 3
    if "both" in scheme_words:
        score += 1

    # Penalize entries with no north star (less useful as references)
    if not norm["northStar"]:
        score -= 10

    return score


def format_entry(norm, rank=None, score=None):
    """Format a normalized entry for display."""
    name = norm["siteName"] or "Unknown"
    north_star = norm["northStar"] or "(no north star)"
    scheme = norm["colorScheme"] or "unknown"
    colors = norm["colors"]
    fonts = norm["fonts"]
    source = norm["source"]
    industry = norm["industry"]
    tags = norm["tags"][:4]

    color_names = ", ".join(c.get("name", c.get("hex", "?")) for c in colors[:4])
    primary_font = fonts[0] if fonts else "unknown"
    tag_str = ", ".join(tags) if tags else ""

    prefix = f"[{rank}] " if rank else ""
    score_str = f" (score: {score})" if score is not None else ""
    lines = [
        f"{prefix}{name} ({scheme}){score_str}",
        f"  North star: {north_star}",
        f"  Category: {industry}" + (f" · Tags: {tag_str}" if tag_str else ""),
        f"  Colors: {color_names or '(none)'}",
        f"  Font: {primary_font}",
        f"  Source: {source}",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Search the design library for matching styles")
    parser.add_argument("query", help="Product description to match against (e.g. 'dark SaaS productivity tool')")
    parser.add_argument("--top", type=int, default=5, help="Number of results to return (default: 5)")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--scheme", choices=["light", "dark", "both"], help="Filter by color scheme")
    args = parser.parse_args()

    if not os.path.exists(LIBRARY):
        print(f"Library not found at {LIBRARY}. Run seed.py first.", file=sys.stderr)
        sys.exit(1)

    with open(LIBRARY) as f:
        lib = json.load(f)

    styles = lib.get("styles", [])
    query_words = tokenize(args.query)
    expanded = expand_query(query_words)

    # Normalize and score all entries
    scored = []
    for entry in styles:
        norm = normalize(entry)
        # Scheme filter
        if args.scheme and norm["colorScheme"] not in (args.scheme, "both"):
            continue
        s = score_entry(norm, query_words, expanded)
        if s > 0:
            scored.append((s, norm))

    # Sort by score descending, break ties by northStar length (longer = more detail)
    scored.sort(key=lambda x: (x[0], len(x[1]["northStar"])), reverse=True)
    top = scored[: args.top]

    if not top:
        print("No matches found. Try broader terms.")
        sys.exit(0)

    if args.format == "json":
        results = [
            {
                "rank": i + 1,
                "score": s,
                "siteName": n["siteName"],
                "northStar": n["northStar"],
                "colorScheme": n["colorScheme"],
                "industry": n["industry"],
                "tags": n["tags"],
                "colors": n["colors"][:6],
                "fonts": n["fonts"][:3],
                "url": n["url"],
                "source": n["source"],
            }
            for i, (s, n) in enumerate(top)
        ]
        print(json.dumps(results, indent=2))
    else:
        print(f"Top {len(top)} matches for: \"{args.query}\"\n")
        for i, (score, norm) in enumerate(top):
            print(format_entry(norm, rank=i + 1))
            print()


if __name__ == "__main__":
    main()
