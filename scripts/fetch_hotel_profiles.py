#!/usr/bin/env python3
"""Fetch Agoda guest scores, grades, and key features for catalog hotels.

Writes data/hotel-profiles-raw.json used by build_tables.py for ratings.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hotels_catalog import AGODA_CITY_ID, HOTELS  # noqa: E402

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    return s


def fetch(s: requests.Session, hotel_id: int) -> dict:
    url = (
        "https://www.agoda.com/api/cronos/property/BelowFoldParams/GetSecondaryData"
        f"?checkIn=2026-10-19&los=6&adults=2&rooms=1&currency=USD"
        f"&locale=en-us&childs=0&hotel_id={hotel_id}&all=false"
        "&isHostPropertiesEnabled=true"
    )
    r = s.get(
        url,
        headers={
            "Accept": "application/json",
            "Referer": f"https://www.agoda.com/?hotel_id={hotel_id}",
            "Origin": "https://www.agoda.com",
            "CR-Currency-Code": "USD",
            "AG-Language-Locale": "en-us",
        },
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def extract_features(data: dict) -> tuple[list[str], list[str]]:
    names: list[str] = []
    for group in ((data.get("aboutHotel") or {}).get("featureGroups") or []):
        for f in group.get("feature") or []:
            if f.get("available") and f.get("name"):
                names.append(f["name"])
    prioritized = [
        n
        for n in names
        if any(
            k in n.lower()
            for k in (
                "beach",
                "pool",
                "spa",
                "villa",
                "kids",
                "restaurant",
                "bar",
                "gym",
                "fitness",
                "transfer",
                "garden",
                "snorkel",
                "dive",
                "tennis",
                "golf",
                "infinity",
                "private",
                "yoga",
                "water park",
                "sauna",
                "jacuzzi",
                "hot tub",
                "kitchen",
            )
        )
    ]
    seen: set[str] = set()
    out: list[str] = []
    for n in prioritized + names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out[:18], names


def extract_review(data: dict) -> dict:
    rev = data.get("reviews") or {}
    demo = rev.get("demographic") or {}
    combined = rev.get("combinedReview") or {}
    score = None
    try:
        if rev.get("score") not in (None, ""):
            score = float(rev.get("score"))
    except (TypeError, ValueError):
        score = None
    if score is None and isinstance(combined.get("score"), dict):
        try:
            score = float(combined["score"].get("score"))
        except (TypeError, ValueError):
            score = None
    grades: dict[str, float] = {}
    for g in demo.get("grades") or []:
        if g.get("id") is not None and g.get("score") is not None:
            grades[str(g["id"])] = float(g["score"])
    for g in combined.get("grades") or []:
        gid = g.get("id")
        if gid and g.get("score") is not None and str(gid) not in grades:
            grades[str(gid)] = float(g["score"])
    return {
        "guest_score": score,
        "score_text": rev.get("scoreText"),
        "reviews_count": rev.get("reviewsCount")
        or (combined.get("score") or {}).get("reviewCount"),
        "grades": grades,
    }


def parse(data: dict, catalog: dict) -> dict:
    info = data.get("hotelInfo") or {}
    addr = info.get("address") or {}
    star = info.get("starRating")
    star_val = star.get("value") if isinstance(star, dict) else star
    rev = extract_review(data)
    feats, all_feats = extract_features(data)
    restaurants = data.get("restaurantOnSite") or []
    bf = data.get("breakfastInformation") or {}
    love = [
        f.get("text")
        for f in ((data.get("featuresYouLove") or {}).get("features") or [])
        if f.get("text")
    ]
    overview = (((data.get("aboutHotel") or {}).get("hotelDesc") or {}).get("overview") or "")
    return {
        "hotel_id": catalog["id"],
        "name": info.get("englishName") or info.get("name") or catalog["name"],
        "catalog_name": catalog["name"],
        "district": catalog.get("district") or addr.get("areaName"),
        "star": star_val,
        "popularity": catalog.get("popularity"),
        **rev,
        "key_features": feats[:12],
        "features_you_love": love[:8],
        "beachfront": any(
            "beachfront" in n.lower() or n.lower() == "private beach" for n in all_feats
        ),
        "has_spa": any(n.lower() == "spa" or n.lower().startswith("spa ") for n in all_feats),
        "has_kids_club": any("kids" in n.lower() or "children" in n.lower() for n in all_feats),
        "has_pool": any("pool" in n.lower() for n in all_feats),
        "restaurants": [
            {"name": r.get("name"), "cuisines": r.get("cuisines"), "servings": r.get("servings")}
            for r in restaurants[:6]
        ],
        "breakfast_cuisines": bf.get("cuisines") or [],
        "overview_snippet": overview[:400],
    }


def main() -> int:
    # merge extra hotels from live snapshot (Anna* etc.)
    live_path = ROOT / "data" / "agoda-live.json"
    by_id = {h["id"]: h for h in HOTELS}
    if live_path.exists():
        live = json.loads(live_path.read_text(encoding="utf-8"))
        for h in live.get("hotels") or []:
            hid = h.get("hotel_id")
            if hid and hid not in by_id:
                by_id[hid] = {
                    "id": hid,
                    "name": h.get("catalog_name") or h.get("name"),
                    "popularity": h.get("popularity") or "mid",
                    "district": h.get("district"),
                }

    s = session()
    s.get(
        f"https://www.agoda.com/search?city={AGODA_CITY_ID}"
        "&checkIn=2026-10-19&checkOut=2026-10-25&rooms=1&adults=2&currency=USD",
        timeout=40,
    )
    results = []
    errors = []
    items = list(by_id.values())
    for i, cat in enumerate(items, 1):
        try:
            rec = parse(fetch(s, cat["id"]), cat)
            results.append(rec)
            print(
                f"[{i}/{len(items)}] {rec['name'][:42]:42} "
                f"score={rec.get('guest_score')} n={rec.get('reviews_count')}"
            )
        except Exception as e:
            errors.append({"hotel_id": cat["id"], "name": cat["name"], "error": str(e)})
            print(f"[{i}/{len(items)}] ERROR {cat['name']}: {e}")
        time.sleep(0.2)

    out = ROOT / "data" / "hotel-profiles-raw.json"
    payload = {
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "Agoda GetSecondaryData reviews + aboutHotel features",
        "hotels": results,
        "errors": errors,
    }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out} hotels={len(results)} errors={len(errors)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
