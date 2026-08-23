#!/usr/bin/env python3
"""Unit checks for dated Booking.com hotel links."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hotels_catalog import HOTELS  # noqa: E402
from booking_links import (  # noqa: E402
    DEFAULT_CHECKIN,
    DEFAULT_CHECKOUT,
    README_ALIASES,
    booking_url_for_hotel,
    linkify_hotel_columns,
    md_hotel_link,
    resolve_hotel_id,
    hotel_lookup,
)


def assert_true(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def test_slug_url_has_stay_dates() -> None:
    hotel = {
        "id": 1,
        "name": "Regent Phu Quoc",
        "booking_slug": "regent-phu-quoc",
    }
    url = booking_url_for_hotel(hotel, checkin="2026-10-19", checkout="2026-10-25")
    assert_true("booking.com/hotel/vn/regent-phu-quoc.html" in url, url)
    assert_true("checkin=2026-10-19" in url, url)
    assert_true("checkout=2026-10-25" in url, url)
    assert_true("group_adults=2" in url, url)
    assert_true("no_rooms=1" in url, url)


def test_missing_slug_falls_back_to_search() -> None:
    hotel = {"id": 2, "name": "Fusion Resort Phu Quoc"}
    url = booking_url_for_hotel(hotel)
    assert_true("booking.com/searchresults.html" in url, url)
    assert_true("Fusion+Resort+Phu+Quoc" in url or "Fusion%20Resort%20Phu%20Quoc" in url, url)
    assert_true(f"checkin={DEFAULT_CHECKIN}" in url, url)
    assert_true(f"checkout={DEFAULT_CHECKOUT}" in url, url)


def test_md_link_keeps_label() -> None:
    hotel = next(h for h in HOTELS if h["id"] == 1624474)
    cell = md_hotel_link("JW Marriott", hotel=hotel)
    assert_true(cell.startswith("[JW Marriott]("), cell)
    assert_true("jw-marriott-phu-quoc-emerald-bay-resort-spa" in cell, cell)
    assert_true("checkin=2026-10-19" in cell, cell)


def test_every_catalog_hotel_gets_dated_url() -> None:
    for h in HOTELS:
        url = booking_url_for_hotel(h)
        assert_true("booking.com" in url, f"{h['name']} {url}")
        assert_true("checkin=2026-10-19" in url, f"{h['name']} {url}")
        assert_true("checkout=2026-10-25" in url, f"{h['name']} {url}")


def test_readme_aliases_point_at_catalog() -> None:
    ids = {h["id"] for h in HOTELS}
    missing = sorted({hid for hid in README_ALIASES.values() if hid not in ids})
    assert_true(not missing, f"alias ids not in catalog: {missing}")


def test_linkify_hotel_column() -> None:
    md = (
        "| Fit | Отель | Ночь |\n"
        "| --- | --- | --- |\n"
        "| 9.29 | Wyndham Grand | $115 |\n"
        "| 8.41 | Radisson Blu | $97 |\n"
    )
    out = linkify_hotel_columns(md, HOTELS, "2026-10-19", "2026-10-25")
    assert_true("[Wyndham Grand](" in out, out)
    assert_true("[Radisson Blu](" in out, out)
    assert_true("wyndham-grand-phuquoc" in out, out)
    assert_true("radisson-blu-resort-phu-quoc" in out, out)
    assert_true("checkin=2026-10-19" in out, out)


def test_resolve_short_and_catalog_names() -> None:
    _, by_label = hotel_lookup(HOTELS)
    assert_true(resolve_hotel_id("Regent Phu Quoc", by_label) == 21774297, "regent")
    assert_true(resolve_hotel_id("Vinpearl Resort & Spa", by_label) == 625168, "vinpearl")
    assert_true(resolve_hotel_id("JW Marriott Emerald Bay", by_label) == 1624474, "jw")


def main() -> int:
    tests = [
        test_slug_url_has_stay_dates,
        test_missing_slug_falls_back_to_search,
        test_md_link_keeps_label,
        test_every_catalog_hotel_gets_dated_url,
        test_readme_aliases_point_at_catalog,
        test_linkify_hotel_column,
        test_resolve_short_and_catalog_names,
    ]
    for fn in tests:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"passed {len(tests)} tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
