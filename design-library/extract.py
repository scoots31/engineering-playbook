#!/usr/bin/env python3
"""
Design library extractor — visits any URL, pulls its design system,
generates a north star via Claude, and adds the entry to styles.json.

Usage:
  python extract.py https://example.com
  python extract.py https://example.com --name "Brand Name"
  python extract.py https://example.com --update   # overwrite if URL exists
"""
import argparse
import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request

LIBRARY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.json")
_ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


def _load_env():
    """Load .env file from this directory if present."""
    if os.path.exists(_ENV_FILE):
        with open(_ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    val = v.strip().strip("'\"")
                    if val:  # only overwrite if .env has a real value
                        os.environ[k.strip()] = val


_load_env()


def fetch(url, timeout=12):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,text/css,*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="ignore")


def absolute_url(href, base):
    if href.startswith("http"):
        return href
    if href.startswith("//"):
        return "https:" + href
    parsed = urllib.parse.urlparse(base)
    if href.startswith("/"):
        return f"{parsed.scheme}://{parsed.netloc}{href}"
    return None


def extract_stylesheet_urls(html, base_url):
    urls = []
    for m in re.finditer(
        r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']',
        html,
        re.IGNORECASE,
    ):
        url = absolute_url(m.group(1), base_url)
        if url:
            urls.append(url)
    return urls[:6]


def extract_inline_css(html):
    return " ".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.DOTALL | re.IGNORECASE))


def extract_colors(css):
    # Custom properties with color-like names
    custom = {}
    for m in re.finditer(
        r"(--(?:color|bg|background|text|foreground|accent|primary|secondary|brand|surface|muted|border|fill|stroke|base|canvas)[^\s:]*)\s*:\s*"
        r"(#[0-9a-fA-F]{3,8})",
        css,
    ):
        custom[m.group(1).strip()] = m.group(2).strip()

    # Frequency count of direct hex colors
    all_hex = re.findall(
        r"(?:color|background(?:-color)?|border-color|fill|stroke)\s*:\s*(#[0-9a-fA-F]{3,8})",
        css,
    )
    freq = {}
    for c in all_hex:
        freq[c] = freq.get(c, 0) + 1
    top = [c for c, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:16]]

    return {"custom_properties": custom, "frequent_hex": top}


def extract_fonts(html, css):
    fonts = []
    seen = set()

    # @font-face declarations
    for m in re.finditer(r"@font-face\s*\{[^}]*font-family\s*:\s*['\"]?([^;'\"{}]+)['\"]?", css, re.IGNORECASE):
        name = m.group(1).strip().strip("'\"")
        if name and name not in seen:
            fonts.append(name)
            seen.add(name)

    # font-family property values
    for m in re.finditer(r"font-family\s*:\s*([^;}{]+)", css):
        raw = m.group(1).strip()
        first = raw.split(",")[0].strip().strip("'\"")
        skip = {"-apple-system", "system-ui", "sans-serif", "serif", "monospace", "inherit", "initial", "var("}
        if first and not any(first.startswith(s) for s in skip) and first not in seen:
            fonts.append(first)
            seen.add(first)

    # Google Fonts URLs in HTML
    for m in re.finditer(r"fonts\.googleapis\.com/css[^\"']*family=([^\"'&]+)", html):
        for part in m.group(1).split("|"):
            name = part.split(":")[0].replace("+", " ").strip()
            if name and name not in seen:
                fonts.append(name)
                seen.add(name)

    return fonts[:8]


def detect_scheme(css, html):
    dark_media = bool(re.search(r"prefers-color-scheme\s*:\s*dark", css))
    body_bg = re.search(
        r"(?:body|:root|html)\s*\{[^}]*background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,8})", css
    )
    scheme = "light"
    if body_bg:
        c = body_bg.group(1).lstrip("#")
        if len(c) == 3:
            c = "".join(x * 2 for x in c)
        if len(c) == 6:
            r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
            if (0.299 * r + 0.587 * g + 0.114 * b) / 255 < 0.4:
                scheme = "dark"
    return "both" if dark_media else scheme


def extract_meta(html):
    title = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
    desc = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']{0,300})["\']',
        html,
        re.IGNORECASE,
    )
    return (title.group(1).strip() if title else ""), (desc.group(1).strip() if desc else "")


def generate_north_star(url, site_name, colors, fonts, scheme, title, description):
    from anthropic import Anthropic  # import here so the module works without anthropic if just doing --help

    client = Anthropic()

    prompt = f"""You are analyzing the design system of a website to produce a structured design profile.

Website: {site_name} ({url})
Page title: {title}
Description: {description}
Color scheme detected: {scheme}
Fonts found: {', '.join(fonts) if fonts else 'not detected'}
CSS custom property colors: {json.dumps(colors.get('custom_properties', {}), indent=2)[:1200]}
Frequent hex colors: {colors.get('frequent_hex', [])}

Produce a JSON object with exactly these fields:
- "northStar": One evocative sentence (10-20 words) that captures the design's visual identity and feeling. Be specific and cinematic — like "Architectural blueprint on white marble" or "Midnight command center lit by precise accents." Never generic.
- "namedColors": Array of 4-8 objects, each with:
    - "name": evocative 2-word name (e.g. "Midnight Ink", "Powder Blue")
    - "hex": the hex value
    - "usage": what this color is used for (e.g. "primary action", "page background", "body text", "muted text")
  Pick the most distinctive and useful colors. Skip near-duplicates.
- "fonts": Array of font family names, most important first. Max 4.
- "colorScheme": "light", "dark", or "both"

Return only the raw JSON object. No markdown, no explanation."""

    msg = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = msg.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    return json.loads(raw)


def load_library():
    if os.path.exists(LIBRARY):
        with open(LIBRARY) as f:
            return json.load(f)
    return {"source": "refero+extracted", "styles": []}


def save_library(lib):
    lib["count"] = len(lib["styles"])
    with open(LIBRARY, "w") as f:
        json.dump(lib, f, indent=2)


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main():
    parser = argparse.ArgumentParser(description="Extract design system from a URL and add to the library")
    parser.add_argument("url", help="URL to analyze")
    parser.add_argument("--name", help="Brand/site name (overrides auto-detected)")
    parser.add_argument("--update", action="store_true", help="Overwrite if this URL already exists in library")
    args = parser.parse_args()

    url = args.url
    if not url.startswith("http"):
        url = "https://" + url

    print(f"Fetching {url}...")
    try:
        html = fetch(url)
    except Exception as e:
        print(f"Error fetching page: {e}")
        sys.exit(1)

    page_title, meta_desc = extract_meta(html)
    site_name = args.name or urllib.parse.urlparse(url).netloc.replace("www.", "").split(".")[0].capitalize()

    print("Collecting CSS...")
    css_parts = [extract_inline_css(html)]
    for css_url in extract_stylesheet_urls(html, url):
        try:
            css_parts.append(fetch(css_url))
            print(f"  + {css_url[:70]}")
        except Exception:
            pass
    css_text = " ".join(css_parts)

    colors = extract_colors(css_text)
    fonts = extract_fonts(html, css_text)
    scheme = detect_scheme(css_text, html)

    print(f"  Colors — {len(colors['frequent_hex'])} direct hex, {len(colors['custom_properties'])} custom props")
    print(f"  Fonts  — {fonts or 'none detected'}")
    print(f"  Scheme — {scheme}")

    print("\nGenerating north star via Claude...")
    try:
        result = generate_north_star(url, site_name, colors, fonts, scheme, page_title, meta_desc)
    except Exception as e:
        print(f"Claude error: {e}")
        sys.exit(1)

    entry = {
        "id": slug(site_name),
        "url": url,
        "siteName": site_name,
        "colorScheme": result.get("colorScheme", scheme),
        "colors": result.get("namedColors", []),
        "fonts": result.get("fonts", fonts),
        "northStar": result.get("northStar", ""),
        "source": "extracted",
        "createdAt": datetime.datetime.now().isoformat(),
    }

    print(f"\n  North star: {entry['northStar']}")
    print(f"  Colors:     {[c['name'] for c in entry['colors']]}")
    print(f"  Fonts:      {entry['fonts']}")

    lib = load_library()
    existing = [i for i, s in enumerate(lib["styles"]) if s.get("url") == url]

    if existing:
        if args.update:
            lib["styles"][existing[0]] = entry
            print(f"\nUpdated existing entry for {url}.")
        else:
            print(f"\nEntry for {url} already exists. Use --update to overwrite.")
            sys.exit(0)
    else:
        lib["styles"].append(entry)
        print(f"\nAdded to library.")

    save_library(lib)
    print(f"Library now has {lib['count']} entries → {LIBRARY}")


if __name__ == "__main__":
    main()
