"""Location and entertainment POIs for Phu Quoc hotel comparison.

Criteria added 2026-08-23 (user request):
1. proximity to Grand World
2. Vinpearl Safari
3. water park on-site or nearby
4. modern / beautiful rooms
5. distance to the sea and to Duong Dong (island “centre”)

Distances are typical **taxi / VinBus drive** unless `gw_walk` is set.
Sources: hotel official pages (Wyndham Grand 300 m / Safari 3 km),
Marriott/IHG/Vinpearl listings, VinBus routes 2026, LocalVietnam /
impresstravel 2026. Labelled as typical, not live GPS.
"""

from __future__ import annotations

import re
from typing import Any

# Landmark notes (north cluster is one complex):
# Grand World + VinWonders (Typhoon World water park) sit together on Bai Dai.
# Vinpearl Safari is 3–7 km / 8–12 min from that plaza (free VinBus).
# Duong Dong night market = practical “city centre”.
# Hon Thom Aquatopia (south) is a separate water-park day trip via cable car.

# District fallbacks when a hotel has no override.
DISTRICT_POIS: dict[str, dict[str, Any]] = {
    "Bai Dai": {
        "gw_km": 2.5,
        "gw_min": 8,
        "safari_km": 4.5,
        "safari_min": 12,
        "center_km": 28.0,
        "center_min": 42,
        "water": "vinwonders",
        "water_note": "VinWonders Typhoon World рядом (север)",
    },
    "Bai Dai / Starbay": {
        "gw_km": 3.6,
        "gw_min": 8,
        "safari_km": 7.0,
        "safari_min": 12,
        "center_km": 22.0,
        "center_min": 35,
        "water": "vinwonders",
        "water_note": "VinWonders ~4 км / 8–10 мин",
    },
    "Long Beach": {
        "gw_km": 32.0,
        "gw_min": 45,
        "safari_km": 36.0,
        "safari_min": 52,
        "center_km": 6.0,
        "center_min": 12,
        "water": "none",
        "water_note": "аквапарк только поездкой на север или юг",
    },
    "Ong Lang": {
        "gw_km": 16.0,
        "gw_min": 26,
        "safari_km": 20.0,
        "safari_min": 32,
        "center_km": 10.0,
        "center_min": 18,
        "water": "none",
        "water_note": "VinBus вдоль западного берега до Grand World ~25–30 мин",
    },
    "Vung Bau": {
        "gw_km": 14.0,
        "gw_min": 22,
        "safari_km": 11.0,
        "safari_min": 18,
        "center_km": 22.0,
        "center_min": 35,
        "water": "none",
        "water_note": "севернее Лонг-Бич; Safari ближе, чем центр",
    },
    "Duong Dong": {
        "gw_km": 28.0,
        "gw_min": 40,
        "safari_km": 32.0,
        "safari_min": 48,
        "center_km": 0.6,
        "center_min": 5,
        "water": "none",
        "water_note": "ночной рынок пешком; аквапарк — день-трип",
    },
    "Bai Khem": {
        "gw_km": 50.0,
        "gw_min": 70,
        "safari_km": 54.0,
        "safari_min": 78,
        "center_km": 26.0,
        "center_min": 40,
        "water": "none",
        "water_note": "восток: спокойное море, далеко от Grand World",
    },
    "Ham Ninh": {
        "gw_km": 40.0,
        "gw_min": 55,
        "safari_km": 44.0,
        "safari_min": 62,
        "center_km": 16.0,
        "center_min": 25,
        "water": "none",
        "water_note": "восточная бухта, без парков",
    },
    "An Thoi": {
        "gw_km": 52.0,
        "gw_min": 75,
        "safari_km": 56.0,
        "safari_min": 82,
        "center_km": 28.0,
        "center_min": 42,
        "water": "hon-thom",
        "water_note": "Aquatopia на Hon Thom: канатка от An Thoi",
    },
    "Duong To": {
        "gw_km": 38.0,
        "gw_min": 55,
        "safari_km": 42.0,
        "safari_min": 62,
        "center_km": 12.0,
        "center_min": 18,
        "water": "none",
        "water_note": "юг острова, ближе к канатке чем к Grand World",
    },
}

# Per-hotel overrides. Keys match Agoda catalog ids.
# water: on-site | splash | vinwonders | hon-thom | none
HOTEL_POIS: dict[int, dict[str, Any]] = {
    # --- North Bai Dai / Grand World cluster ---
    2163073: {  # Wyndham Grand — official: GW 300 m, VinWonders 1.2 km, Safari 3 km
        "gw_km": 0.3,
        "gw_min": 4,
        "gw_walk": True,
        "safari_km": 3.0,
        "safari_min": 8,
        "center_km": 28.0,
        "center_min": 45,
        "beach_m": 0,
        "water": "on-site",
        "water_note": "лагуна с горками + kids area; VinWonders 1,2 км",
        "room": "modern",
        "room_note": "сеть 5★, номера современные, не «икона дизайна»",
    },
    35958304: {  # Wyndham Garden Grandworld — inside / steps from Grand World
        "gw_km": 0.15,
        "gw_min": 3,
        "gw_walk": True,
        "safari_km": 3.5,
        "safari_min": 10,
        "center_km": 28.0,
        "center_min": 45,
        "beach_m": 80,
        "water": "splash",
        "water_note": "горка в бассейне; VinWonders ~1 км",
        "room": "modern",
        "room_note": "4★ pragmatic, новые корпуса у Grand World",
    },
    625168: {  # Vinpearl Resort & Spa — 1.4 km GW, 4.7 km Safari
        "gw_km": 1.4,
        "gw_min": 15,
        "gw_walk": True,
        "safari_km": 4.7,
        "safari_min": 10,
        "center_km": 28.0,
        "center_min": 45,
        "beach_m": 0,
        "water": "vinwonders",
        "water_note": "VinWonders Typhoon World ~15 мин пешком; VinBus внутри комплекса",
        "room": "standard",
        "room_note": "классика Vinpearl ~2014, просторные, не самый свежий дизайн",
    },
    1985199: {  # Meliá Vinpearl — VinBus V5 to GW / Safari
        "gw_km": 2.0,
        "gw_min": 8,
        "safari_km": 5.0,
        "safari_min": 12,
        "center_km": 28.0,
        "center_min": 45,
        "beach_m": 0,
        "water": "vinwonders",
        "water_note": "VinBus до VinWonders / Grand World / Safari",
        "room": "villa",
        "room_note": "виллы с private pool, современный семейный формат",
    },
    5442703: {  # Radisson Blu — Trip.com ~0.47 km Grand World plaza
        "gw_km": 0.5,
        "gw_min": 8,
        "gw_walk": True,
        "safari_km": 4.0,
        "safari_min": 10,
        "center_km": 27.0,
        "center_min": 42,
        "beach_m": 0,
        "water": "vinwonders",
        "water_note": "пешком к Grand World; VinWonders рядом",
        "room": "modern",
        "room_note": "value 5★, светлые современные deluxe",
    },
    1032420: {  # Sheraton Bai Dai — VinBus V3 Sheraton→VinWonders→GW→Safari; ~5 km Safari
        "gw_km": 2.5,
        "gw_min": 8,
        "safari_km": 5.0,
        "safari_min": 12,
        "center_km": 26.0,
        "center_min": 40,
        "beach_m": 100,
        "water": "vinwonders",
        "water_note": "свой большой пул; аквапарк — VinWonders (VinBus)",
        "room": "standard",
        "room_note": "Marriott 5★, неоклассика, не самый новый корпус",
    },
    14695651: {  # Peppercorn Bai Dai
        "gw_km": 3.5,
        "gw_min": 10,
        "safari_km": 5.5,
        "safari_min": 12,
        "center_km": 27.0,
        "center_min": 42,
        "beach_m": 0,
        "water": "splash",
        "water_note": "Agoda помечает water park — небольшой kids/slides, не VinWonders",
        "room": "boutique",
        "room_note": "маленький курорт, уютнее сетей",
    },
    # Starbay (Regent + Crowne Plaza): 3.6 km GW, 7 km Safari, 4.3 km VinWonders
    21774297: {
        "gw_km": 3.6,
        "gw_min": 8,
        "safari_km": 7.0,
        "safari_min": 12,
        "center_km": 22.0,
        "center_min": 35,
        "beach_m": 80,
        "water": "vinwonders",
        "water_note": "8–12 мин до Grand World / Safari / VinWonders",
        "room": "modern",
        "room_note": "новые suite 2023, один из лучших roomComfort на острове",
    },
    21774298: {
        "gw_km": 3.6,
        "gw_min": 8,
        "safari_km": 7.0,
        "safari_min": 12,
        "center_km": 22.0,
        "center_min": 35,
        "beach_m": 0,
        "water": "vinwonders",
        "water_note": "как у Regent: ~10 мин до парков",
        "room": "modern",
        "room_note": "новый IHG 2023, современный 5★ дешевле Regent",
    },
    # --- Long Beach (Bai Truong, west, south of town) ---
    3648660: {  # InterContinental — kids splash, far from GW
        "gw_km": 35.0,
        "gw_min": 50,
        "safari_km": 39.0,
        "safari_min": 55,
        "center_km": 8.0,
        "center_min": 15,
        "beach_m": 0,
        "water": "splash",
        "water_note": "splash-зона kids club; большой аквапарк — день-трип",
        "room": "modern",
        "room_note": "современный IHG, residence 1BR, сильный дизайн общественных зон",
    },
    5943665: {  # Sunset Sanato — on-site Sanato Water Park (Jan 2026); 30 km VinWonders
        "gw_km": 30.0,
        "gw_min": 45,
        "safari_km": 34.0,
        "safari_min": 50,
        "center_km": 8.0,
        "center_min": 15,
        "beach_m": 0,
        "water": "on-site",
        "water_note": "Sanato Water Park на территории (открыт янв 2026)",
        "room": "villa",
        "room_note": "виллы с private pool, инстаграм-арт, не классический «номер»",
    },
    9776735: {
        "gw_km": 33.0,
        "gw_min": 48,
        "safari_km": 37.0,
        "safari_min": 54,
        "center_km": 6.0,
        "center_min": 12,
        "beach_m": 0,
        "water": "none",
        "room": "modern",
        "room_note": "Accor 5★ 2019, светлые современные номера",
    },
    1157572: {  # Novotel — VinBus P5 Novotel → Grand World
        "gw_km": 32.0,
        "gw_min": 45,
        "safari_km": 36.0,
        "safari_min": 52,
        "center_km": 5.0,
        "center_min": 10,
        "beach_m": 0,
        "water": "none",
        "room": "standard",
        "room_note": "предсказуемый Novotel, сад/twin, не wow-дизайн",
    },
    569108: {
        "gw_km": 31.0,
        "gw_min": 45,
        "safari_km": 35.0,
        "safari_min": 50,
        "center_km": 4.5,
        "center_min": 10,
        "beach_m": 0,
        "water": "none",
        "room": "boutique",
        "room_note": "бутик, красиво и ухоженно, не «новый стеклянный»",
    },
    70425: {
        "gw_km": 30.0,
        "gw_min": 42,
        "safari_km": 34.0,
        "safari_min": 50,
        "center_km": 2.5,
        "center_min": 8,
        "beach_m": 0,
        "water": "none",
        "room": "colonial",
        "room_note": "колониальный MGallery — красиво, но не современный минимализм",
    },
    4968811: {
        "gw_km": 33.0,
        "gw_min": 48,
        "safari_km": 37.0,
        "safari_min": 54,
        "center_km": 6.0,
        "center_min": 12,
        "beach_m": 0,
        "water": "none",
        "room": "modern",
        "room_note": "Dusit beachfront, сильный roomComfort",
    },
    83294991: {
        "gw_km": 33.0,
        "gw_min": 48,
        "safari_km": 37.0,
        "safari_min": 54,
        "center_km": 6.0,
        "center_min": 12,
        "beach_m": 90,
        "water": "none",
        "room": "modern",
        "room_note": "новый resort, высокие оценки номера при малом n отзывов",
    },
    1266957: {
        "gw_km": 32.0,
        "gw_min": 46,
        "safari_km": 36.0,
        "safari_min": 52,
        "center_km": 6.0,
        "center_min": 12,
        "beach_m": 270,
        "water": "none",
        "room": "modern",
        "room_note": "молодёжный Meliá SOL, дизайн тусовки",
    },
    7008284: {
        "gw_km": 31.0,
        "gw_min": 45,
        "safari_km": 35.0,
        "safari_min": 50,
        "center_km": 7.0,
        "center_min": 14,
        "beach_m": 250,
        "water": "none",
        "room": "standard",
        "room_note": "Sonasea 5★ value, не новый люкс",
    },
    8836100: {
        "gw_km": 31.0,
        "gw_min": 45,
        "safari_km": 35.0,
        "safari_min": 50,
        "center_km": 5.0,
        "center_min": 10,
        "beach_m": 220,
        "water": "none",
        "room": "modern",
        "room_note": "высокие оценки, в выдаче часто suite",
    },
    2430159: {
        "gw_km": 32.0,
        "gw_min": 46,
        "safari_km": 36.0,
        "safari_min": 52,
        "center_km": 6.0,
        "center_min": 12,
        "beach_m": 0,
        "water": "none",
        "room": "standard",
        "room_note": "много отзывов; дешёвый тариф часто 2BR",
    },
    31187083: {
        "gw_km": 34.0,
        "gw_min": 50,
        "safari_km": 38.0,
        "safari_min": 55,
        "center_km": 8.0,
        "center_min": 15,
        "beach_m": 0,
        "water": "none",
        "room": "villa",
        "room_note": "дизайн Sailing Club, pool villa 2BR",
    },
    96572: {
        "gw_km": 31.0,
        "gw_min": 44,
        "safari_km": 35.0,
        "safari_min": 50,
        "center_km": 5.0,
        "center_min": 10,
        "beach_m": 0,
        "water": "none",
        "room": "boutique",
        "room_note": "коттеджи в саду, романтика, не high-rise modern",
    },
    400217: {
        "gw_km": 32.0,
        "gw_min": 46,
        "safari_km": 36.0,
        "safari_min": 52,
        "center_km": 7.0,
        "center_min": 14,
        "beach_m": 0,
        "water": "none",
        "room": "standard",
        "room_note": "семейный mid-range",
    },
    39897314: {
        "gw_km": 30.0,
        "gw_min": 42,
        "safari_km": 34.0,
        "safari_min": 50,
        "center_km": 4.0,
        "center_min": 8,
        "beach_m": 460,
        "water": "none",
        "room": "modern",
        "room_note": "высокие оценки номера, мало отзывов, не люкс",
    },
    1624612: {
        "gw_km": 30.0,
        "gw_min": 42,
        "safari_km": 34.0,
        "safari_min": 50,
        "center_km": 4.0,
        "center_min": 8,
        "beach_m": 310,
        "water": "none",
        "room": "dated",
        "room_note": "сеть value, отзывы скромнее, номера проще",
    },
    983880: {
        "gw_km": 31.0,
        "gw_min": 44,
        "safari_km": 35.0,
        "safari_min": 50,
        "center_km": 5.0,
        "center_min": 10,
        "beach_m": 510,
        "water": "none",
        "room": "standard",
        "room_note": "простой 3★",
    },
    4999788: {
        "gw_km": 34.0,
        "gw_min": 50,
        "safari_km": 38.0,
        "safari_min": 55,
        "center_km": 8.0,
        "center_min": 15,
        "beach_m": 0,
        "water": "none",
        "room": "standard",
        "room_note": "mid 3★ beachfront",
    },
    3007308: {
        "gw_km": 32.0,
        "gw_min": 46,
        "safari_km": 36.0,
        "safari_min": 52,
        "center_km": 7.0,
        "center_min": 14,
        "beach_m": 390,
        "water": "none",
        "room": "eco",
        "room_note": "wellness/йога, скромные номера",
    },
    9612717: {
        "gw_km": 32.0,
        "gw_min": 46,
        "safari_km": 36.0,
        "safari_min": 52,
        "center_km": 6.0,
        "center_min": 12,
        "beach_m": 0,
        "water": "none",
        "room": "standard",
        "room_note": "beachfront + шоу, не бутик",
    },
    2570684: {
        "gw_km": 32.0,
        "gw_min": 46,
        "safari_km": 36.0,
        "safari_min": 52,
        "center_km": 6.0,
        "center_min": 12,
        "beach_m": 0,
        "water": "none",
        "room": "dated",
        "room_note": "слабые отзывы — риск по номеру",
    },
    181816: {
        "gw_km": 32.0,
        "gw_min": 46,
        "safari_km": 36.0,
        "safari_min": 52,
        "center_km": 6.0,
        "center_min": 12,
        "room": "standard",
        "room_note": "локальный 3★, мало отзывов",
    },
    # --- Ong Lang ---
    14654959: {
        "gw_km": 16.0,
        "gw_min": 25,
        "safari_km": 20.0,
        "safari_min": 32,
        "center_km": 10.0,
        "center_min": 18,
        "beach_m": 0,
        "water": "none",
        "room": "modern",
        "room_note": "Mövenpick mid-luxury, сад/балкон",
    },
    14676909: {
        "gw_km": 16.0,
        "gw_min": 25,
        "safari_km": 20.0,
        "safari_min": 32,
        "center_km": 10.0,
        "center_min": 18,
        "beach_m": 0,
        "water": "none",
        "room": "villa",
        "room_note": "студии/виллы Mövenpick",
    },
    48370: {
        "gw_km": 17.0,
        "gw_min": 26,
        "safari_km": 21.0,
        "safari_min": 32,
        "center_km": 10.0,
        "center_min": 18,
        "beach_m": 0,
        "water": "none",
        "room": "eco",
        "room_note": "rammed earth, природа, без глянца",
    },
    148661: {  # Chen Sea — VinBus P5 stop
        "gw_km": 15.0,
        "gw_min": 24,
        "safari_km": 19.0,
        "safari_min": 30,
        "center_km": 9.0,
        "center_min": 16,
        "beach_m": 0,
        "water": "none",
        "room": "boutique",
        "room_note": "beach villa, джунгли",
    },
    21967772: {
        "gw_km": 14.0,
        "gw_min": 22,
        "safari_km": 18.0,
        "safari_min": 28,
        "center_km": 12.0,
        "center_min": 20,
        "beach_m": 0,
        "water": "none",
        "room": "eco",
        "room_note": "jungle bungalow",
    },
    47021962: {
        "gw_km": 14.0,
        "gw_min": 22,
        "safari_km": 18.0,
        "safari_min": 28,
        "center_km": 12.0,
        "center_min": 20,
        "beach_m": 0,
        "water": "none",
        "room": "villa",
        "room_note": "крупные family bungalow",
    },
    # --- Vung Bau ---
    1624152: {
        "gw_km": 14.0,
        "gw_min": 22,
        "safari_km": 11.0,
        "safari_min": 18,
        "center_km": 22.0,
        "center_min": 35,
        "beach_m": 0,
        "water": "none",
        "room": "villa",
        "room_note": "spa-виллы, уединение",
    },
    2061878: {
        "gw_km": 15.0,
        "gw_min": 24,
        "safari_km": 12.0,
        "safari_min": 20,
        "center_km": 23.0,
        "center_min": 36,
        "beach_m": 0,
        "water": "none",
        "room": "villa",
        "room_note": "полуостров, private beach",
    },
    406794: {
        "gw_km": 14.0,
        "gw_min": 22,
        "safari_km": 11.0,
        "safari_min": 18,
        "center_km": 22.0,
        "center_min": 35,
        "beach_m": 0,
        "water": "none",
        "room": "eco",
        "room_note": "бамбуковые коттеджи",
    },
    # --- Bai Khem (east) ---
    1624474: {
        "gw_km": 50.0,
        "gw_min": 70,
        "safari_km": 54.0,
        "safari_min": 78,
        "center_km": 26.0,
        "center_min": 40,
        "beach_m": 0,
        "water": "none",
        "room": "design",
        "room_note": "Bill Bensley — самый «красивый» дизайн острова, не минимализм",
    },
    34249576: {  # New World — Aqua World on site
        "gw_km": 50.0,
        "gw_min": 70,
        "safari_km": 54.0,
        "safari_min": 78,
        "center_km": 26.0,
        "center_min": 40,
        "beach_m": 0,
        "water": "on-site",
        "water_note": "Aqua World: горки и splash на территории; Grand World далеко",
        "room": "villa",
        "room_note": "новые pool villa, современный семейный курорт",
    },
    4518431: {
        "gw_km": 50.0,
        "gw_min": 70,
        "safari_km": 54.0,
        "safari_min": 78,
        "center_km": 26.0,
        "center_min": 40,
        "beach_m": 0,
        "water": "none",
        "room": "villa",
        "room_note": "2–3BR Accor villa + private pool",
    },
    5972590: {
        "gw_km": 50.0,
        "gw_min": 70,
        "safari_km": 54.0,
        "safari_min": 78,
        "center_km": 26.0,
        "center_min": 40,
        "beach_m": 0,
        "water": "none",
        "room": "modern",
        "room_note": "Accor suite у JW, спокойнее восточное море",
    },
    11081947: {
        "gw_km": 49.0,
        "gw_min": 68,
        "safari_km": 53.0,
        "safari_min": 76,
        "center_km": 25.0,
        "center_min": 38,
        "beach_m": 80,
        "water": "none",
        "room": "standard",
        "room_note": "4★ у белого песка, не люкс",
    },
    32482497: {
        "gw_km": 49.0,
        "gw_min": 68,
        "safari_km": 53.0,
        "safari_min": 76,
        "center_km": 25.0,
        "center_min": 38,
        "beach_m": 120,
        "water": "none",
        "room": "standard",
        "room_note": "простой 3★ Bai Khem",
    },
    # --- Duong Dong (centre) ---
    6352970: {
        "gw_km": 28.0,
        "gw_min": 40,
        "safari_km": 32.0,
        "safari_min": 48,
        "center_km": 0.4,
        "center_min": 5,
        "beach_m": 920,
        "water": "none",
        "room": "standard",
        "room_note": "городская база у ночного рынка",
    },
    1119483: {
        "gw_km": 28.0,
        "gw_min": 40,
        "safari_km": 32.0,
        "safari_min": 48,
        "center_km": 0.3,
        "center_min": 4,
        "beach_m": 320,
        "water": "none",
        "room": "standard",
        "room_note": "у ночного рынка; roomComfort высокий для 3★",
    },
    2061904: {
        "gw_km": 28.0,
        "gw_min": 40,
        "safari_km": 32.0,
        "safari_min": 48,
        "center_km": 0.8,
        "center_min": 6,
        "beach_m": 20,
        "water": "none",
        "room": "standard",
        "room_note": "город + почти пляж",
    },
    46581613: {
        "gw_km": 29.0,
        "gw_min": 42,
        "safari_km": 33.0,
        "safari_min": 50,
        "center_km": 1.5,
        "center_min": 8,
        "beach_m": 0,
        "water": "none",
        "room": "standard",
        "room_note": "первая линия Duong Dong",
    },
    # --- South / Hon Thom ---
    65344078: {
        "gw_km": 52.0,
        "gw_min": 75,
        "safari_km": 56.0,
        "safari_min": 82,
        "center_km": 28.0,
        "center_min": 42,
        "beach_m": None,
        "water": "hon-thom",
        "water_note": "Sunset Town / канатка Hon Thom Aquatopia",
        "room": "modern",
        "room_note": "апартаменты, высокий roomComfort, не beach resort",
    },
    81185611: {
        "gw_km": 52.0,
        "gw_min": 75,
        "safari_km": 56.0,
        "safari_min": 82,
        "center_km": 28.0,
        "center_min": 42,
        "water": "hon-thom",
        "water_note": "промо с билетами на канатку / Hon Thom Water Park",
        "room": "standard",
        "room_note": "юг, бюджет",
    },
    12536303: {
        "gw_km": 52.0,
        "gw_min": 75,
        "safari_km": 56.0,
        "safari_min": 82,
        "center_km": 28.0,
        "center_min": 42,
        "water": "hon-thom",
        "room": "dated",
        "room_note": "бюджет An Thoi",
    },
    87765217: {
        "gw_km": 52.0,
        "gw_min": 75,
        "safari_km": 56.0,
        "safari_min": 82,
        "center_km": 28.0,
        "center_min": 42,
        "water": "hon-thom",
        "room": "dated",
        "room_note": "ультра-бюджет",
    },
    37281036: {
        "gw_km": 38.0,
        "gw_min": 55,
        "safari_km": 42.0,
        "safari_min": 62,
        "center_km": 12.0,
        "center_min": 18,
        "beach_m": 110,
        "water": "none",
        "room": "standard",
        "room_note": "4★ южнее центра",
    },
    60710642: {
        "gw_km": 40.0,
        "gw_min": 55,
        "safari_km": 44.0,
        "safari_min": 62,
        "center_km": 16.0,
        "center_min": 25,
        "beach_m": 0,
        "water": "none",
        "room": "boutique",
        "room_note": "тихий восток Ham Ninh",
    },
}

ROOM_STYLE_RU = {
    "modern": "современный",
    "design": "дизайн",
    "villa": "вилла",
    "boutique": "бутик",
    "colonial": "колониальный",
    "eco": "эко",
    "standard": "стандарт",
    "dated": "простой / устаревший",
}

WATER_RANK = {
    "on-site": 10.0,
    "splash": 6.5,
    "vinwonders": 8.5,
    "hon-thom": 7.0,
    "none": 1.5,
}

STYLE_ROOM_ADJ = {
    "modern": 0.25,
    "design": 0.35,
    "villa": 0.15,
    "boutique": 0.05,
    "colonial": -0.15,  # beautiful but not “modern”
    "eco": -0.6,
    "standard": -0.2,
    "dated": -1.2,
}

_BEACH_RE = re.compile(r"(\d+)\s*meters?\s+to the beach", re.I)


def beach_m_from_features(features: list[str] | None, beachfront: bool = False) -> int | None:
    texts = [str(x) for x in (features or []) if x]
    meters: list[int] = []
    for t in texts:
        m = _BEACH_RE.search(t)
        if m:
            meters.append(int(m.group(1)))
    if meters:
        return min(meters)
    blob = " ".join(texts).lower()
    if beachfront or "beachfront" in blob or "private beach" in blob:
        return 0
    return None


def _district_base(district: str) -> dict[str, Any]:
    if district in DISTRICT_POIS:
        return dict(DISTRICT_POIS[district])
    # fuzzy
    for key, val in DISTRICT_POIS.items():
        if key.lower() in (district or "").lower() or (district or "").lower() in key.lower():
            return dict(val)
    return dict(DISTRICT_POIS["Long Beach"])


def resolve_poi(
    hotel_id: int | None,
    district: str = "",
    *,
    features: list[str] | None = None,
    beachfront: bool = False,
    room_comfort: float | None = None,
) -> dict[str, Any]:
    base = _district_base(district or "")
    over = dict(HOTEL_POIS.get(int(hotel_id), {})) if hotel_id is not None else {}
    gw_km = float(over.get("gw_km", base["gw_km"]))
    safari_km = float(over.get("safari_km", base["safari_km"]))
    center_km = float(over.get("center_km", base["center_km"]))
    water = over.get("water") or base.get("water") or "none"
    water_note = over.get("water_note") or base.get("water_note") or ""
    # Agoda “Water park” flag can upgrade none → splash unless curated says otherwise
    feat_l = " ".join(features or []).lower()
    if water == "none" and "water park" in feat_l:
        water = "splash"
        water_note = water_note or "Agoda: Water park (уточнить масштаб)"

    beach_m = over.get("beach_m")
    if beach_m is None:
        beach_m = beach_m_from_features(features, beachfront=beachfront)

    room_style = over.get("room") or "standard"
    room_note = over.get("room_note") or ""
    comfort = float(room_comfort) if room_comfort is not None else None
    room_score = None
    if comfort is not None:
        room_score = round(max(1.0, min(10.0, comfort + STYLE_ROOM_ADJ.get(room_style, 0))), 1)
    elif hotel_id is not None:
        # style-only placeholder so ranking still works
        room_score = round(7.4 + STYLE_ROOM_ADJ.get(room_style, 0), 1)

    gw_score = _dist_score(gw_km, walk=bool(over.get("gw_walk")))
    safari_score = _dist_score(safari_km)
    water_score = WATER_RANK.get(water, 1.5)
    # Nearby Typhoon World (VinWonders) counts as “рядом” for the north cluster.
    if gw_km <= 6:
        water_score = max(water_score, 8.7 - min(gw_km, 6) * 0.2)
    if water == "vinwonders" and gw_km > 12:
        water_score = 3.0
    if water == "hon-thom" and center_km >= 20:
        water_score = 8.0
    if water == "on-site":
        water_score = max(water_score, 10.0)
    beach_score = _beach_score(beach_m)
    center_score = _dist_score(center_km)

    # Entertainment cluster fit (Grand World + Safari + water + modern room + sea).
    # City centre is the opposite axis — shown separately, light weight only.
    rs = room_score if room_score is not None else 7.0
    fit = round(
        0.28 * gw_score
        + 0.22 * safari_score
        + 0.20 * water_score
        + 0.18 * rs
        + 0.08 * beach_score
        + 0.04 * center_score,
        2,
    )

    return {
        "gw_km": gw_km,
        "gw_min": int(over.get("gw_min", base["gw_min"])),
        "gw_walk": bool(over.get("gw_walk")),
        "safari_km": safari_km,
        "safari_min": int(over.get("safari_min", base["safari_min"])),
        "center_km": center_km,
        "center_min": int(over.get("center_min", base["center_min"])),
        "beach_m": beach_m,
        "water": water,
        "water_note": water_note,
        "room_style": room_style,
        "room_note": room_note,
        "room_comfort": comfort,
        "room_score": room_score,
        "gw_score": round(gw_score, 2),
        "safari_score": round(safari_score, 2),
        "water_score": round(water_score, 2),
        "beach_score": round(beach_score, 2),
        "center_score": round(center_score, 2),
        "fit": fit,
    }


def _dist_score(km: float, walk: bool = False) -> float:
    if walk and km <= 1.5:
        return 10.0 if km <= 0.4 else 9.4
    if km <= 1:
        return 9.6
    if km <= 3:
        return 9.0
    if km <= 6:
        return 8.0
    if km <= 10:
        return 6.5
    if km <= 18:
        return 4.5
    if km <= 28:
        return 2.8
    if km <= 40:
        return 1.6
    return 0.8


def _beach_score(beach_m: int | None) -> float:
    if beach_m is None:
        return 3.0
    if beach_m <= 30:
        return 10.0
    if beach_m <= 100:
        return 8.5
    if beach_m <= 250:
        return 6.5
    if beach_m <= 500:
        return 4.5
    if beach_m <= 1000:
        return 2.5
    return 1.5


def fmt_place(km: float, minutes: int, walk: bool = False) -> str:
    if walk and km < 1:
        meters = int(round(km * 1000))
        return f"{meters} м, пешком ~{minutes} мин"
    if km < 1:
        meters = int(round(km * 1000))
        return f"{meters} м / {minutes} мин"
    if km == int(km):
        km_s = str(int(km))
    else:
        km_s = f"{km:.1f}".replace(".", ",")
    return f"{km_s} км / {minutes} мин"


def fmt_beach(beach_m: int | None) -> str:
    if beach_m is None:
        return "не у моря"
    if beach_m <= 30:
        return "beachfront"
    return f"{beach_m} м"


def fmt_water(poi: dict) -> str:
    kind = poi.get("water") or "none"
    note = (poi.get("water_note") or "").strip()
    labels = {
        "on-site": "на территории",
        "splash": "splash / горка",
        "vinwonders": "VinWonders рядом",
        "hon-thom": "Hon Thom Aquatopia",
        "none": "нет рядом",
    }
    head = labels.get(kind, kind)
    if note:
        return f"{head}: {note}"
    return head


def fmt_room(poi: dict) -> str:
    style = ROOM_STYLE_RU.get(poi.get("room_style") or "standard", poi.get("room_style") or "")
    score = poi.get("room_score")
    comfort = poi.get("room_comfort")
    bits = [style]
    if score is not None:
        bits.append(f"{score:.1f}")
    elif comfort is not None:
        bits.append(f"comfort {comfort:.1f}")
    note = (poi.get("room_note") or "").strip()
    head = " ".join(bits)
    if note:
        return f"{head} — {note}"
    return head
