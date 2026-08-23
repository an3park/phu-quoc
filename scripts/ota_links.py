"""Dated Trip.com and OnlineTours links for Phu Quoc hotels.

Trip.com: hotel-detail when trip_id is known, otherwise city search with keyword.
OnlineTours: hotel page when the slug path is known, otherwise the Phu Quoc hotel list with q=.
"""

from __future__ import annotations

import re
from urllib.parse import urlencode

from booking_links import (
    DEFAULT_CHECKIN,
    DEFAULT_CHECKOUT,
    hotel_lookup,
    plain_cell,
    resolve_hotel_id,
)

TRIP_CITY_ID = "5649"  # Phu Quoc Island
TRIP_CURRENCY = "RUB"
EXTRA_COLUMN = "Ещё"

# Agoda catalog id → (trip hotel id, url slug)
TRIP_HOTELS: dict[int, tuple[str, str]] = {
    1624474: ("6489167", "jw-marriott-phu-quoc-emerald-bay-resort-and-spa"),
}

# Agoda catalog id → path after /oteli/vietnam/
ONLINETOURS_PATHS: dict[int, str] = {
    625168: "fukuok/vinpearl-resort-phu-quoc",
    2163073: "ganh-dau/vinoasis-phu-quoc",
    569108: "fukuok/salinda-premium-resort-and-spa",
    21774298: "ganh-dau/crowne-plaza-phu-quoc-starbay-an-ihg",
    35958304: "ganh-dau/wyndham-garden-0",
    5442703: "ganh-dau/radisson-blu-resort-phu-quoc",
    70425: "fukuok/la-veranda-resort-phu-quoc",
}


def _search_name(name: str) -> str:
    text = (name or "").strip()
    if text and "phu quoc" not in text.lower() and "phú quốc" not in text.lower():
        text = f"{text} Phu Quoc"
    return text or "Phu Quoc"


def trip_search_url(name: str, checkin: str | None = None, checkout: str | None = None) -> str:
    q = {
        "city": TRIP_CITY_ID,
        "checkIn": checkin or DEFAULT_CHECKIN,
        "checkOut": checkout or DEFAULT_CHECKOUT,
        "adult": "2",
        "children": "0",
        "crn": "1",
        "curr": TRIP_CURRENCY,
        "locale": "ru-RU",
        "keyword": _search_name(name),
    }
    return "https://ru.trip.com/hotels/list?" + urlencode(q)


def trip_hotel_url(
    trip_id: str,
    slug: str,
    checkin: str | None = None,
    checkout: str | None = None,
) -> str:
    q = {
        "checkIn": checkin or DEFAULT_CHECKIN,
        "checkOut": checkout or DEFAULT_CHECKOUT,
        "adult": "2",
        "children": "0",
        "crn": "1",
        "curr": TRIP_CURRENCY,
        "locale": "ru-RU",
    }
    return (
        f"https://ru.trip.com/hotels/phu-quoc-island-hotel-detail-{trip_id}/{slug}/?"
        + urlencode(q)
    )


def trip_url_for_hotel(
    hotel: dict | None,
    *,
    name: str | None = None,
    checkin: str | None = None,
    checkout: str | None = None,
) -> str:
    hotel = hotel or {}
    search_name = name or hotel.get("name") or ""
    hid = hotel.get("id")
    mapped = TRIP_HOTELS.get(int(hid)) if hid is not None else None
    if mapped:
        return trip_hotel_url(mapped[0], mapped[1], checkin, checkout)
    return trip_search_url(search_name, checkin, checkout)


def onlinetours_search_url(name: str) -> str:
    return "https://www.onlinetours.ru/oteli/vietnam/fukuok?" + urlencode(
        {"q": _search_name(name)}
    )


def onlinetours_hotel_url(path: str) -> str:
    path = path.strip("/")
    return f"https://www.onlinetours.ru/oteli/vietnam/{path}"


def onlinetours_url_for_hotel(
    hotel: dict | None,
    *,
    name: str | None = None,
) -> str:
    hotel = hotel or {}
    hid = hotel.get("id")
    path = None
    if hid is not None:
        path = hotel.get("onlinetours_path") or ONLINETOURS_PATHS.get(int(hid))
    if path:
        return onlinetours_hotel_url(path)
    return onlinetours_search_url(name or hotel.get("name") or "")


def ota_links_md(
    hotel: dict | None,
    *,
    name: str | None = None,
    checkin: str | None = None,
    checkout: str | None = None,
) -> str:
    search_name = name or (hotel or {}).get("name") or ""
    trip = trip_url_for_hotel(hotel, name=search_name, checkin=checkin, checkout=checkout)
    ot = onlinetours_url_for_hotel(hotel, name=search_name)
    return f"[Trip.com]({trip}) · [OnlineTours]({ot})"


def _is_sep(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells)


def append_ota_links_column(
    markdown: str,
    hotels: list[dict],
    checkin: str,
    checkout: str,
) -> str:
    """Add a right-hand Ещё column (Trip.com + OnlineTours) to tables with Отель."""
    by_id, by_label = hotel_lookup(hotels)
    lines = markdown.split("\n")
    out: list[str] = []
    hotel_col: int | None = None
    has_extra = False
    for line in lines:
        if not line.startswith("|"):
            hotel_col = None
            has_extra = False
            out.append(line)
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if _is_sep(cells):
            if hotel_col is not None and not has_extra:
                cells.append("---")
                out.append("| " + " | ".join(cells) + " |")
            else:
                out.append(line)
            continue
        lowered = [c.lower() for c in cells]
        if "отель" in lowered:
            hotel_col = lowered.index("отель")
            has_extra = EXTRA_COLUMN.lower() in lowered
            if not has_extra:
                cells.append(EXTRA_COLUMN)
                out.append("| " + " | ".join(cells) + " |")
            else:
                out.append(line)
            continue
        if hotel_col is None or hotel_col >= len(cells) or has_extra:
            out.append(line)
            continue
        name = plain_cell(cells[hotel_col])
        if not name or name == "—":
            cells.append("—")
            out.append("| " + " | ".join(cells) + " |")
            continue
        hid = resolve_hotel_id(name, by_label)
        hotel = by_id.get(hid) if hid is not None else None
        cells.append(ota_links_md(hotel, name=name, checkin=checkin, checkout=checkout))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)
