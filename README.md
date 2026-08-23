# Отели Фукуок (Phú Quốc), 19–25 октября 2026

Репозиторий для выбора отеля на острове **Фукуок, Вьетнам** (не путать с японской Фукуокой). Даты: заезд **19 октября 2026**, выезд **25 октября 2026** — **6 ночей**.

Полная таблица: [`data/comparison.md`](data/comparison.md) · CSV: [`data/comparison.csv`](data/comparison.csv) · профили: [`data/hotel-profiles.json`](data/hotel-profiles.json) · тарифы: [`data/agoda-live.json`](data/agoda-live.json)

Инструкции для агентов: [`AGENTS.md`](AGENTS.md) · память поездки: [`memory/`](memory/)

---

## Параметры сравнения

| Параметр | Значение |
| --- | --- |
| Остров | Phú Quốc, Вьетнам |
| Заезд / выезд | 19.10.2026 → 25.10.2026 |
| Ночей | 6 |
| Гости | 2 взрослых, 1 номер (если вас больше — цены будут выше) |
| Валюта | USD, с налогами и сборами (обычно 5% service + 8% VAT, у Accor часто 13.4%) |
| Ссылки на отели | **Booking.com** на 19–25.10.2026, 2 взрослых, 1 номер, валюта **₽ (RUB)** |
| Снято | 22 августа 2026 (цены); отзывы Agoda — август 2026 |
| Главный источник живых тарифов | **Agoda** API `GetSecondaryData` на эти даты |
| Рейтинг и завтрак | сводный /10 из отзывов + категорий + завтрака + звёзд (см. `data/comparison.md`) |
| Другие площадки | Google Hotels, Kayak, Booking, Expedia, Hotels.com, Marriott, IHG, Accor, Traveloka, Trip.com, Trivago, официальные сайты |
| **Grand World** | типичная поездка такси/VinBus до комплекса на Bãi Dài (север) |
| **Safari** | Vinpearl Safari, тот же северный кластер (~8–12 мин от Grand World) |
| **Аквапарк** | на территории / splash / VinWonders Typhoon World / Hon Thom Aquatopia |
| **Номер** | стиль (современный / дизайн / вилла / бутик / колониальный / эко) + Agoda roomComfort |
| **Море / центр** | метры до пляжа и км до ночного рынка Dương Đông |

Октябрь на Фукуоке — переход с сезона дождей к сухому. Море на **западном** берегу (Long Beach, Ong Lang, Bai Dai) ещё может быть волнистым; на **востоке** (Bai Khem, Bai Sao) обычно спокойнее. 19–25 октября — вторая половина месяца, погода уже лучше, чем в начале октября, а цены ещё не пиковые (пик — ноябрь–март).

---

## Короткий вывод

**По сводному рейтингу** (не по цене): Regent **9.56**, Salinda **9.45**, JW Marriott **9.28**, InterContinental / Dusit **~9.24**, Crowne Plaza Starbay **9.18**.

Если нужен **5★ без переплаты**: Radisson Blu (**рейтинг 8.96**, **$97**), Vinpearl (**8.86**, **$104**), Mövenpick Waverly (**8.82**, **$105**), Novotel (**8.75**, **$111**), Wyndham Grand (**8.68**, **$115**).

Если важна **восточная сторона в октябре**: Paralia Khem Beach **$84** (рейтинг 8.46), Premier Residences Emerald Bay **$157** (8.80), New World **$252** (8.86), JW Marriott **$459** (9.28).

Если **бутик / романтика / завтрак**: Salinda (**9.45**, завтрак **9.1**, sparkling wine) **$210**; La Veranda (**9.12**, завтрак **8.4**) **$208**; Cassia (**8.96**) **$224**; Chen Sea (**8.70**) **$201**.

Если **бюджет**: An Phu **$33**, Muong Thanh **$50**, Bauhinia **$66**, Praha **$67** — рейтинги ниже люкса (~7.9–8.7).

**Fusion Resort** (spa inclusive) и **Nam Nghi** на Agoda на эти даты **не продаются**. Перед бронью JW Marriott сверьте официальный сайт и Traveloka: Google Hotels показывал типичные **$310–358**, тогда как Agoda — **$459**.

---

## Если нужны Grand World, Safari, аквапарк и красивый номер

Это **разные оси**. Grand World + VinWonders (аквапарк Typhoon World) + Vinpearl Safari стоят одним северным кластером на **Bãi Dài**. Центр — ночной рынок **Dương Đông**, ~28–32 км / 40–50 мин от парков. Beachfront на севере есть; «море у дверей **и** прогулка по городу» почти не складывается.

Полные колонки: [`data/comparison.md`](data/comparison.md) (блок «Локация и развлечения») и CSV.

**Fit** (смесь близости к паркам + аквапарк + номер + море): лидирует север Bãi Dài.

| Fit | Отель | Grand World | Safari | Аквапарк | Номер | Море | Центр | Ночь |
| --- | ---: | --- | --- | --- | --- | --- | --- | ---: |
| **9.29** | [Wyndham Grand](https://www.booking.com/hotel/vn/wyndham-grand-phuquoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | 300 м пешком | 3 км / 8 мин | горки в лагуне + VinWonders 1,2 км | современный 8.9 | beachfront | 28 км / 45 мин | **$115** |
| **8.57** | [Vinpearl Resort & Spa](https://www.booking.com/hotel/vn/vinpearl-resort-phu-quoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | 1,4 км / 15 мин | 4,7 км | Typhoon World ~15 мин пешком | стандарт 8.7 (корпус ~2014) | beachfront | 28 км | **$104** |
| **8.47** | [Wyndham Garden Grandworld](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=Wyndham+Garden+Grandworld+Phu+Quoc) | **150 м пешком** | 3,5 км | горка в бассейне + VinWonders ~1 км | современный 4★ | 80 м | 28 км | **$106** |
| **8.41** | [Radisson Blu](https://www.booking.com/hotel/vn/radisson-blu-resort-phu-quoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | 500 м пешком | 4 км | VinWonders рядом | современный value 5★ | beachfront | 27 км | **$97** |
| **8.36** | [Sheraton Bai Dai](https://www.booking.com/hotel/vn/sheraton-phu-quoc-long-beach-resort.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | 2,5 км / 8 мин (VinBus) | 5 км | VinWonders (VinBus) | Marriott, не самый новый | 100 м | 26 км | **$129** |
| **8.01** | [Crowne Plaza Starbay](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=Crowne+Plaza+Phu+Quoc+Starbay) | 3,6 км / 8 мин | 7 км | VinWonders ~10 мин | **новые** номера 2023 (9.6) | beachfront | 22 км | **$146** |
| **7.96** | [Regent Starbay](https://www.booking.com/hotel/vn/regent-phu-quoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | 3,6 км / 8 мин | 7 км | VinWonders ~10 мин | suite **10.0** roomComfort | 80 м | 22 км | $500 |

Практичный выбор, если все пять пунктов важны сразу: **Radisson Blu $97** (пешком до Grand World) или **Wyndham Grand $115** (горки + 300 м до каналов). Если номер важнее цены — **Crowne Plaza $146** (новый IHG) или **Regent**.

Аквапарк **на территории**, но не у Grand World: **Sunset Sanato** (Sanato Water Park, янв 2026, Long Beach, вилла **$352**) и **New World** (Aqua World, Bai Khem, вилла **$252**). Юг: **Hon Thom Aquatopia** через канатку из An Thoi / Sunset Town.

Самый красивый номер **не** на севере: JW Marriott (Bensley, Bai Khem, **$459**, ~70 мин до парков), WorldHotels / Dusit / InterContinental на Long Beach.

Ближе к центру Dương Đông: **Praha / An Phu** (ночной рынок пешком, пляж 300–900 м, Grand World ~40 мин). La Veranda ~2,5 км от города, beachfront, колониальный стиль.

---

## Топ по сводному рейтингу (есть тариф на даты)

| Рейтинг | Отель | Район | Отзывы | Завтрак /10 | Ночь | Кому |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| **9.56** | [Regent Phu Quoc](https://www.booking.com/hotel/vn/regent-phu-quoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Starbay | 9.4 | **9.5** | $500 | ультра-люкс, сильнейший F&B |
| **9.45** | [Salinda](https://www.booking.com/hotel/vn/salinda-premium-resort-and-spa.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Long Beach | 9.4 | **9.1** | $210 | бутик, sparkling wine breakfast |
| **9.28** | [JW Marriott Emerald Bay](https://www.booking.com/hotel/vn/jw-marriott-phu-quoc-emerald-bay-resort-spa.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Bai Khem | 9.2 | **9.2** | $459 | топ острова, восток |
| **9.27** | [WorldHotels Long Beach](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=WorldHotels+Long+Beach+Resort+Phu+Quoc) | Long Beach | 9.3 | 8.4 | $247 | новый; мало отзывов |
| **9.24** | [Dusit Princess Moonrise](https://www.booking.com/hotel/vn/dusit-princess-moonrise-beach-resort.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Long Beach | 9.2 | 8.8 | $247 | beachfront mid-luxury |
| **9.24** | [InterContinental Long Beach](https://www.booking.com/hotel/vn/intercontinental-hotels-phu-quoc-long-beach-resort.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Long Beach | 9.0 | **9.3** | $264 | семьи, kids club, завтрак |
| **9.18** | [Crowne Plaza Starbay](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=Crowne+Plaza+Phu+Quoc+Starbay) | Starbay | 9.1 | 8.7 | $146 | новый IHG дешевле Regent |
| **9.14** | [L'Azure](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=L%27Azure+Resort+and+Spa+Phu+Quoc) | Long Beach | 9.2 | 8.4 | $225 | высокие оценки, suite |
| **9.12** | [La Veranda MGallery](https://www.booking.com/hotel/vn/test-grand-mercure-la-veranda-phu-quoc-do-not-book.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Long Beach | 9.1 | 8.4 | $208 | колониальный бутик |
| **8.96** | [Radisson Blu](https://www.booking.com/hotel/vn/radisson-blu-resort-phu-quoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Bai Dai | 8.9 | 8.4 | **$97** | лучший value 5★ |

Полная колонка описаний и фич — в [`data/comparison.md`](data/comparison.md).

---

## Сводная таблица по цене (Agoda, живые тарифы)

Самый дешёвый доступный номер, **USD за ночь с налогами**, 2 взрослых. Ниже — ориентир; для выбора по качеству смотрите рейтинг выше.

### Популярные 5★

| Отель | Район | Рейтинг | Завтрак /10 | Ночь | 6 ночей | Номер |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| [Radisson Blu Resort](https://www.booking.com/hotel/vn/radisson-blu-resort-phu-quoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Bai Dai | 8.96 | 8.4 | **$97** | $582 | Deluxe King/Twin |
| [Vinpearl Resort & Spa](https://www.booking.com/hotel/vn/vinpearl-resort-phu-quoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Bai Dai | 8.86 | 8.4 | **$104** | $626 | Deluxe Twin |
| [Mövenpick Resort Waverly](https://www.booking.com/hotel/vn/movenpick-resort-waverly-phu-quoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Ong Lang | 8.82 | 8.5 | **$105** | $628 | Superior Twin Garden |
| [Novotel Phu Quoc](https://www.booking.com/hotel/vn/novotel-phu-quoc-resort.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Long Beach | 8.75 | 8.0 | **$111** | $667 | Superior Twin Garden |
| [Wyndham Grand](https://www.booking.com/hotel/vn/wyndham-grand-phuquoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Bai Dai | 8.68 | 8.2 | **$115** | $689 | Superior Twin |
| [Sheraton Long Beach](https://www.booking.com/hotel/vn/sheraton-phu-quoc-long-beach-resort.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Bai Dai | 8.80 | 8.0 | **$129** | $775 | Deluxe Twin Garden |
| [Pullman Beach Resort](https://www.booking.com/hotel/vn/pullman-phu-quoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Long Beach | 8.93 | 8.5 | **$139** | $833 | Superior Twin |
| [Premier Residences Emerald Bay](https://www.booking.com/hotel/vn/premier-residences-phu-quoc-emerald-bay.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Bai Khem | 8.80 | 8.3 | **$157** | $943 | Superior Suite |
| [La Veranda MGallery](https://www.booking.com/hotel/vn/test-grand-mercure-la-veranda-phu-quoc-do-not-book.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Long Beach | 9.12 | 8.4 | **$208** | $1 249 | Deluxe Garden (завтрак не в дешёвом тарифе) |
| [Salinda Resort](https://www.booking.com/hotel/vn/salinda-premium-resort-and-spa.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Long Beach | 9.45 | **9.1** | **$210** | $1 259 | Deluxe |
| [New World Phu Quoc](https://www.booking.com/hotel/vn/new-world-phu-quoc-resort-kien-giang.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Bai Khem | 8.86 | 8.6 | **$252** | $1 512 | Garden Pool Villa 1BR |
| [InterContinental Long Beach](https://www.booking.com/hotel/vn/intercontinental-hotels-phu-quoc-long-beach-resort.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Long Beach | 9.24 | **9.3** | **$264** | $1 585 | Classic / 1BR Residence |
| [Premier Village (вилла 3BR)](https://www.booking.com/hotel/vn/premier-village-phu-quoc-resort.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Bai Khem | 8.76 | 8.5 | **$306** | $1 837 | 3BR Garden Villa + pool |
| [Meliá Vinpearl (вилла 1BR)](https://www.booking.com/hotel/vn/melia-vinpearl-phu-quoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Bai Dai | 8.69 | 8.3 | **$314** | $1 887 | 1BR Lake Villa + pool |
| [JW Marriott Emerald Bay](https://www.booking.com/hotel/vn/jw-marriott-phu-quoc-emerald-bay-resort-spa.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Bai Khem | 9.28 | **9.2** | **$459** | $2 753 | Guest room King, balcony |
| [Regent Phu Quoc](https://www.booking.com/hotel/vn/regent-phu-quoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Starbay | 9.56 | **9.5** | **$500** | $3 003 | Resort View Suite |
| [Fusion Resort (spa inclusive)](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=Fusion+Resort+Phu+Quoc) | Vung Bau | 8.86 | 8.7 | нет тарифа | — | виллы не продаются на даты |

### Менее известные и средний сегмент (выборка)

| Отель | Район | Рейтинг | Завтрак /10 | Ночь | Комментарий |
| --- | --- | ---: | ---: | ---: | --- |
| [An Phu Hotel](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=An+Phu+Hotel+Phu+Quoc) | Duong Dong | 8.66 | 7.5 | **$33** | город, завтрак |
| [Muong Thanh Luxury](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=Muong+Thanh+Luxury+Phu+Quoc) | Long Beach | 7.95 | 7.4 | **$50** | сеть, value |
| [Paralia Khem Beach](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=Paralia+Khem+Beach+Phu+Quoc) | Bai Khem | 8.46 | 7.8 | **$84** | восток, белый песок |
| [Famiana Resort & Spa](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=Famiana+Resort+%26+Spa+Phu+Quoc) | Long Beach | 8.66 | 7.7 | **$94** | семьи, mid-range |
| [Crowne Plaza Starbay](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=Crowne+Plaza+Phu+Quoc+Starbay) | Starbay | 9.18 | 8.7 | **$146** | IHG, новый |
| [Chen Sea / The Slate](https://www.booking.com/hotel/vn/chen-sea-resort-spa.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Ong Lang | 8.70 | 7.7 | **$201** | beach villa |
| [Cassia Cottage](https://www.booking.com/hotel/vn/cassia-cottage.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Long Beach | 8.96 | 8.1 | **$224** | бунгало в саду |
| [Dusit Princess Moonrise](https://www.booking.com/hotel/vn/dusit-princess-moonrise-beach-resort.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | Long Beach | 9.24 | 8.8 | **$247** | junior suite |

---

## Сравнение площадок

Один и тот же отель на разных сайтах легко расходится на **15–30%**. Что получилось 22.08.2026:

| Отель | Agoda live (наши даты) | Другие площадки | Вывод |
| --- | ---: | --- | --- |
| [JW Marriott](https://www.booking.com/hotel/vn/jw-marriott-phu-quoc-emerald-bay-resort-spa.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | **$459** all-in | Google: типично **$188–366**, «типично $310»; Traveloka **$358** с налогами; официальный Marriott **$356**; Kayak «from $239», сентябрь — самый дешёвый месяц (~$314) | **Agoda дороже бренда.** Сверить Marriott.com и Traveloka перед бронью. |
| [InterContinental](https://www.booking.com/hotel/vn/intercontinental-hotels-phu-quoc-long-beach-resort.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | **$264** | Google sponsored official **$200**; Agoda средний по отелю ~$216 | Прямой IHG может быть дешевле. |
| [Vinpearl Resort & Spa](https://www.booking.com/hotel/vn/vinpearl-resort-phu-quoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | **$104** | Google typical **$61**; Booking **$93**; official **$101**; Kayak **$69** | Booking/Kayak выглядят дешевле Agoda. |
| [Wyndham Grand](https://www.booking.com/hotel/vn/wyndham-grand-phuquoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | **$115** | Google/Expedia **$113** | Совпадает. |
| [Radisson Blu](https://www.booking.com/hotel/vn/radisson-blu-resort-phu-quoc.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB) | **$97** | Google nearby **$72–77** (другие даты) | Ориентир low-season 5★ ~$80–100. |
| [Fusion](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=Fusion+Resort+Phu+Quoc) | нет мест | Google: «call for rates»; типично **$180–350**/вилла, spa included | На октябрь 2026 пока не открыт продажами на Agoda. |
| [Muong Thanh](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=Muong+Thanh+Luxury+Phu+Quoc) | **$50** | Google/HotelsCombined **$78** | Agoda выгоднее. |
| [WorldHotels Long Beach](https://www.booking.com/searchresults.html?checkin=2026-10-19&checkout=2026-10-25&group_adults=2&no_rooms=1&group_children=0&selected_currency=RUB&ss=WorldHotels+Long+Beach+Resort+Phu+Quoc) | **$247** | Google/Booking **$100**; Kayak from **£43** | Сильный разброс: проверить категорию номера. |

**Booking.com, Expedia, Hotels.com, Marriott.com, IHG, Accor, Traveloka, Tripadvisor** с сервера без браузера отдают WAF/403/429. Живые датированные цены удалось стабильно снять только с **Agoda**. Google Hotels и Kayak дали полезные **ориентиры и кросс-чек**.

Гайд VietnamSpot (июль 2026): в низкий сезон (май–окт) 5★ от ~$59, люкс JW/InterContinental от ~$200; в высокий сезон 5★ от ~$200, люкс от ~$400. Наши даты попадают в **конец низкого сезона**.

---

## По районам (что выбирать в октябре)

| Район | Кому | Море в октябре | Примеры из таблицы |
| --- | --- | --- | --- |
| **Bai Khem / Bai Sao** (восток-юг) | кто едет купаться | обычно спокойнее | Paralia $84, Premier Residences $157, New World $252, JW $459 |
| **Long Beach** (запад) | первый визит, закаты, рестораны | волны / мутнее вода | Famiana $94, Novotel $111, Pullman $139, Salinda $210, InterContinental $264 |
| **Bai Dai / Ganh Dau** (север) | семьи, VinWonders, Safari | западный берег | Radisson $97, Vinpearl $104, Wyndham $115, Sheraton $129 |
| **Ong Lang** | тихо, пары | запад, спокойнее толпы | Mövenpick $105, Mango Bay $168, Chen Sea $201 |
| **Duong Dong** | бюджет, еда, ночной рынок | пляж не у дверей | An Phu $33, Praha $67 |
| **Vung Bau** | уединение, виллы | северо-запад | Bamboo $69; Fusion/Nam Nghi — нет тарифа |

---

## Практические замечания

- В таблице — **самый дешёвый** номер. У Premier Village, Meliá, Sailing Club, Seashells, Sunset Sanato дешёвая категория — это **вилла/сьют**, не стандарт.
- Колонка **«Завтрак /10»** — качество (не «включён ли»); «в тарифе» отдельно. Salinda / Regent / InterContinental / JW лидируют по завтраку.
- Бесплатная отмена есть не везде: у Radisson, Novotel, Famiana, Pullman, Salinda дешёвый тариф часто **non-refundable**.
- Трансфер в Bai Khem ~40 мин от аэропорта, ~$15–20; Long Beach ближе (~10–15 мин).
- Прямая бронь у мелких отелей иногда бьёт OTA (комиссия 15–18%). У сетей (Marriott, IHG, Accor, Vinpearl) прямой сайт чаще даёт **апгрейд/поздний выезд**, не всегда меньшую цену — но у JW Marriott прямой сайт как раз может быть дешевле Agoda.
- Курс ориентир VietnamSpot июль 2026: **~26 000 ₫ = $1**. $100 ≈ 2,6 млн ₫.

---

## Как обновить цены и рейтинги

```bash
python3 scripts/fetch_agoda_prices.py --checkin 2026-10-19 --checkout 2026-10-25
python3 scripts/fetch_hotel_profiles.py   # отзывы, категории, фичи
python3 scripts/build_tables.py
```

Нужен `requests`. Список отелей: `scripts/hotels_catalog.py`. Описания и база оценки завтрака: `scripts/hotel_profiles.py`. Локации Grand World / Safari / аквапарк / море / центр: `scripts/hotel_pois.py`. Проверка: `python3 scripts/test_hotel_pois.py`.

---

## Файлы

| Файл | Зачем |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | правила для агентов |
| [`memory/trip.md`](memory/trip.md) | даты, гости, допущения |
| [`memory/sources.md`](memory/sources.md) | какие сайты отвечали |
| [`memory/picks.md`](memory/picks.md) | короткие рекомендации |
| [`data/comparison.md`](data/comparison.md) | полная таблица + районы + блок локаций (Grand World / Safari / аквапарк) |
| [`data/comparison.csv`](data/comparison.csv) | то же в Excel |
| [`data/hotel-profiles.json`](data/hotel-profiles.json) | рейтинг, завтрак, описание |
| [`data/hotel-profiles-raw.json`](data/hotel-profiles-raw.json) | сырые отзывы/фичи Agoda |
| [`data/agoda-live.json`](data/agoda-live.json) | сырой снимок тарифов |
| [`scripts/fetch_agoda_prices.py`](scripts/fetch_agoda_prices.py) | обновить Agoda |
| [`scripts/fetch_hotel_profiles.py`](scripts/fetch_hotel_profiles.py) | обновить отзывы/фичи |
| [`scripts/build_tables.py`](scripts/build_tables.py) | собрать таблицы |
| [`scripts/booking_links.py`](scripts/booking_links.py) | ссылки Booking.com на даты поездки |
| [`scripts/test_booking_links.py`](scripts/test_booking_links.py) | проверки ссылок Booking |
| [`scripts/hotel_profiles.py`](scripts/hotel_profiles.py) | описания + оценка завтрака |
| [`scripts/hotel_pois.py`](scripts/hotel_pois.py) | Grand World, Safari, аквапарк, стиль номера, море, центр |
| [`scripts/test_hotel_pois.py`](scripts/test_hotel_pois.py) | проверки локаций |
