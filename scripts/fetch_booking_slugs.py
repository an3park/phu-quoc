#!/usr/bin/env python3
"""Resolve Booking.com hotel slugs via DuckDuckGo HTML search.

Booking.com itself returns AWS WAF 202 for non-browser clients.
DuckDuckGo regularly indexes the canonical /hotel/vn/{slug}.html pages.

Usage:
    python3 scripts/fetch_booking_slugs.py
"""

from __future__ import annotations

import html as html_lib
import re
import sys
import time
import urllib.parse
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hotels_catalog import HOTELS  # noqa: E402

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

SLUG_RE = re.compile(
    r"https?://(?:www\.)?booking\.com/hotel/vn/([a-z0-9][a-z0-9-]{2,})",
    re.I,
)

STOP = {
    "phu",
    "quoc",
    "phú",
    "quốc",
    "hotel",
    "resort",
    "spa",
    "and",
    "the",
    "by",
    "ihg",
    "a",
    "of",
    "at",
}


def tokens(name: str) -> set[str]:
    cleaned = re.sub(r"[^a-z0-9]+", " ", name.lower())
    return {t for t in cleaned.split() if t and t not in STOP and len(t) > 2}


def slug_tokens(slug: str) -> set[str]:
    return {t for t in slug.lower().split("-") if t and t not in STOP and len(t) > 2}


def score_slug(name: str, slug: str) -> float:
    nt = tokens(name)
    st = slug_tokens(slug)
    if not nt or not st:
        return 0.0
    overlap = nt & st
    # require at least one distinctive token
    if not overlap:
        return 0.0
    return len(overlap) / len(nt) + 0.15 * len(overlap) / max(len(st), 1)


def extract_slugs(page: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for raw in SLUG_RE.findall(html_lib.unescape(page)):
        slug = raw.lower().split(".")[0].strip("-")
        if not slug or slug in seen:
            continue
        seen.add(slug)
        found.append(slug)
    return found


def ddg_search(session: requests.Session, query: str) -> str:
    r = session.post(
        "https://html.duckduckgo.com/html/",
        data={"q": query},
        timeout=30,
        headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"},
    )
    r.raise_for_status()
    return r.text


def pick_slug(name: str, slugs: list[str]) -> tuple[str | None, float, list[tuple[str, float]]]:
    ranked = sorted(((s, score_slug(name, s)) for s in slugs), key=lambda x: -x[1])
    if not ranked:
        return None, 0.0, []
    best, score = ranked[0]
    if score < 0.25:
        return None, score, ranked[:5]
    return best, score, ranked[:5]


def resolve_one(session: requests.Session, hotel: dict) -> dict:
    name = hotel["name"]
    queries = [
        f'site:booking.com/hotel/vn {name} Phu Quoc',
        f'site:www.booking.com/hotel/vn {name}',
    ]
    all_slugs: list[str] = []
    for q in queries:
        html = ddg_search(session, q)
        all_slugs.extend(extract_slugs(html))
        if all_slugs:
            break
        time.sleep(0.4)
    # unique, preserve order
    uniq: list[str] = []
    seen: set[str] = set()
    for s in all_slugs:
        if s not in seen:
            seen.add(s)
            uniq.append(s)
    slug, score, ranked = pick_slug(name, uniq)
    return {
        "id": hotel["id"],
        "name": name,
        "slug": slug,
        "score": round(score, 3),
        "candidates": ranked,
    }


def main() -> int:
    session = requests.Session()
    results = []
    missing = []
    for i, hotel in enumerate(HOTELS, 1):
        rec = resolve_one(session, hotel)
        results.append(rec)
        mark = rec["slug"] or "MISSING"
        print(f"{i:02d}/{len(HOTELS)} {mark:50s}  {rec['score']:.2f}  {hotel['name']}")
        if rec["slug"] is None:
            missing.append(rec)
        time.sleep(0.55)
    print("\n--- missing ---")
    for rec in missing:
        print(rec["id"], rec["name"], rec["candidates"][:4])
    out = ROOT / "data" / "booking-slugs-raw.json"
    import json

    payload = {str(r["id"]): r for r in results}
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(results)} hotels, {len(missing)} missing)")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
