"""Booking.com dated links for Phu Quoc hotels.

Direct /hotel/vn/{slug}.html when the slug is verified.
Otherwise a searchresults URL with the property name and stay dates.
"""

from __future__ import annotations

import re
from urllib.parse import urlencode

DEFAULT_CHECKIN = "2026-10-19"
DEFAULT_CHECKOUT = "2026-10-25"
BOOKING_CURRENCY = "RUB"

# Short labels in README tables → catalog hotel id
README_ALIASES: dict[str, int] = {
    "JW Marriott Emerald Bay": 1624474,
    "JW Marriott": 1624474,
    "InterContinental Long Beach": 3648660,
    "InterContinental": 3648660,
    "New World Phu Quoc": 34249576,
    "New World": 34249576,
    "Regent Phu Quoc": 21774297,
    "Regent Starbay": 21774297,
    "Regent": 21774297,
    "Premier Village (вилла 3BR)": 4518431,
    "Premier Village": 4518431,
    "Fusion Resort (spa inclusive)": 1624152,
    "Fusion Resort": 1624152,
    "Fusion": 1624152,
    "Salinda Resort": 569108,
    "Salinda": 569108,
    "Vinpearl Resort & Spa": 625168,
    "Vinpearl": 625168,
    "Meliá Vinpearl (вилла 1BR)": 1985199,
    "Meliá Vinpearl": 1985199,
    "Pullman Beach Resort": 9776735,
    "Pullman": 9776735,
    "Radisson Blu Resort": 5442703,
    "Radisson Blu": 5442703,
    "Wyndham Grand": 2163073,
    "Wyndham Garden Grandworld": 35958304,
    "Mövenpick Resort Waverly": 14654959,
    "Mövenpick Waverly": 14654959,
    "Mövenpick Villas": 14676909,
    "Novotel Phu Quoc": 1157572,
    "Novotel": 1157572,
    "La Veranda MGallery": 70425,
    "La Veranda": 70425,
    "Sheraton Long Beach": 1032420,
    "Sheraton Bai Dai": 1032420,
    "Sheraton": 1032420,
    "Premier Residences Emerald Bay": 5972590,
    "Premier Residences Emerald Bay": 5972590,
    "Premier Residences": 5972590,
    "SOL by Meliá": 1266957,
    "Sailing Club Signature": 31187083,
    "Dusit Princess Moonrise": 4968811,
    "Crowne Plaza Starbay": 21774298,
    "Crowne Plaza": 21774298,
    "Nam Nghi Coral Peninsula": 2061878,
    "Sunset Sanato": 5943665,
    "Best Western Premier Sonasea": 7008284,
    "WorldHotels Long Beach": 83294991,
    "WorldHotels": 83294991,
    "Seashells Phu Quoc": 2430159,
    "Seashells": 2430159,
    "Cassia Cottage": 96572,
    "Mango Bay": 48370,
    "Chen Sea / The Slate": 148661,
    "Chen Sea": 148661,
    "Famiana Resort & Spa": 400217,
    "Famiana": 400217,
    "Lahana Resort & Spa": 2577124,
    "Lahana": 2577124,
    "Camia Resort & Spa": 3647146,
    "Camia": 3647146,
    "M Village": 24356624,
    "Soul Boutique Hotel": 56230219,
    "Soul Boutique": 56230219,
    "Soul": 56230219,
    "Grand Ocean Bay": 47021962,
    "L'Azure": 8836100,
    "L'Azure": 8836100,
    "Ocean Bay Phu Quoc": 21967772,
    "Grand Resort Ocean Bay": 47021962,
    "Wyndham Garden Grandworld": 35958304,
    "Wyndham Garden": 35958304,
    "Peppercorn Beach": 14695651,
    "Paralia Khem Beach": 11081947,
    "Paralia": 11081947,
    "Muong Thanh Luxury": 1624612,
    "Muong Thanh": 1624612,
    "An Phu Hotel": 6352970,
    "An Phu": 6352970,
    "Rocks Beach Boutique": 60710642,
    "Brenta Phu Quoc": 2061904,
    "Bamboo Cottages": 406794,
    "Praha Hotel": 1119483,
    "Praha": 1119483,
    "Bauhinia Resort": 983880,
    "Green Inn": 39897314,
    "Coral Bay": 4999788,
    "An Nhien Retreat": 3007308,
    "Ann Hotel & Spa": 32482497,
    "Sunset Beach Resort": 9612717,
    "The Palmy": 2570684,
    "Novus Sol Hotel": 65344078,
    "Hawaii Resort": 181816,
}


def stay_query(checkin: str | None = None, checkout: str | None = None) -> dict[str, str]:
    return {
        "checkin": checkin or DEFAULT_CHECKIN,
        "checkout": checkout or DEFAULT_CHECKOUT,
        "group_adults": "2",
        "no_rooms": "1",
        "group_children": "0",
        "selected_currency": BOOKING_CURRENCY,
    }


def booking_search_url(name: str, checkin: str | None = None, checkout: str | None = None) -> str:
    q = stay_query(checkin, checkout)
    ss = (name or "").strip()
    if ss and "phu quoc" not in ss.lower() and "phú quốc" not in ss.lower():
        ss = f"{ss} Phu Quoc"
    q["ss"] = ss or "Phu Quoc"
    return "https://www.booking.com/searchresults.html?" + urlencode(q)


def booking_hotel_url(
    slug: str | None,
    name: str,
    checkin: str | None = None,
    checkout: str | None = None,
) -> str:
    q = stay_query(checkin, checkout)
    if slug:
        return f"https://www.booking.com/hotel/vn/{slug}.html?" + urlencode(q)
    return booking_search_url(name, checkin, checkout)


def booking_url_for_hotel(
    hotel: dict | None,
    *,
    name: str | None = None,
    checkin: str | None = None,
    checkout: str | None = None,
) -> str:
    hotel = hotel or {}
    slug = hotel.get("booking_slug")
    search_name = name or hotel.get("name") or ""
    return booking_hotel_url(slug, search_name, checkin, checkout)


def md_hotel_link(
    label: str,
    *,
    hotel: dict | None = None,
    slug: str | None = None,
    checkin: str | None = None,
    checkout: str | None = None,
) -> str:
    text = (label or "").replace("|", "/").replace("\n", " ").strip() or "отель"
    if hotel is not None:
        url = booking_url_for_hotel(hotel, name=hotel.get("name") or text, checkin=checkin, checkout=checkout)
    else:
        url = booking_hotel_url(slug, text, checkin, checkout)
    return f"[{text}]({url})"


def plain_cell(cell: str) -> str:
    cell = (cell or "").strip()
    m = re.fullmatch(r"\[([^\]]+)\]\([^)]+\)", cell)
    if m:
        return m.group(1).strip()
    return cell.strip("*").strip()


def hotel_lookup(hotels: list[dict]) -> tuple[dict[int, dict], dict[str, int]]:
    by_id = {int(h["id"]): h for h in hotels}
    by_label: dict[str, int] = {}
    for h in hotels:
        by_label[h["name"].strip().lower()] = int(h["id"])
    for label, hid in README_ALIASES.items():
        by_label[label.strip().lower()] = hid
    return by_id, by_label


def resolve_hotel_id(label: str, by_label: dict[str, int]) -> int | None:
    key = plain_cell(label).lower()
    if not key:
        return None
    if key in by_label:
        return by_label[key]
    for alias, hid in sorted(by_label.items(), key=lambda x: -len(x[0])):
        if len(alias) < 8:
            continue
        if key == alias or key.startswith(alias + " ") or alias.startswith(key + " "):
            return hid
        if alias in key or (len(key) >= 10 and key in alias):
            return hid
    return None


def linkify_hotel_columns(markdown: str, hotels: list[dict], checkin: str, checkout: str) -> str:
    """Replace the Отель column in markdown tables with dated Booking links."""
    by_id, by_label = hotel_lookup(hotels)
    lines = markdown.split("\n")
    out: list[str] = []
    hotel_col: int | None = None
    for line in lines:
        if not line.startswith("|"):
            hotel_col = None
            out.append(line)
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            out.append(line)
            continue
        lowered = [c.lower() for c in cells]
        if "отель" in lowered:
            hotel_col = lowered.index("отель")
            out.append(line)
            continue
        if hotel_col is None or hotel_col >= len(cells):
            out.append(line)
            continue
        name = plain_cell(cells[hotel_col])
        if not name or name == "—":
            out.append(line)
            continue
        hid = resolve_hotel_id(name, by_label)
        hotel = by_id.get(hid) if hid is not None else None
        cells[hotel_col] = md_hotel_link(name, hotel=hotel, checkin=checkin, checkout=checkout)
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)
