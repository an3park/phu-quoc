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
python3 scripts/build_tables.py
```

Then update `README.md` summary tables if the ranking changed.

Add new hotels in `scripts/hotels_catalog.py` (Agoda property id + district + popularity).

## Sources

- **Agoda `GetSecondaryData`** currently returns dated live rates. Treat inclusive USD as the comparable number.
- Booking.com, Expedia, Hotels.com, brand CRSs, Traveloka often block non-browser clients (WAF / 403 / 429). Do not invent prices for blocked sites.
- Google Hotels and Kayak are useful as **cross-checks**, especially for Marriott/IHG/Vinpearl where Agoda can be 15–30% off the official rate.
- Always label whether a figure is **live for these dates** or a **typical / seasonal range**.
- Do not scrape in a way that dumps secrets, cookies, or personal accounts into the repo.

## October on Phu Quoc

Shoulder / late rainy season. East coast (Bai Khem, Bai Sao) is usually calmer for swimming than Long Beach / Bai Dai / Ong Lang. Prices are still closer to low season; high season starts November.

## Output rules

- Keep comparison tables in `data/comparison.md` and `data/comparison.csv`.
- Prefer USD all-in (tax + service). Mention VND only with an explicit rate.
- State room type: a “cheap” Premier Village / Meliá / Sailing Club row may be a multi-bedroom villa.
- Do not book anything unless the user asks.

## Memory

Update `memory/` when assumptions change (party size, budget, must-have beach, kids).  
Do not store personal card data.
