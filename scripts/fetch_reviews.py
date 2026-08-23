#!/usr/bin/env python3
"""Fetch guest-review scores and sample comments.

Agoda GetSecondaryData currently returns:
  - combined Agoda + Booking.com score (combinedReview)
  - Agoda-only score (reviews.score / demographic)
  - category grades (cleanliness, service, location, value, facilities)

ReviewComments mixes Agoda (provider 332) and Booking.com (3038).
Google / Tripadvisor / brand sites are collected separately (see data/reviews-external.json).

Usage:
    python3 scripts/fetch_reviews.py
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

COMMENTS_URL = "https://www.agoda.com/api/cronos/property/review/ReviewComments"
SECONDARY_URL = "https://www.agoda.com/api/cronos/property/BelowFoldParams/GetSecondaryData"

# Pull comment samples for these catalog ids (decision set + newly added).
COMMENT_IDS = {
    1624474,  # JW
    3648660,  # InterContinental
    34249576,  # New World
    21774297,  # Regent
    1624152,  # Fusion
    569108,  # Salinda
    625168,  # Vinpearl
    5442703,  # Radisson Blu
    2163073,  # Wyndham Grand
    14654959,  # Mövenpick Waverly
    1157572,  # Novotel
    70425,  # La Veranda
    1032420,  # Sheraton
    5972590,  # Premier Residences
    400217,  # Famiana
    2577124,  # Lahana
    3647146,  # Camia
    24356624,  # M Village
    56230219,  # Soul Boutique
    47021962,  # Grand Ocean Bay
    11081947,  # Paralia
    148661,  # Chen Sea
    96572,  # Cassia
    21967772,  # Ocean Bay
}


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    return s


def warmup(s: requests.Session) -> None:
    s.get(
        f"https://www.agoda.com/search?city={AGODA_CITY_ID}"
        "&checkIn=2026-10-19&checkOut=2026-10-25&rooms=1&adults=2&currency=USD",
        timeout=40,
    )


def fetch_secondary(s: requests.Session, hotel_id: int) -> dict:
    url = (
        f"{SECONDARY_URL}?checkIn=2026-10-19&los=6&adults=2&rooms=1"
        f"&currency=USD&locale=en-us&childs=0&hotel_id={hotel_id}&all=false"
    )
    r = s.get(
        url,
        headers={
            "Accept": "application/json",
            "Referer": f"https://www.agoda.com/?hotel_id={hotel_id}",
            "Origin": "https://www.agoda.com",
        },
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def fetch_comments(s: requests.Session, hotel_id: int, sorting: int, page_size: int = 8) -> list[dict]:
    payload = {
        "hotelId": hotel_id,
        "providerId": 332,
        "demographicId": 0,
        "pageNo": 1,
        "pageSize": page_size,
        "sorting": sorting,
        "reviewProviderIds": [332, 3038],
        "isReviewPage": False,
        "isCrawlablePage": True,
        "paginationSize": 1,
    }
    r = s.post(
        COMMENTS_URL,
        json=payload,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Referer": f"https://www.agoda.com/?hotel_id={hotel_id}",
            "Origin": "https://www.agoda.com",
        },
        timeout=60,
    )
    r.raise_for_status()
    data = r.json() or {}
    out = []
    for c in data.get("comments") or []:
        info = c.get("reviewerInfo") or {}
        text = " ".join(
            x for x in (c.get("reviewTitle"), c.get("reviewComments"), c.get("reviewPositives"), c.get("reviewNegatives")) if x
        ).strip()
        if not text:
            continue
        out.append(
            {
                "source": c.get("reviewProviderText") or "Agoda",
                "rating": c.get("rating"),
                "date": c.get("formattedReviewDate") or c.get("reviewDate"),
                "title": c.get("reviewTitle"),
                "text": (c.get("reviewComments") or "")[:600],
                "positives": (c.get("reviewPositives") or "")[:400],
                "negatives": (c.get("reviewNegatives") or "")[:400],
                "group": info.get("reviewGroupName"),
                "country": info.get("countryName"),
                "room": info.get("roomTypeName"),
            }
        )
    return out


def grades_map(grades: list | None) -> dict:
    out = {}
    for g in grades or []:
        gid = g.get("id")
        if gid:
            out[gid] = g.get("score")
    return out


def parse_reviews(data: dict, catalog: dict) -> dict:
    info = data.get("hotelInfo") or {}
    rev = data.get("reviews") or {}
    comb = (rev.get("combinedReview") or {}).get("score") or {}
    demo = rev.get("demographic") or {}
    star = info.get("starRating")
    star_val = star.get("value") if isinstance(star, dict) else star
    name = info.get("englishName") or info.get("name") or catalog["name"]
    providers = []
    for p in (rev.get("combinedReview") or {}).get("providers") or []:
        n = p.get("logoName") or p.get("logoAltText")
        if n:
            providers.append(n)
    return {
        "name": name,
        "catalog_name": catalog["name"],
        "hotel_id": catalog["id"],
        "popularity": catalog.get("popularity"),
        "district": catalog.get("district"),
        "star": star_val,
        "agoda_score": _num(rev.get("score")),
        "agoda_count": rev.get("reviewsCount"),
        "agoda_label": rev.get("scoreText"),
        "combined_score": comb.get("score"),
        "combined_count": comb.get("reviewCount"),
        "combined_comments": comb.get("reviewCommentsCount"),
        "combined_label": comb.get("scoreText"),
        "combined_providers": providers,
        "agoda_only_count": demo.get("count"),
        "grades": grades_map(comb.get("grades") or demo.get("grades")),
        "score_distribution": demo.get("scoreDistribution") or [],
        "city_average_note": demo.get("cityAverageText"),
    }


def _num(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main() -> int:
    s = session()
    warmup(s)
    hotels = []
    for i, hotel in enumerate(HOTELS, 1):
        try:
            raw = fetch_secondary(s, hotel["id"])
            rec = parse_reviews(raw, hotel)
            if hotel["id"] in COMMENT_IDS:
                rec["comments_recent"] = fetch_comments(s, hotel["id"], sorting=1, page_size=6)
                time.sleep(0.12)
                rec["comments_low"] = fetch_comments(s, hotel["id"], sorting=3, page_size=6)
            else:
                rec["comments_recent"] = []
                rec["comments_low"] = []
            hotels.append(rec)
            print(
                f"[{i}/{len(HOTELS)}] {rec['name']}: "
                f"Agoda {rec['agoda_score']} ({rec['agoda_count']}) "
                f"combined {rec['combined_score']} ({rec['combined_count']})"
            )
        except Exception as e:
            print(f"[{i}/{len(HOTELS)}] {hotel['name']}: ERROR {e}")
            hotels.append(
                {
                    "name": hotel["name"],
                    "hotel_id": hotel["id"],
                    "status": "error",
                    "error": str(e),
                }
            )
        time.sleep(0.15)
    payload = {
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "note": "Agoda GetSecondaryData + ReviewComments. combined_score mixes Agoda and Booking.com.",
        "hotels": hotels,
    }
    out = ROOT / "data" / "reviews-agoda.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
