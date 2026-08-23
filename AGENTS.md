# AGENTS.md

This repository is a **hotel-research workspace**, not an application.

## What we are doing

Find a hotel on **Phú Quốc island, Vietnam** (Russian: Фукуок).  
**Not** Fukuoka, Japan.

Stay: **2026-10-19 → 2026-10-25** (6 nights). Default party: **2 adults, 1 room**.  
If the user later specifies children, extra adults, or a budget, update `memory/trip.md` and re-fetch.

Read first: `README.md`, `memory/trip.md`, `memory/sources.md`, `memory/picks.md`.

## How to refresh prices

```bash
python3 scripts/fetch_agoda_prices.py --checkin 2026-10-19 --checkout 2026-10-25
python3 scripts/fetch_hotel_profiles.py
python3 scripts/build_tables.py
python3 scripts/fetch_reviews.py
python3 scripts/build_reviews.py
```

Then update `README.md` summary tables if the ranking changed. Write guest-review notes in `data/reviews.md` (Agoda+Booking comments plus Google/Tripadvisor/OTA scores — never invent scores for blocked sites).

Add new hotels in `scripts/hotels_catalog.py` (Agoda property id + district + popularity).  
Hotel blurbs + curated breakfast scores: `scripts/hotel_profiles.py`.  
Grand World / Safari / water park / room style / sea & town distances: `scripts/hotel_pois.py`.  
Booking.com dated name-links: `scripts/booking_links.py` (optional `booking_slug` on each catalog hotel).  
Trip.com + OnlineTours extra column: `scripts/ota_links.py`.  
Tables sort by **composite rating**; a second **fit** score ranks the entertainment-cluster request.  
POI unit checks: `python3 scripts/test_hotel_pois.py`.  
Booking link checks: `python3 scripts/test_booking_links.py`.  
Extra OTA link checks: `python3 scripts/test_ota_links.py`.

## Sources

- **Agoda `GetSecondaryData`** currently returns dated live rates **and** guest-review scores. Combined scores often include Booking.com.
- Booking.com HTML is WAF-blocked; still capture Booking comments via Agoda ReviewComments (provider 3038) and published Booking scores from OTA snippets. Do not invent scores.
- Google Hotels and Kayak are useful as **cross-checks**, especially for Marriott/IHG/Vinpearl where Agoda can be 15–30% off the official rate.
- Always label whether a figure is **live for these dates** or a **typical / seasonal range**.
- Do not scrape in a way that dumps secrets, cookies, or personal accounts into the repo.

## October on Phu Quoc

Shoulder / late rainy season. East coast (Bai Khem, Bai Sao) is usually calmer for swimming than Long Beach / Bai Dai / Ong Lang. Prices are still closer to low season; high season starts November.

## Output rules

- Keep comparison tables in `data/comparison.md` and `data/comparison.csv`.
- Hotel names in markdown tables must be Booking.com links for the trip dates (2 adults, 1 room, `selected_currency=RUB`). Comparison tables stay in USD.
- Add a right-hand **Ещё** column with Trip.com (same dates, `curr=RUB`) and OnlineTours links. Direct hotel pages when the slug/id is known; otherwise a Phu Quoc search.
- State room type: a “cheap” Premier Village / Meliá / Sailing Club row may be a multi-bedroom villa.
- Do not book anything unless the user asks.

## Memory

Update `memory/` when assumptions change (party size, budget, must-have beach, kids).  
Do not store personal card data.
