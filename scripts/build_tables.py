#!/usr/bin/env python3
"""Build CSV + Markdown comparison tables from Agoda snapshot + hotel profiles.

Sorts by composite rating (guest reviews, category grades, breakfast, stars).
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hotels_catalog import HOTELS  # noqa: E402
from hotel_profiles import (  # noqa: E402
    BREAKFAST_NOTES,
    breakfast_quality_for,
    description_for,
)

CATALOG_BY_ID = {h["id"]: h for h in HOTELS}

POP_RU = {
    "popular": "популярный",
    "mid": "средний",
    "lesser-known": "менее известный",
}

DISTRICT_NOTE = {
    "Bai Khem": "восток / юг — спокойнее море в октябре",
    "Long Beach": "запад, закаты, инфраструктура",
    "Bai Dai": "север, VinWonders / Grand World",
    "Bai Dai / Starbay": "север, Starbay / гольф",
    "Ong Lang": "тихий запад, севернее Лонг-Бич",
    "Vung Bau": "северо-запад, уединённые виллы",
    "Duong Dong": "город, ночной рынок",
    "Ham Ninh": "восток, рыбацкая деревня",
    "An Thoi": "юг, Sunset Town / канатная дорога",
}

RATING_METHOD = (
    "Сводный рейтинг /10: отзывы гостей Agoda+Booking (40%, с лёгким сжатием к среднему острова "
    "при малом числе отзывов), качество завтрака (15%), удобства (12%), чистота (10%), сервис (10%), "
    "локация (8%), value (5%), звёзды (5%). Веса перенормируются, если части оценок нет. "
    "Завтрак: Agoda foodDining при наличии + кураторская оценка F&B "
    "(Salinda sparkling wine, Regent Rice Market, InterContinental Sora & Umi и т.д.)."
)


def load_snapshot(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {
            "fetched_at_utc": None,
            "checkin": "2026-10-19",
            "checkout": "2026-10-25",
            "nights": 6,
            "hotels": data,
        }
    return data


def load_profiles(path: Path) -> dict[int, dict]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    hotels = data.get("hotels") if isinstance(data, dict) else data
    out: dict[int, dict] = {}
    for h in hotels or []:
        hid = h.get("hotel_id")
        if hid is not None:
            out[int(hid)] = h
    return out


def cheapest(h: dict) -> dict:
    return h.get("cheapest") or {}


def nightly(h: dict):
    ch = cheapest(h)
    return ch.get("nightly_usd_incl") or ch.get("nightly_incl")


def shrink_guest_score(score: float | None, reviews_count) -> float | None:
    """Mild Bayesian shrink toward island average for tiny samples."""
    if score is None:
        return None
    try:
        n = float(reviews_count or 0)
    except (TypeError, ValueError):
        n = 0.0
    prior, prior_n = 8.7, 80.0
    if n <= 0:
        return float(score)
    return (float(score) * n + prior * prior_n) / (n + prior_n)


def composite_rating(
    guest_score: float | None,
    breakfast: float | None,
    grades: dict,
    star: float | None,
    reviews_count=None,
) -> float | None:
    guest_for_rating = shrink_guest_score(guest_score, reviews_count)
    parts: list[tuple[float, float]] = []
    if guest_for_rating is not None:
        parts.append((float(guest_for_rating), 0.40))
    if breakfast is not None:
        parts.append((float(breakfast), 0.15))
    for key, w in (
        ("facilities", 0.12),
        ("cleanliness", 0.10),
        ("staffPerformance", 0.10),
        ("location", 0.08),
        ("valueForMoney", 0.05),
    ):
        if grades.get(key) is not None:
            parts.append((float(grades[key]), w))
    if star is not None and float(star) > 0:
        parts.append((min(float(star), 5.0) * 2.0, 0.05))
    if not parts:
        return None
    tw = sum(w for _, w in parts)
    return round(sum(v * w for v, w in parts) / tw, 2)


def short_features(prof: dict) -> str:
    love = [x for x in (prof.get("features_you_love") or []) if x]
    keys = [x for x in (prof.get("key_features") or []) if x]
    tags: list[str] = []
    seen_norm: set[str] = set()

    def add(x: str) -> None:
        norm = x.strip().lower()
        if not norm or norm in seen_norm:
            return
        # collapse spa / spa/sauna duplicates
        if norm.startswith("spa") and any(s.startswith("spa") for s in seen_norm):
            return
        seen_norm.add(norm)
        tags.append(x)

    if prof.get("beachfront"):
        add("beachfront")
    for x in love[:3]:
        add(x)
    for x in keys:
        xl = x.lower()
        if any(
            k in xl
            for k in ("private beach", "kids club", "spa", "villa", "yoga", "water park")
        ):
            add(x)
        if len(tags) >= 6:
            break
    return ", ".join(tags[:6]) if tags else "—"


def enrich(h: dict, profiles: dict[int, dict]) -> dict:
    hid = h.get("hotel_id")
    cat = CATALOG_BY_ID.get(hid) or {}
    ch = cheapest(h)
    n = nightly(h)
    prof = profiles.get(int(hid)) if hid is not None else {}
    grades = dict(prof.get("grades") or {})
    # also accept grades embedded in live snapshot
    if not grades and h.get("grades"):
        grades = dict(h.get("grades") or {})
    guest = prof.get("guest_score")
    if guest is None:
        guest = h.get("guest_score")
    if guest is not None:
        guest = float(guest)
    reviews_count = prof.get("reviews_count") or h.get("reviews_count")
    food = grades.get("foodDining")
    breakfast_q = breakfast_quality_for(int(hid), food if food is not None else None) if hid else None
    star = h.get("star") if h.get("star") is not None else prof.get("star")
    if isinstance(star, (int, float)) and float(star) <= 0:
        star = None
    rating = composite_rating(
        guest,
        breakfast_q,
        grades,
        star if isinstance(star, (int, float)) else None,
        reviews_count,
    )
    desc = description_for(int(hid), h.get("catalog_name") or h.get("name") or "") if hid else ""
    bf_note = BREAKFAST_NOTES.get(int(hid), "") if hid else ""
    return {
        **h,
        "popularity": h.get("popularity") or cat.get("popularity") or "mid",
        "district": h.get("district") or cat.get("district") or h.get("area") or h.get("area_agoda") or "",
        "nightly_incl": n,
        "nightly_excl": ch.get("nightly_usd_excl") or ch.get("nightly_excl"),
        "total6": ch.get("total_usd_incl") or ch.get("total6_incl"),
        "room": ch.get("room_type"),
        "breakfast": ch.get("breakfast") if "breakfast" in ch else ch.get("breakfast_included"),
        "free_cancel": ch.get("free_cancellation") if "free_cancellation" in ch else ch.get("free_cancel"),
        "taxes": ch.get("taxes"),
        "occupancy": ch.get("occupancy"),
        "guest_score": guest,
        "reviews_count": reviews_count,
        "grades": grades,
        "breakfast_quality": breakfast_q,
        "breakfast_note": bf_note,
        "rating": rating,
        "description": desc,
        "features_short": short_features(prof) if prof else "—",
        "star": star,
    }


def usd(n) -> str:
    if n is None:
        return "—"
    return f"${n:,.2f}"


def yn(v) -> str:
    if v is True:
        return "да"
    if v is False:
        return "нет"
    return "—"


def fmt_score(n, digits: int = 1) -> str:
    if n is None:
        return "—"
    return f"{float(n):.{digits}f}"


def fmt_breakfast_col(r: dict) -> str:
    q = r.get("breakfast_quality")
    if q is None:
        return "—"
    note = r.get("breakfast_note") or ""
    base = fmt_score(q)
    if note:
        return f"{base} ({note})"
    return base


def md_escape(s: str) -> str:
    return (s or "").replace("|", "/").replace("\n", " ")


def md_table(rows: list[dict], *, compact: bool = False) -> str:
    if compact:
        headers = [
            "Рейтинг",
            "Отель",
            "Район",
            "★",
            "Отзывы",
            "Завтрак /10",
            "Ночь",
            "Фичи",
        ]
        lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
        for r in rows:
            lines.append(
                "| "
                + " | ".join(
                    [
                        fmt_score(r.get("rating"), 2),
                        md_escape(r.get("name") or r.get("catalog_name") or ""),
                        r.get("district") or "",
                        str(r.get("star") or "—"),
                        fmt_score(r.get("guest_score")),
                        fmt_breakfast_col(r),
                        usd(r.get("nightly_incl")),
                        md_escape((r.get("features_short") or "—")[:80]),
                    ]
                )
                + " |"
            )
        return "\n".join(lines) + "\n"

    headers = [
        "Рейтинг",
        "Отель",
        "Район",
        "★",
        "Отзывы",
        "Завтрак /10",
        "В тарифе",
        "Ночь, USD",
        "6 ночей",
        "Номер",
        "Описание / фичи",
        "Отмена",
        "Статус",
    ]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for r in rows:
        status = "есть места" if r.get("status") == "available" and r.get("nightly_incl") else "нет тарифа на даты"
        desc = r.get("description") or ""
        feats = r.get("features_short") or ""
        blob = desc if not feats or feats == "—" else f"{desc} · {feats}"
        lines.append(
            "| "
            + " | ".join(
                [
                    fmt_score(r.get("rating"), 2),
                    md_escape(r.get("name") or r.get("catalog_name") or ""),
                    r.get("district") or "",
                    str(r.get("star") or "—"),
                    fmt_score(r.get("guest_score")),
                    fmt_breakfast_col(r),
                    yn(r.get("breakfast")),
                    usd(r.get("nightly_incl")),
                    usd(r.get("total6")),
                    md_escape(r.get("room") or "—"),
                    md_escape(blob),
                    yn(r.get("free_cancel")),
                    status,
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def sort_by_rating(rows: list[dict]) -> list[dict]:
    return sorted(
        rows,
        key=lambda r: (
            r.get("rating") is None,
            -(r.get("rating") or 0),
            -(r.get("guest_score") or 0),
            r.get("nightly_incl") is None,
            r.get("nightly_incl") or 9e9,
        ),
    )


def write_csv(path: Path, rows: list[dict], meta: dict) -> None:
    fields = [
        "rating",
        "guest_score",
        "reviews_count",
        "breakfast_quality",
        "breakfast_note",
        "breakfast_included",
        "name",
        "district",
        "star",
        "popularity",
        "description",
        "features",
        "nightly_usd_incl",
        "nightly_usd_excl",
        "total_6_nights_usd_incl",
        "room_type",
        "free_cancellation",
        "taxes",
        "status",
        "hotel_id",
        "url",
        "checkin",
        "checkout",
        "grade_cleanliness",
        "grade_facilities",
        "grade_location",
        "grade_service",
        "grade_value",
        "grade_food",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            g = r.get("grades") or {}
            w.writerow(
                {
                    "rating": r.get("rating"),
                    "guest_score": r.get("guest_score"),
                    "reviews_count": r.get("reviews_count"),
                    "breakfast_quality": r.get("breakfast_quality"),
                    "breakfast_note": r.get("breakfast_note"),
                    "breakfast_included": r.get("breakfast"),
                    "name": r.get("name"),
                    "district": r.get("district"),
                    "star": r.get("star"),
                    "popularity": r.get("popularity"),
                    "description": r.get("description"),
                    "features": r.get("features_short"),
                    "nightly_usd_incl": r.get("nightly_incl"),
                    "nightly_usd_excl": r.get("nightly_excl"),
                    "total_6_nights_usd_incl": r.get("total6"),
                    "room_type": r.get("room"),
                    "free_cancellation": r.get("free_cancel"),
                    "taxes": r.get("taxes"),
                    "status": r.get("status"),
                    "hotel_id": r.get("hotel_id"),
                    "url": r.get("url"),
                    "checkin": meta.get("checkin"),
                    "checkout": meta.get("checkout"),
                    "grade_cleanliness": g.get("cleanliness"),
                    "grade_facilities": g.get("facilities"),
                    "grade_location": g.get("location"),
                    "grade_service": g.get("staffPerformance"),
                    "grade_value": g.get("valueForMoney"),
                    "grade_food": g.get("foodDining"),
                }
            )


def write_profiles_clean(path: Path, rows: list[dict]) -> None:
    payload = []
    for r in rows:
        payload.append(
            {
                "hotel_id": r.get("hotel_id"),
                "name": r.get("name"),
                "district": r.get("district"),
                "star": r.get("star"),
                "rating": r.get("rating"),
                "guest_score": r.get("guest_score"),
                "reviews_count": r.get("reviews_count"),
                "breakfast_quality": r.get("breakfast_quality"),
                "breakfast_note": r.get("breakfast_note") or None,
                "description": r.get("description"),
                "features": r.get("features_short"),
                "grades": r.get("grades") or {},
            }
        )
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    src = ROOT / "data" / "agoda-live.json"
    if not src.exists():
        src = ROOT / "data" / "agoda-live-raw.json"
    profiles = load_profiles(ROOT / "data" / "hotel-profiles-raw.json")
    meta = load_snapshot(src)
    rows = [enrich(h, profiles) for h in meta["hotels"]]
    available = sort_by_rating([r for r in rows if r.get("nightly_incl")])
    missing = sort_by_rating([r for r in rows if not r.get("nightly_incl")])
    rows = available + missing

    csv_path = ROOT / "data" / "comparison.csv"
    md_path = ROOT / "data" / "comparison.md"
    write_csv(csv_path, rows, meta)
    write_profiles_clean(ROOT / "data" / "hotel-profiles.json", rows)

    popular = [r for r in available if r.get("popularity") == "popular"]
    lesser = [r for r in available if r.get("popularity") == "lesser-known"]

    by_district: dict[str, list] = {}
    for r in available:
        by_district.setdefault(r.get("district") or "другое", []).append(r)

    top10 = available[:10]

    parts = [
        "# Сравнение отелей Фукуок (Phu Quoc)",
        "",
        f"- Заезд: **{meta.get('checkin')}**, выезд: **{meta.get('checkout')}** ({meta.get('nights') or 6} ночей)",
        "- 2 взрослых, 1 номер",
        "- Цены: Agoda, **с налогами и сборами**, USD, самый дешёвый доступный номер",
        "- Снято: 22 августа 2026 (цены); отзывы/фичи Agoda — август 2026",
        f"- {RATING_METHOD}",
        "- Таблица отсортирована по **сводному рейтингу** (выше = лучше)",
        "",
        "## Топ-10 по рейтингу (с ценой на даты)",
        "",
        md_table(top10, compact=True),
        "",
        "## Все отели с тарифом (по рейтингу)",
        "",
        md_table(available),
        "",
        "## Популярные",
        "",
        md_table(popular),
        "",
        "## Менее известные",
        "",
        md_table(lesser),
        "",
        "## По районам",
        "",
    ]
    for dist, items in sorted(
        by_district.items(),
        key=lambda kv: (-(kv[1][0].get("rating") or 0), kv[0]),
    ):
        note = DISTRICT_NOTE.get(dist, "")
        title = f"### {dist}" + (f" — {note}" if note else "")
        parts += [title, "", md_table(items), ""]

    if missing:
        missing_sorted = sort_by_rating(missing)
        parts += ["## Нет живого тарифа на эти даты (Agoda)", "", md_table(missing_sorted), ""]

    md_path.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {csv_path} ({len(rows)} rows)")
    print(f"Wrote {md_path}")
    print(f"Wrote {ROOT / 'data' / 'hotel-profiles.json'}")
    if available:
        print("Top by rating:")
        for r in available[:8]:
            print(
                f"  {r.get('rating'):.2f} | bf {r.get('breakfast_quality')} | "
                f"{r.get('guest_score')} | {r.get('name')[:40]} | ${r.get('nightly_incl')}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
