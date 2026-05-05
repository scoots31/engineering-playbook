#!/usr/bin/env python3
"""
Seed the design library from the Refero Styles API.
Pulls all style listings + full detail for each entry.
Saves to styles.json in this directory.

Usage: python seed.py
"""
import json
import os
import time
import urllib.request
import urllib.error

BASE = "https://styles.refero.design/api"
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.json")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def fetch_all_listings():
    entries = []
    page = 1
    while True:
        print(f"  Fetching page {page}...")
        data = get(f"{BASE}/styles?page={page}")
        batch = data.get("styles", [])
        entries.extend(batch)
        next_page = data.get("nextPage")
        if not next_page or next_page == page:
            break
        page = next_page
        time.sleep(0.4)
    return entries


def fetch_detail(style_id):
    try:
        return get(f"{BASE}/styles/{style_id}")
    except Exception:
        return None


def load_existing():
    if os.path.exists(OUTPUT):
        with open(OUTPUT) as f:
            return json.load(f)
    return {"source": "refero+extracted", "styles": []}


def main():
    print("Fetching Refero style listings...")
    listings = fetch_all_listings()
    print(f"Found {len(listings)} styles. Fetching full detail...\n")

    library = load_existing()
    existing_ids = {s.get("id") for s in library["styles"] if s.get("source") == "refero"}

    added = 0
    for i, listing in enumerate(listings):
        style_id = listing.get("id")
        site_name = listing.get("siteName", style_id)

        if style_id in existing_ids:
            print(f"  [{i+1}/{len(listings)}] {site_name} — already in library, skipping")
            continue

        detail = fetch_detail(style_id)
        entry = detail if detail else listing
        entry["source"] = "refero"
        library["styles"].append(entry)
        added += 1
        print(f"  [{i+1}/{len(listings)}] {site_name} ✓")
        time.sleep(0.3)

    library["count"] = len(library["styles"])
    with open(OUTPUT, "w") as f:
        json.dump(library, f, indent=2)

    print(f"\nDone. Added {added} new entries. Library total: {library['count']} styles.")
    print(f"Saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
