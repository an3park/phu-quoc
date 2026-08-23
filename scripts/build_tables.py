#!/usr/bin/env python3
"""Build CSV + Markdown comparison tables from a live Agoda snapshot."""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path

MONTHS_RU = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hotels_catalog import HOTELS  # noqa: E402

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


def cheapest(h: dict) -> dict:
    return h.get("cheapest") or {}


def nightly(h: dict):
    ch = cheapest(h)
    return ch.get("nightly_usd_incl") or ch.get("nightly_incl")


def enrich(h: dict) -> dict:
    hid = h.get("hotel_id")
    cat = CATALOG_BY_ID.get(hid) or {}
    ch = cheapest(h)
    n = nightly(h)
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


def md_table(rows: list[dict]) -> str:
    headers = [
        "Отель",
        "Район",
        "★",
        "Известность",
        "Ночь, USD (с налогами)",
        "6 ночей, USD",
        "Номер",
        "Завтрак",
        "Отмена",
        "Статус",
    ]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for r in rows:
        status = "есть места" if r.get("status") == "available" and r.get("nightly_incl") else "нет тарифа на даты"
        lines.append(
            "| "
            + " | ".join(
                [
                    r.get("name") or r.get("catalog_name") or "",
                    r.get("district") or "",
                    str(r.get("star") or "—"),
                    POP_RU.get(r.get("popularity"), r.get("popularity") or ""),
                    usd(r.get("nightly_incl")),
                    usd(r.get("total6")),
                    (r.get("room") or "—").replace("|", "/"),
                    yn(r.get("breakfast")),
                    yn(r.get("free_cancel")),
                    status,
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def write_csv(path: Path, rows: list[dict], meta: dict) -> None:
    fields = [
        "name",
        "district",
        "star",
        "popularity",
        "nightly_usd_incl",
        "nightly_usd_excl",
        "total_6_nights_usd_incl",
        "room_type",
        "breakfast",
        "free_cancellation",
        "taxes",
        "status",
        "hotel_id",
        "url",
        "checkin",
        "checkout",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(
                {
                    "name": r.get("name"),
                    "district": r.get("district"),
                    "star": r.get("star"),
                    "popularity": r.get("popularity"),
                    "nightly_usd_incl": r.get("nightly_incl"),
                    "nightly_usd_excl": r.get("nightly_excl"),
                    "total_6_nights_usd_incl": r.get("total6"),
                    "room_type": r.get("room"),
                    "breakfast": r.get("breakfast"),
                    "free_cancellation": r.get("free_cancel"),
                    "taxes": r.get("taxes"),
                    "status": r.get("status"),
                    "hotel_id": r.get("hotel_id"),
                    "url": r.get("url"),
                    "checkin": meta.get("checkin"),
                    "checkout": meta.get("checkout"),
                }
            )


def main() -> int:
    src = ROOT / "data" / "agoda-live.json"
    if not src.exists():
        src = ROOT / "data" / "agoda-live-raw.json"
    meta = load_snapshot(src)
    rows = [enrich(h) for h in meta["hotels"]]
    rows.sort(key=lambda r: (r.get("nightly_incl") is None, r.get("nightly_incl") or 9e9))

    csv_path = ROOT / "data" / "comparison.csv"
    md_path = ROOT / "data" / "comparison.md"
    write_csv(csv_path, rows, meta)

    fetched = meta.get("fetched_at_utc") or ""
    try:
        dt = datetime.fromisoformat(fetched.replace("Z", "+00:00"))
        snapshot_ru = f"{dt.day} {MONTHS_RU[dt.month]} {dt.year}"
    except (TypeError, ValueError):
        snapshot_ru = "23 августа 2026"

    available = [r for r in rows if r.get("nightly_incl")]
    missing = [r for r in rows if not r.get("nightly_incl")]
    popular = [r for r in available if r.get("popularity") == "popular"]
    lesser = [r for r in available if r.get("popularity") == "lesser-known"]

    by_district: dict[str, list] = {}
    for r in available:
        by_district.setdefault(r.get("district") or "другое", []).append(r)

    parts = [
        f"# Сравнение отелей Фукуок (Phu Quoc)",
        "",
        f"- Заезд: **{meta.get('checkin')}**, выезд: **{meta.get('checkout')}** ({meta.get('nights') or 6} ночей)",
        "- 2 взрослых, 1 номер",
        "- Цены: Agoda, **с налогами и сборами**, USD, самый дешёвый доступный номер",
        f"- Снято: {snapshot_ru}",
        "",
        "## Все отели по возрастанию цены",
        "",
        md_table(rows),
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
    for dist, items in sorted(by_district.items(), key=lambda kv: nightly(kv[1][0]) or 9e9):
        note = DISTRICT_NOTE.get(dist, "")
        title = f"### {dist}" + (f" — {note}" if note else "")
        parts += [title, "", md_table(items), ""]

    if missing:
        parts += ["## Нет живого тарифа на эти даты (Agoda)", "", md_table(missing), ""]

    md_path.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {csv_path} ({len(rows)} rows)")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
