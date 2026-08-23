#!/usr/bin/env python3
"""Unit checks for Trip.com and OnlineTours extra-link column."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hotels_catalog import HOTELS  # noqa: E402
from ota_links import (  # noqa: E402
    EXTRA_COLUMN,
    append_ota_links_column,
    ota_links_md,
    onlinetours_url_for_hotel,
    trip_search_url,
    trip_url_for_hotel,
)
from booking_links import linkify_hotel_columns  # noqa: E402


def assert_true(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def test_trip_search_has_dates_and_rub() -> None:
    url = trip_search_url("Radisson Blu Resort Phu Quoc")
    assert_true("ru.trip.com/hotels/list" in url, url)
    assert_true("city=5649" in url, url)
    assert_true("checkIn=2026-10-19" in url, url)
    assert_true("checkOut=2026-10-25" in url, url)
    assert_true("curr=RUB" in url, url)
    assert_true("adult=2" in url, url)
    assert_true("Radisson" in url, url)


def test_trip_direct_for_jw() -> None:
    hotel = next(h for h in HOTELS if h["id"] == 1624474)
    url = trip_url_for_hotel(hotel)
    assert_true("hotel-detail-6489167" in url, url)
    assert_true("checkIn=2026-10-19" in url, url)
    assert_true("curr=RUB" in url, url)


def test_onlinetours_direct_and_search() -> None:
    vinpearl = next(h for h in HOTELS if h["id"] == 625168)
    url = onlinetours_url_for_hotel(vinpearl)
    assert_true("onlinetours.ru/oteli/vietnam/fukuok/vinpearl-resort-phu-quoc" in url, url)

    fusion = {"id": 1624152, "name": "Fusion Resort Phu Quoc"}
    search = onlinetours_url_for_hotel(fusion)
    assert_true("onlinetours.ru/oteli/vietnam/fukuok" in search, search)
    assert_true("q=" in search, search)
    assert_true("Fusion" in search, search)


def test_extra_md_has_both_sites() -> None:
    hotel = next(h for h in HOTELS if h["id"] == 5442703)
    cell = ota_links_md(hotel, name="Radisson Blu")
    assert_true("[Trip.com](" in cell, cell)
    assert_true("[OnlineTours](" in cell, cell)
    assert_true("radisson-blu-resort-phu-quoc" in cell, cell)


def test_every_catalog_hotel_gets_both_urls() -> None:
    for h in HOTELS:
        trip = trip_url_for_hotel(h)
        ot = onlinetours_url_for_hotel(h)
        assert_true("trip.com" in trip, f"{h['name']} {trip}")
        assert_true("checkIn=2026-10-19" in trip, f"{h['name']} {trip}")
        assert_true("onlinetours.ru" in ot, f"{h['name']} {ot}")


def test_append_column_to_readme_style_table() -> None:
    md = (
        "| Fit | Отель | Ночь |\n"
        "| --- | --- | --- |\n"
        "| 9.29 | Wyndham Grand | $115 |\n"
        "| 8.41 | Radisson Blu | $97 |\n"
    )
    linked = linkify_hotel_columns(md, HOTELS, "2026-10-19", "2026-10-25")
    out = append_ota_links_column(linked, HOTELS, "2026-10-19", "2026-10-25")
    header = out.splitlines()[0]
    assert_true(header.endswith("| Ещё |") or f"| {EXTRA_COLUMN} |" in header, header)
    assert_true("trip.com" in out, out)
    assert_true("onlinetours.ru" in out, out)
    assert_true("[Trip.com](" in out, out)
    assert_true("[OnlineTours](" in out, out)
    again = append_ota_links_column(out, HOTELS, "2026-10-19", "2026-10-25")
    assert_true(again.count("| Ещё |") == 1, again.splitlines()[0])


def main() -> int:
    tests = [
        test_trip_search_has_dates_and_rub,
        test_trip_direct_for_jw,
        test_onlinetours_direct_and_search,
        test_extra_md_has_both_sites,
        test_every_catalog_hotel_gets_both_urls,
        test_append_column_to_readme_style_table,
    ]
    for fn in tests:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"passed {len(tests)} tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
