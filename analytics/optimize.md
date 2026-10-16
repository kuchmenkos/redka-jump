# Баланс Редька Джамп

Другий шар аналітики — **не «скільки зайшло»**, а **як грається і що крутити**. Живі цифри збирає PostHog EU. Цей файл імпортуй у чат Cursor (`@analytics/optimize.md`), коли треба підкрутити механіки по даних, а не навмання.

Живі дашборди (PostHog EU, проєкт redkajump, період 30 днів):

- [Як грають](https://eu.posthog.com/project/307751/dashboard/1027950) — KPI, медіани, воронки, Threads
- [Баланс](https://eu.posthog.com/project/307751/dashboard/1027951) — секції: наскільки важко → чим кінчають → етапи → бонуси → прогрес

MCP у Cloud Agent не логіниться. SQL нижче — якщо треба свіжий знімок у чат Cursor.

## Два шари

1. **Гра → PostHog** — події в `index.html` (`ph()`).
2. **Цей файл + canvas у Cursor** — рішення по балансу. Після хвилі трафіку встав знімок з SQL у чат і скажи «оптимізуй по цьому».

## Події

| Подія | Навіщо для балансу |
|---|---|
| `play_start` | `from` cta/again, `look`, `returning` |
| `game_over` | знімок катки: `duration_s`, `score`, `zone`, `cause`, механіки |
| `run_abandon` | вихід з паузи (`cause=quit`) або закрита вкладка посеред забігу (`cause=closed`); багато vs смерті — здаються, не вмирають |
| `hater_met` | вперше зустрінутий хейтер | 
| `lb_open` / `lb_submit` | відкрито лідерборд / відправлено імʼя |
| `dock` | кнопки дока на інтро (`btn`: achs, ward, help) |
| `zone_enter` | де відвалюються |
| `express` / `gordon` / `ticket` / `stomp` | чи бонуси взагалі трапляються |
| `look_buy` / `look_wear` / `ach` | чи гардероб живе |
| `share` | чи є чим хвалитись |
| `threads_click` | чіп у «Про гру» |

`game_over` / `run_abandon` поля: `cause`, `score`, `zone`, `zone_idx`, `duration_s` (без паузи), `wall_s`, `look`, `tickets`, `express`, `gordon` (caught/missed/none), `stomps`, `stomp_*`, `combo_max`, `minus`, `fakes`, `threads`, `labels`, `idle_s`, `record`, `million`, `pauses`.

## Пороги в коді (орієнтири)

| Що | Поріг |
|---|---|
| Львів, перший хейтер | 60 000 |
| Князь | 140 000 |
| Суджа | 240 000 |
| Київ | 370 000 |
| Одіссея | 530 000 |
| Стадіон | 750 000 |
| Експрес | 60 000, кулдаун 50 000, ~5–9% |
| Гордон | 300 000, 34%, один раз |
| Квитки | ~12 000 |
| Хейтерів на екрані | 1 / 2 / 3 / 4 після 60k, 140k, 280k, 550k |

## Як читати «легко vs складно»

Бери **медіану**, не середнє (мільйонники тягнуть середнє).

- **Заскладно:** p50 `score` < 40k (не бачать Стукача); p50 `duration_s` < 25 с; >55% `cause=fall` на Сумах; багато `run_abandon` на Сумах.
- **Залегко:** p50 `score` > 250k; >15% забігів з `zone_enter` на Одіссею; мало смертей від хейтерів.
- **Львів ріже:** багато `cause=stuk` або `lang` одразу після 60k — щілина / кап хейтерів.
- **Бонуси не чіпляють:** серед забігів зі `score` ≥ 60k частка `express` < 20%; на ≥ 300k `gordon=none` або майже всі `missed`.
- **Немає сенсу шерити:** `share` / `game_over` < 5%.
- **Threads:** `threads_click` / унікальні `pageview` — окремо від ігрової складності.

## SQL (вставити в PostHog EU → SQL)

Медіани за 7 днів:

```sql
SELECT
  quantile(0.5)(toFloat(properties.score)) AS p50_score,
  quantile(0.9)(toFloat(properties.score)) AS p90_score,
  quantile(0.5)(toFloat(properties.duration_s)) AS p50_duration_s,
  quantile(0.9)(toFloat(properties.duration_s)) AS p90_duration_s,
  count() AS runs
FROM events
WHERE event = 'game_over' AND timestamp > now() - interval 7 day
```

Чим кінчають:

```sql
SELECT if(event = 'run_abandon', 'quit', toString(properties.cause)) AS end, count() n
FROM events
WHERE event IN ('game_over', 'run_abandon') AND timestamp > now() - interval 7 day
GROUP BY 1 ORDER BY n DESC
```

Де відвалюються (max-зона фіналу):

```sql
SELECT toString(properties.zone) AS zone, count() n
FROM events
WHERE event = 'game_over' AND timestamp > now() - interval 7 day
GROUP BY 1 ORDER BY n DESC
```

Воронка етапів:

```sql
SELECT
  countIf(event = 'play_start') AS starts,
  countIf(event = 'zone_enter' AND properties.zone_idx = '1') AS lviv,
  countIf(event = 'zone_enter' AND properties.zone_idx = '3') AS sudzha,
  countIf(event = 'zone_enter' AND properties.zone_idx = '4') AS kyiv,
  countIf(event = 'zone_enter' AND properties.zone_idx = '5') AS odyssey,
  countIf(event = 'zone_enter' AND properties.zone_idx = '6') AS stadium
FROM events
WHERE timestamp > now() - interval 7 day
```

Гордон / експрес / Threads / шеринг:

```sql
SELECT
  countIf(event = 'play_start') AS starts,
  countIf(event = 'express') AS express,
  countIf(event = 'gordon' AND properties.result = 'caught') AS gordon_caught,
  countIf(event = 'gordon' AND properties.result = 'missed') AS gordon_missed,
  countIf(event = 'share') AS shares,
  countIf(event = 'threads_click') AS threads_clicks
FROM events
WHERE timestamp > now() - interval 7 day
```

## Знімок для Cursor

Після SQL скопіюй таблиці в чат і напиши: оптимізуй баланс по цьому знімку, тримай Гордона / квитки / гардероб / сплеш. Агент має змінювати пороги в `index.html` (`ZONES[].from`, щілина в `genStep`, `EPOOL` / кап хейтерів, `EXPRESS_*`, `GORDON_P`), не вигадувати механіки.
