# Источники (снимок 23 августа 2026)

## Сработало

| Источник | Что дали | Датировано 19–25.10.2026? |
| --- | --- | --- |
| Agoda GetSecondaryData | Живые тарифы 56 отелей, с налогами + **оценки/категории отзывов** | тарифы **да**; отзывы — накопленные |
| Agoda GetSecondaryData `reviews` / grades | Guest score, cleanliness/facilities/location/service/value, иногда foodDining | нет (накопительные отзывы) |
| Agoda aboutHotel + featuresYouLove | Фичи (beachfront, spa, kids club…) для описаний | нет |
| Agoda ReviewComments | Тексты Agoda **и Booking.com** (провайдер 3038) | нет, репутация |
| Google Hotels | Кросс-чек JW, Vinpearl, InterContinental, sponsored-цены | частично |
| Google Maps (карточки) | Radisson **4.8**/5 (6 106), Grand Ocean Bay **4.3**/5 (890) | нет |
| Tripadvisor | JW 4.8/1 663; Camia 4.8/337; Radisson 4.5/1 199 | нет |
| Expedia / Trivago / HotelsCombined / Trip.com | Агрегированные оценки Lahana, Camia, Soul, Grand | нет |
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

Booking.com HTML (AWS WAF 202) — оценки Booking всё же видны через Agoda combined + сниппеты. Expedia/Hotels.com (429), Marriott.com (403), IHG (403/401), Accor API (401), Traveloka (403), Tripadvisor HTML (403), Vinpearl official (403), Melia.com (403), Trivago SPA.

## Вывод для следующих прогонов

1. Сначала Agoda live (`scripts/fetch_agoda_prices.py`).
2. Затем профили отзывов (`scripts/fetch_hotel_profiles.py`) → `scripts/build_tables.py`.
3. Отзывы: `scripts/fetch_reviews.py` (Agoda+Booking comments) + ручной кросс Google/TA для шорт-листа → `scripts/build_reviews.py`.
4. Для JW / InterContinental / Vinpearl / Accor — вручную или через Google Hotels сверить бренд.
5. Fusion и Nam Nghi могут не продаваться далеко вперёд.
6. Не смешивать «типичная цена» и «тариф на наши даты» в одной колонке без пометки. Не смешивать оценку Google /5 с Agoda /10 без пересчёта.
7. Колонка «Завтрак /10» — качество; отдельно флаг «включён в тариф».
8. Километры до Grand World / Safari / центра — типичная поездка, не live GPS. Не смешивать с ценами Agoda.
