#!/usr/bin/env python3
"""Build reviews CSV + ranking markdown from Agoda snapshot + external scores."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def to10(score, scale) -> float | None:
    if score is None or scale in (None, 0):
        return None
    return round(float(score) * (10.0 / float(scale)), 2)


def main() -> int:
    agoda = json.loads((ROOT / "data" / "reviews-agoda.json").read_text(encoding="utf-8"))
    ext = json.loads((ROOT / "data" / "reviews-external.json").read_text(encoding="utf-8"))
    ext_by_name = {h["name"]: h for h in ext.get("hotels") or []}

    rows = []
    for h in agoda.get("hotels") or []:
        g = h.get("grades") or {}
        row = {
            "name": h.get("name"),
            "district": h.get("district"),
            "star": h.get("star"),
            "agoda_score": h.get("agoda_score"),
            "agoda_count": h.get("agoda_count"),
            "combined_agoda_booking": h.get("combined_score"),
            "combined_count": h.get("combined_count"),
            "cleanliness": g.get("cleanliness"),
            "facilities": g.get("facilities"),
            "location": g.get("location"),
            "service": g.get("staffPerformance"),
            "value": g.get("valueForMoney"),
            "google_score_10": None,
            "google_count": None,
            "tripadvisor_score_10": None,
            "tripadvisor_count": None,
            "booking_score": None,
            "booking_count": None,
        }
        extra = ext_by_name.get(h.get("name") or "") or ext_by_name.get(h.get("catalog_name") or "")
        if extra is None:
            nm = (h.get("name") or "").lower()
            for k, v in ext_by_name.items():
                if k.lower() in nm or nm in k.lower():
                    extra = v
                    break
        if extra:
            for s in extra.get("sources") or []:
                site = (s.get("site") or "").lower()
                sc10 = to10(s.get("score"), s.get("scale") or 10)
                if site == "google":
                    row["google_score_10"] = sc10
                    row["google_count"] = s.get("count")
                elif site == "tripadvisor":
                    row["tripadvisor_score_10"] = sc10
                    row["tripadvisor_count"] = s.get("count")
                elif site == "booking.com":
                    row["booking_score"] = sc10
                    row["booking_count"] = s.get("count")
        rows.append(row)

    rows.sort(key=lambda r: (r.get("agoda_score") is None, -(r.get("agoda_score") or 0), -(r.get("agoda_count") or 0)))

    csv_path = ROOT / "data" / "reviews.csv"
    fields = list(rows[0].keys()) if rows else []
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    md = [
        "# Рейтинг отзывов (Agoda + Booking combined)",
        "",
        f"- Снято: {agoda.get('fetched_at_utc', '')[:10]}",
        "- Agoda `GetSecondaryData`: оценка и число отзывов; combined включает Booking.com, если площадка отдаёт.",
        "- Категории: чистота / сервис / локация / value / удобства — шкала 10.",
        "",
        "| Отель | Район | Agoda | N | Сервис | Чистота | Локация | Value |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in rows:
        md.append(
            "| {name} | {district} | {agoda_score} | {agoda_count} | {service} | {cleanliness} | {location} | {value} |".format(
                name=r.get("name") or "",
                district=r.get("district") or "",
                agoda_score=r.get("agoda_score") if r.get("agoda_score") is not None else "—",
                agoda_count=r.get("agoda_count") if r.get("agoda_count") is not None else "—",
                service=r.get("service") if r.get("service") is not None else "—",
                cleanliness=r.get("cleanliness") if r.get("cleanliness") is not None else "—",
                location=r.get("location") if r.get("location") is not None else "—",
                value=r.get("value") if r.get("value") is not None else "—",
            )
        )
    md.append("")
    (ROOT / "data" / "reviews-ranking.md").write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {csv_path} ({len(rows)} rows)")
    print(f"Wrote {ROOT / 'data' / 'reviews-ranking.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
