"""Curated hotel blurbs and breakfast quality for Phu Quoc comparison tables.

Descriptions are short Russian pick-helpers (what makes the hotel distinctive).
Breakfast scores are /10: Agoda foodDining when present, else curated from
brand F&B reputation, cuisine breadth, and review consensus (labeled in tables).
"""

from __future__ import annotations

# hotel_id -> Russian one-liner of the main things that matter when choosing
DESCRIPTIONS: dict[int, str] = {
    1624474: "Икона острова (дизайн Bill Bensley): Bai Khem, спокойное море в октябре; Grand World / Safari ~70 мин — плохо, если цель парки.",
    3648660: "Крупный IHG на Long Beach: свой пляж, kids splash, резиденции 1BR+, сильный завтрак; до Grand World ~50 мин.",
    34249576: "Восток Bai Khem, виллы с бассейном + Aqua World (горки на территории); море спокойное, парки севера далеко.",
    21774297: "Ультра-люкс IHG Starbay: новые suite, сильнейший F&B; ~8 мин до Grand World, ~12 мин до Safari.",
    4518431: "Accor на Bai Khem: семейные виллы 2–3BR с private pool; купаться в октябре удобно, до Grand World час+.",
    1624152: "Уединённый Vung Bau, виллы + spa inclusive; Safari ближе (~18 мин), чем центр; без своего аквапарка.",
    569108: "Бутик Long Beach: sparkling wine breakfast, private beach; до города ~10 мин, до Grand World ~45 мин.",
    625168: "Bai Dai у VinWonders: 1,4 км / пешком до Grand World, Safari 4,7 км, VinBus по комплексу; номера не самые новые.",
    1985199: "Vinpearl-виллы у озера с private pool; VinBus до Grand World / Safari / VinWonders; не стандартный номер.",
    9776735: "Accor beachfront Long Beach: современные номера 5★; удобная база на западе, парки севера — ~50 мин.",
    5442703: "Value 5★ Bai Dai: ~500 м пешком до Grand World, Safari ~10 мин; лучший баланс цена/парки/море.",
    2163073: "Самый близкий 5★ к Grand World (300 м, багги); Safari 3 км, горки в лагуне. Не beachfront: море ~1,2 км.",
    14654959: "Mövenpick на тихом Ong Lang: спокойнее Long Beach, сад/балкон, mid-luxury без толпы.",
    14676909: "Виллы/студии Mövenpick Ong Lang: больше приватности, тот же тихий район.",
    1157572: "Accor Long Beach: надёжный семейный 5★, сад и пляж, предсказуемый сервис Novotel.",
    70425: "MGallery колониальный бутик Long Beach: атмосфера, private beach, сильная репутация у пар; завтрак часто не в дешёвом тарифе.",
    1032420: "Marriott Bai Dai: beachfront 5★, VinBus до Grand World / VinWonders / Safari; номера не самые новые.",
    5972590: "Accor suite на Bai Khem у JW: восток, спокойнее море, заметно дешевле JW Marriott.",
    1266957: "Meliá SOL — молодёжный 5★ Long Beach: тусовка/дизайн, ближе к вечеринкам, чем к тишине.",
    31187083: "Signature pool villas Long Beach (часто 2BR): дизайн Sailing Club, для компаний, не стандарт.",
    4968811: "Dusit beachfront Long Beach: сильные отзывы, private beach, Thai-сеть; хороший mid-luxury.",
    21774298: "Новый IHG Starbay: современные номера, beachfront; ~8 мин до Grand World, ~12 мин до Safari, дешевле Regent.",
    2061878: "Уединённый полуостров Vung Bau: private beach, spa; мало инфраструктуры вокруг.",
    5943665: "Sunset Sanato: виллы + Sanato Water Park на территории (янв 2026); Long Beach, до VinWonders ~30 км.",
    7008284: "Недооценённый 5★ Sonasea Long Beach: spa/бассейн, ближе к пляжу пешком, value vs бренды.",
    83294991: "Новый Long Beach resort (WorldHotels): высокие оценки при малом числе отзывов; сверить категорию номера.",
    2430159: "Очень много отзывов, beachfront Long Beach; в дешёвой выдаче часто 2BR suite — смотреть тип номера.",
    96572: "Бутик-коттеджи в саду Long Beach: private beach, spa, романтика; не «большой» курорт.",
    48370: "Эко-бунгало Ong Lang (rammed earth): природа, тишина, сильный food score; без люкс-глянца.",
    148661: "Chen Sea / The Slate Ong Lang: beach villa, джунгли у моря, пары; тихий запад.",
    400217: "Famiana mid-range Long Beach: семьи, сад, spa; разумный 4.5★ без люкс-ценника.",
    2577124: "4★ на холме Long Beach: лучшая репутация в новой четвёрке (Agoda 9.1 / 7.5k), не beachfront — 7–10 мин до воды.",
    3647146: "Тихий Ong Lang 4★, свой узкий/каменистый пляж, закаты; Agoda 9.0 / Booking 9.3 / TA 4.8.",
    24356624: "Домики на холме у Cua Lap (не пляж). Agoda 8.9, но Booking 8.3 — шум, слабее Lahana/Soul за $153.",
    56230219: "Новый бутик 2024 на юге Long Beach; завтрак и бассейн часто через Sailing Club (шаттл), не в здании.",
    8836100: "L'Azure: высокие оценки, private beach ~200 м; в выдаче часто executive suite.",
    21967772: "Jungle bungalow Ong Lang: природа и тишина, свой пляж; не центр развлечений.",
    47021962: "Grand Ocean Bay Ong Lang: крупные bungalow/family, beachfront; тихий севернее Long Beach.",
    35958304: "Wyndham Garden внутри Grand World: пешком до шоу/каналов, горка в бассейне, VinWonders ~1 км; 4★ не люкс.",
    14695651: "Небольшой Peppercorn Bai Dai: тише крупных сетей, сад; завтрак часто не включён.",
    11081947: "Paralia на Bai Khem: лучший бюджетный восток для купания в октябре, 4★ у белого песка.",
    1624612: "Сеть Mường Thanh Long Beach: дешёвый 4★ value; отзывы скромнее люкса.",
    6352970: "Центр Dương Đông: ночной рынок пешком, бюджет; пляж ~900 м, Grand World ~40 мин.",
    60710642: "Boutique Ham Ninh (восток): тише, private beach/сад; мало тусовок.",
    2061904: "Duong Dong у пляжа (~20 м): бюджет город+море; без бесплатной отмены в дешёвом тарифе.",
    406794: "Эко Bamboo Cottages Vung Bau: private beach, высокие оценки еды/сервиса; уединение.",
    1119483: "Praha у ночного рынка Duong Dong: городская база; завтрак часто не в тарифе.",
    983880: "Bauhinia Long Beach у моря: простой 3★ beachfront value.",
    39897314: "Green Inn: очень высокие оценки (мало отзывов), ~460 м до пляжа, family suite; не люкс-бренд.",
    4999788: "Coral Bay свой пляж Long Beach: mid 3★ beachfront без сети.",
    3007308: "An Nhien: йога ежедневно, сад, доступ к пляжу; wellness-бюджет, завтрак обычно нет.",
    32482497: "Ann Hotel Bai Khem: восток/спа спокойнее западного моря; простой 3★.",
    9612717: "Sunset Beach Long Beach: beachfront + pirate fire show; тусовочнее, чем бутик.",
    2570684: "Palmy Long Beach: private beach, но слабые отзывы — риск по качеству.",
    65344078: "Novus Sol Sunset Town: апартаменты у юга/канатки Hon Thom; не beach resort.",
    181816: "Hawaii Resort Long Beach: простой локальный вариант; мало отзывов.",
    12536303: "Hotel D'Anna An Thoi: бюджет юг/Sunset Town; без пляжного курорта.",
    87765217: "Anna Seaview An Thoi: ультра-бюджет, мало отзывов; только ночлег.",
    37281036: "Anna Beach Duong To: 4★ mid, ближе к югу; без завтрака в дешёвом тарифе.",
    81185611: "Anna Hotel An Thoi: иногда билеты на канатку/Hon Thom в промо; юг острова.",
    46581613: "AND Sunset Beach: на первой линии Duong Dong; на наши даты тарифа на Agoda нет.",
}

# Explicit breakfast quality /10 (curated). Prefer Agoda foodDining when merging in build.
BREAKFAST_QUALITY: dict[int, float] = {
    1624474: 9.2,  # JW — large luxury buffet, multiple restaurants
    3648660: 9.3,  # InterContinental Sora & Umi — widely praised
    34249576: 8.6,
    21774297: 9.5,  # Regent Rice Market — top-tier F&B
    4518431: 8.5,
    1624152: 8.7,  # Fusion — spa resort dining
    569108: 9.6,  # signature sparkling wine breakfast
    625168: 8.4,
    1985199: 8.3,
    9776735: 8.5,
    5442703: 8.4,
    2163073: 8.2,
    14654959: 8.5,
    14676909: 8.4,
    1157572: 8.0,  # foodDining 8.0
    70425: 8.6,  # La Veranda — boutique breakfast reputation / foodDining 8.2 + uplift
    1032420: 8.0,  # foodDining 7.7 + brand buffet
    5972590: 8.3,
    1266957: 8.1,
    31187083: 8.6,
    4968811: 8.8,
    21774298: 8.7,
    2061878: 8.2,
    5943665: 8.0,
    7008284: 8.2,
    83294991: 8.4,
    2430159: 8.5,
    96572: 8.3,  # foodDining 8.0 + boutique praise
    48370: 8.8,  # foodDining 8.8
    148661: 7.8,  # foodDining 7.5
    400217: 7.8,  # foodDining 7.5
    2577124: 8.4,  # Lahana — сильный 4★ сервис, не signature-buffet
    3647146: 8.2,  # Camia
    24356624: 7.6,  # M Village — смешанные отзывы, Booking слабее
    56230219: 8.0,  # Soul — завтрак часто в Sailing Club
    8836100: 8.4,
    21967772: 8.2,
    47021962: 8.0,
    35958304: 8.0,
    14695651: 7.2,  # often no breakfast in rate
    11081947: 7.8,
    1624612: 7.4,
    6352970: 7.5,
    60710642: 7.3,
    2061904: 7.4,
    406794: 8.3,  # foodDining 8.1
    1119483: 7.6,  # foodDining 8.0 but often not in cheap rate
    983880: 7.5,
    39897314: 8.2,  # high overall; small property
    4999788: 7.8,
    3007308: 6.5,  # typically no breakfast
    32482497: 7.6,
    9612717: 8.0,
    2570684: 6.5,  # weak reviews overall
    65344078: 7.5,
    181816: 7.2,
    12536303: 6.8,
    87765217: 6.5,
    37281036: 7.0,
    81185611: 7.4,
    46581613: 7.5,
}

BREAKFAST_NOTES: dict[int, str] = {
    569108: "фирменный sparkling wine breakfast",
    3648660: "Sora & Umi buffet / Club lounge",
    21774297: "Rice Market — большой люкс-buffet",
    1624474: "люкс-buffet + несколько ресторанов",
    70425: "бутик-завтрак MGallery",
    48370: "сильный foodDining у эко-курорта",
    3007308: "в дешёвом тарифе обычно без завтрака",
    1119483: "часто без завтрака в дешёвом тарифе",
    2577124: "не пляж: холм, 7–10 мин до воды",
    56230219: "завтрак часто в Sailing Club (шаттл)",
}


def description_for(hotel_id: int, fallback_name: str = "") -> str:
    return DESCRIPTIONS.get(hotel_id) or (
        f"Курорт на Фукуоке ({fallback_name}). Сверить пляж, тип номера и завтрак в тарифе."
        if fallback_name
        else "Сверить пляж, тип номера и завтрак в тарифе."
    )


def breakfast_quality_for(hotel_id: int, food_dining: float | None = None) -> float:
    """Prefer live Agoda foodDining when present; else curated score."""
    if food_dining is not None:
        curated = BREAKFAST_QUALITY.get(hotel_id)
        if curated is None:
            return round(float(food_dining), 1)
        # blend: 60% live foodDining, 40% curated (signature breakfasts etc.)
        return round(0.6 * float(food_dining) + 0.4 * curated, 1)
    if hotel_id in BREAKFAST_QUALITY:
        return BREAKFAST_QUALITY[hotel_id]
    return 7.5
