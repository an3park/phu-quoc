# Источники (снимок 22 августа 2026)

## Сработало

| Источник | Что дали | Датировано 19–25.10.2026? |
| --- | --- | --- |
| Agoda GetSecondaryData | Живые тарифы ~50 отелей, с налогами | **да** |
| Agoda GetSecondaryData `reviews` / grades | Guest score, cleanliness/facilities/location/service/value, иногда foodDining | нет (накопительные отзывы) |
| Agoda aboutHotel + featuresYouLove | Фичи (beachfront, spa, kids club…) для описаний | нет |
| Google Hotels | Кросс-чек JW, Vinpearl, InterContinental, sponsored-цены | частично |
| Kayak / Momondo | Сезонность, «from $», октябрь часто дешёвый месяц | нет, средние |
| VietnamSpot (июль 2026) | Диапазоны low/high season, районы | ориентиры 2026 |
| Luxury / brand reviews 2026 | Завтраки Regent Rice Market, InterContinental Sora & Umi, Salinda sparkling wine | нет |
| Agoda hotel pages | Средние цены отеля (JW ~$317, InterContinental ~$216) | нет |
| Официальный Wyndham Grand | Grand World 300 м, VinWonders 1,2 км, Safari 3 км | ориентир |
| Vinpearl / Trip.com / Almosafer | Vinpearl 1,4 км до GW, 4,7 км Safari; Radisson ~0,5 км GW; Crowne Plaza 3,6 км GW, 7 км Safari | ориентир |
| VinBus 2026 | маршруты Sheraton / Melia / Vinpearl ↔ GW / Safari / VinWonders | нет |
| LocalVietnam / impresstravel 2026 | Dương Đông → Grand World ~30 км / 40 мин; Safari 5–10 мин от GW | ориентир |
| Sunset Sanato / LocalVietnam water parks | Sanato Water Park (янв 2026); New World Aqua World; Typhoon World; Hon Thom Aquatopia | нет |

## Заблокировано / пусто без браузера

Booking.com (AWS WAF 202), Expedia/Hotels.com (429), Marriott.com (403), IHG (403/401), Accor API (401), Traveloka (403), Tripadvisor (403), Vinpearl official (403), Melia.com (403), Trivago (пустой SPA), Kayak HTML без цен.

## Вывод для следующих прогонов

1. Сначала Agoda live (`fetch_agoda_prices.py`).
2. Затем профили отзывов (`fetch_hotel_profiles.py`) → `build_tables.py`.
3. Для JW / InterContinental / Vinpearl / Accor — вручную или через Google Hotels сверить бренд.
4. Fusion и Nam Nghi могут не продаваться далеко вперёд.
5. Не смешивать «типичная цена» и «тариф на наши даты» в одной колонке без пометки.
6. Колонка «Завтрак /10» — качество; отдельно флаг «включён в тариф».
7. Километры до Grand World / Safari / центра — типичная поездка, не live GPS. Не смешивать с ценами Agoda.
