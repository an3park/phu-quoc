#!/usr/bin/env python3
"""Fetch live Agoda rates for Phu Quoc hotels.

Default stay: 2026-10-19 → 2026-10-25, 2 adults, 1 room, USD.
Other OTAs (Booking, Expedia, Hotels.com, brand sites) typically block
non-browser clients; Agoda's GetSecondaryData endpoint currently returns
dated room rates.

Usage:
    python3 scripts/fetch_agoda_prices.py
    python3 scripts/fetch_agoda_prices.py --checkin 2026-10-19 --checkout 2026-10-25
"""

from __future__ import annotations

import argparse
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


def nights(checkin: str, checkout: str) -> int:
    a = datetime.strptime(checkin, "%Y-%m-%d")
    b = datetime.strptime(checkout, "%Y-%m-%d")
    n = (b - a).days
    if n < 1:
        raise ValueError("checkout must be after checkin")
    return n


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    return s


def warmup(s: requests.Session, checkin: str, checkout: str) -> None:
    url = (
        f"https://www.agoda.com/search?city={AGODA_CITY_ID}"
        f"&checkIn={checkin}&checkOut={checkout}&rooms=1&adults=2&currency=USD"
    )
    s.get(url, timeout=40)


def fetch_property(s: requests.Session, hotel_id: int, checkin: str, los: int) -> dict:
    url = (
        "https://www.agoda.com/api/cronos/property/BelowFoldParams/GetSecondaryData"
        f"?checkIn={checkin}&los={los}&adults=2&rooms=1&currency=USD"
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


def parse_property(data: dict, catalog: dict, checkin: str, checkout: str, los: int) -> dict:
    info = data.get("hotelInfo") or {}
    sc = data.get("hotelSearchCriteria") or {}
    rg = data.get("roomGridData") or {}
    rooms = rg.get("masterRooms") or []
    taxes_global = (rg.get("taxesAndSurcharges") or {}).get("title")
    addr = info.get("address") or {}
    cheapest = None
    offers = []
    for mr in rooms:
        for room in mr.get("rooms") or []:
            ip = (room.get("inclusivePrice") or {}).get("display")
            ep = (room.get("exclusivePrice") or {}).get("display")
            tp = (room.get("totalPrice") or {}).get("display")
            pricing = room.get("pricing") or {}
            ds = (pricing.get("displaySummary") or {}).get("perRoomPerNight") or {}
            pb = (pricing.get("displaySummary") or {}).get("perBook") or {}
            if ip is None:
                ip = (ds.get("displayTotal") or {}).get("allInclusive")
            if ep is None:
                ep = (ds.get("displayTotal") or {}).get("exclusive")
            if tp is None:
                tp = (pb.get("displayTotal") or {}).get("allInclusive")
            if ip is None:
                continue
            offer = {
                "room_type": room.get("name") or mr.get("name"),
                "breakfast": bool(room.get("isBreakfastIncluded")),
                "free_cancellation": bool(room.get("isFreeCancellation")),
                "nightly_usd_incl": float(ip),
                "nightly_usd_excl": float(ep) if ep is not None else None,
                "total_usd_incl": float(tp) if tp is not None else round(float(ip) * los, 2),
                "taxes": (room.get("taxesAndSurcharges") or {}).get("title") or taxes_global,
                "pay_later": (room.get("payLater") or {}).get("description"),
                "is_average_price": bool(room.get("isAveragePrice")),
                "occupancy": room.get("maxOccupancy") or mr.get("maxOccupancy"),
            }
            offers.append(offer)
            if cheapest is None or offer["nightly_usd_incl"] < cheapest["nightly_usd_incl"]:
                cheapest = offer
    star = info.get("starRating")
    star_val = star.get("value") if isinstance(star, dict) else star
    hid = sc.get("hotelId") or catalog["id"]
    rev = data.get("reviews") or {}
    demo = rev.get("demographic") or {}
    combined = rev.get("combinedReview") or {}
    guest_score = None
    raw_score = rev.get("score")
    if raw_score not in (None, ""):
        try:
            guest_score = float(raw_score)
        except (TypeError, ValueError):
            guest_score = None
    if guest_score is None and isinstance(combined.get("score"), dict):
        try:
            guest_score = float(combined["score"].get("score"))
        except (TypeError, ValueError):
            guest_score = None
    grades: dict[str, float] = {}
    for g in demo.get("grades") or []:
        if g.get("id") is not None and g.get("score") is not None:
            grades[str(g["id"])] = float(g["score"])
    for g in combined.get("grades") or []:
        gid = g.get("id")
        if gid and g.get("score") is not None and str(gid) not in grades:
            grades[str(gid)] = float(g["score"])
    reviews_count = rev.get("reviewsCount")
    if reviews_count is None and isinstance(combined.get("score"), dict):
        reviews_count = combined["score"].get("reviewCount")
    return {
        "name": info.get("englishName") or info.get("name") or catalog["name"],
        "catalog_name": catalog["name"],
        "hotel_id": hid,
        "popularity": catalog.get("popularity"),
        "district": catalog.get("district") or addr.get("areaName"),
        "area_agoda": addr.get("areaName"),
        "address": addr.get("full") or addr.get("address"),
        "star": star_val,
        "guest_score": guest_score,
        "reviews_count": reviews_count,
        "grades": grades,
        "status": "available" if cheapest else "no_rate",
        "cheapest": cheapest,
        "n_offers": len(offers),
        "url": (
            f"https://www.agoda.com/search?city={AGODA_CITY_ID}"
            f"&checkIn={checkin}&checkOut={checkout}&los={los}"
            f"&rooms=1&adults=2&currency=USD&selectedproperty={hid}"
        ),
        "source": "Agoda GetSecondaryData",
        "live_for_dates": True,
        "checkin": checkin,
        "checkout": checkout,
        "nights": los,
        "adults": 2,
        "rooms": 1,
        "currency": "USD",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--checkin", default="2026-10-19")
    p.add_argument("--checkout", default="2026-10-25")
    p.add_argument("--sleep", type=float, default=0.15)
    p.add_argument("--out", default=str(ROOT / "data" / "agoda-live.json"))
    args = p.parse_args()
    los = nights(args.checkin, args.checkout)
    s = session()
    warmup(s, args.checkin, args.checkout)
    results = []
    for i, hotel in enumerate(HOTELS, 1):
        try:
            raw = fetch_property(s, hotel["id"], args.checkin, los)
            rec = parse_property(raw, hotel, args.checkin, args.checkout, los)
            results.append(rec)
            price = (rec.get("cheapest") or {}).get("nightly_usd_incl")
            print(f"[{i}/{len(HOTELS)}] {rec['name']}: {price if price else 'NO RATE'}")
        except Exception as e:
            print(f"[{i}/{len(HOTELS)}] {hotel['name']}: ERROR {e}")
            results.append(
                {
                    "name": hotel["name"],
                    "hotel_id": hotel["id"],
                    "popularity": hotel.get("popularity"),
                    "district": hotel.get("district"),
                    "status": "error",
                    "error": str(e),
                    "checkin": args.checkin,
                    "checkout": args.checkout,
                }
            )
        time.sleep(args.sleep)
    payload = {
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "checkin": args.checkin,
        "checkout": args.checkout,
        "nights": los,
        "adults": 2,
        "rooms": 1,
        "currency": "USD",
        "hotels": results,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
