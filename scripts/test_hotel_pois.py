#!/usr/bin/env python3
"""Unit checks for location/entertainment POI comparison fields."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hotels_catalog import HOTELS  # noqa: E402
from hotel_pois import (  # noqa: E402
    fmt_beach,
    fmt_place,
    fmt_room,
    fmt_water,
    resolve_poi,
    beach_m_from_features,
)


def assert_true(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def test_every_catalog_hotel_resolves() -> None:
    for h in HOTELS:
        poi = resolve_poi(h["id"], h["district"], room_comfort=9.0)
        for key in ("gw_km", "safari_km", "center_km", "fit", "water", "room_style"):
            assert_true(poi.get(key) is not None, f"{h['name']} missing {key}")
        assert_true(0 <= poi["fit"] <= 10, f"{h['name']} fit out of range: {poi['fit']}")
        assert_true(poi["gw_km"] >= 0 and poi["safari_km"] >= 0, f"{h['name']} negative km")


def test_grand_world_cluster_is_closest() -> None:
    wyndham = resolve_poi(2163073, "Bai Dai")
    garden = resolve_poi(35958304, "Bai Dai")
    radisson = resolve_poi(5442703, "Bai Dai")
    jw = resolve_poi(1624474, "Bai Khem")
    anphu = resolve_poi(6352970, "Duong Dong")
    assert_true(garden["gw_km"] <= 0.2, f"Garden should be inside GW, got {garden['gw_km']}")
    assert_true(wyndham["gw_km"] <= 0.4, f"Wyndham Grand official 300 m, got {wyndham['gw_km']}")
    assert_true(radisson["gw_km"] <= 0.6, "Radisson should be walkable to GW")
    assert_true(jw["gw_km"] > 40, "JW Bai Khem must be far from Grand World")
    assert_true(wyndham["fit"] > jw["fit"], "north cluster must beat JW on entertainment fit")
    assert_true(anphu["center_km"] < 1, "An Phu is in Duong Dong")
    assert_true(anphu["gw_km"] > 20, "town is not next to Grand World")


def test_safari_near_wyndham() -> None:
    w = resolve_poi(2163073, "Bai Dai")
    assert_true(w["safari_km"] == 3.0, f"official Safari 3 km, got {w['safari_km']}")
    assert_true(w["gw_walk"] is True, "Wyndham Grand is a walk/buggy to GW")


def test_waterparks() -> None:
    sanato = resolve_poi(5943665, "Long Beach")
    new_world = resolve_poi(34249576, "Bai Khem")
    wyndham = resolve_poi(2163073, "Bai Dai")
    ic = resolve_poi(3648660, "Long Beach")
    novus = resolve_poi(65344078, "An Thoi")
    salinda = resolve_poi(569108, "Long Beach")
    assert_true(sanato["water"] == "on-site", "Sanato Water Park on site")
    assert_true(new_world["water"] == "on-site", "New World Aqua World")
    assert_true(wyndham["water"] == "on-site", "Wyndham lagoon slides")
    assert_true(ic["water"] == "splash", "InterContinental kids splash")
    assert_true(novus["water"] == "hon-thom", "Novus Sol near Hon Thom")
    assert_true(salinda["water"] == "none", "Salinda has no water park")


def test_room_styles() -> None:
    jw = resolve_poi(1624474, "Bai Khem", room_comfort=9.7)
    la_veranda = resolve_poi(70425, "Long Beach", room_comfort=8.9)
    mango = resolve_poi(48370, "Ong Lang", room_comfort=8.6)
    muong = resolve_poi(1624612, "Long Beach", room_comfort=7.9)
    assert_true(jw["room_style"] == "design", "JW is Bensley design")
    assert_true(jw["room_score"] >= 9.7, "design uplift")
    assert_true(la_veranda["room_style"] == "colonial", "La Veranda colonial")
    assert_true(mango["room_style"] == "eco", "Mango Bay eco")
    assert_true(muong["room_score"] < jw["room_score"], "dated chain below JW")


def test_beach_parser() -> None:
    assert_true(beach_m_from_features(["80 meters to the beach"]) == 80, "parse meters")
    assert_true(beach_m_from_features(["Private beach"], beachfront=True) == 0, "private=0")
    l_azure = resolve_poi(
        8836100,
        "Long Beach",
        features=["beachfront", "220 meters to the beach", "Private beach"],
        beachfront=True,
    )
    assert_true(l_azure["beach_m"] == 220, "explicit meters beat beachfront flag")


def test_formatters_ru() -> None:
    w = resolve_poi(2163073, "Bai Dai", room_comfort=8.7)
    gw = fmt_place(w["gw_km"], w["gw_min"], w["gw_walk"])
    assert_true("300 м" in gw and "пешком" in gw, gw)
    assert_true(fmt_beach(0) == "beachfront", fmt_beach(0))
    water = fmt_water(w)
    assert_true("территории" in water, water)
    room = fmt_room(w)
    assert_true("современный" in room, room)


def test_fit_ranking_prefers_north() -> None:
    ids = [
        (2163073, "Bai Dai"),
        (35958304, "Bai Dai"),
        (5442703, "Bai Dai"),
        (21774298, "Bai Dai / Starbay"),
        (569108, "Long Beach"),
        (1624474, "Bai Khem"),
        (6352970, "Duong Dong"),
    ]
    garden = resolve_poi(35958304, "Bai Dai", room_comfort=8.7)
    assert_true(garden["water_score"] >= 8.0, "Garden is next to VinWonders even with only a slide")
    ranked = sorted(
        [(hid, resolve_poi(hid, dist, room_comfort=8.8)["fit"]) for hid, dist in ids],
        key=lambda x: -x[1],
    )
    top = [x[0] for x in ranked[:3]]
    assert_true(2163073 in top and 35958304 in top, f"Wyndham pair should lead: {ranked}")
    assert_true(ranked[-1][0] in (1624474, 6352970), f"JW or town last: {ranked}")


def _catalog_id(name_part: str) -> tuple[int, str]:
    hotel = next(h for h in HOTELS if name_part.lower() in h["name"].lower())
    return hotel["id"], hotel["district"]


def test_added_hotels_poi_overrides() -> None:
    lahana_id, lahana_d = _catalog_id("Lahana")
    camia_id, camia_d = _catalog_id("Camia")
    village_id, village_d = _catalog_id("M Village")
    soul_id, soul_d = _catalog_id("Soul Boutique")
    lahana = resolve_poi(lahana_id, lahana_d)
    camia = resolve_poi(camia_id, camia_d)
    village = resolve_poi(village_id, village_d)
    soul = resolve_poi(soul_id, soul_d)
    assert_true((lahana.get("beach_m") or 0) >= 500, f"Lahana is hillside, got {lahana.get('beach_m')}")
    assert_true(camia.get("beach_m") == 0, f"Camia has its own beach, got {camia.get('beach_m')}")
    assert_true((village.get("beach_m") or 0) >= 500, f"M Village is not beachfront, got {village.get('beach_m')}")
    assert_true((soul.get("beach_m") or 0) >= 100, f"Soul is not in-building beach, got {soul.get('beach_m')}")
    assert_true(lahana["gw_km"] > 20, "Lahana is not next to Grand World")
    assert_true(camia["gw_km"] < lahana["gw_km"], "Ong Lang is closer to Grand World than Long Beach hillside")
    assert_true(lahana["room_style"] == "boutique", lahana["room_style"])
    assert_true(soul["room_style"] == "modern", soul["room_style"])


def main() -> int:
    tests = [
        test_every_catalog_hotel_resolves,
        test_grand_world_cluster_is_closest,
        test_safari_near_wyndham,
        test_waterparks,
        test_room_styles,
        test_beach_parser,
        test_formatters_ru,
        test_fit_ranking_prefers_north,
        test_added_hotels_poi_overrides,
    ]
    for fn in tests:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"passed {len(tests)} tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
