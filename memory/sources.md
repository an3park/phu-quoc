# Источники (снимок 23 августа 2026)

## Сработало

| Источник | Что дали | Датировано 19–25.10.2026? |
| --- | --- | --- |
| Agoda GetSecondaryData | Живые тарифы 56 отелей + **оценки/категории отзывов** | тарифы **да**; отзывы — накопленные |
| Agoda ReviewComments | Тексты Agoda **и Booking.com** (провайдер 3038) | нет, репутация |
| Google Hotels | Кросс-чек JW, Vinpearl, InterContinental | частично |
| Google Maps (карточки) | Radisson **4.8**/5 (6 106), Grand Ocean Bay **4.3**/5 (890) | нет |
| Tripadvisor | JW 4.8/1 663; Camia 4.8/337; Radisson 4.5/1 199 | нет |
| Expedia / Trivago / HotelsCombined / Trip.com | Агрегированные оценки Lahana, Camia, Soul, Grand | нет |
| Kayak / Momondo | Сезонность | нет, средние |
| VietnamSpot (июль 2026) | Low/high season | ориентиры 2026 |

## Заблокировано / пусто без браузера

Booking.com HTML (AWS WAF 202) — оценки Booking всё же видны через Agoda combined + сниппеты. Expedia/Hotels.com (429), Marriott.com (403), IHG (403/401), Accor API (401), Traveloka (403), Tripadvisor HTML (403), Vinpearl official (403), Melia.com (403), Trivago SPA.

## Вывод для следующих прогонов

1. Сначала Agoda live тарифы.
2. Отзывы: `scripts/fetch_reviews.py` (Agoda+Booking comments) + ручной кросс Google/TA для шорт-листа.
3. Для JW / InterContinental / Vinpearl / Accor — сверить бренд.
4. Fusion и Nam Nghi могут не продаваться далеко вперёд.
5. Не смешивать «типичная цена» и «тариф на наши даты». Не смешивать оценку Google /5 с Agoda /10 без пересчёта.
